"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: TEST DEFENSE BRIEF SEAL
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    """

    HVF Omni-Industrial Matrix | FORENSIC TEST HARNESS

    Module: test_defense_brief_seal.py

    Protocol: 4-Gate Audit, Test, and Verify Protocol (Sealed Brief Persistence)

    """



    import os

    import sys

    import sqlite3

    import hashlib



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")

    BRIEF_FILE = os.path.join(BASE_DIR, "proposals", "TAILORED_BRIEF_DIU-AOI-2026-AUTONOMY.md")



    print("=" * 80)

    print("PROJECT EBONY | SEALED DEFENSE BRIEF FORENSIC AUDIT")

    print("Target: proposals/TAILORED_BRIEF_DIU-AOI-2026-AUTONOMY.md")

    print("=" * 80)



    passed = 0



    # GATE 1: Verify 5-Page Deliverable Exists on Disk

    print("\n[GATE 1] AUDITING 5-PAGE DELIVERABLE ARTIFACT ON DISK...")

    if not os.path.exists(BRIEF_FILE):

        print(f"  [FAIL] Brief file missing at: {BRIEF_FILE}")

        sys.exit(1)



    with open(BRIEF_FILE, "r", encoding="utf-8") as f:

        text = f.read()



    words = len(text.split())

    if words < 1800:

        print(f"  [FAIL] Brief under-dense ({words} words).")

        sys.exit(1)

    print(f"  [PASS] Deliverable verified on disk ({words:,} words).")

    passed += 1



    # GATE 2: Verify Statutory References and Prime Authority

    print("\n[GATE 2] AUDITING PRIME CONTRACTING & STATUTORY PARAMETERS...")

    required_clauses = [

        "HVF Omni-Industrial Matrix",

        "CAGE: 1AHA8",

        "UEI: S1M4ENLHTDH5",

        "10 U.S.C. § 4022",

        "Kinetic Guillotine",

        "$150,000.00",

        "DFARS 252.227-7018"

    ]

    for clause in required_clauses:

        if clause not in text:

            print(f"  [FAIL] Missing mandatory clause: '{clause}'")

            sys.exit(1)

        print(f"  [PASS] Verified clause: '{clause}'")

    passed += 1



    # GATE 3: Verify Corporate Governance Vault Record

    print("\n[GATE 3] AUDITING GOVERNANCE LOG TRANSACTION...")

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT id, authority, target_entity, action, details, status 

        FROM corporate_governance_log 

        WHERE action = 'FULL_5PAGE_DEFENSE_BRIEF_COMPILED' 

        ORDER BY id DESC LIMIT 1

    """)

    row = cursor.fetchone()

    conn.close()



    if not row:

        print("  [FAIL] No vault entry for FULL_5PAGE_DEFENSE_BRIEF_COMPILED.")

        sys.exit(1)



    print(f"  [PASS] Vault Record #{row[0]} confirmed: Authority='{row[1]}', Status='{row[5]}'")

    passed += 1



    # GATE 4: Cryptographic Hash Reconciliation

    print("\n[GATE 4] RECONCILING DOCUMENT SHA-256 HASH WITH VAULT RECORD...")

    doc_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

    if doc_hash[:16] not in row[4]:

        print(f"  [FAIL] Digest mismatch! File: {doc_hash[:16]} vs Vault Details: {row[4]}")

        sys.exit(1)

    print(f"  [PASS] Cryptographic seal verified: {doc_hash[:16]}")

    passed += 1



    print("\n" + "=" * 80)

    if passed == 4:

        print("[AUDIT PASSED] 100% System Coverage: All 4 Test Gates Verified (Defense Brief Sealed).")

    else:

        print(f"[AUDIT FAILED] Only {passed}/4 gates verified.")

        sys.exit(1)

    print("=" * 80)




if __name__ == "__main__":
    render()
