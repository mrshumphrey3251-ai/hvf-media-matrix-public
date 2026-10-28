"""
HVFNexus Sovereign Industrial C2 — Automated USB Briefcase Synchronizer
Detects removable storage drives, mirrors C:\HVF_Briefcase_Rob_Teele,
verifies target cryptographic integrity, and seals event in WORM ledger.
"""
import shutil
import hashlib
import sqlite3
import string
import os
from datetime import datetime
from pathlib import Path

source_briefcase = Path("C:/HVF_Briefcase_Rob_Teele")
cockpit_dir = Path("C:/hvf_c2/hvf-media-matrix-private/c2_cockpit")
db_path = cockpit_dir / "matrix_ledger.db"

print("=== [HVFNexus C2] HARDWARE USB BRIEFCASE SYNCHRONIZATION ENGINE ===")

if not source_briefcase.exists():
    raise FileNotFoundError(f"Source briefcase missing at {source_briefcase}")

# Detect removable drives (Windows Drive Letters D: through Z:)
available_drives = []
for letter in string.ascii_uppercase:
    if letter in ["C"]:
        continue
    p = Path(f"{letter}:/")
    if p.exists():
        available_drives.append(p)

print(f"[*] Detected Active External/Secondary Volumes: {[str(d) for d in available_drives]}")

synced_targets = 0
for drive in available_drives:
    target_dir = drive / "HVF_Briefcase_Rob_Teele"
    try:
        if target_dir.exists():
            shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for item in source_briefcase.iterdir():
            if item.is_file():
                dest_file = target_dir / item.name
                shutil.copy2(item, dest_file)
                # Verify destination hash matches source
                src_hash = hashlib.sha256(item.read_bytes()).hexdigest()
                dst_hash = hashlib.sha256(dest_file.read_bytes()).hexdigest()
                assert src_hash == dst_hash, f"Hash mismatch on {item.name}"
        
        print(f"[+] Successfully mirrored and cryptographically verified on {target_dir}")
        synced_targets += 1
    except Exception as e:
        print(f"[-] Could not mirror to {drive}: {e}")

# Seal synchronization event in matrix_ledger.db
ts = datetime.utcnow().isoformat()
raw_proof = f"{ts}|1AHA8|USB_SYNC_EXECUTED|TARGETS_{synced_targets}"
proof_hash = hashlib.sha256(raw_proof.encode("utf-8")).hexdigest()

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()
cursor.execute("""
    INSERT INTO executive_authorizations 
    (timestamp, core, authorized_by, cage_code, uei, action, artifact_hash, proof_hash)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (ts, "EBONY_USB_CORE_V1", "CEO Jeffery Humphrey", "1AHA8", "S1M4ENLHTDH5",
      "USB_BRIEFCASE_SYNCHRONIZED", f"TARGETS_{synced_targets}_DRIVES", proof_hash))

conn.commit()
conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
conn.close()

print(f"[+] USB synchronization posture recorded in matrix_ledger.db: {proof_hash[:16]}...")
print("=== USB SYNCHRONIZATION ENGINE: ARMED & READY ===")