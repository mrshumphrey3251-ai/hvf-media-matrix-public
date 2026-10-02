"""
HVF Omni-Industrial Matrix | FORENSIC TEST HARNESS
Module: test_article_staging.py
Protocol: 4-Gate Audit, Test, and Verify Protocol (LinkedIn Technical Editorial Certification)
"""

import os
import sys
import sqlite3
import hashlib

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
ARTICLE_FILE = os.path.join(BASE_DIR, "strategic_comms", "ARTICLE_01_MULTI_BRAIN_VS_LEGACY_TMR.md")

print("=" * 80)
print("PROJECT EBONY | LINKEDIN ARTICLE 01 FORENSIC AUDIT")
print("Target: strategic_comms/ARTICLE_01_MULTI_BRAIN_VS_LEGACY_TMR.md")
print("=" * 80)

passed = 0

# GATE 1: Verify Article File Presence and Density
print("\n[GATE 1] AUDITING EDITORIAL DELIVERABLE ON DISK...")
if not os.path.exists(ARTICLE_FILE):
    print(f"  [FAIL] Article file missing at: {ARTICLE_FILE}")
    sys.exit(1)

with open(ARTICLE_FILE, "r", encoding="utf-8") as f:
    text = f.read()

words = len(text.split())
if words < 600:
    print(f"  [FAIL] Article under-dense ({words} words). Minimum standard is 600 words.")
    sys.exit(1)
print(f"  [PASS] Deliverable verified on disk ({words:,} words of high-density technical analysis).")
passed += 1

# GATE 2: Audit Technical Depth and Comparative Clauses
print("\n[GATE 2] AUDITING TECHNICAL & ARCHITECTURAL BENCHMARKS...")
mandatory_concepts = [
    "Triple Modular Redundancy (TMR)",
    "Common-Mode Firmware Vulnerability",
    "ASIL-D",
    "Three-Brain Architecture",
    "Brain One: The Deterministic Controller",
    "Kinetic Guillotine",
    "<1.0 microsecond",
    "Brain Two: The Offline Cognitive Analyst",
    "Brain Three: The Local Cryptographic Arbiter",
    "Merkle Directed Acyclic Graph (DAG)",
    "NIST SP 800-230"
]

for concept in mandatory_concepts:
    if concept not in text:
        print(f"  [FAIL] Missing mandatory technical concept: '{concept}'")
        sys.exit(1)
    print(f"  [PASS] Verified architectural concept: '{concept}'")
passed += 1

# GATE 3: Audit Prime Contractor Identifiers and IP Rights
print("\n[GATE 3] AUDITING STATUTORY PRIME CONTRACTOR PROTECTIONS...")
statutory_clauses = [
    "HVF Omni-Industrial Matrix",
    "10 U.S.C. § 4022",
    "CAGE: 1AHA8",
    "UEI: S1M4ENLHTDH5",
    "DFARS 252.227-7018"
]

for clause in statutory_clauses:
    if clause not in text:
        print(f"  [FAIL] Missing statutory protection clause: '{clause}'")
        sys.exit(1)
    print(f"  [PASS] Verified statutory clause: '{clause}'")
passed += 1

# GATE 4: Corporate Governance Vault Record Audit
print("\n[GATE 4] AUDITING VAULT GOVERNANCE LOGGING...")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
    SELECT id, details, status FROM corporate_governance_log 
    WHERE action = 'LINKEDIN_ARTICLE_01_STAGED' 
    ORDER BY id DESC LIMIT 1
""")
row = cursor.fetchone()
conn.close()

if not row or row[2] != "ARTICLE_SEALED_AND_COPIED":
    print(f"  [FAIL] Governance record not found or status mismatch.")
    sys.exit(1)

doc_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
if doc_hash[:16] not in row[1]:
    print(f"  [FAIL] Hash mismatch! Disk: {doc_hash[:16]} vs Vault Details: {row[1]}")
    sys.exit(1)

print(f"  [PASS] Vault Record #{row[0]} cryptographically matched (Hash: {doc_hash[:16]}).")
passed += 1

print("\n" + "=" * 80)
if passed == 4:
    print("[AUDIT PASSED] 100% System Coverage: All 4 Test Gates Verified (LinkedIn Article 01 Certified).")
else:
    print(f"[AUDIT FAILED] Only {passed}/4 gates verified.")
    sys.exit(1)
print("=" * 80)

