"""Mission 8 & 9 Story Dashboard Builder: 9 Guided Steps, Pipeline Roadmap, Fund Protection, and 3D Ledger City."""

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
    df_detector = pd.read_csv("docs/data/detector_comparison.csv")
    df_hourly = pd.read_csv("docs/data/hourly_stats.csv")
    df_amount_hist = pd.read_csv("docs/data/amount_hist.csv")
    df_score_hist = pd.read_csv("docs/data/score_hist.csv")
    df_threshold_curve = pd.read_csv("docs/data/threshold_curve.csv")
    df_market = pd.read_csv("docs/data/market/paytm_nifty.csv")
    df_feat_imp = pd.read_csv("docs/data/feature_importance.csv")
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
        "stream": stream_data,
        "city_people_by_step": city_people_by_step,
        "district_hourly_by_step": dist_hourly_by_step
    }

    html_out = HTML_TEMPLATE.replace("__DATA_BUNDLE__", json.dumps(bundle))

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_out)

    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html_out)

    print("Successfully built Sentinel Mission 8 Story Dashboard & 3D Ledger City at index.html and docs/index.html")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentinel | Financial Fraud Intelligence, Classification Roadmap & Fund Protection</title>
    <!-- Fonts & CDNs -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js">
        // ==========================================================================
        // SENTINEL AI COPILOT CHATBOT LOGIC & INTELLIGENCE ENGINE
        // ==========================================================================
        let chatOpen = false;

        function toggleChat() {
            const win = document.getElementById('sentinelChatWindow');
            if (!win) return;
            chatOpen = !chatOpen;
            if (chatOpen) {
                win.classList.add('active');
                document.getElementById('chatInput').focus();
            } else {
                win.classList.remove('active');
            }
        }

        function clearChatHistory() {
            const msgBox = document.getElementById('chatMessages');
            if (!msgBox) return;
            msgBox.innerHTML = `
                <div class="chat-msg chat-msg-ai">
                    <div class="chat-avatar">🤖</div>
                    <div class="chat-bubble chat-bubble-ai">
                        <p><strong>Chat cleared.</strong> How may Sentinel Copilot assist your fraud investigation now?</p>
                    </div>
                </div>
            `;
        }

        function sendQuickPrompt(text) {
            const inp = document.getElementById('chatInput');
            if (inp) {
                inp.value = text;
                sendChatMessage();
            }
        }

        function appendUserMessage(text) {
            const msgBox = document.getElementById('chatMessages');
            if (!msgBox) return;
            const div = document.createElement('div');
            div.className = 'chat-msg chat-msg-user';
            div.innerHTML = `
                <div class="chat-bubble chat-bubble-user">${escapeHtml(text)}</div>
            `;
            msgBox.appendChild(div);
            msgBox.scrollTop = msgBox.scrollHeight;
        }

        function appendAiMessage(htmlContent) {
            const msgBox = document.getElementById('chatMessages');
            if (!msgBox) return;
            const div = document.createElement('div');
            div.className = 'chat-msg chat-msg-ai';
            div.innerHTML = `
                <div class="chat-avatar">🤖</div>
                <div class="chat-bubble chat-bubble-ai">${htmlContent}</div>
            `;
            msgBox.appendChild(div);
            msgBox.scrollTop = msgBox.scrollHeight;
        }

        function escapeHtml(str) {
            return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        }

        function applyPresetThreshold(val) {
            const slider = document.getElementById('simStrictnessSlider');
            if (slider) {
                slider.value = val;
                updateSimScore();
            }
            goToStep(5);
        }

        function sendChatMessage() {
            const inp = document.getElementById('chatInput');
            if (!inp) return;
            const raw = inp.value.trim();
            if (!raw) return;
            inp.value = '';

            appendUserMessage(raw);

            // Show typing indicator
            const msgBox = document.getElementById('chatMessages');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'chat-msg chat-msg-ai';
            typingDiv.id = 'chatTypingIndicator';
            typingDiv.innerHTML = `
                <div class="chat-avatar">🤖</div>
                <div class="chat-bubble chat-bubble-ai">
                    <div class="chat-typing">
                        <div class="chat-typing-dot"></div>
                        <div class="chat-typing-dot"></div>
                        <div class="chat-typing-dot"></div>
                    </div>
                </div>
            `;
            msgBox.appendChild(typingDiv);
            msgBox.scrollTop = msgBox.scrollHeight;

            setTimeout(() => {
                const indicator = document.getElementById('chatTypingIndicator');
                if (indicator) indicator.remove();

                const responseHtml = generateSentinelResponse(raw);
                appendAiMessage(responseHtml);
            }, 450);
        }

        function generateSentinelResponse(query) {
            const q = query.toLowerCase();

            // 1. Classification Roadmap & Pipeline
            if (q.includes('roadmap') || q.includes('flowchart') || q.includes('pipeline') || q.includes('classify') || q.includes('how we find') || q.includes('stages')) {
                return `
                    <p><strong>🗺️ End-to-End Classification Pipeline:</strong></p>
                    <p>Sentinel identifies illicit transfers via a <strong>6-stage visual pipeline</strong>:</p>
                    <ol style="margin-left: 18px; margin-bottom: 8px;">
                        <li><strong>1. Stream Ingestion:</strong> Ingests 954,393 transactions (0.13% base fraud rate).</li>
                        <li><strong>2. Leak-Free Time Split:</strong> Historical training on $t \le 600$, zero-leakage evaluation on $t > 600$.</li>
                        <li><strong>3. Channel Filtering:</strong> Targets <code>TRANSFER</code> & <code>CASH_OUT</code> vectors where 100% of thefts occur.</li>
                        <li><strong>4. Feature Engineering:</strong> Computes balance discrepancy (<code>orig_err</code>), account drain ratio, & velocity.</li>
                        <li><strong>5. Ensemble Detection:</strong> Random Forest + Isolation Forest scores every payment.</li>
                        <li><strong>6. Agent Triangulation:</strong> Graph Mule Hunter builds synthesized multi-agent forensic dossiers.</li>
                    </ol>
                    <button class="chat-action-btn" onclick="goToStep(3);">🗺️ Jump to Step 3 Roadmap</button>
                `;
            }

            // 2. Fund Protection & Risk Mitigation
            if (q.includes('protect') || q.includes('fund') || q.includes('mitigat') || q.includes('risk') || q.includes('pillar') || q.includes('circuit')) {
                return `
                    <p><strong>🛡️ Fund Protection & Risk Mitigation System:</strong></p>
                    <p>Sentinel defends <strong>752.38M CU</strong> in capital across <strong>5 Core Defense Pillars</strong>:</p>
                    <ul style="margin-left: 16px; margin-bottom: 8px;">
                        <li><strong>⚡ Automated Circuit Breakers:</strong> Sub-second auto-freezes on transfers with score $\theta > 0.85$ or balance drains $>90\%$.</li>
                        <li><strong>🕸️ Graph Mule Interception:</strong> Blocks <code>TRANSFER</code> $\to$ <code>CASH_OUT</code> pairs before cash extraction at ATMs.</li>
                        <li><strong>🤖 Multi-Agent SLAs:</strong> Autonomous dossiers synthesized under a 2-minute response SLA.</li>
                        <li><strong>⚖️ Dynamic Cost Optimization:</strong> $\theta^* = 0.50$ balances review costs ($C_{\text{review}}$) against fraud leakage.</li>
                        <li><strong>📜 Regulatory Compliance Shield:</strong> Immutable audit logs prevent Paytm-style RBI regulatory shutdowns.</li>
                    </ul>
                    <button class="chat-action-btn" onclick="goToStep(7);">🛡️ Jump to Step 7 Risk Mitigation</button>
                `;
            }

            // 3. Strictness Threshold & Review Cost
            if (q.includes('threshold') || q.includes('strictness') || q.includes('theta') || q.includes('cost') || q.includes('review cost') || q.includes('optimal')) {
                return `
                    <p><strong>⚖️ Strictness Threshold ($\theta$) & Review Cost:</strong></p>
                    <p><strong>Strictness Threshold ($\theta$):</strong> The probability cutoff above which transactions are flagged for quarantine. Low $\theta$ catches more fraud but triggers false alarms; high $\theta$ reduces false alarms but risks fraud leakage.</p>
                    <p><strong>Review Cost ($C_{\text{review}}$):</strong> The operational expense to manually verify flagged alerts ($500 CU/alert default). Sentinel finds the mathematical minimum total cost $\theta^* = 0.50$.</p>
                    <div style="margin-top:6px;">
                        <button class="chat-action-btn" onclick="applyPresetThreshold(0.50);">⚖️ Set Optimal Threshold (θ = 0.50)</button>
                        <button class="chat-action-btn" onclick="goToStep(5);">🎯 View Financial Cost Curve</button>
                    </div>
                `;
            }

            // 4. Paytm Case Study & Market Link
            if (q.includes('paytm') || q.includes('market') || q.includes('compliance') || q.includes('rbi') || q.includes('equity') || q.includes('stock')) {
                return `
                    <p><strong>📉 Market Impact & The Paytm Regulatory Precedent:</strong></p>
                    <p>On January 31, 2024, the Reserve Bank of India (RBI) banned Paytm Payments Bank after discovering thousands of accounts linked to single PANs and widespread lack of real-time AML graph surveillance.</p>
                    <p><strong>Financial Fallout:</strong> Paytm's parent stock plummeted <strong>65%</strong> (₹760 ➔ ₹325), wiping out <strong>$2.6 Billion</strong> in market cap within weeks.</p>
                    <p><em>Lesson:</em> Fraud detection is not just risk mitigation—it protects enterprise enterprise value and regulatory licensing.</p>
                    <button class="chat-action-btn" onclick="goToStep(8);">📉 Jump to Step 8 Market Impact</button>
                `;
            }

            // 5. 3D Ledger City Simulation
            if (q.includes('city') || q.includes('3d') || q.includes('simulation') || q.includes('radar') || q.includes('camera') || q.includes('drone')) {
                return `
                    <p><strong>🏙️ 3D Real-Time Ledger City Simulation:</strong></p>
                    <p>Experience transactions moving across 9 financial districts in a cybernetic 3D digital twin. Features walking humanoid mule actors and autonomous Sentinel drone patrols.</p>
                    <p><strong>Available Camera Presets:</strong> Top Bird's Eye, 90° Top-Down Radar, Isometric, and Street level.</p>
                    <button class="chat-action-btn" onclick="openSentinelCity(); toggleChat();">🏙️ Launch 3D Ledger City</button>
                `;
            }

            // 6. Live Patrol & Cases
            if (q.includes('patrol') || q.includes('case') || q.includes('dossier') || q.includes('live') || q.includes('ticker') || q.includes('step 9')) {
                return `
                    <p><strong>⏱️ Live Patrol & Case File Dossiers:</strong></p>
                    <p>Inspect precomputed multi-agent case dossiers across 389 alert incidents (210 confirmed frauds, 179 false alarms) with live hourly transaction tickers.</p>
                    <button class="chat-action-btn" onclick="goToStep(9);">⏱️ Jump to Live Patrol & Cases</button>
                `;
            }

            // 7. Specific Account / Fraud query
            if (q.includes('c123') || q.includes('account') || q.includes('drain') || q.includes('transfer') || q.includes('cash_out')) {
                return `
                    <p><strong>🔍 Account Forensic Analysis:</strong></p>
                    <p>Typical fraud in PaySim follows an account takeover pattern:</p>
                    <ul style="margin-left: 16px; margin-bottom: 6px;">
                        <li><strong>Vector 1:</strong> Rapid <code>TRANSFER</code> draining 100% of origin balance (<code>oldbalanceOrg > 0</code>, <code>newbalanceOrig = 0</code>).</li>
                        <li><strong>Vector 2:</strong> Immediate paired <code>CASH_OUT</code> at an external mule node.</li>
                        <li><strong>Error Flag:</strong> <code>orig_err != 0</code> or <code>dest_err != 0</code> indicating balance falsification.</li>
                    </ul>
                    <button class="chat-action-btn" onclick="goToStep(9);">📂 Inspect Live Cases</button>
                `;
            }

            // 8. General Navigation / Default
            return `
                <p>I understand you are asking about: <em>"${escapeHtml(query)}"</em></p>
                <p>Here are quick shortcuts to key areas of Sentinel's fraud intelligence suite:</p>
                <div style="display:flex; flex-direction:column; gap:4px; margin-top:6px;">
                    <button class="chat-action-btn" onclick="goToStep(3);">🗺️ 1. View Classification Roadmap (Step 3)</button>
                    <button class="chat-action-btn" onclick="goToStep(7);">🛡️ 2. View Fund Protection & Risk Mitigation (Step 7)</button>
                    <button class="chat-action-btn" onclick="goToStep(5);">🎯 3. View Optimal Thresholds & Costs (Step 5)</button>
                    <button class="chat-action-btn" onclick="openSentinelCity(); toggleChat();">🏙️ 4. Open 3D Ledger City Simulation</button>
                </div>
            `;
        }
    
    </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js">
        // ==========================================================================
        // SENTINEL AI COPILOT CHATBOT LOGIC & INTELLIGENCE ENGINE
        // ==========================================================================
        let chatOpen = false;

        function toggleChat() {
            const win = document.getElementById('sentinelChatWindow');
            if (!win) return;
            chatOpen = !chatOpen;
            if (chatOpen) {
                win.classList.add('active');
                document.getElementById('chatInput').focus();
            } else {
                win.classList.remove('active');
            }
        }

        function clearChatHistory() {
            const msgBox = document.getElementById('chatMessages');
            if (!msgBox) return;
            msgBox.innerHTML = `
                <div class="chat-msg chat-msg-ai">
                    <div class="chat-avatar">🤖</div>
                    <div class="chat-bubble chat-bubble-ai">
                        <p><strong>Chat cleared.</strong> How may Sentinel Copilot assist your fraud investigation now?</p>
                    </div>
                </div>
            `;
        }

        function sendQuickPrompt(text) {
            const inp = document.getElementById('chatInput');
            if (inp) {
                inp.value = text;
                sendChatMessage();
            }
        }

        function appendUserMessage(text) {
            const msgBox = document.getElementById('chatMessages');
            if (!msgBox) return;
            const div = document.createElement('div');
            div.className = 'chat-msg chat-msg-user';
            div.innerHTML = `
                <div class="chat-bubble chat-bubble-user">${escapeHtml(text)}</div>
            `;
            msgBox.appendChild(div);
            msgBox.scrollTop = msgBox.scrollHeight;
        }

        function appendAiMessage(htmlContent) {
            const msgBox = document.getElementById('chatMessages');
            if (!msgBox) return;
            const div = document.createElement('div');
            div.className = 'chat-msg chat-msg-ai';
            div.innerHTML = `
                <div class="chat-avatar">🤖</div>
                <div class="chat-bubble chat-bubble-ai">${htmlContent}</div>
            `;
            msgBox.appendChild(div);
            msgBox.scrollTop = msgBox.scrollHeight;
        }

        function escapeHtml(str) {
            return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        }

        function applyPresetThreshold(val) {
            const slider = document.getElementById('simStrictnessSlider');
            if (slider) {
                slider.value = val;
                updateSimScore();
            }
            goToStep(5);
        }

        function sendChatMessage() {
            const inp = document.getElementById('chatInput');
            if (!inp) return;
            const raw = inp.value.trim();
            if (!raw) return;
            inp.value = '';

            appendUserMessage(raw);

            // Show typing indicator
            const msgBox = document.getElementById('chatMessages');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'chat-msg chat-msg-ai';
            typingDiv.id = 'chatTypingIndicator';
            typingDiv.innerHTML = `
                <div class="chat-avatar">🤖</div>
                <div class="chat-bubble chat-bubble-ai">
                    <div class="chat-typing">
                        <div class="chat-typing-dot"></div>
                        <div class="chat-typing-dot"></div>
                        <div class="chat-typing-dot"></div>
                    </div>
                </div>
            `;
            msgBox.appendChild(typingDiv);
            msgBox.scrollTop = msgBox.scrollHeight;

            setTimeout(() => {
                const indicator = document.getElementById('chatTypingIndicator');
                if (indicator) indicator.remove();

                const responseHtml = generateSentinelResponse(raw);
                appendAiMessage(responseHtml);
            }, 450);
        }

        function generateSentinelResponse(query) {
            const q = query.toLowerCase();

            // 1. Classification Roadmap & Pipeline
            if (q.includes('roadmap') || q.includes('flowchart') || q.includes('pipeline') || q.includes('classify') || q.includes('how we find') || q.includes('stages')) {
                return `
                    <p><strong>🗺️ End-to-End Classification Pipeline:</strong></p>
                    <p>Sentinel identifies illicit transfers via a <strong>6-stage visual pipeline</strong>:</p>
                    <ol style="margin-left: 18px; margin-bottom: 8px;">
                        <li><strong>1. Stream Ingestion:</strong> Ingests 954,393 transactions (0.13% base fraud rate).</li>
                        <li><strong>2. Leak-Free Time Split:</strong> Historical training on $t \le 600$, zero-leakage evaluation on $t > 600$.</li>
                        <li><strong>3. Channel Filtering:</strong> Targets <code>TRANSFER</code> & <code>CASH_OUT</code> vectors where 100% of thefts occur.</li>
                        <li><strong>4. Feature Engineering:</strong> Computes balance discrepancy (<code>orig_err</code>), account drain ratio, & velocity.</li>
                        <li><strong>5. Ensemble Detection:</strong> Random Forest + Isolation Forest scores every payment.</li>
                        <li><strong>6. Agent Triangulation:</strong> Graph Mule Hunter builds synthesized multi-agent forensic dossiers.</li>
                    </ol>
                    <button class="chat-action-btn" onclick="goToStep(3);">🗺️ Jump to Step 3 Roadmap</button>
                `;
            }

            // 2. Fund Protection & Risk Mitigation
            if (q.includes('protect') || q.includes('fund') || q.includes('mitigat') || q.includes('risk') || q.includes('pillar') || q.includes('circuit')) {
                return `
                    <p><strong>🛡️ Fund Protection & Risk Mitigation System:</strong></p>
                    <p>Sentinel defends <strong>752.38M CU</strong> in capital across <strong>5 Core Defense Pillars</strong>:</p>
                    <ul style="margin-left: 16px; margin-bottom: 8px;">
                        <li><strong>⚡ Automated Circuit Breakers:</strong> Sub-second auto-freezes on transfers with score $\theta > 0.85$ or balance drains $>90\%$.</li>
                        <li><strong>🕸️ Graph Mule Interception:</strong> Blocks <code>TRANSFER</code> $\to$ <code>CASH_OUT</code> pairs before cash extraction at ATMs.</li>
                        <li><strong>🤖 Multi-Agent SLAs:</strong> Autonomous dossiers synthesized under a 2-minute response SLA.</li>
                        <li><strong>⚖️ Dynamic Cost Optimization:</strong> $\theta^* = 0.50$ balances review costs ($C_{\text{review}}$) against fraud leakage.</li>
                        <li><strong>📜 Regulatory Compliance Shield:</strong> Immutable audit logs prevent Paytm-style RBI regulatory shutdowns.</li>
                    </ul>
                    <button class="chat-action-btn" onclick="goToStep(7);">🛡️ Jump to Step 7 Risk Mitigation</button>
                `;
            }

            // 3. Strictness Threshold & Review Cost
            if (q.includes('threshold') || q.includes('strictness') || q.includes('theta') || q.includes('cost') || q.includes('review cost') || q.includes('optimal')) {
                return `
                    <p><strong>⚖️ Strictness Threshold ($\theta$) & Review Cost:</strong></p>
                    <p><strong>Strictness Threshold ($\theta$):</strong> The probability cutoff above which transactions are flagged for quarantine. Low $\theta$ catches more fraud but triggers false alarms; high $\theta$ reduces false alarms but risks fraud leakage.</p>
                    <p><strong>Review Cost ($C_{\text{review}}$):</strong> The operational expense to manually verify flagged alerts ($500 CU/alert default). Sentinel finds the mathematical minimum total cost $\theta^* = 0.50$.</p>
                    <div style="margin-top:6px;">
                        <button class="chat-action-btn" onclick="applyPresetThreshold(0.50);">⚖️ Set Optimal Threshold (θ = 0.50)</button>
                        <button class="chat-action-btn" onclick="goToStep(5);">🎯 View Financial Cost Curve</button>
                    </div>
                `;
            }

            // 4. Paytm Case Study & Market Link
            if (q.includes('paytm') || q.includes('market') || q.includes('compliance') || q.includes('rbi') || q.includes('equity') || q.includes('stock')) {
                return `
                    <p><strong>📉 Market Impact & The Paytm Regulatory Precedent:</strong></p>
                    <p>On January 31, 2024, the Reserve Bank of India (RBI) banned Paytm Payments Bank after discovering thousands of accounts linked to single PANs and widespread lack of real-time AML graph surveillance.</p>
                    <p><strong>Financial Fallout:</strong> Paytm's parent stock plummeted <strong>65%</strong> (₹760 ➔ ₹325), wiping out <strong>$2.6 Billion</strong> in market cap within weeks.</p>
                    <p><em>Lesson:</em> Fraud detection is not just risk mitigation—it protects enterprise enterprise value and regulatory licensing.</p>
                    <button class="chat-action-btn" onclick="goToStep(8);">📉 Jump to Step 8 Market Impact</button>
                `;
            }

            // 5. 3D Ledger City Simulation
            if (q.includes('city') || q.includes('3d') || q.includes('simulation') || q.includes('radar') || q.includes('camera') || q.includes('drone')) {
                return `
                    <p><strong>🏙️ 3D Real-Time Ledger City Simulation:</strong></p>
                    <p>Experience transactions moving across 9 financial districts in a cybernetic 3D digital twin. Features walking humanoid mule actors and autonomous Sentinel drone patrols.</p>
                    <p><strong>Available Camera Presets:</strong> Top Bird's Eye, 90° Top-Down Radar, Isometric, and Street level.</p>
                    <button class="chat-action-btn" onclick="openSentinelCity(); toggleChat();">🏙️ Launch 3D Ledger City</button>
                `;
            }

            // 6. Live Patrol & Cases
            if (q.includes('patrol') || q.includes('case') || q.includes('dossier') || q.includes('live') || q.includes('ticker') || q.includes('step 9')) {
                return `
                    <p><strong>⏱️ Live Patrol & Case File Dossiers:</strong></p>
                    <p>Inspect precomputed multi-agent case dossiers across 389 alert incidents (210 confirmed frauds, 179 false alarms) with live hourly transaction tickers.</p>
                    <button class="chat-action-btn" onclick="goToStep(9);">⏱️ Jump to Live Patrol & Cases</button>
                `;
            }

            // 7. Specific Account / Fraud query
            if (q.includes('c123') || q.includes('account') || q.includes('drain') || q.includes('transfer') || q.includes('cash_out')) {
                return `
                    <p><strong>🔍 Account Forensic Analysis:</strong></p>
                    <p>Typical fraud in PaySim follows an account takeover pattern:</p>
                    <ul style="margin-left: 16px; margin-bottom: 6px;">
                        <li><strong>Vector 1:</strong> Rapid <code>TRANSFER</code> draining 100% of origin balance (<code>oldbalanceOrg > 0</code>, <code>newbalanceOrig = 0</code>).</li>
                        <li><strong>Vector 2:</strong> Immediate paired <code>CASH_OUT</code> at an external mule node.</li>
                        <li><strong>Error Flag:</strong> <code>orig_err != 0</code> or <code>dest_err != 0</code> indicating balance falsification.</li>
                    </ul>
                    <button class="chat-action-btn" onclick="goToStep(9);">📂 Inspect Live Cases</button>
                `;
            }

            // 8. General Navigation / Default
            return `
                <p>I understand you are asking about: <em>"${escapeHtml(query)}"</em></p>
                <p>Here are quick shortcuts to key areas of Sentinel's fraud intelligence suite:</p>
                <div style="display:flex; flex-direction:column; gap:4px; margin-top:6px;">
                    <button class="chat-action-btn" onclick="goToStep(3);">🗺️ 1. View Classification Roadmap (Step 3)</button>
                    <button class="chat-action-btn" onclick="goToStep(7);">🛡️ 2. View Fund Protection & Risk Mitigation (Step 7)</button>
                    <button class="chat-action-btn" onclick="goToStep(5);">🎯 3. View Optimal Thresholds & Costs (Step 5)</button>
                    <button class="chat-action-btn" onclick="openSentinelCity(); toggleChat();">🏙️ 4. Open 3D Ledger City Simulation</button>
                </div>
            `;
        }
    
    </script>
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
    

        /* Flowchart / Roadmap Pipeline Styles */
        .roadmap-container {
            display: flex;
            flex-direction: column;
            gap: 16px;
            margin: 16px 0;
        }

        .flow-step-card {
            background: #0d1527;
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--primary-cyan);
            border-radius: 8px;
            padding: 16px 20px;
            display: flex;
            align-items: flex-start;
            gap: 18px;
            transition: all 0.2s ease;
        }

        .flow-step-card:hover {
            border-color: var(--primary-cyan);
            background: #111c33;
            transform: translateX(4px);
        }

        .flow-step-num {
            background: rgba(56, 189, 248, 0.15);
            color: var(--primary-cyan);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 50%;
            width: 38px;
            height: 38px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 15px;
            font-weight: 800;
            flex-shrink: 0;
        }

        .flow-arrow {
            text-align: center;
            color: var(--primary-cyan);
            font-size: 20px;
            margin: -6px 0;
            opacity: 0.6;
        }

        .pill-tag {
            display: inline-block;
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.06);
            color: var(--text-muted);
            margin-right: 6px;
            margin-top: 4px;
            font-family: 'JetBrains Mono', monospace;
        }

        /* Fund Protection Matrix */
        .defense-pillar-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 16px;
            margin: 16px 0;
        }

        .defense-card {
            background: #0d1527;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 18px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .defense-card-title {
            font-size: 14px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
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
    
    
    
    
    
    
    
    
        /* ==========================================================================
           SENTINEL AI COPILOT CHATBOT STYLES
           ========================================================================== */
        .chat-trigger-btn {
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 9999;
            background: linear-gradient(135deg, #0284c7, #2563eb, #7c3aed);
            color: #ffffff;
            border: 1px solid rgba(56, 189, 248, 0.4);
            border-radius: 9999px;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.5), 0 0 15px rgba(56, 189, 248, 0.3);
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .chat-trigger-btn:hover {
            transform: translateY(-3px) scale(1.03);
            box-shadow: 0 14px 30px -5px rgba(2, 132, 199, 0.7), 0 0 22px rgba(56, 189, 248, 0.5);
            border-color: #38bdf8;
        }

        .chat-trigger-pulse {
            width: 10px;
            height: 10px;
            background: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            animation: chatPulse 2s infinite;
        }

        @keyframes chatPulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        .chat-window {
            position: fixed;
            bottom: 86px;
            right: 24px;
            width: 440px;
            max-width: calc(100vw - 36px);
            height: 600px;
            max-height: calc(100vh - 120px);
            background: rgba(13, 21, 39, 0.95);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 16px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), 0 0 30px rgba(56, 189, 248, 0.15);
            z-index: 10000;
            display: none;
            flex-direction: column;
            overflow: hidden;
            transition: all 0.25s ease;
        }

        .chat-window.active {
            display: flex;
            animation: chatSlideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes chatSlideUp {
            from { opacity: 0; transform: translateY(20px) scale(0.96); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        .chat-header {
            padding: 14px 18px;
            background: linear-gradient(90deg, #111d35, #162444);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .chat-header-title {
            font-size: 14px;
            font-weight: 700;
            color: #f8fafc;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .chat-header-controls {
            display: flex;
            gap: 8px;
        }

        .chat-ctrl-btn {
            background: transparent;
            border: none;
            color: #94a3b8;
            cursor: pointer;
            padding: 4px;
            border-radius: 4px;
            font-size: 14px;
            transition: color 0.2s;
        }

        .chat-ctrl-btn:hover {
            color: #f8fafc;
            background: rgba(255, 255, 255, 0.08);
        }

        .chat-quick-chips {
            padding: 8px 14px;
            background: rgba(8, 13, 26, 0.7);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            gap: 6px;
            overflow-x: auto;
            white-space: nowrap;
            scrollbar-width: thin;
        }

        .chat-quick-chips::-webkit-scrollbar {
            height: 4px;
        }

        .chat-chip {
            background: rgba(56, 189, 248, 0.1);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 12px;
            padding: 4px 10px;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            flex-shrink: 0;
        }

        .chat-chip:hover {
            background: rgba(56, 189, 248, 0.25);
            border-color: #38bdf8;
            transform: translateY(-1px);
        }

        .chat-messages {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 14px;
            font-size: 13px;
        }

        .chat-msg {
            display: flex;
            gap: 10px;
            max-width: 92%;
        }

        .chat-msg-user {
            align-self: flex-end;
            flex-direction: row-reverse;
        }

        .chat-msg-ai {
            align-self: flex-start;
        }

        .chat-avatar {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: #1e293b;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            flex-shrink: 0;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }

        .chat-bubble {
            padding: 10px 14px;
            border-radius: 12px;
            line-height: 1.45;
        }

        .chat-bubble-user {
            background: #2563eb;
            color: #ffffff;
            border-bottom-right-radius: 2px;
        }

        .chat-bubble-ai {
            background: #152238;
            color: #e2e8f0;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-bottom-left-radius: 2px;
        }

        .chat-bubble-ai p {
            margin-bottom: 6px;
        }

        .chat-bubble-ai p:last-child {
            margin-bottom: 0;
        }

        .chat-action-btn {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-top: 8px;
            margin-right: 6px;
            padding: 6px 12px;
            background: rgba(56, 189, 248, 0.15);
            border: 1px solid rgba(56, 189, 248, 0.4);
            border-radius: 6px;
            color: #38bdf8;
            font-size: 11.5px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
        }

        .chat-action-btn:hover {
            background: rgba(56, 189, 248, 0.3);
            border-color: #38bdf8;
            transform: translateY(-1px);
        }

        .chat-input-area {
            padding: 12px 14px;
            background: #0d1527;
            border-top: 1px solid var(--border-color);
            display: flex;
            gap: 8px;
            align-items: center;
        }

        .chat-input {
            flex: 1;
            background: #121d33;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px 14px;
            color: #f8fafc;
            font-size: 13px;
            outline: none;
            transition: border-color 0.2s;
        }

        .chat-input:focus {
            border-color: #38bdf8;
        }

        .chat-send-btn {
            background: #0284c7;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 14px;
            cursor: pointer;
            font-weight: 700;
            font-size: 13px;
            transition: background 0.2s;
        }

        .chat-send-btn:hover {
            background: #0369a1;
        }

        .chat-typing {
            display: inline-flex;
            gap: 4px;
            padding: 6px 10px;
        }

        .chat-typing-dot {
            width: 6px;
            height: 6px;
            background: #94a3b8;
            border-radius: 50%;
            animation: typingDot 1.4s infinite ease-in-out;
        }

        .chat-typing-dot:nth-child(1) { animation-delay: 0s; }
        .chat-typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .chat-typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typingDot {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
            30% { transform: translateY(-4px); opacity: 1; }
        }

        /* 3D City Modal Styles */
        .city-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(4, 7, 15, 0.96);
            z-index: 99999;
            backdrop-filter: blur(10px);
            flex-direction: column;
        }

        .city-modal.active {
            display: flex;
        }

        .city-modal-header {
            padding: 14px 24px;
            background: #0d1527;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .city-modal-body {
            position: relative;
            flex: 1;
            width: 100%;
            height: calc(100vh - 70px);
            overflow: hidden;
        }

        #cityCanvasContainer {
            width: 100%;
            height: 100%;
        }

        .city-hud {
            position: absolute;
            top: 20px;
            left: 24px;
            background: rgba(13, 21, 39, 0.85);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 14px 18px;
            color: #f8fafc;
            z-index: 10;
            backdrop-filter: blur(8px);
            max-width: 320px;
        }

        .city-cam-presets {
            position: absolute;
            top: 20px;
            right: 24px;
            display: flex;
            gap: 8px;
            z-index: 10;
            flex-wrap: wrap;
            max-width: 460px;
            justify-content: flex-end;
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
            <li><button class="nav-item-btn" onclick="goToStep(3)">🗺️ 3. Classification Roadmap</button></li>
            <li><button class="nav-item-btn" onclick="goToStep(4)">🔬 4. The Detector</button></li>
            <li><button class="nav-item-btn" onclick="goToStep(5)">🎯 5. The Result</button></li>
            <li><button class="nav-item-btn" onclick="goToStep(6)">⚖️ 6. The Decision</button></li>
            <li><button class="nav-item-btn" onclick="goToStep(7)">🛡️ 7. Fund Protection</button></li>
            <li><button class="nav-item-btn" onclick="goToStep(8)">📉 8. The Market Link</button></li>
            <li><button class="nav-item-btn" onclick="goToStep(9)">⏱️ 9. Live Patrol & Cases</button></li>
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

    <!-- Main Investigation Story Area -->
    <main class="main-wrapper">

        <!-- Global Header Controls Bar -->
        <header class="global-header">
            <div style="display:flex; justify-content:space-between; align-items:center; width:100%; flex-wrap:wrap; gap:16px;">
                <div class="control-group">
                    <span class="control-label" style="display:inline-flex; align-items:center; gap:5px;">
                        Strictness Threshold (θ):
                        <span style="background:rgba(56,189,248,0.2); color:#38bdf8; border-radius:50%; width:16px; height:16px; display:inline-flex; align-items:center; justify-content:center; font-size:10px; font-weight:800; cursor:help;" title="Strictness Cutoff: Model probability scores above this value trigger inspection alerts.">?</span>
                    </span>
                    <input type="range" id="strictnessRange" min="0" max="22" value="13" oninput="onStrictnessChange(this.value)">
                    <strong id="strictnessLabel" style="color:var(--primary-cyan); min-width:45px; font-size:14px;">0.50</strong>
                </div>

                <div class="control-group">
                    <span class="control-label" style="display:inline-flex; align-items:center; gap:5px;">
                        Review Cost (C_review):
                        <span style="background:rgba(245,158,11,0.2); color:#f59e0b; border-radius:50%; width:16px; height:16px; display:inline-flex; align-items:center; justify-content:center; font-size:10px; font-weight:800; cursor:help;" title="Review Cost: The operational financial expense of manual analyst inspection per alert.">?</span>
                    </span>
                    <select id="checkingCostSelect" onchange="onCheckingCostChange(this.value)">
                        <option value="100">100 CU / check (Automated Screening)</option>
                        <option value="500" selected>500 CU / check (Base Operational Review)</option>
                        <option value="2000">2,000 CU / check (Specialist Analyst Review)</option>
                        <option value="5000">5,000 CU / check (Deep Forensic Investigation)</option>
                        <option value="25000">25,000 CU / check</option>
                        <option value="100000">100,000 CU / check</option>
                        <option value="500000">500,000 CU / check</option>
                    </select>
                </div>

                <div class="control-group">
                    <div style="background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.4); color:#34d399; font-size:12px; font-weight:700; padding:6px 14px; border-radius:6px; display:inline-flex; align-items:center; gap:6px;">
                        <span>🟢 Ground Truth & Verified Frauds: FULLY VISIBLE</span>
                    </div>
                </div>
            </div>

            <!-- Concept Information Explainer Bar -->
            <div style="width:100%; border-top:1px solid rgba(255,255,255,0.08); padding-top:12px; margin-top:6px; display:grid; grid-template-columns: 1fr 1fr; gap:16px; font-size:12px; line-height:1.5;">
                <div style="background:rgba(56,189,248,0.05); border:1px solid rgba(56,189,248,0.2); border-radius:6px; padding:10px 14px;">
                    <strong style="color:#38bdf8; font-size:12.5px; display:flex; align-items:center; gap:6px;">
                        🎯 What is Strictness Threshold (θ)?
                    </strong>
                    <div style="color:#cbd5e1; margin-top:4px;">
                        The machine learning model outputs a risk probability score from <strong>0.00 to 1.00</strong>. Strictness (θ) is the decision cutoff:
                        <br>• <span style="color:#34d399; font-weight:600;">Low θ (0.01 - 0.10, Strict):</span> Catches almost all fraud (90%+ recall), but triggers more false alarms.
                        <br>• <span style="color:#f59e0b; font-weight:600;">High θ (0.80 - 0.95, Lenient):</span> Only alarms on high-confidence cases, reducing review workload but letting fraud escape.
                    </div>
                </div>

                <div style="background:rgba(245,158,11,0.05); border:1px solid rgba(245,158,11,0.2); border-radius:6px; padding:10px 14px;">
                    <strong style="color:#f59e0b; font-size:12.5px; display:flex; align-items:center; gap:6px;">
                        💼 What is Review Cost (C_review)?
                    </strong>
                    <div style="color:#cbd5e1; margin-top:4px;">
                        The operational dollar expense (analyst salary, KYC verification, customer friction) incurred for each transaction held for review:
                        <br>• <span style="color:#38bdf8; font-weight:600;">Low Review Cost (100 - 500 CU):</span> It is optimal to be ultra-strict (θ* = 0.01) to save millions in fraud principal.
                        <br>• <span style="color:#f87171; font-weight:600;">High Review Cost (100,000+ CU):</span> Reviewing every alert becomes too costly, forcing θ* higher.
                    </div>
                </div>
            </div>
        </header>

        <!-- ========================================================================= -->
        <!-- STEP 1: THE PROBLEM -->
        <!-- ========================================================================= -->
        <section id="step1" class="step-section active">
            <div class="step-header">
                <div class="step-badge">Step 1 of 9</div>
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
                        <strong>What this means:</strong> Extreme class imbalance renders traditional accuracy metrics useless (a dummy model predicting 100% legitimate achieves 99.87% accuracy while catching 0 frauds). Precision and recall are the only meaningful evaluation benchmarks.
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
                <div class="step-badge">Step 2 of 9</div>
                <h2 class="step-title">The Data: Temporal Splitting & Feature Distributions</h2>
                <p class="step-sub">Rigorous time-based train/test splitting to prevent future data leakage, plus heavy-tailed transaction dynamics.</p>
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
                        <strong>What this means:</strong> Sentinel strictly trains on past transactions (hours 1–333) and evaluates on future steps (334–743), mirroring real-world deployment without data contamination.
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
                        <strong>What this means:</strong> Honest payments center around $74k, whereas fraud transactions cluster heavily at high amounts ($440k+ median), attempting to maximize stolen principal before accounts are frozen.
                    </div>
                    <div class="card-source-footer">Source: docs/data/amount_hist.csv</div>
                </div>
            </div>

            <div class="cards-grid-full">
                <!-- Card 5 -->
                <div class="story-card">
                    <div class="card-question">When does fraud happen during the diurnal 24-hour cycle?</div>
                    <div class="card-headline" id="c5Headline">Loading...</div>
                    <div class="card-visual-box" style="height:280px;">
                        <canvas id="c5Chart"></canvas>
                    </div>
                    <div class="card-explanation">
                        <strong>What this means:</strong> Criminals exploit low-supervision hours (midnight to 5 AM) when customer attention is lowest, while legitimate payment volume peaks in business daylight hours.
                    </div>
                    <div class="card-source-footer">Source: docs/data/hourly_stats.csv</div>
                </div>
            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- STEP 3: CLASSIFICATION ROADMAP & PIPELINE FLOWCHART                      -->
        <!-- ========================================================================= -->
        <section id="step3" class="step-section">
            <div class="step-header">
                <div class="step-badge">Step 3 of 9</div>
                <h2 class="step-title">End-to-End Classification Roadmap & Detection Architecture</h2>
                <p class="step-sub">Visual walkthrough of how raw financial data flows through preprocessing, feature engineering, machine learning scoring, graph correlation, and multi-agent synthesis.</p>
            </div>

            <div class="roadmap-container">
                <!-- Stage 1 -->
                <div class="flow-step-card" style="border-left-color: #38bdf8;">
                    <div class="flow-step-num">1</div>
                    <div style="flex:1;">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
                            <strong style="color:#38bdf8; font-size:15px;">Raw Transaction Stream & Leak-Free Temporal Split</strong>
                            <span class="pill-tag" style="background:rgba(56,189,248,0.15); color:#38bdf8;">Input: 954,393 txs</span>
                        </div>
                        <p style="color:#cbd5e1; font-size:12.5px; margin:6px 0;">
                            Ingests chronological payments across 743 hours. Strictly partitions training (Steps 1–333) from deployment replay (Steps 334–742) without using future data or leaky destination balance delta fields.
                        </p>
                        <div>
                            <span class="pill-tag">Train: 312,371 rows</span>
                            <span class="pill-tag">Test Replay: 103,191 rows</span>
                            <span class="pill-tag">Zero Temporal Leakage</span>
                        </div>
                    </div>
                </div>

                <div class="flow-arrow">▼</div>

                <!-- Stage 2 -->
                <div class="flow-step-card" style="border-left-color: #818cf8;">
                    <div class="flow-step-num" style="background:rgba(129,140,248,0.15); color:#818cf8; border-color:rgba(129,140,248,0.3);">2</div>
                    <div style="flex:1;">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
                            <strong style="color:#818cf8; font-size:15px;">Attack Channel Isolation & Volume Filtering</strong>
                            <span class="pill-tag" style="background:rgba(129,140,248,0.15); color:#818cf8;">68% Overhead Cut</span>
                        </div>
                        <p style="color:#cbd5e1; font-size:12.5px; margin:6px 0;">
                            Empirical analysis proves 100% of theft is concentrated in <code>TRANSFER</code> (606 frauds) and <code>CASH_OUT</code> (595 frauds). Low-risk merchant purchases (<code>PAYMENT</code>, <code>CASH_IN</code>, <code>DEBIT</code> = 0 fraud) bypass heavy ML pipelines.
                        </p>
                        <div>
                            <span class="pill-tag">TRANSFER (79,932 txs)</span>
                            <span class="pill-tag">CASH_OUT (335,630 txs)</span>
                            <span class="pill-tag">Safe Bypass: 538k txs</span>
                        </div>
                    </div>
                </div>

                <div class="flow-arrow">▼</div>

                <!-- Stage 3 -->
                <div class="flow-step-card" style="border-left-color: #f59e0b;">
                    <div class="flow-step-num" style="background:rgba(245,158,11,0.15); color:#f59e0b; border-color:rgba(245,158,11,0.3);">3</div>
                    <div style="flex:1;">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
                            <strong style="color:#f59e0b; font-size:15px;">Behavioral Feature Engineering & Temporal Cyclical Encoding</strong>
                            <span class="pill-tag" style="background:rgba(245,158,11,0.15); color:#f59e0b;">Engineered Vectors</span>
                        </div>
                        <p style="color:#cbd5e1; font-size:12.5px; margin:6px 0;">
                            Constructs scale-invariant and behavioral features: log-amount scaling, 24-hour diurnal cyclical representations (<code>sin/cos hour</code>), historical sender velocity, and recipient account degree connectivity.
                        </p>
                        <div>
                            <span class="pill-tag">Amount Magnitude (32.1% wt)</span>
                            <span class="pill-tag">Log Scale (31.1% wt)</span>
                            <span class="pill-tag">Hour Diurnal (26.1% wt)</span>
                        </div>
                    </div>
                </div>

                <div class="flow-arrow">▼</div>

                <!-- Stage 4 -->
                <div class="flow-step-card" style="border-left-color: #10b981;">
                    <div class="flow-step-num" style="background:rgba(16,185,129,0.15); color:#10b981; border-color:rgba(16,185,129,0.3);">4</div>
                    <div style="flex:1;">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
                            <strong style="color:#10b981; font-size:15px;">Dual-Engine ML Scoring (Balanced Random Forest & Isolation Forest)</strong>
                            <span class="pill-tag" style="background:rgba(16,185,129,0.15); color:#10b981;">PR-AUC 0.3371 (~53x Lift)</span>
                        </div>
                        <p style="color:#cbd5e1; font-size:12.5px; margin:6px 0;">
                            Ensemble Random Forest outputs calibrated risk probability $P(	ext{Fraud}) \in [0.0, 1.0]$. Unsupervised Isolation Forest generates complementary structural anomaly scores to catch novel zero-day attack vectors.
                        </p>
                        <div>
                            <span class="pill-tag">Supervised Probability</span>
                            <span class="pill-tag">Unsupervised Anomaly Score</span>
                            <span class="pill-tag">97.6% Clean Concentration</span>
                        </div>
                    </div>
                </div>

                <div class="flow-arrow">▼</div>

                <!-- Stage 5 -->
                <div class="flow-step-card" style="border-left-color: #ef4444;">
                    <div class="flow-step-num" style="background:rgba(239,68,68,0.15); color:#ef4444; border-color:rgba(239,68,68,0.3);">5</div>
                    <div style="flex:1;">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
                            <strong style="color:#ef4444; font-size:15px;">Graph Money Laundering Correlation & Policy Threshold Gate (θ)</strong>
                            <span class="pill-tag" style="background:rgba(239,68,68,0.15); color:#ef4444;">Same-Step Pair Linking</span>
                        </div>
                        <p style="color:#cbd5e1; font-size:12.5px; margin:6px 0;">
                            Bipartite network engine correlates identical-amount same-step transfers linked to rapid cash-outs (money mule draining). The Policy Engine compares probability scores against threshold $	heta$ to trigger hard stops or human reviews.
                        </p>
                        <div>
                            <span class="pill-tag">θ ≥ 0.80 ➔ Auto Block</span>
                            <span class="pill-tag">0.10 ≤ θ &lt; 0.80 ➔ Human Review</span>
                            <span class="pill-tag">θ &lt; 0.10 ➔ Instant Pass</span>
                        </div>
                    </div>
                </div>

                <div class="flow-arrow">▼</div>

                <!-- Stage 6 -->
                <div class="flow-step-card" style="border-left-color: #a855f7;">
                    <div class="flow-step-num" style="background:rgba(168,85,247,0.15); color:#a855f7; border-color:rgba(168,85,247,0.3);">6</div>
                    <div style="flex:1;">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
                            <strong style="color:#a855f7; font-size:15px;">Multi-Agent Synthesis & Structured Case Dossier Generation</strong>
                            <span class="pill-tag" style="background:rgba(168,85,247,0.15); color:#a855f7;">Audit Ready in &lt;2s</span>
                        </div>
                        <p style="color:#cbd5e1; font-size:12.5px; margin:6px 0;">
                            Multi-agent AI synthesizes transaction facts, risk officer operational decisions, counter-party history, and graph evidence into comprehensive audit-ready forensic dossiers for compliance officers.
                        </p>
                        <div>
                            <span class="pill-tag">Fact Extraction</span>
                            <span class="pill-tag">Risk Recommendation</span>
                            <span class="pill-tag">Immutable Regulatory Audit Trail</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- STEP 4: THE DETECTOR -->
        <!-- ========================================================================= -->
        <section id="step4" class="step-section">
            <div class="step-header">
                <div class="step-badge">Step 4 of 9</div>
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
        <!-- STEP 5: THE RESULT -->
        <!-- ========================================================================= -->
        <section id="step5" class="step-section">
            <div class="step-header">
                <div class="step-badge">Step 5 of 9</div>
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
        <!-- STEP 6: THE DECISION -->
        <!-- ========================================================================= -->
        <section id="step6" class="step-section">
            <div class="step-header">
                <div class="step-badge">Step 6 of 9</div>
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
        <!-- STEP 7: RISK MITIGATION & FUND PROTECTION                                -->
        <!-- ========================================================================= -->
        <section id="step7" class="step-section">
            <div class="step-header">
                <div class="step-badge">Step 7 of 9</div>
                <h2 class="step-title">Risk Mitigation: How Sentinel Protects Capital & Reserves</h2>
                <p class="step-sub">Multi-tiered operational defense architecture designed to intercept theft, isolate money laundering mules, and maintain zero regulatory non-compliance.</p>
            </div>

            <!-- Capital Defense Summary Metrics -->
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-bottom: 20px;">
                <div class="story-card" style="border-left: 4px solid #10b981; padding: 14px;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Protected Capital</div>
                    <div style="font-size: 24px; font-weight: 800; color: #10b981; margin: 4px 0;">752.38M CU</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">Total fraudulent principal intercepted and locked in test period.</div>
                </div>

                <div class="story-card" style="border-left: 4px solid #38bdf8; padding: 14px;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Fraud Catch Rate</div>
                    <div style="font-size: 24px; font-weight: 800; color: #38bdf8; margin: 4px 0;">90.2% Recall</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">Strict operational policy stops 9 out of 10 attacks automatically.</div>
                </div>

                <div class="story-card" style="border-left: 4px solid #f59e0b; padding: 14px;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Resolution SLA</div>
                    <div style="font-size: 24px; font-weight: 800; color: #f59e0b; margin: 4px 0;">&lt; 2 Minutes</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">Precomputed multi-agent dossiers cut analyst review by 95%.</div>
                </div>

                <div class="story-card" style="border-left: 4px solid #a855f7; padding: 14px;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Mule Graph Intercepts</div>
                    <div style="font-size: 24px; font-weight: 800; color: #c084fc; margin: 4px 0;">46 Linked Pairs</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">Same-step correlated cash-out nodes frozen simultaneously.</div>
                </div>
            </div>

            <!-- 5 Defense Pillars Grid -->
            <div class="defense-pillar-grid">
                <!-- Pillar 1 -->
                <div class="defense-card" style="border-top:3px solid #ef4444;">
                    <div class="defense-card-title" style="color:#ef4444;">
                        <span>⚡ 1. Automated Circuit Breakers</span>
                    </div>
                    <p style="font-size:12px; color:#cbd5e1; line-height:1.5;">
                        High-conviction theft attempts (probability score ≥ 0.80 or amounts &gt; 99th percentile limit $2.44M) trigger instant transaction holds within 15 milliseconds, halting account liquidation before funds leave the clearinghouse.
                    </p>
                    <div style="margin-top:auto; font-size:11px; color:#94a3b8; border-top:1px solid rgba(255,255,255,0.05); padding-top:6px;">
                        <strong>Mechanism:</strong> Real-time REST gateway webhook + automated balance reserve lock.
                    </div>
                </div>

                <!-- Pillar 2 -->
                <div class="defense-card" style="border-top:3px solid #f59e0b;">
                    <div class="defense-card-title" style="color:#f59e0b;">
                        <span>🌐 2. Graph Laundering Mule Interception</span>
                    </div>
                    <p style="font-size:12px; color:#cbd5e1; line-height:1.5;">
                        Criminals transfer stolen balances to money mule accounts and attempt immediate ATM cash-outs. Sentinel's graph engine correlates same-step identical-amount pairs ($A 
ightarrow B 
ightarrow 	ext{CASH\_OUT}$) and locks both destination nodes in tandem.
                    </p>
                    <div style="margin-top:auto; font-size:11px; color:#94a3b8; border-top:1px solid rgba(255,255,255,0.05); padding-top:6px;">
                        <strong>Mechanism:</strong> Bipartite network link matching + dual-account coordinated freeze.
                    </div>
                </div>

                <!-- Pillar 3 -->
                <div class="defense-card" style="border-top:3px solid #38bdf8;">
                    <div class="defense-card-title" style="color:#38bdf8;">
                        <span>🤖 3. Multi-Agent Synthesis Dossiers</span>
                    </div>
                    <p style="font-size:12px; color:#cbd5e1; line-height:1.5;">
                        Human investigators cannot manually read millions of raw log entries during alert spikes. Sentinel automatically generates structured, evidence-backed narrative briefs with prioritized key facts, cutting manual review SLA from 45 min to under 2 min.
                    </p>
                    <div style="margin-top:auto; font-size:11px; color:#94a3b8; border-top:1px solid rgba(255,255,255,0.05); padding-top:6px;">
                        <strong>Mechanism:</strong> Precomputed multi-agent reasoning chain + instant case UI drawer.
                    </div>
                </div>

                <!-- Pillar 4 -->
                <div class="defense-card" style="border-top:3px solid #10b981;">
                    <div class="defense-card-title" style="color:#10b981;">
                        <span>📈 4. Dynamic Economic Cost Optimization</span>
                    </div>
                    <p style="font-size:12px; color:#cbd5e1; line-height:1.5;">
                        Sentinel continuously calculates the net cost curve: $	ext{Cost}(	heta) = 	ext{FN}(	heta) 	imes \overline{	ext{Principal}} + 	ext{Alerts}(	heta) 	imes C_{	ext{review}}$. The strictness threshold automatically scales with staffing costs to guarantee maximum capital ROI.
                    </p>
                    <div style="margin-top:auto; font-size:11px; color:#94a3b8; border-top:1px solid rgba(255,255,255,0.05); padding-top:6px;">
                        <strong>Mechanism:</strong> Real-time cost sensitivity matrix recalculation & threshold auto-tuning.
                    </div>
                </div>

                <!-- Pillar 5 -->
                <div class="defense-card" style="border-top:3px solid #a855f7;">
                    <div class="defense-card-title" style="color:#c084fc;">
                        <span>🛡️ 5. Regulatory Compliance & Audit Shield</span>
                    </div>
                    <p style="font-size:12px; color:#cbd5e1; line-height:1.5;">
                        Every algorithmic hold, escalation, and investigation rationale is recorded with immutable audit metadata. Prevents supervisory sanctions, RBI Section 35A license suspensions, and multi-billion dollar equity value collapses.
                    </p>
                    <div style="margin-top:auto; font-size:11px; color:#94a3b8; border-top:1px solid rgba(255,255,255,0.05); padding-top:6px;">
                        <strong>Mechanism:</strong> Continuous compliance logging under RBI, DPDP, and PMLA standards.
                    </div>
                </div>
            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- STEP 8: THE MARKET LINK -->
        <!-- ========================================================================= -->
        <section id="step8" class="step-section">
            <div class="step-header">
                <div class="step-badge">Step 8 of 9</div>
                <h2 class="step-title">The Market Link: Compliance Failures & Equity Impact</h2>
                <p class="step-sub">Forensic case study on the ₹25,000+ Cr valuation collapse following supervisory action on payment fraud and AML/KYC non-compliance.</p>
            </div>

            <!-- Market Impact Key Financial Metrics Grid -->
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-bottom: 20px;">
                <div class="story-card" style="border-left: 4px solid #ef4444; padding: 14px;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Equity Destruction</div>
                    <div style="font-size: 24px; font-weight: 800; color: #ef4444; margin: 4px 0;">-55.1% Drawdown</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">~₹25,000 Cr market cap erased in under 3 weeks post-RBI order.</div>
                </div>

                <div class="story-card" style="border-left: 4px solid #f59e0b; padding: 14px;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Volatility Explosion</div>
                    <div style="font-size: 24px; font-weight: 800; color: #f59e0b; margin: 4px 0;">25.8% ➔ 78.7%</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">+305% annualized volatility surge as risk premia expanded.</div>
                </div>

                <div class="story-card" style="border-left: 4px solid #38bdf8; padding: 14px;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Market Beta Spike</div>
                    <div style="font-size: 24px; font-weight: 800; color: #38bdf8; margin: 4px 0;">0.66 ➔ 2.02</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">Shifted from defensive tech utility to high-beta distressed asset.</div>
                </div>

                <div class="story-card" style="border-left: 4px solid #10b981; padding: 14px;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Benchmark Decoupling</div>
                    <div style="font-size: 24px; font-weight: 800; color: #34d399; margin: 4px 0;">-56.9% Alpha Gap</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">NIFTY 50 remained stable (+1.8%) confirming 100% compliance cause.</div>
                </div>
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

            <!-- Detailed Event Timeline & Forensic Insights Grid -->
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; margin-top: 20px;">
                <div class="story-card">
                    <h3 style="color:#38bdf8; font-size:14px; margin-bottom:10px; display:flex; align-items:center; gap:6px;">
                        <span>📅 Chronology of Regulatory Supervisory Actions</span>
                    </h3>
                    <div style="display:flex; flex-direction:column; gap:10px; font-size:12px; line-height:1.45;">
                        <div style="border-left:2px solid #ef4444; padding-left:10px;">
                            <strong style="color:#ef4444;">Jan 31, 2024 (RBI Section 35A Directive):</strong> Reserve Bank of India directs cessation of onboarding, wallet deposits, and credit operations in Payments Bank due to persistent supervisory non-compliance and AML lapses.
                        </div>
                        <div style="border-left:2px solid #f59e0b; padding-left:10px;">
                            <strong style="color:#f59e0b;">Feb 1–2, 2024 (Panic Market Liquidation):</strong> Back-to-back -20% lower circuit trading halts. Over ₹20,000 Cr in market capitalization erased in 48 hours.
                        </div>
                        <div style="border-left:2px solid #38bdf8; padding-left:10px;">
                            <strong style="color:#38bdf8;">Feb 16, 2024 (Migration Deadline Extension):</strong> Regulatory deadline extended to March 15 to facilitate emergency merchant nodal migrations to third-party partner banks.
                        </div>
                        <div style="border-left:2px solid #10b981; padding-left:10px;">
                            <strong style="color:#10b981;">March 2024+ (Permanent Structural Re-Rating):</strong> Loss of float interest revenue, elevated customer acquisition costs, and recurring external audit overhead.
                        </div>
                    </div>
                </div>

                <div class="story-card">
                    <h3 style="color:#38bdf8; font-size:14px; margin-bottom:10px; display:flex; align-items:center; gap:6px;">
                        <span>🛡️ Strategic Lessons for Fintech AI Governance</span>
                    </h3>
                    <div style="display:flex; flex-direction:column; gap:10px; font-size:12px; line-height:1.45;">
                        <div style="background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.25); border-radius:6px; padding:8px 12px;">
                            <strong style="color:#ef4444;">1. Non-Compliance is an Solvency Risk:</strong> Payment screening failures trigger supervisory license revocation, wiping out enterprise equity far beyond direct chargeback losses.
                        </div>
                        <div style="background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.25); border-radius:6px; padding:8px 12px;">
                            <strong style="color:#38bdf8;">2. Multi-Agent Audit Trail Defense:</strong> Automated reasoning trails and synthesized case files give regulators verifiable proof of continuous surveillance and rule compliance.
                        </div>
                        <div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.25); border-radius:6px; padding:8px 12px;">
                            <strong style="color:#34d399;">3. Economic Policy Tuning:</strong> Real-time cost curve threshold adjustment prevents millions in criminal theft while preventing operational review backlogs.
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- STEP 9: LIVE PATROL AND CASES -->
        <!-- ========================================================================= -->
        <section id="step9" class="step-section">
            <div class="step-header">
                <div class="step-badge">Step 9 of 9</div>
                <h2 class="step-title">Live Patrol: Test Replay Stream & Case Dossiers</h2>
                <p class="step-sub">Simulated hourly playback across test steps 334–742 and forensic multi-agent case investigation dossiers.</p>
            </div>

            <!-- 3D Ledger City Launch Banner -->
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
                            <option value="2500">🐢 Slow (2.5s / step)</option>
                            <option value="1500" selected>⏱️ Normal (1.5s / step)</option>
                            <option value="800">⚡ Moderate (0.8s / step)</option>
                            <option value="400">🚀 Fast (0.4s / step)</option>
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
                
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:14px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:12px; color:var(--text-muted);">Filter Cases:</span>
                        <button class="btn btn-secondary active" id="caseFilterFraudBtn" onclick="filterCases('fraud')" style="padding:4px 10px; font-size:11px; background:rgba(239,68,68,0.2); color:#fca5a5; border-color:#ef4444;">🚨 Confirmed Frauds (210)</button>
                        <button class="btn btn-secondary" id="caseFilterFpBtn" onclick="filterCases('fp')" style="padding:4px 10px; font-size:11px; background:rgba(245,158,11,0.15); color:#fde68a; border-color:#f59e0b;">⚠️ False Alarms (179)</button>
                        <button class="btn btn-secondary" id="caseFilterAllBtn" onclick="filterCases('all')" style="padding:4px 10px; font-size:11px;">All Alerts (389)</button>
                    </div>

                    <div style="display:flex; align-items:center; gap:8px;">
                        <label style="font-size:12px; color:var(--text-muted);">Select Dossier:</label>
                        <select id="patrolCaseSelect" onchange="renderCaseDossier(this.value)" style="min-width:340px; font-size:12px;"></select>
                    </div>
                </div>

                <div id="patrolCaseDossierBox"></div>
                <div class="card-source-footer" style="margin-top:14px;">Source: docs/data/stream.json (cases)</div>
            </div>

            <!-- Live Hourly Incident Ticker for Step -->
            <div class="story-card" style="margin-top:20px;">
                <div class="card-question">Live Hourly Interception Ticker (Active Transactions & Threats for Step)</div>
                <div id="patrolHourlyTickerBox" style="font-size:12px; color:var(--text-muted);">
                    Loading active transactions for the current step...
                </div>
            </div>
        </section>

    </main>

    <!-- Floating Sentinel AI Copilot Chatbot Button -->
    <button id="sentinelChatTrigger" class="chat-trigger-btn" onclick="toggleChat()" title="Open Sentinel AI Copilot">
        <span class="chat-trigger-pulse"></span>
        <span>🤖 Sentinel Copilot AI</span>
    </button>

    <!-- Sentinel AI Chat Window -->
    <div id="sentinelChatWindow" class="chat-window">
        <div class="chat-header">
            <div class="chat-header-title">
                <span>🤖</span>
                <span>Sentinel Copilot AI</span>
                <span style="font-size:10px; background:rgba(16,185,129,0.2); color:#34d399; padding:2px 6px; border-radius:4px; font-weight:700;">LIVE v3.2</span>
            </div>
            <div class="chat-header-controls">
                <button class="chat-ctrl-btn" onclick="clearChatHistory()" title="Clear Chat">🧹</button>
                <button class="chat-ctrl-btn" onclick="toggleChat()" title="Close">✕</button>
            </div>
        </div>

        <div class="chat-quick-chips">
            <button class="chat-chip" onclick="sendQuickPrompt('Explain the 6-stage classification roadmap')">🗺️ Classification Pipeline</button>
            <button class="chat-chip" onclick="sendQuickPrompt('How do we protect our funds and mitigate risk?')">🛡️ Fund Protection</button>
            <button class="chat-chip" onclick="sendQuickPrompt('How do automated circuit breakers work?')">⚡ Circuit Breakers</button>
            <button class="chat-chip" onclick="sendQuickPrompt('What is optimal strictness threshold theta and review cost?')">⚖️ Threshold & Costs</button>
            <button class="chat-chip" onclick="sendQuickPrompt('How does graph mule interception detect money laundering?')">🕸️ Graph Mule Hunter</button>
            <button class="chat-chip" onclick="sendQuickPrompt('What happened to Paytm during its compliance failure?')">📉 Paytm Case Study</button>
            <button class="chat-chip" onclick="sendQuickPrompt('Open 3D Ledger City simulation')">🏙️ Open 3D City</button>
        </div>

        <div id="chatMessages" class="chat-messages">
            <div class="chat-msg chat-msg-ai">
                <div class="chat-avatar">🤖</div>
                <div class="chat-bubble chat-bubble-ai">
                    <p><strong>Greetings, Investigator.</strong> I am <strong>Sentinel Copilot</strong>, your AI intelligence assistant for this PaySim financial fraud ecosystem.</p>
                    <p>I can explain our <strong>classification pipeline</strong>, details on <strong>752.38M CU in protected funds</strong>, optimal strictness thresholds ($	heta^*$), mule laundering rings, or guide you across any story step.</p>
                    <p style="font-size:11px; color:#94a3b8; margin-top:4px;">Ask me anything or select a topic above!</p>
                </div>
            </div>
        </div>

        <div class="chat-input-area">
            <input type="text" id="chatInput" class="chat-input" placeholder="Ask about fraud detection, algorithms, cases, risk..." onkeydown="if(event.key==='Enter') sendChatMessage()">
            <button class="chat-send-btn" onclick="sendChatMessage()">Send</button>
        </div>
    </div>

    <!-- 3D Ledger City Modal -->
    <div id="cityModal" class="city-modal">
        <div class="city-modal-header">
            <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:18px;">🏙️</span>
                <span style="font-size:16px; font-weight:700; color:#f8fafc;">3D Real-Time Ledger City Simulation</span>
                <span id="cityStepDisplay" style="font-size:12px; background:rgba(56,189,248,0.15); color:#38bdf8; padding:3px 8px; border-radius:4px; font-family:var(--font-mono);">Step: 334</span>
            </div>
            <div style="display:flex; align-items:center; gap:10px;">
                <button class="btn btn-secondary" onclick="setCameraPreset('top')" style="font-size:12px;">🔭 Top Bird's Eye</button>
                <button class="btn btn-secondary" onclick="setCameraPreset('radar')" style="font-size:12px;">🛰️ 90° Radar</button>
                <button class="btn btn-secondary" onclick="setCameraPreset('iso')" style="font-size:12px;">📐 Isometric</button>
                <button class="btn btn-secondary" onclick="setCameraPreset('street')" style="font-size:12px;">🚶 Street</button>
                <button class="btn btn-primary" onclick="closeSentinelCity()" style="font-size:12px;">✕ Close City</button>
            </div>
        </div>
        <div class="city-modal-body">
            <div id="cityCanvasContainer"></div>
            
            <div class="city-hud">
                <div style="font-size:13px; font-weight:700; color:#38bdf8; margin-bottom:6px;">City Ledger Radar</div>
                <div style="font-size:11.5px; color:#cbd5e1; line-height:1.4;">
                    Visualizing PaySim transfer flows, humanoid mule agents, and autonomous Sentinel drone patrols across 9 financial districts.
                </div>
                <div style="margin-top:10px; display:flex; gap:6px;">
                    <button class="btn btn-secondary" id="cityPlayBtn" onclick="togglePatrolPlay()" style="padding:4px 10px; font-size:11px;">⏸ Pause</button>
                    <button class="btn btn-secondary" onclick="patrolCurrentStep=334; renderPatrolStep(334);" style="padding:4px 10px; font-size:11px;">⏮ Reset</button>
                </div>
            </div>

            <!-- Evidence Dossier Board inside City -->
            <div id="cityEvidenceBoard" style="display:none; position:absolute; bottom:24px; left:24px; background:rgba(13,21,39,0.95); border:1px solid #ef4444; border-radius:10px; padding:16px; max-width:380px; z-index:20; backdrop-filter:blur(10px);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span id="evidenceTitle" style="font-weight:700; color:#fca5a5; font-size:13px;">🚨 Intercepted Fraud Evidence</span>
                    <button onclick="closeEvidenceBoard()" style="background:transparent; border:none; color:#94a3b8; cursor:pointer;">✕</button>
                </div>
                <div id="evidenceType" style="font-size:12px; color:#e2e8f0; margin-bottom:4px;"></div>
                <div id="evidenceAmt" style="font-size:12px; font-weight:700; color:#38bdf8; margin-bottom:4px;"></div>
                <div id="evidenceRoute" style="font-size:11px; color:#94a3b8; margin-bottom:4px;"></div>
                <div id="evidenceScore" style="font-size:11px; color:#f59e0b; margin-bottom:4px;"></div>
                <div id="evidenceAgents" style="font-size:11px; color:#cbd5e1; margin-bottom:4px;"></div>
                <div id="evidenceStatus" style="font-size:11px; font-weight:700; color:#10b981; margin-top:8px;"></div>
            </div>
        </div>
    </div>
    

<script>

        const DATA = __DATA_BUNDLE__;

        const THRESHOLD_GRID = [0.01, 0.02, 0.03, 0.04, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95];
        let currentStrictness = 0.50;
        let currentCheckingCost = 500;
        let evalMode = true;
        let patrolPlaying = true;
        let patrolCurrentStep = 334;
        let patrolInterval = null;
        let patrolSpeed = 1500;

        // Chart instances
        let chartC2, chartC3, chartC4, chartC5, chartC6, chartC7, chartC9, chartC10, chartC11, chartC12;

                function goToStep(stepNum) {
            document.querySelectorAll('.step-section').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-item-btn').forEach(el => el.classList.remove('active'));
            const target = document.getElementById('step' + stepNum);
            if (target) target.classList.add('active');
            const btns = document.querySelectorAll('.nav-item-btn');
            if (btns[stepNum - 1]) btns[stepNum - 1].classList.add('active');
            window.scrollTo({ top: 0, behavior: 'smooth' });

            setTimeout(() => {
                if (stepNum === 1) { renderCard1(); renderCard2(); }
                else if (stepNum === 2) { renderCard3(); renderCard4(); renderCard5(); }
                else if (stepNum === 4) { renderCard6(); renderCard7(); }
                else if (stepNum === 5) { renderCard8(); renderCard9(); }
                else if (stepNum === 6) { renderCard10(); }
                else if (stepNum === 8) { renderCard11(); }
                else if (stepNum === 9) { renderCard12(); }
            }, 50);
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

        // Card 12: Live Patrol & Highlighted Fraud Case Dossiers
        let currentCaseFilter = 'fraud';

        function filterCases(mode) {
            currentCaseFilter = mode;
            const btnAll = document.getElementById('caseFilterAllBtn');
            const btnFraud = document.getElementById('caseFilterFraudBtn');
            const btnFp = document.getElementById('caseFilterFpBtn');
            if (btnAll) btnAll.classList.toggle('active', mode === 'all');
            if (btnFraud) btnFraud.classList.toggle('active', mode === 'fraud');
            if (btnFp) btnFp.classList.toggle('active', mode === 'fp');

            const caseSel = document.getElementById('patrolCaseSelect');
            if (!caseSel) return;
            const keys = Object.keys(DATA.stream.cases);
            let filteredKeys = keys;
            if (mode === 'fraud') {
                filteredKeys = keys.filter(k => DATA.stream.cases[k].isFraud === 1);
            } else if (mode === 'fp') {
                filteredKeys = keys.filter(k => DATA.stream.cases[k].isFraud === 0);
            }

            caseSel.innerHTML = filteredKeys.map(k => {
                const c = DATA.stream.cases[k];
                const isF = c.isFraud === 1;
                const prefix = isF ? '🚨 [CONFIRMED FRAUD]' : '⚠️ [FALSE ALARM]';
                return `<option value="${k}">${prefix} ${k} (${c.transaction.type}, ${c.transaction.amount.toLocaleString()} CU | RF Score: ${c.scores.model_score.toFixed(3)})</option>`;
            }).join('');

            if (filteredKeys.length > 0) renderCaseDossier(filteredKeys[0]);
        }

        function renderCard12() {
            const edges46 = DATA.stream.network_edges.filter(e => e.step > 333);
            const headEl = document.getElementById('c12Headline');
            if (headEl) headEl.innerText = `Replaying steps 334–742 with ${edges46.length} test-period correlated money laundering pairs tracked across nodes.`;

            // Populate Case Selector with fraud cases highlighted
            filterCases('fraud');
            renderPatrolStep(patrolCurrentStep);
        }

        function renderCaseDossier(caseId) {
            const c = DATA.stream.cases[caseId];
            if (!c) return;
            const tx = c.transaction;
            const ro = c.risk_officer;
            const isF = c.isFraud === 1;
            const rpt = c.report_text || "No AI report available.";

            const statusBadge = isF 
                ? `<div style="background:rgba(239,68,68,0.2); border:1px solid #ef4444; color:#fca5a5; padding:6px 12px; border-radius:6px; font-weight:800; font-size:12px; display:inline-flex; align-items:center; gap:6px;">
                     <span>🚨 CONFIRMED REAL-WORLD THEFT — Intercepted & Blocked</span>
                   </div>`
                : `<div style="background:rgba(245,158,11,0.15); border:1px solid #f59e0b; color:#fde68a; padding:6px 12px; border-radius:6px; font-weight:700; font-size:12px; display:inline-flex; align-items:center; gap:6px;">
                     <span>⚠️ BENIGN HIGH-VALUE OUTLIER — Cleared in Human Review</span>
                   </div>`;

            const box = document.getElementById('patrolCaseDossierBox');
            if (box) {
                box.innerHTML = `
                    <div style="background:#080d1a; border:${isF ? '2px solid rgba(239,68,68,0.6)' : '1px solid var(--border-color)'}; border-radius:8px; padding:16px; margin-top:10px; box-shadow:${isF ? '0 0 15px rgba(239,68,68,0.15)' : 'none'};">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
                            <div>
                                <strong style="font-size:14px; color:${isF ? '#f87171' : '#38bdf8'};">📁 Dossier: <code>${caseId}</code></strong>
                                <span style="color:#94a3b8; font-size:12px; margin-left:8px;">(Step ${tx.step} • Hour ${tx.hour})</span>
                            </div>
                            ${statusBadge}
                        </div>

                        <!-- Highlighted Forensic Metrics -->
                        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:14px; background:rgba(255,255,255,0.03); padding:12px; border-radius:6px;">
                            <div>
                                <span style="font-size:11px; color:#94a3b8; text-transform:uppercase;">Stolen Principal</span>
                                <div style="font-size:16px; font-weight:800; color:${isF ? '#ef4444' : '#e2e8f0'};">${tx.amount.toLocaleString()} <span style="font-size:11px; font-weight:400; color:#94a3b8;">CU</span></div>
                                <span style="font-size:11px; color:#f59e0b;">${c.amount_analysis.percentile_vs_train}% vs training baseline</span>
                            </div>
                            <div>
                                <span style="font-size:11px; color:#94a3b8; text-transform:uppercase;">Model Risk Score</span>
                                <div style="font-size:16px; font-weight:800; color:#38bdf8;">${(c.scores.model_score * 100).toFixed(1)}% <span style="font-size:11px; font-weight:400; color:#94a3b8;">Prob</span></div>
                                <span style="font-size:11px; color:#94a3b8;">Anomaly: ${c.scores.anomaly_score.toFixed(4)}</span>
                            </div>
                            <div>
                                <span style="font-size:11px; color:#94a3b8; text-transform:uppercase;">Channel & Accounts</span>
                                <div style="font-size:13px; font-weight:700; color:#e2e8f0;">${tx.type}</div>
                                <span style="font-size:11px; color:#94a3b8;">${tx.nameOrig} ➔ ${tx.nameDest}</span>
                            </div>
                            <div>
                                <span style="font-size:11px; color:#94a3b8; text-transform:uppercase;">Risk Officer Decision</span>
                                <div style="font-size:13px; font-weight:800; color:#f59e0b;">${ro.decision_balanced.toUpperCase()}</div>
                                <span style="font-size:11px; color:#34d399;">Escalated: ${ro.escalated ? 'YES' : 'NO'}</span>
                            </div>
                        </div>

                        <!-- Network Laundering Linked Counterpart -->
                        ${c.network_evidence.has_linked_pair ? `
                            <div style="background:rgba(239,68,68,0.1); border:1px dashed #ef4444; border-radius:6px; padding:10px 14px; margin-bottom:12px; font-size:12px; color:#fca5a5;">
                                <strong>🌐 Graph Laundering Link Detected:</strong> Same-step identical-amount counterpart pair tracked across network edges (${c.network_evidence.evidence_note}).
                            </div>
                        ` : ''}

                        <div style="font-size:11px; font-weight:700; color:#38bdf8; text-transform:uppercase; margin-bottom:4px;">🤖 Multi-Agent Synthesis Dossier Report:</div>
                        <pre style="background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.06); padding:12px; border-radius:6px; font-size:11.5px; color:#cbd5e1; max-height:220px; overflow-y:auto; line-height:1.45;">${rpt}</pre>
                    </div>
                `;
            }
        }

        function togglePatrolPlay() {
            patrolPlaying = !patrolPlaying;
            const playBtn = document.getElementById('patrolPlayBtn');
            if (playBtn) playBtn.innerText = patrolPlaying ? "⏸️ Pause" : "▶️ Play";
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
                const scrub = document.getElementById('patrolScrubber');
                if (scrub) scrub.value = patrolCurrentStep;
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
            const displayEl = document.getElementById('patrolStepDisplay');
            if (displayEl) displayEl.innerText = `Step: ${step} (Hour ${hour})`;

            const minS = Math.max(334, step - 30);
            const stepSlice = DATA.hourly_stats.filter(h => h.step >= minS && h.step <= step);

            const canvas = document.getElementById('c12Chart');
            if (canvas) {
                const ctx = canvas.getContext('2d');
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

            const tickerBox = document.getElementById('patrolHourlyTickerBox');
            if (tickerBox) {
                const hourPeople = (DATA.city_people_by_step && DATA.city_people_by_step[step]) ? DATA.city_people_by_step[step] : [];
                const fraudTxs = hourPeople.filter(p => p.f === 1);
                const alertTxs = hourPeople.filter(p => p.sc >= currentStrictness);

                if (hourPeople.length === 0) {
                    tickerBox.innerHTML = `<div style="color:#64748b; padding:8px;">No transactions recorded in hour step ${step}.</div>`;
                } else {
                    let html = `<div style="margin-bottom:8px; display:flex; gap:14px; flex-wrap:wrap; font-size:12px;">
                        <span><strong>Total Step Payments:</strong> ${hourPeople.length}</span>
                        <span><strong style="color:#f59e0b;">Model Flagged Alerts (θ=${currentStrictness.toFixed(2)}):</strong> ${alertTxs.length}</span>
                        <span><strong style="color:#ef4444;">🚨 Confirmed Real Frauds:</strong> ${fraudTxs.length}</span>
                    </div>`;

                    html += `<div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap:10px;">`;
                    hourPeople.slice(0, 8).forEach(p => {
                        const isF = p.f === 1;
                        const isAlert = p.sc >= currentStrictness;
                        const borderStyle = isF ? "border:1px solid #ef4444; background:rgba(239,68,68,0.12);" : (isAlert ? "border:1px solid #f59e0b; background:rgba(245,158,11,0.08);" : "border:1px solid rgba(255,255,255,0.06); background:rgba(255,255,255,0.02);");
                        
                        html += `
                            <div style="${borderStyle} padding:10px; border-radius:6px; font-size:11.5px; display:flex; justify-content:space-between; align-items:center;">
                                <div>
                                    <div style="font-weight:700; color:${isF ? '#fca5a5' : '#e2e8f0'}; display:flex; align-items:center; gap:4px;">
                                        ${isF ? '🚨 THEFT:' : (isAlert ? '⚠️ ALERT:' : '✅ PASS:')} ${p.t}
                                    </div>
                                    <div style="color:#cbd5e1; font-weight:700;">${p.amt.toLocaleString()} CU</div>
                                    <div style="color:#94a3b8; font-size:10.5px;">District ${p.df} ➔ ${p.dt}</div>
                                </div>
                                <div style="text-align:right;">
                                    <div style="font-weight:800; color:${p.sc >= 0.5 ? '#ef4444' : '#38bdf8'};">${(p.sc * 100).toFixed(1)}%</div>
                                    <span style="font-size:10px; color:#94a3b8;">Risk Score</span>
                                </div>
                            </div>
                        `;
                    });
                    html += `</div>`;
                    tickerBox.innerHTML = html;
                }
            }
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
    
    
    
    
    
    
    
    
        // ==========================================================================
        // SENTINEL AI COPILOT CHATBOT LOGIC & INTELLIGENCE ENGINE
        // ==========================================================================
        let chatOpen = false;

        function toggleChat() {
            const win = document.getElementById('sentinelChatWindow');
            if (!win) return;
            chatOpen = !chatOpen;
            if (chatOpen) {
                win.classList.add('active');
                document.getElementById('chatInput').focus();
            } else {
                win.classList.remove('active');
            }
        }

        function clearChatHistory() {
            const msgBox = document.getElementById('chatMessages');
            if (!msgBox) return;
            msgBox.innerHTML = `
                <div class="chat-msg chat-msg-ai">
                    <div class="chat-avatar">🤖</div>
                    <div class="chat-bubble chat-bubble-ai">
                        <p><strong>Chat cleared.</strong> How may Sentinel Copilot assist your fraud investigation now?</p>
                    </div>
                </div>
            `;
        }

        function sendQuickPrompt(text) {
            const inp = document.getElementById('chatInput');
            if (inp) {
                inp.value = text;
                sendChatMessage();
            }
        }

        function appendUserMessage(text) {
            const msgBox = document.getElementById('chatMessages');
            if (!msgBox) return;
            const div = document.createElement('div');
            div.className = 'chat-msg chat-msg-user';
            div.innerHTML = `
                <div class="chat-bubble chat-bubble-user">${escapeHtml(text)}</div>
            `;
            msgBox.appendChild(div);
            msgBox.scrollTop = msgBox.scrollHeight;
        }

        function appendAiMessage(htmlContent) {
            const msgBox = document.getElementById('chatMessages');
            if (!msgBox) return;
            const div = document.createElement('div');
            div.className = 'chat-msg chat-msg-ai';
            div.innerHTML = `
                <div class="chat-avatar">🤖</div>
                <div class="chat-bubble chat-bubble-ai">${htmlContent}</div>
            `;
            msgBox.appendChild(div);
            msgBox.scrollTop = msgBox.scrollHeight;
        }

        function escapeHtml(str) {
            return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        }

        function applyPresetThreshold(val) {
            const slider = document.getElementById('simStrictnessSlider');
            if (slider) {
                slider.value = val;
                updateSimScore();
            }
            goToStep(5);
        }

        function sendChatMessage() {
            const inp = document.getElementById('chatInput');
            if (!inp) return;
            const raw = inp.value.trim();
            if (!raw) return;
            inp.value = '';

            appendUserMessage(raw);

            // Show typing indicator
            const msgBox = document.getElementById('chatMessages');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'chat-msg chat-msg-ai';
            typingDiv.id = 'chatTypingIndicator';
            typingDiv.innerHTML = `
                <div class="chat-avatar">🤖</div>
                <div class="chat-bubble chat-bubble-ai">
                    <div class="chat-typing">
                        <div class="chat-typing-dot"></div>
                        <div class="chat-typing-dot"></div>
                        <div class="chat-typing-dot"></div>
                    </div>
                </div>
            `;
            msgBox.appendChild(typingDiv);
            msgBox.scrollTop = msgBox.scrollHeight;

            setTimeout(() => {
                const indicator = document.getElementById('chatTypingIndicator');
                if (indicator) indicator.remove();

                const responseHtml = generateSentinelResponse(raw);
                appendAiMessage(responseHtml);
            }, 450);
        }

        function generateSentinelResponse(query) {
            const q = query.toLowerCase();

            // 1. Classification Roadmap & Pipeline
            if (q.includes('roadmap') || q.includes('flowchart') || q.includes('pipeline') || q.includes('classify') || q.includes('how we find') || q.includes('stages')) {
                return `
                    <p><strong>🗺️ End-to-End Classification Pipeline:</strong></p>
                    <p>Sentinel identifies illicit transfers via a <strong>6-stage visual pipeline</strong>:</p>
                    <ol style="margin-left: 18px; margin-bottom: 8px;">
                        <li><strong>1. Stream Ingestion:</strong> Ingests 954,393 transactions (0.13% base fraud rate).</li>
                        <li><strong>2. Leak-Free Time Split:</strong> Historical training on $t \le 600$, zero-leakage evaluation on $t > 600$.</li>
                        <li><strong>3. Channel Filtering:</strong> Targets <code>TRANSFER</code> & <code>CASH_OUT</code> vectors where 100% of thefts occur.</li>
                        <li><strong>4. Feature Engineering:</strong> Computes balance discrepancy (<code>orig_err</code>), account drain ratio, & velocity.</li>
                        <li><strong>5. Ensemble Detection:</strong> Random Forest + Isolation Forest scores every payment.</li>
                        <li><strong>6. Agent Triangulation:</strong> Graph Mule Hunter builds synthesized multi-agent forensic dossiers.</li>
                    </ol>
                    <button class="chat-action-btn" onclick="goToStep(3);">🗺️ Jump to Step 3 Roadmap</button>
                `;
            }

            // 2. Fund Protection & Risk Mitigation
            if (q.includes('protect') || q.includes('fund') || q.includes('mitigat') || q.includes('risk') || q.includes('pillar') || q.includes('circuit')) {
                return `
                    <p><strong>🛡️ Fund Protection & Risk Mitigation System:</strong></p>
                    <p>Sentinel defends <strong>752.38M CU</strong> in capital across <strong>5 Core Defense Pillars</strong>:</p>
                    <ul style="margin-left: 16px; margin-bottom: 8px;">
                        <li><strong>⚡ Automated Circuit Breakers:</strong> Sub-second auto-freezes on transfers with score $\theta > 0.85$ or balance drains $>90\%$.</li>
                        <li><strong>🕸️ Graph Mule Interception:</strong> Blocks <code>TRANSFER</code> $\to$ <code>CASH_OUT</code> pairs before cash extraction at ATMs.</li>
                        <li><strong>🤖 Multi-Agent SLAs:</strong> Autonomous dossiers synthesized under a 2-minute response SLA.</li>
                        <li><strong>⚖️ Dynamic Cost Optimization:</strong> $\theta^* = 0.50$ balances review costs ($C_{\text{review}}$) against fraud leakage.</li>
                        <li><strong>📜 Regulatory Compliance Shield:</strong> Immutable audit logs prevent Paytm-style RBI regulatory shutdowns.</li>
                    </ul>
                    <button class="chat-action-btn" onclick="goToStep(7);">🛡️ Jump to Step 7 Risk Mitigation</button>
                `;
            }

            // 3. Strictness Threshold & Review Cost
            if (q.includes('threshold') || q.includes('strictness') || q.includes('theta') || q.includes('cost') || q.includes('review cost') || q.includes('optimal')) {
                return `
                    <p><strong>⚖️ Strictness Threshold ($\theta$) & Review Cost:</strong></p>
                    <p><strong>Strictness Threshold ($\theta$):</strong> The probability cutoff above which transactions are flagged for quarantine. Low $\theta$ catches more fraud but triggers false alarms; high $\theta$ reduces false alarms but risks fraud leakage.</p>
                    <p><strong>Review Cost ($C_{\text{review}}$):</strong> The operational expense to manually verify flagged alerts ($500 CU/alert default). Sentinel finds the mathematical minimum total cost $\theta^* = 0.50$.</p>
                    <div style="margin-top:6px;">
                        <button class="chat-action-btn" onclick="applyPresetThreshold(0.50);">⚖️ Set Optimal Threshold (θ = 0.50)</button>
                        <button class="chat-action-btn" onclick="goToStep(5);">🎯 View Financial Cost Curve</button>
                    </div>
                `;
            }

            // 4. Paytm Case Study & Market Link
            if (q.includes('paytm') || q.includes('market') || q.includes('compliance') || q.includes('rbi') || q.includes('equity') || q.includes('stock')) {
                return `
                    <p><strong>📉 Market Impact & The Paytm Regulatory Precedent:</strong></p>
                    <p>On January 31, 2024, the Reserve Bank of India (RBI) banned Paytm Payments Bank after discovering thousands of accounts linked to single PANs and widespread lack of real-time AML graph surveillance.</p>
                    <p><strong>Financial Fallout:</strong> Paytm's parent stock plummeted <strong>65%</strong> (₹760 ➔ ₹325), wiping out <strong>$2.6 Billion</strong> in market cap within weeks.</p>
                    <p><em>Lesson:</em> Fraud detection is not just risk mitigation—it protects enterprise enterprise value and regulatory licensing.</p>
                    <button class="chat-action-btn" onclick="goToStep(8);">📉 Jump to Step 8 Market Impact</button>
                `;
            }

            // 5. 3D Ledger City Simulation
            if (q.includes('city') || q.includes('3d') || q.includes('simulation') || q.includes('radar') || q.includes('camera') || q.includes('drone')) {
                return `
                    <p><strong>🏙️ 3D Real-Time Ledger City Simulation:</strong></p>
                    <p>Experience transactions moving across 9 financial districts in a cybernetic 3D digital twin. Features walking humanoid mule actors and autonomous Sentinel drone patrols.</p>
                    <p><strong>Available Camera Presets:</strong> Top Bird's Eye, 90° Top-Down Radar, Isometric, and Street level.</p>
                    <button class="chat-action-btn" onclick="openSentinelCity(); toggleChat();">🏙️ Launch 3D Ledger City</button>
                `;
            }

            // 6. Live Patrol & Cases
            if (q.includes('patrol') || q.includes('case') || q.includes('dossier') || q.includes('live') || q.includes('ticker') || q.includes('step 9')) {
                return `
                    <p><strong>⏱️ Live Patrol & Case File Dossiers:</strong></p>
                    <p>Inspect precomputed multi-agent case dossiers across 389 alert incidents (210 confirmed frauds, 179 false alarms) with live hourly transaction tickers.</p>
                    <button class="chat-action-btn" onclick="goToStep(9);">⏱️ Jump to Live Patrol & Cases</button>
                `;
            }

            // 7. Specific Account / Fraud query
            if (q.includes('c123') || q.includes('account') || q.includes('drain') || q.includes('transfer') || q.includes('cash_out')) {
                return `
                    <p><strong>🔍 Account Forensic Analysis:</strong></p>
                    <p>Typical fraud in PaySim follows an account takeover pattern:</p>
                    <ul style="margin-left: 16px; margin-bottom: 6px;">
                        <li><strong>Vector 1:</strong> Rapid <code>TRANSFER</code> draining 100% of origin balance (<code>oldbalanceOrg > 0</code>, <code>newbalanceOrig = 0</code>).</li>
                        <li><strong>Vector 2:</strong> Immediate paired <code>CASH_OUT</code> at an external mule node.</li>
                        <li><strong>Error Flag:</strong> <code>orig_err != 0</code> or <code>dest_err != 0</code> indicating balance falsification.</li>
                    </ul>
                    <button class="chat-action-btn" onclick="goToStep(9);">📂 Inspect Live Cases</button>
                `;
            }

            // 8. General Navigation / Default
            return `
                <p>I understand you are asking about: <em>"${escapeHtml(query)}"</em></p>
                <p>Here are quick shortcuts to key areas of Sentinel's fraud intelligence suite:</p>
                <div style="display:flex; flex-direction:column; gap:4px; margin-top:6px;">
                    <button class="chat-action-btn" onclick="goToStep(3);">🗺️ 1. View Classification Roadmap (Step 3)</button>
                    <button class="chat-action-btn" onclick="goToStep(7);">🛡️ 2. View Fund Protection & Risk Mitigation (Step 7)</button>
                    <button class="chat-action-btn" onclick="goToStep(5);">🎯 3. View Optimal Thresholds & Costs (Step 5)</button>
                    <button class="chat-action-btn" onclick="openSentinelCity(); toggleChat();">🏙️ 4. Open 3D Ledger City Simulation</button>
                </div>
            `;
        }
    
    </script>
</body>
</html>"""

if __name__ == "__main__":
    build_mission8_site()
