#!/usr/bin/env python3
"""
restore_perfect_city.py
Restores the full, crystal-clear 3D Ledger City simulation with:
1. Real-Time Live Situation Briefing Header (Top Center)
2. Hourly Threat Radar Feed (Top Left) with clickable suspect cards
3. Floating Forensic Evidence Dossier & Decision Stamp (Top Right)
4. Comprehensive Camera Controls & Scrubbers (Bottom Center)
5. Visual Legend and clarity aids so anyone instantly understands what is happening
"""

import re

def main():
    with open("src/build_mission8_dashboard.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Full City CSS
    full_city_css = """
        /* ========================================================================= */
        /* 3D LEDGER CITY (SENTINEL MODE) MODAL STYLES                              */
        /* ========================================================================= */
        .city-modal-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: #030712;
            z-index: 99999;
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
            font-size: 15px;
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
            width: 350px;
            max-width: calc(100vw - 30px);
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
            max-height: 220px;
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
            max-width: calc(100vw - 30px);
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
            top: 14px; left: 380px; right: 390px;
            background: rgba(13, 21, 39, 0.94);
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 12px;
            padding: 10px 16px;
            backdrop-filter: blur(14px);
            z-index: 1004;
            color: #f8fafc;
            box-shadow: 0 10px 30px rgba(0,0,0,0.7);
            font-size: 12px;
            line-height: 1.45;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        @media (max-width: 1280px) {
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
            padding: 4px 10px;
            border-radius: 6px;
            font-weight: 800;
            font-size: 11px;
            letter-spacing: 0.5px;
        }

        .stamp-block {
            background: rgba(239, 68, 68, 0.2);
            color: #fca5a5;
            border: 1px solid #ef4444;
        }

        .stamp-allow {
            background: rgba(16, 185, 129, 0.2);
            color: #6ee7b7;
            border: 1px solid #10b981;
        }

        .city-legend-bar {
            position: absolute;
            bottom: 64px; left: 50%;
            transform: translateX(-50%);
            background: rgba(13, 21, 39, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 4px 14px;
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 11px;
            color: #94a3b8;
            z-index: 1004;
            backdrop-filter: blur(8px);
        }
    """

    # Full City HTML Markup
    full_city_html = """
    <!-- ========================================================================= -->
    <!-- 3D LEDGER CITY (SENTINEL MODE) MODAL VIEW                                 -->
    <!-- ========================================================================= -->
    <div class="city-modal-overlay" id="cityModal">
        <!-- City Header Bar -->
        <div class="city-header">
            <div class="city-header-title">
                <span>🏙️</span>
                <span>LEDGER CITY // 3D SENTINEL THREAT RADAR</span>
            </div>

            <!-- Integrated Timeline & Step Replay Controls -->
            <div class="city-timeline-controls">
                <button class="btn btn-secondary" style="padding:4px 8px; font-size:11px;" onclick="cityStepChange(-1)" title="Previous Hour">◀ Prev</button>
                <button class="btn btn-secondary" style="padding:4px 10px; font-size:11px;" id="cityPlayBtn" onclick="togglePatrolPlay()">⏸️ Pause</button>
                <button class="btn btn-secondary" style="padding:4px 8px; font-size:11px;" onclick="cityStepChange(1)" title="Next Hour">Next ▶</button>
                
                <input type="range" id="cityStepSlider" min="334" max="742" value="334" style="width:130px;" oninput="scrubPatrol(this.value)">
                <span class="pill-badge" id="cityStepClock" style="font-size:11.5px; padding:3px 8px; background:rgba(56,189,248,0.15); color:#38bdf8;">Step 334 | 22:00</span>
            </div>

            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                <div style="display:flex; align-items:center; gap:6px; background:#080e1f; padding:4px 10px; border-radius:8px; border:1px solid rgba(56,189,248,0.2);">
                    <span style="font-size:11px; color:#94a3b8;">Strictness (θ):</span>
                    <strong style="color:#38bdf8; font-size:12px; font-family:var(--font-mono);" id="cityStrictnessBadge">0.50</strong>
                </div>
                <button class="btn btn-primary" onclick="closeSentinelCity()" style="font-size:12px; padding:6px 14px;">✕ Close City</button>
            </div>
        </div>

        <!-- Educational Disclaimer Banner -->
        <div class="city-disclaimer-banner">
            ⚠️ <strong>Live Financial Digital Twin:</strong> Replaying synthetic PaySim payment flows across 8 account hash districts. Red beams show autonomous AI circuit breaker fund freezes.
        </div>

        <!-- 3D WebGL Canvas Container -->
        <div class="city-canvas-container" id="cityCanvasContainer">
            <canvas id="cityFallback2D" style="display:none; width:100%; height:100%;"></canvas>

            <!-- Live City Situation Briefing (Top Center) -->
            <div class="city-situation-briefing" id="cityBriefingBox">
                <div class="briefing-pulse"></div>
                <div>
                    <strong style="color:#38bdf8; font-size:12px;">📡 LIVE SITUATION BRIEFING:</strong>
                    <span id="cityBriefingText" style="color:#e2e8f0; margin-left:4px;">Initializing payment stream...</span>
                </div>
            </div>

            <!-- Hourly Threat Briefing & Live Incident Feed (Top-Left) -->
            <div class="city-threat-radar-panel">
                <div style="font-weight:800; color:#38bdf8; font-size:13px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(56,189,248,0.2); padding-bottom:6px;">
                    <span>🚨 HOURLY THREAT RADAR</span>
                    <span class="pill-badge" id="radarThreatCountBadge" style="background:rgba(239,68,68,0.25); color:#fca5a5; font-size:11px;">0 Threats</span>
                </div>
                <div style="font-size:11.5px; color:#cbd5e1; line-height:1.4;">
                    <div>• <strong>Current Hour:</strong> <span id="radarHourDisplay" style="color:#38bdf8; font-weight:700;">22:00</span></div>
                    <div>• <strong>Active Transactions:</strong> <span id="radarActiveTxCount" style="font-weight:700;">0</span> moving</div>
                    <div>• <strong>Alarm Strictness (θ):</strong> <span id="cityStrictnessDisplay" style="color:#38bdf8; font-weight:700;">0.50</span></div>
                </div>

                <div style="font-weight:700; color:#f59e0b; font-size:11.5px; margin-top:4px;">
                    ⚡ Intercepted Threats (Click to Track):
                </div>
                <div class="threat-incident-list" id="radarThreatList">
                    <div style="color:#64748b; font-size:11px; padding:6px;">No high-risk threats detected in this hour.</div>
                </div>
            </div>

            <!-- Floating Evidence Board & Decision Stamp (Top Right) -->
            <div class="city-evidence-board" id="cityEvidenceBoard">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; border-bottom:1px solid rgba(56,189,248,0.25); padding-bottom:6px;">
                    <strong style="color:#38bdf8; font-size:13.5px;" id="ebTxId">🔍 Select Suspect</strong>
                    <button style="background:transparent; border:none; color:#94a3b8; cursor:pointer; font-size:16px;" onclick="closeEvidenceBoard()">✕</button>
                </div>
                <div style="font-size:12px; color:#cbd5e1; display:flex; flex-direction:column; gap:6px;" id="ebTxBody">
                    <div>Click any suspect or payment in the city or threat list to inspect forensic evidence...</div>
                </div>
            </div>

            <!-- Visual Legend Bar -->
            <div class="city-legend-bar">
                <span>🔴 <strong style="color:#ef4444;">Red:</strong> Theft / Auto-Quarantine</span>
                <span>⚠️ <strong style="color:#f59e0b;">Amber:</strong> Suspicious Alert</span>
                <span>🔵 <strong style="color:#38bdf8;">Cyan:</strong> Transfer</span>
                <span>🟣 <strong style="color:#c084fc;">Purple:</strong> Cash-Out</span>
            </div>

            <!-- City Interactive Controls Bar -->
            <div class="city-controls-bar">
                <button class="btn btn-secondary" onclick="setCameraPreset('top')" style="font-size:12px; padding:6px 12px;">🔭 Top Bird's Eye</button>
                <button class="btn btn-secondary" onclick="setCameraPreset('radar')" style="font-size:12px; padding:6px 12px;">🛰️ 90° Radar</button>
                <button class="btn btn-secondary" onclick="setCameraPreset('iso')" style="font-size:12px; padding:6px 12px;">📐 Isometric</button>
                <button class="btn btn-secondary" onclick="setCameraPreset('street')" style="font-size:12px; padding:6px 12px;">🚶 Street Cam</button>
                <button class="btn btn-secondary" onclick="focusOnNextThreat()" style="font-size:12px; padding:6px 12px; border-color:#ef4444; color:#fca5a5;">🎯 Focus Threat</button>
            </div>
        </div>
    </div>
    """

    # Replace old city styles
    content = re.sub(r'/\* 3D City Modal Styles \*/[\s\S]*?/\* ==========================================================================\n\s*SENTINEL AI COPILOT CHATBOT STYLES', full_city_css + "\n        /* SENTINEL AI COPILOT CHATBOT STYLES", content)
    
    # Also ensure the city modal HTML is replaced cleanly
    content = re.sub(r'<!-- 3D Ledger City Modal -->[\s\S]*?<!-- ========================================================================= -->\n\s*<!-- 3D LEDGER CITY', "<!-- 3D LEDGER CITY", content)
    content = re.sub(r'<!-- ========================================================================= -->\n\s*<!-- 3D LEDGER CITY \(SENTINEL MODE\) MODAL VIEW[\s\S]*?</div>\s*</div>\s*</div>', full_city_html.strip(), content)
    if "class=\"city-modal-overlay\"" not in content:
        content = content.replace("</main>", "</main>\n" + full_city_html)

    with open("src/build_mission8_dashboard.py", "w", encoding="utf-8") as f:
        f.write(content)

    print("Restored perfect 3D Ledger City modal markup and styling.")

if __name__ == "__main__":
    main()
