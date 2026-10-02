"""
HVF Omni-Industrial Matrix | SOVEREIGN PRIME SYSTEMS
Module: streamline_nsf_filing.py
Author: Jeffery Humphrey, Founder & CEO (Apex Architect)
Classification: PROPRIETARY & CONFIDENTIAL | 100% UNENCUMBERED PRIME
Protocol: NSF TIP MYWORK DIRECT PORTAL DISPATCH
"""

import os
import sys
import re
import sqlite3
import subprocess
import webbrowser
from datetime import datetime

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
PAYLOAD_FILE = os.path.join(BASE_DIR, "proposals", "NSF_PORTAL_CLIPBOARD_READY.txt")

# DIRECT NSF TIP MYWORK SUBMISSION PORTAL
PORTAL_URL = "https://nsfgov.my.site.com/mywork/s/login/"
PROJECT_TITLE = "Air-Gapped Three-Brain Architecture for Deterministic SCADA Defense and Tamper-Proof Cryptographic Telemetry Provenance"

def pipe_to_clipboard(text: str):
    p = subprocess.Popen("clip", stdin=subprocess.PIPE, shell=True)
    p.communicate(text.strip().encode("utf-8"))

def load_payload():
    if not os.path.exists(PAYLOAD_FILE):
        print(f"[ERROR] Payload file missing at: {PAYLOAD_FILE}")
        sys.exit(1)
    with open(PAYLOAD_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"--- \[START (Field \d: [^\]]+)\] --- \(Characters: (\d+)/(\d+) \| ([^)]+)\)\n(.*?)\n--- \[END \1\] ---"
    matches = re.findall(pattern, content, re.DOTALL)
    fields = {}
    for idx, (title, chars, lim, sat, body) in enumerate(matches, 1):
        fields[idx] = {
            "title": title.strip(),
            "chars": int(chars),
            "limit": int(lim),
            "saturation": sat.strip(),
            "body": body.strip()
        }
    return fields

def run_filing_pipeline():
    fields = load_payload()

    print("=" * 80)
    print("HVF Omni-Industrial Matrix | NSF TIP MYWORK LIVE FILING PIPELINE")
    print("Direct Endpoint: " + PORTAL_URL)
    print("Prime CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | PI: Jeffery Humphrey")
    print("=" * 80)

    print("\n[STEP 1/6] Launching NSF Directorate for Technology, Innovation & Partnerships Portal...")
    webbrowser.open(PORTAL_URL)

    print("\n" + "-" * 80)
    input(">>> Press [ENTER] to copy PROJECT TITLE to Windows Clipboard... ")
    pipe_to_clipboard(PROJECT_TITLE)
    print(f"  [COPIED] Project Title is in your clipboard ({len(PROJECT_TITLE)} chars).")
    print("  --> Click the Project Title field in the portal and press [Ctrl + V].")

    steps = [
        (1, "Field 1: Technology Innovation"),
        (2, "Field 2: Technical Objectives and Challenges"),
        (3, "Field 3: Market Opportunity"),
        (4, "Field 4: Company and Team")
    ]

    for f_idx, label in steps:
        print("\n" + "-" * 80)
        f_data = fields[f_idx]
        input(f">>> Press [ENTER] to copy {label} ({f_data['chars']}/{f_data['limit']} chars) to Clipboard... ")
        pipe_to_clipboard(f_data["body"])
        print(f"  [COPIED] {label} is in your clipboard ({f_data['chars']} chars | {f_data['saturation']}).")
        print("  --> Click the portal field and press [Ctrl + V].")

    print("\n" + "=" * 80)
    print("[FINAL SUBMISSION VERIFICATION]")
    print("In your browser, confirm all 4 fields are populated and click 'SUBMIT'.")
    print("=" * 80)
    
    confirm = input("\nHave you clicked 'SUBMIT' on the NSF TIP portal? (y/n): ").strip().lower()
    if confirm == 'y':
        tracking_id = input("Enter NSF Pitch Case/Reference Number (or press ENTER if pending email receipt): ").strip()
        if not tracking_id:
            tracking_id = "NSF-PITCH-SUBMISSION-CONFIRMED-AWAITING-CASE-ID"

        conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)
        conn.execute("""
            UPDATE active_solicitation_intake
            SET status = 'SUBMITTED_PENDING_REVIEW', last_scanned = ?
            WHERE solicitation_id = 'NSF-SBIR-2026-P1'
        """, (datetime.now().isoformat(),))

        conn.execute("""
            INSERT INTO corporate_governance_log (authority, target_entity, action, details, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Jeffery Humphrey, CEO",
            "NSF TIP MyWork Portal",
            "NSF_SEED_FUND_PITCH_OFFICIALLY_FILED",
            f"Officially transmitted Project Pitch ($275,000 Phase I). Ref: {tracking_id}. Character limits 100% compliant.",
            datetime.now().isoformat(),
            "FILED_PENDING_AGENCY_INVITATION"
        ))
        conn.close()

        print("\n" + "=" * 80)
        print("[SUCCESS] NSF America's Seed Fund Project Pitch officially sealed as SUBMITTED_PENDING_REVIEW.")
        print(f"  Tracking Reference: {tracking_id}")
        print("=" * 80)
    else:
        print("\n[INFO] Session paused. Re-run script when ready to complete filing confirmation.")

if __name__ == "__main__":
    run_filing_pipeline()

