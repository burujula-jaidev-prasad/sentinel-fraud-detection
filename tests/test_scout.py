"""Unit tests for Scout agent."""

import pytest
import pandas as pd
from agents.scout import Scout


def test_scout_scoring():
    scout = Scout(rf_model_path="models/rf.pkl", iso_model_path="models/iso.pkl")
    scout.load_models()

    tx = {"step": 400, "type": "TRANSFER", "amount": 500000.0}
    res = scout.score_transaction(tx, threshold=0.1)

    assert "model_score" in res
    assert "anomaly_score" in res
    assert "is_flagged" in res
    assert 0.0 <= res["model_score"] <= 1.0
    assert isinstance(res["is_flagged"], bool)
