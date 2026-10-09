#!/usr/bin/env python3
"""
repair_chatbot_cleanly.py
1. Cleans corrupted duplicate scripts from <head>.
2. Restores proper <script src="three.min.js"></script> in <head>.
3. Places the full Sentinel AI Copilot Chatbot script cleanly in the main JS bundle.
4. Rebuilds docs/index.html and index.html.
"""

import re

def main():
    with open("src/build_mission8_dashboard.py", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Clean out any script block accidentally injected into <head>
    pattern_head_corrupt = r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/three\.js/r128/three\.min\.js">[\s\S]*?</script>'
    content = re.sub(pattern_head_corrupt, '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>', content)

    pattern_early_script = r'<script>\s*// ==========================================================================\s*// SENTINEL AI COPILOT CHATBOT LOGIC[\s\S]*?</script>'
    content = re.sub(pattern_early_script, '', content)

    # 2. Complete, robust Chatbot JS implementation to place before </body>
    chatbot_js_clean = """
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
                win.style.display = 'flex';
                const inp = document.getElementById('chatInput');
                if (inp) setTimeout(() => inp.focus(), 100);
            } else {
                win.classList.remove('active');
                win.style.display = 'none';
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
            }, 300);
        }

        function generateSentinelResponse(query) {
            const q = query.toLowerCase();

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

            // 1. Classification Roadmap & Pipeline
            if (q.includes('roadmap') || q.includes('flowchart') || q.includes('pipeline') || q.includes('classify') || q.includes('how we find') || q.includes('stages')) {
                return `
                    <p><strong>🗺️ End-to-End Classification Pipeline:</strong></p>
                    <p>Sentinel identifies illicit transfers via a <strong>6-stage visual pipeline</strong>:</p>
                    <ol style="margin-left: 18px; margin-bottom: 8px;">
                        <li><strong>1. Stream Ingestion:</strong> Ingests 954,393 transactions (0.13% base fraud rate).</li>
                        <li><strong>2. Leak-Free Time Split:</strong> Historical training on $t \\le 333$, zero-leakage evaluation on $t \\in [334, 742]$.</li>
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
                    <p>Sentinel defends capital across <strong>5 Core Defense Pillars</strong>:</p>
                    <ul style="margin-left: 16px; margin-bottom: 8px;">
                        <li><strong>⚡ Automated Circuit Breakers:</strong> Sub-second auto-freezes on transfers with score $\\theta > 0.85$ or balance drains $>90\\%$.</li>
                        <li><strong>🕸️ Graph Mule Interception:</strong> Blocks <code>TRANSFER</code> $\\to$ <code>CASH_OUT</code> pairs before cash extraction at ATMs.</li>
                        <li><strong>🤖 Multi-Agent SLAs:</strong> Autonomous dossiers synthesized under a 2-minute response SLA.</li>
                        <li><strong>⚖️ Dynamic Cost Optimization:</strong> $\\theta^* = 0.50$ balances review costs ($C_{\\text{review}}$) against fraud leakage.</li>
                        <li><strong>📜 Regulatory Compliance Shield:</strong> Immutable audit logs prevent Paytm-style RBI regulatory shutdowns.</li>
                    </ul>
                    <button class="chat-action-btn" onclick="goToStep(7);">🛡️ Jump to Step 7 Risk Mitigation</button>
                `;
            }

            // 3. Strictness Threshold & Review Cost
            if (q.includes('threshold') || q.includes('strictness') || q.includes('theta') || q.includes('cost') || q.includes('review cost') || q.includes('optimal')) {
                return `
                    <p><strong>⚖️ Strictness Threshold ($\\theta$) & Review Cost:</strong></p>
                    <p><strong>Strictness Threshold ($\\theta$):</strong> The probability cutoff above which transactions are flagged for quarantine. Low $\\theta$ catches more fraud but triggers false alarms; high $\\theta$ reduces false alarms but risks fraud leakage.</p>
                    <p><strong>Review Cost ($C_{\\text{review}}$):</strong> The operational expense to manually verify flagged alerts ($500 CU/alert default).</p>
                    <div style="margin-top:6px;">
                        <button class="chat-action-btn" onclick="applyPresetThreshold(0.50);">⚖️ Set Strictness (θ = 0.50)</button>
                        <button class="chat-action-btn" onclick="goToStep(5);">🎯 View Financial Cost Curve</button>
                    </div>
                `;
            }

            // 4. Paytm Case Study & Market Link
            if (q.includes('paytm') || q.includes('market') || q.includes('compliance') || q.includes('rbi') || q.includes('equity') || q.includes('stock')) {
                return `
                    <p><strong>📉 Market Impact & The Paytm Regulatory Precedent:</strong></p>
                    <p>On January 31, 2024, the Reserve Bank of India (RBI) directed Paytm Payments Bank to halt onboarding and deposits following persistent KYC violations and lack of real-time AML graph surveillance.</p>
                    <p><strong>Financial Impact:</strong> Paytm equity dropped <strong>-42.4%</strong> (₹761.20 ➔ ₹438.50) while volatility surged +48.4% (44.6% ➔ 66.2%).</p>
                    <button class="chat-action-btn" onclick="goToStep(8);">📉 Jump to Step 8 Market Impact</button>
                `;
            }

            // 5. 3D Ledger City Simulation
            if (q.includes('city') || q.includes('3d') || q.includes('simulation') || q.includes('radar') || q.includes('camera') || q.includes('drone')) {
                return `
                    <p><strong>🏙️ 3D Real-Time Ledger City Simulation:</strong></p>
                    <p>Experience transactions moving across 8 financial districts in a cybernetic 3D digital twin. Features walking humanoid mule actors and autonomous Sentinel drone patrols.</p>
                    <p><strong>Available Camera Presets:</strong> Top Bird's Eye, 90° Top-Down Radar, Isometric, and Street level.</p>
                    <button class="chat-action-btn" onclick="openSentinelCity(); toggleChat();">🏙️ Launch 3D Ledger City</button>
                `;
            }

            // 6. Live Patrol & Cases
            if (q.includes('patrol') || q.includes('case') || q.includes('dossier') || q.includes('live') || q.includes('ticker') || q.includes('step 9')) {
                return `
                    <p><strong>⏱️ Live Patrol & Case File Dossiers:</strong></p>
                    <p>Inspect precomputed multi-agent case dossiers across 389 alert incidents (258 Held, 131 Escalated) with live hourly transaction tickers.</p>
                    <button class="chat-action-btn" onclick="goToStep(9);">⏱️ Jump to Live Patrol & Cases</button>
                `;
            }

            // 7. Specific Account / Fraud query
            if (q.includes('c123') || q.includes('account') || q.includes('drain') || q.includes('transfer') || q.includes('cash_out')) {
                return `
                    <p><strong>🔍 Account Forensic Analysis:</strong></p>
                    <p>Typical fraud in PaySim follows an account takeover pattern:</p>
                    <ul style="margin-left: 16px; margin-bottom: 6px;">
                        <li><strong>Vector 1:</strong> Rapid <code>TRANSFER</code> draining 100% of origin balance.</li>
                        <li><strong>Vector 2:</strong> Immediate paired <code>CASH_OUT</code> at an external mule node.</li>
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
    """

    # Remove any existing chatbot block at the bottom and re-insert cleanly
    pattern_bottom_chat = r'// ==========================================================================\s*// SENTINEL AI COPILOT CHATBOT LOGIC[\s\S]*?</script>'
    content = re.sub(pattern_bottom_chat, '', content)

    # Insert chatbot JS cleanly before </script>
    content = content.replace("</script>\n</body>", chatbot_js_clean.strip() + "\n    </script>\n</body>")

    with open("src/build_mission8_dashboard.py", "w", encoding="utf-8") as f:
        f.write(content)

    print("Cleaned and restored chatbot implementation.")

if __name__ == "__main__":
    main()
