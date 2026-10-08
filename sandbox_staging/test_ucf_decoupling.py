"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: TEST UCF DECOUPLING
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    """

    HVF Omni-Industrial Matrix | FORENSIC TEST HARNESS

    Module: test_ucf_decoupling.py

    Protocol: 4-Gate Audit, Test, and Verify Protocol (UCF Decoupling Certification)

    """



    import os

    import sys

    import sqlite3



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")

    MSG_FILE = os.path.join(BASE_DIR, "corporate_governance", "OUTBOUND_UCF_REPLY_MESSAGE.txt")



    print("=" * 80)

    print("PROJECT EBONY | UCF INSTITUTIONAL DECOUPLING FORENSIC AUDIT")

    print("Target: corporate_governance/log_ucf_severance_confirmation.py")

    print("=" * 80)



    passed = 0



    # GATE 1: Verify Governance Record in SQLite Vault

    print("\n[GATE 1] AUDITING UCF GOVERNANCE RECORD IN VAULT...")

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT id, details, status FROM corporate_governance_log 

        WHERE action = 'UCF_AOR_RECORD_DISCARDED_CONFIRMED' 

        ORDER BY id DESC LIMIT 1

    """)

    gov_row = cursor.fetchone()



    if not gov_row or gov_row[2] != "INSTITUTIONAL_RECORD_DISCARDED":

        print(f"  [FAIL] Missing or invalid governance record.")

        conn.close()

        sys.exit(1)

    print(f"  [PASS] Governance Record #{gov_row[0]} confirmed: Status='{gov_row[2]}'")

    passed += 1



    # GATE 2: Verify Legal Surrender Tracker Status for Wendy Land

    print("\n[GATE 2] AUDITING LEGAL SURRENDER TRACKER STATUS...")

    cursor.execute("""

        SELECT status, notes FROM legal_surrender_tracker 

        WHERE target_party LIKE '%Wendy Land%' 

        ORDER BY id DESC LIMIT 1

    """)

    tracker_row = cursor.fetchone()



    if not tracker_row or tracker_row[0] != "DISCARDED_AND_CONFIRMED":

        print(f"  [FAIL] Surrender tracker not updated for UCF (Found: {tracker_row[0] if tracker_row else 'None'}).")

        conn.close()

        sys.exit(1)

    print(f"  [PASS] Tracker confirmed for Wendy Land: Status='{tracker_row[0]}'")

    passed += 1



    # GATE 3: Verify Mandatory Severance Terms in Outbound Message

    print("\n[GATE 3] AUDITING OUTBOUND MESSAGE ARTIFACT & CLAUSES...")

    if not os.path.exists(MSG_FILE):

        print(f"  [FAIL] Outbound message file missing at: {MSG_FILE}")

        conn.close()

        sys.exit(1)



    with open(MSG_FILE, "r", encoding="utf-8") as f:

        text = f.read()



    mandatory_terms = [

        "severed its partnership with SignalLink Protocol LLC",

        "could not in good conscience rush an accelerated submission",

        "result in the creation of something truly novel",

        "next available open solicitation window",

        "CAGE: 1AHA8",

        "UEI: S1M4ENLHTDH5"

    ]

    for term in mandatory_terms:

        if term not in text:

            print(f"  [FAIL] Missing mandatory term in outbound message: '{term}'")

            conn.close()

            sys.exit(1)

        print(f"  [PASS] Verified message statement: '{term}'")

    passed += 1



    # GATE 4: Verify Outbound Severance Disclosure Record in Vault

    print("\n[GATE 4] AUDITING OUTBOUND SEVERANCE DISCLOSURE RECORD...")

    cursor.execute("""

        SELECT id, status FROM corporate_governance_log 

        WHERE action = 'UCF_REPLY_SEVERANCE_DISCLOSED' 

        ORDER BY id DESC LIMIT 1

    """)

    reply_row = cursor.fetchone()

    conn.close()



    if not reply_row or reply_row[1] != "OUTBOUND_REPLY_LOGGED_AND_PIPED":

        print(f"  [FAIL] Outbound reply action missing from vault.")

        sys.exit(1)

    print(f"  [PASS] Outbound severance disclosure verified: Record #{reply_row[0]}")

    passed += 1



    print("\n" + "=" * 80)

    if passed == 4:

        print("[AUDIT PASSED] 100% System Coverage: All 4 Test Gates Verified (UCF Decoupling Certified).")

    else:

        print(f"[AUDIT FAILED] Only {passed}/4 gates verified.")

        sys.exit(1)

    print("=" * 80)




if __name__ == "__main__":
    render()
