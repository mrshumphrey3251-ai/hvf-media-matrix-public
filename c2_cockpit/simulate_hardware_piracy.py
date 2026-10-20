import sys
import json
from pathlib import Path

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
sys.path.insert(0, str(cockpit_dir))

from ebony_client_updater import check_license_validity, get_hardware_uuid

lic_path = cockpit_dir / "ebony_license.json"

if not lic_path.exists():
    print("[CRITICAL ERROR] ebony_license.json not found on disk.")
    sys.exit(1)

lic_data = json.loads(lic_path.read_text(encoding="utf-8"))

print("\n" + "=" * 80)
print("     [HW_AUDIT] Original Machine Signature: " + lic_data.get("hardware_signature", "UNKNOWN"))

# SIMULATING PIRACY: Modify the license file to simulate running on a different computer
print("     [HW_AUDIT] Simulating unauthorized copy to external device...")
lic_data["hardware_signature"] = "badd01234invalidhw56789signature"
lic_path.write_text(json.dumps(lic_data), encoding="utf-8")

# Re-run license validity check
is_valid, lic_status, _ = check_license_validity()
print(f"     [HW_AUDIT] Validity Check Returns: Valid={is_valid} | Status={lic_status}")

if lic_status == "HARDWARE_MISMATCH_PIRACY_LOCKOUT":
    print("     [SUCCESS] Piracy detected! Hardware lock successfully engaged.")
else:
    print("     [ERROR] Hardware lock failed to engage.")

# RESTORING TRUE LICENSE FOR LIVE OPERATIONS
print("     [HW_AUDIT] Restoring true hardware signature for live operations...")
lic_data["hardware_signature"] = get_hardware_uuid()
lic_path.write_text(json.dumps(lic_data), encoding="utf-8")
print("=" * 80 + "\n")