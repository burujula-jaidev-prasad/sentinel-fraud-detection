"""Replay test period transactions chronologically through Scout, Investigator, and Risk Officer agents."""

import os
import sys
import json
import numpy as np
import pandas as pd

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.data_loader import load_and_filter_data, split_by_percentile
from src.features import extract_features
from agents.scout import Scout
from agents.investigator import Investigator
from agents.network_analyst import NetworkAnalyst
from agents.risk_officer import RiskOfficer, compute_policy_comparison


def run_replay(
    data_path: str = "data/paysim_sample.csv",
    rf_model_path: str = "models/rf.pkl",
    iso_model_path: str = "models/iso.pkl",
    output_dir: str = "outputs",
):
    """
    Executes the chronological transaction replay pipeline:
    1. Loads test period data (step > 333) sorted by step.
    2. Scores all transactions through Scout (RF fraud probability + IsolationForest anomaly score).
    3. Evaluates decisions under Strict, Balanced, and Lenient policies using RiskOfficer.
    4. Filters all alerts with RF score >= 0.1 and saves outputs/replay_alerts.csv.
    5. Generates forensic case files via Investigator for all alerts with RF score >= 0.5 into outputs/cases/.
    6. Computes and saves economic evaluation to outputs/policy_comparison.csv.
    7. Prints the first 10 flagged case files and the policy comparison table.
    """
    os.makedirs(output_dir, exist_ok=True)
    cases_dir = os.path.join(output_dir, "cases")
    os.makedirs(cases_dir, exist_ok=True)

    print("=" * 70)
    print(" SENTINEL FRAUD MONITORING: CHRONOLOGICAL TEST REPLAY ENGINE")
    print("=" * 70)

    # 1. Load data and extract test partition
    print(f"\n[1/5] Loading data from {data_path}...")
    df = load_and_filter_data(data_path)
    train_df, test_df, cutoff_step = split_by_percentile(df, percentile=75.0)

    # Ensure strictly chronological step order
    test_df = test_df.sort_values(by=["step"]).reset_index(drop=True)
    print(f"Test period contains {len(test_df):,} transactions (steps {test_df['step'].min()} to {test_df['step'].max()}).")

    # 2. Initialize Agents
    print("\n[2/5] Initializing Scout, Investigator, and RiskOfficer agents...")
    scout = Scout(rf_model_path=rf_model_path, iso_model_path=iso_model_path, default_threshold=0.1)
    if not os.path.exists(iso_model_path):
        print("Training IsolationForest on training partition (step <= 333)...")
        scout.train_isolation_forest(data_path=data_path, save_path=iso_model_path)
    scout.load_models()

    investigator = Investigator(data_path=data_path)
    network_analyst = NetworkAnalyst(data_path=data_path)
    risk_officer = RiskOfficer(p99_amount=investigator.p99_amount, data_path=data_path)

    # 3. Vectorized Scoring via Scout
    print("\n[3/5] Scoring test period transactions with Scout (Random Forest + Isolation Forest)...")
    rf_scores, anomaly_scores, is_flagged_01 = scout.score_dataframe(test_df, threshold=0.1)

    test_df["model_score"] = np.round(rf_scores, 4)
    test_df["anomaly_score"] = np.round(anomaly_scores, 4)

    # Risk Officer Decisions across all 3 policies
    print("Applying Risk Officer decision policies (Strict, Balanced, Lenient)...")
    amounts = test_df["amount"].values
    decisions_strict = [
        risk_officer.evaluate_decision(s, a, policy="strict")
        for s, a in zip(rf_scores, amounts)
    ]
    decisions_balanced = [
        risk_officer.evaluate_decision(s, a, policy="balanced")
        for s, a in zip(rf_scores, amounts)
    ]
    decisions_lenient = [
        risk_officer.evaluate_decision(s, a, policy="lenient")
        for s, a in zip(rf_scores, amounts)
    ]

    test_df["decision_strict"] = decisions_strict
    test_df["decision_balanced"] = decisions_balanced
    test_df["decision_lenient"] = decisions_lenient
    test_df["decision"] = decisions_balanced  # Default operational policy

    # 4. Save replay_alerts.csv (all transactions with RF score >= 0.1)
    print("\n[4/5] Exporting flagged alert stream (RF score >= 0.1)...")
    alerts_df = test_df[test_df["model_score"] >= 0.1].copy().reset_index(drop=True)

    alert_columns = [
        "step",
        "type",
        "amount",
        "nameOrig",
        "nameDest",
        "model_score",
        "anomaly_score",
        "decision_strict",
        "decision_balanced",
        "decision_lenient",
        "decision",
        "isFraud",
    ]
    replay_alerts_path = os.path.join(output_dir, "replay_alerts.csv")
    alerts_df[alert_columns].to_csv(replay_alerts_path, index=False)
    print(f"Saved {len(alerts_df):,} alerts (score >= 0.1) to: {replay_alerts_path}")

    # 5. Build Case Files for all alerts with RF score >= 0.5
    print("\n[5/5] Generating forensic case files for alerts with RF score >= 0.5...")
    cases_df = test_df[test_df["model_score"] >= 0.5].copy().reset_index(drop=True)
    generated_cases = []

    for idx, row in cases_df.iterrows():
        case_id = f"case_{idx+1:04d}_{row['step']}_{row['nameOrig'][-6:]}"
        case_file = investigator.build_case_file(
            transaction=row,
            model_score=row["model_score"],
            anomaly_score=row["anomaly_score"],
            case_id=case_id,
        )
        # Network Analyst evidence: same step + identical amount pair
        network_evidence = network_analyst.find_linked_pair(row)
        case_file["network_evidence"] = network_evidence

        case_file["risk_officer"] = {
            "decision_strict": row["decision_strict"],
            "decision_balanced": row["decision_balanced"],
            "decision_lenient": row["decision_lenient"],
            "escalated": bool(row["decision_balanced"] == "escalate_to_human"),
        }
        case_file["isFraud"] = int(row["isFraud"])

        case_filepath = os.path.join(cases_dir, f"{case_id}.json")
        with open(case_filepath, "w", encoding="utf-8") as f:
            json.dump(case_file, f, indent=2)

        generated_cases.append(case_file)

    print(f"Generated {len(generated_cases):,} JSON case files in: {cases_dir}")

    # 6. Policy Economic Comparison
    policy_df = compute_policy_comparison(data_path=data_path, model_path=rf_model_path)
    policy_comparison_path = os.path.join(output_dir, "policy_comparison.csv")
    policy_df.to_csv(policy_comparison_path, index=False)
    print(f"Saved policy comparison table to: {policy_comparison_path}")

    # 7. Print First 10 Flagged Case Summaries
    print("\n" + "=" * 70)
    print(" FIRST 10 FLAGGED CASE FILES (RF SCORE >= 0.5)")
    print("=" * 70)
    for i, case in enumerate(generated_cases[:10], 1):
        tx = case["transaction"]
        scores = case["scores"]
        analysis = case["amount_analysis"]
        ro = case["risk_officer"]
        net = case.get("network_evidence", {})
        print(f"\n[Case #{i}] {case['case_id']}")
        print(f"  Step: {tx['step']} (Hour: {tx['hour']}) | Type: {tx['type']} | Amount: ${tx['amount']:,.2f} ({analysis['percentile_vs_train']:.1f}th %ile)")
        print(f"  Sender: {tx['nameOrig']} (Prior TXs: {case['sender_history']['prior_tx_count']}) -> Receiver: {tx['nameDest']}")
        print(f"  RF Score: {scores['model_score']:.4f} | Anomaly Score: {scores['anomaly_score']:.4f}")
        print(f"  Network Evidence: {net.get('evidence_note', 'None')}")
        print(f"  Decisions -> Strict: {ro['decision_strict']} | Balanced: {ro['decision_balanced']} | Lenient: {ro['decision_lenient']}")
        print(f"  Ground Truth: {'FRAUD' if case['isFraud'] == 1 else 'LEGITIMATE'}")

    # 8. Print Policy Comparison Table
    print("\n" + "=" * 70)
    print(" RISK POLICY COST-BENEFIT COMPARISON TABLE")
    print("=" * 70)
    print(policy_df.to_string(index=False))
    print("=" * 70 + "\n")

    return alerts_df, generated_cases, policy_df


if __name__ == "__main__":
    run_replay()
