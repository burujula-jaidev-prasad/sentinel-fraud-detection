"""Build production-grade static web application for GitHub Pages (Sentinel Patrol)."""

import os
import json

def build_site():
    with open("docs/data/stream.json", "r", encoding="utf-8") as f:
        stream_data = json.load(f)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentinel Patrol | Multi-Agent AI Fraud Intelligence</title>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-color: #0b1120;
            --card-bg: #131d31;
            --card-header: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #1e2e4a;
            --primary-blue: #3b82f6;
            --primary-hover: #2563eb;
            --safe-green: #10b981;
            --risky-red: #ef4444;
            --warning-amber: #f59e0b;
            --accent-purple: #8b5cf6;
            --agent-scout: #38bdf8;
            --agent-inv: #a78bfa;
            --agent-net: #f472b6;
            --agent-ro: #fbbf24;
            --agent-rep: #34d399;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
        }}

        body {{
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.5;
            padding: 20px;
        }}

        .container {{
            max-width: 1480px;
            margin: 0 auto;
        }}

        /* Header */
        header {{
            background: var(--card-bg);
            padding: 18px 24px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 14px;
        }}

        .header-title h1 {{
            font-size: 22px;
            font-weight: 700;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .header-title p {{
            color: var(--text-muted);
            font-size: 13px;
            margin-top: 3px;
        }}

        .header-actions {{
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }}

        .btn {{
            padding: 8px 14px;
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

        .btn-primary {{ background: var(--primary-blue); color: #ffffff; }}
        .btn-primary:hover {{ background: var(--primary-hover); }}
        .btn-secondary {{ background: #1a2438; color: var(--text-main); border-color: var(--border-color); }}
        .btn-secondary:hover {{ background: #263550; }}
        .btn-warning {{ background: var(--warning-amber); color: white; }}
        .btn-danger {{ background: var(--risky-red); color: white; }}
        .btn-success {{ background: var(--safe-green); color: white; }}

        /* Navigation Tabs */
        .tabs-nav {{
            display: flex;
            gap: 8px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 20px;
            overflow-x: auto;
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

        .tab-btn:hover {{ color: var(--text-main); background: rgba(255, 255, 255, 0.05); }}
        .tab-btn.active {{
            color: #ffffff;
            background: var(--card-bg);
            border-bottom: 3px solid var(--primary-blue);
        }}

        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}

        .tab-desc {{
            color: var(--text-muted);
            font-size: 13px;
            font-style: italic;
            margin-bottom: 18px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-color);
        }}

        /* KPI Cards Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 14px;
            margin-bottom: 20px;
        }}

        .kpi-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 16px;
            border-top: 4px solid var(--primary-blue);
        }}
        .kpi-card.amber {{ border-top-color: var(--warning-amber); }}
        .kpi-card.red {{ border-top-color: var(--risky-red); }}
        .kpi-card.green {{ border-top-color: var(--safe-green); }}
        .kpi-card.purple {{ border-top-color: var(--accent-purple); }}

        .kpi-title {{ font-size: 11px; font-weight: 600; text-transform: uppercase; color: var(--text-muted); }}
        .kpi-value {{ font-size: 24px; font-weight: 700; color: var(--text-main); margin: 4px 0 2px 0; }}
        .kpi-sub {{ font-size: 12px; color: var(--text-muted); }}

        /* Cards and Sections */
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }}

        .card-header {{
            font-size: 15px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 14px;
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

        /* Patrol Live Screen Layout */
        .patrol-container {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
        }}
        @media (max-width: 1024px) {{
            .patrol-container {{ grid-template-columns: 1fr; }}
        }}

        /* Agent Cards */
        .agent-cards-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 10px;
            margin-bottom: 16px;
        }}

        .agent-card {{
            background: #0f172a;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
            border-left: 4px solid var(--primary-blue);
        }}
        .agent-card.scout {{ border-left-color: var(--agent-scout); }}
        .agent-card.investigator {{ border-left-color: var(--agent-inv); }}
        .agent-card.network {{ border-left-color: var(--agent-net); }}
        .agent-card.risk {{ border-left-color: var(--agent-ro); }}
        .agent-card.reporter {{ border-left-color: var(--agent-rep); }}

        .agent-name {{ font-size: 13px; font-weight: 700; color: var(--text-main); }}
        .agent-status {{ font-size: 11px; color: var(--safe-green); margin-top: 2px; }}

        /* Chat Feed */
        .chat-feed-box {{
            height: 420px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
            padding-right: 6px;
        }}

        .chat-msg {{
            background: #0f172a;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px 12px;
            font-size: 12px;
            line-height: 1.4;
        }}
        .chat-msg .sender {{ font-weight: 700; font-size: 12px; margin-bottom: 2px; }}
        .chat-msg.scout .sender {{ color: var(--agent-scout); }}
        .chat-msg.inv .sender {{ color: var(--agent-inv); }}
        .chat-msg.net .sender {{ color: var(--agent-net); }}
        .chat-msg.ro .sender {{ color: var(--agent-ro); }}
        .chat-msg.rep .sender {{ color: var(--agent-rep); }}

        /* District Canvas Map */
        #districtCanvas {{
            width: 100%;
            height: 420px;
            background: #090e1a;
            border-radius: 10px;
            border: 1px solid var(--border-color);
            display: block;
        }}

        /* Table Styling */
        .table-responsive {{
            overflow-x: auto;
            max-height: 460px;
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
            background: #182338;
            color: var(--text-muted);
            font-weight: 600;
            padding: 10px 12px;
            position: sticky;
            top: 0;
            border-bottom: 1px solid var(--border-color);
            white-space: nowrap;
        }}

        td {{
            padding: 10px 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            color: var(--text-main);
            white-space: nowrap;
        }}

        tr:hover td {{ background: rgba(255, 255, 255, 0.03); }}

        /* Badges */
        .badge {{
            display: inline-block;
            padding: 2px 7px;
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
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
            margin-bottom: 14px;
        }}

        input, select {{
            background: #0f172a;
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 7px 11px;
            border-radius: 6px;
            font-size: 13px;
            outline: none;
        }}

        .disclaimer-box {{
            background: rgba(59, 130, 246, 0.1);
            border-left: 4px solid var(--primary-blue);
            padding: 10px 14px;
            border-radius: 4px;
            font-size: 12px;
            color: #93c5fd;
            margin: 12px 0;
        }}

        pre {{
            background: #090e1a;
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
    </style>
</head>
<body>
    <div class="container">
        <!-- Main Header -->
        <header>
            <div class="header-title">
                <h1>🛡️ Sentinel Patrol & Command Center</h1>
                <p>Multi-Agent Financial Fraud Intelligence & Live PaySim Simulation Replay | Steps 334 – 743</p>
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
                <a href="https://github.com/burujula-jaidev-prasad/sentinel-fraud-detection" target="_blank" class="btn btn-primary">
                    ⭐ GitHub Source
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
            <button class="tab-btn active" onclick="showTab('tab1')">1. Sentinel Patrol</button>
            <button class="tab-btn" onclick="showTab('tab2')">2. Alert Queue</button>
            <button class="tab-btn" onclick="showTab('tab3')">3. Case File Dossier</button>
            <button class="tab-btn" onclick="showTab('tab4')">4. Policy Simulator</button>
            <button class="tab-btn" onclick="showTab('tab5')">5. Model Card & Ethics</button>
            <button class="tab-btn" onclick="showTab('tab6')">6. Market Impact (Paytm vs NIFTY 50)</button>
            <button class="tab-btn" onclick="showTab('tab7')">7. Investigation Workspace</button>
        </div>

        <!-- ========================================================================= -->
        <!-- TAB 1: SENTINEL PATROL (HOME SCREEN) -->
        <!-- ========================================================================= -->
        <div id="tab1" class="tab-content active">
            <p class="tab-desc">Sentinel Patrol live simulation replay with geospatial payment district corridors, moving transaction flows, and real-time multi-agent chat feed.</p>
            
            <div class="card" style="margin-bottom:16px;">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <button class="btn btn-primary" id="playBtn" onclick="togglePlayPause()">⏸️ Pause</button>
                        <span id="stepTicker" style="font-weight:700; font-size:14px; color:var(--safe-green);">Simulation Step: 334 (Hour 22)</span>
                    </div>
                    <div style="display:flex; align-items:center; gap:16px; flex:1; max-width:500px;">
                        <span style="font-size:12px; color:var(--text-muted);">Step:</span>
                        <input type="range" id="simStepSlider" min="334" max="743" value="334" style="flex:1;" oninput="scrubStep(this.value)">
                    </div>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:12px; color:var(--text-muted);">Speed:</span>
                        <select id="speedSelect" onchange="changeSpeed(this.value)">
                            <option value="1000">1 Step/sec</option>
                            <option value="500" selected>2 Steps/sec</option>
                            <option value="200">5 Steps/sec</option>
                            <option value="80">12 Steps/sec</option>
                        </select>
                    </div>
                </div>
                <div class="disclaimer-box" style="margin-top:10px; margin-bottom:0;">
                    ℹ️ <strong>Simulated Live Stream:</strong> Replay of PaySim test period (steps 334–743, 103,191 transactions). 1 step = 1 simulated hour. This is an offline test evaluation replay, not live bank data.
                </div>
            </div>

            <!-- Agent State Cards -->
            <div class="agent-cards-row">
                <div class="agent-card scout">
                    <div class="agent-name">🛡️ Scout</div>
                    <div class="agent-status" id="statusScout">Screening RF + Iso</div>
                </div>
                <div class="agent-card investigator">
                    <div class="agent-name">🔍 Investigator</div>
                    <div class="agent-status" id="statusInv">Prior Velocity Active</div>
                </div>
                <div class="agent-card network">
                    <div class="agent-name">🕸️ Network Analyst</div>
                    <div class="agent-status" id="statusNet">Tandem Matcher Active</div>
                </div>
                <div class="agent-card risk">
                    <div class="agent-name">⚖️ Risk Officer</div>
                    <div class="agent-status" id="statusRO">Policy: Balanced</div>
                </div>
                <div class="agent-card reporter">
                    <div class="agent-name">📝 Reporter</div>
                    <div class="agent-status" id="statusRep">Synthesis Ready</div>
                </div>
            </div>

            <!-- Patrol Main Split -->
            <div class="patrol-container">
                <div class="card" style="padding:14px;">
                    <div class="card-header">
                        <span>🗺️ Payment Corridors & District Flows</span>
                        <span style="font-size:12px; color:var(--text-muted);">Live Transaction Particle Movement</span>
                    </div>
                    <canvas id="districtCanvas" width="800" height="420"></canvas>
                </div>

                <div class="card" style="padding:14px;">
                    <div class="card-header">
                        <span>💬 Live Agent Feed</span>
                        <span id="feedCount" style="font-size:11px; color:var(--text-muted);">0 msgs</span>
                    </div>
                    <div class="chat-feed-box" id="chatFeed"></div>
                </div>
            </div>
        </div>

        <!-- ========================================================================= -->
        <!-- TAB 2: ALERT QUEUE -->
        <!-- ========================================================================= -->
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
                <table>
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

        <!-- ========================================================================= -->
        <!-- TAB 3: CASE FILE DOSSIER -->
        <!-- ========================================================================= -->
        <div id="tab3" class="tab-content">
            <p class="tab-desc">Forensic case investigation dossier with behavioral history, network correlation, and human decision actions.</p>
            
            <div class="filters-bar">
                <label style="font-size:13px; color:var(--text-muted);">Select Dossier:</label>
                <select id="caseSelector" onchange="loadCaseDetails(this.value)" style="min-width: 320px;"></select>
            </div>

            <div id="caseFileView"></div>
        </div>

        <!-- ========================================================================= -->
        <!-- TAB 4: POLICY SIMULATOR -->
        <!-- ========================================================================= -->
        <div id="tab4" class="tab-content">
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

        <!-- ========================================================================= -->
        <!-- TAB 5: MODEL CARD & ETHICS -->
        <!-- ========================================================================= -->
        <div id="tab5" class="tab-content">
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

        <!-- ========================================================================= -->
        <!-- TAB 6: MARKET IMPACT (PAYTM VS NIFTY 50) -->
        <!-- ========================================================================= -->
        <div id="tab6" class="tab-content">
            <p class="tab-desc">Macroeconomic case study: The market capitalization impact and systemic fallout of compliance and fraud governance failures in digital payments.</p>
            
            <div class="grid-2">
                <div class="card">
                    <div class="card-header">📉 Paytm Payments Bank Regulatory Fallout vs NIFTY 50</div>
                    <div style="height: 280px;">
                        <canvas id="marketChart"></canvas>
                    </div>
                    <p style="font-size:12px; color:var(--text-muted); margin-top:10px;">
                        <em>Normalized stock performance (Jan 2024 – Mar 2024). Paytm shares experienced a <strong>~55% market cap collapse</strong> following RBI directives regarding persistent non-compliance and lack of supervisory KYC controls.</em>
                    </p>
                </div>

                <div class="card">
                    <div class="card-header">🏛️ Executive Governance Lessons for Digital Payments</div>
                    <div style="font-size:13px; color:var(--text-muted); line-height: 1.7;">
                        <h4 style="color:var(--text-main); margin-bottom:4px;">1. The High Cost of Supervisory Non-Compliance</h4>
                        <p>Regulatory penalties go far beyond fines: loss of payment gateway licenses, frozen escrow accounts, and massive equity destruction occur when fraud monitoring fails.</p>

                        <h4 style="color:var(--text-main); margin-top:10px; margin-bottom:4px;">2. Multi-Tiered Alerting (Sentinel Model)</h4>
                        <p>Deploying automated screening (Scout) with mandatory dual-stage human verification (Risk Officer + Case File) guarantees regulatory audit compliance under RBI standards.</p>

                        <h4 style="color:var(--text-main); margin-top:10px; margin-bottom:4px;">3. Human-in-the-Loop Safeguards</h4>
                        <p>AI models flag risk scores, but human officers retain final binding authority on freezing accounts, fulfilling DPDP and consumer protection laws.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- ========================================================================= -->
        <!-- TAB 7: INVESTIGATION WORKSPACE -->
        <!-- ========================================================================= -->
        <div id="tab7" class="tab-content">
            <p class="tab-desc">Collaborative human decision audit trail, compliance records, and case activity logs.</p>
            
            <div class="card">
                <div class="card-header">
                    <span>📜 Human Decision Audit Log (Stored in Browser localStorage)</span>
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

    </div>

    <!-- Embedded Data & Scripts -->
    <script>
        const STREAM_DATA = {json.dumps(stream_data)};
        const ALERTS = STREAM_DATA.alerts;
        const POLICIES = STREAM_DATA.policy_comparison;
        const CASES = STREAM_DATA.cases;
        const EDGES = STREAM_DATA.network_edges;

        let currentPolicy = "balanced";
        let evalMode = false;
        let isPlaying = true;
        let currentSimStep = 334;
        let simInterval = null;
        let simSpeed = 500;
        let chatMessages = [];
        let humanDecisions = JSON.parse(localStorage.getItem('sentinel_decisions') || '[]');

        // District nodes
        const DISTRICTS = [
            {{ id: 'metro', name: 'Metro Commercial Hub', x: 180, y: 110, color: '#38bdf8' }},
            {{ id: 'wallet', name: 'Mobile Wallet Gateway', x: 620, y: 100, color: '#34d399' }},
            {{ id: 'transfer', name: 'Inter-Bank Transfer Node', x: 400, y: 210, color: '#a78bfa' }},
            {{ id: 'cashout', name: 'High-Value Cashout Zone', x: 180, y: 320, color: '#f59e0b' }},
            {{ id: 'mule', name: 'Mule Settlement Corridor', x: 620, y: 320, color: '#ef4444' }}
        ];

        let particles = [];

        function showTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }}

        function switchPolicy(policy) {{
            currentPolicy = policy;
            document.getElementById('statusRO').innerText = "Policy: " + policy.toUpperCase();
            updateKPICards();
            renderAlertQueue();
            renderPolicyView();
        }}

        function toggleEvalMode() {{
            evalMode = !evalMode;
            document.getElementById('evalToggleText').innerText = evalMode ? "👁️ Reveal Ground Truth: ON" : "👁️ Reveal Ground Truth: OFF";
            document.querySelectorAll('.eval-col').forEach(el => el.style.display = evalMode ? "table-cell" : "none");
            updateKPICards();
            renderAlertQueue();
        }}

        function updateKPICards() {{
            const decCol = "decision_" + currentPolicy;
            const activeAlerts = ALERTS.filter(r => r[decCol] === "hold" || r[decCol] === "escalate_to_human");
            
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

        function togglePlayPause() {{
            isPlaying = !isPlaying;
            document.getElementById('playBtn').innerText = isPlaying ? "⏸️ Pause" : "▶️ Play";
            if (isPlaying) startSimLoop();
            else clearInterval(simInterval);
        }}

        function changeSpeed(val) {{
            simSpeed = parseInt(val);
            if (isPlaying) {{
                clearInterval(simInterval);
                startSimLoop();
            }}
        }}

        function scrubStep(step) {{
            currentSimStep = parseInt(step);
            processStep(currentSimStep);
        }}

        function startSimLoop() {{
            clearInterval(simInterval);
            simInterval = setInterval(() => {{
                if (currentSimStep >= 743) currentSimStep = 334;
                else currentSimStep++;
                document.getElementById('simStepSlider').value = currentSimStep;
                processStep(currentSimStep);
            }}, simSpeed);
        }}

        function processStep(step) {{
            const hour = step % 24;
            document.getElementById('stepTicker').innerText = `Simulation Step: ${{step}} (Hour ${{hour}})`;

            // Check alerts at this step
            const stepAlerts = ALERTS.filter(r => r.step === step);
            if (stepAlerts.length > 0) {{
                stepAlerts.forEach(a => {{
                    const decCol = "decision_" + currentPolicy;
                    const dec = a[decCol];
                    
                    // Spawn particle on district map
                    const fromNode = a.type === "TRANSFER" ? DISTRICTS[0] : DISTRICTS[3];
                    const toNode = a.type === "TRANSFER" ? DISTRICTS[2] : DISTRICTS[4];
                    particles.push({{
                        x: fromNode.x,
                        y: fromNode.y,
                        tx: toNode.x,
                        ty: toNode.y,
                        color: dec === "escalate_to_human" ? "#ef4444" : "#f59e0b",
                        progress: 0,
                        speed: 0.04
                    }});

                    // Add agent chat message
                    addAgentMessage('scout', `[Scout] Flagged ${{a.type}} | ${{a.amount.toLocaleString()}} currency units | Score: ${{a.model_score.toFixed(3)}}`);
                    if (a.model_score >= 0.5) {{
                        addAgentMessage('inv', `[Investigator] Querying prior step history for ${{a.nameOrig}}...`);
                        addAgentMessage('ro', `[RiskOfficer] Policy ${{currentPolicy.toUpperCase()}} -> ${{dec.toUpperCase()}}`);
                    }}
                }});
            }}
        }}

        function addAgentMessage(type, text) {{
            const chatFeed = document.getElementById('chatFeed');
            const el = document.createElement('div');
            el.className = `chat-msg ${{type}}`;
            el.innerHTML = `<div class="sender">${{text}}</div>`;
            chatFeed.prepend(el);
            if (chatFeed.children.length > 60) {{
                chatFeed.removeChild(chatFeed.lastChild);
            }}
            document.getElementById('feedCount').innerText = chatFeed.children.length + " msgs";
        }}

        // Canvas animation
        function initDistrictCanvas() {{
            const canvas = document.getElementById('districtCanvas');
            const ctx = canvas.getContext('2d');

            function draw() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Draw connecting corridors
                ctx.strokeStyle = '#1e2e4a';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(DISTRICTS[0].x, DISTRICTS[0].y); ctx.lineTo(DISTRICTS[2].x, DISTRICTS[2].y);
                ctx.moveTo(DISTRICTS[1].x, DISTRICTS[1].y); ctx.lineTo(DISTRICTS[2].x, DISTRICTS[2].y);
                ctx.moveTo(DISTRICTS[2].x, DISTRICTS[2].y); ctx.lineTo(DISTRICTS[3].x, DISTRICTS[3].y);
                ctx.moveTo(DISTRICTS[2].x, DISTRICTS[2].y); ctx.lineTo(DISTRICTS[4].x, DISTRICTS[4].y);
                ctx.moveTo(DISTRICTS[3].x, DISTRICTS[3].y); ctx.lineTo(DISTRICTS[4].x, DISTRICTS[4].y);
                ctx.stroke();

                // Draw moving particles
                for (let i = particles.length - 1; i >= 0; i--) {{
                    const p = particles[i];
                    p.progress += p.speed;
                    const cx = p.x + (p.tx - p.x) * p.progress;
                    const cy = p.y + (p.ty - p.y) * p.progress;

                    ctx.fillStyle = p.color;
                    ctx.beginPath();
                    ctx.arc(cx, cy, 5, 0, Math.PI * 2);
                    ctx.fill();

                    if (p.progress >= 1) particles.splice(i, 1);
                }}

                // Draw district nodes
                DISTRICTS.forEach(d => {{
                    ctx.fillStyle = '#131d31';
                    ctx.strokeStyle = d.color;
                    ctx.lineWidth = 3;
                    ctx.beginPath();
                    ctx.arc(d.x, d.y, 20, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.stroke();

                    ctx.fillStyle = '#f8fafc';
                    ctx.font = 'bold 11px sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText(d.name, d.x, d.y + 35);
                }});

                requestAnimationFrame(draw);
            }}

            draw();
        }}

        function renderAlertQueue() {{
            const search = document.getElementById('queueSearch').value.toUpperCase();
            const typeF = document.getElementById('typeFilter').value;
            const decF = document.getElementById('decisionFilter').value;
            const decCol = "decision_" + currentPolicy;

            let list = ALERTS.filter(r => {{
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
            const keys = Object.keys(CASES);
            sel.innerHTML = keys.map(k => `<option value="${{k}}">${{k}} (${{CASES[k].transaction.type}}, ${{CASES[k].transaction.amount.toLocaleString()}} currency units)</option>`).join('');
            if (keys.length > 0) loadCaseDetails(keys[0]);
        }}

        function loadCaseDetails(caseId) {{
            const c = CASES[caseId];
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
                                <li>• <strong>Sender Prior History:</strong> ${{c.sender_history.prior_tx_count > 0 ? (c.sender_history.prior_tx_count + ' prior txs') : 'no prior history available'}}</li>
                                <li>• <strong>Network Correlated Pair:</strong> ${{c.network_evidence && c.network_evidence.has_linked_pair ? '⚠️ Same-step identical amount counterpart detected!' : 'None detected'}}</li>
                            </ul>
                        </div>
                    </div>

                    <div style="margin-top:20px;">
                        <h4>📝 AI Investigation Report</h4>
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

        function selectAndShowCase(caseId) {{
            showTab('tab3');
            document.querySelectorAll('.tab-btn')[2].classList.add('active');
            document.getElementById('caseSelector').value = caseId;
            loadCaseDetails(caseId);
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
            localStorage.setItem('sentinel_decisions', JSON.stringify(humanDecisions));
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

        function renderPolicyView() {{
            const tbody = document.getElementById('policyTableBody');
            tbody.innerHTML = POLICIES.map(p => `
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

        // Initialization
        window.addEventListener('DOMContentLoaded', () => {{
            populateCaseSelector();
            updateKPICards();
            renderAlertQueue();
            renderPolicyView();
            renderDecisionsTable();
            initDistrictCanvas();
            startSimLoop();

            // Policy Cost Chart
            const polCtx = document.getElementById('policyChart').getContext('2d');
            new Chart(polCtx, {{
                type: 'bar',
                data: {{
                    labels: POLICIES.map(p => p.policy),
                    datasets: [
                        {{ label: 'Review Cost (currency units)', data: POLICIES.map(p => p.review_cost), backgroundColor: '#f59e0b' }},
                        {{ label: 'Missed Fraud Loss (currency units)', data: POLICIES.map(p => p.fraud_value_lost), backgroundColor: '#ef4444' }},
                        {{ label: 'Total Net Cost (currency units)', data: POLICIES.map(p => p.total_cost), backgroundColor: '#3b82f6' }}
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

            // Market Impact Chart (Paytm vs NIFTY 50)
            const mktCtx = document.getElementById('marketChart').getContext('2d');
            new Chart(mktCtx, {{
                type: 'line',
                data: {{
                    labels: ['Jan 15', 'Jan 22', 'Jan 31 (RBI Action)', 'Feb 7', 'Feb 15', 'Feb 28', 'Mar 15'],
                    datasets: [
                        {{
                            label: 'Paytm (One97 Communications) Normalized %',
                            data: [100, 102, 78, 54, 46, 44, 45],
                            borderColor: '#ef4444',
                            backgroundColor: 'rgba(239, 68, 68, 0.1)',
                            fill: true,
                            tension: 0.3
                        }},
                        {{
                            label: 'NIFTY 50 Benchmark Normalized %',
                            data: [100, 99.5, 100.8, 101.5, 102.2, 103.1, 104.0],
                            borderColor: '#3b82f6',
                            borderDash: [5, 5],
                            tension: 0.2
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
                        y: {{ title: {{ display: true, text: 'Normalized Performance (Base=100)', color: '#94a3b8' }}, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }}
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

    print("Successfully built Sentinel Patrol static application for GitHub Pages.")

if __name__ == "__main__":
    build_site()
