#!/usr/bin/env python3
"""
fix_numbers_strictly.py
Updates numbers strictly based on source data files:
1. Market Link: Volatility 44.6% -> 66.2% (+48.4% surge), Beta 0.91 -> 0.87, R² 4.4% -> 3.4%, Price 761.20 (31 Jan 2024) -> 438.50 (5 Feb 2024), -42.4%.
2. Escalated & Held counts from outputs/replay_alerts.csv:
   - Balanced (default): 258 Held, 131 Escalated
   - Strict: 1,977 Held, 453 Escalated
   - Lenient: 0 Held, 85 Escalated
3. Step range text: 334 to 742
"""

import re

def main():
    with open("src/build_mission8_dashboard.py", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Step Range Replacements (334 to 742)
    content = content.replace("steps 334–743", "steps 334 to 742")
    content = content.replace("steps 334-743", "steps 334 to 742")
    content = content.replace("(334–743)", "(steps 334 to 742)")
    content = content.replace("across 743 hours", "across 742 hours")

    # 2. Market Link KPI Card numbers in Step 8
    # Card 1: Equity destruction (-42.4% Drawdown, 761.20 to 438.50)
    old_market_card1 = """                <div class="story-card" style="border-left: 4px solid #ef4444; padding: 14px;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Equity Destruction</div>
                    <div style="font-size: 24px; font-weight: 800; color: #ef4444; margin: 4px 0;">-55.1% Drawdown</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">~₹25,000 Cr market cap erased in under 3 weeks post-RBI order.</div>
                </div>"""

    new_market_card1 = """                <div class="story-card" style="border-left: 4px solid #ef4444; padding: 14px;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Equity Destruction</div>
                    <div style="font-size: 24px; font-weight: 800; color: #ef4444; margin: 4px 0;">-42.4% Drawdown</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">₹761.20 (31 Jan 2024) ➔ ₹438.50 (5 Feb 2024) post-RBI directive.</div>
                </div>"""

    # Card 2: Volatility (44.6% to 66.2%, +48.4% surge)
    old_market_card2 = """                <div class="story-card" style="border-left: 4px solid #f59e0b; padding: 14px;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Volatility Explosion</div>
                    <div style="font-size: 24px; font-weight: 800; color: #f59e0b; margin: 4px 0;">25.8% ➔ 78.7%</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">+305% annualized volatility surge as risk premia expanded.</div>
                </div>"""

    new_market_card2 = """                <div class="story-card" style="border-left: 4px solid #f59e0b; padding: 14px;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Volatility Explosion</div>
                    <div style="font-size: 24px; font-weight: 800; color: #f59e0b; margin: 4px 0;">44.6% ➔ 66.2%</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">+48.4% annualized volatility surge as risk premia expanded.</div>
                </div>"""

    # Card 3: Market Beta (0.91 to 0.87)
    old_market_card3 = """                <div class="story-card" style="border-left: 4px solid #38bdf8; padding: 14px;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Market Beta Spike</div>
                    <div style="font-size: 24px; font-weight: 800; color: #38bdf8; margin: 4px 0;">0.66 ➔ 2.02</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">Shifted from defensive tech utility to high-beta distressed asset.</div>
                </div>"""

    new_market_card3 = """                <div class="story-card" style="border-left: 4px solid #38bdf8; padding: 14px;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Market Beta Spike</div>
                    <div style="font-size: 24px; font-weight: 800; color: #38bdf8; margin: 4px 0;">0.91 ➔ 0.87</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">Covariance shift against broader benchmark index.</div>
                </div>"""

    # Card 4: R-squared (4.4% to 3.4%)
    old_market_card4 = """                <div class="story-card" style="border-left: 4px solid #10b981; padding: 14px;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Benchmark Decoupling</div>
                    <div style="font-size: 24px; font-weight: 800; color: #34d399; margin: 4px 0;">-56.9% Alpha Gap</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">NIFTY 50 remained stable (+1.8%) confirming 100% compliance cause.</div>
                </div>"""

    new_market_card4 = """                <div class="story-card" style="border-left: 4px solid #10b981; padding: 14px;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Benchmark Decoupling</div>
                    <div style="font-size: 24px; font-weight: 800; color: #34d399; margin: 4px 0;">4.4% ➔ 3.4% R²</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">R-squared decoupling confirming firm-specific regulatory shock.</div>
                </div>"""

    content = content.replace(old_market_card1, new_market_card1)
    content = content.replace(old_market_card2, new_market_card2)
    content = content.replace(old_market_card3, new_market_card3)
    content = content.replace(old_market_card4, new_market_card4)

    # 3. Market Link Card 11 Headline in JS
    old_c11_headline = "document.getElementById('c11Headline').innerText = `Post-RBI supervisory action, Paytm equity dropped ~55%; annualized volatility surged from ${preVol}% to ${postVol}% while market beta rose from ${betaPre} to ${betaPost}.`;"
    new_c11_headline = "document.getElementById('c11Headline').innerText = `Post-RBI supervisory action, Paytm equity dropped -42.4% (₹761.20 to ₹438.50); annualized volatility surged from 44.6% to 66.2% (+48.4% surge) with market beta at 0.91 to 0.87 and R-squared shifting from 4.4% to 3.4%.`;"

    content = content.replace(old_c11_headline, new_c11_headline)

    # 4. Case File Dossier Explorer & Risk Officer Decision Counts in Step 9
    # Add explicit Held & Escalated breakdown display for Risk Officer Decisions in Step 9
    old_case_filter_bar = """                        <button class="btn btn-secondary active" id="caseFilterFraudBtn" onclick="filterCases('fraud')" style="padding:4px 10px; font-size:11px; background:rgba(239,68,68,0.2); color:#fca5a5; border-color:#ef4444;">🚨 Confirmed Frauds (210)</button>
                        <button class="btn btn-secondary" id="caseFilterFpBtn" onclick="filterCases('fp')" style="padding:4px 10px; font-size:11px; background:rgba(245,158,11,0.15); color:#fde68a; border-color:#f59e0b;">⚠️ False Alarms (179)</button>
                        <button class="btn btn-secondary" id="caseFilterAllBtn" onclick="filterCases('all')" style="padding:4px 10px; font-size:11px;">All Alerts (389)</button>"""

    new_case_filter_bar = """                        <button class="btn btn-secondary active" id="caseFilterFraudBtn" onclick="filterCases('fraud')" style="padding:4px 10px; font-size:11px; background:rgba(239,68,68,0.2); color:#fca5a5; border-color:#ef4444;">🚨 Confirmed Frauds (210)</button>
                        <button class="btn btn-secondary" id="caseFilterFpBtn" onclick="filterCases('fp')" style="padding:4px 10px; font-size:11px; background:rgba(245,158,11,0.15); color:#fde68a; border-color:#f59e0b;">⚠️ False Alarms (179)</button>
                        <button class="btn btn-secondary" id="caseFilterAllBtn" onclick="filterCases('all')" style="padding:4px 10px; font-size:11px;">All Alerts (389: 258 Held, 131 Escalated)</button>"""

    content = content.replace(old_case_filter_bar, new_case_filter_bar)

    with open("src/build_mission8_dashboard.py", "w", encoding="utf-8") as f:
        f.write(content)

    print("Successfully updated numbers in src/build_mission8_dashboard.py")

if __name__ == "__main__":
    main()
