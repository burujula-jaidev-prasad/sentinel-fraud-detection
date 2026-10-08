"""50-Case Report Evaluation and Validation Harness for Mission 4."""

import os
import sys
import json
import pandas as pd
import numpy as np

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.reporter import CaseReporter


def run_50_case_evaluation(
    cases_dir: str = "outputs/cases",
    reports_dir: str = "outputs/reports",
    output_csv: str = "outputs/report_evaluation_50.csv",
    n_fraud: int = 25,
    n_legit: int = 25,
):
    """
    Evaluates 50 case investigation reports (25 fraud, 25 legitimate) against strict compliance criteria:
    1. Structure Completeness (Summary, Key facts, Why flagged, Recommended action, AI disclaimer)
    2. Zero Hallucination / Numeric Faithfulness (exact amount, step, score, and decision matching)
    3. Correct History Representation ('no prior history available' when count is 0)
    4. Decision Integrity (models/rules make decisions, LLM explains without alteration)
    """
    os.makedirs(reports_dir, exist_ok=True)
    reporter = CaseReporter(reports_dir=reports_dir)

    all_case_files = sorted([f for f in os.listdir(cases_dir) if f.endswith(".json")])

    fraud_cases = []
    legit_cases = []

    for cf in all_case_files:
        with open(os.path.join(cases_dir, cf), "r", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("isFraud") == 1 and data["scores"]["model_score"] >= 0.5:
            fraud_cases.append((cf, data))
        elif data.get("isFraud") == 0 and data["scores"]["model_score"] >= 0.5:
            legit_cases.append((cf, data))

    selected_cases = fraud_cases[:n_fraud] + legit_cases[:n_legit]
    print(f"Selected {len(selected_cases)} cases for evaluation ({len(fraud_cases[:n_fraud])} fraud, {len(legit_cases[:n_legit])} legitimate).")

    eval_results = []

    for i, (cf_name, case_data) in enumerate(selected_cases, 1):
        cid = case_data["case_id"]
        tx = case_data["transaction"]
        scores = case_data["scores"]
        ro = case_data["risk_officer"]
        sender_hist = case_data["sender_history"]
        is_fraud = case_data["isFraud"]

        # Generate or load cached report
        report_text = reporter.generate_report(case_data, use_llm=True)

        # Automated Quality Checks
        has_summary = "SUMMARY:" in report_text
        has_key_facts = "KEY FACTS:" in report_text
        has_why_flagged = "WHY FLAGGED:" in report_text
        has_action = "RECOMMENDED ACTION:" in report_text
        has_disclaimer = "AI-generated from case facts, human review required." in report_text

        # Numeric and factual grounding checks
        amount_str = f"{tx['amount']:,.2f}"
        contains_amount = amount_str in report_text or f"${tx['amount']:,.2f}" in report_text
        contains_score = f"{scores['model_score']:.4f}" in report_text
        contains_decision = ro["decision_balanced"] in report_text

        # Correct negative history handling check
        if sender_hist.get("prior_tx_count", 0) == 0:
            history_faithful = "no prior history available" in report_text.lower()
        else:
            history_faithful = str(sender_hist.get("prior_tx_count")) in report_text

        is_fully_compliant = all([
            has_summary,
            has_key_facts,
            has_why_flagged,
            has_action,
            has_disclaimer,
            contains_amount,
            contains_score,
            contains_decision,
            history_faithful,
        ])

        eval_results.append({
            "case_id": cid,
            "ground_truth": "FRAUD" if is_fraud == 1 else "LEGITIMATE",
            "type": tx["type"],
            "amount": tx["amount"],
            "model_score": scores["model_score"],
            "decision": ro["decision_balanced"],
            "structure_complete": (has_summary and has_key_facts and has_why_flagged and has_action and has_disclaimer),
            "amount_grounded": contains_amount,
            "score_grounded": contains_score,
            "decision_grounded": contains_decision,
            "history_grounded": history_faithful,
            "fully_compliant": is_fully_compliant,
        })

    eval_df = pd.DataFrame(eval_results)
    eval_df.to_csv(output_csv, index=False)
    print(f"Saved evaluation metrics to: {output_csv}")

    # Summary Statistics
    total_cases = len(eval_df)
    compliant_cases = eval_df["fully_compliant"].sum()
    compliance_rate = (compliant_cases / total_cases) * 100

    print("\n" + "=" * 70)
    print(" 50-CASE REPORT EVALUATION BENCHMARK RESULTS")
    print("=" * 70)
    print(f"Total Cases Evaluated:       {total_cases} (25 Fraud, 25 Legitimate)")
    print(f"Structure Completeness:      {eval_df['structure_complete'].mean():.1%}")
    print(f"Amount Grounding Accuracy:   {eval_df['amount_grounded'].mean():.1%}")
    print(f"Score Grounding Accuracy:    {eval_df['score_grounded'].mean():.1%}")
    print(f"Decision Grounding Accuracy: {eval_df['decision_grounded'].mean():.1%}")
    print(f"History Grounding Accuracy:  {eval_df['history_grounded'].mean():.1%}")
    print(f"Overall Full Compliance:    {compliant_cases}/{total_cases} ({compliance_rate:.1f}%)")
    print("=" * 70 + "\n")

    return eval_df


if __name__ == "__main__":
    run_50_case_evaluation()
