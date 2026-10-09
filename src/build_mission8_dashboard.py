"""Mission 8 Story Dashboard Builder: Left-hand story navigation, 12 dynamic cards, interactive tooltips, and live patrol."""

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
            width: 290px;
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
            justify-content: space-between;
            margin-bottom: 20px;
            padding-bottom: 14px;
            border-bottom: 1px solid var(--border-color);
        }

        .brand-logo {
            height: 40px;
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
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .nav-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 6px;
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
            flex-direction: column;
            gap: 2px;
            width: 100%;
            position: relative;
        }

        .nav-item-btn:hover {
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(56, 189, 248, 0.2);
        }

        .nav-item-btn.active {
            color: #ffffff;
            background: #192744;
            border-color: var(--primary-cyan);
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.18);
        }

        .nav-item-main {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
        }

        .nav-item-sub {
            font-size: 11px;
            color: #94a3b8;
            padding-left: 24px;
            font-weight: 400;
        }

        .sidebar-guide-btn {
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid #38bdf8;
            color: #38bdf8;
            padding: 10px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-bottom: 16px;
            transition: all 0.2s;
        }

        .sidebar-guide-btn:hover {
            background: rgba(56, 189, 248, 0.15);
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
            color: #ffffff;
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
            margin-left: 290px;
            flex: 1;
            padding: 24px 32px 60px 32px;
            max-width: 1400px;
        }

        /* Sticky Global Controls Header */
        .global-header {
            position: sticky;
            top: 0;
            background: rgba(13, 21, 39, 0.95);
            backdrop-filter: blur(12px);
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
            position: relative;
        }

        .control-label-box {
            display: flex;
            flex-direction: column;
        }

        .control-label {
            color: var(--text-main);
            font-weight: 700;
            font-size: 12.5px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .control-subtext {
            font-size: 10.5px;
            color: var(--text-muted);
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
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
            border: 1px solid var(--border-color);
            background: #080d1a;
            color: var(--text-muted);
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 2px;
        }

        .btn-toggle-key.active {
            background: rgba(239, 68, 68, 0.18);
            border-color: var(--fraud-red);
            color: #f87171;
            box-shadow: 0 0 14px rgba(239, 68, 68, 0.35);
        }

        /* Info Badge & Interactive Popover */
        .info-btn {
            background: rgba(56, 189, 248, 0.12);
            color: var(--primary-cyan);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 50%;
            width: 18px;
            height: 18px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s;
            user-select: none;
        }

        .info-btn:hover, .info-btn:focus {
            background: var(--primary-cyan);
            color: #080d1a;
            box-shadow: 0 0 8px var(--primary-cyan);
        }

        /* Tooltip Box */
        .tooltip-container {
            position: relative;
            display: inline-flex;
            align-items: center;
        }

        .popover-box {
            position: absolute;
            bottom: calc(100% + 10px);
            left: 50%;
            transform: translateX(-50%);
            background: #0f172a;
            border: 1px solid #38bdf8;
            border-radius: 8px;
            padding: 12px 14px;
            width: 280px;
            color: #f8fafc;
            font-size: 12px;
            line-height: 1.4;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6);
            pointer-events: none;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.2s ease, transform 0.2s ease;
            z-index: 999;
        }

        .popover-box::after {
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border-width: 6px;
            border-style: solid;
            border-color: #38bdf8 transparent transparent transparent;
        }

        .popover-box.align-right {
            left: auto;
            right: 0;
            transform: none;
        }
        .popover-box.align-right::after {
            left: auto;
            right: 20px;
            transform: none;
        }

        .tooltip-container:hover .popover-box,
        .tooltip-container:focus-within .popover-box,
        .popover-box.show {
            opacity: 1;
            visibility: visible;
            transform: translateX(-50%) translateY(-2px);
        }
        .tooltip-container:hover .popover-box.align-right,
        .tooltip-container:focus-within .popover-box.align-right,
        .popover-box.align-right.show {
            transform: translateY(-2px);
        }

        .popover-title {
            font-weight: 700;
            color: var(--primary-cyan);
            margin-bottom: 4px;
            font-size: 12.5px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .popover-desc {
            color: #cbd5e1;
            margin-bottom: 6px;
        }
        .popover-action {
            color: #f59e0b;
            font-size: 11px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 4px;
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
            display: flex;
            align-items: center;
            gap: 10px;
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

        /* Card Container */
        .story-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 22px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            position: relative;
        }

        .card-header-bar {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 8px;
            margin-bottom: 6px;
        }

        .card-question {
            font-size: 16px;
            font-weight: 700;
            color: #ffffff;
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
            display: flex;
            justify-content: space-between;
            align-items: center;
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
            position: relative;
            cursor: pointer;
            transition: all 0.2s;
        }
        .matrix-cell:hover {
            border-color: rgba(56, 189, 248, 0.4);
            transform: translateY(-2px);
        }
        .matrix-cell.tp { border-left: 4px solid var(--safe-green); }
        .matrix-cell.fp { border-left: 4px solid var(--alert-amber); }
        .matrix-cell.fn { border-left: 4px solid var(--fraud-red); }
        .matrix-cell.tn { border-left: 4px solid var(--honest-grey); }

        .matrix-cell-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .matrix-cell-title {
            font-size: 12.5px;
            font-weight: 700;
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

        /* Terminology Modal */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(8px);
            z-index: 1000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .modal-overlay.active {
            display: flex;
        }

        .modal-content {
            background: #0f172a;
            border: 1px solid #38bdf8;
            border-radius: 14px;
            max-width: 800px;
            width: 100%;
            max-height: 85vh;
            overflow-y: auto;
            padding: 26px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8);
            position: relative;
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-color);
        }

        .modal-title {
            font-size: 20px;
            font-weight: 700;
            color: var(--primary-cyan);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .modal-close-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 20px;
            cursor: pointer;
            padding: 4px 8px;
            border-radius: 4px;
        }
        .modal-close-btn:hover {
            color: white;
            background: rgba(255, 255, 255, 0.1);
        }

        .term-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 14px;
        }

        .term-card {
            background: #1e293b;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 14px;
        }

        .term-card-title {
            font-size: 14px;
            font-weight: 700;
            color: #38bdf8;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .term-card-tech {
            font-size: 11px;
            color: #94a3b8;
            margin-bottom: 6px;
        }
        .term-card-body {
            font-size: 12px;
            color: #e2e8f0;
            line-height: 1.4;
        }
        .term-card-example {
            font-size: 11px;
            color: #f59e0b;
            margin-top: 6px;
            border-top: 1px dashed rgba(255, 255, 255, 0.1);
            padding-top: 4px;
        }
    </style>
</head>
<body>

    <!-- Left-Hand Story Navigation -->
    <aside class="sidebar">
        <div class="brand-box">
            <img src="assets/sentinel-logo.svg" alt="Sentinel Logo" class="brand-logo">
        </div>

        <button class="sidebar-guide-btn" onclick="openGlossaryModal()">
            <span>📖</span> Beginner's Terminology Guide
        </button>

        <div class="nav-section-title">
            <span>Investigation Story</span>
            <span style="font-size:10px; color:#38bdf8;">7 Steps</span>
        </div>
        <ul class="nav-list">
            <li>
                <button class="nav-item-btn active" onclick="goToStep(1)">
                    <div class="nav-item-main">🔴 1. The Problem</div>
                    <div class="nav-item-sub">How rare is fraud?</div>
                </button>
            </li>
            <li>
                <button class="nav-item-btn" onclick="goToStep(2)">
                    <div class="nav-item-main">📊 2. The Data</div>
                    <div class="nav-item-sub">Past vs future timeline</div>
                </button>
            </li>
            <li>
                <button class="nav-item-btn" onclick="goToStep(3)">
                    <div class="nav-item-main">🔬 3. The Detector</div>
                    <div class="nav-item-sub">AI vs rules benchmark</div>
                </button>
            </li>
            <li>
                <button class="nav-item-btn" onclick="goToStep(4)">
                    <div class="nav-item-main">🎯 4. The Result</div>
                    <div class="nav-item-sub">Caught vs false alarms</div>
                </button>
            </li>
            <li>
                <button class="nav-item-btn" onclick="goToStep(5)">
                    <div class="nav-item-main">⚖️ 5. The Decision</div>
                    <div class="nav-item-sub">Cost curves & money saved</div>
                </button>
            </li>
            <li>
                <button class="nav-item-btn" onclick="goToStep(6)">
                    <div class="nav-item-main">📉 6. The Market Link</div>
                    <div class="nav-item-sub">Stock impact & compliance</div>
                </button>
            </li>
            <li>
                <button class="nav-item-btn" onclick="goToStep(7)">
                    <div class="nav-item-main">⏱️ 7. Live Patrol & Cases</div>
                    <div class="nav-item-sub">Live stream & dossier files</div>
                </button>
            </li>
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
            <!-- Control 1: Strictness Threshold -->
            <div class="control-group">
                <div class="control-label-box">
                    <div class="control-label">
                        <span>Filter Strictness</span>
                        <div class="tooltip-container">
                            <span class="info-btn" tabindex="0">i</span>
                            <div class="popover-box">
                                <div class="popover-title">🎯 Filter Strictness (θ)</div>
                                <div class="popover-desc">Sets how picky the AI detector is before sounding an alarm. Lower numbers catch more fraud; higher numbers reduce false alarms.</div>
                                <div class="popover-action">⚙️ Dragging this recalculates caught frauds, false alarms, and total costs instantly.</div>
                            </div>
                        </div>
                    </div>
                    <span class="control-subtext">Cutoff: <strong id="strictnessLabel" style="color:var(--primary-cyan);">0.50</strong></span>
                </div>
                <input type="range" id="strictnessRange" min="0" max="22" value="13" oninput="onStrictnessChange(this.value)">
            </div>

            <!-- Control 2: Review Cost Selector -->
            <div class="control-group">
                <div class="control-label-box">
                    <div class="control-label">
                        <span>Cost per Check</span>
                        <div class="tooltip-container">
                            <span class="info-btn" tabindex="0">i</span>
                            <div class="popover-box">
                                <div class="popover-title">💼 Cost per Human Check</div>
                                <div class="popover-desc">The salary, tooling, and customer support expense to investigate one flagged transaction.</div>
                                <div class="popover-action">⚙️ Selecting a cost finds the mathematically lowest-cost strictness setting.</div>
                            </div>
                        </div>
                    </div>
                    <span class="control-subtext">Analyst expense per alert</span>
                </div>
                <select id="checkingCostSelect" onchange="onCheckingCostChange(this.value)">
                    <option value="100">100 CU / check (Low)</option>
                    <option value="500" selected>500 CU / check (Base Standard)</option>
                    <option value="2000">2,000 CU / check</option>
                    <option value="5000">5,000 CU / check</option>
                    <option value="25000">25,000 CU / check (Specialist)</option>
                    <option value="100000">100,000 CU / check</option>
                    <option value="500000">500,000 CU / check (High Legal)</option>
                </select>
            </div>

            <!-- Control 3: Answer Key / Ground Truth -->
            <div class="control-group">
                <div class="tooltip-container">
                    <button class="btn-toggle-key" id="evalKeyToggle" onclick="toggleAnswerKey()">
                        <span id="evalKeyText">👁️ Show True Fraud: OFF</span>
                        <span style="font-size:10px; opacity:0.8;">[Reveal bank ground truth]</span>
                    </button>
                    <div class="popover-box align-right">
                        <div class="popover-title">👁️ Reveal Ground Truth (Answer Key)</div>
                        <div class="popover-desc">By default, true fraud labels are masked like in real life. Turning this ON unmasks confirmed fraud answers in red across all cards.</div>
                        <div class="popover-action">⚙️ Click to toggle true fraud visibility on/off.</div>
                    </div>
                </div>
            </div>

            <!-- Guide Button in Header -->
            <button class="btn btn-secondary" onclick="openGlossaryModal()" style="font-size:12px; gap:6px;">
                <span>💡 Cheat Sheet</span>
            </button>
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
                    <div class="card-header-bar">
                        <div class="card-question">How rare is financial fraud in digital payments?</div>
                        <div class="tooltip-container">
                            <span class="info-btn" tabindex="0">i</span>
                            <div class="popover-box align-right">
                                <div class="popover-title">🔍 Class Imbalance</div>
                                <div class="popover-desc">When only 1 in 800 transactions is fraud, regular accuracy is deceiving. An algorithm that flags nothing is 99.4% accurate but completely useless!</div>
                            </div>
                        </div>
                    </div>
                    <div class="card-headline" id="c1Headline">Loading...</div>
                    <div class="card-visual-box">
                        <div class="dot-grid-container" id="c1DotGrid"></div>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Extreme rarity requires models that focus on <em>Precision</em> (accuracy of alarms) and <em>Recall</em> (percentage of fraud stopped) rather than plain accuracy.
                    </div>
                    <div class="card-source-footer">Source: docs/data/data_overview.json</div>
                </div>

                <!-- Card 2 -->
                <div class="story-card">
                    <div class="card-header-bar">
                        <div class="card-question">Which payment types carry fraud risk?</div>
                        <div class="tooltip-container">
                            <span class="info-btn" tabindex="0">i</span>
                            <div class="popover-box align-right">
                                <div class="popover-title">💳 Payment Channels</div>
                                <div class="popover-desc">Fraudsters only steal money by transferring it out (TRANSFER) or cashing out at an ATM/agent (CASH_OUT). Merchant payments (PAYMENT) are completely safe in this dataset.</div>
                            </div>
                        </div>
                    </div>
                    <div class="card-headline" id="c2Headline">Loading...</div>
                    <div class="card-visual-box">
                        <canvas id="c2Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Fraud is structurally confined to outbound transfers and cash-outs. Low-risk merchant purchases and deposits can safely bypass heavy screening.
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
                <h2 class="step-title">The Data: Past vs Future Split & Payment Patterns</h2>
                <p class="step-sub">Preventing lookahead data leakage and analyzing monetary and 24-hour day/night cycles.</p>
            </div>

            <div class="cards-grid">
                <!-- Card 3 -->
                <div class="story-card">
                    <div class="card-header-bar">
                        <div class="card-question">How is the data split across time to prevent cheating?</div>
                        <div class="tooltip-container">
                            <span class="info-btn" tabindex="0">i</span>
                            <div class="popover-box align-right">
                                <div class="popover-title">⏳ Temporal Train/Test Split</div>
                                <div class="popover-desc">We train only on past steps (1–333) and test on future steps (334–742). Randomly shuffling data would be cheating because in real life you cannot see future fraud!</div>
                            </div>
                        </div>
                    </div>
                    <div class="card-headline" id="c3Headline">Loading...</div>
                    <div class="card-visual-box">
                        <canvas id="c3Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Temporal splitting strictly evaluates the model on unseen future days, faithfully replicating live bank deployment.
                    </div>
                    <div class="card-source-footer">Source: docs/data/data_overview.json</div>
                </div>

                <!-- Card 4 -->
                <div class="story-card">
                    <div class="card-header-bar">
                        <div class="card-question">How do stolen amounts compare to honest payments?</div>
                        <div class="tooltip-container">
                            <span class="info-btn" tabindex="0">i</span>
                            <div class="popover-box align-right">
                                <div class="popover-title">💰 Log-Scale Amount Distribution</div>
                                <div class="popover-desc">Honest payments range from small to large, but fraudsters almost always try to drain large sums (>200,000 currency units) at once.</div>
                            </div>
                        </div>
                    </div>
                    <div class="card-headline" id="c4Headline">Loading...</div>
                    <div class="card-visual-box">
                        <canvas id="c4Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Fraudsters aim for maximum money stolen per compromised account. However, high amount alone is not enough to prove guilt.
                    </div>
                    <div class="card-source-footer">Source: docs/data/amount_hist.csv</div>
                </div>
            </div>

            <!-- Card 5 -->
            <div class="cards-grid-full">
                <div class="story-card">
                    <div class="card-header-bar">
                        <div class="card-question">When does fraud happen during the 24-hour day/night cycle?</div>
                        <div class="tooltip-container">
                            <span class="info-btn" tabindex="0">i</span>
                            <div class="popover-box align-right">
                                <div class="popover-title">🌙 Diurnal 24-Hour Pattern</div>
                                <div class="popover-desc">Humans sleep at night, so honest payments drop between 11 PM and 6 AM. Automated fraud bots and money drainers run constantly 24/7.</div>
                            </div>
                        </div>
                    </div>
                    <div class="card-headline" id="c5Headline">Loading...</div>
                    <div class="card-visual-box" style="height:260px;">
                        <canvas id="c5Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Honest payments follow normal business hours, while automated theft scripts operate around the clock, making nighttime transfers relatively more risky.
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
                    <div class="card-header-bar">
                        <div class="card-question">Which detector catches fraud best without cheating?</div>
                        <div class="tooltip-container">
                            <span class="info-btn" tabindex="0">i</span>
                            <div class="popover-box align-right">
                                <div class="popover-title">🏆 PR-AUC Discovery Power</div>
                                <div class="popover-desc">PR-AUC measures how well a model discovers rare fraud across all strictness levels. Higher is much better (Random Forest achieves 0.3371 vs random baseline 0.0063).</div>
                            </div>
                        </div>
                    </div>
                    <div class="card-headline" id="c6Headline">Loading...</div>
                    <div class="card-visual-box">
                        <canvas id="c6Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Random Forest achieves a PR-AUC of 0.3371 (~53x higher than random guessing), outperforming simple rules and unweighted models without using leaked balance columns.
                    </div>
                    <div class="card-source-footer">Source: docs/data/detector_comparison.csv</div>
                </div>

                <!-- Card 7 -->
                <div class="story-card">
                    <div class="card-header-bar">
                        <div class="card-question">How confident is the AI detector across all transactions?</div>
                        <div class="tooltip-container">
                            <span class="info-btn" tabindex="0">i</span>
                            <div class="popover-box align-right">
                                <div class="popover-title">📊 Score Histogram</div>
                                <div class="popover-desc">Shows the distribution of AI suspicion scores. Over 96% of payments are cleanly scored near 0.0, meaning normal users are not bothered by false alarms.</div>
                            </div>
                        </div>
                    </div>
                    <div class="card-headline" id="c7Headline">Loading...</div>
                    <div class="card-visual-box">
                        <canvas id="c7Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> 97.6% of transactions score below 0.10, showing the detector concentrates risk into a small, manageable investigation queue.
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
                    <div class="card-header-bar">
                        <div class="card-question">What is the operational outcome at the chosen strictness?</div>
                        <div class="tooltip-container">
                            <span class="info-btn" tabindex="0">i</span>
                            <div class="popover-box align-right">
                                <div class="popover-title">🎯 The 2x2 Outcome Box</div>
                                <div class="popover-desc">Breaks transactions into 4 buckets: Caught Fraud (thieves stopped), False Alarms (innocent questioned), Missed Fraud (theft lost), and Clean Passes (innocent approved).</div>
                            </div>
                        </div>
                    </div>
                    <div class="card-headline" id="c8Headline">Loading...</div>
                    <div class="card-visual-box">
                        <div class="matrix-2x2" id="c8Matrix"></div>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Lower strictness captures more fraud (higher catch rate) but increases false alarms for analysts to verify.
                    </div>
                    <div class="card-source-footer">Source: docs/data/threshold_curve.csv</div>
                </div>

                <!-- Card 9 -->
                <div class="story-card">
                    <div class="card-header-bar">
                        <div class="card-question">What is the total financial loss at this checking cost?</div>
                        <div class="tooltip-container">
                            <span class="info-btn" tabindex="0">i</span>
                            <div class="popover-box align-right">
                                <div class="popover-title">📉 Financial Cost Curve</div>
                                <div class="popover-desc">Total Loss = (Missed Fraud Stolen Money) + (Alerts × Cost per Human Check). The red dot marks the lowest-loss strictness setting.</div>
                            </div>
                        </div>
                    </div>
                    <div class="card-headline" id="c9Headline">Loading...</div>
                    <div class="card-visual-box">
                        <canvas id="c9Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> <em>"The best strictness depends on the cost of one check."</em> Because missing large fraud is so costly, catching fraud skews the optimal setting toward sensitive thresholds.
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
                    <div class="card-header-bar">
                        <div class="card-question">How much fraud money is stopped under each policy?</div>
                        <div class="tooltip-container">
                            <span class="info-btn" tabindex="0">i</span>
                            <div class="popover-box align-right">
                                <div class="popover-title">⚖️ Three Operating Policies</div>
                                <div class="popover-desc">Compares Strict (catch everything), Balanced (standard trade-off), and Lenient (low analyst workload).</div>
                            </div>
                        </div>
                    </div>
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
                    <div class="card-header-bar">
                        <div class="card-question">What happens to fintech company value when fraud controls fail?</div>
                        <div class="tooltip-container">
                            <span class="info-btn" tabindex="0">i</span>
                            <div class="popover-box align-right">
                                <div class="popover-title">📈 Stock & Regulatory Shock</div>
                                <div class="popover-desc">When regulators step in due to weak fraud monitoring, stock value plunges and price volatility doubles. Strong AI fraud auditing protects the entire enterprise.</div>
                            </div>
                        </div>
                    </div>
                    <div class="card-headline" id="c11Headline">Loading...</div>
                    <div class="card-visual-box" style="height:320px;">
                        <canvas id="c11Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Weak supervisory AML/KYC controls lead to direct equity destruction and regulatory license restrictions. Automated multi-agent monitoring with full audit logs guarantees compliance under regulatory directives.
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
                <div class="card-header-bar">
                    <div class="card-question">How does Sentinel monitor transactions live?</div>
                    <div class="tooltip-container">
                        <span class="info-btn" tabindex="0">i</span>
                        <div class="popover-box align-right">
                            <div class="popover-title">⏱️ Live Patrol Replay</div>
                            <div class="popover-desc">Replays each simulated hour from step 334 to 742. Use Play, Pause, Scrubber, and Speed controls to inspect traffic surges and alarms.</div>
                        </div>
                    </div>
                </div>
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
                <div class="card-header-bar">
                    <div class="card-question">Forensic Case File Dossier (Precomputed Multi-Agent Synthesis)</div>
                    <div class="tooltip-container">
                        <span class="info-btn" tabindex="0">i</span>
                        <div class="popover-box align-right">
                            <div class="popover-title">📁 Investigation Case Files</div>
                            <div class="popover-desc">Detailed multi-agent investigative reports summarizing transaction flags, user history, and final risk officer decisions.</div>
                        </div>
                    </div>
                </div>
                <div style="display:flex; gap:12px; margin-bottom:14px; align-items:center; flex-wrap:wrap;">
                    <label style="font-size:12px; color:var(--text-muted);">Select Alert Dossier:</label>
                    <select id="patrolCaseSelect" onchange="renderCaseDossier(this.value)" style="min-width:320px;"></select>
                </div>
                <div id="patrolCaseDossierBox"></div>
                <div class="card-source-footer" style="margin-top:14px;">Source: docs/data/stream.json (cases)</div>
            </div>
        </section>

    </main>

    <!-- Beginners' Terminology Modal Dialog -->
    <div class="modal-overlay" id="glossaryModal" onclick="closeGlossaryModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header">
                <div class="modal-title">📖 Beginner's Fraud Intelligence Cheat Sheet</div>
                <button class="modal-close-btn" onclick="closeGlossaryModal()">✕</button>
            </div>
            <p style="color:var(--text-muted); font-size:13px; margin-bottom:16px;">
                Everything in Sentinel explained in simple, everyday language. Hover over any <span class="info-btn">i</span> button on the dashboard for instant help!
            </p>

            <div class="term-grid">
                <div class="term-card">
                    <div class="term-card-title">🎯 Filter Strictness (θ)</div>
                    <div class="term-card-tech">Technical term: Decision Threshold</div>
                    <div class="term-card-body">The sensitivity cutoff. Scores above this number sound an alarm. Low (0.01) catches almost all fraud; high (0.80) only alarms on high-confidence cases.</div>
                    <div class="term-card-example">💡 Rule of thumb: Low review cost = keep strictness low to stop big theft.</div>
                </div>

                <div class="term-card">
                    <div class="term-card-title">💼 Cost per Check</div>
                    <div class="term-card-tech">Technical term: Review / Inspection Cost</div>
                    <div class="term-card-body">The money spent paying an analyst and running support when a payment is held for verification. Baseline is 500 currency units.</div>
                    <div class="term-card-example">💡 High review costs push companies to raise strictness.</div>
                </div>

                <div class="term-card">
                    <div class="term-card-title">👁️ Show True Fraud</div>
                    <div class="term-card-tech">Technical term: Ground Truth / Answer Key</div>
                    <div class="term-card-body">In real life, you don't know who is a thief until days later. This toggle unmasks the actual verified fraud answers in red for evaluation.</div>
                    <div class="term-card-example">💡 Keep OFF for realistic simulation; turn ON to grade performance.</div>
                </div>

                <div class="term-card">
                    <div class="term-card-title">🟢 Caught Fraud</div>
                    <div class="term-card-tech">Technical term: True Positive (TP)</div>
                    <div class="term-card-body">A real fraudster successfully caught and blocked by the model. Money saved!</div>
                </div>

                <div class="term-card">
                    <div class="term-card-title">🟡 False Alarm</div>
                    <div class="term-card-tech">Technical term: False Positive (FP)</div>
                    <div class="term-card-body">An innocent customer flagged by mistake. Costs analyst time to review and clear.</div>
                </div>

                <div class="term-card">
                    <div class="term-card-title">🔴 Missed Fraud</div>
                    <div class="term-card-tech">Technical term: False Negative (FN)</div>
                    <div class="term-card-body">A thief who slipped past the detector. The entire stolen principal is lost!</div>
                </div>

                <div class="term-card">
                    <div class="term-card-title">⚪ Clean Pass</div>
                    <div class="term-card-tech">Technical term: True Negative (TN)</div>
                    <div class="term-card-body">An honest payment approved immediately without annoying the user.</div>
                </div>

                <div class="term-card">
                    <div class="term-card-title">🏆 PR-AUC Discovery Power</div>
                    <div class="term-card-tech">Technical term: Precision-Recall Area Under Curve</div>
                    <div class="term-card-body">The master score for fraud AI. Measures how well the model catches rare needles in a giant haystack without drowning in false alarms.</div>
                </div>

                <div class="term-card">
                    <div class="term-card-title">⏳ Past vs Future Split</div>
                    <div class="term-card-tech">Technical term: Temporal Train/Test Split</div>
                    <div class="term-card-body">Training on past days (steps 1–333) and testing on future days (steps 334–742) so the AI never cheats by looking ahead.</div>
                </div>

                <div class="term-card">
                    <div class="term-card-title">🔗 Same-Step Pair</div>
                    <div class="term-card-tech">Technical term: Correlated Laundering Graph</div>
                    <div class="term-card-body">When stolen funds are transferred to an accomplice and cashed out at the exact same hour for the exact same amount.</div>
                </div>
            </div>
        </div>
    </div>

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

        function openGlossaryModal() {
            document.getElementById('glossaryModal').classList.add('active');
        }

        function closeGlossaryModal(e) {
            if (!e || e.target === document.getElementById('glossaryModal') || e.target.classList.contains('modal-close-btn')) {
                document.getElementById('glossaryModal').classList.remove('active');
            }
        }

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
            document.getElementById('evalKeyText').innerText = evalMode ? "👁️ Show True Fraud: ON" : "👁️ Show True Fraud: OFF";
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
                document.getElementById('c1Headline').innerText = `Fraud represents under 1% of digital payments across the network, making detection an extreme needle-in-a-haystack challenge.`;
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
            document.getElementById('c3Headline').innerText = `Training on past steps 1–${sp.split_step} (${sp.train_rows.toLocaleString()} payments) and evaluating on future steps ${sp.test_steps[0]}–${sp.test_steps[1]} (${sp.test_rows.toLocaleString()} payments).`;

            const ctx = document.getElementById('c3Chart').getContext('2d');
            if (chartC3) chartC3.destroy();
            chartC3 = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Past Training (Steps 1-333: 75%)', 'Future Test (Steps 334-742: 25%)'],
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
                        label: 'PR-AUC (Fraud Discovery Score)',
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
                <div class="matrix-cell tp" title="Caught Fraud: Real criminals stopped">
                    <div class="matrix-cell-header">
                        <span class="matrix-cell-title">🟢 Caught Fraud</span>
                        <span class="info-btn">i</span>
                    </div>
                    <div class="matrix-cell-tech">True Positives (TP)</div>
                    <div class="matrix-cell-val" style="color:var(--safe-green);">${evalMode ? row.tp.toLocaleString() : 'Masked (Turn ON Ground Truth)'}</div>
                </div>
                <div class="matrix-cell fp" title="False Alarm: Innocent customers flagged for review">
                    <div class="matrix-cell-header">
                        <span class="matrix-cell-title">🟡 False Alarms</span>
                        <span class="info-btn">i</span>
                    </div>
                    <div class="matrix-cell-tech">False Positives (FP)</div>
                    <div class="matrix-cell-val" style="color:var(--alert-amber);">${evalMode ? row.fp.toLocaleString() : alerts.toLocaleString() + ' Alerts'}</div>
                </div>
                <div class="matrix-cell fn" title="Missed Fraud: Thieves who got away undetected">
                    <div class="matrix-cell-header">
                        <span class="matrix-cell-title">🔴 Missed Fraud</span>
                        <span class="info-btn">i</span>
                    </div>
                    <div class="matrix-cell-tech">False Negatives (FN)</div>
                    <div class="matrix-cell-val" style="color:var(--fraud-red);">${evalMode ? row.fn.toLocaleString() : 'Masked (Turn ON Ground Truth)'}</div>
                </div>
                <div class="matrix-cell tn" title="Clean Passes: Honest customers approved smoothly">
                    <div class="matrix-cell-header">
                        <span class="matrix-cell-title">⚪ Clean Passes</span>
                        <span class="info-btn">i</span>
                    </div>
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
                        x: { title: { display: true, text: 'Filter Strictness (θ)', color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
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

    print("Successfully built Mission 8 Story Dashboard with Easy Terminology and Interactive Tooltips at index.html and docs/index.html")

if __name__ == "__main__":
    build_mission8_site()
