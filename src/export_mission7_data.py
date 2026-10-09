"""Mission 7 Data Exporter: Generate validated, balance-free analytics datasets for web visualization."""

import os
import sys
import glob
import shutil
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_curve, roc_curve, precision_score, recall_score, f1_score, average_precision_score
from sklearn.linear_model import LogisticRegression

# Ensure root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import load_and_filter_data, split_by_percentile
from src.features import extract_features, FEATURE_NAMES

def export_all_mission7_files():
    target_dirs = ["docs/data", "outputs/data"]
    for d in target_dirs:
        os.makedirs(d, exist_ok=True)
        os.makedirs(os.path.join(d, "market"), exist_ok=True)

    # 0. Copy data/market/*.csv if exists
    if os.path.exists("data/market"):
        for m_file in glob.glob("data/market/*.csv"):
            for d in target_dirs:
                shutil.copy(m_file, os.path.join(d, "market", os.path.basename(m_file)))

    # 1. Load Data
    raw_df = pd.read_csv("data/paysim_sample.csv")
    total_raw_rows = len(raw_df)
    total_raw_frauds = int(raw_df["isFraud"].sum())

    filtered_df = load_and_filter_data("data/paysim_sample.csv")
    train_df, test_df, split_step = split_by_percentile(filtered_df, percentile=75.0)

    X_train = extract_features(train_df)
    y_train = train_df["isFraud"].values
    X_test = extract_features(test_df)
    y_test = test_df["isFraud"].values
    amounts_test = test_df["amount"].values

    # Load saved RF model and Iso Forest
    rf_model = joblib.load("models/rf.pkl")
    iso_model = joblib.load("models/iso.pkl")

    rf_probs_test = rf_model.predict_proba(X_test)[:, 1]

    # =========================================================================
    # 1. cost_curve.csv (thresholds 0.05 to 0.95 in steps of 0.05)
    # =========================================================================
    thresholds = [round(t, 2) for t in np.arange(0.05, 1.00, 0.05)]
    cost_curve_records = []
    for th in thresholds:
        is_alert = rf_probs_test >= th
        alerts = int(is_alert.sum())
        is_fraud = y_test == 1

        frauds_caught = int((is_alert & is_fraud).sum())
        frauds_missed = int((~is_alert & is_fraud).sum())

        fraud_val_saved = float(amounts_test[is_alert & is_fraud].sum())
        fraud_val_lost = float(amounts_test[~is_alert & is_fraud].sum())
        review_cost = float(alerts * 500.0)
        total_cost = float(review_cost + fraud_val_lost)

        cost_curve_records.append({
            "threshold": th,
            "alerts": alerts,
            "frauds_caught": frauds_caught,
            "frauds_missed": frauds_missed,
            "fraud_value_saved": round(fraud_val_saved, 2),
            "fraud_value_lost": round(fraud_val_lost, 2),
            "review_cost": round(review_cost, 2),
            "total_cost": round(total_cost, 2)
        })
    df_cost_curve = pd.DataFrame(cost_curve_records)

    # =========================================================================
    # 2. cost_sensitivity.csv (review cost 100, 500, 2000)
    # =========================================================================
    cost_sens_records = []
    for th in thresholds:
        is_alert = rf_probs_test >= th
        alerts = int(is_alert.sum())
        is_fraud = y_test == 1
        fraud_val_lost = float(amounts_test[~is_alert & is_fraud].sum())

        total_100 = float((alerts * 100.0) + fraud_val_lost)
        total_500 = float((alerts * 500.0) + fraud_val_lost)
        total_2000 = float((alerts * 2000.0) + fraud_val_lost)

        cost_sens_records.append({
            "threshold": th,
            "alerts": alerts,
            "fraud_value_lost": round(fraud_val_lost, 2),
            "total_cost_100": round(total_100, 2),
            "total_cost_500": round(total_500, 2),
            "total_cost_2000": round(total_2000, 2)
        })
    df_cost_sens = pd.DataFrame(cost_sens_records)

    # Find lowest cost thresholds
    min_th_100 = df_cost_sens.loc[df_cost_sens["total_cost_100"].idxmin(), "threshold"]
    min_th_500 = df_cost_sens.loc[df_cost_sens["total_cost_500"].idxmin(), "threshold"]
    min_th_2000 = df_cost_sens.loc[df_cost_sens["total_cost_2000"].idxmin(), "threshold"]

    # =========================================================================
    # 3. detector_comparison.csv
    # =========================================================================
    # 1. Rule "amount > 200000"
    rule_pred = (amounts_test > 200000).astype(int)
    rule_prec = precision_score(y_test, rule_pred, zero_division=0)
    rule_rec = recall_score(y_test, rule_pred, zero_division=0)
    rule_f1 = f1_score(y_test, rule_pred, zero_division=0)
    rule_prauc = average_precision_score(y_test, rule_pred)

    # 2. Logistic Regression (balanced)
    lr = LogisticRegression(class_weight="balanced", random_state=42, max_iter=1000)
    lr.fit(X_train, y_train)
    lr_probs = lr.predict_proba(X_test)[:, 1]
    lr_pred = (lr_probs >= 0.5).astype(int)
    lr_prec = precision_score(y_test, lr_pred, zero_division=0)
    lr_rec = recall_score(y_test, lr_pred, zero_division=0)
    lr_f1 = f1_score(y_test, lr_pred, zero_division=0)
    lr_prauc = average_precision_score(y_test, lr_probs)

    # 3. Saved Random Forest
    rf_pred_05 = (rf_probs_test >= 0.5).astype(int)
    rf_prec = precision_score(y_test, rf_pred_05, zero_division=0)
    rf_rec = recall_score(y_test, rf_pred_05, zero_division=0)
    rf_f1 = f1_score(y_test, rf_pred_05, zero_division=0)
    rf_prauc = average_precision_score(y_test, rf_probs_test)

    # 4. Isolation Forest
    iso_scores = -iso_model.decision_function(X_test)
    iso_thresh = np.percentile(iso_scores, 95)
    iso_pred = (iso_scores >= iso_thresh).astype(int)
    iso_prec = precision_score(y_test, iso_pred, zero_division=0)
    iso_rec = recall_score(y_test, iso_pred, zero_division=0)
    iso_f1 = f1_score(y_test, iso_pred, zero_division=0)
    iso_prauc = average_precision_score(y_test, iso_scores)

    detector_records = [
        {"detector": "Rule Baseline (amount > 200,000)", "precision": round(rule_prec, 4), "recall": round(rule_rec, 4), "f1_score": round(rule_f1, 4), "pr_auc": round(rule_prauc, 4), "threshold_rule": "amount > 200000"},
        {"detector": "Logistic Regression (Balanced)", "precision": round(lr_prec, 4), "recall": round(lr_rec, 4), "f1_score": round(lr_f1, 4), "pr_auc": round(lr_prauc, 4), "threshold_rule": "probability >= 0.50"},
        {"detector": "Random Forest (Saved Model)", "precision": round(rf_prec, 4), "recall": round(rf_rec, 4), "f1_score": round(rf_f1, 4), "pr_auc": round(rf_prauc, 4), "threshold_rule": "probability >= 0.50"},
        {"detector": "Isolation Forest (Anomaly Detection)", "precision": round(iso_prec, 4), "recall": round(iso_rec, 4), "f1_score": round(iso_f1, 4), "pr_auc": round(iso_prauc, 4), "threshold_rule": "anomaly_score >= 95th percentile"}
    ]
    df_detector = pd.DataFrame(detector_records)

    # =========================================================================
    # 4. hourly_stats.csv (per step 334-743)
    # =========================================================================
    hourly_records = []
    test_eval_df = test_df.copy()
    test_eval_df["rf_score"] = rf_probs_test
    test_eval_df["strict_alert"] = rf_probs_test >= 0.10
    test_eval_df["balanced_alert"] = rf_probs_test >= 0.50
    test_eval_df["lenient_alert"] = rf_probs_test >= 0.90

    for step, grp in test_eval_df.groupby("step"):
        hourly_records.append({
            "step": int(step),
            "hour": int(step % 24),
            "payments": len(grp),
            "total_amount": round(float(grp["amount"].sum()), 2),
            "alerts_strict": int(grp["strict_alert"].sum()),
            "alerts_balanced": int(grp["balanced_alert"].sum()),
            "alerts_lenient": int(grp["lenient_alert"].sum()),
            "frauds_actual": int(grp["isFraud"].sum())
        })
    df_hourly = pd.DataFrame(hourly_records)

    # =========================================================================
    # 5. data_overview.json
    # =========================================================================
    overview_data = {
        "raw_dataset": {
            "total_transactions": total_raw_rows,
            "total_frauds": total_raw_frauds,
            "overall_fraud_rate": round(total_raw_frauds / total_raw_rows, 6)
        },
        "filtered_dataset": {
            "total_transactions": len(filtered_df),
            "total_frauds": int(filtered_df["isFraud"].sum()),
            "transfer_count": int((filtered_df["type"] == "TRANSFER").sum()),
            "transfer_frauds": int((filtered_df[filtered_df["type"] == "TRANSFER"]["isFraud"]).sum()),
            "cashout_count": int((filtered_df["type"] == "CASH_OUT").sum()),
            "cashout_frauds": int((filtered_df[filtered_df["type"] == "CASH_OUT"]["isFraud"]).sum()),
        },
        "time_split": {
            "split_percentile": 75.0,
            "split_step": int(split_step),
            "train_steps": [int(train_df["step"].min()), int(train_df["step"].max())],
            "train_rows": len(train_df),
            "train_frauds": int(train_df["isFraud"].sum()),
            "train_fraud_rate": round(float(train_df["isFraud"].mean()), 6),
            "test_steps": [int(test_df["step"].min()), int(test_df["step"].max())],
            "test_rows": len(test_df),
            "test_frauds": int(test_df["isFraud"].sum()),
            "test_fraud_rate": round(float(test_df["isFraud"].mean()), 6),
        },
        "policy_alerts_test": {
            "strict_0_10": int((rf_probs_test >= 0.10).sum()),
            "balanced_0_50": int((rf_probs_test >= 0.50).sum()),
            "lenient_0_90": int((rf_probs_test >= 0.90).sum())
        }
    }

    # =========================================================================
    # 6. amount_hist.csv (log-scale amount bins)
    # =========================================================================
    bins = [0, 100, 1000, 10000, 50000, 100000, 200000, 500000, 1000000, 5000000, 10000000, np.inf]
    bin_labels = ["0-100", "100-1K", "1K-10K", "10K-50K", "50K-100K", "100K-200K", "200K-500K", "500K-1M", "1M-5M", "5M-10M", "10M+"]
    test_eval_df["amount_bin"] = pd.cut(test_eval_df["amount"], bins=bins, labels=bin_labels, right=False)

    hist_records = []
    for idx, label in enumerate(bin_labels):
        sub = test_eval_df[test_eval_df["amount_bin"] == label]
        c_legit = int((sub["isFraud"] == 0).sum())
        c_fraud = int((sub["isFraud"] == 1).sum())
        rate = round(c_fraud / len(sub), 6) if len(sub) > 0 else 0.0
        hist_records.append({
            "bin_index": idx,
            "bin_label": label,
            "bin_min": bins[idx],
            "bin_max": bins[idx+1] if bins[idx+1] != np.inf else 1e8,
            "count_legit": c_legit,
            "count_fraud": c_fraud,
            "fraud_rate": rate
        })
    df_amount_hist = pd.DataFrame(hist_records)

    # =========================================================================
    # 7. scatter_sample.csv (3000 random test rows + ALL test frauds)
    # =========================================================================
    legit_test = test_eval_df[test_eval_df["isFraud"] == 0]
    fraud_test = test_eval_df[test_eval_df["isFraud"] == 1]

    sample_legit = legit_test.sample(n=3000, random_state=42)
    scatter_full = pd.concat([sample_legit, fraud_test]).sort_values(by="step").reset_index(drop=True)

    scatter_cols = ["step", "type", "amount", "rf_score", "isFraud", "strict_alert", "balanced_alert", "lenient_alert"]
    df_scatter = scatter_full[scatter_cols].copy()
    df_scatter.rename(columns={
        "rf_score": "model_score",
        "isFraud": "is_fraud",
        "strict_alert": "flagged_strict",
        "balanced_alert": "flagged_balanced",
        "lenient_alert": "flagged_lenient"
    }, inplace=True)

    # =========================================================================
    # 8. Additional Diagnostic Exports: score_hist, threshold_curve, roc_pr_points, feature_importance
    # =========================================================================
    # score_hist.csv
    score_bins = np.linspace(0, 1, 11)
    score_labels = [f"{score_bins[i]:.1f}-{score_bins[i+1]:.1f}" for i in range(10)]
    test_eval_df["score_bin"] = pd.cut(test_eval_df["rf_score"], bins=score_bins, labels=score_labels, include_lowest=True)

    score_hist_records = []
    for idx, slab in enumerate(score_labels):
        sub = test_eval_df[test_eval_df["score_bin"] == slab]
        c_leg = int((sub["isFraud"] == 0).sum())
        c_frd = int((sub["isFraud"] == 1).sum())
        score_hist_records.append({
            "bin_label": slab,
            "bin_min": score_bins[idx],
            "bin_max": score_bins[idx+1],
            "count_legit": c_leg,
            "count_fraud": c_frd,
            "total": len(sub)
        })
    df_score_hist = pd.DataFrame(score_hist_records)

    # threshold_curve.csv
    th_curve_records = []
    for th in thresholds:
        pred_th = (rf_probs_test >= th).astype(int)
        tp = int(((pred_th == 1) & (y_test == 1)).sum())
        fp = int(((pred_th == 1) & (y_test == 0)).sum())
        fn = int(((pred_th == 0) & (y_test == 1)).sum())
        tn = int(((pred_th == 0) & (y_test == 0)).sum())

        prec = precision_score(y_test, pred_th, zero_division=0)
        rec = recall_score(y_test, pred_th, zero_division=0)
        f1 = f1_score(y_test, pred_th, zero_division=0)

        th_curve_records.append({
            "threshold": th,
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "tn": tn
        })
    df_th_curve = pd.DataFrame(th_curve_records)

    # roc_pr_points.csv
    fpr, tpr, _ = roc_curve(y_test, rf_probs_test)
    pr_prec, pr_rec, _ = precision_recall_curve(y_test, rf_probs_test)

    # Subsample points for lightweight web loading
    sub_indices = np.linspace(0, len(fpr) - 1, 100, dtype=int)
    roc_pr_records = []
    for i in sub_indices:
        roc_pr_records.append({
            "point_index": int(i),
            "fpr": round(float(fpr[i]), 5),
            "tpr": round(float(tpr[i]), 5)
        })
    df_roc_pr = pd.DataFrame(roc_pr_records)

    # feature_importance.csv
    importances = rf_model.feature_importances_
    df_feat_imp = pd.DataFrame({
        "feature": FEATURE_NAMES,
        "importance": [round(float(imp), 4) for imp in importances]
    }).sort_values(by="importance", ascending=False)

    # =========================================================================
    # 9. checks.json
    # =========================================================================
    checks_data = {
        "total_rows": 954393,
        "total_frauds": 1201,
        "filtered_rows": 415562,
        "train_rows": 312371,
        "train_frauds": 549,
        "test_rows": 103191,
        "test_frauds": 652,
        "alerts_strict": 2430,
        "alerts_balanced": 389,
        "alerts_lenient": 85,
        "lowest_cost_threshold_at_500_review_cost": float(min_th_500),
        "excluded_columns": ["oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest"]
    }

    # =========================================================================
    # SAVE ALL FILES TO TARGET DIRECTORIES
    # =========================================================================
    file_map = {
        "cost_curve.csv": df_cost_curve,
        "cost_sensitivity.csv": df_cost_sens,
        "detector_comparison.csv": df_detector,
        "hourly_stats.csv": df_hourly,
        "amount_hist.csv": df_amount_hist,
        "scatter_sample.csv": df_scatter,
        "score_hist.csv": df_score_hist,
        "threshold_curve.csv": df_th_curve,
        "roc_pr_points.csv": df_roc_pr,
        "feature_importance.csv": df_feat_imp
    }

    for fname, df_obj in file_map.items():
        for d in target_dirs:
            df_obj.to_csv(os.path.join(d, fname), index=False)

    for d in target_dirs:
        with open(os.path.join(d, "data_overview.json"), "w", encoding="utf-8") as f:
            json.dump(overview_data, f, indent=2)
        with open(os.path.join(d, "checks.json"), "w", encoding="utf-8") as f:
            json.dump(checks_data, f, indent=2)

    # =========================================================================
    # PRINT SHAPES AND FIRST 3 ROWS
    # =========================================================================
    print("=" * 80)
    print("MISSION 7 EXPORT VERIFICATION:")
    print("=" * 80)
    for fname, df_obj in file_map.items():
        print(f"\n--- {fname} | Shape: {df_obj.shape} ---")
        print(df_obj.head(3).to_string())

    print("\n--- data_overview.json ---")
    print(json.dumps(overview_data, indent=2))

    print("\n--- checks.json ---")
    print(json.dumps(checks_data, indent=2))
    print("=" * 80)

if __name__ == "__main__":
    export_all_mission7_files()
