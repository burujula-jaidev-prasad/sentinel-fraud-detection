"""Run feature ablation study and update extended cost sensitivity curves."""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, roc_auc_score, precision_score, recall_score, f1_score

# Ensure root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import load_and_filter_data, split_by_percentile
from src.features import extract_features

def run_updates():
    # 1. Load Data
    filtered_df = load_and_filter_data("data/paysim_sample.csv")
    train_df, test_df, _ = split_by_percentile(filtered_df, percentile=75.0)

    X_train_full = extract_features(train_df)
    y_train = train_df["isFraud"].values
    X_test_full = extract_features(test_df)
    y_test = test_df["isFraud"].values
    amounts_test = test_df["amount"].values

    # Load saved RF model (read-only)
    rf_saved = joblib.load("models/rf.pkl")
    rf_probs_test = rf_saved.predict_proba(X_test_full)[:, 1]

    # =========================================================================
    # 1. Extended cost_curve.csv
    # =========================================================================
    thresholds = [0.01, 0.02, 0.03, 0.04] + [round(t, 2) for t in np.arange(0.05, 1.00, 0.05)]
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

    # Save to docs/data/ and outputs/data/
    for d in ["docs/data", "outputs/data"]:
        df_cost_curve.to_csv(os.path.join(d, "cost_curve.csv"), index=False)

    # =========================================================================
    # 2. Extended cost_sensitivity.csv (100, 500, 2000, 5000, 25000, 100000, 500000)
    # =========================================================================
    review_costs = [100, 500, 2000, 5000, 25000, 100000, 500000]
    cost_sens_records = []

    for th in thresholds:
        is_alert = rf_probs_test >= th
        alerts = int(is_alert.sum())
        is_fraud = y_test == 1
        fraud_val_lost = float(amounts_test[~is_alert & is_fraud].sum())

        row = {
            "threshold": th,
            "alerts": alerts,
            "fraud_value_lost": round(fraud_val_lost, 2),
        }
        for rc in review_costs:
            row[f"cost_{rc}"] = round(float((alerts * rc) + fraud_val_lost), 2)
        cost_sens_records.append(row)

    df_cost_sens = pd.DataFrame(cost_sens_records)

    # Compute lowest cost threshold per review cost
    lowest_row = {
        "threshold": "lowest_cost_threshold",
        "alerts": "-",
        "fraud_value_lost": "-"
    }
    lowest_threshold_dict = {}
    for rc in review_costs:
        col = f"cost_{rc}"
        min_idx = df_cost_sens[col].idxmin()
        opt_th = df_cost_sens.loc[min_idx, "threshold"]
        lowest_row[col] = opt_th
        lowest_threshold_dict[rc] = opt_th

    df_cost_sens_with_summary = pd.concat([df_cost_sens, pd.DataFrame([lowest_row])], ignore_index=True)

    for d in ["docs/data", "outputs/data"]:
        df_cost_sens_with_summary.to_csv(os.path.join(d, "cost_sensitivity.csv"), index=False)

    # =========================================================================
    # 3. Update data_overview.json (rename raw_dataset -> sample_dataset)
    # =========================================================================
    for d in ["docs/data", "outputs/data"]:
        p = os.path.join(d, "data_overview.json")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                d_json = json.load(f)
            if "raw_dataset" in d_json:
                d_json["sample_dataset"] = d_json.pop("raw_dataset")
            with open(p, "w", encoding="utf-8") as f:
                json.dump(d_json, f, indent=2)

    # =========================================================================
    # 4. Feature Ablation Study (outputs/ablation.csv only)
    # =========================================================================
    experiments = [
        ("(a) All 4 features", ["amount", "log_amount", "is_transfer", "hour"]),
        ("(b) Without hour", ["amount", "log_amount", "is_transfer"]),
        ("(c) Without log_amount", ["amount", "is_transfer", "hour"]),
        ("(d) Amount only", ["amount"]),
    ]

    ablation_records = []
    print("\nTraining feature ablation models...")

    for name, feat_list in experiments:
        X_tr = X_train_full[feat_list]
        X_te = X_test_full[feat_list]

        rf_exp = RandomForestClassifier(
            n_estimators=200,
            min_samples_leaf=5,
            class_weight="balanced_subsample",
            random_state=42,
            n_jobs=-1
        )
        rf_exp.fit(X_tr, y_train)

        probs_te = rf_exp.predict_proba(X_te)[:, 1]
        pred_05 = (probs_te >= 0.50).astype(int)

        pr_auc = average_precision_score(y_test, probs_te)
        roc_auc = roc_auc_score(y_test, probs_te)
        prec = precision_score(y_test, pred_05, zero_division=0)
        rec = recall_score(y_test, pred_05, zero_division=0)
        f1 = f1_score(y_test, pred_05, zero_division=0)

        ablation_records.append({
            "experiment": name,
            "features_used": ", ".join(feat_list),
            "num_features": len(feat_list),
            "pr_auc": round(pr_auc, 4),
            "roc_auc": round(roc_auc, 4),
            "precision_at_0_5": round(prec, 4),
            "recall_at_0_5": round(rec, 4),
            "f1_at_0_5": round(f1, 4)
        })

    df_ablation = pd.DataFrame(ablation_records)
    df_ablation.to_csv("outputs/ablation.csv", index=False)

    # =========================================================================
    # 5. Print Output Results
    # =========================================================================
    print("=" * 85)
    print("LOWEST-COST THRESHOLD PER REVIEW COST LEVEL:")
    print("=" * 85)
    df_lowest = pd.DataFrame([
        {"Review Cost (CU/alert)": f"{rc:,}", "Optimal Threshold": lowest_threshold_dict[rc], "Economic Rationale": "High alert queue justified by large saved fraud loss" if rc <= 2000 else "Higher threshold preferred as review costs escalate"}
        for rc in review_costs
    ])
    print(df_lowest.to_string(index=False))

    print("\n" + "=" * 85)
    print("FEATURE ABLATION STUDY RESULTS (Saved to outputs/ablation.csv):")
    print("=" * 85)
    print(df_ablation.to_string(index=False))
    print("=" * 85)

if __name__ == "__main__":
    run_updates()
