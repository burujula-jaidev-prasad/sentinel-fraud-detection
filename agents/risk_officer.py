"""Risk Officer Agent: applies decision policies, human escalations, and cost-benefit financial risk evaluation."""

import os
import sys
from typing import Dict, Any, List, Optional
import joblib
import numpy as np
import pandas as pd

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import load_and_filter_data, split_by_percentile
from src.features import extract_features

REVIEW_COST_PER_ALERT: float = 500.0

POLICY_THRESHOLDS: Dict[str, float] = {
    "strict": 0.1,
    "balanced": 0.5,
    "lenient": 0.9,
}


class RiskOfficer:
    """Risk Officer agent managing policy decisions, escalations, and financial cost-loss accounting."""

    def __init__(self, p99_amount: Optional[float] = None, data_path: str = "data/paysim_sample.csv"):
        self.data_path = data_path
        self.p99_amount = p99_amount
        if self.p99_amount is None:
            self._compute_train_p99()

    def _compute_train_p99(self) -> None:
        """Computes the 99th percentile limit using strictly training data (step <= 333)."""
        df = load_and_filter_data(self.data_path)
        train_df, _, _ = split_by_percentile(df, percentile=75.0)
        self.p99_amount = float(np.percentile(train_df["amount"].values.astype(float), 99.0))

    def evaluate_decision(
        self,
        model_score: float,
        amount: float,
        policy: str = "balanced",
    ) -> str:
        """
        Determines the operational verdict for a transaction:
        - 'allow': Transaction score is at or below policy threshold.
        - 'hold': Transaction exceeds threshold and is held for automated/standard review.
        - 'escalate_to_human': Score >= 0.9 OR transaction amount >= 99th percentile of training amounts.

        Args:
            model_score: Random Forest fraud probability.
            amount: Transaction monetary value.
            policy: 'strict' (> 0.1), 'balanced' (> 0.5), or 'lenient' (> 0.9).

        Returns:
            str: 'allow', 'hold', or 'escalate_to_human'
        """
        threshold = POLICY_THRESHOLDS.get(policy.lower(), 0.5)

        if model_score < threshold:
            return "allow"

        # Escalation condition: High model certainty (>= 0.9) OR extreme monetary value (>= p99)
        if model_score >= 0.9 or (self.p99_amount is not None and amount >= self.p99_amount):
            return "escalate_to_human"

        return "hold"

    def evaluate_all_policies(self, model_score: float, amount: float) -> Dict[str, str]:
        """Evaluates decisions across all three policies for a single transaction."""
        return {
            "decision_strict": self.evaluate_decision(model_score, amount, policy="strict"),
            "decision_balanced": self.evaluate_decision(model_score, amount, policy="balanced"),
            "decision_lenient": self.evaluate_decision(model_score, amount, policy="lenient"),
        }


def compute_policy_comparison(
    data_path: str = "data/paysim_sample.csv",
    model_path: str = "models/rf.pkl",
    review_cost_per_alert: float = REVIEW_COST_PER_ALERT,
) -> pd.DataFrame:
    """
    Computes economic cost-benefit metrics for the three policies on the primary test period (step > 333):
    - alerts: Total flagged transactions
    - frauds_caught: True Positives
    - frauds_missed: False Negatives
    - fraud_value_saved: Sum of amounts of detected frauds
    - fraud_value_lost: Sum of amounts of missed frauds
    - review_cost: alerts * 500
    - total_cost: review_cost + fraud_value_lost

    Returns:
        pd.DataFrame: Summary table comparing Strict, Balanced, and Lenient policies.
    """
    df = load_and_filter_data(data_path)
    train_df, test_df, _ = split_by_percentile(df, percentile=75.0)

    rf_model = joblib.load(model_path)
    X_test = extract_features(test_df)
    y_prob = rf_model.predict_proba(X_test)[:, 1]
    y_true = test_df["isFraud"].values
    amounts = test_df["amount"].values

    records = []
    for policy_name, th in POLICY_THRESHOLDS.items():
        is_alert = y_prob >= th
        alerts = int(is_alert.sum())

        is_fraud = y_true == 1
        frauds_caught = int((is_alert & is_fraud).sum())
        frauds_missed = int((~is_alert & is_fraud).sum())

        fraud_value_saved = float(amounts[is_alert & is_fraud].sum())
        fraud_value_lost = float(amounts[~is_alert & is_fraud].sum())

        review_cost = float(alerts * review_cost_per_alert)
        total_cost = float(review_cost + fraud_value_lost)

        records.append(
            {
                "policy": policy_name,
                "threshold": th,
                "alerts": alerts,
                "frauds_caught": frauds_caught,
                "frauds_missed": frauds_missed,
                "fraud_value_saved": round(fraud_value_saved, 2),
                "fraud_value_lost": round(fraud_value_lost, 2),
                "review_cost": round(review_cost, 2),
                "total_cost": round(total_cost, 2),
            }
        )

    summary_df = pd.DataFrame(records)
    return summary_df
