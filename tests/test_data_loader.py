"""Tests for data loading and time-based splitting."""

import pandas as pd
import pytest
from src.data_loader import load_and_filter_data, split_by_percentile, split_by_calendar_time


def test_split_by_percentile():
    # 4 transactions at step 10, 20, 30, 40
    data = {
        "step": [10, 20, 30, 40],
        "type": ["TRANSFER", "CASH_OUT", "TRANSFER", "CASH_OUT"],
        "amount": [100.0, 200.0, 300.0, 400.0],
        "isFraud": [0, 0, 1, 1],
    }
    df = pd.DataFrame(data)

    # 75th percentile of [10, 20, 30, 40] is 32.5
    train_df, test_df, cutoff = split_by_percentile(df, percentile=75.0)

    assert cutoff == 32.5
    assert len(train_df) == 3  # steps 10, 20, 30
    assert len(test_df) == 1   # step 40
    assert test_df.iloc[0]["step"] == 40


def test_split_by_calendar_time():
    data = {
        "step": [1, 10, 25, 50, 75, 100],
        "type": ["TRANSFER", "CASH_OUT", "TRANSFER", "CASH_OUT", "TRANSFER", "CASH_OUT"],
        "amount": [100.0, 200.0, 300.0, 400.0, 500.0, 600.0],
        "isFraud": [0, 0, 0, 0, 1, 1],
    }
    df = pd.DataFrame(data)

    # 75% calendar time between step 1 and 100: cutoff = 1 + 0.75 * 99 = 75.25
    train_df, test_df, cutoff = split_by_calendar_time(df, train_ratio=0.75)

    assert cutoff == 75.25
    assert len(train_df) == 5  # steps 1, 10, 25, 50, 75
    assert len(test_df) == 1   # step 100
    assert test_df.iloc[0]["step"] == 100


def test_filter_types(tmp_path):
    csv_file = tmp_path / "test_paysim.csv"
    data = {
        "step": [1, 2, 3, 4],
        "type": ["TRANSFER", "PAYMENT", "CASH_OUT", "DEBIT"],
        "amount": [100, 200, 300, 400],
        "isFraud": [1, 0, 0, 0],
    }
    pd.DataFrame(data).to_csv(csv_file, index=False)

    filtered_df = load_and_filter_data(str(csv_file))
    assert set(filtered_df["type"].unique()) == {"TRANSFER", "CASH_OUT"}
    assert len(filtered_df) == 2
