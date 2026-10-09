"""Export precomputed PaySim replay stream and case records to a compact JSON bundle."""

import os
import glob
import json
import pandas as pd

def export_stream():
    os.makedirs("data", exist_ok=True)
    os.makedirs("docs/data", exist_ok=True)

    # 1. Load alerts
    df_alerts = pd.read_csv("outputs/replay_alerts.csv")
    alerts_list = df_alerts.to_dict(orient="records")

    # 2. Load policy comparison
    df_policy = pd.read_csv("outputs/policy_comparison.csv")
    policy_list = df_policy.to_dict(orient="records")

    # 3. Load network edges
    df_edges = pd.read_csv("outputs/network_edges.csv")
    edges_list = df_edges.to_dict(orient="records")

    # 4. Load all case dossiers and AI reports
    cases = {}
    for p in sorted(glob.glob("outputs/cases/*.json")):
        with open(p, "r", encoding="utf-8") as f:
            case_data = json.load(f)
            cid = case_data["case_id"]
            
            # Attach report text if exists
            rpt_path = f"outputs/reports/{cid}.txt"
            if os.path.exists(rpt_path):
                with open(rpt_path, "r", encoding="utf-8") as rf:
                    case_data["report_text"] = rf.read()
            else:
                case_data["report_text"] = "No precomputed report file available."
            
            cases[cid] = case_data

    # 5. Build combined bundle
    bundle = {
        "metadata": {
            "source": "PaySim 15% Sample (Synthetic Mobile Money)",
            "test_steps_range": [334, 743],
            "total_test_transactions": 103191,
            "total_candidate_alerts": len(alerts_list),
            "total_cases": len(cases),
            "total_network_pairs": len(edges_list),
            "disclaimer": "Simulated replay of PaySim test dataset (steps 334-743). Not real-time bank data."
        },
        "alerts": alerts_list,
        "policy_comparison": policy_list,
        "network_edges": edges_list,
        "cases": cases,
    }

    # Save to data/stream.json and docs/data/stream.json
    for out_path in ["data/stream.json", "docs/data/stream.json"]:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(bundle, f)
        print(f"Exported stream bundle to {out_path} ({os.path.getsize(out_path) / 1024 / 1024:.2f} MB)")

if __name__ == "__main__":
    export_stream()
