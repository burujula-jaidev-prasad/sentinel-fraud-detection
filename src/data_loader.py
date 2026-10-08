"""Data loading, filtering, and time-based splitting module for PaySim dataset."""

import os
from typing import Tuple
import pandas as pd
import numpy as np


def load_and_filter_data(filepath: str) -> pd.DataFrame:
    """
    Loads transaction data from a CSV file and filters only 'TRANSFER' and 'CASH_OUT' transactions.

    Rationale:
    In financial fraud datasets like PaySim, fraud almost exclusively occurs in TRANSFER
    (moving stolen money out of an account) and CASH_OUT (withdrawing stolen funds).
    Filtering out non-fraudulent transaction types (PAYMENT, CASH_IN, DEBIT) focuses the model
    on the subset of transactions where financial risk exists and reduces noise.

    Args:
        filepath (str): Path to the PaySim CSV dataset.

    Returns:
        pd.DataFrame: Filtered DataFrame containing only TRANSFER and CASH_OUT rows.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at: {filepath}")

    df = pd.read_csv(filepath)

    required_columns = {"step", "type", "amount", "isFraud"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    filtered_df = df[df["type"].isin(["TRANSFER", "CASH_OUT"])].copy()
    filtered_df.reset_index(drop=True, inplace=True)
    return filtered_df


def split_by_percentile(
    df: pd.DataFrame, percentile: float = 75.0
) -> Tuple[pd.DataFrame, pd.DataFrame, float]:
    """
    Main split: Splits transactions by the percentile of 'step' among filtered rows.
    For 75th percentile, step <= 333 (first 75% of transaction volume/steps in filtered data)
    forms the training set, and step > 333 forms the test set.

    Args:
        df (pd.DataFrame): Filtered DataFrame with 'step' column.
        percentile (float): Percentile threshold (default 75.0).

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, float]: (train_df, test_df, cutoff_step)
    """
    cutoff_step = float(np.percentile(df["step"], percentile))
    train_df = df[df["step"] <= cutoff_step].copy().reset_index(drop=True)
    test_df = df[df["step"] > cutoff_step].copy().reset_index(drop=True)
    return train_df, test_df, cutoff_step


def split_by_calendar_time(
    df: pd.DataFrame, train_ratio: float = 0.75
) -> Tuple[pd.DataFrame, pd.DataFrame, float]:
    """
    Secondary split: Splits by the overall time horizon span (calendar duration).
    cutoff_step = min_step + train_ratio * (max_step - min_step), e.g. step <= 556.8.

    Args:
        df (pd.DataFrame): Filtered DataFrame with 'step' column.
        train_ratio (float): Ratio of total time duration for training (default 0.75).

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, float]: (train_df, test_df, cutoff_step)
    """
    min_step = df["step"].min()
    max_step = df["step"].max()
    cutoff_step = float(min_step + train_ratio * (max_step - min_step))

    train_df = df[df["step"] <= cutoff_step].copy().reset_index(drop=True)
    test_df = df[df["step"] > cutoff_step].copy().reset_index(drop=True)
    return train_df, test_df, cutoff_step


# Alias for backward compatibility / primary default split
split_by_time = split_by_percentile
