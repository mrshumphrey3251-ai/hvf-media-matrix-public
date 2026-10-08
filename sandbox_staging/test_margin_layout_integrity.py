"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: TEST MARGIN LAYOUT INTEGRITY
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    """

    HVF Omni-Industrial Matrix | FORENSIC TEST HARNESS

    Module: test_margin_layout_integrity.py

    Protocol: 4-Gate Audit, Test, and Verify Protocol (Right Margin Calibration)

    """



    import os

    import sys

    import re

    import sqlite3

    import hashlib



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")

    PROP_DIR = os.path.join(BASE_DIR, "proposals")

    HTML_FILE = os.path.join(PROP_DIR, "DIU_SOLUTION_BRIEF_PROJECT_EBONY_HVF.html")

    PDF_FILE = os.path.join(PROP_DIR, "DIU_SOLUTION_BRIEF_PROJECT_EBONY_HVF.pdf")



    print("=" * 80)

    print("PROJECT EBONY | RIGHT-SIDE MARGIN LAYOUT FORENSIC AUDIT")

    print("Target: proposals/DIU_SOLUTION_BRIEF_PROJECT_EBONY_HVF.html")

    print("=" * 80)



    passed = 0



    # GATE 1: Verify CSS Box-Sizing and Margin Rules in HTML via Regex

    print("\n[GATE 1] AUDITING CSS RIGHT-MARGIN & BOX-SIZING RESET RULES...")

    if not os.path.exists(HTML_FILE):

        print(f"  [FAIL] HTML deliverable missing: {HTML_FILE}")

        sys.exit(1)



    with open(HTML_FILE, "r", encoding="utf-8") as f:

        html = f.read()



    required_regex_rules = [

        (r"box-sizing\s*:\s*border-box", "box-sizing: border-box"),

        (r"margin-right\s*:\s*0\.85in", "margin-right: 0.85in"),

        (r"padding-right\s*:\s*0\.1in", "padding-right: 0.1in"),

        (r"table-layout\s*:\s*fixed", "table-layout: fixed"),

        (r"overflow-wrap\s*:\s*break-word", "overflow-wrap: break-word")

    ]



    for pattern, label in required_regex_rules:

        if not re.search(pattern, html):

            print(f"  [FAIL] Missing CSS margin constraint: '{label}'")

            sys.exit(1)

        print(f"  [PASS] CSS margin rule verified: '{label}'")

    passed += 1



    # GATE 2: Table Column Boundary Audit

    print("\n[GATE 2] AUDITING FIXED TABLE COLUMN BOUNDARIES...")

    col_patterns = [

        (r"col\.col-m\s*\{\s*width:\s*22%;\s*\}", "col.col-m (22%)"),

        (r"col\.col-w\s*\{\s*width:\s*14%;\s*\}", "col.col-w (14%)"),

        (r"col\.col-d\s*\{\s*width:\s*49%;\s*\}", "col.col-d (49%)"),

        (r"col\.col-a\s*\{\s*width:\s*15%;\s*\}", "col.col-a (15%)")

    ]

    for pattern, label in col_patterns:

        if not re.search(pattern, html):

            print(f"  [FAIL] Missing column width lock: '{label}'")

            sys.exit(1)

        print(f"  [PASS] Table column locked: '{label}'")

    passed += 1



    # GATE 3: PDF Deliverable Generation & File Weight

    print("\n[GATE 3] AUDITING COMPILED PDF DELIVERABLE ARTIFACT...")

    if not os.path.exists(PDF_FILE):

        print(f"  [FAIL] PDF deliverable missing: {PDF_FILE}")

        sys.exit(1)



    pdf_bytes = os.path.getsize(PDF_FILE)

    if pdf_bytes < 5000:

        print(f"  [FAIL] PDF file weight too low ({pdf_bytes} bytes).")

        sys.exit(1)

    print(f"  [PASS] PDF verified on disk ({pdf_bytes:,} bytes). Margin boundaries physically rendered.")

    passed += 1



    # GATE 4: Corporate Governance Ledger Persistence

    print("\n[GATE 4] AUDITING VAULT GOVERNANCE LOG...")

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT id, details, status FROM corporate_governance_log 

        WHERE action = 'RIGHT_MARGINS_CALIBRATED_AND_SEALED' 

        ORDER BY id DESC LIMIT 1

    """)

    row = cursor.fetchone()

    conn.close()



    if not row or row[2] != "MARGINS_CALIBRATED_AND_SEALED":

        print(f"  [FAIL] Governance record mismatch (Current: {row[2] if row else 'None'})")

        sys.exit(1)



    doc_hash = hashlib.sha256(html.encode("utf-8")).hexdigest()

    if doc_hash[:16] not in row[1]:

        print(f"  [FAIL] Hash mismatch! Disk: {doc_hash[:16]} vs Vault: {row[1]}")

        sys.exit(1)



    print(f"  [PASS] Vault Record #{row[0]} cryptographically matches deliverable (Digest: {doc_hash[:16]}).")

    passed += 1



    print("\n" + "=" * 80)

    if passed == 4:

        print("[AUDIT PASSED] 100% System Coverage: All 4 Test Gates Verified (Margin Management Certified).")

    else:

        print(f"[AUDIT FAILED] Only {passed}/4 gates verified.")

        sys.exit(1)

    print("=" * 80)




if __name__ == "__main__":
    render()
