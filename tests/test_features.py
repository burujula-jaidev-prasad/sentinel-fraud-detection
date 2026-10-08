"""Tests for feature engineering logic."""

import pandas as pd
import numpy as np
import pytest
from src.features import extract_features, FEATURE_NAMES


def test_extract_features_values():
    df = pd.DataFrame(
        [
            {"step": 0, "type": "TRANSFER", "amount": 0.0, "isFraud": 0},
            {"step": 25, "type": "CASH_OUT", "amount": 99.0, "isFraud": 1},
            {"step": 48, "type": "TRANSFER", "amount": 1000.0, "isFraud": 0},
        ]
    )

    X = extract_features(df)

    # Check columns
    assert list(X.columns) == FEATURE_NAMES

    # Check amount
    assert np.allclose(X["amount"].values, [0.0, 99.0, 1000.0])

    # Check log_amount: log(1 + amount)
    assert np.allclose(X["log_amount"].values, [0.0, np.log(100.0), np.log(1001.0)])

    # Check is_transfer
    assert list(X["is_transfer"].values) == [1, 0, 1]

    # Check hour: step % 24
    assert list(X["hour"].values) == [0, 1, 0]
