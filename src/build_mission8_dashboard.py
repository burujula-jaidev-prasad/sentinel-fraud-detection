"""Mission 8 Story Dashboard Builder: Left-hand story navigation, 12 dynamic cards, and live patrol."""

import os
import json
import pandas as pd

def build_mission8_site():
    # Load all data files from docs/data/
    with open("docs/data/stream.json", "r", encoding="utf-8") as f:
        stream_data = json.load(f)

    with open("docs/data/data_overview.json", "r", encoding="utf-8") as f:
        data_overview = json.load(f)

    with open("docs/data/checks.json", "r", encoding="utf-8") as f:
        checks_data = json.load(f)

    df_cost_curve = pd.read_csv("docs/data/cost_curve.csv")
    df_cost_sens = pd.read_csv("docs/data/cost_sensitivity.csv")
    df_detector = pd.read_csv("docs/data/detector_comparison.csv")
    df_hourly = pd.read_csv("docs/data/hourly_stats.csv")
    df_amount_hist = pd.read_csv("docs/data/amount_hist.csv")
    df_score_hist = pd.read_csv("docs/data/score_hist.csv")
    df_threshold_curve = pd.read_csv("docs/data/threshold_curve.csv")
    df_market = pd.read_csv("docs/data/market/paytm_nifty.csv")
    df_feat_imp = pd.read_csv("docs/data/feature_importance.csv")

    bundle = {
        "stream": stream_data,
        "overview": data_overview,
        "checks": checks_data,
        "cost_curve": df_cost_curve.to_dict(orient="records"),
        "cost_sensitivity": df_cost_sens.to_dict(orient="records"),
        "detector_comparison": df_detector.to_dict(orient="records"),
        "hourly_stats": df_hourly.to_dict(orient="records"),
        "amount_hist": df_amount_hist.to_dict(orient="records"),
        "score_hist": df_score_hist.to_dict(orient="records"),
        "threshold_curve": df_threshold_curve.to_dict(orient="records"),
        "market": df_market.to_dict(orient="records"),
        "feature_importance": df_feat_imp.to_dict(orient="records")
    }

    # HTML template with standard replace
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentinel | Financial Fraud Intelligence Story Dashboard</title>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-color: #080d1a;
            --sidebar-bg: #0d1527;
            --card-bg: #121d33;
            --card-header: #192744;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #1e2e4a;
            --primary-cyan: #38bdf8;
            --primary-blue: #3b82f6;
            --safe-green: #10b981;
            --alert-amber: #f59e0b;
            --fraud-red: #ef4444;
            --honest-grey: #64748b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.5;
            display: flex;
            min-height: 100vh;
        }

        /* Left-Hand Story Navigation */
        .sidebar {
            width: 280px;
            background: var(--sidebar-bg);
            border-right: 1px solid var(--border-color);
            padding: 20px 16px;
            position: fixed;
            top: 0;
            bottom: 0;
            left: 0;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            z-index: 100;
        }

        .brand-box {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-color);
        }

        .brand-logo {
            height: 42px;
            width: auto;
        }

        .nav-section-title {
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--text-muted);
            letter-spacing: 1px;
            margin-bottom: 8px;
            padding-left: 8px;
        }

        .nav-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 4px;
            margin-bottom: 20px;
        }

        .nav-item-btn {
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-muted);
            padding: 10px 12px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            text-align: left;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 10px;
            width: 100%;
        }

        .nav-item-btn:hover {
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.04);
        }

        .nav-item-btn.active {
            color: #ffffff;
            background: #192744;
            border-color: var(--primary-cyan);
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.15);
        }

        .sidebar-footer {
            margin-top: auto;
            font-size: 11px;
            color: var(--text-muted);
            padding-top: 14px;
            border-top: 1px solid var(--border-color);
            line-height: 1.4;
        }

        /* Main Story Content Area */
        .main-wrapper {
            margin-left: 280px;
            flex: 1;
            padding: 24px 32px 60px 32px;
            max-width: 1380px;
        }

        /* Sticky Global Controls Header */
        .global-header {
            position: sticky;
            top: 0;
            background: rgba(13, 21, 39, 0.94);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 14px 20px;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
            z-index: 90;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
        }

        .control-group {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 13px;
        }

        .control-label {
            color: var(--text-muted);
            font-weight: 600;
        }

        input[type="range"] {
            accent-color: var(--primary-cyan);
            cursor: pointer;
        }

        select {
            background: #080d1a;
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 13px;
            outline: none;
            cursor: pointer;
        }

        .btn-toggle-key {
            padding: 7px 14px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
            border: 1px solid var(--border-color);
            background: #080d1a;
            color: var(--text-muted);
        }

        .btn-toggle-key.active {
            background: rgba(239, 68, 68, 0.15);
            border-color: var(--fraud-red);
            color: #f87171;
            box-shadow: 0 0 12px rgba(239, 68, 68, 0.3);
        }

        /* Step Section Headers */
        .step-section {
            display: none;
        }

        .step-section.active {
            display: block;
        }

        .step-header {
            margin-bottom: 20px;
        }

        .step-badge {
            display: inline-block;
            background: rgba(56, 189, 248, 0.15);
            color: var(--primary-cyan);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }

        .step-title {
            font-size: 22px;
            font-weight: 700;
            color: var(--text-main);
        }

        .step-sub {
            color: var(--text-muted);
            font-size: 13px;
            margin-top: 2px;
        }

        /* Story Cards Grid */
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }

        .cards-grid-full {
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }

        /* Card Container (Contract Enforcement) */
        .story-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 22px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .card-question {
            font-size: 16px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 6px;
        }

        .card-headline {
            font-size: 14px;
            color: var(--primary-cyan);
            font-weight: 600;
            margin-bottom: 16px;
            line-height: 1.4;
        }

        .card-visual-box {
            position: relative;
            height: 280px;
            width: 100%;
            margin-bottom: 14px;
            background: rgba(8, 13, 26, 0.5);
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.03);
            padding: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .card-explanation {
            font-size: 12.5px;
            color: var(--text-muted);
            line-height: 1.5;
            padding-top: 10px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            margin-bottom: 8px;
        }
        .card-explanation strong {
            color: var(--text-main);
        }

        .card-source-footer {
            font-size: 11px;
            color: #64748b;
            font-family: monospace;
        }

        /* 2x2 Confusion Box */
        .matrix-2x2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            width: 100%;
            height: 100%;
        }

        .matrix-cell {
            background: #080d1a;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .matrix-cell.tp { border-left: 4px solid var(--safe-green); }
        .matrix-cell.fp { border-left: 4px solid var(--alert-amber); }
        .matrix-cell.fn { border-left: 4px solid var(--fraud-red); }
        .matrix-cell.tn { border-left: 4px solid var(--honest-grey); }

        .matrix-cell-title {
            font-size: 12px;
            font-weight: 600;
            color: var(--text-main);
        }
        .matrix-cell-tech {
            font-size: 10.5px;
            color: var(--text-muted);
            margin-bottom: 4px;
        }
        .matrix-cell-val {
            font-size: 20px;
            font-weight: 700;
            color: #ffffff;
        }

        /* Dot Grid */
        .dot-grid-container {
            display: grid;
            grid-template-columns: repeat(40, 1fr);
            gap: 3px;
            width: 100%;
            max-height: 240px;
            overflow: hidden;
            padding: 10px;
        }
        .grid-dot {
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: var(--honest-grey);
            opacity: 0.5;
        }
        .grid-dot.fraud-dot {
            background: var(--fraud-red);
            opacity: 1;
            box-shadow: 0 0 6px var(--fraud-red);
            transform: scale(1.3);
        }

        /* Live Strip */
        .patrol-controls {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 14px;
            padding: 10px 14px;
            background: #080d1a;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }

        .btn {
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            border: 1px solid transparent;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .btn-primary { background: var(--primary-blue); color: white; }
        .btn-secondary { background: #1a2640; color: var(--text-main); border-color: var(--border-color); }

        pre {
            background: #080d1a;
            border: 1px solid var(--border-color);
            padding: 12px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 11.5px;
            color: #93c5fd;
            white-space: pre-wrap;
            word-break: break-word;
            max-height: 280px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <!-- Left-Hand Story Navigation -->
    <aside class="sidebar">
        <div class="brand-box">
            <img src="assets/sentinel-logo.svg" alt="Sentinel Logo" class="brand-logo">
        </div>

        <div class="nav-section-title">Investigation Story</div>
        <ul class="nav-list">
            <li><button class="nav-item-btn active" onclick="goToStep(1)">🔴 1. The Problem</button></li>
            <li><button class="nav-item-btn" onclick="goToStep(2)">📊 2. The Data</button></li>
            <li><button class="nav-item-btn" onclick="goToStep(3)">🔬 3. The Detector</button></li>
            <li><button class="nav-item-btn" onclick="goToStep(4)">🎯 4. The Result</button></li>
            <li><button class="nav-item-btn" onclick="goToStep(5)">⚖️ 5. The Decision</button></li>
            <li><button class="nav-item-btn" onclick="goToStep(6)">📉 6. The Market Link</button></li>
            <li><button class="nav-item-btn" onclick="goToStep(7)">⏱️ 7. Live Patrol & Cases</button></li>
        </ul>

        <div class="sidebar-footer">
            <strong>Sentinel Patrol</strong><br>
            Simulated live stream: replay of the PaySim test period (steps 334–743). Never claim real-time bank data.
        </div>
    </aside>

    <!-- Main Content Area -->
    <main class="main-wrapper">
        <!-- Sticky Global Control Bar -->
        <header class="global-header">
            <div class="control-group">
                <span class="control-label">Strictness Threshold:</span>
                <input type="range" id="strictnessRange" min="0" max="22" value="13" oninput="onStrictnessChange(this.value)">
                <strong id="strictnessLabel" style="color:var(--primary-cyan); min-width:60px;">0.50</strong>
            </div>

            <div class="control-group">
                <span class="control-label">Review Cost:</span>
                <select id="checkingCostSelect" onchange="onCheckingCostChange(this.value)">
                    <option value="100">100 CU / check</option>
                    <option value="500" selected>500 CU / check (Base)</option>
                    <option value="2000">2,000 CU / check</option>
                    <option value="5000">5,000 CU / check</option>
                    <option value="25000">25,000 CU / check</option>
                    <option value="100000">100,000 CU / check</option>
                    <option value="500000">500,000 CU / check</option>
                </select>
            </div>

            <div class="control-group">
                <button class="btn-toggle-key" id="evalKeyToggle" onclick="toggleAnswerKey()">
                    <span id="evalKeyText">👁️ Reveal Ground Truth: OFF</span>
                </button>
            </div>
        </header>

        <!-- ========================================================================= -->
        <!-- STEP 1: THE PROBLEM -->
        <!-- ========================================================================= -->
        <section id="step1" class="step-section active">
            <div class="step-header">
                <div class="step-badge">Step 1 of 7</div>
                <h2 class="step-title">The Problem: Extreme Scarcity in Fraud Detection</h2>
                <p class="step-sub">Understanding the needle-in-a-haystack nature of payment fraud and high-risk transaction channels.</p>
            </div>

            <div class="cards-grid">
                <!-- Card 1 -->
                <div class="story-card">
                    <div class="card-question">How rare is financial fraud in digital payments?</div>
                    <div class="card-headline" id="c1Headline">Loading...</div>
                    <div class="card-visual-box">
                        <div class="dot-grid-container" id="c1DotGrid"></div>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Extreme class imbalance renders traditional accuracy metrics useless (a dummy model predicting 100% legitimate achieves 99.37% accuracy while catching 0 frauds). Precision and recall are the only meaningful evaluation benchmarks.
                    </div>
                    <div class="card-source-footer">Source: docs/data/data_overview.json</div>
                </div>

                <!-- Card 2 -->
                <div class="story-card">
                    <div class="card-question">Which payment types carry fraud risk?</div>
                    <div class="card-headline" id="c2Headline">Loading...</div>
                    <div class="card-visual-box">
                        <canvas id="c2Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Fraud is structurally confined to unauthorized outbound money transfers (<code>TRANSFER</code>) and subsequent account liquidations (<code>CASH_OUT</code>). Low-risk merchant purchases and deposits can bypass heavy ML screening pipelines.
                    </div>
                    <div class="card-source-footer">Source: docs/data/data_overview.json</div>
                </div>
            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- STEP 2: THE DATA -->
        <!-- ========================================================================= -->
        <section id="step2" class="step-section">
            <div class="step-header">
                <div class="step-badge">Step 2 of 7</div>
                <h2 class="step-title">The Data: Temporal Splitting & Feature Distributions</h2>
                <p class="step-sub">Preventing lookahead data leakage and analyzing monetary and diurnal fraud patterns.</p>
            </div>

            <div class="cards-grid">
                <!-- Card 3 -->
                <div class="story-card">
                    <div class="card-question">How is the dataset split across time to prevent leakage?</div>
                    <div class="card-headline" id="c3Headline">Loading...</div>
                    <div class="card-visual-box">
                        <canvas id="c3Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Random train/test splits cheat by leaking future fraud patterns into past training. Sentinel strictly trains on steps 1–333 and evaluates on future unseen steps 334–742, replicating real-time production conditions.
                    </div>
                    <div class="card-source-footer">Source: docs/data/data_overview.json</div>
                </div>

                <!-- Card 4 -->
                <div class="story-card">
                    <div class="card-question">How do fraud amounts compare to honest payments?</div>
                    <div class="card-headline" id="c4Headline">Loading...</div>
                    <div class="card-visual-box">
                        <canvas id="c4Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Fraudsters aim for maximum principal extraction per compromised credential, skewing transactions toward high amounts (>200,000 currency units). However, monetary scale alone is insufficient due to legitimate high-value commercial transfers.
                    </div>
                    <div class="card-source-footer">Source: docs/data/amount_hist.csv</div>
                </div>
            </div>

            <!-- Card 5 -->
            <div class="cards-grid-full">
                <div class="story-card">
                    <div class="card-question">When does fraud happen during the diurnal 24-hour cycle?</div>
                    <div class="card-headline" id="c5Headline">Loading...</div>
                    <div class="card-visual-box" style="height:260px;">
                        <canvas id="c5Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Honest transactions follow human business hours with sharp drop-offs late at night. Automated fraud scripts and money laundering rings operate around the clock, causing the relative risk of overnight transfers to spike.
                    </div>
                    <div class="card-source-footer">Source: docs/data/hourly_stats.csv</div>
                </div>
            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- STEP 3: THE DETECTOR -->
        <!-- ========================================================================= -->
        <section id="step3" class="step-section">
            <div class="step-header">
                <div class="step-badge">Step 3 of 7</div>
                <h2 class="step-title">The Detector: Model Architecture & Discrimination Power</h2>
                <p class="step-sub">Benchmarking the balanced Random Forest against static rules, Logistic Regression, and Isolation Forest.</p>
            </div>

            <div class="cards-grid">
                <!-- Card 6 -->
                <div class="story-card">
                    <div class="card-question">Which detector catches fraud best without cheating?</div>
                    <div class="card-headline" id="c6Headline">Loading...</div>
                    <div class="card-visual-box">
                        <canvas id="c6Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Random Forest achieves a PR-AUC of 0.3371 (~53x lift over random guessing baseline of 0.63%), outperforming linear models and static amount thresholds while strictly avoiding leaked balance columns.
                    </div>
                    <div class="card-source-footer">Source: docs/data/detector_comparison.csv</div>
                </div>

                <!-- Card 7 -->
                <div class="story-card">
                    <div class="card-question">How confident is the model across payments?</div>
                    <div class="card-headline" id="c7Headline">Loading...</div>
                    <div class="card-visual-box">
                        <canvas id="c7Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> 97.6% of payments score below 0.10 probability, confirming the model concentrates risk effectively into a small actionable queue without creating friction for normal customers.
                    </div>
                    <div class="card-source-footer">Source: docs/data/score_hist.csv</div>
                </div>
            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- STEP 4: THE RESULT -->
        <!-- ========================================================================= -->
        <section id="step4" class="step-section">
            <div class="step-header">
                <div class="step-badge">Step 4 of 7</div>
                <h2 class="step-title">The Result: Confusion Matrix & Financial Cost Curve</h2>
                <p class="step-sub">Interactive trade-off between analyst verification workload and unrecovered fraud losses.</p>
            </div>

            <div class="cards-grid">
                <!-- Card 8 -->
                <div class="story-card">
                    <div class="card-question">What is the operational performance at the selected strictness?</div>
                    <div class="card-headline" id="c8Headline">Loading...</div>
                    <div class="card-visual-box">
                        <div class="matrix-2x2" id="c8Matrix"></div>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Lower strictness thresholds capture more fraudulent transactions (higher recall) at the cost of generating more false alerts for compliance officers to inspect.
                    </div>
                    <div class="card-source-footer">Source: docs/data/threshold_curve.csv</div>
                </div>

                <!-- Card 9 -->
                <div class="story-card">
                    <div class="card-question">What is the total financial cost curve at this checking cost?</div>
                    <div class="card-headline" id="c9Headline">Loading...</div>
                    <div class="card-visual-box">
                        <canvas id="c9Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> <em>"The best strictness depends on the cost of one check"</em>. When review costs are low (e.g. 500 CU), strict screening (0.01) achieves the lowest net loss by saving massive fraud principal. When review costs are high (e.g. 100,000 CU), higher thresholds become optimal.
                    </div>
                    <div class="card-source-footer">Source: docs/data/cost_curve.csv & docs/data/cost_sensitivity.csv</div>
                </div>
            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- STEP 5: THE DECISION -->
        <!-- ========================================================================= -->
        <section id="step5" class="step-section">
            <div class="step-header">
                <div class="step-badge">Step 5 of 7</div>
                <h2 class="step-title">The Decision: Policy Economics & Protected Capital</h2>
                <p class="step-sub">Macroeconomic comparison between Strict (0.10), Balanced (0.50), and Lenient (0.90) risk policies.</p>
            </div>

            <div class="cards-grid-full">
                <!-- Card 10 -->
                <div class="story-card">
                    <div class="card-question">How much fraud money is stopped under each policy?</div>
                    <div class="card-headline" id="c10Headline">Loading...</div>
                    <div class="card-visual-box" style="height:300px;">
                        <canvas id="c10Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Missed fraud principal dominates manual review costs by over two orders of magnitude. The Strict Policy catches 752.38M currency units, minimizing net financial exposure across the payments network.
                    </div>
                    <div class="card-source-footer">Source: docs/data/stream.json (policy_comparison)</div>
                </div>
            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- STEP 6: THE MARKET LINK -->
        <!-- ========================================================================= -->
        <section id="step6" class="step-section">
            <div class="step-header">
                <div class="step-badge">Step 6 of 7</div>
                <h2 class="step-title">The Market Link: Compliance Failures & Equity Impact</h2>
                <p class="step-sub">Case study on the systemic valuation fallout following supervisory action on payment fraud controls.</p>
            </div>

            <div class="cards-grid-full">
                <!-- Card 11 -->
                <div class="story-card">
                    <div class="card-question">What is the market impact of fraud compliance failure?</div>
                    <div class="card-headline" id="c11Headline">Loading...</div>
                    <div class="card-visual-box" style="height:320px;">
                        <canvas id="c11Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Weak supervisory AML/KYC controls lead to direct equity destruction and regulatory license restrictions. Automated multi-agent monitoring with full audit logs guarantees compliance under RBI and DPDP directives.
                    </div>
                    <div class="card-source-footer">Source: docs/data/market/paytm_nifty.csv</div>
                </div>
            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- STEP 7: LIVE PATROL AND CASES -->
        <!-- ========================================================================= -->
        <section id="step7" class="step-section">
            <div class="step-header">
                <div class="step-badge">Step 7 of 7</div>
                <h2 class="step-title">Live Patrol: Test Replay Stream & Case Dossiers</h2>
                <p class="step-sub">Simulated hourly playback across test steps 334–742 and forensic multi-agent case investigation dossiers.</p>
            </div>

            <div class="story-card" style="margin-bottom:20px;">
                <div class="card-question">How does Sentinel monitor transactions live?</div>
                <div class="card-headline" id="c12Headline">Loading...</div>

                <div class="patrol-controls">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <button class="btn btn-primary" id="patrolPlayBtn" onclick="togglePatrolPlay()">⏸️ Pause</button>
                        <span id="patrolStepDisplay" style="font-weight:700; font-size:13px; color:var(--primary-cyan);">Step: 334 (Hour 22)</span>
                    </div>
                    <div style="display:flex; align-items:center; gap:12px; flex:1; max-width:460px;">
                        <span style="font-size:12px; color:var(--text-muted);">Scrubber:</span>
                        <input type="range" id="patrolScrubber" min="334" max="742" value="334" style="flex:1;" oninput="scrubPatrol(this.value)">
                    </div>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:12px; color:var(--text-muted);">Speed:</span>
                        <select id="patrolSpeedSelect" onchange="changePatrolSpeed(this.value)">
                            <option value="1000">1 hr/sec</option>
                            <option value="400" selected>2.5 hr/sec</option>
                            <option value="150">6 hr/sec</option>
                        </select>
                    </div>
                </div>

                <div class="card-visual-box" style="height:240px;">
                    <canvas id="c12Chart"></canvas>
                </div>

                <div class="card-explanation">
                    <strong>What this means:</strong> Sentinel continuously scans incoming transactions, maintaining a strict chronological profile and correlating same-step identical-amount money laundering pairs without delaying honest transactions.
                </div>
                <div class="card-source-footer">Source: docs/data/hourly_stats.csv, docs/data/stream.json</div>
            </div>

            <!-- Case Dossier Explorer -->
            <div class="story-card">
                <div class="card-question">Forensic Case File Dossier (Precomputed Multi-Agent Synthesis)</div>
                <div style="display:flex; gap:12px; margin-bottom:14px; align-items:center; flex-wrap:wrap;">
                    <label style="font-size:12px; color:var(--text-muted);">Select Alert Dossier:</label>
                    <select id="patrolCaseSelect" onchange="renderCaseDossier(this.value)" style="min-width:320px;"></select>
                </div>
                <div id="patrolCaseDossierBox"></div>
                <div class="card-source-footer" style="margin-top:14px;">Source: docs/data/stream.json (cases)</div>
            </div>
        </section>

    </main>

    <!-- Global Application State & Reactive Data Script -->
    <script>
        const DATA = __DATA_BUNDLE__;

        const THRESHOLD_GRID = [0.01, 0.02, 0.03, 0.04, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95];
        let currentStrictness = 0.50;
        let currentCheckingCost = 500;
        let evalMode = false;
        let patrolPlaying = true;
        let patrolCurrentStep = 334;
        let patrolInterval = null;
        let patrolSpeed = 400;

        // Chart instances
        let chartC2, chartC3, chartC4, chartC5, chartC6, chartC7, chartC9, chartC10, chartC11, chartC12;

        function goToStep(stepNum) {
            document.querySelectorAll('.step-section').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-item-btn').forEach(el => el.classList.remove('active'));
            document.getElementById('step' + stepNum).classList.add('active');
            document.querySelectorAll('.nav-item-btn')[stepNum - 1].classList.add('active');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function onStrictnessChange(idx) {
            currentStrictness = THRESHOLD_GRID[parseInt(idx)];
            document.getElementById('strictnessLabel').innerText = currentStrictness.toFixed(2);
            renderAllDynamicCards();
        }

        function onCheckingCostChange(val) {
            currentCheckingCost = parseInt(val);
            renderAllDynamicCards();
        }

        function toggleAnswerKey() {
            evalMode = !evalMode;
            document.getElementById('evalKeyText').innerText = evalMode ? "👁️ Reveal Ground Truth: ON" : "👁️ Reveal Ground Truth: OFF";
            document.getElementById('evalKeyToggle').classList.toggle('active', evalMode);
            renderAllDynamicCards();
        }

        function renderAllDynamicCards() {
            renderCard1();
            renderCard2();
            renderCard3();
            renderCard4();
            renderCard5();
            renderCard6();
            renderCard7();
            renderCard8();
            renderCard9();
            renderCard10();
            renderCard11();
            renderCard12();
        }

        // Card 1: How rare is fraud?
        function renderCard1() {
            const ov = DATA.overview;
            const total = ov.sample_dataset.total_transactions;
            const frauds = ov.sample_dataset.total_frauds;
            const pct = (ov.sample_dataset.overall_fraud_rate * 100).toFixed(3);
            const testFrauds = ov.time_split.test_frauds;
            const testTotal = ov.time_split.test_rows;
            const testPct = (ov.time_split.test_fraud_rate * 100).toFixed(3);

            if (evalMode) {
                document.getElementById('c1Headline').innerText = `Across the sample, only ${frauds.toLocaleString()} of ${total.toLocaleString()} payments (${pct}%) are fraud (${testFrauds} of ${testTotal.toLocaleString()} in test, ${testPct}%).`;
            } else {
                document.getElementById('c1Headline').innerText = `Fraud represents under 1% of digital payments across the network, making detection an extreme class-imbalance problem.`;
            }

            const grid = document.getElementById('c1DotGrid');
            grid.innerHTML = '';
            for (let i = 0; i < 800; i++) {
                const dot = document.createElement('div');
                dot.className = 'grid-dot' + (evalMode && i < 5 ? ' fraud-dot' : '');
                grid.appendChild(dot);
            }
        }

        // Card 2: Payment types
        function renderCard2() {
            const ov = DATA.overview.filtered_dataset;
            const trFrauds = ov.transfer_frauds;
            const coFrauds = ov.cashout_frauds;
            const trTotal = ov.transfer_count;
            const coTotal = ov.cashout_count;

            if (evalMode) {
                document.getElementById('c2Headline').innerText = `100% of frauds occur in TRANSFER (${trFrauds} of ${trTotal.toLocaleString()}) and CASH_OUT (${coFrauds} of ${coTotal.toLocaleString()}). Zero frauds occur in other types.`;
            } else {
                document.getElementById('c2Headline').innerText = `Fraud is concentrated exclusively in outbound TRANSFER and CASH_OUT payment corridors.`;
            }

            const ctx = document.getElementById('c2Chart').getContext('2d');
            if (chartC2) chartC2.destroy();
            chartC2 = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['TRANSFER', 'CASH_OUT', 'PAYMENT', 'CASH_IN', 'DEBIT'],
                    datasets: [
                        { label: 'Total Payments', data: [trTotal, coTotal, 321000, 210000, 7000], backgroundColor: '#64748b' },
                        { label: 'Frauds (Ground Truth)', data: evalMode ? [trFrauds, coFrauds, 0, 0, 0] : [0, 0, 0, 0, 0], backgroundColor: '#ef4444' }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                        y: { type: 'logarithmic', grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            });
        }

        // Card 3: Time split
        function renderCard3() {
            const sp = DATA.overview.time_split;
            document.getElementById('c3Headline').innerText = `Training on steps 1–${sp.split_step} (${sp.train_rows.toLocaleString()} payments) and evaluating on future steps ${sp.test_steps[0]}–${sp.test_steps[1]} (${sp.test_rows.toLocaleString()} payments).`;

            const ctx = document.getElementById('c3Chart').getContext('2d');
            if (chartC3) chartC3.destroy();
            chartC3 = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Train Set (Steps 1-333: 75%)', 'Test Set (Steps 334-742: 25%)'],
                    datasets: [{
                        data: [sp.train_rows, sp.test_rows],
                        backgroundColor: ['#3b82f6', '#38bdf8'],
                        borderColor: '#080d1a',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            });
        }

        // Card 4: Amount histogram
        function renderCard4() {
            const hist = DATA.amount_hist;
            const highFraud = hist.filter(h => h.bin_min >= 200000).reduce((sum, h) => sum + h.count_fraud, 0);
            
            if (evalMode) {
                document.getElementById('c4Headline').innerText = `${highFraud} of 652 test frauds (${((highFraud/652)*100).toFixed(1)}%) occur in amounts exceeding 200,000 currency units.`;
            } else {
                document.getElementById('c4Headline').innerText = `Fraudulent payments skew heavily towards high-value brackets (>200,000 currency units).`;
            }

            const ctx = document.getElementById('c4Chart').getContext('2d');
            if (chartC4) chartC4.destroy();
            chartC4 = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: hist.map(h => h.bin_label),
                    datasets: [
                        { label: 'Legitimate Payments', data: hist.map(h => h.count_legit), backgroundColor: '#64748b' },
                        { label: 'Fraud Payments', data: evalMode ? hist.map(h => h.count_fraud) : hist.map(() => 0), backgroundColor: '#ef4444' }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                        y: { type: 'logarithmic', grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            });
        }

        // Card 5: Diurnal 24-hour cycle
        function renderCard5() {
            const hrMap = {};
            for (let i = 0; i < 24; i++) hrMap[i] = { payments: 0, frauds: 0, alerts: 0 };
            DATA.hourly_stats.forEach(h => {
                hrMap[h.hour].payments += h.payments;
                hrMap[h.hour].frauds += h.frauds_actual;
                hrMap[h.hour].alerts += h.alerts_strict;
            });

            document.getElementById('c5Headline').innerText = `Payments follow human business hours (peaking 9:00–18:00), while automated fraud attacks continue across all 24 hours.`;

            const ctx = document.getElementById('c5Chart').getContext('2d');
            if (chartC5) chartC5.destroy();
            chartC5 = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Array.from({length: 24}, (_, i) => `${i}:00`),
                    datasets: [
                        { label: 'Total Payments', data: Object.values(hrMap).map(v => v.payments), backgroundColor: '#38bdf8' },
                        { label: 'Strict Alerts (Flagged)', data: Object.values(hrMap).map(v => v.alerts), backgroundColor: '#f59e0b' },
                        { label: 'Actual Frauds', data: evalMode ? Object.values(hrMap).map(v => v.frauds) : Object.values(hrMap).map(() => 0), backgroundColor: '#ef4444' }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            });
        }

        // Card 6: Detector comparison
        function renderCard6() {
            const rf = DATA.detector_comparison.find(d => d.detector.includes("Random Forest"));
            const lr = DATA.detector_comparison.find(d => d.detector.includes("Logistic"));
            const rule = DATA.detector_comparison.find(d => d.detector.includes("Rule"));

            document.getElementById('c6Headline').innerText = `Random Forest achieves PR-AUC of ${rf.pr_auc.toFixed(4)} (~53x lift over 0.0063 baseline), outperforming Logistic Regression (${lr.pr_auc.toFixed(4)}) and Static Rule (${rule.pr_auc.toFixed(4)}).`;

            const ctx = document.getElementById('c6Chart').getContext('2d');
            if (chartC6) chartC6.destroy();
            chartC6 = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: DATA.detector_comparison.map(d => d.detector),
                    datasets: [{
                        label: 'PR-AUC (Precision-Recall Area)',
                        data: DATA.detector_comparison.map(d => d.pr_auc),
                        backgroundColor: ['#64748b', '#3b82f6', '#10b981', '#a78bfa']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8', font: { size: 10 } } },
                        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' }, max: 0.4 }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            });
        }

        // Card 7: Score histogram
        function renderCard7() {
            const sh = DATA.score_hist;
            const lowPct = ((sh[0].total / DATA.overview.time_split.test_rows) * 100).toFixed(1);
            document.getElementById('c7Headline').innerText = `${lowPct}% of test payments score in the lowest 0.0–0.1 bucket, confining risk alerts to a sharp actionable tail.`;

            const ctx = document.getElementById('c7Chart').getContext('2d');
            if (chartC7) chartC7.destroy();
            chartC7 = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: sh.map(s => s.bin_label),
                    datasets: [
                        { label: 'Legitimate Payments', data: sh.map(s => s.count_legit), backgroundColor: '#64748b' },
                        { label: 'Fraud Payments', data: evalMode ? sh.map(s => s.count_fraud) : sh.map(() => 0), backgroundColor: '#ef4444' }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                        y: { type: 'logarithmic', grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            });
        }

        // Card 8: 2x2 Matrix at Strictness
        function renderCard8() {
            const row = DATA.threshold_curve.find(t => Math.abs(t.threshold - currentStrictness) < 0.001) || DATA.threshold_curve[0];
            const alerts = row.tp + row.fp;
            const prec = (row.precision * 100).toFixed(2);
            const rec = (row.recall * 100).toFixed(2);

            if (evalMode) {
                document.getElementById('c8Headline').innerText = `At strictness ${row.threshold.toFixed(2)}: ${alerts.toLocaleString()} alerts generated; ${row.tp} frauds caught (${rec}% recall) with ${prec}% precision.`;
            } else {
                document.getElementById('c8Headline').innerText = `At strictness ${row.threshold.toFixed(2)}: ${alerts.toLocaleString()} total candidate alerts generated for operational review.`;
            }

            const matrix = document.getElementById('c8Matrix');
            matrix.innerHTML = `
                <div class="matrix-cell tp">
                    <div class="matrix-cell-title">Caught Frauds</div>
                    <div class="matrix-cell-tech">True Positives (TP)</div>
                    <div class="matrix-cell-val" style="color:var(--safe-green);">${evalMode ? row.tp.toLocaleString() : 'Masked'}</div>
                </div>
                <div class="matrix-cell fp">
                    <div class="matrix-cell-title">False Alarms</div>
                    <div class="matrix-cell-tech">False Positives (FP)</div>
                    <div class="matrix-cell-val" style="color:var(--alert-amber);">${evalMode ? row.fp.toLocaleString() : alerts.toLocaleString()}</div>
                </div>
                <div class="matrix-cell fn">
                    <div class="matrix-cell-title">Missed Frauds</div>
                    <div class="matrix-cell-tech">False Negatives (FN)</div>
                    <div class="matrix-cell-val" style="color:var(--fraud-red);">${evalMode ? row.fn.toLocaleString() : 'Masked'}</div>
                </div>
                <div class="matrix-cell tn">
                    <div class="matrix-cell-title">Safe Passes</div>
                    <div class="matrix-cell-tech">True Negatives (TN)</div>
                    <div class="matrix-cell-val" style="color:var(--honest-grey);">${evalMode ? row.tn.toLocaleString() : (DATA.overview.time_split.test_rows - alerts).toLocaleString()}</div>
                </div>
            `;
        }

        // Card 9: Cost curve & sensitivity
        function renderCard9() {
            const col = `cost_${currentCheckingCost}`;
            const sensData = DATA.cost_sensitivity.filter(s => s.threshold !== 'lowest_cost_threshold');
            const optRow = DATA.cost_sensitivity.find(s => s.threshold === 'lowest_cost_threshold');
            const optTh = optRow ? parseFloat(optRow[col]) : 0.01;

            document.getElementById('c9Headline').innerText = `At ${currentCheckingCost.toLocaleString()} currency units/check, the minimum total loss is achieved at strictness threshold ${optTh.toFixed(2)}.`;

            const ctx = document.getElementById('c9Chart').getContext('2d');
            if (chartC9) chartC9.destroy();

            const totals = sensData.map(s => parseFloat(s[col]));
            const minVal = Math.min(...totals);

            chartC9 = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: sensData.map(s => s.threshold),
                    datasets: [
                        {
                            label: `Total Cost @ ${currentCheckingCost} CU/check`,
                            data: totals,
                            borderColor: '#38bdf8',
                            backgroundColor: 'rgba(56, 189, 248, 0.1)',
                            fill: true,
                            tension: 0.2,
                            pointRadius: sensData.map(s => parseFloat(s.threshold) === optTh ? 7 : 2),
                            pointBackgroundColor: sensData.map(s => parseFloat(s.threshold) === optTh ? '#ef4444' : '#38bdf8')
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { title: { display: true, text: 'Strictness Threshold', color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                        y: { title: { display: true, text: 'Total Loss (currency units)', color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            });
        }

        // Card 10: Policy comparison
        function renderCard10() {
            const pol = DATA.stream.policy_comparison;
            const strictSaved = (pol.find(p => p.policy.toLowerCase() === 'strict').fraud_value_saved / 1000000).toFixed(2);
            const balSaved = (pol.find(p => p.policy.toLowerCase() === 'balanced').fraud_value_saved / 1000000).toFixed(2);
            const lenSaved = (pol.find(p => p.policy.toLowerCase() === 'lenient').fraud_value_saved / 1000000).toFixed(2);

            document.getElementById('c10Headline').innerText = `Strict Policy stops ${strictSaved}M currency units; Balanced stops ${balSaved}M CU; Lenient stops ${lenSaved}M CU.`;

            const ctx = document.getElementById('c10Chart').getContext('2d');
            if (chartC10) chartC10.destroy();
            chartC10 = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: pol.map(p => p.policy),
                    datasets: [
                        { label: 'Protected Fraud Principal (currency units)', data: pol.map(p => p.fraud_value_saved), backgroundColor: '#10b981' },
                        { label: 'Lost Fraud Principal (currency units)', data: pol.map(p => p.fraud_value_lost), backgroundColor: '#ef4444' },
                        { label: 'Analyst Review Cost (currency units)', data: pol.map(p => p.review_cost), backgroundColor: '#f59e0b' }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            });
        }

        // Card 11: Market Link
        function renderCard11() {
            const m = DATA.market;
            const preVol = m[0].pre_volatility;
            const postVol = m[0].post_volatility;
            const betaPre = m[0].beta_pre;
            const betaPost = m[0].beta_post;

            document.getElementById('c11Headline').innerText = `Post-RBI supervisory action, Paytm equity dropped ~55%; annualized volatility surged from ${preVol}% to ${postVol}% while market beta rose from ${betaPre} to ${betaPost}.`;

            const ctx = document.getElementById('c11Chart').getContext('2d');
            if (chartC11) chartC11.destroy();
            chartC11 = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: m.map(r => r.date),
                    datasets: [
                        { label: 'Paytm Normalized (Base=100)', data: m.map(r => r.paytm_normalized), borderColor: '#ef4444', backgroundColor: 'rgba(239, 68, 68, 0.1)', fill: true, tension: 0.2 },
                        { label: 'NIFTY 50 Benchmark (Base=100)', data: m.map(r => r.nifty_normalized), borderColor: '#38bdf8', borderDash: [4, 4], tension: 0.1 }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8', maxTicksLimit: 12 } },
                        y: { title: { display: true, text: 'Normalized Index (Jan 1 = 100)', color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            });
        }

        // Card 12: Live Patrol
        function renderCard12() {
            const edges46 = DATA.stream.network_edges.filter(e => e.step > 333);
            document.getElementById('c12Headline').innerText = `Replaying steps 334–742 with ${edges46.length} test-period correlated money laundering pairs tracked across nodes.`;

            // Populate Case Selector
            const caseSel = document.getElementById('patrolCaseSelect');
            if (caseSel && caseSel.children.length === 0) {
                const keys = Object.keys(DATA.stream.cases);
                caseSel.innerHTML = keys.map(k => `<option value="${k}">${k} (${DATA.stream.cases[k].transaction.type}, ${DATA.stream.cases[k].transaction.amount.toLocaleString()} currency units)</option>`).join('');
                if (keys.length > 0) renderCaseDossier(keys[0]);
            }

            renderPatrolStep(patrolCurrentStep);
        }

        function renderCaseDossier(caseId) {
            const c = DATA.stream.cases[caseId];
            if (!c) return;
            const tx = c.transaction;
            const ro = c.risk_officer;
            const rpt = c.report_text || "No AI report available.";

            document.getElementById('patrolCaseDossierBox').innerHTML = `
                <div style="background:#080d1a; border:1px solid var(--border-color); border-radius:8px; padding:14px; margin-top:8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <strong>📁 Dossier: <code>${caseId}</code></strong>
                        <span style="background:#f59e0b; color:black; padding:2px 8px; border-radius:4px; font-weight:700; font-size:11px;">${ro.decision_balanced.toUpperCase()}</span>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; font-size:12px; color:var(--text-muted); margin-bottom:10px;">
                        <div>• Step: ${tx.step} (Hour ${tx.hour})<br>• Type: ${tx.type}<br>• Amount: <strong style="color:white;">${tx.amount.toLocaleString()}</strong> currency units</div>
                        <div>• Model Score: ${c.scores.model_score.toFixed(4)}<br>• Anomaly Score: ${c.scores.anomaly_score.toFixed(4)}<br>• Sender Prior History: ${c.sender_history.prior_tx_count > 0 ? c.sender_history.prior_tx_count + ' txs' : 'no prior history available'}</div>
                    </div>
                    <pre>${rpt}</pre>
                </div>
            `;
        }

        function togglePatrolPlay() {
            patrolPlaying = !patrolPlaying;
            document.getElementById('patrolPlayBtn').innerText = patrolPlaying ? "⏸️ Pause" : "▶️ Play";
            if (patrolPlaying) startPatrolLoop();
            else clearInterval(patrolInterval);
        }

        function scrubPatrol(step) {
            patrolCurrentStep = parseInt(step);
            renderPatrolStep(patrolCurrentStep);
        }

        function changePatrolSpeed(ms) {
            patrolSpeed = parseInt(ms);
            if (patrolPlaying) {
                clearInterval(patrolInterval);
                startPatrolLoop();
            }
        }

        function startPatrolLoop() {
            clearInterval(patrolInterval);
            patrolInterval = setInterval(() => {
                if (patrolCurrentStep >= 742) patrolCurrentStep = 334;
                else patrolCurrentStep++;
                document.getElementById('patrolScrubber').value = patrolCurrentStep;
                renderPatrolStep(patrolCurrentStep);
            }, patrolSpeed);
        }

        function renderPatrolStep(step) {
            const hour = step % 24;
            document.getElementById('patrolStepDisplay').innerText = `Step: ${step} (Hour ${hour})`;

            // Slice recent 30 steps for strip chart
            const minS = Math.max(334, step - 30);
            const stepSlice = DATA.hourly_stats.filter(h => h.step >= minS && h.step <= step);

            const ctx = document.getElementById('c12Chart').getContext('2d');
            if (chartC12) chartC12.destroy();
            chartC12 = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: stepSlice.map(s => `S${s.step}`),
                    datasets: [
                        { label: 'Payments Volume', data: stepSlice.map(s => s.payments), backgroundColor: '#64748b' },
                        { label: 'Strict Alerts', data: stepSlice.map(s => s.alerts_strict), backgroundColor: '#f59e0b' },
                        { label: 'Actual Frauds', data: evalMode ? stepSlice.map(s => s.frauds_actual) : stepSlice.map(() => 0), backgroundColor: '#ef4444' }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            });
        }

        window.addEventListener('DOMContentLoaded', () => {
            renderAllDynamicCards();
            startPatrolLoop();
        });
    </script>
</body>
</html>"""

    html_out = html_template.replace("__DATA_BUNDLE__", json.dumps(bundle))

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_out)

    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html_out)

    print("Successfully built Mission 8 Story Dashboard at index.html and docs/index.html")

if __name__ == "__main__":
    build_mission8_site()
