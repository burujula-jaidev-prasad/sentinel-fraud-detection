"""Unit tests for Reporter agent."""

import pytest
from agents.reporter import CaseReporter


def test_template_reporter_generation():
    reporter = CaseReporter()

    mock_case = {
        "case_id": "case_test_001",
        "transaction": {
            "step": 350,
            "type": "CASH_OUT",
            "amount": 500000.00,
            "nameOrig": "C1000",
            "nameDest": "M2000",
            "hour": 14,
        },
        "scores": {
            "model_score": 0.65,
            "anomaly_score": 0.12,
        },
        "amount_analysis": {
            "percentile_vs_train": 88.5,
            "is_above_p99": False,
        },
        "sender_history": {
            "prior_tx_count": 0,
        },
        "receiver_history": {
            "prior_tx_count": 1,
            "prior_total_amount": 100000.00,
        },
        "risk_officer": {
            "decision_balanced": "hold",
            "escalated": False,
        },
        "network_evidence": {
            "has_linked_pair": False,
        },
    }

    report = reporter.generate_template_report(mock_case)

    assert "SUMMARY:" in report
    assert "KEY FACTS:" in report
    assert "WHY FLAGGED:" in report
    assert "RECOMMENDED ACTION:" in report
    assert "no prior history available" in report
    assert "0.6500" in report
    assert report.strip().endswith("AI-generated from case facts, human review required.")
