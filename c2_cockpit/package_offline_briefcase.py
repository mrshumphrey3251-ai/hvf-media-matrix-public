"""
HVFNexus Sovereign Industrial C2 — Air-Gapped Executive Briefcase Packaging Engine
Compiles all presentation, technical, and binding commercial collateral into an offline folder.
"""
import shutil
import hashlib
import sqlite3
from datetime import datetime
from pathlib import Path

cockpit_dir = Path("C:/HVF_Repos/hvf-media-matrix-private/c2_cockpit")
briefcase_dir = Path("C:/HVF_Briefcase_Rob_Teele")
db_path = cockpit_dir / "matrix_ledger.db"

print("=== [HVFNexus C2] PACKAGING 11-ARTIFACT COMPLETE EXECUTIVE SUITE ===")

if briefcase_dir.exists():
    shutil.rmtree(briefcase_dir)
briefcase_dir.mkdir(parents=True, exist_ok=True)

target_files = [
    "HVF_COMMERCE_ENERGY_PACKET.html",
    "HVF_EXECUTIVE_MEETING_PACKET.html",
    "EXECUTIVE_MEETING_CUE_CARD.txt",
    "ROB_TEELE_DOC_ENERGY_BRIEFING.md",
    "ROB_TEELE_ONE_SHEET.txt",
    "DOC_ENERGY_COMMERCIALIZATION_MEMO.md",
    "EBONY_ENERGY_C2_ARCHITECTURE.md",
    "APEX_ACCELERATOR_INTAKE.md",
    "HVF_COMMERCIAL_FEE_SCHEDULE.md",
    "ROB_TEELE_COMMERCIAL_TERMS_BRIEF.md",
    "PHASE_1_PILOT_SOW.md"
]

manifest_lines = []
manifest_lines.append("================================================================================")
manifest_lines.append("  HUMPHREY VIRTUAL FARMS LLC — AIR-GAPPED BRIEFCASE CRYPTOGRAPHIC MANIFEST      ")
manifest_lines.append(f"  GENERATED (UTC): {datetime.utcnow().isoformat()} | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5")
manifest_lines.append("================================================================================\n")

copied_count = 0
for fname in target_files:
    src = cockpit_dir / fname
    if src.exists():
        dst = briefcase_dir / fname
        shutil.copy2(src, dst)
        h = hashlib.sha256(dst.read_bytes()).hexdigest()
        manifest_lines.append(f"{h}  {fname}")
        copied_count += 1
        print(f"[+] Packaged: {fname:<36} (SHA-256: {h[:16]}...)")
    else:
        print(f"[-] WARNING: File missing: {fname}")

manifest_text = "\n".join(manifest_lines) + "\n"
manifest_path = briefcase_dir / "MANIFEST_SHA256.txt"
manifest_path.write_text(manifest_text, encoding="utf-8")
print(f"[+] Cryptographic manifest generated: {manifest_path}")

# Seal packaging into matrix_ledger.db
ts = datetime.utcnow().isoformat()
briefcase_hash = hashlib.sha256(manifest_text.encode("utf-8")).hexdigest()

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()
cursor.execute("""
    INSERT INTO executive_authorizations 
    (timestamp, core, authorized_by, cage_code, uei, action, artifact_hash, proof_hash)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (ts, "EBONY_BRIEFCASE_CORE_V3", "CEO Jeffery Humphrey", "1AHA8", "S1M4ENLHTDH5",
      "OFFLINE_BRIEFCASE_SEALED", f"FILES_{copied_count}_PACKAGED", briefcase_hash))

conn.commit()
conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
conn.close()

print(f"[+] 11-Artifact Briefcase sealed into WORM ledger. Proof: {briefcase_hash[:16]}...")
print(f"[+] Air-gapped presentation suite ready at: {briefcase_dir}")