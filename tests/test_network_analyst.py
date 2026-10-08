"""Unit tests for Network Analyst agent (same-step identical-amount pair rule)."""

import pytest
from agents.network_analyst import NetworkAnalyst


def test_network_analyst_same_step_identical_amount():
    analyst = NetworkAnalyst(data_path=None)

    # Add a TRANSFER of $125,000 at step 50
    analyst.add_transaction(
        sender="C_VICTIM_1",
        receiver="C_MULE_1",
        step=50,
        tx_type="TRANSFER",
        amount=125000.00,
        tx_id=101,
    )

    # Test CASH_OUT at step 50 with exact same amount $125,000
    cashout_tx = {
        "step": 50,
        "type": "CASH_OUT",
        "amount": 125000.00,
        "nameOrig": "C_MULE_2",
        "nameDest": "M_MERCHANT_1",
    }

    result = analyst.find_linked_pair(cashout_tx)
    assert result["has_linked_pair"] is True
    assert result["matched_counterpart_type"] == "TRANSFER"
    assert result["matched_pair_count"] == 1
    assert result["linked_counterparts"][0]["nameOrig"] == "C_VICTIM_1"


def test_network_analyst_step_or_amount_mismatch():
    analyst = NetworkAnalyst(data_path=None)

    # Add TRANSFER at step 50
    analyst.add_transaction(
        sender="C_VICTIM_1",
        receiver="C_MULE_1",
        step=50,
        tx_type="TRANSFER",
        amount=125000.00,
    )

    # Different step (step 51)
    cashout_diff_step = {
        "step": 51,
        "type": "CASH_OUT",
        "amount": 125000.00,
        "nameOrig": "C_MULE_2",
        "nameDest": "M_MERCHANT_1",
    }
    assert analyst.find_linked_pair(cashout_diff_step)["has_linked_pair"] is False

    # Different amount
    cashout_diff_amt = {
        "step": 50,
        "type": "CASH_OUT",
        "amount": 125001.00,
        "nameOrig": "C_MULE_2",
        "nameDest": "M_MERCHANT_1",
    }
    assert analyst.find_linked_pair(cashout_diff_amt)["has_linked_pair"] is False
