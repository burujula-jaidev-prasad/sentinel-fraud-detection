"""Mission 9a: Export district hourly aggregations and 3D city people data."""

import os
import sys
import json
import hashlib
import numpy as np
import pandas as pd
import joblib

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.features import extract_features

def compute_district(account_id: str) -> int:
    """Compute deterministic district 1-8 from account id MD5 hash."""
    md5_hex = hashlib.md5(str(account_id).encode("utf-8")).hexdigest()[:8]
    return (int(md5_hex, 16) % 8) + 1

def main():
    print("Loading primary PaySim dataset...")
    df = pd.read_csv("data/paysim_sample.csv")
    
    # Filter to primary transfer/cashout
    df = df[df["type"].isin(["TRANSFER", "CASH_OUT"])].copy()
    
    # Exclude all balance columns strictly
    safe_cols = ["step", "type", "amount", "nameOrig", "nameDest", "isFraud"]
    df = df[safe_cols].copy()
    df["hour"] = (df["step"] % 24).astype(int)

    # Split train/test
    train_df = df[df["step"] <= 333].copy()
    test_df = df[df["step"] > 333].copy().sort_values("step").reset_index(drop=True)

    print(f"Train rows: {len(train_df):,}, Test rows: {len(test_df):,}")

    # Compute amount percentiles based on training amounts
    train_amounts = np.sort(train_df["amount"].values)
    
    def get_amount_percentile(amt):
        idx = np.searchsorted(train_amounts, amt)
        return float(np.clip(idx / len(train_amounts), 0.05, 1.0))

    # Compute districts for test accounts
    test_df["district_from"] = test_df["nameOrig"].apply(compute_district)
    test_df["district_to"] = test_df["nameDest"].apply(compute_district)
    test_df["amount_pct"] = test_df["amount"].apply(get_amount_percentile)

    # Load model and score test rows using exact extract_features
    print("Scoring test rows with saved Random Forest model...")
    rf_model = joblib.load("models/rf.pkl")
    X_test = extract_features(test_df)
    
    scores = rf_model.predict_proba(X_test)[:, 1]
    test_df["score"] = scores
    test_df["alert_strict"] = (scores >= 0.10).astype(int)
    test_df["alert_balanced"] = (scores >= 0.50).astype(int)
    test_df["alert_lenient"] = (scores >= 0.90).astype(int)

    print(f"Alerts verified -> Strict (>=0.10): {test_df['alert_strict'].sum():,}, "
          f"Balanced (>=0.50): {test_df['alert_balanced'].sum():,}, "
          f"Lenient (>=0.90): {test_df['alert_lenient'].sum():,}")

    # Generate district_hourly.csv
    print("Generating district_hourly.csv...")
    steps = list(range(334, 744))
    districts = list(range(1, 9))
    
    grouped = test_df.groupby(["step", "district_from"]).agg(
        payments=("amount", "count"),
        alerts_strict=("alert_strict", "sum"),
        alerts_balanced=("alert_balanced", "sum"),
        alerts_lenient=("alert_lenient", "sum")
    ).reset_index()
    
    group_map = {(r["step"], r["district_from"]): r for _, r in grouped.iterrows()}
    
    grid_records = []
    for s in steps:
        for d in districts:
            if (s, d) in group_map:
                r = group_map[(s, d)]
                grid_records.append({
                    "step": s,
                    "district": d,
                    "payments": int(r["payments"]),
                    "alerts_strict": int(r["alerts_strict"]),
                    "alerts_balanced": int(r["alerts_balanced"]),
                    "alerts_lenient": int(r["alerts_lenient"])
                })
            else:
                grid_records.append({
                    "step": s,
                    "district": d,
                    "payments": 0,
                    "alerts_strict": 0,
                    "alerts_balanced": 0,
                    "alerts_lenient": 0
                })

    df_district_hourly = pd.DataFrame(grid_records)
    
    os.makedirs("docs/data", exist_ok=True)
    os.makedirs("outputs/data", exist_ok=True)
    
    df_district_hourly.to_csv("docs/data/district_hourly.csv", index=False)
    df_district_hourly.to_csv("outputs/data/district_hourly.csv", index=False)
    print(f"\nSaved district_hourly.csv: shape {df_district_hourly.shape}")
    print("district_hourly.csv first 3 rows:")
    print(df_district_hourly.head(3))

    # Generate city_people.json: all flagged payments + stratified clean sample
    print("\nGenerating city_people.json...")
    flagged_mask = (test_df["score"] >= 0.10) | (test_df["isFraud"] == 1)
    df_flagged = test_df[flagged_mask].copy()
    df_clean = test_df[~flagged_mask].sample(n=6000, random_state=42).copy()
    
    combined_people = pd.concat([df_flagged, df_clean]).sort_values("step").reset_index(drop=True)
    
    people_list = []
    for idx, row in combined_people.iterrows():
        people_list.append({
            "id": f"tx_{row['step']}_{idx}",
            "step": int(row["step"]),
            "hour": int(row["hour"]),
            "type": str(row["type"]),
            "district_from": int(row["district_from"]),
            "district_to": int(row["district_to"]),
            "amount": float(row["amount"]),
            "amount_pct": round(float(row["amount_pct"]), 3),
            "score": round(float(row["score"]), 4),
            "alert_strict": bool(row["alert_strict"]),
            "alert_balanced": bool(row["alert_balanced"]),
            "alert_lenient": bool(row["alert_lenient"]),
            "is_fraud": int(row["isFraud"])
        })

    with open("docs/data/city_people.json", "w", encoding="utf-8") as f:
        json.dump(people_list, f)
    with open("outputs/data/city_people.json", "w", encoding="utf-8") as f:
        json.dump(people_list, f)

    print(f"\nSaved city_people.json with {len(people_list)} people records.")
    print("city_people.json first 3 records:")
    print(json.dumps(people_list[:3], indent=2))

if __name__ == "__main__":
    main()
