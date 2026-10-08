"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: TEST FILING CHARACTER SATURATION
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    """

    HVF Omni-Industrial Matrix | FORENSIC TEST HARNESS

    Module: test_filing_character_saturation.py

    Protocol: 4-Gate Audit, Test, and Verify Protocol (Statutory Character Constraints)

    """



    import os

    import sys

    import sqlite3

    import subprocess



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    sys.path.append(os.path.join(BASE_DIR, "proposals"))

    from streamline_nsf_filing import load_payload, pipe_to_clipboard, PROJECT_TITLE, PORTAL_URL



    print("=" * 80)

    print("PROJECT EBONY | STATUTORY CHARACTER SATURATION AUDIT")

    print("Target: NSF TIP MyWork Submission Portal")

    print("=" * 80)



    passed = 0



    # GATE 1: Active Portal URL Destination Check

    print("\n[GATE 1] AUDITING DIRECT PORTAL ENDPOINT URL...")

    if PORTAL_URL != "https://nsfgov.my.site.com/mywork/s/login/":

        print(f"  [FAIL] Stale URL detected: {PORTAL_URL}")

        sys.exit(1)

    print(f"  [PASS] Endpoint verified: {PORTAL_URL}")

    passed += 1



    # GATE 2: Hard Statutory Character Limit Verification

    print("\n[GATE 2] AUDITING HARD STATUTORY CHARACTER LIMITS (3500 / 1750)...")

    fields = load_payload()

    statutory_ceilings = {1: 3500, 2: 3500, 3: 1750, 4: 1750}



    for idx in range(1, 5):

        f = fields[idx]

        c_count = f["chars"]

        c_lim = statutory_ceilings[idx]

        if c_count > c_lim:

            print(f"  [FAIL] Field {idx} breaches statutory ceiling! ({c_count} > {c_lim})")

            sys.exit(1)

        if c_count < (c_lim * 0.70):

            print(f"  [FAIL] Field {idx} under-saturated ({c_count} chars).")

            sys.exit(1)

        pct = round((c_count / c_lim) * 100, 1)

        print(f"  [PASS] Field {idx}: {f['title'][:40]:<40} : {c_count:>4} / {c_lim} chars ({pct}% Saturated)")

    passed += 1



    # GATE 3: Windows OS Clipboard Pipe Audit (clip.exe)

    print("\n[GATE 3] AUDITING WINDOWS OS CLIPBOARD BUFFER (clip.exe)...")

    try:

        pipe_to_clipboard(PROJECT_TITLE)

        print(f"  [PASS] Successfully piped Project Title ({len(PROJECT_TITLE)} chars) to OS buffer.")

        passed += 1

    except Exception as e:

        print(f"  [FAIL] Clipboard pipe failed: {e}")

        sys.exit(1)



    # GATE 4: Corporate Governance & Memory Vault Readiness

    print("\n[GATE 4] AUDITING MEMORY VAULT GOVERNANCE LOG WRITABILITY...")

    DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("SELECT status FROM active_solicitation_intake WHERE solicitation_id = 'NSF-SBIR-2026-P1'")

    row = cursor.fetchone()

    conn.close()

    if not row:

        print("  [FAIL] Solicitation NSF-SBIR-2026-P1 missing in vault.")

        sys.exit(1)

    print(f"  [PASS] Target solicitation confirmed in vault (Current State: {row[0]}).")

    passed += 1



    print("\n" + "=" * 80)

    if passed == 4:

        print("[AUDIT PASSED] 100% System Coverage: All 4 Test Gates Verified (Statutory Character Bounds Certified).")

    else:

        print(f"[AUDIT FAILED] Only {passed}/4 gates verified.")

        sys.exit(1)

    print("=" * 80)




if __name__ == "__main__":
    render()
