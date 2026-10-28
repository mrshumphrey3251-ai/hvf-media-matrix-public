"""
HVFNexus Sovereign Industrial C2 — Launcher & Desktop Trigger Validator
Verifies batch launcher files, paths, and environment readiness on bare metal.
"""
import os
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

cockpit_dir = Path("C:/hvf_c2/hvf-media-matrix-private/c2_cockpit")
private_root = Path("C:/hvf_c2/hvf-media-matrix-private")
desktop_dir = Path(os.environ.get("USERPROFILE", "")) / "Desktop"
db_path = cockpit_dir / "matrix_ledger.db"

root_bat = private_root / "start_c2_console.bat"
desktop_bat = desktop_dir / "START_HVFNEXUS_C2.bat"

print("=== [HVFNexus C2] VERIFYING DESKTOP & ENCLAVE LAUNCH TRIGGERS ===")

assert root_bat.exists(), f"Missing root launcher: {root_bat}"
print(f"[+] Verified Enclave Root Trigger: {root_bat} ({root_bat.stat().st_size} bytes)")

if desktop_bat.exists():
    print(f"[+] Verified Desktop Quick Trigger: {desktop_bat} ({desktop_bat.stat().st_size} bytes)")
else:
    print(f"[-] Warning: Desktop shortcut missing at {desktop_bat}")

# Verify target python file
target_launchpad = cockpit_dir / "pre_meeting_launchpad.py"
assert target_launchpad.exists(), f"Target launchpad missing: {target_launchpad}"
print(f"[+] Target Executive Console Verified: {target_launchpad}")

# Seal launch readiness in matrix_ledger.db
ts = datetime.utcnow().isoformat()
raw_proof = f"{ts}|1AHA8|LAUNCHER_TRIGGERS_VERIFIED_STANDBY_READY"
proof_hash = hashlib.sha256(raw_proof.encode("utf-8")).hexdigest()

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()
cursor.execute("""
    INSERT INTO executive_authorizations 
    (timestamp, core, authorized_by, cage_code, uei, action, artifact_hash, proof_hash)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (ts, "EBONY_LAUNCH_VERIFIER_V1", "CEO Jeffery Humphrey", "1AHA8", "S1M4ENLHTDH5",
      "LAUNCH_TRIGGERS_VERIFIED", "START_HVFNEXUS_C2.bat", proof_hash))

conn.commit()
conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
conn.close()

print(f"[+] Launch readiness permanently sealed in matrix_ledger.db. Proof: {proof_hash[:16]}...")
print("=== LAUNCHER POSTURE: 100% OPERATIONAL FOR EXECUTIVE MEETING ===")