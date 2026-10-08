"""Fraud Investigation Agent Module.

Combines rule-based policies and machine learning inference for intelligent fraud screening.
"""

from typing import Dict, Any
import joblib
import pandas as pd
import numpy as np


class FraudAgent:
    """Agent responsible for assessing transaction risk and orchestrating decisions."""

    def __init__(self, model_path: str = "models/rf.pkl", threshold: float = 0.5):
        self.model_path = model_path
        self.threshold = threshold
        self.model = None

    def load_model(self):
        """Loads serialized Random Forest model."""
        self.model = joblib.load(self.model_path)

    def analyze_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes a single transaction payload.

        Args:
            transaction: Dictionary containing 'step', 'type', 'amount'.

        Returns:
            Dict[str, Any]: Decision verdict, fraud score, and reasoning.
        """
        tx_type = transaction.get("type", "").upper()
        amount = float(transaction.get("amount", 0.0))
        step = int(transaction.get("step", 0))

        # Check if transaction is eligible for fraud review
        if tx_type not in ["TRANSFER", "CASH_OUT"]:
            return {
                "verdict": "APPROVE",
                "risk_score": 0.0,
                "reason": f"Transaction type '{tx_type}' has negligible historical fraud incidence in this portfolio.",
            }

        if self.model is None:
            self.load_model()

        # Prepare feature vector
        features = pd.DataFrame(
            [
                {
                    "amount": amount,
                    "log_amount": np.log1p(amount),
                    "is_transfer": 1 if tx_type == "TRANSFER" else 0,
                    "hour": step % 24,
                }
            ]
        )

        fraud_prob = float(self.model.predict_proba(features)[0, 1])
        is_fraud = fraud_prob >= self.threshold

        verdict = "BLOCK" if is_fraud else "APPROVE"
        reason = (
            f"Model predicted fraud probability {fraud_prob:.4f} (threshold: {self.threshold:.2f})."
        )

        return {
            "verdict": verdict,
            "risk_score": round(fraud_prob, 4),
            "is_flagged": is_fraud,
            "reason": reason,
        }
