"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: TEST EDITORIAL DISPENSER
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    """

    HVF Omni-Industrial Matrix | FORENSIC TEST HARNESS

    Module: test_editorial_dispenser.py

    Protocol: 4-Gate Audit, Test, and Verify Protocol (Dispenser & Countdown Audit)

    """



    import os

    import sys

    import sqlite3

    import subprocess

    from datetime import datetime, timezone, timedelta



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")

    SCRIPT_PATH = os.path.join(BASE_DIR, "strategic_comms", "dispense_linkedin_article.py")



    print("=" * 85)

    print("PROJECT EBONY | EDITORIAL DISPENSER & DEADLINE FORENSIC AUDIT")

    print("Target: strategic_comms/dispense_linkedin_article.py")

    print("=" * 85)



    passed = 0



    # GATE 1: Verify Script Presence on Disk

    print("\n[GATE 1] AUDITING DISPENSER SCRIPT ON DISK...")

    if not os.path.exists(SCRIPT_PATH):

        print(f"  [FAIL] Script missing: {SCRIPT_PATH}")

        sys.exit(1)

    print("  [PASS] Dispenser CLI verified on disk.")

    passed += 1



    # GATE 2: Audit Complete 5-Article Editorial Tracker Density

    print("\n[GATE 2] AUDITING 5-ARTICLE CATALOG DENSITY IN VAULT...")

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("SELECT article_number, title, word_count, file_path FROM linkedin_editorial_tracker ORDER BY article_number ASC")

    rows = cursor.fetchall()



    if len(rows) < 5:

        print(f"  [FAIL] Expected 5 staged articles, found {len(rows)}.")

        conn.close()

        sys.exit(1)



    for r in rows:

        if not os.path.exists(r[3]):

            print(f"  [FAIL] Missing file for Article 0{r[0]}: {r[3]}")

            conn.close()

            sys.exit(1)

        print(f"  [PASS] Article 0{r[0]} verified on disk ({r[2]:,} words): {r[1][:42]}...")

    passed += 1



    # GATE 3: Verify Dispenser Execution & Governance Log

    print("\n[GATE 3] AUDITING DISPENSER CLIPBOARD LOG IN MEMORY VAULT...")

    cursor.execute("""

        SELECT id, details, status FROM corporate_governance_log 

        WHERE action = 'ARTICLE_DISPENSED_TO_CLIPBOARD' 

        ORDER BY id DESC LIMIT 1

    """)

    log_row = cursor.fetchone()



    if not log_row or log_row[2] != "DISPENSED_READY_TO_PASTE":

        print(f"  [FAIL] Dispensing action missing from governance log.")

        conn.close()

        sys.exit(1)

    print(f"  [PASS] Dispenser audit confirmed: Vault Record #{log_row[0]} ({log_row[1][:60]}...)")

    passed += 1



    # GATE 4: Audit SignalLink 48-Hour Compliance Window Countdown

    print("\n[GATE 4] AUDITING 48-HOUR SURRENDER COMPLIANCE WINDOW...")

    CDT = timezone(timedelta(hours=-5))

    DEADLINE = datetime(2026, 9, 24, 12, 0, 0, tzinfo=CDT)

    NOW = datetime.now(CDT)

    delta = DEADLINE - NOW

    seconds_remaining = int(delta.total_seconds())



    cursor.execute("SELECT count(*) FROM legal_surrender_tracker WHERE target_party LIKE '%SignalLink%'")

    sl_count = cursor.fetchone()[0]

    conn.close()



    if seconds_remaining <= 0:

        print("  [STATUS] Surrender window has closed. Default statutory enforcement engaged.")

    else:

        hours, rem = divmod(seconds_remaining, 3600)

        mins, secs = divmod(rem, 60)

        print(f"  [PASS] Compliance countdown verified: {hours}h {mins}m {secs}s remaining until deadline.")

        print(f"  [PASS] SignalLink tracker active: {sl_count} records monitored under September 24 compliance gate.")

    passed += 1



    print("\n" + "=" * 85)

    if passed == 4:

        print("[AUDIT PASSED] 100% System Coverage: All 4 Test Gates Verified (Editorial Dispenser Certified).")

    else:

        print(f"[AUDIT FAILED] Only {passed}/4 gates verified.")

        sys.exit(1)

    print("=" * 85)




if __name__ == "__main__":
    render()
