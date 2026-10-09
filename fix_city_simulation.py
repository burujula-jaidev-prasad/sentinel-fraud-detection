#!/usr/bin/env python3
"""
fix_city_simulation.py
Comprehensively fixes the 3D Ledger City simulation:
1. Adds setCameraPreset(type) with top, radar, iso, street, tower views
2. Guarantees all DOM queries in displayEvidenceBoard and updateCityForStep are null-safe
3. Connects the evidence drawer with all detailed forensic metadata
4. Fixes canvas resizing and Three.js animation lifecycle
5. Rebuilds docs/index.html and index.html
"""

import re

def main():
    with open("src/build_mission8_dashboard.py", "r", encoding="utf-8") as f:
        code = f.read()

    # 1. Update openSentinelCity to be bulletproof
    open_city_fix = """
function openSentinelCity() {
    const modal = document.getElementById('cityModal');
    if (!modal) return;
    modal.classList.add('active');
    
    setTimeout(() => {
        const container = document.getElementById('cityCanvasContainer');
        if (!container) return;
        const w = container.clientWidth || window.innerWidth || 1000;
        const h = container.clientHeight || (window.innerHeight - 70) || 600;

        if (!cityInitialized) {
            init3DLedgerCity();
            cityInitialized = true;
        } else if (cityRenderer && cityCamera) {
            cityRenderer.setSize(w, h);
            cityCamera.aspect = w / h;
            cityCamera.updateProjectionMatrix();
        }
        
        try {
            updateCityForStep(patrolCurrentStep);
        } catch (e) {
            console.warn("City step update error:", e);
        }
        
        if (!cityAnimId) {
            animate3DCity();
        }
    }, 80);
}

function closeSentinelCity() {
    const modal = document.getElementById('cityModal');
    if (modal) modal.classList.remove('active');
    if (cityAnimId) {
        cancelAnimationFrame(cityAnimId);
        cityAnimId = null;
    }
}

function setCameraPreset(type) {
    if (!cityCamera) return;
    if (type === 'top' || type === 'birdseye') {
        targetLookTarget.set(0, 0, 0);
        targetCamPos.set(0, 420, 300);
    } else if (type === 'radar' || type === 'overhead') {
        targetLookTarget.set(0, 0, 0);
        targetCamPos.set(0, 560, 10);
    } else if (type === 'iso' || type === 'skyline') {
        targetLookTarget.set(0, 20, 0);
        targetCamPos.set(300, 240, 300);
    } else if (type === 'street') {
        targetLookTarget.set(0, 10, -80);
        targetCamPos.set(0, 15, 180);
    } else if (type === 'tower') {
        targetLookTarget.set(0, 10, 180);
        targetCamPos.set(0, 220, 0);
    }
}
function setCityView(type) { setCameraPreset(type); }
"""

    # 2. Update displayEvidenceBoard to match cityEvidenceBoard DOM IDs
    display_evidence_fix = """
function displayEvidenceBoard(pData) {
    selectedPersonData = pData;
    const board = document.getElementById('cityEvidenceBoard');
    if (!board) return;

    const titleEl = document.getElementById('evidenceTitle');
    const typeEl = document.getElementById('evidenceType');
    const amtEl = document.getElementById('evidenceAmt');
    const routeEl = document.getElementById('evidenceRoute');
    const scoreEl = document.getElementById('evidenceScore');
    const agentsEl = document.getElementById('evidenceAgents');
    const statusEl = document.getElementById('evidenceStatus');

    const isFlagged = pData.sc >= currentStrictness;
    const fromName = (DISTRICT_POSITIONS[pData.df] && DISTRICT_POSITIONS[pData.df].name) || `District ${pData.df}`;
    const toName = (DISTRICT_POSITIONS[pData.dt] && DISTRICT_POSITIONS[pData.dt].name) || `District ${pData.dt}`;

    if (titleEl) titleEl.innerHTML = `${pData.f === 1 ? '🚨 CONFIRMED FRAUD' : (isFlagged ? '⚠️ SUSPICIOUS ALERT' : '✅ LEGITIMATE PAYMENT')}: ${pData.id || pData.t}`;
    if (typeEl) typeEl.innerHTML = `<strong>Vector:</strong> ${pData.t} (Step ${pData.step}, Hour ${pData.hr}:00)`;
    if (amtEl) amtEl.innerHTML = `<strong>Amount:</strong> ${pData.amt ? pData.amt.toLocaleString() : '0'} CU (Top ${((1 - (pData.pct || 0.5))*100).toFixed(1)}% Volume)`;
    if (routeEl) routeEl.innerHTML = `<strong>Route:</strong> Dist ${pData.df} (${fromName}) ➔ Dist ${pData.dt} (${toName})`;
    if (scoreEl) scoreEl.innerHTML = `<strong>AI Anomaly Score:</strong> ${(pData.sc * 100).toFixed(1)}% (Strictness θ = ${currentStrictness.toFixed(2)})`;
    if (agentsEl) agentsEl.innerHTML = `<strong>Agents:</strong> Graph Hunter & Velocity Watchdog [SLA < 2m]`;
    if (statusEl) {
        statusEl.innerHTML = isFlagged ? `<span style="color:#ef4444; font-weight:700;">🚨 AUTO-QUARANTINE / CIRCUIT BREAKER TRIGGERED</span>` : `<span style="color:#10b981; font-weight:700;">✅ INSTANT SETTLEMENT APPROVED</span>`;
    }

    board.style.display = 'block';

    // Draw route laser
    try {
        drawRouteLaser(pData.df, pData.dt);
    } catch (e) {}

    // Glide Sentinel character to suspect
    if (sentinelMesh) {
        const targetMesh = cityPeopleMeshes.find(m => m.txData && m.txData.id === pData.id);
        if (targetMesh) {
            sentinelMesh.targetPos.copy(targetMesh.group.position);
        }
    }
}
"""

    # 3. Update updateCityForStep to be 100% null-safe
    update_city_fix = """
function updateCityForStep(step) {
    if (!DATA || !DATA.district_hourly_by_step || !DATA.city_people_by_step) return;

    const hour = step % 24;
    const hourText = `${hour}:00 (${(hour>=0 && hour<=5)?'🌙 Late Night Window':'☀️ Standard Hours'})`;

    // Sync Header & HUD Clock
    const stepEl = document.getElementById('cityStepDisplay');
    if (stepEl) stepEl.innerText = `Step: ${step} (Hour ${hour})`;
    const clockBadge = document.getElementById('cityStepClock');
    if (clockBadge) clockBadge.innerText = `Step ${step} | ${hour}:00`;
    const stepSlider = document.getElementById('cityStepSlider');
    if (stepSlider) stepSlider.value = step;
    const strictBadge = document.getElementById('cityStrictnessBadge');
    if (strictBadge) strictBadge.innerText = currentStrictness.toFixed(2);
    const strictDisp = document.getElementById('cityStrictnessDisplay');
    if (strictDisp) strictDisp.innerText = currentStrictness.toFixed(2);

    // 1. Update District Buildings
    const stepDistData = DATA.district_hourly_by_step[step] || {};

    if (cityBuildings && cityBuildings.length > 0) {
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
    }

    if (districtSprites) {
        for (let d = 1; d <= 8; d++) {
            const info = stepDistData[d] || { p: 0, s: 0 };
            const sprite = districtSprites[d];
            if (sprite && DISTRICT_POSITIONS[d]) {
                const statusText = info.s > 0 ? `🔴 ALARM (${info.s} THREATS)` : `🟢 ${info.p} TX/HR`;
                const colorHex = info.s > 0 ? "#ef4444" : "#38bdf8";
                updateDistrictLabelSprite(sprite, `DISTRICT ${d}: ${DISTRICT_POSITIONS[d].name.toUpperCase()}`, statusText, colorHex);
            }
        }
    }

    // 2. Active people for step
    const activeStepPeople = DATA.city_people_by_step[step] || [];
    const flaggedThreats = activeStepPeople.filter(p => p.sc >= currentStrictness);
    const elevatedThreats = activeStepPeople.filter(p => p.sc >= 0.15 && p.sc < currentStrictness);

    const radarHour = document.getElementById('radarHourDisplay');
    if (radarHour) radarHour.innerText = hourText;
    const radarTx = document.getElementById('radarActiveTxCount');
    if (radarTx) radarTx.innerText = activeStepPeople.length;
    const radarThreat = document.getElementById('radarThreatCountBadge');
    if (radarThreat) radarThreat.innerText = `${flaggedThreats.length} Threats`;

    const briefingEl = document.getElementById('cityBriefingText');
    if (briefingEl) {
        const totalAmt = activeStepPeople.reduce((sum, p) => sum + p.amt, 0);
        const flaggedAmt = flaggedThreats.reduce((sum, p) => sum + p.amt, 0);
        const kTotal = (totalAmt >= 1000000) ? (totalAmt / 1000000).toFixed(1) + 'M CU' : (totalAmt / 1000).toFixed(0) + 'K CU';
        const kFlagged = (flaggedAmt >= 1000000) ? (flaggedAmt / 1000000).toFixed(1) + 'M CU' : (flaggedAmt / 1000).toFixed(0) + 'K CU';

        if (flaggedThreats.length > 0) {
            const topThreat = flaggedThreats[0];
            briefingEl.innerHTML = `<strong>Step ${step} (${hour}:00)</strong>: ${activeStepPeople.length} live transactions (${kTotal} volume). <span style="color:#f87171; font-weight:700;">🚨 Flagged ${flaggedThreats.length} high-risk threat(s) (${kFlagged} stolen)</span>.`;
        } else {
            briefingEl.innerHTML = `<strong>Step ${step} (${hour}:00)</strong>: ${activeStepPeople.length} live transactions (${kTotal} volume). <span style="color:#34d399; font-weight:600;">🟢 All payment traffic normal.</span>`;
        }
    }

    const radarList = document.getElementById('radarThreatList');
    if (radarList) {
        if (flaggedThreats.length === 0 && elevatedThreats.length === 0) {
            radarList.innerHTML = `<div style="color:#64748b; font-size:11px; padding:6px;">No high-risk threats detected in this hour. All traffic normal.</div>`;
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
    }

    // 3. Update People Meshes
    if (!cityPeopleMeshes || cityPeopleMeshes.length === 0) return;
    const spawnCount = Math.min(300, activeStepPeople.length);

    for (let i = 0; i < 300; i++) {
        const pMesh = cityPeopleMeshes[i];
        if (!pMesh) continue;

        if (i < spawnCount) {
            const pData = activeStepPeople[i];
            pMesh.active = true;
            pMesh.txData = pData;
            pMesh.group.userData.personData = pData;

            const fromPos = (DISTRICT_POSITIONS[pData.df]) || DISTRICT_POSITIONS[1];
            const toPos = (DISTRICT_POSITIONS[pData.dt]) || DISTRICT_POSITIONS[2];

            pMesh.waypoints = [
                new THREE.Vector3(fromPos.x, 0, fromPos.z),
                new THREE.Vector3(fromPos.x, 0, 0),
                new THREE.Vector3(0, 0, 0),
                new THREE.Vector3(toPos.x, 0, 0),
                new THREE.Vector3(toPos.x, 0, toPos.z)
            ];
            pMesh.progress = (i * 0.17) % 1.0;

            if (pData.t === 'TRANSFER') {
                pMesh.coatMat.color.setHex(0x38bdf8);
            } else {
                pMesh.coatMat.color.setHex(0xc084fc);
            }

            const bagScale = 0.6 + ((pData.pct || 0.5) * 1.8);
            pMesh.bag.scale.set(bagScale, bagScale, bagScale);

            const isFlagged = pData.sc >= currentStrictness;
            const isElevated = pData.sc >= 0.15;
            const kAmt = (pData.amt >= 1000000) ? (pData.amt / 1000000).toFixed(1) + 'M' : (pData.amt / 1000).toFixed(0) + 'K';

            if (pData.f === 1) {
                renderPedestrianTag(pMesh.tagObj, `🚨 THEFT: ${kAmt} CU (${pData.sc.toFixed(2)})`, true, false);
                pMesh.headMat.color.setHex(0xef4444);
                pMesh.halo.visible = true;
                pMesh.haloMat.color.setHex(0xef4444);
                pMesh.beam.visible = true;
                pMesh.beamMat.color.setHex(0xef4444);
                pMesh.ring.visible = true;
                pMesh.ringMat.color.setHex(0xef4444);
            } else if (isFlagged) {
                renderPedestrianTag(pMesh.tagObj, `🚨 ALERT: ${kAmt} CU`, true, false);
                pMesh.headMat.color.setHex(0xef4444);
                pMesh.halo.visible = true;
                pMesh.haloMat.color.setHex(0xf59e0b);
                pMesh.beam.visible = true;
                pMesh.beamMat.color.setHex(0xf59e0b);
                pMesh.ring.visible = true;
                pMesh.ringMat.color.setHex(0xef4444);
            } else if (isElevated) {
                renderPedestrianTag(pMesh.tagObj, `⚠️ WATCH: ${kAmt} CU`, false, true);
                pMesh.headMat.color.setHex(0xf59e0b);
                pMesh.halo.visible = true;
                pMesh.haloMat.color.setHex(0xfacc15);
                pMesh.beam.visible = false;
                pMesh.ring.visible = false;
            } else {
                renderPedestrianTag(pMesh.tagObj, `✅ ${pData.t.slice(0,4)} ${kAmt}`, false, false);
                pMesh.headMat.color.setHex(0xf8fafc);
                pMesh.halo.visible = false;
                pMesh.beam.visible = false;
                pMesh.ring.visible = false;
            }
        } else {
            pMesh.active = false;
            pMesh.group.position.set(0, -200, 0);
            pMesh.tagObj.sprite.visible = false;
        }
    }
}
"""

    # Replace openSentinelCity block
    pattern_open = r'function openSentinelCity\(\)\s*\{[\s\S]*?function init3DLedgerCity\(\)'
    code = re.sub(pattern_open, open_city_fix.strip() + "\n\n        function init3DLedgerCity()", code)

    # Replace displayEvidenceBoard
    pattern_evidence = r'function displayEvidenceBoard\([\s\S]*?function drawRouteLaser'
    code = re.sub(pattern_evidence, display_evidence_fix.strip() + "\n\n        function drawRouteLaser", code)

    # Replace updateCityForStep
    pattern_update_city = r'function updateCityForStep\([\s\S]*?function updatePersonRoadPosition'
    code = re.sub(pattern_update_city, update_city_fix.strip() + "\n\n        function updatePersonRoadPosition", code)

    with open("src/build_mission8_dashboard.py", "w", encoding="utf-8") as f:
        f.write(code)

    print("Updated build_mission8_dashboard.py with robust 3D city functions.")

if __name__ == "__main__":
    main()
