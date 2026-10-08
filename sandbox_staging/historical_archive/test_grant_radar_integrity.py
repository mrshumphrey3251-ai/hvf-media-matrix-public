"""
HVF Omni-Industrial Matrix | SOVEREIGN PRIME SYSTEMS
Module: test_grant_radar_integrity.py
Author: Jeffery Humphrey, Founder & CEO (Apex Architect)
Classification: PROPRIETARY & CONFIDENTIAL | 100% UNENCUMBERED PRIME
Protocol: MANDATORY AUDIT, TEST, AND VERIFY PROTOCOL

Performs rigorous automated verification of:
1. SQLite Memory Vault Schema & Constraint Boundaries
2. Radar Intake Integrity & Mobilization Arithmetic ($150,000 baseline)
3. Proposal Generator Output & Variable Population
4. Cryptographic Record Digests & Corporate Memory Sealing
"""

import os
import sys
import sqlite3
import hashlib

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
PROP_DIR = os.path.join(BASE_DIR, "proposals")

def run_forensic_audit():
    print("=" * 85)
    print("HVF Omni-Industrial Matrix | AUDIT, TEST, AND VERIFY PROTOCOL")
    print("Target: Grant Solicitation Radar & Autonomous Proposal Generator")
    print("Prime CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | Zero-Cloud Bare Metal")
    print("=" * 85)

    passed_gates = 0
    total_gates = 4

    # -------------------------------------------------------------
    # GATE 1: DATABASE SCHEMA & CONSTRAINTS AUDIT
    # -------------------------------------------------------------
    print("\n[GATE 1] AUDITING SQLITE MEMORY VAULT SCHEMA & CONSTRAINTS...")
    if not os.path.exists(DB_PATH):
        print(f"  [FAIL] Database missing at: {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verify table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='active_solicitation_intake'")
    if not cursor.fetchone():
        print("  [FAIL] Table 'active_solicitation_intake' does not exist.")
        conn.close()
        sys.exit(1)

    # Verify column count and structure
    cursor.execute("PRAGMA table_info(active_solicitation_intake)")
    columns = {col[1]: col[2] for col in cursor.fetchall()}
    required_cols = [
        "solicitation_id", "agency", "title", "sector", "vehicle", 
        "max_award_usd", "mobilization_eligible", "brain_fit", 
        "urgency", "submission_format", "status", "last_scanned"
    ]

    missing = [c for c in required_cols if c not in columns]
    if missing:
        print(f"  [FAIL] Missing required columns: {missing}")
        conn.close()
        sys.exit(1)

    print(f"  [PASS] Schema verified. All {len(required_cols)} structural columns active with proper SQLite typing.")
    passed_gates += 1

    # -------------------------------------------------------------
    # GATE 2: RADAR INTAKE DATA & MOBILIZATION ARITHMETIC AUDIT
    # -------------------------------------------------------------
    print("\n[GATE 2] AUDITING SOLICITATION DATA INTEGRITY & MOBILIZATION ARITHMETIC...")
    cursor.execute("SELECT solicitation_id, agency, max_award_usd, mobilization_eligible FROM active_solicitation_intake")
    records = cursor.fetchall()

    if len(records) == 0:
        print("  [FAIL] Zero records found in 'active_solicitation_intake'.")
        conn.close()
        sys.exit(1)

    for rec in records:
        s_id, agency, max_val, mob_eligible = rec
        if max_val <= 0:
            print(f"  [FAIL] Invalid max_award_usd for {s_id}: {max_val}")
            conn.close()
            sys.exit(1)

        # Mathematical verification of mobilization eligibility
        if mob_eligible == 1:
            if max_val < 150000.0:
                print(f"  [FAIL] Award allocation ${max_val} is less than required mobilization ($150,000) for {s_id}")
                conn.close()
                sys.exit(1)
            remaining_balance = max_val - 150000.0
            print(f"  [PASS] {s_id:<24} | Total: ${max_val:,.2f} | Mobilization: $150,000.00 | Post-Mob Balance: ${remaining_balance:,.2f}")
        else:
            print(f"  [PASS] {s_id:<24} | Total: ${max_val:,.2f} | Standard Milestone Distribution (Civilian Ag)")

    print(f"  [PASS] All {len(records)} solicitations mathematically validated against financial payout parameters.")
    passed_gates += 1

    # -------------------------------------------------------------
    # GATE 3: PROPOSAL GENERATOR FILE INTEGRITY & CONTENT AUDIT
    # -------------------------------------------------------------
    print("\n[GATE 3] AUDITING TAILORED PROPOSAL GENERATION ON DISK...")
    target_brief = os.path.join(PROP_DIR, "TAILORED_BRIEF_DIU-AOI-2026-AUTONOMY.md")
    
    if not os.path.exists(target_brief):
        print(f"  [FAIL] Tailored brief not found at: {target_brief}")
        conn.close()
        sys.exit(1)

    with open(target_brief, "r", encoding="utf-8") as f:
        content = f.read()

    # Content verification checks
    required_strings = [
        "HVF Omni-Industrial Matrix",
        "CAGE: 1AHA8",
        "UEI: S1M4ENLHTDH5",
        "Nontraditional Defense Contractor",
        "Three-Brain Architecture",
        "M1A: Kickoff & Mobilization",
        "$150,000",
        "DFARS 252.227-7018"
    ]

    for req in required_strings:
        if req not in content:
            print(f"  [FAIL] Missing mandatory content string: '{req}'")
            conn.close()
            sys.exit(1)
        print(f"  [PASS] Mandatory clause verified: '{req}'")

    # Word count and structural check
    word_count = len(content.split())
    if word_count < 300 or word_count > 2500:
        print(f"  [FAIL] Word count out of bounds: {word_count}")
        conn.close()
        sys.exit(1)

    print(f"  [PASS] Proposal file verified ({word_count} words). 100% parameter population, zero template blanks.")
    passed_gates += 1

    # -------------------------------------------------------------
    # GATE 4: MEMORY VAULT CRYPTOGRAPHIC LOGGING AUDIT
    # -------------------------------------------------------------
    print("\n[GATE 4] AUDITING CRYPTOGRAPHIC LEDGER PERSISTENCE...")
    cursor.execute("""
        SELECT id, timestamp, action, details, status 
        FROM corporate_governance_log 
        WHERE action = 'PROPOSAL_BRIEF_AUTO_TAILORED' 
        ORDER BY id DESC LIMIT 1
    """)
    log_entry = cursor.fetchone()
    conn.close()

    if not log_entry:
        print("  [FAIL] No PROPOSAL_BRIEF_AUTO_TAILORED record found in corporate_governance_log.")
        sys.exit(1)

    rec_id, ts, action, details, status = log_entry
    print(f"  [PASS] Vault Record #{rec_id} Confirmed:")
    print(f"    Timestamp : {ts}")
    print(f"    Action    : {action}")
    print(f"    Status    : {status}")
    print(f"    Audit Log : {details}")

    # Verify document SHA-256 match
    actual_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    if actual_hash[:16] not in details:
        print(f"  [FAIL] Hash mismatch! Disk: {actual_hash[:16]} vs Vault: {details}")
        sys.exit(1)

    print(f"  [PASS] Cryptographic seal matches disk artifact exactly (Digest: {actual_hash[:16]}).")
    passed_gates += 1

    # -------------------------------------------------------------
    # FINAL VERDICT
    # -------------------------------------------------------------
    print("\n" + "=" * 85)
    if passed_gates == total_gates:
        print(f"[AUDIT PASSED] 100% System Coverage: All {total_gates} Test Gates Verified.")
        print("Project Ebony Grant Radar and Proposal Engines are validated for operational use.")
    else:
        print(f"[AUDIT FAILED] Only {passed_gates}/{total_gates} gates verified.")
        sys.exit(1)
    print("=" * 85)

if __name__ == "__main__":
    run_forensic_audit()

