import os
import shutil
from pathlib import Path

staging_dir = Path.cwd()
archive_dir = staging_dir / "historical_archive"
archive_dir.mkdir(exist_ok=True)

# The essential pipeline engines that must stay in the airlock
protected_files = {
    "sovereign_coder.py",
    "sovereign_comms.py",
    "sovereign_comms_core.py",
    "sandbox_harness.py",
    "sanitize_sandbox.py",
    "deep_code_sentinel.py",
    "ceo_authorization_gate.py",
    "build_a_production_grade.py"  # Our newly synthesized SCADA module
}

print("==================================================")
print(" 🧹 E.B.O.N.Y. AIRLOCK PURGE & ARCHIVE")
print("==================================================")

archived_count = 0
for py_file in staging_dir.glob("*.py"):
    if py_file.name not in protected_files:
        shutil.move(str(py_file), str(archive_dir / py_file.name))
        archived_count += 1

print(f"[+] Successfully archived {archived_count} historical files.")
print("[+] Protected pipeline engines and active candidate module retained.")

print("\n[*] CURRENT AIRLOCK INVENTORY:")
for remaining in staging_dir.glob("*.py"):
    print(f"    - {remaining.name}")
print("==================================================")
