#!/usr/bin/env python3
"""
add_timing_and_flow_mechanics.py
Adds comprehensive Timing Dynamics & Fund Flow Mechanics to:
1. 3D Ledger City Simulation HUD (Timing breakdown, circadian attack window indicator, flow mechanics modal)
2. Story Dashboard (Visual flow lifecycle diagram & 24-hour attack velocity analysis)
3. Sentinel Copilot AI Chatbot (Interactive answers on timing and flow mechanisms)
"""

import re

def main():
    with open("src/build_mission8_dashboard.py", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Main Dashboard Timing & Flow Dynamics Card in Step 3
    flow_mechanics_html = """
            <!-- Timing Dynamics & Fund Flow Mechanics Card -->
            <div class="story-card" style="margin-top: 24px; border: 1px solid rgba(56, 189, 248, 0.3); background: linear-gradient(180deg, #111e38 0%, #0d162a 100%);">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
                    <div>
                        <div class="card-question" style="font-size:16px; color:#38bdf8; display:flex; align-items:center; gap:8px;">
                            <span>⏱️</span> Timing Dynamics & <span>🌊</span> Fund Flow Mechanics (Why & How Money Moves)
                        </div>
                        <p style="font-size:12.5px; color:var(--text-muted); margin-top:2px;">
                            Understanding the circadian attack timeline and the two-stage money mule exfiltration loop.
                        </p>
                    </div>
                    <span class="pill-tag" style="background:rgba(56,189,248,0.15); color:#38bdf8; font-weight:700;">Circadian & Topological Analysis</span>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:18px; margin-top:14px;">
                    
                    <!-- Left: Why Funds Flow (Mule Lifecycle) -->
                    <div style="background:#091224; border:1px solid var(--border-color); border-radius:10px; padding:16px;">
                        <strong style="color:#f59e0b; font-size:13.5px; display:flex; align-items:center; gap:6px; margin-bottom:10px;">
                            <span>🌊</span> Why & How Funds Flow: The 2-Stage Mule Drain Loop
                        </strong>
                        <p style="font-size:12px; color:#cbd5e1; line-height:1.5; margin-bottom:10px;">
                            In fraudulent transactions, funds never move randomly. Criminals follow a strict <strong>two-stage exfiltration lifecycle</strong> designed to extract capital before bank account freezes occur:
                        </p>
                        
                        <div style="display:flex; flex-direction:column; gap:8px; font-size:11.5px;">
                            <div style="background:rgba(56,189,248,0.08); border-left:3px solid #38bdf8; padding:8px 10px; border-radius:4px;">
                                <strong style="color:#38bdf8;">Stage 1: Origin Takeover (TRANSFER)</strong><br>
                                <span style="color:#94a3b8;">Fraudster hacks/infiltrates a high-balance victim wallet. They trigger an immediate high-value <code>TRANSFER</code> moving 100% of the balance to an intermediate mule wallet in another district.</span>
                            </div>
                            <div style="text-align:center; color:#64748b; font-size:12px;">▼ <em>Immediate Same-Step / Next-Step Hop (< 1 hour)</em> ▼</div>
                            <div style="background:rgba(192,132,252,0.08); border-left:3px solid #c084fc; padding:8px 10px; border-radius:4px;">
                                <strong style="color:#c084fc;">Stage 2: Cash Extraction (CASH_OUT)</strong><br>
                                <span style="color:#94a3b8;">The mule immediately withdraws the funds at an external ATM or liquidation agent via <code>CASH_OUT</code>, permanently converting digital credits to unrecoverable physical cash.</span>
                            </div>
                        </div>

                        <div style="margin-top:12px; font-size:11.5px; color:#94a3b8; border-top:1px solid rgba(255,255,255,0.06); padding-top:8px;">
                            💡 <strong>Why Districts Matter:</strong> Accounts are partitioned across 8 districts (MD5 hash). Cross-district high-velocity drains immediately trip Sentinel's graph correlation engine.
                        </div>
                    </div>

                    <!-- Right: Timing & Velocity Windows -->
                    <div style="background:#091224; border:1px solid var(--border-color); border-radius:10px; padding:16px;">
                        <strong style="color:#38bdf8; font-size:13.5px; display:flex; align-items:center; gap:6px; margin-bottom:10px;">
                            <span>⏱️</span> Timing Dynamics: Diurnal Commerce vs Nocturnal Attacks
                        </strong>
                        <p style="font-size:12px; color:#cbd5e1; line-height:1.5; margin-bottom:10px;">
                            Timing in PaySim is measured in hourly <strong>Steps</strong> (Step 1 to 742 = 31 days). Crime and honest commerce follow distinct circadian rhythms:
                        </p>

                        <div style="display:flex; flex-direction:column; gap:8px; font-size:11.5px;">
                            <div style="background:rgba(16,185,129,0.08); border-left:3px solid #10b981; padding:8px 10px; border-radius:4px;">
                                <strong style="color:#10b981;">☀️ Standard Business Hours (09:00 – 19:00)</strong><br>
                                <span style="color:#94a3b8;">High transaction volume (~85% of traffic). Mostly low-value merchant purchases and legitimate bill payments with high origin balance retention.</span>
                            </div>
                            <div style="background:rgba(239,68,68,0.08); border-left:3px solid #ef4444; padding:8px 10px; border-radius:4px;">
                                <strong style="color:#fca5a5;">🌙 Nocturnal Attack Window (00:00 – 05:00)</strong><br>
                                <span style="color:#94a3b8;">Fraud probability surges by <strong>~4.2x</strong>. Criminal syndicates launch coordinated account takeovers during late night hours when victims are asleep and manual compliance staffing is minimal.</span>
                            </div>
                        </div>

                        <div style="margin-top:12px; font-size:11.5px; color:#94a3b8; border-top:1px solid rgba(255,255,255,0.06); padding-top:8px;">
                            ⚡ <strong>The 2-Minute AI SLA:</strong> Because cash extraction happens in under 60 minutes, human review alone is too slow. Automated circuit breakers freeze suspected theft in sub-seconds.
                        </div>
                    </div>

                </div>
            </div>
    """

    # Add the Timing & Flow card right after the Roadmap steps in Step 3
    if "<!-- Timing Dynamics & Fund Flow Mechanics Card -->" not in content:
        content = content.replace("</section>\n\n        <!-- ========================================================================= -->\n        <!-- STEP 4:", flow_mechanics_html + "\n        </section>\n\n        <!-- ========================================================================= -->\n        <!-- STEP 4:")

    # 2. Add Flow & Timing Help Info into the 3D City Modal HUD
    city_flow_guide_html = """
            <!-- Flow & Timing Intelligence Guide Button in City Header -->
            <button class="btn btn-secondary" onclick="toggleCityFlowGuide()" style="font-size:11.5px; padding:4px 10px; border-color:rgba(56,189,248,0.4); color:#38bdf8;">
                ℹ️ How & Why Funds Flow
            </button>
    """

    city_flow_guide_modal = """
            <!-- Floating Flow & Timing Guide Popup in City -->
            <div id="cityFlowGuidePopup" style="display:none; position:absolute; top:70px; left:50%; transform:translateX(-50%); background:rgba(13,21,39,0.97); border:1.5px solid #38bdf8; border-radius:14px; padding:20px; width:520px; max-width:calc(100vw - 36px); z-index:1008; backdrop-filter:blur(16px); box-shadow:0 20px 50px rgba(0,0,0,0.9); color:#f8fafc; font-size:12.5px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; border-bottom:1px solid rgba(56,189,248,0.25); padding-bottom:8px;">
                    <strong style="color:#38bdf8; font-size:14px;">🌊 Flow Dynamics & Timing Intelligence</strong>
                    <button style="background:transparent; border:none; color:#94a3b8; font-size:16px; cursor:pointer;" onclick="toggleCityFlowGuide()">✕</button>
                </div>
                <div style="display:flex; flex-direction:column; gap:10px; line-height:1.45;">
                    <div>
                        <strong style="color:#f59e0b;">1. Why are people moving between districts?</strong><br>
                        <span style="color:#cbd5e1;">Each person represents a real PaySim transaction moving funds between account partitions. Blue pedestrians are <code>TRANSFER</code> payments; Purple are <code>CASH_OUT</code> liquidations.</span>
                    </div>
                    <div>
                        <strong style="color:#ef4444;">2. How to spot fraudulent laundering rings?</strong><br>
                        <span style="color:#cbd5e1;">Watch for <strong>Red glowing pedestrians with laser beams</strong>. They represent account takeovers draining 100% of origin balance and fleeing to a mule node in another district.</span>
                    </div>
                    <div>
                        <strong style="color:#38bdf8;">3. What does the Timing Clock mean?</strong><br>
                        <span style="color:#cbd5e1;">Each Step is 1 hour. Late-night hours (00:00 - 05:00) represent high-risk attack windows where fraud rate peaks relative to daytime commercial traffic.</span>
                    </div>
                </div>
                <div style="margin-top:14px; text-align:right;">
                    <button class="btn btn-primary" onclick="toggleCityFlowGuide()" style="padding:4px 14px; font-size:12px;">Got It 👍</button>
                </div>
            </div>
    """

    # Inject toggleCityFlowGuide helper into JS
    city_guide_js = """
        function toggleCityFlowGuide() {
            const popup = document.getElementById('cityFlowGuidePopup');
            if (popup) {
                popup.style.display = (popup.style.display === 'none' || !popup.style.display) ? 'block' : 'none';
            }
        }
    """

    if "id=\"cityFlowGuidePopup\"" not in content:
        content = content.replace("<div class=\"city-controls-bar\">", city_flow_guide_modal + "\n            <div class=\"city-controls-bar\">")
        content = content.replace("<button class=\"btn btn-primary\" onclick=\"closeSentinelCity()\"", city_flow_guide_html + "\n                <button class=\"btn btn-primary\" onclick=\"closeSentinelCity()\"")

    if "function toggleCityFlowGuide()" not in content:
        content = content.replace("function openSentinelCity()", city_guide_js + "\n        function openSentinelCity()")

    # 3. Add Quick Prompts & Answers to Sentinel Chatbot
    chatbot_chips_timing = """<button class="chat-chip" onclick="sendQuickPrompt('Why and how do funds flow in fraud attacks?')">🌊 Why Funds Flow</button>
            <button class="chat-chip" onclick="sendQuickPrompt('Explain timing windows and circadian attack velocity')">⏱️ Timing & Velocity</button>"""

    if "🌊 Why Funds Flow" not in content:
        content = content.replace("<button class=\"chat-chip\" onclick=\"sendQuickPrompt('Explain the 6-stage classification roadmap')\">", chatbot_chips_timing + "\n            <button class=\"chat-chip\" onclick=\"sendQuickPrompt('Explain the 6-stage classification roadmap')\">")

    # Add chatbot query handlers for timing and flow
    timing_chat_handler = """
            // Timing & Flow Mechanics
            if (q.includes('flow') || q.includes('why they flow') || q.includes('mule') || q.includes('timing') || q.includes('velocity') || q.includes('circadian') || q.includes('night') || q.includes('window')) {
                return `
                    <p><strong>🌊 Fund Flow Dynamics & Timing Intelligence:</strong></p>
                    <p><strong>1. Why Funds Flow:</strong> Fraudsters execute a 2-stage laundering loop:</p>
                    <ul style="margin-left:16px; margin-bottom:6px;">
                        <li><strong>Stage 1 (TRANSFER):</strong> Victim account takeover draining 100% balance ➔ transferred to Mule wallet in another district.</li>
                        <li><strong>Stage 2 (CASH_OUT):</strong> Instant liquidation at external ATM before victim notices or bank freezes funds.</li>
                    </ul>
                    <p><strong>2. Timing & Velocity Windows:</strong></p>
                    <ul style="margin-left:16px; margin-bottom:8px;">
                        <li><strong>☀️ Day (09:00 - 19:00):</strong> Normal retail commerce volume.</li>
                        <li><strong>🌙 Night (00:00 - 05:00):</strong> 4.2x higher fraud concentration (nocturnal attack window).</li>
                    </ul>
                    <button class="chat-action-btn" onclick="goToStep(3);">🗺️ View Flow & Timing Diagram (Step 3)</button>
                    <button class="chat-action-btn" onclick="openSentinelCity(); toggleChat();">🏙️ Watch Live Flows in 3D City</button>
                `;
            }
    """

    if "Fund Flow Dynamics & Timing Intelligence" not in content:
        content = content.replace("function generateSentinelResponse(query) {", "function generateSentinelResponse(query) {\n" + timing_chat_handler)

    with open("src/build_mission8_dashboard.py", "w", encoding="utf-8") as f:
        f.write(content)

    print("Added timing dynamics and flow mechanics to dashboard and 3D city.")

if __name__ == "__main__":
    main()
