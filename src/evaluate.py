"""Evaluation metrics module for fraud detection."""

from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)


def compute_metrics(
    y_true: pd.Series | np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray,
) -> Dict[str, Any]:
    """
    Computes standard evaluation metrics for fraud detection models.

    Key Metrics:
    - Precision: TP / (TP + FP) - Proportion of flagged transactions that are truly fraud.
    - Recall:    TP / (TP + FN) - Proportion of all actual frauds detected.
    - F1:        Harmonic mean of precision and recall.
    - PR-AUC:    Area under the Precision-Recall curve.
    - ROC-AUC:   Area under Receiver Operating Characteristic curve.

    Args:
        y_true: True binary target labels (0 or 1).
        y_pred: Predicted binary labels (0 or 1).
        y_prob: Predicted probabilities for the positive class (fraud).

    Returns:
        Dict[str, Any]: Dictionary containing metric values and confusion matrix.
    """
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    pr_auc = average_precision_score(y_true, y_prob)
    roc_auc = roc_auc_score(y_true, y_prob)
    cm = confusion_matrix(y_true, y_pred)

    return {
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "pr_auc": float(pr_auc),
        "roc_auc": float(roc_auc),
        "confusion_matrix": cm,
        "classification_report": classification_report(y_true, y_pred, zero_division=0),
    }


def print_comparison_table(splits_results: Dict[str, Dict[str, Any]]) -> None:
    """
    Prints a formatted side-by-side comparison table for multiple split evaluations.

    Args:
        splits_results: Dictionary mapping split names to their computed metrics dict.
    """
    header = f"{'Split Name':<32} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10} | {'PR-AUC':<10} | {'ROC-AUC':<10}"
    separator = "-" * len(header)

    print("\n" + "=" * len(header))
    print(" MODEL PERFORMANCE EVALUATION COMPARISON")
    print("=" * len(header))
    print(header)
    print(separator)

    for split_name, metrics in splits_results.items():
        p = metrics["precision"]
        r = metrics["recall"]
        f1 = metrics["f1"]
        pr_auc = metrics["pr_auc"]
        roc_auc = metrics["roc_auc"]
        print(
            f"{split_name:<32} | {p:<10.4f} | {r:<10.4f} | {f1:<10.4f} | {pr_auc:<10.4f} | {roc_auc:<10.4f}"
        )

    print(separator)
    print("=" * len(header) + "\n")
