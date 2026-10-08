"""Feature engineering module for fraud detection."""

from typing import List, Tuple, Optional
import pandas as pd
import numpy as np

FEATURE_NAMES: List[str] = ["amount", "log_amount", "is_transfer", "hour"]
TARGET_NAME: str = "isFraud"


def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts the four specified core features from the transaction records:
    1. `amount`: The raw monetary value of the transaction.
    2. `log_amount`: Natural log transformation np.log1p(amount) to compress extreme financial outliers.
    3. `is_transfer`: Binary indicator (1 if type is TRANSFER, 0 if CASH_OUT).
    4. `hour`: The hour of the day (step % 24) capturing daily behavioral patterns.

    Args:
        df (pd.DataFrame): Input transactions DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing only the engineered feature columns.
    """
    features = pd.DataFrame(index=df.index)

    # 1. Raw amount
    features["amount"] = df["amount"].astype(float)

    # 2. Log-transformed amount: log(1 + amount)
    features["log_amount"] = np.log1p(df["amount"].astype(float))

    # 3. Binary flag for TRANSFER transaction
    features["is_transfer"] = (df["type"] == "TRANSFER").astype(int)

    # 4. Hour of the day derived from step
    features["hour"] = (df["step"] % 24).astype(int)

    return features[FEATURE_NAMES]


def prepare_feature_target_split(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
    """
    Extracts features matrix X and target vector y (if isFraud exists in df).

    Args:
        df (pd.DataFrame): Input transactions DataFrame.

    Returns:
        Tuple[pd.DataFrame, Optional[pd.Series]]: (X, y)
    """
    X = extract_features(df)
    y = df[TARGET_NAME] if TARGET_NAME in df.columns else None
    return X, y
