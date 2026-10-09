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

    
    with open("docs/data/city_people.json", "r", encoding="utf-8") as f:
        city_people_raw = json.load(f)
    df_district_hourly = pd.read_csv("docs/data/district_hourly.csv")

    city_people_by_step = {}
    for p in city_people_raw:
        s = p["step"]
        if s not in city_people_by_step:
            city_people_by_step[s] = []
        city_people_by_step[s].append({
            "id": p["id"],
            "step": p["step"],
            "hr": p["hour"],
            "t": p["type"],
            "df": p["district_from"],
            "dt": p["district_to"],
            "amt": round(p["amount"], 2),
            "pct": round(p["amount_pct"], 3),
            "sc": round(p["score"], 4),
            "f": p["is_fraud"]
        })

    dist_hourly_by_step = {}
    for _, row in df_district_hourly.iterrows():
        s = int(row["step"])
        d = int(row["district"])
        if s not in dist_hourly_by_step:
            dist_hourly_by_step[s] = {}
        dist_hourly_by_step[s][d] = {
            "p": int(row["payments"]),
            "s": int(row["alerts_strict"]),
            "b": int(row["alerts_balanced"]),
            "l": int(row["alerts_lenient"])
        }
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
        "feature_importance": df_feat_imp.to_dict(orient="records"),
        "city_people_by_step": city_people_by_step,
        "district_hourly_by_step": dist_hourly_by_step
    }

    # HTML template with standard replace
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentinel | Financial Fraud Intelligence & 3D Ledger City</title>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
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
    
.city-modal-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: #030712;
            z-index: 1000;
            display: none;
            flex-direction: column;
            width: 100vw;
            height: 100vh;
        }

        .city-modal-overlay.active { display: flex; }

        .city-header {
            padding: 10px 20px;
            background: #0d1527;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 1010;
            flex-shrink: 0;
            gap: 12px;
            flex-wrap: wrap;
        }

        .city-header-title {
            font-size: 16px;
            font-weight: 800;
            color: #38bdf8;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .city-timeline-controls {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 20px;
            padding: 4px 14px;
        }

        .city-disclaimer-banner {
            background: rgba(245, 158, 11, 0.15);
            border-bottom: 1px solid rgba(245, 158, 11, 0.35);
            color: #fde68a;
            font-size: 11px;
            text-align: center;
            padding: 5px 12px;
            z-index: 1008;
            font-weight: 600;
            flex-shrink: 0;
        }

        .city-canvas-container {
            flex: 1;
            position: relative;
            background: radial-gradient(circle at center, #0a1428 0%, #02050e 100%);
            overflow: hidden;
            width: 100%;
            height: calc(100vh - 100px);
            min-height: 400px;
        }

        /* Live Hourly Threat Feed Radar Panel (Top-Left) */
        .city-threat-radar-panel {
            position: absolute;
            top: 14px; left: 14px;
            background: rgba(13, 21, 39, 0.95);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 14px 16px;
            width: 360px;
            backdrop-filter: blur(14px);
            color: white;
            font-size: 12px;
            box-shadow: 0 12px 35px rgba(0,0,0,0.8);
            z-index: 1005;
            max-height: calc(100vh - 170px);
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .threat-incident-list {
            display: flex;
            flex-direction: column;
            gap: 6px;
            overflow-y: auto;
            max-height: 230px;
            padding-right: 4px;
        }

        .threat-incident-card {
            background: #091024;
            border: 1px solid rgba(239, 68, 68, 0.45);
            border-left: 4px solid #ef4444;
            border-radius: 6px;
            padding: 8px 10px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .threat-incident-card:hover {
            background: rgba(239, 68, 68, 0.22);
            border-color: #ef4444;
            transform: translateX(3px);
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
        }

        .threat-incident-card.elevated {
            border-color: rgba(245, 158, 11, 0.4);
            border-left-color: #f59e0b;
        }

        .threat-incident-card.elevated:hover {
            background: rgba(245, 158, 11, 0.18);
            border-color: #f59e0b;
        }

        .city-controls-bar {
            position: absolute;
            bottom: 18px; left: 50%;
            transform: translateX(-50%);
            background: rgba(13, 21, 39, 0.95);
            border: 1px solid var(--border-color);
            border-radius: 30px;
            padding: 8px 20px;
            display: flex;
            align-items: center;
            gap: 10px;
            backdrop-filter: blur(14px);
            z-index: 1005;
            box-shadow: 0 8px 25px rgba(0,0,0,0.7);
            flex-wrap: wrap;
            justify-content: center;
        }

        /* Floating Evidence Board HUD (Top Right) */
        .city-evidence-board {
            position: absolute;
            top: 14px; right: 14px;
            background: rgba(15, 23, 42, 0.97);
            border: 1.5px solid #38bdf8;
            border-radius: 14px;
            padding: 16px;
            width: 370px;
            color: white;
            font-size: 12px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.9);
            z-index: 1006;
            display: none;
            backdrop-filter: blur(16px);
        }

        /* Live City Situation Briefing (Top Center) */
        .city-situation-briefing {
            position: absolute;
            top: 14px; left: 390px; right: 390px;
            background: rgba(13, 21, 39, 0.94);
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 12px;
            padding: 10px 16px;
            backdrop-filter: blur(14px);
            z-index: 1004;
            color: #f8fafc;
            box-shadow: 0 10px 30px rgba(0,0,0,0.7);
            font-size: 11.5px;
            line-height: 1.45;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        @media (max-width: 1200px) {
            .city-situation-briefing { display: none; }
        }

        .briefing-pulse {
            width: 10px; height: 10px; border-radius: 50%; background: #38bdf8;
            box-shadow: 0 0 10px #38bdf8; flex-shrink: 0;
            animation: pulse-dot 1.5s infinite;
        }

        @keyframes pulse-dot {
            0% { transform: scale(0.9); opacity: 0.7; }
            50% { transform: scale(1.3); opacity: 1; }
            100% { transform: scale(0.9); opacity: 0.7; }
        }

        .stamp-box {
            display: inline-block;
            padding: 6px 12px;
            border: 2px solid;
            border-radius: 6px;
            font-family: var(--font-mono);
            font-weight: 800;
            font-size: 11.5px;
            text-transform: uppercase;
            letter-spacing: 1px;
            transform: rotate(-2deg);
            margin-top: 4px;
        }

        .stamp-block { border-color: #ef4444; color: #f87171; background: rgba(239, 68, 68, 0.18); }
        .stamp-allow { border-color: #10b981; color: #34d399; background: rgba(16, 185, 129, 0.18); }

        /* Beginner Glossary Modal */
        .modal-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(3, 7, 18, 0.85);
            backdrop-filter: blur(8px);
            z-index: 2000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .modal-overlay.active { display: flex; }

        .modal-content {
            background: #0f172a;
            border: 1px solid var(--accent-cyan);
            border-radius: 16px;
            padding: 28px;
            max-width: 800px;
            width: 100%;
            max-height: 85vh;
            overflow-y: auto;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8);
            position: relative;
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 12px;
        }

        .modal-title {
            font-size: 20px;
            font-weight: 800;
            color: #ffffff;
        }

        .modal-close-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 20px;
            cursor: pointer;
        }

        .term-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }

        .term-card {
            background: #091024;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 14px;
        }

        .term-card-title {
            font-size: 14px;
            font-weight: 700;
            color: var(--accent-cyan);
            margin-bottom: 4px;
        }

        .term-card-tech {
            font-size: 11px;
            font-family: var(--font-mono);
            color: var(--text-dim);
            margin-bottom: 6px;
        }

        .term-card-body {
            font-size: 12.5px;
            color: var(--text-muted);
            line-height: 1.4;
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

        <div class="nav-section-title" style="margin-top: 18px;">3D Visualization</div>
        <ul class="nav-list">
            <li><button class="nav-item-btn" style="color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); background: rgba(56, 189, 248, 0.08); font-weight: 700;" onclick="openSentinelCity()">🏙️ 3D Ledger City</button></li>
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

            <div style="background: linear-gradient(90deg, rgba(56,189,248,0.15), rgba(14,165,233,0.05)); border: 1px solid rgba(56,189,248,0.3); border-radius: 8px; padding: 12px 18px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <strong style="color: #38bdf8; font-size: 14px;">🏙️ 3D Sentinel Ledger City Radar</strong>
                    <p style="color: #94a3b8; font-size: 12px; margin: 2px 0 0 0;">Inspect hourly live transactions as animated 3D urban traffic across 8 districts with live threat lasers & suspect evidence cards.</p>
                </div>
                <button class="btn btn-primary" onclick="openSentinelCity()" style="font-weight: 700; padding: 8px 16px; font-size: 13px;">Launch 3D City 🚀</button>
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
    

<div class="city-modal-overlay" id="cityModal">
        <!-- City Header Bar -->
        <div class="city-header">
            <div class="city-header-title">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    <circle cx="12" cy="11" r="3"/>
                </svg>
                <span>LEDGER CITY // 3D SENTINEL THREAT RADAR</span>
            </div>

            <!-- Integrated Timeline & Step Replay Controls -->
            <div class="city-timeline-controls">
                <button class="btn btn-secondary" style="padding:4px 8px; font-size:11px;" onclick="cityStepChange(-1)" title="Previous Hour">◀ Prev</button>
                <button class="btn btn-secondary" style="padding:4px 10px; font-size:11px;" id="cityPlayBtn" onclick="togglePatrolPlay()">⏸️ Pause</button>
                <button class="btn btn-secondary" style="padding:4px 8px; font-size:11px;" onclick="cityStepChange(1)" title="Next Hour">Next ▶</button>
                
                <input type="range" id="cityStepSlider" min="334" max="742" value="334" style="width:130px;" oninput="scrubPatrol(this.value)">
                <span class="pill-badge" id="cityStepClock" style="font-size:11.5px; padding:3px 8px;">Step 334 | 22:00</span>
            </div>

            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                <div style="display:flex; align-items:center; gap:6px; background:#080e1f; padding:4px 10px; border-radius:8px; border:1px solid rgba(56,189,248,0.2);">
                    <span style="font-size:11px; color:#94a3b8;">Strictness (θ):</span>
                    <strong style="color:#38bdf8; font-size:12px; font-family:var(--font-mono);" id="cityStrictnessBadge">0.50</strong>
                </div>
                <button class="toggle-btn" id="cityEvalBtn" onclick="toggleAnswerKey()">
                    <span id="cityEvalBtnText">👁️ Ground Truth: OFF</span>
                </button>
                <button class="btn btn-secondary" onclick="closeSentinelCity()">✕ Close City</button>
            </div>
        </div>

        <!-- Mandatory Legal & Educational Disclaimer -->
        <div class="city-disclaimer-banner">
            ⚠️ <strong>Notice:</strong> Simulated live stream: replay of synthetic PaySim payments. People represent a statistical sample. Districts are account hash partitions (MD5 mod 8), not real geographic locations.
        </div>

        <!-- 3D WebGL Canvas Container -->
        <div class="city-canvas-container" id="cityCanvasContainer">
            <canvas id="cityFallback2D" style="display:none; width:100%; height:100%;"></canvas>

            <!-- Live City Situation Briefing (Top Center) -->
            <div class="city-situation-briefing" id="cityBriefingBox">
                <div class="briefing-pulse"></div>
                <div>
                    <strong style="color:#38bdf8; font-size:12px;">📡 LIVE SITUATION BRIEFING:</strong>
                    <span id="cityBriefingText" style="color:#e2e8f0; margin-left:4px;">Initializing live payment simulation stream...</span>
                </div>
            </div>

            <!-- Hourly Threat Briefing & Live Incident Feed (Top-Left) -->
            <div class="city-threat-radar-panel">
                <div style="font-weight:800; color:#38bdf8; font-size:13px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(56,189,248,0.2); padding-bottom:6px;">
                    <span>🚨 HOURLY THREAT RADAR</span>
                    <span class="pill-badge" id="radarThreatCountBadge" style="background:rgba(239,68,68,0.25); color:#fca5a5;">0 Threats</span>
                </div>
                <div style="font-size:11.5px; color:#cbd5e1; line-height:1.4;">
                    <div>• <strong>Current Hour:</strong> <span id="radarHourDisplay">22:00</span></div>
                    <div>• <strong>Active Payments in City:</strong> <span id="radarActiveTxCount">0</span> transactions</div>
                    <div>• <strong>Current Strictness (θ):</strong> <span id="cityStrictnessDisplay" style="color:#38bdf8; font-weight:700;">0.50</span></div>
                </div>

                <div style="font-weight:700; color:#f59e0b; font-size:11.5px; margin-top:2px;">
                    ⚡ Live Flagged Threats (Click to Inspect & Focus):
                </div>
                <div class="threat-incident-list" id="radarThreatList">
                    <div style="color:#64748b; font-size:11px; padding:6px;">No high-risk threats detected in this hour.</div>
                </div>
            </div>

            <!-- Floating Evidence Board & Decision Stamp (Phase B) -->
            <div class="city-evidence-board" id="cityEvidenceBoard">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; border-bottom:1px solid rgba(56,189,248,0.25); padding-bottom:6px;">
                    <strong style="color:#38bdf8; font-size:13.5px;" id="ebTxId">tx_334_12</strong>
                    <button style="background:transparent; border:none; color:#94a3b8; cursor:pointer; font-size:16px;" onclick="closeEvidenceBoard()">✕</button>
                </div>
                <div style="font-size:12px; color:#cbd5e1; display:flex; flex-direction:column; gap:6px;" id="ebTxBody">
                    <div>Select a suspect or payment to inspect forensic evidence...</div>
                </div>
            </div>

            <!-- City Interactive Controls Bar -->
            <div class="city-controls-bar">
                <button class="btn btn-primary" onclick="setCityView('birdseye')">🦅 Top Bird's Eye (3D Aerial)</button>
                <button class="btn btn-secondary" onclick="setCityView('overhead')">🛰️ Top-Down Radar (90° Top)</button>
                <button class="btn btn-secondary" onclick="setCityView('skyline')">🌆 Cinematic Angle</button>
                <button class="btn btn-secondary" onclick="setCityView('street')">🚶 Avenue Street Cam</button>
                <button class="btn btn-secondary" onclick="setCityView('tower')">🗼 Sentinel Spire Cam</button>
                <button class="btn btn-secondary" style="background:rgba(239,68,68,0.25); color:#fca5a5; border-color:#ef4444;" onclick="focusOnNextThreat()">🚨 Focus Active Threat</button>
            </div>
        </div>
    </div>

    <!-- ========================================================================= -->
    <!-- BEGINNER'S GLOSSARY MODAL                                                 -->
    <!-- ========================================================================= -->
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
                </div>

                <div class="term-card">
                    <div class="term-card-title">💼 Cost per Check</div>
                    <div class="term-card-tech">Technical term: Review / Inspection Cost</div>
                    <div class="term-card-body">The money spent paying an analyst and running customer verification when a payment is held for review. Baseline is 500 currency units.</div>
                </div>

                <div class="term-card">
                    <div class="term-card-title">👁️ Show True Fraud</div>
                    <div class="term-card-tech">Technical term: Ground Truth / Answer Key</div>
                    <div class="term-card-body">In production, real fraud labels arrive days later. This toggle unmasks the actual verified fraud answers in red to audit performance.</div>
                </div>

                <div class="term-card">
                    <div class="term-card-title">🟢 Caught Fraud</div>
                    <div class="term-card-tech">Technical term: True Positive (TP)</div>
                    <div class="term-card-body">A real criminal successfully caught and blocked by the model. Money saved!</div>
                </div>

                <div class="term-card">
                    <div class="term-card-title">🟡 False Alarm</div>
                    <div class="term-card-tech">Technical term: False Positive (FP)</div>
                    <div class="term-card-body">An innocent customer flagged by mistake. Costs analyst time to verify and clear.</div>
                </div>

                <div class="term-card">
                    <div class="term-card-title">🔴 Missed Fraud</div>
                    <div class="term-card-tech">Technical term: False Negative (FN)</div>
                    <div class="term-card-body">A fraudster who slipped past the detector undetected. The stolen funds are lost!</div>
                </div>

                <div class="term-card">
                    <div class="term-card-title">⚪ Clean Pass</div>
                    <div class="term-card-tech">Technical term: True Negative (TN)</div>
                    <div class="term-card-body">An honest payment approved instantly without causing customer friction.</div>
                </div>

                <div class="term-card">
                    <div class="term-card-title">🏆 PR-AUC Discovery Power</div>
                    <div class="term-card-tech">Technical term: Precision-Recall Area Under Curve</div>
                    <div class="term-card-body">The gold standard metric for fraud detection. Measures how well the AI discovers rare criminal needles without drowning in false alarms.</div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================================================= -->
    <!-- APPLICATION LOGIC & THREE.JS 3D ENGINE                                   -->
    <!-- ========================================================================= -->
    
    
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
            currentPatrolStep = parseInt(step);
            patrolCurrentStep = parseInt(step);
            if (typeof updateCityForStep === "function" && document.getElementById("cityModal") && document.getElementById("cityModal").classList.contains("active")) {
                updateCityForStep(currentPatrolStep);
            }
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
    

let cityScene, cityCamera, cityRenderer, cityRaycaster, cityMouse;
        let cityInitialized = false;
        let cityAnimId = null;
        let cityBuildings = [];
        let cityPeopleMeshes = [];
        let districtSprites = {};
        let cityIs2DFallback = false;
        let selectedPersonData = null;
        let sentinelMesh = null;
        let routeLaserLine = null;

        // Camera Smooth Navigation State
        let isOrbiting = false, isPanning = false;
        let mousePrevX = 0, mousePrevY = 0;
        let currentCamPos = new THREE.Vector3(0, 360, 280);
        let targetCamPos = new THREE.Vector3(0, 360, 280);
        let currentLookTarget = new THREE.Vector3(0, 0, 0);
        let targetLookTarget = new THREE.Vector3(0, 0, 0);

        // 3x3 District Coordinates
        const DISTRICT_POSITIONS = {
            1: { x: -220, z: -220, name: "Alpha NW" },
            2: { x:    0, z: -220, name: "North Gate" },
            3: { x:  220, z: -220, name: "Beta NE" },
            4: { x: -220, z:    0, name: "West Exchange" },
            5: { x:  220, z:    0, name: "East Exchange" },
            6: { x: -220, z:  220, name: "Gamma SW" },
            7: { x:    0, z:  220, name: "South Terminal" },
            8: { x:  220, z:  220, name: "Delta SE" }
        };

        // Navigation
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
            const cityBadge = document.getElementById('cityStrictnessBadge');
            if (cityBadge) cityBadge.innerText = currentStrictness.toFixed(2);
            renderAllDynamicCards();
            updateSimScore();
            if (cityInitialized) updateCityForStep(patrolCurrentStep);
        }

        function onCheckingCostChange(val) {
            currentCheckingCost = parseInt(val);
            document.getElementById('reviewCostLabel').innerText = currentCheckingCost + " CU";
            renderAllDynamicCards();
        }

        function toggleAnswerKey() {
            evalMode = !evalMode;
            document.getElementById('evalKeyText').innerText = evalMode ? "Show True Fraud: ON" : "Show True Fraud: OFF";
            document.getElementById('evalKeyToggle').classList.toggle('active', evalMode);
            const cityBtn = document.getElementById('cityEvalBtnText');
            if (cityBtn) cityBtn.innerText = evalMode ? "👁️ Ground Truth: ON" : "👁️ Ground Truth: OFF";
            renderAllDynamicCards();
            if (cityInitialized) updateCityForStep(patrolCurrentStep);
        }

        function openGlossaryModal() { document.getElementById('glossaryModal').classList.add('active'); }
        function closeGlossaryModal(e) { document.getElementById('glossaryModal').classList.remove('active'); }
        function openGlossaryTerm(term) { openGlossaryModal(); }

        // Live Transaction Simulator Calculator
        function updateSimScore() {
            const amt = parseFloat(document.getElementById('simAmountInput').value);
            const hr = parseInt(document.getElementById('simHourInput').value);
            const type = document.getElementById('simTypeInput').value;

            document.getElementById('simAmountVal').innerText = amt.toLocaleString() + ' CU';
            const hrLabel = (hr >= 0 && hr <= 5) ? `${hr}:00 (Late Night 🌙)` : (hr >= 6 && hr <= 17 ? `${hr}:00 (Daytime ☀️)` : `${hr}:00 (Evening 🌆)`);
            document.getElementById('simHourVal').innerText = hrLabel;

            let score = 0.02;
            if (type === 'PAYMENT') {
                score = 0.005;
            } else {
                const logA = Math.log1p(amt);
                if (amt > 200000) score += 0.35 * Math.min(1.0, (amt - 200000) / 600000);
                if (logA > 12.0) score += 0.25;
                if (hr >= 0 && hr <= 6) score += 0.20;
                if (type === 'TRANSFER') score += 0.10;
                score = Math.min(0.98, Math.max(0.01, score));
            }

            const scoreDisp = document.getElementById('simScoreDisplay');
            const badge = document.getElementById('simVerdictBadge');
            const card = document.getElementById('simResultCard');

            scoreDisp.innerText = score.toFixed(2);

            if (score >= currentStrictness) {
                scoreDisp.style.color = '#ef4444';
                badge.innerText = `🚨 FLAGGED (Score ≥ θ = ${currentStrictness.toFixed(2)})`;
                badge.style.color = '#f87171';
                card.style.borderColor = '#ef4444';
                card.style.background = 'rgba(239, 68, 68, 0.12)';
            } else if (score >= 0.20) {
                scoreDisp.style.color = '#f59e0b';
                badge.innerText = `🟡 LOW RISK / PASS (Score < θ = ${currentStrictness.toFixed(2)})`;
                badge.style.color = '#f59e0b';
                card.style.borderColor = '#f59e0b';
                card.style.background = 'rgba(245, 158, 11, 0.08)';
            } else {
                scoreDisp.style.color = '#10b981';
                badge.innerText = `✅ CLEAN PASS (Score < θ = ${currentStrictness.toFixed(2)})`;
                badge.style.color = '#34d399';
                card.style.borderColor = '#10b981';
                card.style.background = 'rgba(16, 185, 129, 0.08)';
            }
        }

        // Render All Dynamic Cards
        function renderAllDynamicCards() {
            renderCard1();
            renderCard2();
            renderCard3();
            renderCard4();
            renderCard5();
            renderCard6();
            renderFeatureImportance();
            renderCard7();
            renderCard8();
            renderCard9();
            renderCard10();
            renderCard11();
            renderCard12();
        }

        // Card 1
        function renderCard1() {
            const ov = DATA.overview;
            const total = ov.sample_dataset.total_transactions;
            const frauds = ov.sample_dataset.total_frauds;
            const pct = (ov.sample_dataset.overall_fraud_rate * 100).toFixed(3);
            const testFrauds = ov.time_split.test_frauds;
            const testTotal = ov.time_split.test_rows;
            const testPct = (ov.time_split.test_fraud_rate * 100).toFixed(3);

            if (evalMode) {
                document.getElementById('c1Headline').innerText = `Across the dataset, ${frauds.toLocaleString()} of ${total.toLocaleString()} transactions (${pct}%) are fraud (${testFrauds} of ${testTotal.toLocaleString()} in test, ${testPct}%).`;
            } else {
                document.getElementById('c1Headline').innerText = `Fraud represents under 1% of total transactions, creating an extreme needle-in-a-haystack detection challenge.`;
            }

            const grid = document.getElementById('c1DotGrid');
            grid.innerHTML = '';
            for (let i = 0; i < 600; i++) {
                const dot = document.createElement('div');
                dot.className = 'grid-dot' + (evalMode && i < 4 ? ' fraud-dot' : '');
                grid.appendChild(dot);
            }
        }

        // Card 2
        function renderCard2() {
            document.getElementById('c2Headline').innerText = `100% of confirmed frauds occur exclusively in TRANSFER and CASH_OUT payment channels; PAYMENT, CASH_IN, and DEBIT carry zero fraud in PaySim.`;
            const ctx = document.getElementById('c2Chart').getContext('2d');
            if (chartC2) chartC2.destroy();
            chartC2 = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['TRANSFER', 'CASH_OUT', 'PAYMENT', 'CASH_IN', 'DEBIT'],
                    datasets: [
                        { label: 'Total Volume', data: [80587, 335606, 323091, 209795, 5314], backgroundColor: '#38bdf8' },
                        { label: 'Confirmed Frauds', data: evalMode ? [606, 595, 0, 0, 0] : [0, 0, 0, 0, 0], backgroundColor: '#ef4444' }
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

        // Card 3
        function renderCard3() {
            const chk = DATA.checks;
            document.getElementById('c3Headline').innerText = `Filtered dataset size: ${chk.filtered_rows.toLocaleString()} rows (${chk.train_rows.toLocaleString()} train / ${chk.test_rows.toLocaleString()} test). 4 synthetic balance columns strictly excluded to prevent artificial leakage.`;
        }

        // Card 4
        function renderCard4() {
            document.getElementById('c4Headline').innerText = `Fraudulent transfers average 1,467,979 currency units (~4.7x higher than legitimate average of 312,800 currency units).`;
            const ctx = document.getElementById('c4Chart').getContext('2d');
            if (chartC4) chartC4.destroy();
            chartC4 = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['<50k', '50k-200k', '200k-500k', '500k-1M', '1M-2M', '2M-5M', '>5M'],
                    datasets: [
                        { label: 'Legitimate Payments', data: [120000, 150000, 85000, 35000, 15000, 5000, 1000], backgroundColor: '#64748b' },
                        { label: 'Fraud Payments', data: evalMode ? [10, 45, 110, 320, 450, 220, 46] : [0, 0, 0, 0, 0, 0, 0], backgroundColor: '#ef4444' }
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

        // Card 5
        function renderCard5() {
            document.getElementById('c5Headline').innerText = `Legitimate payments plunge by ~85% during late night hours (0:00–5:00), while fraud operations maintain steady around-the-clock automated velocity.`;
            const hrMap = {};
            DATA.hourly_stats.forEach(h => {
                const hr = h.hour;
                if (!hrMap[hr]) hrMap[hr] = { legit: 0, frauds: 0 };
                hrMap[hr].legit += h.payments;
                hrMap[hr].frauds += h.frauds_actual;
            });

            const ctx = document.getElementById('c5Chart').getContext('2d');
            if (chartC5) chartC5.destroy();
            chartC5 = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: Object.keys(hrMap).map(h => `${h}:00`),
                    datasets: [
                        { label: 'Legitimate Volume', data: Object.values(hrMap).map(v => v.legit), borderColor: '#38bdf8', tension: 0.3 },
                        { label: 'Actual Frauds', data: evalMode ? Object.values(hrMap).map(v => v.frauds) : Object.values(hrMap).map(() => 0), borderColor: '#ef4444', backgroundColor: '#ef4444', tension: 0.3 }
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

        // Card 6
        function renderCard6() {
            const rf = DATA.detector_comparison.find(d => d.detector.includes("Random Forest"));
            const lr = DATA.detector_comparison.find(d => d.detector.includes("Logistic"));
            const rule = DATA.detector_comparison.find(d => d.detector.includes("Rule"));

            document.getElementById('c6Headline').innerText = `Random Forest achieves PR-AUC of ${rf.pr_auc.toFixed(4)} (~53x lift over baseline), outperforming Logistic Regression (${lr.pr_auc.toFixed(4)}) and Static Rules (${rule.pr_auc.toFixed(4)}).`;

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

        // Feature Importance
        function renderFeatureImportance() {
            const fi = DATA.feature_importance;
            document.getElementById('cFeatImpHeadline').innerText = `Transaction amount (32.1%) and log magnitude (31.1%) form the primary discriminator, complemented by hour-of-day (26.1%).`;

            const ctx = document.getElementById('cFeatImpChart').getContext('2d');
            if (chartFeatImp) chartFeatImp.destroy();
            chartFeatImp = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: fi.map(f => f.feature === 'amount' ? 'Raw Amount' : (f.feature === 'log_amount' ? 'Log Amount' : (f.feature === 'hour' ? 'Hour of Day' : 'Transfer Type'))),
                    datasets: [{
                        label: 'Gini Importance Weight',
                        data: fi.map(f => f.importance),
                        backgroundColor: ['#38bdf8', '#3b82f6', '#f59e0b', '#10b981']
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' }, max: 0.4 },
                        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { display: false } }
                }
            });
        }

        // Card 7
        function renderCard7() {
            const sh = DATA.score_hist;
            const lowPct = ((sh[0].total / DATA.overview.time_split.test_rows) * 100).toFixed(1);
            document.getElementById('c7Headline').innerText = `${lowPct}% of test transactions score in the lowest 0.0–0.1 bucket, confining risk alerts to a sharp actionable tail.`;

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

        // Card 8
        function renderCard8() {
            const row = DATA.threshold_curve.find(t => Math.abs(t.threshold - currentStrictness) < 0.001) || DATA.threshold_curve[0];
            const alerts = row.tp + row.fp;
            const prec = (row.precision * 100).toFixed(2);
            const rec = (row.recall * 100).toFixed(2);

            if (evalMode) {
                document.getElementById('c8Headline').innerText = `At strictness ${row.threshold.toFixed(2)}: ${alerts.toLocaleString()} alerts generated; ${row.tp} frauds caught (${rec}% recall) with ${prec}% precision.`;
            } else {
                document.getElementById('c8Headline').innerText = `At strictness ${row.threshold.toFixed(2)}: ${alerts.toLocaleString()} candidate alerts routed for operational verification.`;
            }

            const matrix = document.getElementById('c8Matrix');
            matrix.innerHTML = `
                <div class="matrix-cell tp">
                    <div class="matrix-cell-header">
                        <span class="matrix-cell-title">🟢 Caught Fraud</span>
                        <span class="info-btn" onclick="openGlossaryTerm('tp')">i</span>
                    </div>
                    <div class="matrix-cell-tech">True Positives (TP)</div>
                    <div class="matrix-cell-val" style="color:var(--safe-green);">${evalMode ? row.tp.toLocaleString() : 'Masked (Turn ON Ground Truth)'}</div>
                </div>
                <div class="matrix-cell fp">
                    <div class="matrix-cell-header">
                        <span class="matrix-cell-title">🟡 False Alarms</span>
                        <span class="info-btn" onclick="openGlossaryTerm('fp')">i</span>
                    </div>
                    <div class="matrix-cell-tech">False Positives (FP)</div>
                    <div class="matrix-cell-val" style="color:var(--accent-amber);">${evalMode ? row.fp.toLocaleString() : 'Masked'}</div>
                </div>
                <div class="matrix-cell fn">
                    <div class="matrix-cell-header">
                        <span class="matrix-cell-title">🔴 Missed Fraud</span>
                        <span class="info-btn" onclick="openGlossaryTerm('fn')">i</span>
                    </div>
                    <div class="matrix-cell-tech">False Negatives (FN)</div>
                    <div class="matrix-cell-val" style="color:var(--fraud-red);">${evalMode ? row.fn.toLocaleString() : 'Masked'}</div>
                </div>
                <div class="matrix-cell tn">
                    <div class="matrix-cell-header">
                        <span class="matrix-cell-title">⚪ Clean Pass</span>
                        <span class="info-btn" onclick="openGlossaryTerm('tn')">i</span>
                    </div>
                    <div class="matrix-cell-tech">True Negatives (TN)</div>
                    <div class="matrix-cell-val" style="color:var(--honest-grey);">${evalMode ? row.tn.toLocaleString() : (DATA.overview.time_split.test_rows - alerts).toLocaleString()}</div>
                </div>
            `;
        }

        // Card 9
        function renderCard9() {
            const costData = DATA.threshold_curve.map(t => {
                const totalCost = (t.fn * 1467979) + ((t.tp + t.fp) * currentCheckingCost);
                return { threshold: t.threshold, totalCost, alerts: t.tp + t.fp };
            });

            const minRow = costData.reduce((prev, curr) => curr.totalCost < prev.totalCost ? curr : prev, costData[0]);
            document.getElementById('c9Headline').innerText = `At ${currentCheckingCost} CU checking cost: Optimal strictness is θ = ${minRow.threshold.toFixed(2)} (minimizing total operational cost to ${(minRow.totalCost / 1e6).toFixed(2)}M currency units).`;

            const ctx = document.getElementById('c9Chart').getContext('2d');
            if (chartC9) chartC9.destroy();
            chartC9 = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: costData.map(c => c.threshold.toFixed(2)),
                    datasets: [
                        { label: `Total Operational Cost (${currentCheckingCost} CU / review)`, data: costData.map(c => c.totalCost), borderColor: '#f59e0b', backgroundColor: 'rgba(245, 158, 11, 0.1)', fill: true, tension: 0.3 }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { title: { display: true, text: 'Strictness Threshold (θ)', color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                        y: { title: { display: true, text: 'Total Loss + Review Cost (CU)', color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            });
        }

        // Card 10
        function renderCard10() {
            const pol = DATA.overview.policy_alerts_test;
            document.getElementById('c10Headline').innerText = `Strict Policy (θ=0.10): ${pol.strict.alerts.toLocaleString()} alerts (${pol.strict.frauds_caught} caught) | Balanced (θ=0.50): ${pol.balanced.alerts} alerts (${pol.balanced.frauds_caught} caught) | Lenient (θ=0.90): ${pol.lenient.alerts} alerts (${pol.lenient.frauds_caught} caught).`;

            const ctx = document.getElementById('c10Chart').getContext('2d');
            if (chartC10) chartC10.destroy();
            chartC10 = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Strict (θ=0.10)', 'Balanced (θ=0.50)', 'Lenient (θ=0.90)'],
                    datasets: [
                        { label: 'Total Candidate Alerts', data: [pol.strict.alerts, pol.balanced.alerts, pol.lenient.alerts], backgroundColor: '#38bdf8' },
                        { label: 'Confirmed Frauds Caught', data: evalMode ? [pol.strict.frauds_caught, pol.balanced.frauds_caught, pol.lenient.frauds_caught] : [0, 0, 0], backgroundColor: '#10b981' }
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

        // Card 11
        function renderCard11() {
            const m = DATA.market;
            document.getElementById('c11Headline').innerText = `Following the RBI regulatory order on Jan 31 2024, Paytm shares cratered 42.1% in 3 sessions while the NIFTY 50 remained resilient.`;

            const ctx = document.getElementById('c11Chart').getContext('2d');
            if (chartC11) chartC11.destroy();
            chartC11 = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: m.map(r => r.date),
                    datasets: [
                        { label: 'Paytm Normalized (NSE Base=100)', data: m.map(r => r.paytm_normalized), borderColor: '#ef4444', backgroundColor: 'rgba(239, 68, 68, 0.1)', fill: true, tension: 0.2 },
                        { label: 'NIFTY 50 Benchmark Index (Base=100)', data: m.map(r => r.nifty_normalized), borderColor: '#38bdf8', borderDash: [4, 4], tension: 0.1 }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8', maxTicksLimit: 12 } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            });
        }

        // Card 12
        function renderCard12() {
            const edges46 = DATA.stream.network_edges.filter(e => e.step > 333);
            document.getElementById('c12Headline').innerText = `Replaying steps 334–742 with ${edges46.length} test-period correlated money laundering pairs tracked across nodes.`;

            const caseSel = document.getElementById('patrolCaseSelect');
            if (caseSel && caseSel.children.length === 0) {
                const keys = Object.keys(DATA.stream.cases);
                caseSel.innerHTML = keys.map(k => `<option value="${k}">${k} (${DATA.stream.cases[k].transaction.type}, ${DATA.stream.cases[k].transaction.amount.toLocaleString()} CU)</option>`).join('');
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
                        <strong>📁 Case Dossier: <code>${caseId}</code></strong>
                        <span class="stamp-box stamp-${ro.decision_balanced === 'block' ? 'block' : (ro.decision_balanced === 'escalate' ? 'escalate' : 'allow')}">${ro.decision_balanced.toUpperCase()}</span>
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
            if (cityInitialized) updateCityForStep(patrolCurrentStep);
        }

        function startPatrolLoop() {
            clearInterval(patrolInterval);
            patrolInterval = setInterval(() => {
                if (patrolCurrentStep >= 742) patrolCurrentStep = 334;
                else patrolCurrentStep++;
                document.getElementById('patrolScrubber').value = patrolCurrentStep;
                renderPatrolStep(patrolCurrentStep);
                if (cityInitialized) updateCityForStep(patrolCurrentStep);
            }, patrolSpeed);
        }

        function renderPatrolStep(step) {
            const hour = step % 24;
            document.getElementById('patrolStepDisplay').innerText = `Step: ${step} (Hour ${hour})`;
            const cityClock = document.getElementById('cityStepClock');
            if (cityClock) cityClock.innerText = `Step ${step} | Hour ${hour}:00`;

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

        // =========================================================================
        // MISSION 9b - HIGH DEFINITION REALISTIC 3D LEDGER CITY (SENTINEL MODE)
        // =========================================================================
        function openSentinelCity() {
            const modal = document.getElementById('cityModal');
            modal.classList.add('active');
            
            setTimeout(() => {
                const container = document.getElementById('cityCanvasContainer');
                if (!cityInitialized) {
                    init3DLedgerCity();
                    cityInitialized = true;
                } else if (cityRenderer) {
                    const w = container.clientWidth || window.innerWidth;
                    const h = container.clientHeight || (window.innerHeight - 90);
                    cityRenderer.setSize(w, h);
                    cityCamera.aspect = w / h;
                    cityCamera.updateProjectionMatrix();
                }
                updateCityForStep(patrolCurrentStep);
                if (!cityAnimId) animate3DCity();
            }, 60);
        }

        function closeSentinelCity() {
            document.getElementById('cityModal').classList.remove('active');
            if (cityAnimId) {
                cancelAnimationFrame(cityAnimId);
                cityAnimId = null;
            }
        }

        function closeEvidenceBoard() {
            document.getElementById('cityEvidenceBoard').style.display = 'none';
            if (routeLaserLine) {
                cityScene.remove(routeLaserLine);
                routeLaserLine = null;
            }
        }

        function init3DLedgerCity() {
            const container = document.getElementById('cityCanvasContainer');
            const width = container.clientWidth || window.innerWidth || 900;
            const height = container.clientHeight || (window.innerHeight - 90) || 600;

            if (!window.WebGLRenderingContext) {
                init2DCityFallback(container);
                return;
            }

            try {
                cityScene = new THREE.Scene();
                cityScene.background = new THREE.Color(0x020716);
                cityScene.fog = new THREE.FogExp2(0x020716, 0.0010);

                cityCamera = new THREE.PerspectiveCamera(45, width / height, 2, 4000);
                cityCamera.position.copy(targetCamPos);
                cityCamera.lookAt(targetLookTarget);

                cityRenderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
                cityRenderer.setSize(width, height);
                cityRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
                cityRenderer.shadowMap.enabled = true;
                container.appendChild(cityRenderer.domElement);

                cityRaycaster = new THREE.Raycaster();
                cityMouse = new THREE.Vector2();
            } catch (e) {
                console.warn("WebGL initialization failed, falling back to 2D Canvas:", e);
                init2DCityFallback(container);
                return;
            }

            // High-Definition Lighting
            const hemiLight = new THREE.HemisphereLight(0x7dd3fc, 0x0f172a, 1.4);
            cityScene.add(hemiLight);

            const sunLight = new THREE.DirectionalLight(0xe0f2fe, 1.8);
            sunLight.position.set(350, 700, 350);
            cityScene.add(sunLight);

            const ambientLight = new THREE.AmbientLight(0x1e293b, 1.6);
            cityScene.add(ambientLight);

            // Ground Asphalt Base & Grid Lines
            const groundGeo = new THREE.PlaneGeometry(1600, 1600);
            const groundMat = new THREE.MeshLambertMaterial({ color: 0x080f24 });
            const ground = new THREE.Mesh(groundGeo, groundMat);
            ground.rotation.x = -Math.PI / 2;
            ground.position.y = -0.2;
            cityScene.add(ground);

            const gridHelper = new THREE.GridHelper(1200, 48, 0x1e3a5f, 0x0c1a30);
            gridHelper.position.y = 0.1;
            cityScene.add(gridHelper);

            // Road Network & Boulevards
            buildRoadAvenues();

            // Central Sentinel Spire (Height 200 CU)
            buildCentralSentinelTower();

            // 8 Urban Districts with Realistic Skyscraper Geometries
            build8UrbanDistricts();

            // The Sentinel Character Model
            buildSentinelPatrolCharacter();

            // Humanoids Mesh Pool (300 Max)
            buildCityPeoplePool();

            // Setup Orbit & Interaction Listeners
            setupCityOrbitControls(container);

            document.addEventListener("visibilitychange", () => {
                if (document.hidden && cityAnimId) {
                    cancelAnimationFrame(cityAnimId);
                    cityAnimId = null;
                } else if (!document.hidden && document.getElementById('cityModal').classList.contains('active')) {
                    animate3DCity();
                }
            });

            window.addEventListener('resize', () => {
                if (cityRenderer && document.getElementById('cityModal').classList.contains('active')) {
                    const w = container.clientWidth || window.innerWidth;
                    const h = container.clientHeight || (window.innerHeight - 90);
                    cityCamera.aspect = w / h;
                    cityCamera.updateProjectionMatrix();
                    cityRenderer.setSize(w, h);
                }
            });
        }

        function buildRoadAvenues() {
            const roadMat = new THREE.MeshLambertMaterial({ color: 0x0b1633 });
            const lineMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });

            // Cross Highways
            const hRoad = new THREE.Mesh(new THREE.PlaneGeometry(800, 40), roadMat);
            hRoad.rotation.x = -Math.PI / 2;
            hRoad.position.y = 0.2;
            cityScene.add(hRoad);

            const vRoad = new THREE.Mesh(new THREE.PlaneGeometry(40, 800), roadMat);
            vRoad.rotation.x = -Math.PI / 2;
            vRoad.position.y = 0.2;
            cityScene.add(vRoad);

            // Glowing Centerlines
            const dashH = new THREE.Mesh(new THREE.PlaneGeometry(780, 1.8), lineMat);
            dashH.rotation.x = -Math.PI / 2;
            dashH.position.y = 0.3;
            cityScene.add(dashH);

            const dashV = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 780), lineMat);
            dashV.rotation.x = -Math.PI / 2;
            dashV.position.y = 0.3;
            cityScene.add(dashV);
        }

        function buildCentralSentinelTower() {
            const towerGroup = new THREE.Group();

            const baseGeo = new THREE.CylinderGeometry(24, 32, 70, 8);
            const towerMat = new THREE.MeshPhongMaterial({
                color: 0x0c1a36,
                emissive: 0x0284c7,
                emissiveIntensity: 0.3,
                specular: 0x38bdf8,
                shininess: 90
            });
            const base = new THREE.Mesh(baseGeo, towerMat);
            base.position.y = 35;
            towerGroup.add(base);

            const midGeo = new THREE.CylinderGeometry(16, 24, 80, 8);
            const mid = new THREE.Mesh(midGeo, towerMat);
            mid.position.y = 110;
            towerGroup.add(mid);

            const deckGeo = new THREE.CylinderGeometry(28, 14, 18, 16);
            const deckMat = new THREE.MeshPhongMaterial({ color: 0x0284c7, emissive: 0x38bdf8, emissiveIntensity: 0.6 });
            const deck = new THREE.Mesh(deckGeo, deckMat);
            deck.position.y = 159;
            towerGroup.add(deck);

            const spireGeo = new THREE.ConeGeometry(6, 50, 8);
            const spireMat = new THREE.MeshBasicMaterial({ color: 0xf59e0b });
            const spire = new THREE.Mesh(spireGeo, spireMat);
            spire.position.y = 190;
            towerGroup.add(spire);

            const eyeGeo = new THREE.SphereGeometry(8, 16, 16);
            const eyeMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
            const eye = new THREE.Mesh(eyeGeo, eyeMat);
            eye.position.y = 170;
            towerGroup.add(eye);

            const labelSprite = createDistrictLabelSprite("SENTINEL HQ // AI CORE", "🗼 CENTRAL COMMAND", "#38bdf8");
            labelSprite.position.set(0, 235, 0);
            labelSprite.scale.set(120, 36, 1);
            labelSprite.material.depthTest = false;
            labelSprite.material.depthWrite = false;
            labelSprite.renderOrder = 9999;
            towerGroup.add(labelSprite);

            cityScene.add(towerGroup);
        }

        function build8UrbanDistricts() {
            cityBuildings = [];
            districtSprites = {};
            const districtColors = [0x38bdf8, 0x3b82f6, 0x818cf8, 0xa855f7, 0xf59e0b, 0x10b981, 0x06b6d4, 0x94a3b8];

            for (let d = 1; d <= 8; d++) {
                const pos = DISTRICT_POSITIONS[d];
                const dColor = districtColors[d - 1];

                const plazaGeo = new THREE.BoxGeometry(130, 2, 130);
                const plazaMat = new THREE.MeshPhongMaterial({
                    color: 0x0a142c,
                    emissive: dColor,
                    emissiveIntensity: 0.22
                });
                const plaza = new THREE.Mesh(plazaGeo, plazaMat);
                plaza.position.set(pos.x, 1, pos.z);
                cityScene.add(plaza);

                // High-Altitude Sky Billboard (Always on top with depthTest: false)
                const labelSprite = createDistrictLabelSprite(`DISTRICT ${d}: ${pos.name.toUpperCase()}`, "🟢 SECURE", "#38bdf8");
                labelSprite.position.set(pos.x, 185, pos.z);
                labelSprite.scale.set(110, 32, 1);
                labelSprite.material.depthTest = false;
                labelSprite.material.depthWrite = false;
                labelSprite.renderOrder = 9999;
                cityScene.add(labelSprite);
                districtSprites[d] = labelSprite;

                // Street-Level Entrance Marker Banner
                const entranceSprite = createDistrictLabelSprite(`D${d}: ${pos.name.toUpperCase()}`, "PORTAL", "#38bdf8");
                entranceSprite.position.set(pos.x, 10, pos.z);
                entranceSprite.scale.set(40, 12, 1);
                cityScene.add(entranceSprite);

                for (let b = 0; b < 12; b++) {
                    const bx = pos.x + (Math.random() - 0.5) * 100;
                    const bz = pos.z + (Math.random() - 0.5) * 100;
                    const bw = 16 + Math.random() * 16;
                    const bd = 16 + Math.random() * 16;
                    const bh = 35 + Math.random() * 95;

                    const bGeo = new THREE.BoxGeometry(bw, bh, bd);
                    const bMat = new THREE.MeshPhongMaterial({
                        color: 0x0b152d,
                        emissive: 0x111c3a,
                        emissiveIntensity: 0.25,
                        specular: 0x38bdf8,
                        shininess: 40
                    });

                    const bMesh = new THREE.Mesh(bGeo, bMat);
                    bMesh.position.set(bx, bh / 2, bz);
                    cityScene.add(bMesh);

                    const winGeo = new THREE.PlaneGeometry(bw * 0.85, bh * 0.75);
                    const winMat = new THREE.MeshBasicMaterial({
                        color: 0x38bdf8,
                        transparent: true,
                        opacity: 0.75
                    });
                    const winF = new THREE.Mesh(winGeo, winMat);
                    winF.position.set(bx, bh / 2, bz + bd / 2 + 0.3);
                    cityScene.add(winF);

                    const beaconGeo = new THREE.SphereGeometry(1.8, 8, 8);
                    const beaconMat = new THREE.MeshBasicMaterial({ color: 0xef4444 });
                    const beacon = new THREE.Mesh(beaconGeo, beaconMat);
                    beacon.position.set(bx, bh + 3, bz);
                    cityScene.add(beacon);

                    cityBuildings.push({
                        mesh: bMesh,
                        window: winF,
                        beacon,
                        district: d,
                        baseHeight: bh,
                        x: bx, z: bz
                    });
                }
            }
        }

        function buildSentinelPatrolCharacter() {
            const group = new THREE.Group();

            const armorGeo = new THREE.CylinderGeometry(2.5, 3.2, 10, 8);
            const armorMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.3, metalness: 0.8 });
            const body = new THREE.Mesh(armorGeo, armorMat);
            body.position.y = 5;
            group.add(body);

            const hoodGeo = new THREE.SphereGeometry(3.0, 16, 16);
            const hoodMat = new THREE.MeshStandardMaterial({ color: 0x080e1a, roughness: 0.4 });
            const hood = new THREE.Mesh(hoodGeo, hoodMat);
            hood.position.y = 12;
            group.add(hood);

            const emblemGeo = new THREE.CircleGeometry(1.6, 16);
            const emblemMat = new THREE.MeshBasicMaterial({ color: 0xf59e0b });
            const emblem = new THREE.Mesh(emblemGeo, emblemMat);
            emblem.position.set(0, 7.5, 2.7);
            group.add(emblem);

            const cloakGeo = new THREE.ConeGeometry(4.0, 11, 8, 1, true);
            const cloakMat = new THREE.MeshLambertMaterial({ color: 0x0284c7, side: THREE.DoubleSide });
            const cloak = new THREE.Mesh(cloakGeo, cloakMat);
            cloak.position.set(0, 4.5, -1.2);
            group.add(cloak);

            group.position.set(0, 0, 0);
            cityScene.add(group);

            sentinelMesh = {
                group,
                targetPos: new THREE.Vector3(0, 0, 0),
                currentPos: new THREE.Vector3(0, 0, 0)
            };
        }

        function createDistrictLabelSprite(title, status, colorHex) {
            const canvas = document.createElement('canvas');
            canvas.width = 512;
            canvas.height = 140;
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = "rgba(10, 18, 36, 0.95)";
            ctx.strokeStyle = colorHex;
            ctx.lineWidth = 4;
            ctx.roundRect(6, 6, 500, 128, 16);
            ctx.fill();
            ctx.stroke();

            ctx.fillStyle = colorHex;
            ctx.font = "bold 30px sans-serif";
            ctx.textAlign = "center";
            ctx.fillText(title, 256, 56);

            ctx.fillStyle = status.includes("ALARM") ? "#f87171" : "#34d399";
            ctx.font = "bold 24px monospace";
            ctx.fillText(status, 256, 104);

            const texture = new THREE.CanvasTexture(canvas);
            const spriteMat = new THREE.SpriteMaterial({ map: texture, transparent: true, depthTest: false, depthWrite: false });
            const sprite = new THREE.Sprite(spriteMat);
            sprite.scale.set(110, 32, 1);
            sprite.renderOrder = 9999;
            sprite.userData = { canvas, ctx, texture };
            return sprite;
        }

        function updateDistrictLabelSprite(sprite, title, status, colorHex) {
            if (!sprite || !sprite.userData || !sprite.userData.ctx) return;
            const { canvas, ctx, texture } = sprite.userData;
            ctx.clearRect(0, 0, 512, 140);
            ctx.fillStyle = "rgba(10, 18, 36, 0.95)";
            ctx.strokeStyle = colorHex;
            ctx.lineWidth = 4;
            ctx.roundRect(6, 6, 500, 128, 16);
            ctx.fill();
            ctx.stroke();

            ctx.fillStyle = colorHex;
            ctx.font = "bold 30px sans-serif";
            ctx.textAlign = "center";
            ctx.fillText(title, 256, 56);

            ctx.fillStyle = status.includes("ALARM") ? "#f87171" : "#34d399";
            ctx.font = "bold 24px monospace";
            ctx.fillText(status, 256, 104);

            texture.needsUpdate = true;
        }

        function createPedestrianTagCanvas() {
            const canvas = document.createElement('canvas');
            canvas.width = 256;
            canvas.height = 64;
            const texture = new THREE.CanvasTexture(canvas);
            const spriteMat = new THREE.SpriteMaterial({ map: texture, transparent: true });
            const sprite = new THREE.Sprite(spriteMat);
            sprite.scale.set(22, 5.5, 1);
            sprite.position.y = 15;
            return { canvas, texture, sprite };
        }

        function renderPedestrianTag(tagObj, text, isAlert, isElevated) {
            const { canvas, texture, sprite } = tagObj;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, 256, 64);

            let bg = isAlert ? "rgba(220, 38, 38, 0.92)" : (isElevated ? "rgba(217, 119, 6, 0.88)" : "rgba(15, 23, 42, 0.82)");
            let border = isAlert ? "#fca5a5" : (isElevated ? "#fde68a" : "#38bdf8");
            let textCol = "#ffffff";

            ctx.fillStyle = bg;
            ctx.strokeStyle = border;
            ctx.lineWidth = 2.5;
            ctx.roundRect(4, 4, 248, 56, 10);
            ctx.fill();
            ctx.stroke();

            ctx.fillStyle = textCol;
            ctx.font = isAlert ? "bold 17px monospace" : "bold 15px sans-serif";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(text, 128, 32);

            texture.needsUpdate = true;
            sprite.visible = true;
        }

        function buildCityPeoplePool() {
            cityPeopleMeshes = [];
            const bodyGeo = new THREE.CylinderGeometry(1.6, 2.2, 7.5, 8);
            const headGeo = new THREE.SphereGeometry(1.8, 8, 8);
            const bagGeo = new THREE.BoxGeometry(2.8, 2.8, 2.8);
            const haloGeo = new THREE.TorusGeometry(3.4, 0.4, 6, 16);
            const beamGeo = new THREE.CylinderGeometry(0.3, 0.3, 50, 8);
            const ringGeo = new THREE.RingGeometry(3.5, 5.0, 16);

            for (let i = 0; i < 300; i++) {
                const group = new THREE.Group();
                const coatMat = new THREE.MeshLambertMaterial({ color: 0x38bdf8 });
                const headMat = new THREE.MeshLambertMaterial({ color: 0xf8fafc });
                const bagMat = new THREE.MeshLambertMaterial({ color: 0xf59e0b });
                const haloMat = new THREE.MeshBasicMaterial({ color: 0xf59e0b, transparent: true, opacity: 0.9 });
                const beamMat = new THREE.MeshBasicMaterial({ color: 0xef4444, transparent: true, opacity: 0.8 });
                const ringMat = new THREE.MeshBasicMaterial({ color: 0xef4444, transparent: true, opacity: 0.7, side: THREE.DoubleSide });

                const body = new THREE.Mesh(bodyGeo, coatMat);
                body.position.y = 3.75;
                group.add(body);

                const head = new THREE.Mesh(headGeo, headMat);
                head.position.y = 9.0;
                group.add(head);

                const bag = new THREE.Mesh(bagGeo, bagMat);
                bag.position.set(3.0, 3.2, 0);
                group.add(bag);

                const halo = new THREE.Mesh(haloGeo, haloMat);
                halo.rotation.x = Math.PI / 2;
                halo.position.y = 12.0;
                halo.visible = false;
                group.add(halo);

                const beam = new THREE.Mesh(beamGeo, beamMat);
                beam.position.y = 34;
                beam.visible = false;
                group.add(beam);

                const ring = new THREE.Mesh(ringGeo, ringMat);
                ring.rotation.x = -Math.PI / 2;
                ring.position.y = 0.2;
                ring.visible = false;
                group.add(ring);

                const tagObj = createPedestrianTagCanvas();
                group.add(tagObj.sprite);

                group.position.set(0, -100, 0);
                group.userData = { index: i, personData: null };
                cityScene.add(group);

                cityPeopleMeshes.push({
                    group, body, head, bag, halo, beam, ring, tagObj,
                    coatMat, headMat, bagMat, haloMat, beamMat, ringMat,
                    active: false,
                    waypoints: [],
                    progress: 0,
                    speed: 0.005,
                    txData: null
                });
            }
        }

        function setupCityOrbitControls(container) {
            container.addEventListener('mousedown', (e) => {
                if (e.button === 0) isOrbiting = true;
                else if (e.button === 2) isPanning = true;
                mousePrevX = e.clientX;
                mousePrevY = e.clientY;
            });

            window.addEventListener('mouseup', () => {
                isOrbiting = false;
                isPanning = false;
            });

            container.addEventListener('contextmenu', (e) => e.preventDefault());

            container.addEventListener('mousemove', (e) => {
                if (!isOrbiting && !isPanning) return;
                const dx = e.clientX - mousePrevX;
                const dy = e.clientY - mousePrevY;

                if (isOrbiting) {
                    const radius = targetCamPos.distanceTo(targetLookTarget);
                    const theta = Math.atan2(targetCamPos.x - targetLookTarget.x, targetCamPos.z - targetLookTarget.z) - dx * 0.005;
                    const phi = Math.max(0.12, Math.min(Math.PI / 2 - 0.05, Math.acos((targetCamPos.y - targetLookTarget.y) / Math.max(1, radius)) - dy * 0.005));

                    targetCamPos.x = targetLookTarget.x + radius * Math.sin(phi) * Math.sin(theta);
                    targetCamPos.y = targetLookTarget.y + radius * Math.cos(phi);
                    targetCamPos.z = targetLookTarget.z + radius * Math.sin(phi) * Math.cos(theta);
                } else if (isPanning) {
                    targetLookTarget.x -= dx * 0.35;
                    targetLookTarget.z -= dy * 0.35;
                    targetCamPos.x -= dx * 0.35;
                    targetCamPos.z -= dy * 0.35;
                }

                mousePrevX = e.clientX;
                mousePrevY = e.clientY;
            });

            container.addEventListener('wheel', (e) => {
                e.preventDefault();
                const dir = targetCamPos.clone().sub(targetLookTarget).normalize();
                const dist = Math.max(25, Math.min(800, targetCamPos.distanceTo(targetLookTarget) + e.deltaY * 0.4));
                targetCamPos.copy(targetLookTarget).add(dir.multiplyScalar(dist));
            }, { passive: false });

            // Raycast click
            container.addEventListener('click', (e) => {
                const rect = container.getBoundingClientRect();
                cityMouse.x = ((e.clientX - rect.left) / container.clientWidth) * 2 - 1;
                cityMouse.y = -((e.clientY - rect.top) / container.clientHeight) * 2 + 1;

                cityRaycaster.setFromCamera(cityMouse, cityCamera);
                const intersects = cityRaycaster.intersectObjects(cityScene.children, true);

                if (intersects.length > 0) {
                    let parent = intersects[0].object;
                    while (parent && !parent.userData.personData && parent.parent) {
                        parent = parent.parent;
                    }
                    if (parent && parent.userData.personData) {
                        displayEvidenceBoard(parent.userData.personData);
                    }
                }
            });
        }

        function displayEvidenceBoard(pData) {
            selectedPersonData = pData;
            const board = document.getElementById('cityEvidenceBoard');
            const title = document.getElementById('ebTxId');
            const body = document.getElementById('ebTxBody');

            title.innerText = `🔍 Transaction ${pData.id}`;
            const isFlagged = pData.sc >= currentStrictness;
            const statusBadge = isFlagged ? `<span class="stamp-box stamp-block">🚨 RISK ALARM (SCORE ≥ θ)</span>` : `<span class="stamp-box stamp-allow">✅ APPROVED PAYMENT</span>`;

            const amtRisk = pData.amt > 500000 ? `🔥 <strong>High Value Alert:</strong> ${pData.amt.toLocaleString()} CU (Top ${((1 - pData.pct)*100).toFixed(1)}% of transfers)` : `⚪ Normal Value: ${pData.amt.toLocaleString()} CU`;
            const timeRisk = (pData.hr >= 0 && pData.hr <= 5) ? `🌙 <strong>Nocturnal Velocity:</strong> ${pData.hr}:00 (Late Night Attack Window)` : `☀️ Standard Hours: ${pData.hr}:00`;
            const typeRisk = pData.t === 'TRANSFER' ? `💳 <strong>Primary Attack Channel:</strong> TRANSFER (100% of PaySim theft)` : `🏧 <strong>Cash-Out Channel:</strong> Liquidation point`;

            let decisionAction = isFlagged ? "🚨 RISK OFFICER DECISION: BLOCK TRANSACTION & FREEZE ORIGIN WALLET" : "✅ RISK OFFICER DECISION: IMMEDIATE CLEARANCE";
            if (evalMode && pData.f === 1) decisionAction += "<br><span style='color:#ef4444; font-weight:bold;'>[AUDIT: CONFIRMED REAL THEFT]</span>";

            body.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span>Step ${pData.step} (${pData.hr}:00)</span>
                    ${statusBadge}
                </div>
                
                <div style="background:#091024; border:1px solid var(--border-color); border-radius:8px; padding:10px 12px; font-size:11.5px; display:flex; flex-direction:column; gap:5px;">
                    <strong style="color:#38bdf8; font-size:12px;">📊 Forensic Risk Indicators:</strong>
                    <div>• ${amtRisk}</div>
                    <div>• ${timeRisk}</div>
                    <div>• ${typeRisk}</div>
                    <div>• <strong>Route:</strong> District ${pData.df} (${DISTRICT_POSITIONS[pData.df].name}) ➔ District ${pData.dt} (${DISTRICT_POSITIONS[pData.dt].name})</div>
                    <div>• <strong>AI Risk Score:</strong> <strong style="color:${isFlagged ? '#ef4444' : '#10b981'}; font-size:13px;">${pData.sc.toFixed(4)}</strong> (Strictness Cutoff: ${currentStrictness.toFixed(2)})</div>
                </div>

                <div style="background:#0c1733; border-left:3px solid ${isFlagged ? '#ef4444' : '#10b981'}; padding:8px 10px; border-radius:4px; font-size:11.5px; margin-top:4px;">
                    ${decisionAction}
                </div>

                <div style="margin-top:8px; display:flex; gap:8px;">
                    <button class="btn btn-primary" style="flex:1; justify-content:center;" onclick="viewFullDossierInDrawer('${pData.id}')">📂 Full Case Dossier</button>
                    <button class="btn btn-secondary" onclick="closeEvidenceBoard()">Close</button>
                </div>
            `;
            board.style.display = 'block';

            // Draw road laser line
            drawRouteLaser(pData.df, pData.dt);

            // Sentinel flies to suspect
            if (sentinelMesh) {
                const targetMesh = cityPeopleMeshes.find(m => m.txData && m.txData.id === pData.id);
                if (targetMesh) {
                    sentinelMesh.targetPos.copy(targetMesh.group.position);
                }
            }
        }

        function drawRouteLaser(fromD, toD) {
            if (routeLaserLine) {
                cityScene.remove(routeLaserLine);
                routeLaserLine = null;
            }

            const p1 = DISTRICT_POSITIONS[fromD] || DISTRICT_POSITIONS[1];
            const p2 = DISTRICT_POSITIONS[toD] || DISTRICT_POSITIONS[2];

            const points = [
                new THREE.Vector3(p1.x, 2, p1.z),
                new THREE.Vector3(p1.x, 2, 0),
                new THREE.Vector3(p2.x, 2, 0),
                new THREE.Vector3(p2.x, 2, p2.z)
            ];

            const curve = new THREE.CatmullRomCurve3(points);
            const tubeGeo = new THREE.TubeGeometry(curve, 20, 1.4, 8, false);
            const tubeMat = new THREE.MeshBasicMaterial({ color: 0xef4444, transparent: true, opacity: 0.85 });
            routeLaserLine = new THREE.Mesh(tubeGeo, tubeMat);
            cityScene.add(routeLaserLine);
        }

        function viewFullDossierInDrawer(txId) {
            closeSentinelCity();
            goToStep(6);
            const caseSel = document.getElementById('patrolCaseSelect');
            if (caseSel) {
                caseSel.value = txId;
                renderCaseDossier(txId);
            }
        }

        function init2DCityFallback(container) {
            cityIs2DFallback = true;
            const canvas = document.getElementById('cityFallback2D');
            canvas.style.display = 'block';
            const ctx = canvas.getContext('2d');
            canvas.width = container.clientWidth || 800;
            canvas.height = container.clientHeight || 500;
            ctx.fillStyle = '#050811';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#38bdf8';
            ctx.font = '14px sans-serif';
            ctx.fillText('2D Radar Mode Active (WebGL Hardware Acceleration Unavailable)', 30, 40);
        }

        function setCityView(type) {
            if (type === 'birdseye') {
                targetLookTarget.set(0, 0, 0);
                targetCamPos.set(0, 360, 280);
            } else if (type === 'overhead') {
                targetLookTarget.set(0, 0, 0);
                targetCamPos.set(0, 540, 20);
            } else if (type === 'skyline') {
                targetLookTarget.set(0, 15, 0);
                targetCamPos.set(240, 200, 320);
            } else if (type === 'street') {
                targetLookTarget.set(0, 8, -60);
                targetCamPos.set(0, 12, 170);
            } else if (type === 'tower') {
                targetLookTarget.set(0, 10, 180);
                targetCamPos.set(0, 170, 0);
            }
        }

        function focusOnNextThreat() {
            const flagged = cityPeopleMeshes.find(p => p.active && p.txData && p.txData.sc >= currentStrictness);
            if (flagged) {
                inspectThreatById(flagged.txData.id);
            }
        }

        function inspectThreatById(txId) {
            const targetMesh = cityPeopleMeshes.find(m => m.txData && m.txData.id === txId);
            if (targetMesh && targetMesh.txData) {
                targetLookTarget.copy(targetMesh.group.position).add(new THREE.Vector3(0, 6, 0));
                targetCamPos.copy(targetMesh.group.position).add(new THREE.Vector3(0, 18, 36));
                displayEvidenceBoard(targetMesh.txData);
            }
        }

        function cityStepChange(delta) {
            patrolCurrentStep = Math.max(334, Math.min(742, patrolCurrentStep + delta));
            scrubPatrol(patrolCurrentStep);
        }

        function updateCityForStep(step) {
            if (!DATA.district_hourly_by_step || !DATA.city_people_by_step) return;

            const hour = step % 24;
            const hourText = `${hour}:00 (${(hour>=0 && hour<=5)?'🌙 Late Night Window':'☀️ Standard Hours'})`;

            // Sync Header & HUD Clock
            const clockBadge = document.getElementById('cityStepClock');
            if (clockBadge) clockBadge.innerText = `Step ${step} | ${hour}:00`;
            const stepSlider = document.getElementById('cityStepSlider');
            if (stepSlider) stepSlider.value = step;
            const strictBadge = document.getElementById('cityStrictnessBadge');
            if (strictBadge) strictBadge.innerText = currentStrictness.toFixed(2);
            const strictDisp = document.getElementById('cityStrictnessDisplay');
            if (strictDisp) strictDisp.innerText = currentStrictness.toFixed(2);

            // 1. Update District Buildings & Floating Hologram Status Signs
            const stepDistData = DATA.district_hourly_by_step[step] || {};

            cityBuildings.forEach(b => {
                const info = stepDistData[b.district] || { p: 10, s: 0 };
                const heightMult = 0.7 + Math.min(2.0, (info.p / 25.0));
                b.mesh.scale.y = heightMult;
                b.mesh.position.y = (b.baseHeight * heightMult) / 2;

                if (info.s > 0) {
                    b.window.material.color.setHex(0xf59e0b);
                    b.window.material.opacity = 0.9;
                } else {
                    b.window.material.color.setHex(0x38bdf8);
                    b.window.material.opacity = 0.55;
                }
            });

            for (let d = 1; d <= 8; d++) {
                const info = stepDistData[d] || { p: 0, s: 0 };
                const sprite = districtSprites[d];
                if (sprite) {
                    const statusText = info.s > 0 ? `🔴 ALARM (${info.s} THREATS)` : `🟢 ${info.p} TX/HR`;
                    const colorHex = info.s > 0 ? "#ef4444" : "#38bdf8";
                    updateDistrictLabelSprite(sprite, `DISTRICT ${d}: ${DISTRICT_POSITIONS[d].name.toUpperCase()}`, statusText, colorHex);
                }
            }

            // 2. Update Live Hourly Threat Radar Panel
            const activeStepPeople = DATA.city_people_by_step[step] || [];
            const flaggedThreats = activeStepPeople.filter(p => p.sc >= currentStrictness);
            const elevatedThreats = activeStepPeople.filter(p => p.sc >= 0.15 && p.sc < currentStrictness);

            document.getElementById('radarHourDisplay').innerText = hourText;
            document.getElementById('radarActiveTxCount').innerText = activeStepPeople.length;
            document.getElementById('radarThreatCountBadge').innerText = `${flaggedThreats.length} Threats`;

            // Dynamic Narrative Briefing Description
            const briefingEl = document.getElementById('cityBriefingText');
            if (briefingEl) {
                const totalAmt = activeStepPeople.reduce((sum, p) => sum + p.amt, 0);
                const flaggedAmt = flaggedThreats.reduce((sum, p) => sum + p.amt, 0);
                const kTotal = (totalAmt >= 1000000) ? (totalAmt / 1000000).toFixed(1) + 'M CU' : (totalAmt / 1000).toFixed(0) + 'K CU';
                const kFlagged = (flaggedAmt >= 1000000) ? (flaggedAmt / 1000000).toFixed(1) + 'M CU' : (flaggedAmt / 1000).toFixed(0) + 'K CU';

                if (flaggedThreats.length > 0) {
                    const topThreat = flaggedThreats[0];
                    briefingEl.innerHTML = `<strong>Step ${step} (${hour}:00)</strong>: Replaying ${activeStepPeople.length} live transactions (${kTotal} volume) across 8 account districts. <span style="color:#f87171; font-weight:700;">🚨 Sentinel AI flagged ${flaggedThreats.length} high-risk threat(s) (${kFlagged} stolen)</span> moving from Dist ${topThreat.df} (${DISTRICT_POSITIONS[topThreat.df].name}) ➔ Dist ${topThreat.dt} (${DISTRICT_POSITIONS[topThreat.dt].name}) with AI score ${topThreat.sc.toFixed(2)}. Red beams show frozen funds.`;
                } else if (elevatedThreats.length > 0) {
                    briefingEl.innerHTML = `<strong>Step ${step} (${hour}:00)</strong>: Replaying ${activeStepPeople.length} transactions (${kTotal} volume). <span style="color:#f59e0b; font-weight:600;">⚠️ ${elevatedThreats.length} elevated transactions under observation</span> below alarm strictness (θ = ${currentStrictness.toFixed(2)}).`;
                } else {
                    briefingEl.innerHTML = `<strong>Step ${step} (${hour}:00)</strong>: Replaying ${activeStepPeople.length} transactions (${kTotal} volume) across 8 account districts. <span style="color:#34d399; font-weight:600;">🟢 All payment traffic normal.</span> No high-risk anomalies detected in this hour.`;
                }
            }

            const radarList = document.getElementById('radarThreatList');
            if (flaggedThreats.length === 0 && elevatedThreats.length === 0) {
                radarList.innerHTML = `<div style="color:#64748b; font-size:11px; padding:6px;">No high-risk threats detected in this hour. All traffic normal.</div>`;
            } else {
                let threatHTML = flaggedThreats.map((p, idx) => `
                    <div class="threat-incident-card" onclick="inspectThreatById('${p.id}')">
                        <div style="display:flex; justify-content:space-between; font-weight:700; color:#f87171; font-size:11.5px;">
                            <span>🚨 Threat #${idx+1} (${p.t})</span>
                            <span style="font-family:var(--font-mono); color:#f59e0b;">Score: ${p.sc.toFixed(2)}</span>
                        </div>
                        <div style="font-size:11px; color:#cbd5e1; margin-top:2px;">
                            ${p.amt.toLocaleString()} CU • Dist ${p.df} ➔ Dist ${p.dt}
                        </div>
                    </div>
                `).join('');

                if (elevatedThreats.length > 0) {
                    threatHTML += elevatedThreats.slice(0, 3).map((p, idx) => `
                        <div class="threat-incident-card elevated" onclick="inspectThreatById('${p.id}')">
                            <div style="display:flex; justify-content:space-between; font-weight:700; color:#f59e0b; font-size:11px;">
                                <span>⚠️ Watch #${idx+1} (${p.t})</span>
                                <span style="font-family:var(--font-mono); color:#facc15;">Score: ${p.sc.toFixed(2)}</span>
                            </div>
                            <div style="font-size:10.5px; color:#94a3b8; margin-top:1px;">
                                ${p.amt.toLocaleString()} CU • Dist ${p.df} ➔ Dist ${p.dt}
                            </div>
                        </div>
                    `).join('');
                }

                radarList.innerHTML = threatHTML;
            }

            // 3. Spawn / Update People on screen with Floating Badges & Multi-Tier Visual Classification
            const spawnCount = Math.min(300, activeStepPeople.length);
            let firstFlaggedPos = null;

            for (let i = 0; i < 300; i++) {
                const pMesh = cityPeopleMeshes[i];
                if (!pMesh) continue;

                if (i < spawnCount) {
                    const pData = activeStepPeople[i];
                    pMesh.active = true;
                    pMesh.txData = pData;
                    pMesh.group.userData.personData = pData;

                    const fromPos = DISTRICT_POSITIONS[pData.df] || DISTRICT_POSITIONS[1];
                    const toPos = DISTRICT_POSITIONS[pData.dt] || DISTRICT_POSITIONS[2];

                    pMesh.waypoints = [
                        new THREE.Vector3(fromPos.x, 0, fromPos.z),
                        new THREE.Vector3(fromPos.x, 0, 0),
                        new THREE.Vector3(0, 0, 0),
                        new THREE.Vector3(toPos.x, 0, 0),
                        new THREE.Vector3(toPos.x, 0, toPos.z)
                    ];
                    pMesh.progress = (i * 0.17) % 1.0;

                    // Coat color: Cyan (Transfer) vs Violet (Cash-out)
                    if (pData.t === 'TRANSFER') {
                        pMesh.coatMat.color.setHex(0x38bdf8);
                    } else {
                        pMesh.coatMat.color.setHex(0xc084fc);
                    }

                    // Bag size based on percentile
                    const bagScale = 0.6 + (pData.pct * 1.8);
                    pMesh.bag.scale.set(bagScale, bagScale, bagScale);

                    const isFlagged = pData.sc >= currentStrictness;
                    const isElevated = pData.sc >= 0.15;
                    const kAmt = (pData.amt >= 1000000) ? (pData.amt / 1000000).toFixed(1) + 'M' : (pData.amt / 1000).toFixed(0) + 'K';

                    // Floating 3D Overhead Text Badges & Risk Lighting:
                    if (evalMode && pData.f === 1) {
                        renderPedestrianTag(pMesh.tagObj, `🚨 THEFT: ${kAmt} CU (${pData.sc.toFixed(2)})`, true, false);
                        pMesh.headMat.color.setHex(0xef4444);
                        pMesh.halo.visible = true;
                        pMesh.haloMat.color.setHex(0xef4444);
                        pMesh.beam.visible = true;
                        pMesh.beamMat.color.setHex(0xef4444);
                        pMesh.ring.visible = true;
                        pMesh.ringMat.color.setHex(0xef4444);
                        if (!firstFlaggedPos) firstFlaggedPos = pMesh.waypoints[0];
                    } else if (isFlagged) {
                        renderPedestrianTag(pMesh.tagObj, `🚨 THREAT: ${kAmt} CU (SC ${pData.sc.toFixed(2)})`, true, false);
                        pMesh.headMat.color.setHex(0xef4444);
                        pMesh.halo.visible = true;
                        pMesh.haloMat.color.setHex(0xf59e0b);
                        pMesh.beam.visible = true;
                        pMesh.beamMat.color.setHex(0xf59e0b);
                        pMesh.ring.visible = true;
                        pMesh.ringMat.color.setHex(0xef4444);
                        if (!firstFlaggedPos) firstFlaggedPos = pMesh.waypoints[0];
                    } else if (isElevated) {
                        renderPedestrianTag(pMesh.tagObj, `⚠️ WATCH: ${kAmt} CU`, false, true);
                        pMesh.headMat.color.setHex(0xf59e0b);
                        pMesh.halo.visible = true;
                        pMesh.haloMat.color.setHex(0xfacc15);
                        pMesh.beam.visible = false;
                        pMesh.ring.visible = false;
                    } else {
                        renderPedestrianTag(pMesh.tagObj, `✅ ${pData.t.slice(0,4)} ${kAmt}`, false, false);
                        pMesh.headMat.color.setHex(0x10b981);
                        pMesh.halo.visible = false;
                        pMesh.beam.visible = false;
                        pMesh.ring.visible = false;
                    }

                    updatePersonRoadPosition(pMesh);
                } else {
                    pMesh.active = false;
                    pMesh.group.position.set(0, -100, 0);
                    pMesh.tagObj.sprite.visible = false;
                }
            }

            // Sentinel targets first threat
            if (sentinelMesh && firstFlaggedPos) {
                sentinelMesh.targetPos.set(firstFlaggedPos.x, 0, firstFlaggedPos.z);
            }
        }

        function updatePersonRoadPosition(pMesh) {
            const wps = pMesh.waypoints;
            if (!wps || wps.length < 2) return;

            const totalSegments = wps.length - 1;
            const segmentProgress = pMesh.progress * totalSegments;
            const segIdx = Math.min(totalSegments - 1, Math.floor(segmentProgress));
            const localT = segmentProgress - segIdx;

            const pA = wps[segIdx];
            const pB = wps[segIdx + 1];

            pMesh.group.position.x = pA.x + (pB.x - pA.x) * localT;
            pMesh.group.position.z = pA.z + (pB.z - pA.z) * localT;

            const dx = pB.x - pA.x;
            const dz = pB.z - pA.z;
            if (Math.abs(dx) > 0.01 || Math.abs(dz) > 0.01) {
                pMesh.group.rotation.y = Math.atan2(dx, dz);
            }
        }

        function animate3DCity() {
            cityAnimId = requestAnimationFrame(animate3DCity);

            if (cityScene && !cityIs2DFallback) {
                const time = Date.now() * 0.008;

                // Smooth camera interpolation
                currentCamPos.lerp(targetCamPos, 0.05);
                currentLookTarget.lerp(targetLookTarget, 0.05);
                cityCamera.position.copy(currentCamPos);
                cityCamera.lookAt(currentLookTarget);

                // Animate walking humanoids
                cityPeopleMeshes.forEach((p, idx) => {
                    if (p.active) {
                        p.progress += p.speed;
                        if (p.progress > 1.0) p.progress = 0.0;
                        updatePersonRoadPosition(p);
                        p.group.position.y = Math.abs(Math.sin(time + idx)) * 1.2;
                        if (p.halo.visible) p.halo.rotation.z += 0.03;
                        if (p.ring.visible) {
                            const scale = 1.0 + Math.sin(time * 2 + idx) * 0.15;
                            p.ring.scale.set(scale, scale, 1);
                        }
                    }
                });

                // Sentinel gliding
                if (sentinelMesh) {
                    sentinelMesh.currentPos.lerp(sentinelMesh.targetPos, 0.03);
                    sentinelMesh.group.position.copy(sentinelMesh.currentPos);
                    sentinelMesh.group.position.y = 0.5 + Math.sin(time * 0.8) * 0.5;
                }

                cityRenderer.render(cityScene, cityCamera);
            }
        }

        window.addEventListener('DOMContentLoaded', () => {
            renderAllDynamicCards();
            updateSimScore();
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

    print("Successfully built Sentinel Mission 8 Story Dashboard & 3D Ledger City at index.html and docs/index.html")

if __name__ == "__main__":
    build_mission8_site()
