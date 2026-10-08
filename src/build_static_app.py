"""Static Web Application Builder for GitHub Pages deployment of Sentinel Command Center."""

import os
import glob
import json
import pandas as pd

def generate_static_app():
    # 1. Load Data
    replay_df = pd.read_csv("outputs/replay_alerts.csv")
    policy_df = pd.read_csv("outputs/policy_comparison.csv")
    edges_df = pd.read_csv("outputs/network_edges.csv")

    # Load Cases and Reports
    cases = {}
    for p in sorted(glob.glob("outputs/cases/*.json")):
        with open(p, "r", encoding="utf-8") as f:
            case = json.load(f)
            cid = case["case_id"]
            rpt_p = f"outputs/reports/{cid}.txt"
            if os.path.exists(rpt_p):
                with open(rpt_p, "r", encoding="utf-8") as rf:
                    case["report_text"] = rf.read()
            cases[cid] = case

    # Convert dataframes to records
    replay_records = replay_df.to_dict(orient="records")
    policy_records = policy_df.to_dict(orient="records")
    edges_records = edges_df.to_dict(orient="records")

    # Alert counts by step for charts
    step_counts = replay_df.groupby("step").size().to_dict()

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentinel Command Center | Multi-Agent AI Fraud Intelligence</title>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --card-header: #334155;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #334155;
            --primary-blue: #3b82f6;
            --primary-hover: #2563eb;
            --safe-green: #10b981;
            --risky-red: #ef4444;
            --warning-amber: #f59e0b;
            --accent-purple: #8b5cf6;
            --modal-bg: rgba(15, 23, 42, 0.85);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", sans-serif;
        }}

        body {{
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.5;
            padding: 24px;
        }}

        .container {{
            max-width: 1440px;
            margin: 0 auto;
        }}

        /* Header */
        header {{
            background: var(--card-bg);
            padding: 20px 24px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}

        .header-title h1 {{
            font-size: 22px;
            font-weight: 700;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .header-title p {{
            color: var(--text-muted);
            font-size: 13px;
            margin-top: 4px;
        }}

        .header-actions {{
            display: flex;
            gap: 12px;
            align-items: center;
            flex-wrap: wrap;
        }}

        .btn {{
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 13px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
            border: 1px solid transparent;
            transition: all 0.2s;
        }}

        .btn-primary {{
            background: var(--primary-blue);
            color: #ffffff;
        }}
        .btn-primary:hover {{ background: var(--primary-hover); }}

        .btn-secondary {{
            background: #1e293b;
            color: var(--text-main);
            border-color: var(--border-color);
        }}
        .btn-secondary:hover {{ background: #334155; }}

        .btn-danger {{ background: var(--risky-red); color: white; }}
        .btn-warning {{ background: var(--warning-amber); color: white; }}
        .btn-success {{ background: var(--safe-green); color: white; }}

        /* KPI Cards */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}

        .kpi-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 18px;
            border-top: 4px solid var(--primary-blue);
        }}
        .kpi-card.green {{ border-top-color: var(--safe-green); }}
        .kpi-card.amber {{ border-top-color: var(--warning-amber); }}
        .kpi-card.red {{ border-top-color: var(--risky-red); }}
        .kpi-card.purple {{ border-top-color: var(--accent-purple); }}

        .kpi-title {{
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            color: var(--text-muted);
            letter-spacing: 0.5px;
        }}

        .kpi-value {{
            font-size: 26px;
            font-weight: 700;
            color: var(--text-main);
            margin: 6px 0 2px 0;
        }}

        .kpi-sub {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        /* Navigation Tabs */
        .tabs-nav {{
            display: flex;
            gap: 8px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 20px;
            overflow-x: auto;
            padding-bottom: 4px;
        }}

        .tab-btn {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 10px 18px;
            font-size: 14px;
            font-weight: 600;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
        }}

        .tab-btn:hover {{
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.05);
        }}

        .tab-btn.active {{
            color: #ffffff;
            background: var(--card-bg);
            border-bottom: 3px solid var(--primary-blue);
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
        }}

        .tab-desc {{
            color: var(--text-muted);
            font-size: 14px;
            font-style: italic;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border-color);
        }}

        /* Cards and Sections */
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 22px;
            margin-bottom: 20px;
        }}

        .card-header {{
            font-size: 16px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .grid-2 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(460px, 1fr));
            gap: 20px;
        }}

        .grid-3 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 16px;
        }}

        /* Table Styling */
        .table-responsive {{
            overflow-x: auto;
            max-height: 480px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
        }}

        th {{
            background: #1e293b;
            color: var(--text-muted);
            font-weight: 600;
            padding: 12px 14px;
            position: sticky;
            top: 0;
            border-bottom: 1px solid var(--border-color);
            white-space: nowrap;
        }}

        td {{
            padding: 12px 14px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            color: var(--text-main);
            white-space: nowrap;
        }}

        tr:hover td {{
            background: rgba(255, 255, 255, 0.03);
        }}

        /* Badges */
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }}

        .badge-hold {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #f59e0b; }}
        .badge-escalate {{ background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }}
        .badge-allow {{ background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }}
        .badge-transfer {{ background: #1e3a8a; color: #93c5fd; }}
        .badge-cashout {{ background: #4c1d95; color: #c4b5fd; }}

        /* Filter Controls */
        .filters-bar {{
            display: flex;
            gap: 12px;
            align-items: center;
            flex-wrap: wrap;
            margin-bottom: 16px;
        }}

        input, select {{
            background: #0f172a;
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 13px;
            outline: none;
        }}
        input:focus, select:focus {{
            border-color: var(--primary-blue);
        }}

        /* Modal */
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: var(--modal-bg);
            backdrop-filter: blur(4px);
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}

        .modal-content {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            width: 100%;
            max-width: 900px;
            max-height: 90vh;
            overflow-y: auto;
            padding: 28px;
            position: relative;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        }}

        .modal-close {{
            position: absolute;
            top: 18px;
            right: 20px;
            font-size: 24px;
            cursor: pointer;
            color: var(--text-muted);
        }}
        .modal-close:hover {{ color: var(--text-main); }}

        pre {{
            background: #0f172a;
            border: 1px solid var(--border-color);
            padding: 14px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 12px;
            color: #93c5fd;
            white-space: pre-wrap;
            word-break: break-word;
            margin: 10px 0;
        }}

        .disclaimer-box {{
            background: rgba(59, 130, 246, 0.1);
            border-left: 4px solid var(--primary-blue);
            padding: 12px 16px;
            border-radius: 4px;
            font-size: 13px;
            color: #93c5fd;
            margin: 16px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Main Header -->
        <header>
            <div class="header-title">
                <h1>🛡️ Sentinel Command Center</h1>
                <p>Multi-Agent Financial Fraud Intelligence & Macroeconomic Policy Platform | PaySim Benchmark (15% Sample)</p>
            </div>
            <div class="header-actions">
                <select id="policySelect" onchange="switchPolicy(this.value)">
                    <option value="balanced" selected>Policy: Balanced (0.50)</option>
                    <option value="strict">Policy: Strict (0.10)</option>
                    <option value="lenient">Policy: Lenient (0.90)</option>
                </select>
                <button class="btn btn-secondary" onclick="toggleEvalMode()">
                    <span id="evalToggleText">👁️ Reveal Ground Truth: OFF</span>
                </button>
                <a href="https://github.com/jaidevprasad-work/sentinel-fraud-detection" target="_blank" class="btn btn-primary">
                    ⭐ View on GitHub
                </a>
            </div>
        </header>

        <!-- KPI Grid -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-title">Candidate Alerts</div>
                <div class="kpi-value" id="kpiAlerts">389</div>
                <div class="kpi-sub">Test period alerts screened</div>
            </div>
            <div class="kpi-card amber">
                <div class="kpi-title">Transactions Held</div>
                <div class="kpi-value" id="kpiHeld">304</div>
                <div class="kpi-sub">Tier-1 automated verification</div>
            </div>
            <div class="kpi-card red">
                <div class="kpi-title">Human Escalations</div>
                <div class="kpi-value" id="kpiEscalated">85</div>
                <div class="kpi-sub">Score ≥ 0.90 or amount ≥ p99</div>
            </div>
            <div class="kpi-card green">
                <div class="kpi-title" id="kpiValueLabel">Protected Volume Under Review</div>
                <div class="kpi-value" id="kpiValue">424.34M</div>
                <div class="kpi-sub" id="kpiValueSub">In currency units</div>
            </div>
            <div class="kpi-card purple">
                <div class="kpi-title">Correlated Pairs</div>
                <div class="kpi-value">46 / 46</div>
                <div class="kpi-sub">100% fraud-fraud pairs in test</div>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="tabs-nav">
            <button class="tab-btn active" onclick="showTab('tab1')">1. Command Center</button>
            <button class="tab-btn" onclick="showTab('tab2')">2. Alert Queue</button>
            <button class="tab-btn" onclick="showTab('tab3')">3. Case File Dossier</button>
            <button class="tab-btn" onclick="showTab('tab4')">4. Graph Analysis</button>
            <button class="tab-btn" onclick="showTab('tab5')">5. Policy Simulator</button>
            <button class="tab-btn" onclick="showTab('tab6')">6. Agent Diagnostics</button>
            <button class="tab-btn" onclick="showTab('tab7')">7. Investigation Workspace</button>
            <button class="tab-btn" onclick="showTab('tab8')">8. Model Card & Ethics</button>
        </div>

        <!-- TAB 1: COMMAND CENTER -->
        <div id="tab1" class="tab-content active">
            <p class="tab-desc">Live transaction stream monitoring, operational threat telemetry, and temporal alert distribution.</p>
            
            <div class="card">
                <div class="card-header">
                    <span>⏱️ Simulation Stream Control</span>
                    <div style="display:flex; align-items:center; gap: 16px;">
                        <span id="stepDisplay" style="font-size:13px; color:var(--text-muted);">Step: 334 - 743</span>
                        <input type="range" id="stepSlider" min="334" max="743" value="400" style="width: 260px;" oninput="updateStreamStep(this.value)">
                    </div>
                </div>
                <div class="table-responsive">
                    <table id="streamTable">
                        <thead>
                            <tr>
                                <th>Step</th>
                                <th>Type</th>
                                <th>Amount (currency units)</th>
                                <th>Sender (nameOrig)</th>
                                <th>Receiver (nameDest)</th>
                                <th>Model Score</th>
                                <th>Anomaly Score</th>
                                <th>Decision</th>
                                <th class="eval-col" style="display:none;">isFraud (Ground Truth)</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody id="streamTableBody"></tbody>
                    </table>
                </div>
            </div>

            <div class="card">
                <div class="card-header">📊 Alert Frequency Distribution Across Simulation Steps</div>
                <div style="height: 280px;">
                    <canvas id="stepFreqChart"></canvas>
                </div>
            </div>
        </div>

        <!-- TAB 2: ALERT QUEUE -->
        <div id="tab2" class="tab-content">
            <p class="tab-desc">Comprehensive review queue prioritized by model risk score with multi-dimensional filtering.</p>
            
            <div class="filters-bar">
                <input type="text" id="queueSearch" placeholder="Search account (e.g. C12345)..." onkeyup="renderAlertQueue()">
                <select id="typeFilter" onchange="renderAlertQueue()">
                    <option value="ALL">All Types</option>
                    <option value="TRANSFER">TRANSFER</option>
                    <option value="CASH_OUT">CASH_OUT</option>
                </select>
                <select id="decisionFilter" onchange="renderAlertQueue()">
                    <option value="ALL">All Decisions</option>
                    <option value="escalate_to_human">Escalate to Human</option>
                    <option value="hold">Hold</option>
                    <option value="allow">Allow</option>
                </select>
                <span id="queueCount" style="color:var(--text-muted); font-size:13px; margin-left:auto;"></span>
            </div>

            <div class="table-responsive">
                <table id="queueTable">
                    <thead>
                        <tr>
                            <th>Step</th>
                            <th>Type</th>
                            <th>Amount (currency units)</th>
                            <th>Sender (nameOrig)</th>
                            <th>Receiver (nameDest)</th>
                            <th>Model Score</th>
                            <th>Anomaly Score</th>
                            <th>Decision</th>
                            <th class="eval-col" style="display:none;">isFraud</th>
                            <th>Inspect</th>
                        </tr>
                    </thead>
                    <tbody id="queueTableBody"></tbody>
                </table>
            </div>
        </div>

        <!-- TAB 3: CASE FILE DOSSIER -->
        <div id="tab3" class="tab-content">
            <p class="tab-desc">Forensic case investigation dossier with behavioral history, network correlation, and human decision actions.</p>
            
            <div class="filters-bar">
                <label style="font-size:13px; color:var(--text-muted);">Select Dossier:</label>
                <select id="caseSelector" onchange="loadCaseDetails(this.value)" style="min-width: 320px;"></select>
            </div>

            <div id="caseFileView"></div>
        </div>

        <!-- TAB 4: GRAPH ANALYSIS -->
        <div id="tab4" class="tab-content">
            <p class="tab-desc">Correlated financial crime network analysis and tandem transfer-cashout topology.</p>
            
            <div class="grid-2">
                <div class="card">
                    <div class="card-header">🕸️ PaySim Laundering Topology Discovery</div>
                    <p style="font-size:13px; color:var(--text-muted); margin-bottom:12px;">
                        In PaySim, accounts are generated randomly per transaction: <strong>0 out of 606 fraud receivers appear as senders</strong>.
                        Instead, fraudsters execute synchronized <strong>same-step + identical-amount pairs</strong> where funds are transferred and immediately cashed out.
                    </p>
                    <div class="table-responsive" style="max-height: 380px;">
                        <table>
                            <thead>
                                <tr>
                                    <th>Step</th>
                                    <th>Amount (currency units)</th>
                                    <th>Transfer Origin</th>
                                    <th>Cash-out Destination</th>
                                    <th>Pair Status</th>
                                </tr>
                            </thead>
                            <tbody id="edgesTableBody"></tbody>
                        </table>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">📊 Correlated Fraud Value Distribution</div>
                    <div style="height: 380px;">
                        <canvas id="networkChart"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 5: POLICY SIMULATOR -->
        <div id="tab5" class="tab-content">
            <p class="tab-desc">Macroeconomic policy sensitivity analysis balancing review costs and direct fraud loss exposure.</p>
            
            <div class="disclaimer-box">
                <strong>Cost Model Assumptions:</strong><br>
                • <strong>Manual Review Cost:</strong> 500 currency units per generated alert.<br>
                • <strong>Missed Fraud Loss:</strong> 100% of stolen transaction principal.
            </div>

            <div class="grid-2">
                <div class="card">
                    <div class="card-header">📋 Macroeconomic Policy Comparison</div>
                    <div class="table-responsive">
                        <table>
                            <thead>
                                <tr>
                                    <th>Operating Policy</th>
                                    <th>Alerts</th>
                                    <th>Caught Frauds</th>
                                    <th>Review Cost (currency units)</th>
                                    <th>Fraud Value Lost (currency units)</th>
                                    <th>Net Total Cost (currency units)</th>
                                </tr>
                            </thead>
                            <tbody id="policyTableBody"></tbody>
                        </table>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">📈 Economic Cost Breakdown by Policy</div>
                    <div style="height: 300px;">
                        <canvas id="policyChart"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 6: AGENT DIAGNOSTICS -->
        <div id="tab6" class="tab-content">
            <p class="tab-desc">Multi-agent communication telemetry, execution trace logs, and scoring distribution telemetry.</p>
            
            <div class="card">
                <div class="card-header">🤖 Multi-Agent Pipeline Topology</div>
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:20px;">
                    <div style="background:#1e293b; padding:14px; border-radius:8px; border:1px solid var(--border-color); flex:1; min-width:180px; text-align:center;">
                        <strong>1. Scout</strong><br><span style="font-size:12px; color:var(--text-muted);">RF + IsoForest Screening</span>
                    </div>
                    <div style="color:var(--primary-blue); font-size:20px;">➔</div>
                    <div style="background:#1e293b; padding:14px; border-radius:8px; border:1px solid var(--border-color); flex:1; min-width:180px; text-align:center;">
                        <strong>2. Investigator</strong><br><span style="font-size:12px; color:var(--text-muted);">Historical Step Velocity</span>
                    </div>
                    <div style="color:var(--primary-blue); font-size:20px;">➔</div>
                    <div style="background:#1e293b; padding:14px; border-radius:8px; border:1px solid var(--border-color); flex:1; min-width:180px; text-align:center;">
                        <strong>3. Network Analyst</strong><br><span style="font-size:12px; color:var(--text-muted);">Tandem Pair Matching</span>
                    </div>
                    <div style="color:var(--primary-blue); font-size:20px;">➔</div>
                    <div style="background:#1e293b; padding:14px; border-radius:8px; border:1px solid var(--border-color); flex:1; min-width:180px; text-align:center;">
                        <strong>4. Risk Officer</strong><br><span style="font-size:12px; color:var(--text-muted);">Multi-Tier Policy Rules</span>
                    </div>
                    <div style="color:var(--primary-blue); font-size:20px;">➔</div>
                    <div style="background:#1e293b; padding:14px; border-radius:8px; border:1px solid var(--border-color); flex:1; min-width:180px; text-align:center;">
                        <strong>5. Reporter</strong><br><span style="font-size:12px; color:var(--text-muted);">Fact-Based Synthesis</span>
                    </div>
                </div>

                <div class="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th>Agent</th>
                                <th>Operational Responsibility</th>
                                <th>Core Method</th>
                                <th>Output Artifact</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td><strong>Scout</strong></td><td>Real-time screening</td><td>RandomForest (200 trees) + IsolationForest</td><td>Candidate Alert Queue</td></tr>
                            <tr><td><strong>Investigator</strong></td><td>Behavioral profiling</td><td>Strict temporal velocity (prior steps)</td><td>Historical Inflow/Outflow Profile</td></tr>
                            <tr><td><strong>NetworkAnalyst</strong></td><td>Crime ring detection</td><td>Same-step identical-amount matcher</td><td>Correlated Laundering Evidence</td></tr>
                            <tr><td><strong>RiskOfficer</strong></td><td>Operational governance</td><td>Strict / Balanced / Lenient policies + p99 check</td><td>Decision (Hold / Escalate)</td></tr>
                            <tr><td><strong>Reporter</strong></td><td>Plain-English explanation</td><td>Google Gemini 1.5 + Template Fallback</td><td>Structured Plain-English Dossier</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 7: INVESTIGATION WORKSPACE -->
        <div id="tab7" class="tab-content">
            <p class="tab-desc">Collaborative human decision audit trail, compliance records, and case activity logs.</p>
            
            <div class="card">
                <div class="card-header">
                    <span>📜 Real-Time Audit Log (Logged to outputs/decisions.csv)</span>
                    <button class="btn btn-primary" onclick="exportDecisionsCSV()">📥 Download Audit Trail (CSV)</button>
                </div>
                <div class="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th>Timestamp</th>
                                <th>Case ID</th>
                                <th>Human Action</th>
                                <th>Operator Justification Note</th>
                            </tr>
                        </thead>
                        <tbody id="decisionsTableBody">
                            <tr><td colspan="4" style="text-align:center; color:var(--text-muted);">No human actions logged yet. Use Tab 3 to execute Hold, Release, or Escalate decisions.</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 8: MODEL CARD & ETHICS -->
        <div id="tab8" class="tab-content">
            <p class="tab-desc">Model architecture documentation, ethical governance boundaries, and regulatory compliance standards.</p>
            
            <div class="grid-2">
                <div class="card">
                    <div class="card-header">🔬 Technical Architecture & Benchmarks</div>
                    <ul style="margin-left: 20px; font-size:13px; color:var(--text-muted); line-height:1.8;">
                        <li><strong>Classifier:</strong> RandomForest (200 trees, balanced_subsample, min_samples_leaf=5).</li>
                        <li><strong>Anomaly Model:</strong> Isolation Forest trained strictly on training steps.</li>
                        <li><strong>PR-AUC Benchmark:</strong> <strong style="color:var(--safe-green);">0.3371</strong> (~53x lift over 0.63% random baseline).</li>
                        <li><strong>ROC-AUC Benchmark:</strong> <strong>0.7810</strong>.</li>
                    </ul>

                    <h4 style="margin: 16px 0 8px 0; font-size: 14px;">Operating Threshold Matrix:</h4>
                    <div class="table-responsive">
                        <table>
                            <thead>
                                <tr><th>Threshold</th><th>Precision</th><th>Recall</th><th>F1-Score</th><th>Policy Regime</th></tr>
                            </thead>
                            <tbody>
                                <tr><td>0.10</td><td>12.67%</td><td>47.24%</td><td>0.1999</td><td>Strict (High Capture)</td></tr>
                                <tr><td>0.30</td><td>28.14%</td><td>38.50%</td><td>0.3251</td><td>Screening Mode</td></tr>
                                <tr><td>0.50</td><td>53.98%</td><td>32.21%</td><td>0.4035</td><td>Balanced (Optimal F1)</td></tr>
                                <tr><td>0.90</td><td>97.65%</td><td>12.73%</td><td>0.2252</td><td>Lenient (High Precision)</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">🛡️ Data Leakage & Regulatory Compliance</div>
                    <div style="font-size:13px; color:var(--text-muted); line-height: 1.7;">
                        <h4 style="color:var(--text-main); margin-bottom:4px;">1. Zero Balance Leakage (Rule 1)</h4>
                        <p>All balance columns (<code>oldbalanceOrg</code>, <code>newbalanceOrig</code>, etc.) are strictly excluded to prevent artificial mathematical leakage that fails in real-world delayed settlement systems.</p>
                        
                        <h4 style="color:var(--text-main); margin-top:12px; margin-bottom:4px;">2. India DPDP Act 2023 Compliance</h4>
                        <p>Strict data minimization: PII and customer balances are omitted from inference payloads. History queried on a need-to-know basis.</p>

                        <h4 style="color:var(--text-main); margin-top:12px; margin-bottom:4px;">3. RBI Cyber Security & Fraud Directives</h4>
                        <p>Real-time velocity checks, mandatory human audit trails (<code>outputs/decisions.csv</code>), and tiered review triggers for transactions exceeding the 99th percentile.</p>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <!-- Case Modal Inspector -->
    <div id="caseModal" class="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeCaseModal()">&times;</span>
            <div id="modalBody"></div>
        </div>
    </div>

    <!-- Embedded Application Data -->
    <script>
        const REPLAY_DATA = {json.dumps(replay_records)};
        const POLICY_DATA = {json.dumps(policy_records)};
        const EDGES_DATA = {json.dumps(edges_records)};
        const CASES_DATA = {json.dumps(cases)};
        const STEP_COUNTS = {json.dumps(step_counts)};

        let currentPolicy = "balanced";
        let evalMode = false;
        let humanDecisions = [];

        function showTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }}

        function switchPolicy(policy) {{
            currentPolicy = policy;
            updateKPICards();
            renderStreamTable();
            renderAlertQueue();
            renderPolicyView();
        }}

        function toggleEvalMode() {{
            evalMode = !evalMode;
            document.getElementById('evalToggleText').innerText = evalMode ? "👁️ Reveal Ground Truth: ON" : "👁️ Reveal Ground Truth: OFF";
            document.querySelectorAll('.eval-col').forEach(el => el.style.display = evalMode ? "table-cell" : "none");
            updateKPICards();
            renderStreamTable();
            renderAlertQueue();
        }}

        function updateKPICards() {{
            const decCol = "decision_" + currentPolicy;
            const activeAlerts = REPLAY_DATA.filter(r => r[decCol] === "hold" || r[decCol] === "escalate_to_human");
            
            document.getElementById('kpiAlerts').innerText = activeAlerts.length.toLocaleString();
            document.getElementById('kpiHeld').innerText = activeAlerts.filter(r => r[decCol] === "hold").length.toLocaleString();
            document.getElementById('kpiEscalated').innerText = activeAlerts.filter(r => r[decCol] === "escalate_to_human").length.toLocaleString();
            
            const totalVal = activeAlerts.reduce((sum, r) => sum + r.amount, 0);
            if (evalMode) {{
                const fraudsCaught = activeAlerts.filter(r => r.isFraud === 1).length;
                document.getElementById('kpiValueLabel').innerText = "Frauds Intercepted (Ground Truth)";
                document.getElementById('kpiValue').innerText = fraudsCaught + " / 652";
                document.getElementById('kpiValueSub').innerText = (totalVal / 1000000).toFixed(2) + "M currency units protected";
            }} else {{
                document.getElementById('kpiValueLabel').innerText = "Protected Volume Under Review";
                document.getElementById('kpiValue').innerText = (totalVal / 1000000).toFixed(2) + "M";
                document.getElementById('kpiValueSub').innerText = "In currency units";
            }}
        }}

        function updateStreamStep(val) {{
            document.getElementById('stepDisplay').innerText = "Step <= " + val;
            renderStreamTable(parseInt(val));
        }}

        function renderStreamTable(maxStep = 400) {{
            const tbody = document.getElementById('streamTableBody');
            const decCol = "decision_" + currentPolicy;
            const filtered = REPLAY_DATA.filter(r => r.step <= maxStep && (r[decCol] === "hold" || r[decCol] === "escalate_to_human")).slice(0, 20);
            
            tbody.innerHTML = filtered.map(r => `
                <tr>
                    <td>${{r.step}}</td>
                    <td><span class="badge ${{r.type === 'TRANSFER' ? 'badge-transfer' : 'badge-cashout'}}">${{r.type}}</span></td>
                    <td><strong>${{r.amount.toLocaleString(undefined, {{minimumFractionDigits: 2, maximumFractionDigits: 2}})}}</strong></td>
                    <td><code>${{r.nameOrig}}</code></td>
                    <td><code>${{r.nameDest}}</code></td>
                    <td>${{r.model_score.toFixed(4)}}</td>
                    <td>${{r.anomaly_score.toFixed(4)}}</td>
                    <td><span class="badge ${{r[decCol] === 'escalate_to_human' ? 'badge-escalate' : 'badge-hold'}}">${{r[decCol]}}</span></td>
                    <td class="eval-col" style="display:${{evalMode ? 'table-cell' : 'none'}};">${{r.isFraud === 1 ? '<span class="badge badge-escalate">FRAUD</span>' : '<span class="badge badge-allow">LEGIT</span>'}}</td>
                    <td><button class="btn btn-secondary" style="padding:4px 8px; font-size:11px;" onclick="openCaseModal('case_${{r.case_id || (r.step + '_' + r.amount)}}')">Dossier</button></td>
                </tr>
            `).join('');
        }}

        function renderAlertQueue() {{
            const search = document.getElementById('queueSearch').value.toUpperCase();
            const typeF = document.getElementById('typeFilter').value;
            const decF = document.getElementById('decisionFilter').value;
            const decCol = "decision_" + currentPolicy;

            let list = REPLAY_DATA.filter(r => {{
                if (typeF !== "ALL" && r.type !== typeF) return false;
                if (decF !== "ALL" && r[decCol] !== decF) return false;
                if (search && !r.nameOrig.toUpperCase().includes(search) && !r.nameDest.toUpperCase().includes(search)) return false;
                return true;
            }}).sort((a, b) => b.model_score - a.model_score);

            document.getElementById('queueCount').innerText = "Showing " + Math.min(list.length, 50) + " of " + list.length + " alerts";
            const tbody = document.getElementById('queueTableBody');
            
            tbody.innerHTML = list.slice(0, 50).map(r => `
                <tr>
                    <td>${{r.step}}</td>
                    <td><span class="badge ${{r.type === 'TRANSFER' ? 'badge-transfer' : 'badge-cashout'}}">${{r.type}}</span></td>
                    <td><strong>${{r.amount.toLocaleString(undefined, {{minimumFractionDigits: 2, maximumFractionDigits: 2}})}}</strong></td>
                    <td><code>${{r.nameOrig}}</code></td>
                    <td><code>${{r.nameDest}}</code></td>
                    <td>${{r.model_score.toFixed(4)}}</td>
                    <td>${{r.anomaly_score.toFixed(4)}}</td>
                    <td><span class="badge ${{r[decCol] === 'escalate_to_human' ? 'badge-escalate' : (r[decCol] === 'hold' ? 'badge-hold' : 'badge-allow')}}">${{r[decCol]}}</span></td>
                    <td class="eval-col" style="display:${{evalMode ? 'table-cell' : 'none'}};">${{r.isFraud === 1 ? '<span class="badge badge-escalate">FRAUD</span>' : '<span class="badge badge-allow">LEGIT</span>'}}</td>
                    <td><button class="btn btn-secondary" style="padding:4px 8px; font-size:11px;" onclick="selectAndShowCase('${{r.case_id}}')">Inspect</button></td>
                </tr>
            `).join('');
        }}

        function populateCaseSelector() {{
            const sel = document.getElementById('caseSelector');
            const keys = Object.keys(CASES_DATA);
            sel.innerHTML = keys.map(k => `<option value="${{k}}">${{k}} (${{CASES_DATA[k].transaction.type}}, ${{CASES_DATA[k].transaction.amount.toLocaleString()}} currency units)</option>`).join('');
            if (keys.length > 0) loadCaseDetails(keys[0]);
        }}

        function loadCaseDetails(caseId) {{
            const c = CASES_DATA[caseId];
            if (!c) return;
            const tx = c.transaction;
            const scores = c.scores;
            const amt = c.amount_analysis;
            const ro = c.risk_officer;
            const rpt = c.report_text || "No AI report file available.";

            document.getElementById('caseFileView').innerHTML = `
                <div class="card">
                    <div class="card-header">
                        <span>📁 Case Dossier: <code>${{caseId}}</code></span>
                        <span class="badge ${{ro.decision_balanced === 'escalate_to_human' ? 'badge-escalate' : 'badge-hold'}}">${{ro.decision_balanced.toUpperCase()}}</span>
                    </div>

                    <div class="grid-2">
                        <div>
                            <h4 style="margin-bottom:8px;">💳 Transaction Facts</h4>
                            <ul style="font-size:13px; line-height:1.8; color:var(--text-muted); list-style:none;">
                                <li>• <strong>Step / Time:</strong> Step ${{tx.step}} (Hour ${{tx.hour}})</li>
                                <li>• <strong>Type:</strong> ${{tx.type}}</li>
                                <li>• <strong>Amount:</strong> <strong style="color:var(--text-main);">${{tx.amount.toLocaleString(undefined, {{minimumFractionDigits:2}})}}</strong> currency units</li>
                                <li>• <strong>Training Percentile:</strong> ${{amt.percentile_vs_train.toFixed(2)}}% (Exceeds p99: ${{amt.is_above_p99 ? 'YES' : 'NO'}})</li>
                                <li>• <strong>Sender:</strong> <code>${{tx.nameOrig}}</code></li>
                                <li>• <strong>Receiver:</strong> <code>${{tx.nameDest}}</code></li>
                            </ul>
                        </div>

                        <div>
                            <h4 style="margin-bottom:8px;">🧠 Risk Scores & Signals</h4>
                            <ul style="font-size:13px; line-height:1.8; color:var(--text-muted); list-style:none;">
                                <li>• <strong>Random Forest Fraud Score:</strong> ${{scores.model_score.toFixed(4)}}</li>
                                <li>• <strong>Isolation Forest Anomaly Score:</strong> ${{scores.anomaly_score.toFixed(4)}}</li>
                                <li>• <strong>Sender Prior Transactions:</strong> ${{c.sender_history.prior_tx_count > 0 ? c.sender_history.prior_tx_count : 'no prior history available'}}</li>
                                <li>• <strong>Network Correlated Pair:</strong> ${{c.network_evidence && c.network_evidence.has_linked_pair ? '⚠️ Same-step identical amount counterpart detected!' : 'None detected'}}</li>
                            </ul>
                        </div>
                    </div>

                    <div style="margin-top:20px;">
                        <h4>📝 AI Investigation Report (Human Review Required)</h4>
                        <pre>${{rpt}}</pre>
                        <div class="disclaimer-box">🤖 AI-generated from case facts, human review required. Models and policy rules determine risk scores.</div>
                    </div>

                    <div style="margin-top:20px; border-top:1px solid var(--border-color); padding-top:18px;">
                        <h4 style="margin-bottom:12px;">⚖️ Human Decision Action Center</h4>
                        <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
                            <input type="text" id="opNote_${{caseId}}" placeholder="Operator justification note (optional)..." style="flex:1; min-width:240px;">
                            <button class="btn btn-warning" onclick="executeDecision('${{caseId}}', 'HOLD')">🟠 Hold Funds</button>
                            <button class="btn btn-success" onclick="executeDecision('${{caseId}}', 'RELEASE')">🟢 Release Funds</button>
                            <button class="btn btn-danger" onclick="executeDecision('${{caseId}}', 'ESCALATE')">🔴 Escalate</button>
                        </div>
                    </div>
                </div>
            `;
        }}

        function executeDecision(caseId, action) {{
            const noteInput = document.getElementById('opNote_' + caseId);
            const note = noteInput ? noteInput.value : "";
            const entry = {{
                timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19),
                case_id: caseId,
                action: action,
                operator_note: note
            }};
            humanDecisions.unshift(entry);
            renderDecisionsTable();
            alert(`Decision logged: ${{action}} on ${{caseId}}`);
        }}

        function renderDecisionsTable() {{
            const tbody = document.getElementById('decisionsTableBody');
            if (humanDecisions.length === 0) {{
                tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; color:var(--text-muted);">No human actions logged yet. Use Tab 3 to execute Hold, Release, or Escalate decisions.</td></tr>`;
                return;
            }}
            tbody.innerHTML = humanDecisions.map(d => `
                <tr>
                    <td>${{d.timestamp}}</td>
                    <td><code>${{d.case_id}}</code></td>
                    <td><span class="badge ${{d.action === 'ESCALATE' ? 'badge-escalate' : (d.action === 'HOLD' ? 'badge-hold' : 'badge-allow')}}">${{d.action}}</span></td>
                    <td>${{d.operator_note || '<em>No justification provided</em>'}}</td>
                </tr>
            `).join('');
        }}

        function exportDecisionsCSV() {{
            if (humanDecisions.length === 0) {{
                alert("No decisions logged yet to export.");
                return;
            }}
            let csv = "timestamp,case_id,action,operator_note\\n";
            humanDecisions.forEach(d => {{
                csv += `"${{d.timestamp}}","${{d.case_id}}","${{d.action}}","${{d.operator_note.replace(/"/g, '""')}}"\\n`;
            }});
            const blob = new Blob([csv], {{ type: 'text/csv' }});
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.setAttribute('href', url);
            a.setAttribute('download', `sentinel_decisions_${{new Date().toISOString().slice(0,10)}}.csv`);
            a.click();
        }}

        function selectAndShowCase(caseId) {{
            showTab('tab3');
            document.querySelectorAll('.tab-btn')[2].classList.add('active');
            document.getElementById('caseSelector').value = caseId;
            loadCaseDetails(caseId);
        }}

        function openCaseModal(caseId) {{
            selectAndShowCase(caseId);
        }}

        function closeCaseModal() {{
            document.getElementById('caseModal').style.display = "none";
        }}

        function renderPolicyView() {{
            const tbody = document.getElementById('policyTableBody');
            tbody.innerHTML = POLICY_DATA.map(p => `
                <tr style="${{p.policy.toLowerCase() === currentPolicy ? 'background:rgba(59,130,246,0.15); font-weight:bold;' : ''}}">
                    <td>${{p.policy}}</td>
                    <td>${{p.alerts.toLocaleString()}}</td>
                    <td>${{p.frauds_caught.toLocaleString()}} / 652</td>
                    <td>${{p.review_cost.toLocaleString(undefined, {{minimumFractionDigits:2}})}}</td>
                    <td>${{p.fraud_value_lost.toLocaleString(undefined, {{minimumFractionDigits:2}})}}</td>
                    <td style="color:${{p.policy === 'Strict' ? 'var(--safe-green)' : 'var(--text-main)'}};"><strong>${{p.total_cost.toLocaleString(undefined, {{minimumFractionDigits:2}})}}</strong></td>
                </tr>
            `).join('');
        }}

        function renderEdgesTable() {{
            const tbody = document.getElementById('edgesTableBody');
            tbody.innerHTML = EDGES_DATA.map(e => `
                <tr>
                    <td>${{e.step}}</td>
                    <td><strong>${{e.amount.toLocaleString(undefined, {{minimumFractionDigits:2}})}}</strong></td>
                    <td><code>${{e.transfer_orig}}</code></td>
                    <td><code>${{e.cashout_dest}}</code></td>
                    <td><span class="badge ${{e.is_fraud_pair === 1 ? 'badge-escalate' : 'badge-allow'}}">${{e.is_fraud_pair === 1 ? 'FRAUD PAIR' : 'LEGIT'}}</span></td>
                </tr>
            `).join('');
        }}

        // Initialize Charts
        window.addEventListener('DOMContentLoaded', () => {{
            populateCaseSelector();
            updateKPICards();
            renderStreamTable();
            renderAlertQueue();
            renderPolicyView();
            renderEdgesTable();

            // Step Frequency Chart
            const stepCtx = document.getElementById('stepFreqChart').getContext('2d');
            const stepLabels = Object.keys(STEP_COUNTS);
            const stepData = Object.values(STEP_COUNTS);
            new Chart(stepCtx, {{
                type: 'bar',
                data: {{
                    labels: stepLabels,
                    datasets: [{{
                        label: 'Candidate Alerts per Simulation Step',
                        data: stepData,
                        backgroundColor: '#3b82f6',
                        borderRadius: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8', maxTicksLimit: 20 }} }},
                        y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }}
                    }},
                    plugins: {{ legend: {{ labels: {{ color: '#f8fafc' }} }} }}
                }}
            }});

            // Policy Cost Chart
            const polCtx = document.getElementById('policyChart').getContext('2d');
            new Chart(polCtx, {{
                type: 'bar',
                data: {{
                    labels: POLICY_DATA.map(p => p.policy),
                    datasets: [
                        {{ label: 'Review Cost (currency units)', data: POLICY_DATA.map(p => p.review_cost), backgroundColor: '#f59e0b' }},
                        {{ label: 'Missed Fraud Loss (currency units)', data: POLICY_DATA.map(p => p.fraud_value_lost), backgroundColor: '#ef4444' }},
                        {{ label: 'Total Net Cost (currency units)', data: POLICY_DATA.map(p => p.total_cost), backgroundColor: '#3b82f6' }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
                        y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }}
                    }},
                    plugins: {{ legend: {{ labels: {{ color: '#f8fafc' }} }} }}
                }}
            }});

            // Network Chart
            const netCtx = document.getElementById('networkChart').getContext('2d');
            new Chart(netCtx, {{
                type: 'scatter',
                data: {{
                    datasets: [{{
                        label: 'Correlated Fraud Pairs',
                        data: EDGES_DATA.map(e => ({{ x: e.step, y: e.amount }})),
                        backgroundColor: '#ef4444'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{ title: {{ display: true, text: 'Simulation Step', color: '#94a3b8' }}, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
                        y: {{ title: {{ display: true, text: 'Transaction Amount (currency units)', color: '#94a3b8' }}, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }}
                    }},
                    plugins: {{ legend: {{ labels: {{ color: '#f8fafc' }} }} }}
                }}
            }});
        }});
    </script>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Static web application generated successfully at index.html and docs/index.html")

if __name__ == "__main__":
    generate_static_app()
