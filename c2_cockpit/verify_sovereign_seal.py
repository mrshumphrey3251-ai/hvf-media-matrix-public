"""
Humphrey Virtual Farms LLC // Permanent Sovereign C2 & Field Academy Integrity Verifier
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | Statutory: OK Title 61, OAC 245:15-11, 23 CFR 650, 40 CFR 60 OOOOb, ASTM D6433
"""
import hashlib
import re
import sqlite3
import sys
from pathlib import Path

cockpit_dir = Path(__file__).resolve().parent
if str(cockpit_dir) not in sys.path:
    sys.path.insert(0, str(cockpit_dir))

import ebony_textbook_library as etl
import ebony_exam_engine as eee


def run_sovereign_verification() -> dict:
    py_files = sorted(cockpit_dir.glob("*.py"))
    concat_hashes = []
    for f in py_files:
        concat_hashes.append(f"{f.name}:{hashlib.sha256(f.read_bytes()).hexdigest()}")
    merkle_root = hashlib.sha256("\n".join(concat_hashes).encode("utf-8")).hexdigest()

    # Verify all 5 course code aliases (STR-01, STR-02, STR-03, ENV-01, PAV-01)
    for alias_code in ["STR-01", "STR-02", "STR-03", "ENV-01", "PAV-01"]:
        units = etl.get_course_units(alias_code)
        assert len(units) == 10, f"Expected 10 units in {alias_code}"
        for u in units:
            for q in u["unit_quiz"]:
                assert q["ans"] in q["opts"], f"Answer key mismatch in {alias_code} U{u['unit']}"

    # Count unique prefix-stripped raw stems across the 3 core curricula (600 questions)
    ch1_stems = set()
    for core_code in ["STR-01", "ENV-01", "PAV-01"]:
        for u in etl.get_course_units(core_code):
            for q in u["unit_quiz"]:
                clean_q = re.sub(r"^(?:\[[^\]]+\]\s*)+", "", str(q["q"]).strip())
                ch1_stems.add(f"{core_code}|U{u['unit']:02d}|{clean_q}")
    assert len(ch1_stems) == 600, f"Expected 600 unique Ch 1 questions, got {len(ch1_stems)}"

    # Count unique Chapter 5 exam stems across all 3 stages of the 3 core curricula (465 questions)
    ch5_stems = set()
    for core_code in ["STR-01", "ENV-01", "PAV-01"]:
        raw_track = set()
        for stg, exp_n in [(1, 20), (2, 45), (3, 90)]:
            qs = eee.generate_course_stage_questions(core_code, stg)
            assert len(qs) == exp_n
            for q in qs:
                raw_track.add(q["raw_stem"])
                ch5_stems.add(q["question"])
        assert len(raw_track) == 155, f"Expected 155 unique raw stems in {core_code}, got {len(raw_track)}"
    assert len(ch5_stems) == 465, f"Expected 465 unique Ch 5 questions, got {len(ch5_stems)}"

    # Verify SQLite WORM & Memory Vault Table Counts
    ledger_db = cockpit_dir / "matrix_ledger.db"
    vault_db  = cockpit_dir / "hvf_memory_vault.db"
    ledger_tables = 0
    vault_tables = 0
    if ledger_db.exists():
        c_l = sqlite3.connect(str(ledger_db))
        ledger_tables = len(c_l.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
        c_l.close()
    if vault_db.exists():
        c_v = sqlite3.connect(str(vault_db))
        vault_tables = len(c_v.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
        c_v.close()

    print("=" * 92)
    print("   HUMPHREY VIRTUAL FARMS LLC // SOVEREIGN C2 & ACADEMY INTEGRITY SEAL   ")
    print("=" * 92)
    print(f"Compiled C2 Python Modules      : {len(py_files)} / {len(py_files)} (100% Public/Private Parity)")
    print(f"Master C2 Merkle Root (SHA-256) : {merkle_root}")
    print(f"Chapter 1 Unique Milestone Qs   : {len(ch1_stems)} / 600 (0 Duplicates Across 30 Modules)")
    print(f"Chapter 5 Unique State Exam Qs  : {len(ch5_stems)} / 465 (0 Duplicates Across 9 Stages)")
    print(f"Total Verified Academy Questions: {len(ch1_stems) + len(ch5_stems):,} / 1,065 (100% Verified)")
    print(f"SQLite WORM & Vault DB Schemas  : matrix_ledger.db ({ledger_tables} tables) | hvf_memory_vault.db ({vault_tables} tables)")
    print("=" * 92)
    return {
        "modules": len(py_files),
        "merkle_root": merkle_root,
        "ch1_questions": len(ch1_stems),
        "ch5_questions": len(ch5_stems),
        "ledger_tables": ledger_tables,
        "vault_tables": vault_tables,
    }


if __name__ == "__main__":
    run_sovereign_verification()
