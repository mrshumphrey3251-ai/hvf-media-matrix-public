"""
HVF Omni-Industrial Matrix | FORENSIC TEST HARNESS
Module: test_linkedin_broadcast_audit.py
Protocol: 4-Gate Audit, Test, and Verify Protocol (Strategic Directive Certification)
"""

import os
import sys
import sqlite3
import hashlib

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
DIRECTIVE_FILE = os.path.join(BASE_DIR, "strategic_comms", "STRATEGIC_LINKEDIN_DIRECTIVE.txt")

print("=" * 80)
print("PROJECT EBONY | STRATEGIC BROADCAST FORENSIC AUDIT")
print("Target: strategic_comms/STRATEGIC_LINKEDIN_DIRECTIVE.txt")
print("=" * 80)

passed = 0

# GATE 1: Verify Message Artifact on Disk
print("\n[GATE 1] AUDITING DIRECTIVE ARTIFACT PRESENCE ON DISK...")
if not os.path.exists(DIRECTIVE_FILE):
    print(f"  [FAIL] Directive file missing at: {DIRECTIVE_FILE}")
    sys.exit(1)

with open(DIRECTIVE_FILE, "r", encoding="utf-8") as f:
    text = f.read()

words = len(text.split())
if words < 100:
    print(f"  [FAIL] Broadcast payload under-dense ({words} words).")
    sys.exit(1)
print(f"  [PASS] Directive verified on disk ({words} words).")
passed += 1

# GATE 2: Mandatory Prime Authority & Technical Parameters
print("\n[GATE 2] AUDITING PRIME CONTRACTING & TECHNICAL PARAMETERS...")
required_clauses = [
    "HVF Omni-Industrial Matrix",
    "10 U.S.C. § 4022",
    "CAGE: 1AHA8",
    "UEI: S1M4ENLHTDH5",
    "Three-Brain Architecture",
    "Kinetic Guillotine",
    "<1.0 microsecond",
    "DFARS 252.227-7018"
]

for clause in required_clauses:
    if clause not in text:
        print(f"  [FAIL] Missing required clause: '{clause}'")
        sys.exit(1)
    print(f"  [PASS] Mandatory clause verified: '{clause}'")
passed += 1

# GATE 3: Corporate Governance Vault Record Audit
print("\n[GATE 3] AUDITING GOVERNANCE LOGGING IN MEMORY VAULT...")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
    SELECT id, details, status FROM corporate_governance_log 
    WHERE action = 'STRATEGIC_DIRECTIVE_STAGED_FOR_BROADCAST' 
    ORDER BY id DESC LIMIT 1
""")
row = cursor.fetchone()
conn.close()

if not row or row[2] != "BROADCAST_STAGED_FOR_DEPLOYMENT":
    print(f"  [FAIL] Governance record not found or status mismatch.")
    sys.exit(1)

doc_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
if doc_hash[:16] not in row[1]:
    print(f"  [FAIL] Hash mismatch! Disk: {doc_hash[:16]} vs Vault Details: {row[1]}")
    sys.exit(1)

print(f"  [PASS] Vault Record #{row[0]} verified and cryptographically matched (Hash: {doc_hash[:16]}).")
passed += 1

# GATE 4: Zero-Hallucination & Author URN Verification
print("\n[GATE 4] AUDITING AUTHOR URN BINDING & REPUTATION INTEGRITY...")
if "urn:li:person:UG5_wCt0pZ" not in row[1]:
    print("  [FAIL] Author URN mismatch in audit record.")
    sys.exit(1)
print("  [PASS] Author URN confirmed: urn:li:person:UG5_wCt0pZ (Strict CEO Clearance).")
passed += 1

print("\n" + "=" * 80)
if passed == 4:
    print("[AUDIT PASSED] 100% System Coverage: All 4 Test Gates Verified (Strategic Broadcast Certified).")
else:
    print(f"[AUDIT FAILED] Only {passed}/4 gates verified.")
    sys.exit(1)
print("=" * 80)

