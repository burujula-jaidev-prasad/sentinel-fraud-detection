"""Unit tests for Investigator agent."""

import pytest
import pandas as pd
from agents.investigator import Investigator


def test_investigator_case_building():
    investigator = Investigator(data_path="data/paysim_sample.csv")

    tx = {
        "step": 400,
        "type": "TRANSFER",
        "amount": 2500000.0,
        "nameOrig": "C123456789",
        "nameDest": "M987654321",
    }

    case = investigator.build_case_file(
        transaction=tx,
        model_score=0.75,
        anomaly_score=0.15,
        case_id="case_test_001",
    )

    assert case["case_id"] == "case_test_001"
    assert case["transaction"]["amount"] == 2500000.0
    assert case["scores"]["model_score"] == 0.75
    assert case["amount_analysis"]["percentile_vs_train"] >= 90.0
    assert "prior_tx_count" in case["sender_history"]
    assert "prior_tx_count" in case["receiver_history"]


def test_investigator_strictly_earlier_steps():
    investigator = Investigator(data_path="data/paysim_sample.csv")
    sender = "C_TEST_ACCOUNT"

    # Inject mock historical entries at step 10, 50, 100
    investigator.sender_history_index[sender] = [
        (10, "TRANSFER", 100.0),
        (50, "CASH_OUT", 200.0),
        (100, "TRANSFER", 300.0),
    ]

    # Query at step 60 should only see step 10 and 50 (strictly earlier steps)
    hist_60 = investigator.get_sender_history(sender, current_step=60)
    assert hist_60["prior_tx_count"] == 2
    assert hist_60["prior_total_amount"] == 300.0

    # Query at step 10 should see 0 prior transactions
    hist_10 = investigator.get_sender_history(sender, current_step=10)
    assert hist_10["prior_tx_count"] == 0
