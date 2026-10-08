"""Sentinel Command Center: Streamlit executive dashboard and multi-agent fraud monitoring interface."""

import os
import sys
import glob
import json
import datetime
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Streamlit Page Configuration
st.set_page_config(
    page_title="Sentinel Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Dark Theme Styling
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #1E222D;
        border: 1px solid #2E3648;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .metric-title {
        color: #8C9BAE;
        font-size: 13px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-val {
        color: #FFFFFF;
        font-size: 24px;
        font-weight: 700;
        margin-top: 4px;
    }
    .metric-sub {
        color: #4CAF50;
        font-size: 12px;
        margin-top: 2px;
    }
    .tab-desc {
        color: #9AA5B8;
        font-style: italic;
        font-size: 14px;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 1px solid #2A3142;
    }
    .badge-hold {
        background-color: #D97706;
        color: #FFFFFF;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 600;
    }
    .badge-escalate {
        background-color: #DC2626;
        color: #FFFFFF;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 600;
    }
    .badge-allow {
        background-color: #10B981;
        color: #FFFFFF;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 600;
    }
    .ai-disclaimer {
        background-color: #1A2333;
        border-left: 4px solid #3B82F6;
        padding: 10px 14px;
        font-size: 13px;
        color: #93C5FD;
        border-radius: 4px;
        margin-top: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_replay_alerts(filepath: str = "outputs/replay_alerts.csv") -> pd.DataFrame:
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        return df
    return pd.DataFrame()


@st.cache_data
def load_policy_comparison(filepath: str = "outputs/policy_comparison.csv") -> pd.DataFrame:
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    return pd.DataFrame()


@st.cache_data
def load_network_edges(filepath: str = "outputs/network_edges.csv") -> pd.DataFrame:
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    return pd.DataFrame()


def load_case_file(case_id: str, cases_dir: str = "outputs/cases") -> Optional[Dict[str, Any]]:
    # Look for matching case file
    pattern = os.path.join(cases_dir, f"*{case_id}*.json")
    matches = glob.glob(pattern)
    if matches:
        with open(matches[0], "r", encoding="utf-8") as fp:
            return json.load(fp)
    # Direct lookup
    direct_path = os.path.join(cases_dir, f"{case_id}.json")
    if os.path.exists(direct_path):
        with open(direct_path, "r", encoding="utf-8") as fp:
            return json.load(fp)
    return None


def load_report_file(case_id: str, reports_dir: str = "outputs/reports") -> Optional[str]:
    direct_path = os.path.join(reports_dir, f"{case_id}.txt")
    if os.path.exists(direct_path):
        with open(direct_path, "r", encoding="utf-8") as fp:
            return fp.read()
    # Search by partial
    matches = glob.glob(os.path.join(reports_dir, f"*{case_id}*.txt"))
    if matches:
        with open(matches[0], "r", encoding="utf-8") as fp:
            return fp.read()
    return None


def log_human_decision(case_id: str, action: str, operator_note: str = "", output_path: str = "outputs/decisions.csv") -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    file_exists = os.path.exists(output_path)
    new_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "case_id": case_id,
        "action": action,
        "operator_note": operator_note,
    }
    df_entry = pd.DataFrame([new_entry])
    df_entry.to_csv(output_path, mode="a", header=not file_exists, index=False)


# --- Load Data ---
df_alerts = load_replay_alerts()
df_policy = load_policy_comparison()
df_edges = load_network_edges()

# --- Sidebar Controls ---
st.sidebar.title("🛡️ Sentinel Command")
st.sidebar.markdown("**Real-Time Payment Security**")
st.sidebar.markdown("---")

selected_policy = st.sidebar.selectbox(
    "Active Risk Policy",
    options=["Balanced (0.50)", "Strict (0.10)", "Lenient (0.90)"],
    index=0,
)
policy_key = "balanced"
if "Strict" in selected_policy:
    policy_key = "strict"
elif "Lenient" in selected_policy:
    policy_key = "lenient"

eval_mode = st.sidebar.toggle("Reveal ground truth (evaluation mode)", value=False)
if eval_mode:
    st.sidebar.warning("⚠️ Evaluation Mode ACTIVE: Ground truth fraud labels visible.")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**System Status:** 🟢 Live\n"
    "**Screening Engine:** Random Forest + Isolation Forest\n"
    "**Test Transactions:** 103,191\n"
    "**Total Candidate Alerts:** 2,430"
)

# --- Navigation Tabs ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "1. Command Center",
    "2. Alert Queue",
    "3. Case File",
    "4. Graph Analysis",
    "5. Policy Simulator",
    "6. Agent Diagnostics",
    "7. Investigation Workspace",
    "8. Model Card & Ethics",
])


# =============================================================================
# TAB 1: COMMAND CENTER
# =============================================================================
with tab1:
    st.markdown('<p class="tab-desc">Live transaction stream monitoring, operational threat telemetry, and temporal alert distribution.</p>', unsafe_allow_html=True)

    if not df_alerts.empty:
        # Filter alerts active under current policy
        decision_col = f"decision_{policy_key}"
        active_alerts = df_alerts[df_alerts[decision_col].isin(["hold", "escalate_to_human"])].copy()

        total_alerts_count = len(active_alerts)
        held_count = len(active_alerts[active_alerts[decision_col] == "hold"])
        escalated_count = len(active_alerts[active_alerts[decision_col] == "escalate_to_human"])
        fraud_val_stopped = active_alerts["amount"].sum()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-title">Active Alerts ({policy_key.capitalize()})</div>'
                f'<div class="metric-val">{total_alerts_count:,}</div>'
                f'<div class="metric-sub">From 103,191 test transactions</div></div>',
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f'<div class="metric-card"><div class="metric-title">Transactions Held</div>'
                f'<div class="metric-val">{held_count:,}</div>'
                f'<div class="metric-sub">Awaiting automated / tier-1 review</div></div>',
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                f'<div class="metric-card"><div class="metric-title">Human Escalations</div>'
                f'<div class="metric-val">{escalated_count:,}</div>'
                f'<div class="metric-sub">Score ≥ 0.90 or Amount ≥ p99 limit</div></div>',
                unsafe_allow_html=True,
            )
        with col4:
            if eval_mode:
                frauds_caught_val = int(active_alerts["isFraud"].sum())
                st.markdown(
                    f'<div class="metric-card"><div class="metric-title">Frauds Intercepted (Ground Truth)</div>'
                    f'<div class="metric-val" style="color:#10B981;">{frauds_caught_val:,} / 652</div>'
                    f'<div class="metric-sub">Protected value: {fraud_val_stopped:,.2f} currency units</div></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-title">Protected Volume under Review</div>'
                    f'<div class="metric-val">{fraud_val_stopped:,.2f}</div>'
                    f'<div class="metric-sub">In currency units</div></div>',
                    unsafe_allow_html=True,
                )

        st.markdown("### ⏱️ Live Simulation Stream")
        ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1, 2, 2])
        with ctrl_col1:
            playback = st.radio("Stream Status", ["Paused", "Live Stream"], horizontal=True)
        with ctrl_col2:
            max_step_avail = int(df_alerts["step"].max())
            min_step_avail = int(df_alerts["step"].min())
            current_sim_step = st.slider("Simulation Step", min_value=min_step_avail, max_value=max_step_avail, value=min_step_avail + 50)
        with ctrl_col3:
            playback_speed = st.select_slider("Stream Throttle (Steps/tick)", options=[1, 5, 10, 25, 50], value=10)

        streamed_data = active_alerts[active_alerts["step"] <= current_sim_step].sort_values("step", ascending=False)

        st.markdown(f"**Latest Incoming Alerts (Up to Step {current_sim_step}):**")
        display_cols = ["step", "type", "amount", "nameOrig", "nameDest", "model_score", "anomaly_score", decision_col]
        if eval_mode:
            display_cols.append("isFraud")

        # Rename amount column label to currency units
        disp_df = streamed_data[display_cols].head(15).copy()
        disp_df.rename(columns={"amount": "amount (currency units)", decision_col: "operational_decision"}, inplace=True)
        st.dataframe(disp_df, use_container_width=True, hide_index=True)

        st.markdown("### 📊 Alert Frequency Over Time")
        step_counts = active_alerts.groupby("step").size().reset_index(name="alert_count")
        chart = (
            alt.Chart(step_counts)
            .mark_bar(color="#3B82F6")
            .encode(
                x=alt.X("step:Q", title="Simulation Step (Time)"),
                y=alt.Y("alert_count:Q", title="Alert Volume"),
                tooltip=["step", "alert_count"],
            )
            .properties(height=240)
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No alert records found. Please ensure outputs/replay_alerts.csv exists.")


# =============================================================================
# TAB 2: ALERT QUEUE
# =============================================================================
with tab2:
    st.markdown('<p class="tab-desc">Comprehensive review queue prioritized by model risk score with multi-dimensional filtering.</p>', unsafe_allow_html=True)

    if not df_alerts.empty:
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        with f_col1:
            type_filter = st.multiselect("Transaction Type", options=["TRANSFER", "CASH_OUT"], default=["TRANSFER", "CASH_OUT"])
        with f_col2:
            min_amt = float(df_alerts["amount"].min())
            max_amt = float(df_alerts["amount"].max())
            amt_range = st.slider("Amount Range (currency units)", min_value=min_amt, max_value=max_amt, value=(min_amt, max_amt))
        with f_col3:
            decision_opts = ["All", "hold", "escalate_to_human", "allow"]
            sel_decision = st.selectbox("Decision Status", decision_opts, index=0)
        with f_col4:
            min_score_filter = st.slider("Minimum Model Score", 0.0, 1.0, 0.1, 0.05)

        filtered_queue = df_alerts[
            (df_alerts["type"].isin(type_filter))
            & (df_alerts["amount"] >= amt_range[0])
            & (df_alerts["amount"] <= amt_range[1])
            & (df_alerts["model_score"] >= min_score_filter)
        ].copy()

        decision_column = f"decision_{policy_key}"
        if sel_decision != "All":
            filtered_queue = filtered_queue[filtered_queue[decision_column] == sel_decision]

        filtered_queue = filtered_queue.sort_values(by="model_score", ascending=False).reset_index(drop=True)

        st.markdown(f"**Showing {len(filtered_queue):,} matching alerts sorted by risk severity:**")

        q_cols = ["step", "type", "amount", "nameOrig", "nameDest", "model_score", "anomaly_score", decision_column]
        if eval_mode:
            q_cols.append("isFraud")

        disp_q = filtered_queue[q_cols].copy()
        disp_q.rename(columns={"amount": "amount (currency units)", decision_column: "decision"}, inplace=True)
        st.dataframe(disp_q, use_container_width=True, hide_index=True)
    else:
        st.info("No alert queue available.")


# =============================================================================
# TAB 3: CASE FILE & DECISIONING
# =============================================================================
with tab3:
    st.markdown('<p class="tab-desc">Forensic case investigation dossier with behavioral history, network correlation, and human decision actions.</p>', unsafe_allow_html=True)

    cases_list = sorted([os.path.splitext(f)[0] for f in os.listdir("outputs/cases") if f.endswith(".json")])

    if cases_list:
        selected_case_id = st.selectbox("Select Case Dossier to Investigate", options=cases_list, index=0)
        case_data = load_case_file(selected_case_id)

        if case_data:
            tx = case_data["transaction"]
            scores = case_data["scores"]
            amount_info = case_data["amount_analysis"]
            sender_hist = case_data["sender_history"]
            receiver_hist = case_data["receiver_history"]
            ro = case_data["risk_officer"]
            net = case_data.get("network_evidence", {})

            # Case Header
            c_header_col1, c_header_col2, c_header_col3 = st.columns([2, 1, 1])
            with c_header_col1:
                st.subheader(f"📁 Dossier: {case_data['case_id']}")
                st.caption(f"Simulation Step: {tx['step']} (Hour {tx['hour']}) | Transaction Type: {tx['type']}")
            with c_header_col2:
                st.metric("Model Fraud Probability", f"{scores['model_score']:.4f}")
            with c_header_col3:
                dec = ro["decision_balanced"]
                badge_class = "badge-escalate" if dec == "escalate_to_human" else "badge-hold" if dec == "hold" else "badge-allow"
                st.markdown(f"**Operational Decision:**<br><span class='{badge_class}'>{dec.upper()}</span>", unsafe_allow_html=True)

            st.markdown("---")

            # Section 1: Transaction & Risk Indicators
            sec1_col1, sec1_col2 = st.columns(2)
            with sec1_col1:
                st.markdown("#### 💳 Transaction Details")
                st.markdown(f"- **Amount:** `{tx['amount']:,.2f}` currency units")
                st.markdown(f"- **Training Amount Percentile:** `{amount_info['percentile_vs_train']:.2f}%`")
                st.markdown(f"- **Exceeds 99th Percentile Limit:** `{'YES' if amount_info['is_above_p99'] else 'NO'}` (Limit: {amount_info['train_p99_limit']:,.2f} currency units)")
                st.markdown(f"- **Sender Account:** `{tx['nameOrig']}`")
                st.markdown(f"- **Receiver Account:** `{tx['nameDest']}`")

            with sec1_col2:
                st.markdown("#### 🧠 Behavioral & Anomaly Signals")
                st.markdown(f"- **Random Forest Fraud Score:** `{scores['model_score']:.4f}`")
                st.markdown(f"- **Isolation Forest Anomaly Score:** `{scores['anomaly_score']:.4f}`")
                if net.get("has_linked_pair"):
                    st.error(f"🔗 **Correlated Pair Detected:** Same-step identical-amount {net.get('matched_counterpart_type')} identified ({net.get('evidence_note')}).")
                else:
                    st.info("ℹ️ **Network Evidence:** No same-step identical-amount counterpart found.")

            st.markdown("---")

            # Section 2: Historical Profiles (Strictly Earlier Steps)
            h_col1, h_col2 = st.columns(2)
            with h_col1:
                st.markdown("#### 👤 Sender History (Prior Steps)")
                if sender_hist.get("prior_tx_count", 0) == 0:
                    st.markdown("*No prior history available in transaction records.*")
                else:
                    st.markdown(f"- **Prior Transactions:** `{sender_hist.get('prior_tx_count')}`")
                    st.markdown(f"- **Total Prior Volume:** `{sender_hist.get('prior_total_amount', 0.0):,.2f}` currency units")
                    st.markdown(f"- **Average Prior Amount:** `{sender_hist.get('prior_avg_amount', 0.0):,.2f}` currency units")

            with h_col2:
                st.markdown("#### 👥 Receiver History (Prior Steps)")
                if receiver_hist.get("prior_tx_count", 0) == 0:
                    st.markdown("*No prior history available in transaction records.*")
                else:
                    st.markdown(f"- **Prior Inflow Count:** `{receiver_hist.get('prior_tx_count')}`")
                    st.markdown(f"- **Total Prior Volume:** `{receiver_hist.get('prior_total_amount', 0.0):,.2f}` currency units")
                    st.markdown(f"- **Average Inflow Amount:** `{receiver_hist.get('prior_avg_amount', 0.0):,.2f}` currency units")

            st.markdown("---")

            # Section 3: AI Investigation Report
            st.markdown("#### 📝 Plain-English Investigation Report")
            report_text = load_report_file(case_data["case_id"])
            if report_text:
                st.text_area("Case Summary & Evidence", value=report_text, height=280, disabled=True)
            else:
                st.caption("Generating on-the-fly report...")
                from agents.reporter import CaseReporter
                rep = CaseReporter()
                gen_text = rep.generate_report(case_data)
                st.text_area("Case Summary & Evidence", value=gen_text, height=280, disabled=True)

            st.markdown('<div class="ai-disclaimer">🤖 AI-generated from case facts, human review required. Models and policy rules determine risk scores.</div>', unsafe_allow_html=True)

            st.markdown("---")

            # Section 4: Human-in-the-Loop Action Center
            st.markdown("#### ⚖️ Human Decision Action Center")
            act_col1, act_col2, act_col3 = st.columns([1, 1, 1])
            op_note = st.text_input("Operator Justification Note (Optional)", placeholder="Enter review reasoning...", key=f"note_{selected_case_id}")

            with act_col1:
                if st.button("🟠 Hold in Security Queue", key="btn_hold", use_container_width=True):
                    log_human_decision(case_data["case_id"], action="HOLD", operator_note=op_note)
                    st.success(f"Transaction {case_data['case_id']} held. Decision logged to outputs/decisions.csv.")

            with act_col2:
                if st.button("🟢 Release Funds (Approve)", key="btn_release", use_container_width=True):
                    log_human_decision(case_data["case_id"], action="RELEASE", operator_note=op_note)
                    st.success(f"Transaction {case_data['case_id']} approved. Decision logged to outputs/decisions.csv.")

            with act_col3:
                if st.button("🔴 Escalate to Senior Investigator", key="btn_escalate", use_container_width=True):
                    log_human_decision(case_data["case_id"], action="ESCALATE", operator_note=op_note)
                    st.warning(f"Transaction {case_data['case_id']} escalated. Decision logged to outputs/decisions.csv.")
    else:
        st.info("No case files found in outputs/cases/.")


# =============================================================================
# =============================================================================
# TAB 4: GRAPH ANALYSIS
# =============================================================================
with tab4:
    st.markdown('<p class="tab-desc">Correlated financial crime network analysis and tandem transfer-cashout topology.</p>', unsafe_allow_html=True)

    if not df_edges.empty:
        g_col1, g_col2, g_col3 = st.columns(3)
        with g_col1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-title">Identified Correlated Pairs</div>'
                f'<div class="metric-val">{len(df_edges)}</div>'
                f'<div class="metric-sub">90 Fraud-Fraud, 3 Legit-Legit</div></div>',
                unsafe_allow_html=True,
            )
        with g_col2:
            test_edges = df_edges[df_edges["step"] > 333]
            st.markdown(
                f'<div class="metric-card"><div class="metric-title">Test Period Pairs (step > 333)</div>'
                f'<div class="metric-val">{len(test_edges)}</div>'
                f'<div class="metric-sub">100% (46/46) Fraud-Fraud (Covers 92 test frauds)</div></div>',
                unsafe_allow_html=True,
            )
        with g_col3:
            total_net_val = df_edges["amount"].sum()
            st.markdown(
                f'<div class="metric-card"><div class="metric-title">Total Linked Flow Volume</div>'
                f'<div class="metric-val">{total_net_val:,.2f}</div>'
                f'<div class="metric-sub">In currency units</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("### 🕸️ Correlated Tandem Flow Explorer")
        st.markdown(
            "Empirical discovery: In PaySim, money mule accounts are generated per transaction (0 fraud destination accounts reappear as senders). "
            "However, **same-step + identical-amount pairs** form a distinct structural signature of coordinated laundering."
        )

        f_step_col, f_pair_col = st.columns([1, 2])
        with f_step_col:
            avail_steps = sorted(df_edges["step"].unique())
            selected_step = st.selectbox("Filter Correlated Pairs by Step", options=["All Steps"] + [str(s) for s in avail_steps])
        
        filtered_edges = df_edges.copy()
        if selected_step != "All Steps":
            filtered_edges = filtered_edges[filtered_edges["step"] == int(selected_step)]

        with f_pair_col:
            st.markdown(f"**Viewing {len(filtered_edges)} correlated pairs**")

        disp_edges = filtered_edges[["step", "amount", "transfer_orig", "transfer_dest", "cashout_orig", "cashout_dest", "is_fraud_pair"]].copy()
        disp_edges.rename(columns={"amount": "amount (currency units)"}, inplace=True)
        st.dataframe(disp_edges, use_container_width=True, hide_index=True)

        st.markdown("### 📊 Distribution of Linked Fraud Amounts")
        edge_chart = (
            alt.Chart(df_edges)
            .mark_circle(size=80, color="#EF4444")
            .encode(
                x=alt.X("step:Q", title="Simulation Step"),
                y=alt.Y("amount:Q", title="Tandem Transaction Amount (currency units)"),
                tooltip=["step", "amount", "transfer_orig", "cashout_dest", "is_fraud_pair"],
            )
            .properties(height=260)
        )
        st.altair_chart(edge_chart, use_container_width=True)
    else:
        st.info("No network edges found in outputs/network_edges.csv.")


# =============================================================================
# TAB 5: POLICY SIMULATOR
# =============================================================================
with tab5:
    st.markdown('<p class="tab-desc">Macroeconomic policy sensitivity analysis balancing review costs and direct fraud loss exposure.</p>', unsafe_allow_html=True)

    st.markdown(
        """
        > **Cost Model Assumptions:**
        > - **Manual Review Cost:** `500 currency units` per alert generated.
        > - **Missed Fraud Loss:** `100%` of stolen transaction principal.
        """
    )

    if not df_policy.empty:
        disp_policy = df_policy.copy()
        disp_policy.rename(
            columns={
                "fraud_value_saved": "fraud_value_saved (currency units)",
                "fraud_value_lost": "fraud_value_lost (currency units)",
                "review_cost": "review_cost (currency units)",
                "total_cost": "total_cost (currency units)",
            },
            inplace=True,
        )
        st.dataframe(disp_policy, use_container_width=True, hide_index=True)

        st.markdown("### 📈 Economic Cost Comparison by Policy")
        chart_data = df_policy.melt(
            id_vars=["policy"],
            value_vars=["review_cost", "fraud_value_lost", "total_cost"],
            var_name="Cost Component",
            value_name="Amount",
        )
        chart_data["Amount (currency units)"] = chart_data["Amount"]

        cost_chart = (
            alt.Chart(chart_data)
            .mark_bar()
            .encode(
                x=alt.X("policy:N", title="Operational Policy"),
                y=alt.Y("Amount:Q", title="Cost (currency units)"),
                color=alt.Color("Cost Component:N", scale=alt.Scale(scheme="tableau10")),
                xOffset="Cost Component:N",
                tooltip=["policy", "Cost Component", "Amount"],
            )
            .properties(height=320)
        )
        st.altair_chart(cost_chart, use_container_width=True)

        st.markdown(
            """
            **Strategic Takeaway:**
            Under digital payment conditions with large transaction sizes, **missed fraud costs dominate review costs**.
            The **Strict Policy** achieves the lowest net loss by saving the greatest total fraud volume despite higher alert queues.
            """
        )
    else:
        st.info("No policy comparison data found.")


# =============================================================================
# TAB 6: AGENT DIAGNOSTICS & TELEMETRY
# =============================================================================
with tab6:
    st.markdown('<p class="tab-desc">Multi-agent communication telemetry, execution trace logs, and scoring distribution telemetry.</p>', unsafe_allow_html=True)

    st.markdown("### 🤖 Multi-Agent Pipeline Architecture")
    st.markdown(
        """
        ```mermaid
        flowchart LR
            TX[Incoming Transaction] --> Scout[1. Scout Agent]
            Scout -->|Flagged Alert| Inv[2. Investigator Agent]
            Inv -->|Historical Profile| Net[3. Network Analyst]
            Net -->|Correlated Evidence| RO[4. Risk Officer]
            RO -->|Policy Decision & Case| Rep[5. Reporter Agent]
            Rep -->|Plain-English Report| Case[Case File Dossier]
        ```
        """
    )

    diag_col1, diag_col2 = st.columns(2)
    with diag_col1:
        st.markdown("#### 📋 Agent Operational Matrix")
        agent_table = pd.DataFrame([
            {"Agent": "Scout", "Role": "Real-time Screening", "Model / Method": "Random Forest + Isolation Forest", "Output": "Candidate Alerts"},
            {"Agent": "Investigator", "Role": "Behavioral Profiling", "Model / Method": "Historical Inflow/Outflow Engine", "Output": "Prior Step Velocity Profiles"},
            {"Agent": "NetworkAnalyst", "Role": "Crime Ring Correlation", "Model / Method": "Same-Step Identical-Amount Matcher", "Output": "Correlated Graph Evidence"},
            {"Agent": "RiskOfficer", "Role": "Policy Decisioning", "Model / Method": "Strict / Balanced / Lenient Rules", "Output": "Operational Decisions (Hold/Escalate)"},
            {"Agent": "Reporter", "Role": "Fact-Based Synthesis", "Model / Method": "Google Gemini 1.5 + Template Fallback", "Output": "Plain-English Case Reports"},
        ])
        st.dataframe(agent_table, use_container_width=True, hide_index=True)

    with diag_col2:
        st.markdown("#### 🎯 Score Distribution Telemetry")
        if not df_alerts.empty:
            scatter_chart = (
                alt.Chart(df_alerts.head(500))
                .mark_circle(size=45, opacity=0.7)
                .encode(
                    x=alt.X("model_score:Q", title="Random Forest Fraud Probability"),
                    y=alt.Y("anomaly_score:Q", title="Isolation Forest Anomaly Score"),
                    color=alt.Color("decision_balanced:N", scale=alt.Scale(domain=["allow", "hold", "escalate_to_human"], range=["#10B981", "#F59E0B", "#EF4444"])),
                    tooltip=["step", "type", "amount", "model_score", "anomaly_score", "decision_balanced"],
                )
                .properties(height=260)
            )
            st.altair_chart(scatter_chart, use_container_width=True)


# =============================================================================
# TAB 7: INVESTIGATION WORKSPACE & AUDIT LOG
# =============================================================================
with tab7:
    st.markdown('<p class="tab-desc">Collaborative human decision audit trail, compliance records, and case activity logs.</p>', unsafe_allow_html=True)

    decisions_file = "outputs/decisions.csv"
    if os.path.exists(decisions_file):
        df_dec = pd.read_csv(decisions_file)
    else:
        df_dec = pd.DataFrame(columns=["timestamp", "case_id", "action", "operator_note"])

    d_col1, d_col2, d_col3 = st.columns(3)
    with d_col1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-title">Total Human Decisions Logged</div>'
            f'<div class="metric-val">{len(df_dec)}</div>'
            f'<div class="metric-sub">Recorded in outputs/decisions.csv</div></div>',
            unsafe_allow_html=True,
        )
    with d_col2:
        holds_logged = len(df_dec[df_dec["action"] == "HOLD"]) if not df_dec.empty else 0
        st.markdown(
            f'<div class="metric-card"><div class="metric-title">Operator Holds</div>'
            f'<div class="metric-val">{holds_logged}</div>'
            f'<div class="metric-sub">Funds frozen pending KYC</div></div>',
            unsafe_allow_html=True,
        )
    with d_col3:
        escalations_logged = len(df_dec[df_dec["action"] == "ESCALATE"]) if not df_dec.empty else 0
        st.markdown(
            f'<div class="metric-card"><div class="metric-title">Operator Escalations</div>'
            f'<div class="metric-val">{escalations_logged}</div>'
            f'<div class="metric-sub">Referred to Legal / Law Enforcement</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("### 📜 Real-Time Audit Log")
    if not df_dec.empty:
        st.dataframe(df_dec.sort_values(by="timestamp", ascending=False), use_container_width=True, hide_index=True)
        csv_data = df_dec.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Compliance Audit Trail (CSV)",
            data=csv_data,
            file_name=f"sentinel_audit_trail_{datetime.date.today()}.csv",
            mime="text/csv",
        )
    else:
        st.info("No human decisions logged yet. Use Tab 3 (Case File) to log Hold, Release, or Escalate actions.")


# =============================================================================
# TAB 8: MODEL CARD & ETHICS
# =============================================================================
with tab8:
    st.markdown('<p class="tab-desc">Model architecture documentation, ethical governance boundaries, and regulatory compliance standards.</p>', unsafe_allow_html=True)

    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown("### 🔬 Model Specifications")
        st.markdown(
            """
            - **Architecture:** `RandomForestClassifier` (200 trees, `min_samples_leaf=5`, `class_weight='balanced_subsample'`)
            - **Anomaly Detector:** `IsolationForest` (100 trees, trained on training period only)
            - **PR-AUC Benchmark:** `0.3371` (~53x lift over random guessing baseline of 0.63%)
            - **ROC-AUC Benchmark:** `0.7810`
            """
        )

        st.markdown("#### Precision & Recall Across Operating Thresholds")
        threshold_table = pd.DataFrame([
            {"Threshold": 0.10, "Precision": "12.67%", "Recall": "47.24%", "F1-Score": 0.1999, "Operating Policy": "Strict (High Capture)"},
            {"Threshold": 0.30, "Precision": "28.14%", "Recall": "38.50%", "F1-Score": 0.3251, "Operating Policy": "Balanced Screening"},
            {"Threshold": 0.50, "Precision": "53.98%", "Recall": "32.21%", "F1-Score": 0.4035, "Operating Policy": "Balanced (Optimal F1)"},
            {"Threshold": 0.90, "Precision": "97.65%", "Recall": "12.73%", "F1-Score": 0.2252, "Operating Policy": "Lenient (High Precision)"},
        ])
        st.dataframe(threshold_table, use_container_width=True, hide_index=True)

    with m_col2:
        st.markdown("### 🛡️ Feature Governance & Leakage Prevention")
        st.markdown(
            """
            - **Active Features:**
              1. `amount`: Raw transaction monetary scale
              2. `log_amount`: Log transformation compressing extreme outliers
              3. `is_transfer`: Binary indicator (1 for TRANSFER, 0 for CASH_OUT)
              4. `hour`: Diurnal step time (step % 24)
            - **Strictly Excluded Columns:**
              - `oldbalanceOrg`, `newbalanceOrig`, `oldbalanceDest`, `newbalanceDest`
              - *Rationale:* Balance columns create direct arithmetic data leakage, producing artificially inflated metrics that fail completely in real-world delayed-settlement environments.
            """
        )

    st.markdown("---")

    e_col1, e_col2 = st.columns(2)
    with e_col1:
        st.markdown("### ⚖️ Ethical Governance & Human-in-the-Loop")
        st.markdown(
            """
            - **Decision Ownership:** AI models and algorithmic rules screen and flag risk scores; LLM agents only synthesize verified facts.
            - **Human Supremacy:** Automated systems do not unilaterally freeze legitimate customer accounts indefinitely without human investigator review.
            - **Data Disclosures:** Evaluated on PaySim synthetic financial simulation (15% uniform random sample).
            """
        )

    with e_col2:
        st.markdown("### 🏛️ Regulatory Compliance Alignment")
        st.markdown(
            """
            - **Digital Personal Data Protection (DPDP) Act 2023 (India):**
              - Strict data minimization: PII and balance records are omitted from inference payloads.
              - Purpose limitation: Transaction history is queried on a need-to-know basis strictly for fraud prevention.
            - **Reserve Bank of India (RBI) Cyber Security & Fraud Guidelines:**
              - Real-time transaction velocity monitoring.
              - Mandatory audit trails for all human and automated interventions (`outputs/decisions.csv`).
              - Dual-stage alerting for high-value fund movements exceeding the 99th percentile threshold.
            """
        )
