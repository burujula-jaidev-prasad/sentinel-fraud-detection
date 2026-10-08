"""Reporter Agent: generates concise plain-English case investigation summaries from factual case files."""

import os
import sys
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

# Load environment variables from .env if present
def _load_env_file(dotenv_path: str = ".env") -> None:
    """Loads key-value pairs from .env without external library dependency if dotenv is absent."""
    try:
        from dotenv import load_dotenv
        load_dotenv(dotenv_path)
    except ImportError:
        if os.path.exists(dotenv_path):
            with open(dotenv_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip().strip("'\""))


_load_env_file()


class CaseReporter:
    """Reporter agent producing factual case investigation reports from JSON case files."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        reports_dir: str = "outputs/reports",
    ):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.model_name = model_name or os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
        self.reports_dir = reports_dir
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_template_report(self, case_file: Dict[str, Any]) -> str:
        """
        Deterministic, rule-based template reporter that formats the four standard sections
        using strictly verified case file facts without LLM hallucination risk.
        """
        cid = case_file.get("case_id", "Unknown")
        tx = case_file.get("transaction", {})
        scores = case_file.get("scores", {})
        amount_analysis = case_file.get("amount_analysis", {})
        sender_hist = case_file.get("sender_history", {})
        receiver_hist = case_file.get("receiver_history", {})
        ro = case_file.get("risk_officer", {})
        net = case_file.get("network_evidence", {})

        step = tx.get("step", "N/A")
        hour = tx.get("hour", step % 24 if isinstance(step, int) else "N/A")
        tx_type = tx.get("type", "N/A")
        amount = tx.get("amount", 0.0)
        sender = tx.get("nameOrig", "N/A")
        receiver = tx.get("nameDest", "N/A")

        model_score = scores.get("model_score", 0.0)
        anomaly_score = scores.get("anomaly_score", 0.0)
        percentile = amount_analysis.get("percentile_vs_train", 0.0)
        is_above_p99 = amount_analysis.get("is_above_p99", False)

        decision = ro.get("decision_balanced", "hold")
        is_escalated = ro.get("escalated", False)

        # 1. Summary
        summary = (
            f"Case {cid} concerns a {tx_type} transaction of ${amount:,.2f} at simulation step {step} (Hour {hour}). "
            f"The transaction was assigned a fraud probability score of {model_score:.4f} and an anomaly score of {anomaly_score:.4f}. "
            f"The Risk Officer decision under the balanced policy is '{decision}'."
        )

        # 2. Key facts
        if sender_hist.get("prior_tx_count", 0) == 0:
            sender_history_str = "no prior history available"
        else:
            sender_history_str = (
                f"{sender_hist.get('prior_tx_count')} prior transaction(s) totalling "
                f"${sender_hist.get('prior_total_amount', 0.0):,.2f}"
            )

        if receiver_hist.get("prior_tx_count", 0) == 0:
            receiver_history_str = "no prior history available"
        else:
            receiver_history_str = (
                f"{receiver_hist.get('prior_tx_count')} prior transaction(s) totalling "
                f"${receiver_hist.get('prior_total_amount', 0.0):,.2f}"
            )

        key_facts = (
            f"- Transaction ID/Case: {cid}\n"
            f"- Type: {tx_type}\n"
            f"- Amount: ${amount:,.2f} ({percentile:.1f}th percentile of training transactions)\n"
            f"- Step / Hour: Step {step} (Hour {hour})\n"
            f"- Sender: {sender} ({sender_history_str})\n"
            f"- Receiver: {receiver} ({receiver_history_str})\n"
            f"- Model Score (RF Probability): {model_score:.4f}\n"
            f"- Anomaly Score (Isolation Forest): {anomaly_score:.4f}\n"
            f"- Operational Decision: {decision} (Escalate to human: {is_escalated})"
        )

        # 3. Why flagged
        flag_reasons = []
        if model_score >= 0.5:
            flag_reasons.append(f"Model fraud probability score ({model_score:.4f}) exceeds the 0.50 operational threshold.")
        if is_above_p99:
            flag_reasons.append(f"Transaction amount (${amount:,.2f}) exceeds the training 99th percentile limit ($2,439,133.86).")
        if net.get("has_linked_pair", False):
            flag_reasons.append(f"Network Analyst detected a correlated same-step identical-amount {net.get('matched_counterpart_type')} counterpart.")
        if not flag_reasons:
            flag_reasons.append(f"Flagged based on screening threshold criteria (RF score {model_score:.4f}).")

        why_flagged = "\n".join(f"- {r}" for r in flag_reasons)

        # 4. Recommended action
        if decision == "escalate_to_human" or is_escalated:
            action = "Escalate immediately to a human fraud investigator for manual verification and identity authentication prior to fund release."
        elif decision == "hold":
            action = "Hold transaction in temporary security queue pending standard automated review and customer alert confirmation."
        else:
            action = "Allow transaction to proceed with standard post-transaction logging."

        report = (
            f"SUMMARY:\n{summary}\n\n"
            f"KEY FACTS:\n{key_facts}\n\n"
            f"WHY FLAGGED:\n{why_flagged}\n\n"
            f"RECOMMENDED ACTION:\n{action}\n\n"
            f"AI-generated from case facts, human review required."
        )
        return report

    def generate_llm_report(self, case_file: Dict[str, Any]) -> str:
        """
        Generates a case report using the Gemini API.
        Falls back automatically to the template report if the API key is missing or calls fail.
        """
        if not self.api_key:
            return self.generate_template_report(case_file)

        prompt = (
            "You are a compliance and fraud investigation reporting assistant. "
            "Generate a short plain-English case investigation report from the following case file JSON.\n\n"
            "STRICT RULES:\n"
            "1. Use ONLY facts present in the case file. Do NOT invent numbers, accounts, history, or causes.\n"
            "2. If sender history is empty (prior_tx_count = 0), explicitly say 'no prior history available'.\n"
            "3. State the exact model score and the operational decision.\n"
            "4. If network_evidence indicates a linked_pair/linked_transfer exists, mention it factually.\n"
            "5. You must NEVER make, overturn, or change decisions.\n"
            "6. Follow this FIXED FORMAT exactly with these four section headers:\n"
            "   SUMMARY:\n"
            "   KEY FACTS:\n"
            "   WHY FLAGGED:\n"
            "   RECOMMENDED ACTION:\n"
            "7. End the report with the exact phrase: 'AI-generated from case facts, human review required.'\n\n"
            f"CASE FILE JSON:\n{json.dumps(case_file, indent=2)}"
        )

        try:
            # Attempt official Google GenAI / Gemini API call via REST
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
            payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

            with urllib.request.urlopen(req, timeout=15) as response:
                result = json.loads(response.read().decode("utf-8"))
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                if not text.endswith("AI-generated from case facts, human review required."):
                    text = text.strip() + "\n\nAI-generated from case facts, human review required."
                return text
        except Exception:
            # Graceful fallback to deterministic template generator
            return self.generate_template_report(case_file)

    def generate_report(
        self,
        case_filepath_or_dict: str | Dict[str, Any],
        use_llm: bool = True,
        force_refresh: bool = False,
    ) -> str:
        """
        Generates and caches case report to outputs/reports/<case_id>.txt.
        Skips generation if report file already exists (caching).
        """
        if isinstance(case_filepath_or_dict, str):
            with open(case_filepath_or_dict, "r", encoding="utf-8") as f:
                case_data = json.load(f)
        else:
            case_data = case_filepath_or_dict

        cid = case_data.get("case_id", "case_report")
        report_path = os.path.join(self.reports_dir, f"{cid}.txt")

        if os.path.exists(report_path) and not force_refresh:
            with open(report_path, "r", encoding="utf-8") as f:
                return f.read()

        if use_llm and self.api_key:
            report_text = self.generate_llm_report(case_data)
        else:
            report_text = self.generate_template_report(case_data)

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_text)

        return report_text
