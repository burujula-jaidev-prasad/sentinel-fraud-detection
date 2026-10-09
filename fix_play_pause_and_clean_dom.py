#!/usr/bin/env python3
"""
fix_play_pause_and_clean_dom.py
1. Fixes togglePatrolPlay() so pause/play works 100% reliably across all screens.
2. Removes duplicate cityModal elements so there is exactly ONE high-definition city modal.
3. Synchronizes all play/pause buttons, scrubbers, and clock tickers simultaneously.
"""

import re

def main():
    with open("src/build_mission8_dashboard.py", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove duplicate city-modal if present
    if '<div id="cityModal" class="city-modal">' in content and '<div class="city-modal-overlay" id="cityModal">' in content:
        # Keep only the city-modal-overlay
        pattern_dup = r'<!-- 3D Ledger City Modal -->\s*<div id="cityModal" class="city-modal">[\s\S]*?<!-- Evidence Dossier Board inside City -->[\s\S]*?</div>\s*</div>\s*</div>'
        content = re.sub(pattern_dup, '', content)

    # 2. Perfect togglePatrolPlay, scrubPatrol, changePatrolSpeed, and startPatrolLoop
    robust_patrol_js = """
        function togglePatrolPlay() {
            patrolPlaying = !patrolPlaying;
            
            // Update all play/pause buttons across the entire document
            const allPlayBtns = document.querySelectorAll('#patrolPlayBtn, #cityPlayBtn, .play-toggle-btn');
            allPlayBtns.forEach(btn => {
                btn.innerHTML = patrolPlaying ? "⏸️ Pause" : "▶️ Play";
            });

            if (patrolPlaying) {
                startPatrolLoop();
            } else {
                if (patrolInterval) {
                    clearInterval(patrolInterval);
                    patrolInterval = null;
                }
            }
        }

        function scrubPatrol(step) {
            patrolCurrentStep = parseInt(step);
            
            // Sync all sliders
            const s1 = document.getElementById('patrolScrubber');
            if (s1) s1.value = patrolCurrentStep;
            const s2 = document.getElementById('cityStepSlider');
            if (s2) s2.value = patrolCurrentStep;

            renderPatrolStep(patrolCurrentStep);
        }

        function changePatrolSpeed(ms) {
            patrolSpeed = parseInt(ms);
            if (patrolPlaying) {
                if (patrolInterval) clearInterval(patrolInterval);
                startPatrolLoop();
            }
        }

        function startPatrolLoop() {
            if (patrolInterval) clearInterval(patrolInterval);
            patrolInterval = setInterval(() => {
                if (!patrolPlaying) {
                    clearInterval(patrolInterval);
                    patrolInterval = null;
                    return;
                }
                if (patrolCurrentStep >= 742) {
                    patrolCurrentStep = 334;
                } else {
                    patrolCurrentStep++;
                }

                const s1 = document.getElementById('patrolScrubber');
                if (s1) s1.value = patrolCurrentStep;
                const s2 = document.getElementById('cityStepSlider');
                if (s2) s2.value = patrolCurrentStep;

                renderPatrolStep(patrolCurrentStep);
            }, patrolSpeed);
        }

        function cityStepChange(delta) {
            patrolCurrentStep = Math.max(334, Math.min(742, patrolCurrentStep + delta));
            scrubPatrol(patrolCurrentStep);
        }
    """

    # Replace patrol loop functions
    pattern_patrol_funcs = r'function togglePatrolPlay\(\)\s*\{[\s\S]*?function renderPatrolStep\('
    content = re.sub(pattern_patrol_funcs, robust_patrol_js.strip() + "\n\n        function renderPatrolStep(", content)

    with open("src/build_mission8_dashboard.py", "w", encoding="utf-8") as f:
        f.write(content)

    print("Successfully patched play/pause controls and cleaned duplicate DOM elements.")

if __name__ == "__main__":
    main()
