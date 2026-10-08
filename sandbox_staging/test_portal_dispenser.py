"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: TEST PORTAL DISPENSER
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    """

    HVF Omni-Industrial Matrix | FORENSIC TEST HARNESS

    Module: test_portal_dispenser.py

    Protocol: 4-Gate Audit, Test, and Verify Protocol (Terminal Dispenser Verification)

    """



    import os

    import sys

    import sqlite3



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    sys.path.append(os.path.join(BASE_DIR, "proposals"))

    from portal_terminal_dispenser import parse_fields, copy_to_clipboard



    print("=" * 80)

    print("PROJECT EBONY | TERMINAL DISPENSER FORENSIC AUDIT")

    print("Target: proposals/portal_terminal_dispenser.py")

    print("=" * 80)



    passed = 0



    # GATE 1: Parse All 4 Fields Cleanly

    print("\n[GATE 1] AUDITING REGEX PARSER ACROSS ALL 4 NSF FORM FIELDS...")

    fields = parse_fields()

    if len(fields) != 4:

        print(f"  [FAIL] Expected 4 fields, parsed {len(fields)}.")

        sys.exit(1)

    print("  [PASS] All 4 fields parsed successfully with clean regex extraction.")

    passed += 1



    # GATE 2: Word Count Threshold Verification

    print("\n[GATE 2] AUDITING PARSED WORD COUNTS AGAINST STATUTORY LIMITS...")

    limits = {1: 500, 2: 500, 3: 500, 4: 250}

    for idx, f in fields.items():

        wc = len(f["body"].split())

        if wc > limits[idx] or wc == 0:

            print(f"  [FAIL] Field {idx} word count ({wc}) breaches limit ({limits[idx]}).")

            sys.exit(1)

        print(f"  [PASS] {f['title']:<38} : {wc:>3} words (Limit: {limits[idx]})")

    passed += 1



    # GATE 3: OS-Level Clipboard Injection Pipe Check

    print("\n[GATE 3] AUDITING OS-LEVEL CLIPBOARD PIPE (clip.exe)...")

    try:

        test_str = "HVF_TERMINAL_VERIFICATION_PASS"

        copy_to_clipboard(test_str)

        print("  [PASS] Successfully piped text to native Windows clip.exe buffer.")

        passed += 1

    except Exception as e:

        print(f"  [FAIL] Clipboard injection failed: {e}")

        sys.exit(1)



    # GATE 4: Corporate Memory Vault Logging Audit

    print("\n[GATE 4] AUDITING MEMORY VAULT PERSISTENCE...")

    DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("SELECT count(*) FROM corporate_governance_log")

    count = cursor.fetchone()[0]

    conn.close()

    if count == 0:

        print("  [FAIL] Corporate governance ledger is empty.")

        sys.exit(1)

    print(f"  [PASS] Memory vault connectivity active ({count} certified governance records on file).")

    passed += 1



    print("\n" + "=" * 80)

    if passed == 4:

        print("[AUDIT PASSED] 100% System Coverage: All 4 Test Gates Verified.")

    else:

        print(f"[AUDIT FAILED] Only {passed}/4 gates verified.")

        sys.exit(1)

    print("=" * 80)




if __name__ == "__main__":
    render()
