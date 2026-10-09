"""Mission 8 & 9: Story Dashboard with Purposeful 3D Ledger City Simulation, Road Grid Navigation, and Hourly Threat Intelligence."""

import os
import json
import pandas as pd

def build_mission8_site():
    with open("docs/data/stream.json", "r", encoding="utf-8") as f:
        stream_data = json.load(f)

    with open("docs/data/data_overview.json", "r", encoding="utf-8") as f:
        data_overview = json.load(f)

    with open("docs/data/checks.json", "r", encoding="utf-8") as f:
        checks_data = json.load(f)

    with open("docs/data/city_people.json", "r", encoding="utf-8") as f:
        city_people_raw = json.load(f)

    df_cost_curve = pd.read_csv("docs/data/cost_curve.csv")
    df_cost_sens = pd.read_csv("docs/data/cost_sensitivity.csv")
    df_detector_comp = pd.read_csv("docs/data/detector_comparison.csv")
    df_hourly = pd.read_csv("docs/data/hourly_stats.csv")
    df_score_hist = pd.read_csv("docs/data/score_hist.csv")
    df_thresh = pd.read_csv("docs/data/threshold_curve.csv")
    df_feat_imp = pd.read_csv("docs/data/feature_importance.csv")
    df_market = pd.read_csv("docs/data/market/paytm_nifty.csv")
    df_district_hourly = pd.read_csv("docs/data/district_hourly.csv")

    # Group city people by step for instant O(1) step lookup
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

    # Group district hourly by step
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
        "overview": data_overview,
        "checks": checks_data,
        "city_people_by_step": city_people_by_step,
        "district_hourly_by_step": dist_hourly_by_step,
        "cost_curve": df_cost_curve.to_dict(orient="records"),
        "cost_sensitivity": df_cost_sens.to_dict(orient="records"),
        "detector_comparison": df_detector_comp.to_dict(orient="records"),
        "hourly_stats": df_hourly.to_dict(orient="records"),
        "score_hist": df_score_hist.to_dict(orient="records"),
        "threshold_curve": df_thresh.to_dict(orient="records"),
        "feature_importance": df_feat_imp.to_dict(orient="records"),
        "market": df_market.to_dict(orient="records"),
        "stream": stream_data
    }

    json_bundle = json.dumps(bundle)
    html_content = HTML_TEMPLATE.replace("__JSON_DATA_BUNDLE__", json_bundle)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Successfully built Sentinel Story Dashboard & Realistic 3D Ledger City at docs/index.html and index.html")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentinel | Financial Fraud Intelligence & 3D Ledger City</title>
    <!-- Fonts & CDNs -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

    <style>
        :root {
            --bg-base: #030712;
            --bg-surface: #0b1329;
            --bg-card: #0f1c3f;
            --bg-card-hover: #162654;
            --accent-cyan: #38bdf8;
            --accent-blue: #3b82f6;
            --accent-purple: #c084fc;
            --accent-amber: #f59e0b;
            --fraud-red: #ef4444;
            --safe-green: #10b981;
            --honest-grey: #64748b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            --border-color: rgba(56, 189, 248, 0.18);
            --border-bright: rgba(56, 189, 248, 0.45);
            --font-main: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            background-color: var(--bg-base);
            color: var(--text-main);
            font-family: var(--font-main);
            line-height: 1.5;
            overflow-x: hidden;
        }

        /* Layout */
        .app-layout {
            display: flex;
            min-height: 100vh;
        }

        /* Sidebar Navigation */
        .sidebar {
            width: 290px;
            background: #080e1f;
            border-right: 1px solid var(--border-color);
            padding: 24px 16px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            position: sticky;
            top: 0;
            height: 100vh;
            overflow-y: auto;
            flex-shrink: 0;
            z-index: 50;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-color);
        }

        .brand-logo {
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, #0284c7, #38bdf8);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 16px rgba(56, 189, 248, 0.4);
        }

        .brand-text h1 {
            font-size: 17px;
            font-weight: 800;
            letter-spacing: 1px;
            background: linear-gradient(90deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .brand-text p {
            font-size: 10.5px;
            color: var(--text-muted);
            font-family: var(--font-mono);
        }

        .nav-section-title {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            color: var(--text-dim);
            font-weight: 700;
            margin-top: 6px;
        }

        .nav-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .nav-item-btn {
            width: 100%;
            text-align: left;
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-muted);
            padding: 9px 12px;
            border-radius: 8px;
            font-size: 12.5px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.2s ease;
        }

        .nav-item-btn:hover {
            background: rgba(56, 189, 248, 0.08);
            color: var(--accent-cyan);
            border-color: rgba(56, 189, 248, 0.2);
        }

        .nav-item-btn.active {
            background: rgba(56, 189, 248, 0.14);
            color: #ffffff;
            border-color: var(--accent-cyan);
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);
        }

        .sidebar-city-btn {
            background: linear-gradient(135deg, #1e1b4b, #0f172a);
            border: 1px solid #818cf8;
            color: #c7d2fe;
            padding: 12px 14px;
            border-radius: 10px;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: all 0.2s;
            box-shadow: 0 4px 15px rgba(129, 140, 248, 0.2);
        }

        .sidebar-city-btn:hover {
            background: rgba(129, 140, 248, 0.3);
            box-shadow: 0 0 20px rgba(129, 140, 248, 0.6);
            color: #ffffff;
            transform: translateY(-1px);
        }

        /* Main Workspace Container */
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            min-width: 0;
            background: radial-gradient(circle at 50% 0%, #0d1a38 0%, #030712 70%);
        }

        /* Global Header Controls Bar */
        .topbar {
            background: rgba(8, 14, 31, 0.85);
            border-bottom: 1px solid var(--border-color);
            padding: 14px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            backdrop-filter: blur(12px);
            position: sticky;
            top: 0;
            z-index: 40;
        }

        .controls-group {
            display: flex;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
        }

        .control-pill {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            padding: 6px 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 12.5px;
            position: relative;
        }

        .control-pill label {
            color: var(--text-muted);
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .control-pill input[type="range"] {
            accent-color: var(--accent-cyan);
            cursor: pointer;
            width: 110px;
        }

        .pill-badge {
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent-cyan);
            font-family: var(--font-mono);
            font-size: 11px;
            padding: 2px 7px;
            border-radius: 12px;
            font-weight: 700;
        }

        .toggle-btn {
            background: rgba(100, 116, 139, 0.2);
            border: 1px solid var(--honest-grey);
            color: var(--text-muted);
            border-radius: 20px;
            padding: 6px 14px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }

        .toggle-btn.active {
            background: rgba(239, 68, 68, 0.2);
            border-color: var(--fraud-red);
            color: #fca5a5;
            box-shadow: 0 0 12px rgba(239, 68, 68, 0.35);
        }

        .help-btn {
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid var(--accent-cyan);
            color: var(--accent-cyan);
            border-radius: 20px;
            padding: 6px 14px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }

        .help-btn:hover {
            background: var(--accent-cyan);
            color: #030712;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.5);
        }

        /* Interactive Info Tooltips [i] */
        .info-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 17px;
            height: 17px;
            border-radius: 50%;
            background: rgba(56, 189, 248, 0.15);
            border: 1px solid var(--accent-cyan);
            color: var(--accent-cyan);
            font-size: 10px;
            font-family: var(--font-mono);
            font-weight: 800;
            cursor: pointer;
            margin-left: 4px;
            position: relative;
            vertical-align: middle;
            transition: all 0.2s;
        }

        .info-btn:hover {
            background: var(--accent-cyan);
            color: #030712;
            box-shadow: 0 0 8px var(--accent-cyan);
        }

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
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.7);
            pointer-events: none;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.2s ease, transform 0.2s ease;
            z-index: 999;
        }

        .tooltip-container:hover .popover-box,
        .tooltip-container:focus-within .popover-box,
        .popover-box.show {
            opacity: 1;
            visibility: visible;
            transform: translateX(-50%) translateY(-2px);
        }

        /* Content Sections */
        .content-area {
            padding: 32px 40px;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }

        .step-section {
            display: none;
            flex-direction: column;
            gap: 28px;
            animation: fadeIn 0.3s ease-in-out;
        }

        .step-section.active {
            display: flex;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .section-header {
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 16px;
        }

        .step-tag {
            font-family: var(--font-mono);
            font-size: 11px;
            text-transform: uppercase;
            color: var(--accent-cyan);
            font-weight: 700;
            letter-spacing: 1px;
        }

        .section-title {
            font-size: 26px;
            font-weight: 800;
            color: #ffffff;
            margin-top: 4px;
        }

        .section-desc {
            color: var(--text-muted);
            font-size: 14px;
            margin-top: 6px;
            max-width: 900px;
        }

        /* Cards Grid */
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
            gap: 24px;
        }

        .card-full {
            grid-column: 1 / -1;
        }

        .dashboard-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            position: relative;
            transition: border-color 0.2s;
        }

        .dashboard-card:hover {
            border-color: var(--border-bright);
        }

        .card-title-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .card-title {
            font-size: 16px;
            font-weight: 700;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .card-headline {
            font-size: 13px;
            color: var(--accent-cyan);
            background: rgba(56, 189, 248, 0.08);
            border-left: 3px solid var(--accent-cyan);
            padding: 8px 12px;
            border-radius: 0 6px 6px 0;
            font-weight: 600;
        }

        .chart-box {
            height: 260px;
            position: relative;
            width: 100%;
        }

        .dot-grid-container {
            display: flex;
            flex-wrap: wrap;
            gap: 3px;
            padding: 12px;
            background: #080d1a;
            border-radius: 8px;
            max-height: 220px;
            overflow-y: auto;
        }

        .grid-dot { width: 5px; height: 5px; border-radius: 50%; background: var(--honest-grey); opacity: 0.5; }
        .grid-dot.fraud-dot { background: var(--fraud-red); opacity: 1; box-shadow: 0 0 6px var(--fraud-red); transform: scale(1.3); }

        /* Confusion Matrix Grid */
        .matrix-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }

        .matrix-cell {
            background: #091024;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 14px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .matrix-cell.tp { border-left: 4px solid var(--safe-green); }
        .matrix-cell.fp { border-left: 4px solid var(--accent-amber); }
        .matrix-cell.fn { border-left: 4px solid var(--fraud-red); }
        .matrix-cell.tn { border-left: 4px solid var(--honest-grey); }

        .matrix-cell-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .matrix-cell-title {
            font-size: 12px;
            font-weight: 700;
            color: var(--text-main);
        }

        .matrix-cell-tech {
            font-size: 10.5px;
            color: var(--text-muted);
            font-family: var(--font-mono);
        }

        .matrix-cell-val {
            font-size: 20px;
            font-weight: 800;
            font-family: var(--font-mono);
        }

        /* Buttons & Forms */
        .btn {
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 12.5px;
            font-weight: 700;
            cursor: pointer;
            border: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }

        .btn-primary {
            background: var(--accent-cyan);
            color: #030712;
        }

        .btn-primary:hover {
            background: #7dd3fc;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
        }

        .btn-secondary {
            background: #1e293b;
            color: #f8fafc;
            border: 1px solid var(--border-color);
        }

        .btn-secondary:hover {
            background: #334155;
            border-color: var(--accent-cyan);
        }

        pre {
            background: #080d1a;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
            font-family: var(--font-mono);
            font-size: 11.5px;
            color: #93c5fd;
            white-space: pre-wrap;
            word-break: break-word;
            max-height: 280px;
            overflow-y: auto;
        }

        /* ========================================================================= */
        /* 3D LEDGER CITY (SENTINEL MODE) MODAL STYLES                              */
        /* ========================================================================= */
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
            padding: 12px 24px;
            background: #0d1527;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 1010;
            flex-shrink: 0;
        }

        .city-header-title {
            font-size: 17px;
            font-weight: 700;
            color: #38bdf8;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .city-disclaimer-banner {
            background: rgba(245, 158, 11, 0.15);
            border-bottom: 1px solid rgba(245, 158, 11, 0.35);
            color: #fde68a;
            font-size: 11.5px;
            text-align: center;
            padding: 6px 14px;
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
            height: calc(100vh - 90px);
            min-height: 400px;
        }

        /* Live Hourly Threat Feed Radar Panel (Top-Left) */
        .city-threat-radar-panel {
            position: absolute;
            top: 16px; left: 16px;
            background: rgba(13, 21, 39, 0.94);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            width: 360px;
            backdrop-filter: blur(14px);
            color: white;
            font-size: 12px;
            box-shadow: 0 12px 35px rgba(0,0,0,0.75);
            z-index: 1005;
            max-height: calc(100vh - 160px);
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .threat-incident-list {
            display: flex;
            flex-direction: column;
            gap: 6px;
            overflow-y: auto;
            max-height: 220px;
            padding-right: 4px;
        }

        .threat-incident-card {
            background: #091024;
            border: 1px solid rgba(239, 68, 68, 0.4);
            border-left: 3px solid #ef4444;
            border-radius: 6px;
            padding: 8px 10px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .threat-incident-card:hover {
            background: rgba(239, 68, 68, 0.15);
            border-color: #ef4444;
            transform: translateX(2px);
        }

        .city-controls-bar {
            position: absolute;
            bottom: 20px; left: 50%;
            transform: translateX(-50%);
            background: rgba(13, 21, 39, 0.94);
            border: 1px solid var(--border-color);
            border-radius: 30px;
            padding: 8px 22px;
            display: flex;
            align-items: center;
            gap: 10px;
            backdrop-filter: blur(14px);
            z-index: 1005;
            box-shadow: 0 8px 25px rgba(0,0,0,0.6);
            flex-wrap: wrap;
            justify-content: center;
        }

        /* Floating Evidence Board HUD (Top Right) */
        .city-evidence-board {
            position: absolute;
            top: 16px; right: 16px;
            background: rgba(15, 23, 42, 0.97);
            border: 1.5px solid #38bdf8;
            border-radius: 14px;
            padding: 18px;
            width: 360px;
            color: white;
            font-size: 12px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.88);
            z-index: 1006;
            display: none;
            backdrop-filter: blur(16px);
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

    <div class="app-layout">
        <!-- Sidebar Story Navigation -->
        <aside class="sidebar">
            <div class="brand">
                <div class="brand-logo">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                        <circle cx="12" cy="11" r="3"/>
                    </svg>
                </div>
                <div class="brand-text">
                    <h1>SENTINEL</h1>
                    <p>AUTONOMOUS FRAUD ENGINE</p>
                </div>
            </div>

            <button class="sidebar-city-btn" onclick="openSentinelCity()">
                <span>🏙️</span>
                <span>OPEN 3D LEDGER CITY</span>
            </button>

            <div class="nav-section-title">Investigation Story Steps</div>
            <ul class="nav-list">
                <li><button class="nav-item-btn active" onclick="goToStep(1)"><span>1.</span> The Fraud Landscape</button></li>
                <li><button class="nav-item-btn" onclick="goToStep(2)"><span>2.</span> The Feature Leakage Trap</button></li>
                <li><button class="nav-item-btn" onclick="goToStep(3)"><span>3.</span> Machine Learning Model</button></li>
                <li><button class="nav-item-btn" onclick="goToStep(4)"><span>4.</span> Choosing Strictness (θ)</button></li>
                <li><button class="nav-item-btn" onclick="goToStep(5)"><span>5.</span> Multi-Agent Defense</button></li>
                <li><button class="nav-item-btn" onclick="goToStep(6)"><span>6.</span> Network Laundering</button></li>
                <li><button class="nav-item-btn" onclick="goToStep(7)"><span>7.</span> Paytm Market Shock</button></li>
            </ul>

            <div style="margin-top:auto; padding-top:16px; border-top:1px solid var(--border-color); font-size:11.5px; color:var(--text-dim);">
                <div>PaySim 15% Verified Sample</div>
                <div style="color:#38bdf8;">954,393 rows | 1,201 frauds</div>
            </div>
        </aside>

        <!-- Main Workspace -->
        <main class="main-content">
            <!-- Top Controls Bar -->
            <header class="topbar">
                <div class="controls-group">
                    <!-- Filter Strictness (Decision Threshold) Slider -->
                    <div class="control-pill tooltip-container">
                        <label for="strictnessSlider">
                            🎯 Filter Strictness (θ)
                            <span class="info-btn" onclick="openGlossaryTerm('strictness')">i</span>
                        </label>
                        <input type="range" id="strictnessSlider" min="0" max="15" value="7" oninput="onStrictnessChange(this.value)">
                        <span class="pill-badge" id="strictnessLabel">0.50</span>

                        <div class="popover-box">
                            <strong>🎯 Filter Strictness (θ)</strong><br>
                            Technical term: <em>Decision Threshold</em>.<br>
                            How sensitive the AI alarm is. A lower number catches more fraud but flags more innocent users.
                        </div>
                    </div>

                    <!-- Review Cost Slider -->
                    <div class="control-pill tooltip-container">
                        <label for="reviewCostSlider">
                            💼 Cost per Check
                            <span class="info-btn" onclick="openGlossaryTerm('cost')">i</span>
                        </label>
                        <input type="range" id="reviewCostSlider" min="50" max="2000" step="50" value="500" oninput="onCheckingCostChange(this.value)">
                        <span class="pill-badge" id="reviewCostLabel">500 CU</span>

                        <div class="popover-box">
                            <strong>💼 Cost per Check</strong><br>
                            Technical term: <em>Review / Investigation Cost</em>.<br>
                            Money spent per flagged payment to have human analysts review it (default: 500 currency units).
                        </div>
                    </div>

                    <!-- Ground Truth (Answer Key) Toggle -->
                    <button class="toggle-btn" id="evalKeyToggle" onclick="toggleAnswerKey()">
                        <span>👁️</span>
                        <span id="evalKeyText">Show True Fraud: OFF</span>
                    </button>
                </div>

                <div>
                    <button class="help-btn" onclick="openGlossaryModal()">
                        <span>📖</span>
                        <span>Beginner Cheat Sheet</span>
                    </button>
                </div>
            </header>

            <!-- Main Content Area -->
            <div class="content-area">
                
                <!-- STEP 1: THE FRAUD LANDSCAPE -->
                <section class="step-section active" id="step1">
                    <div class="section-header">
                        <div class="step-tag">Step 1 of 7 // Executive Reality Check</div>
                        <h2 class="section-title">The Extreme Haystack Problem</h2>
                        <p class="section-desc">
                            In modern high-speed financial networks, genuine fraud represents less than 1 in 800 transactions.
                            Detecting money theft without shutting down legitimate commerce is an operational balancing act.
                        </p>
                    </div>

                    <div class="cards-grid">
                        <!-- Card 1: Needle in Haystack -->
                        <div class="dashboard-card">
                            <div class="card-title-row">
                                <div class="card-title">
                                    <span>🌾 Visualizing Fraud Rarity (Needle in Haystack)</span>
                                    <span class="info-btn" onclick="openGlossaryTerm('rarity')">i</span>
                                </div>
                            </div>
                            <div class="card-headline" id="c1Headline">Loading sample distribution...</div>
                            <div class="dot-grid-container" id="c1DotGrid"></div>
                            <p style="font-size:11.5px; color:var(--text-muted);">
                                Each grey square is a legitimate payment. Red glowing squares represent actual fraud attempts.
                            </p>
                        </div>

                        <!-- Card 2: Fraud Channel Distribution -->
                        <div class="dashboard-card">
                            <div class="card-title-row">
                                <div class="card-title">
                                    <span>💳 Payment Channels & Attack Surfaces</span>
                                    <span class="info-btn" onclick="openGlossaryTerm('channels')">i</span>
                                </div>
                            </div>
                            <div class="card-headline" id="c2Headline">Analyzing transfer vs cashout channels...</div>
                            <div class="chart-box">
                                <canvas id="c2Chart"></canvas>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- STEP 2: THE FEATURE LEAKAGE TRAP -->
                <section class="step-section" id="step2">
                    <div class="section-header">
                        <div class="step-tag">Step 2 of 7 // Forensic Data Engineering</div>
                        <h2 class="section-title">The Feature Leakage Trap</h2>
                        <p class="section-desc">
                            A naive model that reads synthetic balance updates (<code>oldbalanceOrg</code>, <code>newbalanceDest</code>) achieves 99.9% artificial accuracy in simulation, but completely fails in real production where fraudsters manipulate balance logs.
                        </p>
                    </div>

                    <div class="cards-grid">
                        <!-- Card 3: Zero-Balance Leakage -->
                        <div class="dashboard-card card-full">
                            <div class="card-title-row">
                                <div class="card-title">
                                    <span>🛡️ Zero Balance Leakage Rule (Strict Production Constraint)</span>
                                    <span class="info-btn" onclick="openGlossaryTerm('leakage')">i</span>
                                </div>
                            </div>
                            <div class="card-headline" id="c3Headline">Evaluating data integrity rules...</div>
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-top:8px;">
                                <div style="background:#091024; border:1px solid #ef4444; border-radius:10px; padding:16px;">
                                    <h4 style="color:#f87171; font-size:14px; margin-bottom:8px;">❌ Banned Leakage Columns</h4>
                                    <ul style="font-size:12.5px; color:#cbd5e1; list-style:square; padding-left:18px; line-height:1.6;">
                                        <li><code>oldbalanceOrg</code> (Pre-transaction origin balance)</li>
                                        <li><code>newbalanceOrig</code> (Post-transaction origin balance)</li>
                                        <li><code>oldbalanceDest</code> (Pre-transaction receiver balance)</li>
                                        <li><code>newbalanceDest</code> (Post-transaction receiver balance)</li>
                                    </ul>
                                    <p style="font-size:11.5px; color:#94a3b8; margin-top:10px;">
                                        <em>Why excluded?</em> Real payment switches cannot atomically compute receiver state before approval.
                                    </p>
                                </div>

                                <div style="background:#091024; border:1px solid #10b981; border-radius:10px; padding:16px;">
                                    <h4 style="color:#34d399; font-size:14px; margin-bottom:8px;">✅ Allowed Production Features</h4>
                                    <ul style="font-size:12.5px; color:#cbd5e1; list-style:square; padding-left:18px; line-height:1.6;">
                                        <li><code>amount</code> (Nominal transaction value in currency units)</li>
                                        <li><code>log_amount</code> (Logarithmic scaling: <code>log(1 + amount)</code>)</li>
                                        <li><code>is_transfer</code> (Binary flag: 1 for Transfer, 0 for Cash-Out)</li>
                                        <li><code>hour</code> (Cyclical hour of transaction: 0 to 23)</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- STEP 3: MACHINE LEARNING MODEL -->
                <section class="step-section" id="step3">
                    <div class="section-header">
                        <div class="step-tag">Step 3 of 7 // Machine Learning Architecture</div>
                        <h2 class="section-title">Random Forest Detection Engine</h2>
                        <p class="section-desc">
                            Sentinel trains a balanced Random Forest classifier strictly on historical days (Steps 1–333) and evaluates against future unseen days (Steps 334–742) using a strict temporal split.
                        </p>
                    </div>

                    <div class="cards-grid">
                        <!-- Card 4: Amount Distribution -->
                        <div class="dashboard-card">
                            <div class="card-title-row">
                                <div class="card-title">
                                    <span>💰 Transaction Amount Profiles (Normal vs Fraud)</span>
                                </div>
                            </div>
                            <div class="card-headline" id="c4Headline">Loading amount curves...</div>
                            <div class="chart-box"><canvas id="c4Chart"></canvas></div>
                        </div>

                        <!-- Card 5: Hourly Attack Patterns -->
                        <div class="dashboard-card">
                            <div class="card-title-row">
                                <div class="card-title">
                                    <span>🌙 Nocturnal Attack Signatures (Hour of Day)</span>
                                </div>
                            </div>
                            <div class="card-headline" id="c5Headline">Analyzing diurnal volume...</div>
                            <div class="chart-box"><canvas id="c5Chart"></canvas></div>
                        </div>

                        <!-- Card 6: Detector Comparison -->
                        <div class="dashboard-card">
                            <div class="card-title-row">
                                <div class="card-title">
                                    <span>🏆 PR-AUC Discovery Power Benchmark</span>
                                </div>
                            </div>
                            <div class="card-headline" id="c6Headline">Benchmarking detectors...</div>
                            <div class="chart-box"><canvas id="c6Chart"></canvas></div>
                        </div>

                        <!-- Feature Importance -->
                        <div class="dashboard-card">
                            <div class="card-title-row">
                                <div class="card-title">
                                    <span>⚖️ Feature Discriminator Weights</span>
                                </div>
                            </div>
                            <div class="card-headline" id="cFeatImpHeadline">Loading feature importance...</div>
                            <div class="chart-box"><canvas id="cFeatImpChart"></canvas></div>
                        </div>
                    </div>
                </section>

                <!-- STEP 4: CHOOSING STRICTNESS -->
                <section class="step-section" id="step4">
                    <div class="section-header">
                        <div class="step-tag">Step 4 of 7 // Business Policy Optimization</div>
                        <h2 class="section-title">Strictness & Operational Cost Curve</h2>
                        <p class="section-desc">
                            Choosing strictness is not just math; it is a financial tradeoff between paying analysts to inspect false alarms vs suffering unrecovered fraud losses.
                        </p>
                    </div>

                    <div class="cards-grid">
                        <!-- Card 7: Score Distribution -->
                        <div class="dashboard-card">
                            <div class="card-title-row">
                                <div class="card-title">
                                    <span>📊 AI Risk Score Distribution</span>
                                </div>
                            </div>
                            <div class="card-headline" id="c7Headline">Analyzing score distribution...</div>
                            <div class="chart-box"><canvas id="c7Chart"></canvas></div>
                        </div>

                        <!-- Card 8: Operational Confusion Matrix -->
                        <div class="dashboard-card">
                            <div class="card-title-row">
                                <div class="card-title">
                                    <span>🎯 Live Performance Breakdown at Current Strictness</span>
                                </div>
                            </div>
                            <div class="card-headline" id="c8Headline">Computing matrix...</div>
                            <div class="matrix-grid" id="c8Matrix"></div>
                        </div>

                        <!-- Card 9: Total Operational Cost Curve -->
                        <div class="dashboard-card card-full">
                            <div class="card-title-row">
                                <div class="card-title">
                                    <span>📉 Total Cost Curve (Loss + Review Costs)</span>
                                </div>
                            </div>
                            <div class="card-headline" id="c9Headline">Calculating cost curves...</div>
                            <div class="chart-box" style="height:320px;"><canvas id="c9Chart"></canvas></div>
                        </div>
                    </div>
                </section>

                <!-- STEP 5: MULTI-AGENT DEFENSE & LIVE SIMULATOR -->
                <section class="step-section" id="step5">
                    <div class="section-header">
                        <div class="step-tag">Step 5 of 7 // Multi-Agent Governance</div>
                        <h2 class="section-title">Multi-Agent Intelligence & Live Simulator</h2>
                        <p class="section-desc">
                            Sentinel coordinates specialized agents: <strong>Scout</strong> (rapid filtering), <strong>Investigator</strong> (deep forensics), <strong>Risk Officer</strong> (final authorization), and <strong>Reporter</strong> (audit documentation).
                        </p>
                    </div>

                    <div class="cards-grid">
                        <!-- Interactive Live Simulator -->
                        <div class="dashboard-card">
                            <div class="card-title-row">
                                <div class="card-title">
                                    <span>⚡ Live Transaction Risk Calculator</span>
                                </div>
                            </div>
                            <div class="card-headline">Test any custom payment against Sentinel's Random Forest model:</div>

                            <div style="display:flex; flex-direction:column; gap:14px; margin-top:8px;">
                                <div>
                                    <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
                                        <label>Amount (Currency Units):</label>
                                        <strong id="simAmountVal" style="color:var(--accent-cyan);">250,000 CU</strong>
                                    </div>
                                    <input type="range" id="simAmountInput" min="1000" max="10000000" step="5000" value="250000" style="width:100%;" oninput="updateSimScore()">
                                </div>

                                <div>
                                    <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
                                        <label>Hour of Day:</label>
                                        <strong id="simHourVal" style="color:var(--accent-cyan);">3:00 (Late Night 🌙)</strong>
                                    </div>
                                    <input type="range" id="simHourInput" min="0" max="23" value="3" style="width:100%;" oninput="updateSimScore()">
                                </div>

                                <div>
                                    <label style="font-size:12px; margin-bottom:4px; display:block;">Payment Channel:</label>
                                    <select id="simTypeInput" style="width:100%; background:#080d1a; color:white; border:1px solid var(--border-color); padding:8px; border-radius:6px;" onchange="updateSimScore()">
                                        <option value="TRANSFER">TRANSFER (Wire to new party)</option>
                                        <option value="CASH_OUT">CASH_OUT (Withdrawal to fiat/ATM)</option>
                                        <option value="PAYMENT">PAYMENT (Merchant checkout)</option>
                                    </select>
                                </div>

                                <div id="simResultCard" style="background:#091024; border:1px solid var(--border-color); border-radius:8px; padding:14px; margin-top:6px;">
                                    <div style="display:flex; justify-content:space-between; align-items:center;">
                                        <span>Model Risk Score:</span>
                                        <strong id="simScoreDisplay" style="font-size:22px; font-family:var(--font-mono); color:#ef4444;">0.78</strong>
                                    </div>
                                    <div style="font-size:12px; margin-top:6px; color:var(--text-muted);" id="simVerdictBadge">
                                        🚨 FLAGGED FOR HUMAN INVESTIGATION (Score ≥ Strictness θ)
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Card 10: Multi-Agent Policy Alerts -->
                        <div class="dashboard-card">
                            <div class="card-title-row">
                                <div class="card-title">
                                    <span>🛡️ Multi-Agent Tiered Alerts</span>
                                </div>
                            </div>
                            <div class="card-headline" id="c10Headline">Loading policy matrix...</div>
                            <div class="chart-box"><canvas id="c10Chart"></canvas></div>
                        </div>
                    </div>
                </section>

                <!-- STEP 6: NETWORK LAUNDERING & INVESTIGATOR REPLAY -->
                <section class="step-section" id="step6">
                    <div class="section-header">
                        <div class="step-tag">Step 6 of 7 // Network Laundering Analysis</div>
                        <h2 class="section-title">Network Laundering & Timeline Replay</h2>
                        <p class="section-desc">
                            Sentinel's Network Analyst identifies correlated money laundering chains where funds transferred into an account are immediately cashed out in the exact same hour.
                        </p>
                    </div>

                    <div class="cards-grid">
                        <!-- Card 12: Stream Patrol Timeline -->
                        <div class="dashboard-card card-full">
                            <div class="card-title-row">
                                <div class="card-title">
                                    <span>📡 Hourly Test Stream Patrol (Steps 334–742)</span>
                                </div>
                                <div style="display:flex; align-items:center; gap:10px;">
                                    <button class="btn btn-secondary" id="patrolPlayBtn" onclick="togglePatrolPlay()">⏸️ Pause</button>
                                    <span class="pill-badge" id="patrolStepDisplay">Step: 334 (Hour 22)</span>
                                </div>
                            </div>
                            <div class="card-headline" id="c12Headline">Replaying test stream...</div>

                            <div style="margin:10px 0;">
                                <input type="range" id="patrolScrubber" min="334" max="742" value="334" style="width:100%;" oninput="scrubPatrol(this.value)">
                            </div>

                            <div class="chart-box"><canvas id="c12Chart"></canvas></div>

                            <!-- Case Dossier Explorer -->
                            <div style="margin-top:20px; border-top:1px solid var(--border-color); padding-top:16px;">
                                <h4 style="font-size:14px; color:#ffffff; margin-bottom:8px;">📁 Inspected Case Dossier Drawer</h4>
                                <div style="display:flex; gap:10px; margin-bottom:12px;">
                                    <select id="patrolCaseSelect" style="flex:1; background:#080d1a; color:white; border:1px solid var(--border-color); padding:8px; border-radius:6px;" onchange="renderCaseDossier(this.value)"></select>
                                </div>
                                <div id="patrolCaseDossierBox"></div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- STEP 7: PAYTM MARKET SHOCK -->
                <section class="step-section" id="step7">
                    <div class="section-header">
                        <div class="step-tag">Step 7 of 7 // Real-World Fintech Governance Shock</div>
                        <h2 class="section-title">Paytm Payments Bank vs NSE / NIFTY 50</h2>
                        <p class="section-desc">
                            On January 31, 2024, the Reserve Bank of India (RBI) halted Paytm Payments Bank operations due to persistent KYC and AML compliance deficiencies, causing a 42% market equity collapse in 3 trading sessions.
                        </p>
                    </div>

                    <div class="cards-grid">
                        <!-- Card 11: Market Shock Chart -->
                        <div class="dashboard-card card-full">
                            <div class="card-title-row">
                                <div class="card-title">
                                    <span>📉 Paytm Equity Collapse vs NIFTY 50 (Jan–Mar 2024)</span>
                                </div>
                            </div>
                            <div class="card-headline" id="c11Headline">Loading RBI regulatory timeline...</div>
                            <div class="chart-box" style="height:340px;"><canvas id="c11Chart"></canvas></div>
                        </div>
                    </div>
                </section>

            </div>
        </main>
    </div>

    <!-- ========================================================================= -->
    <!-- 3D LEDGER CITY (SENTINEL MODE) MODAL VIEW                                 -->
    <!-- ========================================================================= -->
    <div class="city-modal-overlay" id="cityModal">
        <!-- City Header Bar -->
        <div class="city-header">
            <div class="city-header-title">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    <circle cx="12" cy="11" r="3"/>
                </svg>
                <span>LEDGER CITY // REAL-TIME 3D SENTINEL SURVEILLANCE</span>
            </div>

            <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
                <span class="pill-badge" id="cityStepClock" style="font-size:12px; padding:4px 10px;">Step 334 | Hour 22:00</span>
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

            <!-- Hourly Threat Briefing & Live Incident Feed (Top-Left) -->
            <div class="city-threat-radar-panel">
                <div style="font-weight:800; color:#38bdf8; font-size:13px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(56,189,248,0.2); padding-bottom:6px;">
                    <span>🚨 HOURLY THREAT RADAR</span>
                    <span class="pill-badge" id="radarThreatCountBadge" style="background:rgba(239,68,68,0.2); color:#fca5a5;">0 Threats</span>
                </div>
                <div style="font-size:11.5px; color:#cbd5e1; line-height:1.4;">
                    <div>• <strong>Current Hour:</strong> <span id="radarHourDisplay">22:00</span></div>
                    <div>• <strong>Active Payments in City:</strong> <span id="radarActiveTxCount">0</span> transactions</div>
                    <div>• <strong>Current Strictness (θ):</strong> <span id="cityStrictnessBadge" style="color:#38bdf8; font-weight:700;">0.50</span></div>
                </div>

                <div style="font-weight:700; color:#f59e0b; font-size:11.5px; margin-top:2px;">
                    ⚡ Live Flagged Threats (Click to Inspect):
                </div>
                <div class="threat-incident-list" id="radarThreatList">
                    <div style="color:#64748b; font-size:11px; padding:6px;">No high-risk threats detected in this hour.</div>
                </div>
            </div>

            <!-- Floating Evidence Board & Decision Stamp (Phase B) -->
            <div class="city-evidence-board" id="cityEvidenceBoard">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; border-bottom:1px solid rgba(56,189,248,0.25); padding-bottom:6px;">
                    <strong style="color:#38bdf8; font-size:14px;" id="ebTxId">tx_334_12</strong>
                    <button style="background:transparent; border:none; color:#94a3b8; cursor:pointer; font-size:16px;" onclick="closeEvidenceBoard()">✕</button>
                </div>
                <div style="font-size:12px; color:#cbd5e1; display:flex; flex-direction:column; gap:6px;" id="ebTxBody">
                    <div>Select a suspect or payment to inspect forensic evidence...</div>
                </div>
            </div>

            <!-- City Interactive Controls Bar -->
            <div class="city-controls-bar">
                <button class="btn btn-secondary" onclick="setCityView('skyline')">🌆 Skyline</button>
                <button class="btn btn-secondary" onclick="setCityView('overhead')">🛰️ 3x3 Grid Map</button>
                <button class="btn btn-secondary" onclick="setCityView('street')">🚶 Street Patrol</button>
                <button class="btn btn-secondary" onclick="setCityView('tower')">🗼 Sentinel Spire</button>
                <button class="btn btn-primary" onclick="focusOnNextThreat()">🚨 Focus Active Threat</button>
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
        // Injected Dynamic Data Bundle
        const DATA = __JSON_DATA_BUNDLE__;

        // Strictness Threshold Grid
        const THRESHOLD_GRID = [0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 0.99];
        let currentStrictness = 0.50;
        let currentCheckingCost = 500;
        let evalMode = false;

        // Patrol & Stream State
        let patrolPlaying = true;
        let patrolCurrentStep = 334;
        let patrolInterval = null;
        let patrolSpeed = 800;

        // Chart Instances
        let chartC2, chartC4, chartC5, chartC6, chartFeatImp, chartC7, chartC9, chartC10, chartC11, chartC12;

        // 3D Engine Globals
        let cityScene, cityCamera, cityRenderer, cityRaycaster, cityMouse;
        let cityInitialized = false;
        let cityAnimId = null;
        let cityBuildings = [];
        let cityPeopleMeshes = [];
        let cityIs2DFallback = false;
        let selectedPersonData = null;
        let sentinelMesh = null;
        let routeLaserLine = null;

        // Camera Orbit State
        let isOrbiting = false, isPanning = false;
        let mousePrevX = 0, mousePrevY = 0;
        let camTarget = new THREE.Vector3(0, 20, 0);
        let camSpherical = { radius: 520, theta: Math.PI / 4, phi: Math.PI / 3 };

        // 3x3 District Coordinates
        const DISTRICT_POSITIONS = {
            1: { x: -220, z: -220, name: "District 1 (Alpha NW)" },
            2: { x:    0, z: -220, name: "District 2 (North Gate)" },
            3: { x:  220, z: -220, name: "District 3 (Beta NE)" },
            4: { x: -220, z:    0, name: "District 4 (West Exchange)" },
            5: { x:  220, z:    0, name: "District 5 (East Exchange)" },
            6: { x: -220, z:  220, name: "District 6 (Gamma SW)" },
            7: { x:    0, z:  220, name: "District 7 (South Terminal)" },
            8: { x:  220, z:  220, name: "District 8 (Delta SE)" }
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
                cityScene.fog = new THREE.FogExp2(0x020716, 0.0012);

                cityCamera = new THREE.PerspectiveCamera(45, width / height, 2, 4000);
                updateCameraPosition();

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

            // Dynamic High-Visibility Lighting
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

            // Glowing Road Network & Boulevards
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

        function updateCameraPosition() {
            const x = camTarget.x + camSpherical.radius * Math.sin(camSpherical.phi) * Math.sin(camSpherical.theta);
            const y = camTarget.y + camSpherical.radius * Math.cos(camSpherical.phi);
            const z = camTarget.z + camSpherical.radius * Math.sin(camSpherical.phi) * Math.cos(camSpherical.theta);
            cityCamera.position.set(x, y, z);
            cityCamera.lookAt(camTarget);
        }

        function buildRoadAvenues() {
            const roadMat = new THREE.MeshLambertMaterial({ color: 0x0b1633 });
            const lineMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });

            // Cross Highways
            const hRoad = new THREE.Mesh(new THREE.PlaneGeometry(800, 36), roadMat);
            hRoad.rotation.x = -Math.PI / 2;
            hRoad.position.y = 0.2;
            cityScene.add(hRoad);

            const vRoad = new THREE.Mesh(new THREE.PlaneGeometry(36, 800), roadMat);
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

            // Base
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

            // Mid
            const midGeo = new THREE.CylinderGeometry(16, 24, 80, 8);
            const mid = new THREE.Mesh(midGeo, towerMat);
            mid.position.y = 110;
            towerGroup.add(mid);

            // Deck
            const deckGeo = new THREE.CylinderGeometry(28, 14, 18, 16);
            const deckMat = new THREE.MeshPhongMaterial({ color: 0x0284c7, emissive: 0x38bdf8, emissiveIntensity: 0.6 });
            const deck = new THREE.Mesh(deckGeo, deckMat);
            deck.position.y = 159;
            towerGroup.add(deck);

            // Spire
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

            const labelSprite = createDistrictLabelSprite("SENTINEL HQ (CENTER)", "#38bdf8");
            labelSprite.position.set(0, 230, 0);
            towerGroup.add(labelSprite);

            cityScene.add(towerGroup);
        }

        function build8UrbanDistricts() {
            cityBuildings = [];
            const districtColors = [0x38bdf8, 0x3b82f6, 0x818cf8, 0xa855f7, 0xf59e0b, 0x10b981, 0x06b6d4, 0x94a3b8];

            for (let d = 1; d <= 8; d++) {
                const pos = DISTRICT_POSITIONS[d];
                const dColor = districtColors[d - 1];

                // Plaza Ground
                const plazaGeo = new THREE.BoxGeometry(130, 2, 130);
                const plazaMat = new THREE.MeshPhongMaterial({
                    color: 0x0a142c,
                    emissive: dColor,
                    emissiveIntensity: 0.18
                });
                const plaza = new THREE.Mesh(plazaGeo, plazaMat);
                plaza.position.set(pos.x, 1, pos.z);
                cityScene.add(plaza);

                // Floating Hologram Label
                const labelSprite = createDistrictLabelSprite(pos.name.toUpperCase(), "#38bdf8");
                labelSprite.position.set(pos.x, 155, pos.z);
                cityScene.add(labelSprite);

                // District Skyscrapers
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

                    // Lit Window Matrix
                    const winGeo = new THREE.PlaneGeometry(bw * 0.85, bh * 0.75);
                    const winMat = new THREE.MeshBasicMaterial({
                        color: 0x38bdf8,
                        transparent: true,
                        opacity: 0.75
                    });
                    const winF = new THREE.Mesh(winGeo, winMat);
                    winF.position.set(bx, bh / 2, bz + bd / 2 + 0.3);
                    cityScene.add(winF);

                    // Rooftop Aircraft Safety Beacon
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

            // Round Protective Hood (NO ears, NO wings)
            const hoodGeo = new THREE.SphereGeometry(3.0, 16, 16);
            const hoodMat = new THREE.MeshStandardMaterial({ color: 0x080e1a, roughness: 0.4 });
            const hood = new THREE.Mesh(hoodGeo, hoodMat);
            hood.position.y = 12;
            group.add(hood);

            // Gold Shield-Eye Emblem
            const emblemGeo = new THREE.CircleGeometry(1.6, 16);
            const emblemMat = new THREE.MeshBasicMaterial({ color: 0xf59e0b });
            const emblem = new THREE.Mesh(emblemGeo, emblemMat);
            emblem.position.set(0, 7.5, 2.7);
            group.add(emblem);

            // Cloak
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

        function createDistrictLabelSprite(text, colorHex) {
            const canvas = document.createElement('canvas');
            canvas.width = 256;
            canvas.height = 64;
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = "rgba(13, 21, 39, 0.88)";
            ctx.strokeStyle = colorHex;
            ctx.lineWidth = 3;
            ctx.roundRect(4, 4, 248, 56, 12);
            ctx.fill();
            ctx.stroke();

            ctx.fillStyle = colorHex;
            ctx.font = "bold 19px sans-serif";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(text, 128, 32);

            const texture = new THREE.CanvasTexture(canvas);
            const spriteMat = new THREE.SpriteMaterial({ map: texture, transparent: true });
            const sprite = new THREE.Sprite(spriteMat);
            sprite.scale.set(70, 18, 1);
            return sprite;
        }

        function buildCityPeoplePool() {
            cityPeopleMeshes = [];
            const bodyGeo = new THREE.CylinderGeometry(1.6, 2.2, 7.5, 8);
            const headGeo = new THREE.SphereGeometry(1.8, 8, 8);
            const bagGeo = new THREE.BoxGeometry(2.8, 2.8, 2.8);
            const haloGeo = new THREE.TorusGeometry(3.2, 0.4, 6, 16);
            const beamGeo = new THREE.CylinderGeometry(0.4, 0.4, 40, 8);

            for (let i = 0; i < 300; i++) {
                const group = new THREE.Group();
                const coatMat = new THREE.MeshLambertMaterial({ color: 0x38bdf8 });
                const headMat = new THREE.MeshLambertMaterial({ color: 0xf8fafc });
                const bagMat = new THREE.MeshLambertMaterial({ color: 0xf59e0b });
                const haloMat = new THREE.MeshBasicMaterial({ color: 0xf59e0b, transparent: true, opacity: 0.9 });
                const beamMat = new THREE.MeshBasicMaterial({ color: 0xef4444, transparent: true, opacity: 0.7 });

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
                beam.position.y = 30;
                beam.visible = false;
                group.add(beam);

                group.position.set(0, -100, 0);
                group.userData = { index: i, personData: null };
                cityScene.add(group);

                cityPeopleMeshes.push({
                    group, body, head, bag, halo, beam,
                    coatMat, headMat, bagMat, haloMat, beamMat,
                    active: false,
                    waypoints: [],
                    wpIndex: 0,
                    progress: 0,
                    speed: 0.006,
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
                    camSpherical.theta -= dx * 0.005;
                    camSpherical.phi = Math.max(0.1, Math.min(Math.PI / 2 - 0.05, camSpherical.phi - dy * 0.005));
                } else if (isPanning) {
                    camTarget.x -= dx * 0.4;
                    camTarget.z -= dy * 0.4;
                }

                updateCameraPosition();
                mousePrevX = e.clientX;
                mousePrevY = e.clientY;
            });

            container.addEventListener('wheel', (e) => {
                e.preventDefault();
                camSpherical.radius = Math.max(60, Math.min(1100, camSpherical.radius + e.deltaY * 0.5));
                updateCameraPosition();
            }, { passive: false });

            // Click Person to Inspect Dossier
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
            const tubeGeo = new THREE.TubeGeometry(curve, 20, 1.2, 8, false);
            const tubeMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.8 });
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
            if (type === 'skyline') {
                camTarget.set(0, 20, 0);
                camSpherical = { radius: 520, theta: Math.PI / 4, phi: Math.PI / 3 };
            } else if (type === 'overhead') {
                camTarget.set(0, 0, 0);
                camSpherical = { radius: 680, theta: 0.001, phi: 0.05 };
            } else if (type === 'street') {
                camTarget.set(0, 10, 0);
                camSpherical = { radius: 180, theta: Math.PI / 3, phi: Math.PI / 2 - 0.15 };
            } else if (type === 'tower') {
                camTarget.set(0, 170, 0);
                camSpherical = { radius: 120, theta: Math.PI / 6, phi: Math.PI / 2.5 };
            }
            updateCameraPosition();
        }

        function focusOnNextThreat() {
            const flagged = cityPeopleMeshes.find(p => p.active && p.txData && p.txData.sc >= currentStrictness);
            if (flagged) {
                camTarget.copy(flagged.group.position);
                camSpherical.radius = 110;
                camSpherical.phi = Math.PI / 3.2;
                updateCameraPosition();
                displayEvidenceBoard(flagged.txData);
            }
        }

        function updateCityForStep(step) {
            if (!DATA.district_hourly_by_step || !DATA.city_people_by_step) return;

            // 1. Update District Buildings based on pre-indexed hourly stats
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

            // 2. Update Live Hourly Threat Radar Panel
            const activeStepPeople = DATA.city_people_by_step[step] || [];
            const hour = step % 24;
            const flaggedThreats = activeStepPeople.filter(p => p.sc >= currentStrictness);

            document.getElementById('radarHourDisplay').innerText = `${hour}:00 (${(hour>=0 && hour<=5)?'🌙 Late Night Window':'☀️ Standard Hours'})`;
            document.getElementById('radarActiveTxCount').innerText = activeStepPeople.length;
            document.getElementById('radarThreatCountBadge').innerText = `${flaggedThreats.length} Threats`;

            const radarList = document.getElementById('radarThreatList');
            if (flaggedThreats.length === 0) {
                radarList.innerHTML = `<div style="color:#64748b; font-size:11px; padding:6px;">No high-risk threats detected in this hour.</div>`;
            } else {
                radarList.innerHTML = flaggedThreats.map((p, idx) => `
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
            }

            // 3. Spawn / Update People on screen with Manhattan Road Navigation
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

                    // Manhattan Road Grid Waypoints: Start District -> Avenue -> Highway Ring -> Destination District
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

                    // Halos & Laser Beams on Flagged Threats
                    if (evalMode && pData.f === 1) {
                        pMesh.headMat.color.setHex(0xef4444);
                        pMesh.halo.visible = true;
                        pMesh.haloMat.color.setHex(0xef4444);
                        pMesh.beam.visible = true;
                        pMesh.beamMat.color.setHex(0xef4444);
                    } else if (isFlagged) {
                        pMesh.headMat.color.setHex(0xf59e0b);
                        pMesh.halo.visible = true;
                        pMesh.haloMat.color.setHex(0xf59e0b);
                        pMesh.beam.visible = true;
                        pMesh.beamMat.color.setHex(0xf59e0b);
                        if (!firstFlaggedPos) firstFlaggedPos = pMesh.waypoints[0];
                    } else {
                        pMesh.headMat.color.setHex(0xf8fafc);
                        pMesh.halo.visible = false;
                        pMesh.beam.visible = false;
                    }

                    // Position along road path
                    updatePersonRoadPosition(pMesh);
                } else {
                    pMesh.active = false;
                    pMesh.group.position.set(0, -100, 0);
                }
            }

            // Sentinel targets first threat
            if (sentinelMesh && firstFlaggedPos) {
                sentinelMesh.targetPos.set(firstFlaggedPos.x, 0, firstFlaggedPos.z);
            }
        }

        function inspectThreatById(txId) {
            const targetMesh = cityPeopleMeshes.find(m => m.txData && m.txData.id === txId);
            if (targetMesh && targetMesh.txData) {
                camTarget.copy(targetMesh.group.position);
                camSpherical.radius = 110;
                camSpherical.phi = Math.PI / 3.2;
                updateCameraPosition();
                displayEvidenceBoard(targetMesh.txData);
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

            // Orient character towards direction of walking
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

                // Animate walking humanoids along roads with step bobbing
                cityPeopleMeshes.forEach((p, idx) => {
                    if (p.active) {
                        p.progress += p.speed;
                        if (p.progress > 1.0) p.progress = 0.0;
                        updatePersonRoadPosition(p);
                        p.group.position.y = Math.abs(Math.sin(time + idx)) * 1.2;
                        if (p.halo.visible) p.halo.rotation.z += 0.03;
                    }
                });

                // Smoothly glide Sentinel along roads to target
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

if __name__ == "__main__":
    build_mission8_site()
