"""
HVF Omni-Industrial Matrix | FORENSIC TEST HARNESS
Module: test_pipeline_pivot.py
Protocol: 4-Gate Audit, Test, and Verify Protocol (Defense Pipeline Elevation)
"""

import os
import sys
import sqlite3

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
BRIEF_FILE = os.path.join(BASE_DIR, "proposals", "TAILORED_BRIEF_DIU-AOI-2026-AUTONOMY.md")

print("=" * 80)
print("PROJECT EBONY | PIPELINE PIVOT FORENSIC AUDIT")
print("Target: DIU-AOI-2026-AUTONOMY ($1.65M Defense Prototype OT)")
print("=" * 80)

passed = 0

# GATE 1: Database Status Audit for NSF and DIU
print("\n[GATE 1] AUDITING SOLICITATION STATUS TRANSITIONS IN VAULT...")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT status FROM active_solicitation_intake WHERE solicitation_id = 'NSF-SBIR-2026-P1'")
nsf_status = cursor.fetchone()[0]
if nsf_status != "LOCKED_UNTIL_2026-11-04":
    print(f"  [FAIL] NSF status not properly updated (Current: {nsf_status})")
    conn.close()
    sys.exit(1)
print(f"  [PASS] NSF status correctly sealed: {nsf_status}")

cursor.execute("SELECT status, max_award_usd, mobilization_eligible FROM active_solicitation_intake WHERE solicitation_id = 'DIU-AOI-2026-AUTONOMY'")
diu_row = cursor.fetchone()
if not diu_row or diu_row[0] != "PRIMARY_ACTIVE_TARGET":
    print(f"  [FAIL] DIU status not PRIMARY_ACTIVE_TARGET (Current: {diu_row[0] if diu_row else 'None'})")
    conn.close()
    sys.exit(1)
print(f"  [PASS] DIU status verified as PRIMARY_ACTIVE_TARGET ($1,650,000.00 USD).")
passed += 1

# GATE 2: Mobilization Tranche Arithmetic Verification
print("\n[GATE 2] AUDITING DIU MOBILIZATION TRANCHE ARITHMETIC ($150,000)...")
if diu_row[2] != 1:
    print("  [FAIL] DIU solicitation not marked mobilization eligible.")
    conn.close()
    sys.exit(1)
mob_amount = 150000.0
total_award = diu_row[1]
post_mob = total_award - mob_amount
if post_mob != 1500000.0:
    print(f"  [FAIL] Arithmetic error in post-mobilization balance: {post_mob}")
    conn.close()
    sys.exit(1)
print(f"  [PASS] Financial schedule verified: Total: ${total_award:,.2f} | M1A Kickoff: ${mob_amount:,.2f} | Execution: ${post_mob:,.2f}")
passed += 1

# GATE 3: Verify Staged DIU 5-Page Brief Artifact on Disk
print("\n[GATE 3] AUDITING DIU 5-PAGE SOLUTION BRIEF ARTIFACT...")
if not os.path.exists(BRIEF_FILE):
    print(f"  [FAIL] Tailored brief missing at: {BRIEF_FILE}")
    conn.close()
    sys.exit(1)

with open(BRIEF_FILE, "r", encoding="utf-8") as f:
    text = f.read()

required_clauses = [
    "DIU-AOI-2026-AUTONOMY",
    "HVF Omni-Industrial Matrix",
    "CAGE: 1AHA8",
    "UEI: S1M4ENLHTDH5",
    "Nontraditional Defense Contractor",
    "Kinetic Guillotine",
    "M1A: Kickoff & Mobilization",
    "$150,000",
    "DFARS 252.227-7018"
]
for clause in required_clauses:
    if clause not in text:
        print(f"  [FAIL] Missing required clause in DIU brief: '{clause}'")
        conn.close()
        sys.exit(1)
    print(f"  [PASS] Clause verified: '{clause}'")
passed += 1

# GATE 4: Corporate Memory Vault Logging Audit
print("\n[GATE 4] AUDITING GOVERNANCE LOGGING RECORD...")
cursor.execute("""
    SELECT id, details FROM corporate_governance_log 
    WHERE action = 'PIPELINE_PIVOT_DIU_DEFENSE_ELEVATED' 
    ORDER BY id DESC LIMIT 1
""")
log_entry = cursor.fetchone()
conn.close()

if not log_entry:
    print("  [FAIL] Missing PIPELINE_PIVOT_DIU_DEFENSE_ELEVATED record in governance log.")
    sys.exit(1)
print(f"  [PASS] Governance Log Record #{log_entry[0]} confirmed: {log_entry[1][:75]}...")
passed += 1

print("\n" + "=" * 80)
if passed == 4:
    print("[AUDIT PASSED] 100% System Coverage: All 4 Test Gates Verified (DIU Target Elevated).")
else:
    print(f"[AUDIT FAILED] Only {passed}/4 gates verified.")
    sys.exit(1)
print("=" * 80)

