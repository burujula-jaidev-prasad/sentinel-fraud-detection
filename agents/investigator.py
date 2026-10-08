"""Investigator Agent: compiles forensic transaction case files using strictly prior historical context."""

import os
import sys
from typing import Dict, Any, List, Optional
from collections import defaultdict
import numpy as np
import pandas as pd

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import load_and_filter_data, split_by_percentile


class Investigator:
    """Investigator agent that reconstructs chronological transaction history and builds forensic case files."""

    def __init__(self, data_path: str = "data/paysim_sample.csv"):
        self.data_path = data_path
        self.train_amounts = None
        self.p99_amount = None

        # Chronological index of transactions: account -> list of (step, type, amount)
        self.sender_history_index = defaultdict(list)
        self.receiver_history_index = defaultdict(list)

        self._initialize_reference_data()

    def _initialize_reference_data(self) -> None:
        """Loads dataset, computes training amount percentiles (step <= 333), and populates historical indexes."""
        df = load_and_filter_data(self.data_path)
        train_df, test_df, _ = split_by_percentile(df, percentile=75.0)

        # Baseline amount distribution from training period only
        self.train_amounts = np.sort(train_df["amount"].values.astype(float))
        self.p99_amount = float(np.percentile(self.train_amounts, 99.0))

        # Index all transactions chronologically by sender and receiver
        # (Balance columns are strictly excluded per project rules)
        for _, row in df.iterrows():
            step = int(row["step"])
            tx_type = str(row["type"])
            amount = float(row["amount"])
            sender = str(row["nameOrig"])
            receiver = str(row["nameDest"])

            # Store lightweight tuple (step, type, amount)
            self.sender_history_index[sender].append((step, tx_type, amount))
            self.receiver_history_index[receiver].append((step, tx_type, amount))

    def compute_amount_percentile(self, amount: float) -> float:
        """Computes empirical percentile of an amount against the training distribution (0-100%)."""
        if self.train_amounts is None:
            return 50.0
        # Binary search for rank in sorted training amounts
        idx = np.searchsorted(self.train_amounts, amount, side="right")
        return float((idx / len(self.train_amounts)) * 100.0)

    def get_sender_history(self, sender: str, current_step: int) -> Dict[str, Any]:
        """
        Retrieves sender transaction history strictly prior to current_step (step < current_step).
        """
        records = [rec for rec in self.sender_history_index.get(sender, []) if rec[0] < current_step]
        if not records:
            return {
                "prior_tx_count": 0,
                "prior_total_amount": 0.0,
                "prior_avg_amount": 0.0,
                "prior_max_amount": 0.0,
                "prior_types": [],
            }

        amounts = [r[2] for r in records]
        types = list(set(r[1] for r in records))
        return {
            "prior_tx_count": len(records),
            "prior_total_amount": round(float(sum(amounts)), 2),
            "prior_avg_amount": round(float(np.mean(amounts)), 2),
            "prior_max_amount": round(float(max(amounts)), 2),
            "prior_types": types,
        }

    def get_receiver_history(self, receiver: str, current_step: int) -> Dict[str, Any]:
        """
        Retrieves receiver transaction history strictly prior to current_step (step < current_step).
        """
        records = [rec for rec in self.receiver_history_index.get(receiver, []) if rec[0] < current_step]
        if not records:
            return {
                "prior_tx_count": 0,
                "prior_total_amount": 0.0,
                "prior_avg_amount": 0.0,
                "prior_max_amount": 0.0,
            }

        amounts = [r[2] for r in records]
        return {
            "prior_tx_count": len(records),
            "prior_total_amount": round(float(sum(amounts)), 2),
            "prior_avg_amount": round(float(np.mean(amounts)), 2),
            "prior_max_amount": round(float(max(amounts)), 2),
        }

    def build_case_file(
        self,
        transaction: Dict[str, Any] | pd.Series,
        model_score: float,
        anomaly_score: float,
        case_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Builds a comprehensive case file for a flagged transaction.

        Args:
            transaction: Transaction details dict or Series.
            model_score: Random Forest fraud probability.
            anomaly_score: Isolation Forest anomaly score.
            case_id: Optional case identifier string.

        Returns:
            Dict containing forensic case details.
        """
        step = int(transaction["step"])
        tx_type = str(transaction["type"])
        amount = float(transaction["amount"])
        name_orig = str(transaction["nameOrig"])
        name_dest = str(transaction["nameDest"])

        amount_pct = self.compute_amount_percentile(amount)
        is_above_p99 = bool(amount >= self.p99_amount)

        sender_hist = self.get_sender_history(name_orig, current_step=step)
        receiver_hist = self.get_receiver_history(name_dest, current_step=step)

        cid = case_id or f"CASE_{step}_{name_orig[-6:]}_{int(amount)}"

        case_file = {
            "case_id": cid,
            "transaction": {
                "step": step,
                "type": tx_type,
                "amount": round(amount, 2),
                "nameOrig": name_orig,
                "nameDest": name_dest,
                "hour": step % 24,
            },
            "scores": {
                "model_score": round(float(model_score), 4),
                "anomaly_score": round(float(anomaly_score), 4),
            },
            "amount_analysis": {
                "amount": round(amount, 2),
                "percentile_vs_train": round(amount_pct, 2),
                "is_above_p99": is_above_p99,
                "train_p99_limit": round(self.p99_amount, 2),
            },
            "sender_history": {
                "nameOrig": name_orig,
                **sender_hist,
            },
            "receiver_history": {
                "nameDest": name_dest,
                **receiver_hist,
            },
        }

        return case_file
