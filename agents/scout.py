"""Scout Agent: real-time transaction screening using Random Forest and Isolation Forest anomaly detection."""

import os
import sys
from typing import Dict, Any, Tuple, Optional
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.features import extract_features
from src.data_loader import load_and_filter_data, split_by_percentile


class Scout:
    """Scout agent responsible for evaluating fraud probability and anomaly scores."""

    def __init__(
        self,
        rf_model_path: str = "models/rf.pkl",
        iso_model_path: str = "models/iso.pkl",
        default_threshold: float = 0.1,
    ):
        self.rf_model_path = rf_model_path
        self.iso_model_path = iso_model_path
        self.default_threshold = default_threshold
        self.rf_model = None
        self.iso_model = None

    def load_models(self) -> None:
        """Loads serialized RandomForest and IsolationForest models."""
        if not os.path.exists(self.rf_model_path):
            raise FileNotFoundError(f"RandomForest model not found at {self.rf_model_path}")
        self.rf_model = joblib.load(self.rf_model_path)

        if os.path.exists(self.iso_model_path):
            self.iso_model = joblib.load(self.iso_model_path)

    def train_isolation_forest(
        self,
        data_path: str = "data/paysim_sample.csv",
        n_estimators: int = 100,
        random_state: int = 42,
        save_path: Optional[str] = None,
    ) -> IsolationForest:
        """
        Trains IsolationForest exclusively on the training period (step <= 333) and saves artifact.
        """
        df = load_and_filter_data(data_path)
        train_df, _, _ = split_by_percentile(df, percentile=75.0)

        X_train = extract_features(train_df)
        iso = IsolationForest(
            n_estimators=n_estimators,
            random_state=random_state,
            n_jobs=-1,
            contamination="auto",
        )
        iso.fit(X_train)

        target_path = save_path or self.iso_model_path
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        joblib.dump(iso, target_path)
        self.iso_model = iso
        return iso

    def score_transaction(
        self,
        transaction: Dict[str, Any] | pd.Series,
        threshold: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Scores a single transaction row or dictionary.

        Returns:
            Dict with model_score (float), anomaly_score (float), is_flagged (bool).
        """
        if self.rf_model is None or self.iso_model is None:
            self.load_models()

        if self.iso_model is None:
            self.train_isolation_forest()

        th = threshold if threshold is not None else self.default_threshold

        # Convert to single-row DataFrame for feature extractor
        if isinstance(transaction, dict):
            df_single = pd.DataFrame([transaction])
        elif isinstance(transaction, pd.Series):
            df_single = pd.DataFrame([transaction.to_dict()])
        else:
            df_single = transaction

        X = extract_features(df_single)

        # 1. Random Forest fraud probability
        rf_score = float(self.rf_model.predict_proba(X)[0, 1])

        # 2. Isolation Forest anomaly score (negated decision function so higher = more anomalous)
        raw_iso = float(self.iso_model.decision_function(X)[0])
        anomaly_score = float(-raw_iso)

        # 3. Flagging condition
        is_flagged = bool(rf_score >= th)

        return {
            "model_score": round(rf_score, 4),
            "anomaly_score": round(anomaly_score, 4),
            "is_flagged": is_flagged,
            "threshold_used": th,
        }

    def score_dataframe(
        self,
        df: pd.DataFrame,
        threshold: Optional[float] = None,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Vectorized scoring for high-throughput batch evaluation.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray]: (rf_scores, anomaly_scores, is_flagged_array)
        """
        if self.rf_model is None or self.iso_model is None:
            self.load_models()

        if self.iso_model is None:
            self.train_isolation_forest()

        th = threshold if threshold is not None else self.default_threshold

        X = extract_features(df)
        rf_scores = self.rf_model.predict_proba(X)[:, 1]
        iso_decision = self.iso_model.decision_function(X)
        anomaly_scores = -iso_decision
        is_flagged = rf_scores >= th

        return rf_scores, anomaly_scores, is_flagged
