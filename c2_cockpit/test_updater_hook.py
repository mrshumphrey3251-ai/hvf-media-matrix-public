import sys
from pathlib import Path

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
sys.path.insert(0, str(cockpit_dir))

try:
    from ebony_client_updater import check_license_validity, check_and_apply_downstream_updates
    
    is_valid, lic_type, days = check_license_validity()
    print("\n" + "=" * 80)
    print(f"     [LICENSE AUDIT] Valid: {is_valid} | Type: {lic_type} | Days Remaining: {days}")
    print("=" * 80)
    
    res = check_and_apply_downstream_updates()
    print("\n" + "=" * 80)
    print(f"     [UPDATE AUDIT] Files Checked: {len(res['up_to_date_files']) + len(res['updated_files'])} | Updates Applied: {len(res['updated_files'])}")
    print("=" * 80 + "\n")
except Exception as e:
    print(f"[CRITICAL ERROR] Failed to execute updater hook: {e}")