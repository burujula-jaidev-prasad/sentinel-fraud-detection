#!/usr/bin/env python3
"""
patch_dashboard_with_chatbot.py
Updates build_mission8_dashboard.py to incorporate:
1. Sentinel AI Copilot Chatbot (Floating widget + AI response engine + action buttons + natural language Q&A)
2. Verified 3D Ledger City Modal container
3. Full integration with all dashboard state and controllers
"""

import sys
import re

def main():
    with open("src/build_mission8_dashboard.py", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Chatbot CSS
    chatbot_css = """
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
    """

    # Chatbot HTML markup
    chatbot_html = """
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
                    <p>I can explain our <strong>classification pipeline</strong>, details on <strong>752.38M CU in protected funds</strong>, optimal strictness thresholds ($\theta^*$), mule laundering rings, or guide you across any story step.</p>
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
    """

    # Chatbot JavaScript Engine
    chatbot_js = """
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
                        <li><strong>2. Leak-Free Time Split:</strong> Historical training on $t \\le 600$, zero-leakage evaluation on $t > 600$.</li>
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
                    <p><strong>Review Cost ($C_{\\text{review}}$):</strong> The operational expense to manually verify flagged alerts ($500 CU/alert default). Sentinel finds the mathematical minimum total cost $\\theta^* = 0.50$.</p>
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
    """

    # Inject CSS
    if "/* SENTINEL AI COPILOT CHATBOT STYLES */" not in content:
        content = content.replace("</style>", chatbot_css + "\n    </style>")

    # Inject HTML
    if "id=\"sentinelChatTrigger\"" not in content:
        content = content.replace("</main>", "</main>\n" + chatbot_html)

    # Inject JS
    if "function toggleChat()" not in content:
        content = content.replace("</script>", chatbot_js + "\n    </script>")

    with open("src/build_mission8_dashboard.py", "w", encoding="utf-8") as f:
        f.write(content)

    print("Successfully patched build_mission8_dashboard.py with Sentinel AI Copilot Chatbot and 3D Modal markup!")

if __name__ == "__main__":
    main()
