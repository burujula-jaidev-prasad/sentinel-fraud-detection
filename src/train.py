"""Random Forest model training, persistence, and multi-split evaluation pipeline."""

import argparse
import os
import sys
import joblib

# Ensure project root is in Python module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sklearn.ensemble import RandomForestClassifier

from src.data_loader import load_and_filter_data, split_by_percentile, split_by_calendar_time
from src.features import prepare_feature_target_split
from src.evaluate import compute_metrics, print_comparison_table


def train_and_evaluate_splits(
    data_path: str = "data/paysim_sample.csv",
    model_output_path: str = "models/rf.pkl",
    n_estimators: int = 200,
    min_samples_leaf: int = 5,
    class_weight: str = "balanced_subsample",
    random_state: int = 42,
    n_jobs: int = -1,
):
    """
    Executes the training and multi-split evaluation pipeline:
    1. Loads dataset and filters only TRANSFER and CASH_OUT records.
    2. Primary Split (75th Percentile Step Split):
       - Train: step <= 333 (312,371 rows, 549 frauds)
       - Test:  step > 333  (103,191 rows, 652 frauds)
       - Fits RandomForestClassifier with balanced_subsample weights, saves artifact to models/rf.pkl, and computes metrics.
    3. Secondary Split (Calendar Time Split):
       - Train: step <= 556.8 (403,217 rows, 900 frauds)
       - Test:  step > 556.8  (12,345 rows, 301 frauds)
       - Fits RandomForestClassifier and computes metrics.
    4. Prints Precision, Recall, F1, PR-AUC, and ROC-AUC for both splits in a single table.
    """
    print(f"Loading and filtering transactions from: {data_path}")
    df = load_and_filter_data(data_path)
    print(f"Total TRANSFER & CASH_OUT records: {len(df):,} (Total frauds: {df['isFraud'].sum():,})\n")

    results_table = {}

    # -------------------------------------------------------------
    # 1. Primary Split: 75th Percentile Step Split (step <= 333)
    # -------------------------------------------------------------
    print("=" * 65)
    print(" 1. PRIMARY SPLIT: 75th Percentile Step Split (step <= 333)")
    print("=" * 65)
    train_p, test_p, cutoff_p = split_by_percentile(df, percentile=75.0)
    print(f"Cutoff Step: {cutoff_p:.1f}")
    print(f"Train set: {len(train_p):,} rows ({train_p['isFraud'].sum():,} frauds | {train_p['isFraud'].mean():.4%})")
    print(f"Test set:  {len(test_p):,} rows ({test_p['isFraud'].sum():,} frauds | {test_p['isFraud'].mean():.4%})")

    X_train_p, y_train_p = prepare_feature_target_split(train_p)
    X_test_p, y_test_p = prepare_feature_target_split(test_p)

    print(f"\nTraining Primary RandomForestClassifier (n_estimators={n_estimators}, min_samples_leaf={min_samples_leaf}, class_weight='{class_weight}')...")
    rf_primary = RandomForestClassifier(
        n_estimators=n_estimators,
        min_samples_leaf=min_samples_leaf,
        class_weight=class_weight,
        random_state=random_state,
        n_jobs=n_jobs,
    )
    rf_primary.fit(X_train_p, y_train_p)

    # Save primary model to models/rf.pkl
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(rf_primary, model_output_path)
    print(f"Primary model successfully saved to: {model_output_path}")

    # Evaluate Primary Model
    y_pred_p = rf_primary.predict(X_test_p)
    y_prob_p = rf_primary.predict_proba(X_test_p)[:, 1]
    metrics_primary = compute_metrics(y_test_p, y_pred_p, y_prob_p)
    results_table["Primary (75th Percentile, <=333)"] = metrics_primary

    # -------------------------------------------------------------
    # 2. Secondary Split: Calendar Time Split (step <= 556.8)
    # -------------------------------------------------------------
    print("\n" + "=" * 65)
    print(" 2. SECONDARY SPLIT: calendar_time_split (step <= 556.8)")
    print("=" * 65)
    train_c, test_c, cutoff_c = split_by_calendar_time(df, train_ratio=0.75)
    print(f"Cutoff Step: {cutoff_c:.1f}")
    print(f"Train set: {len(train_c):,} rows ({train_c['isFraud'].sum():,} frauds | {train_c['isFraud'].mean():.4%})")
    print(f"Test set:  {len(test_c):,} rows ({test_c['isFraud'].sum():,} frauds | {test_c['isFraud'].mean():.4%})")

    X_train_c, y_train_c = prepare_feature_target_split(train_c)
    X_test_c, y_test_c = prepare_feature_target_split(test_c)

    print(f"\nTraining Calendar Time RandomForestClassifier (n_estimators={n_estimators}, min_samples_leaf={min_samples_leaf}, class_weight='{class_weight}')...")
    rf_calendar = RandomForestClassifier(
        n_estimators=n_estimators,
        min_samples_leaf=min_samples_leaf,
        class_weight=class_weight,
        random_state=random_state,
        n_jobs=n_jobs,
    )
    rf_calendar.fit(X_train_c, y_train_c)

    # Evaluate Calendar Time Model
    y_pred_c = rf_calendar.predict(X_test_c)
    y_prob_c = rf_calendar.predict_proba(X_test_c)[:, 1]
    metrics_calendar = compute_metrics(y_test_c, y_pred_c, y_prob_c)
    results_table["calendar_time_split (<=556.8)"] = metrics_calendar

    # -------------------------------------------------------------
    # 3. Print Combined Performance Table
    # -------------------------------------------------------------
    print_comparison_table(results_table)

    return rf_primary, results_table


# Alias for backward compatibility
train_model = train_and_evaluate_splits


def main():
    parser = argparse.ArgumentParser(description="Train Random Forest fraud detection model with multi-split evaluation.")
    parser.add_argument(
        "--data_path",
        type=str,
        default="data/paysim_sample.csv",
        help="Path to the PaySim dataset CSV file.",
    )
    parser.add_argument(
        "--model_output_path",
        type=str,
        default="models/rf.pkl",
        help="Path where trained model artifact will be saved.",
    )
    parser.add_argument(
        "--n_estimators",
        type=int,
        default=200,
        help="Number of trees in the Random Forest.",
    )
    parser.add_argument(
        "--min_samples_leaf",
        type=int,
        default=5,
        help="Minimum samples per leaf node.",
    )
    parser.add_argument(
        "--class_weight",
        type=str,
        default="balanced_subsample",
        help="Class weight balancing strategy.",
    )
    parser.add_argument(
        "--random_state",
        type=int,
        default=42,
        help="Random seed for reproducibility.",
    )

    args = parser.parse_args()
    train_and_evaluate_splits(
        data_path=args.data_path,
        model_output_path=args.model_output_path,
        n_estimators=args.n_estimators,
        min_samples_leaf=args.min_samples_leaf,
        class_weight=args.class_weight,
        random_state=args.random_state,
    )


if __name__ == "__main__":
    main()
