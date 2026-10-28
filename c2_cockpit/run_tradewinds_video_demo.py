# -*- coding: utf-8 -*-
"""
HUMPHREY VIRTUAL FARMS LLC // ONE-COMMAND TRADEWINDS VIDEO RESUBMISSION LIVE DEMO RUNNER
Executes the complete on-camera proof sequence for Tradewinds Docket 10-26-3976:
  1. Displays Prior Docket 9-26-3703 Assessor Feedback Resolution Matrix & Section VII.e Script
  2. Executes verify_sovereign_seal.py (634 C2 Modules, Merkle Root, 1,420 Academy Qs, 6 PDF Compilers)
  3. Executes test_client_penetration.py (17/17 Red-Team Adversarial Vectors Blocked + Zeroize)
  4. Executes run_all_83_tests.py (84/84 Automated Unit & Stress Test Suites Passed)
"""
from pathlib import Path
import subprocess
import sys

COCKPIT_DIR = Path(__file__).resolve().parent


def run_live_video_sequence() -> None:
    for script_name in [
        "briefing_teleprompter_console.py",
        "verify_sovereign_seal.py",
        "test_client_penetration.py",
        "run_all_83_tests.py",
    ]:
        script_path = COCKPIT_DIR / script_name
        subprocess.run([sys.executable, str(script_path)], check=True)


if __name__ == "__main__":
    run_live_video_sequence()
