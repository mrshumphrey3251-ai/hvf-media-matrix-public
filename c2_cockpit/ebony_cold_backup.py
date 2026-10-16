import os
import sys
import shutil
import hashlib
import zipfile
from datetime import datetime, timezone
from pathlib import Path

base_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private")
cockpit_dir = base_dir / "c2_cockpit"
backup_root = Path(r"C:\hvf_c2\backups")
backup_root.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
archive_name = f"EBONY_COLD_SNAPSHOT_{timestamp}.zip"
archive_path = backup_root / archive_name

CRITICAL_TARGETS = [
    base_dir / "matrix_ledger.db",
    cockpit_dir / "stripe_config.json",
    cockpit_dir / "state_contractor_registry.json",
    cockpit_dir / "ebony_crypto_enclave.py",
    cockpit_dir / "ebony_tier_manager.py"
]

print("\n" + "=" * 90)
print("     E.B.O.N.Y. SOVEREIGN WORM COLD STORAGE SNAPSHOT DAEMON     ")
print(f"     DESTINATION: {archive_path}")
print("=" * 90)

with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for target in CRITICAL_TARGETS:
        if target.exists():
            zf.write(target, arcname=target.name)
            print(f"[PACKED] {target.name:<32} ({target.stat().st_size} bytes)")
        else:
            print(f"[SKIP]   {target.name:<32} (Not found)")

archive_hash = hashlib.sha256(archive_path.read_bytes()).hexdigest()

seal_file = backup_root / f"{archive_name}.sha256"
seal_file.write_text(f"{archive_hash}  *{archive_name}\n", encoding="utf-8")

print("-" * 90)
print(f"[SUCCESS] Cold Storage Archive Created: {archive_path.name}")
print(f"[*] Authoritative SHA-256 Seal:        {archive_hash}")
print("=" * 90 + "\n")