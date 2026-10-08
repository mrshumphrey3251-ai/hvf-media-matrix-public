"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: TEST ARTICLE 05 STAGING
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    """

    HVF Omni-Industrial Matrix | FORENSIC TEST HARNESS

    Module: test_article_05_staging.py

    Protocol: 4-Gate Audit, Test, and Verify Protocol (Article 05 Capstone Certification)

    """



    import os

    import sys

    import re

    import sqlite3

    import hashlib



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")

    COMMS_DIR = os.path.join(BASE_DIR, "strategic_comms")

    ART5_FILE = os.path.join(COMMS_DIR, "ARTICLE_05_SOVEREIGN_PRIME_DOCTRINE.md")



    print("=" * 80)

    print("PROJECT EBONY | ARTICLE 05 CAPSTONE FORENSIC AUDIT")

    print("Target: strategic_comms/ARTICLE_05_SOVEREIGN_PRIME_DOCTRINE.md")

    print("=" * 80)



    passed = 0



    # GATE 1: Verify Article 05 Deliverable on Disk and Word Density

    print("\n[GATE 1] AUDITING ARTICLE 05 DELIVERABLE ON DISK...")

    if not os.path.exists(ART5_FILE):

        print(f"  [FAIL] Article 05 missing at: {ART5_FILE}")

        sys.exit(1)



    with open(ART5_FILE, "r", encoding="utf-8") as f:

        text = f.read()



    words = len(text.split())

    if words < 600:

        print(f"  [FAIL] Article 05 under-dense ({words} words). Minimum standard is 600 words.")

        sys.exit(1)

    print(f"  [PASS] Article 05 verified on disk ({words:,} words of high-density executive doctrine).")

    passed += 1



    # GATE 2: Audit Acquisition Authority & Architectural Moats

    print("\n[GATE 2] AUDITING STATUTORY ACQUISITION BENCHMARKS...")

    mandatory_patterns = [

        (r"Sovereign Prime Doctrine", "The Sovereign Prime Doctrine"),

        (r"10 U\.S\.C\. § 4022", "10 U.S.C. § 4022"),

        (r"Nontraditional Defense Contractor", "Nontraditional Defense Contractor"),

        (r"Three-Brain Architecture", "Three-Brain Architecture"),

        (r"Kinetic Guillotine", "Kinetic Guillotine"),

        (r"<1\.0 microsecond", "<1.0 microsecond analog cutoff"),

        (r"NIST SP 800-230", "NIST SP 800-230"),

        (r"DFARS 252\.227-7018", "DFARS 252.227-7018 Background IP rights")

    ]



    for pattern, label in mandatory_patterns:

        if not re.search(pattern, text, re.IGNORECASE):

            print(f"  [FAIL] Missing required technical/statutory concept: '{label}'")

            sys.exit(1)

        print(f"  [PASS] Verified concept: '{label}'")

    passed += 1



    # GATE 3: Audit Sovereign Entity Identifiers

    print("\n[GATE 3] AUDITING SOVEREIGN ENTITY IDENTIFIERS...")

    statutory_patterns = [

        (r"HVF Omni-Industrial Matrix", "HVF Omni-Industrial Matrix"),

        (r"1AHA8", "CAGE Code: 1AHA8"),

        (r"S1M4ENLHTDH5", "UEI: S1M4ENLHTDH5")

    ]



    for pattern, label in statutory_patterns:

        if not re.search(pattern, text, re.IGNORECASE):

            print(f"  [FAIL] Missing entity identifier: '{label}'")

            sys.exit(1)

        print(f"  [PASS] Verified identifier: '{label}'")

    passed += 1



    # GATE 4: Cryptographic Hash Reconciliation & Complete 5-Article Series Audit

    print("\n[GATE 4] RECONCILING ARTICLE 05 HASH & ENTIRE 5-PART SERIES IN VAULT...")

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()



    # Verify Article 05 Hash

    cursor.execute("SELECT sha256_hash, status FROM linkedin_editorial_tracker WHERE article_number = 5")

    tracker_row = cursor.fetchone()



    if not tracker_row:

        print("  [FAIL] Article 05 record missing from tracker.")

        conn.close()

        sys.exit(1)



    doc_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

    if doc_hash != tracker_row[0]:

        print(f"  [FAIL] Hash mismatch! Disk: {doc_hash[:16]} vs Tracker: {tracker_row[0][:16]}")

        conn.close()

        sys.exit(1)



    # Verify all 5 articles are registered

    cursor.execute("SELECT count(*) FROM linkedin_editorial_tracker WHERE status = 'STAGED_READY_FOR_DEPLOYMENT'")

    staged_count = cursor.fetchone()[0]

    conn.close()



    if staged_count < 5:

        print(f"  [FAIL] Expected 5 staged articles, found {staged_count}.")

        sys.exit(1)



    print(f"  [PASS] Cryptographic seal verified: {doc_hash[:16]} (Status: {tracker_row[1]}).")

    print(f"  [PASS] Complete Editorial Suite verified: All 5 articles registered and staged in memory vault.")

    passed += 1



    print("\n" + "=" * 80)

    if passed == 4:

        print("[AUDIT PASSED] 100% System Coverage: All 4 Test Gates Verified (Article 05 Certified).")

    else:

        print(f"[AUDIT FAILED] Only {passed}/4 gates verified.")

        sys.exit(1)

    print("=" * 80)




if __name__ == "__main__":
    render()
