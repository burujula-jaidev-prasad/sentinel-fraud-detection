"""Unit tests for Risk Officer agent."""

import pytest
import pandas as pd
from agents.risk_officer import RiskOfficer, compute_policy_comparison


def test_risk_officer_decisions():
    officer = RiskOfficer(p99_amount=2000000.0, data_path="data/paysim_sample.csv")

    # Score below threshold -> allow
    assert officer.evaluate_decision(0.05, amount=1000.0, policy="strict") == "allow"
    assert officer.evaluate_decision(0.40, amount=1000.0, policy="balanced") == "allow"

    # Score above threshold but < 0.9 and < p99 -> hold
    assert officer.evaluate_decision(0.60, amount=50000.0, policy="balanced") == "hold"

    # Score >= 0.9 -> escalate_to_human
    assert officer.evaluate_decision(0.95, amount=1000.0, policy="lenient") == "escalate_to_human"

    # Amount >= p99 -> escalate_to_human
    assert officer.evaluate_decision(0.60, amount=3000000.0, policy="balanced") == "escalate_to_human"


def test_policy_comparison_output():
    summary_df = compute_policy_comparison(data_path="data/paysim_sample.csv", model_path="models/rf.pkl")
    assert len(summary_df) == 3
    assert set(summary_df["policy"]) == {"strict", "balanced", "lenient"}
    assert "alerts" in summary_df.columns
    assert "total_cost" in summary_df.columns

    # Verify expected alert counts
    strict_alerts = summary_df[summary_df["policy"] == "strict"]["alerts"].iloc[0]
    balanced_alerts = summary_df[summary_df["policy"] == "balanced"]["alerts"].iloc[0]
    lenient_alerts = summary_df[summary_df["policy"] == "lenient"]["alerts"].iloc[0]

    assert strict_alerts == 2430
    assert balanced_alerts == 389
    assert lenient_alerts == 85
