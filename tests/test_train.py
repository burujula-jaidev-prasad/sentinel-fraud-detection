"""Tests for model training pipeline."""

import os
import joblib
import pandas as pd
import pytest
from src.train import train_and_evaluate_splits


def test_train_model_pipeline(tmp_path):
    # Create a mock dataset
    data = {
        "step": list(range(1, 101)),
        "type": ["TRANSFER" if i % 2 == 0 else "CASH_OUT" for i in range(1, 101)],
        "amount": [float(i * 100) for i in range(1, 101)],
        "isFraud": [1 if i % 10 == 0 else 0 for i in range(1, 101)],
    }
    csv_file = tmp_path / "mock_paysim.csv"
    pd.DataFrame(data).to_csv(csv_file, index=False)

    model_file = tmp_path / "models" / "rf.pkl"

    rf, results_table = train_and_evaluate_splits(
        data_path=str(csv_file),
        model_output_path=str(model_file),
        n_estimators=10,
        random_state=42,
    )

    assert os.path.exists(model_file)
    assert "Primary (75th Percentile, <=333)" in results_table
    assert "calendar_time_split (<=556.8)" in results_table

    for split_name, metrics in results_table.items():
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1" in metrics
        assert "pr_auc" in metrics
        assert "roc_auc" in metrics

    loaded_model = joblib.load(str(model_file))
    assert hasattr(loaded_model, "predict")
