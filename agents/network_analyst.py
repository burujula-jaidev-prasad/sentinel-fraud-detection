"""Network Analyst Agent: identifies correlated same-step identical-amount transfer-cashout pairs as forensic evidence."""

import os
import sys
from typing import Dict, Any, List, Optional
from collections import defaultdict
import networkx as nx
import pandas as pd

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import load_and_filter_data


class NetworkAnalyst:
    """Network Analyst agent identifying same-step identical-amount transfer-cashout laundering pairs."""

    def __init__(self, data_path: Optional[str] = "data/paysim_sample.csv"):
        self.data_path = data_path
        self.graph = nx.MultiDiGraph()
        # Fast lookup mapping: (step, round(amount, 2)) -> list of transfer records
        self.transfers_by_step_amount = defaultdict(list)
        self.cashouts_by_step_amount = defaultdict(list)

        if self.data_path and os.path.exists(self.data_path):
            self.build_graph_from_data(self.data_path)

    def build_graph_from_data(self, data_path: str) -> None:
        """Loads dataset and indexes transfer-cashout pairs by (step, amount)."""
        df = load_and_filter_data(data_path)
        self.graph.clear()
        self.transfers_by_step_amount.clear()
        self.cashouts_by_step_amount.clear()

        for idx, row in df.iterrows():
            step = int(row["step"])
            tx_type = str(row["type"])
            amount = round(float(row["amount"]), 2)
            sender = str(row["nameOrig"])
            receiver = str(row["nameDest"])

            # Add directed edge to graph
            self.graph.add_edge(
                sender,
                receiver,
                step=step,
                type=tx_type,
                amount=amount,
                tx_id=idx,
            )

            record = {
                "step": step,
                "type": tx_type,
                "amount": amount,
                "nameOrig": sender,
                "nameDest": receiver,
                "tx_id": idx,
            }

            if tx_type == "TRANSFER":
                self.transfers_by_step_amount[(step, amount)].append(record)
            elif tx_type == "CASH_OUT":
                self.cashouts_by_step_amount[(step, amount)].append(record)

    def add_transaction(self, sender: str, receiver: str, step: int, tx_type: str, amount: float, tx_id: Any = None) -> None:
        """Adds a single transaction dynamically to the index and graph."""
        amt = round(float(amount), 2)
        self.graph.add_edge(sender, receiver, step=step, type=tx_type, amount=amt, tx_id=tx_id)
        rec = {
            "step": step,
            "type": tx_type,
            "amount": amt,
            "nameOrig": sender,
            "nameDest": receiver,
            "tx_id": tx_id,
        }
        if tx_type == "TRANSFER":
            self.transfers_by_step_amount[(step, amt)].append(rec)
        elif tx_type == "CASH_OUT":
            self.cashouts_by_step_amount[(step, amt)].append(rec)

    def find_linked_pair(self, transaction: Dict[str, Any] | pd.Series) -> Dict[str, Any]:
        """
        Evaluates the same-step identical-amount pair rule:
        - For a CASH_OUT transaction: looks for a TRANSFER at the exact same step with identical amount.
        - For a TRANSFER transaction: looks for a CASH_OUT at the exact same step with identical amount.

        Returns:
            Dict containing forensic pair linkage evidence for case files and Network tab.
        """
        step = int(transaction["step"])
        tx_type = str(transaction["type"]).upper()
        amount = round(float(transaction["amount"]), 2)
        sender = str(transaction["nameOrig"])
        receiver = str(transaction["nameDest"])

        if tx_type == "CASH_OUT":
            matched = self.transfers_by_step_amount.get((step, amount), [])
            counterpart_type = "TRANSFER"
        elif tx_type == "TRANSFER":
            matched = self.cashouts_by_step_amount.get((step, amount), [])
            counterpart_type = "CASH_OUT"
        else:
            matched = []
            counterpart_type = "NONE"

        has_link = len(matched) > 0

        # Construct evidence object
        return {
            "has_linked_pair": has_link,
            "pattern": "same_step_identical_amount",
            "matched_counterpart_type": counterpart_type if has_link else None,
            "matched_pair_count": len(matched),
            "linked_counterparts": matched,
            "evidence_note": (
                f"Detected {len(matched)} matching {counterpart_type} transaction(s) at step {step} "
                f"with identical amount ${amount:,.2f}."
                if has_link
                else "No same-step identical-amount counterpart found."
            ),
        }
