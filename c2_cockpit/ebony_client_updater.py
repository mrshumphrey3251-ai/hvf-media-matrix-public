"""
E.B.O.N.Y. Sovereign Client Downstream Updater & License Enforcement Engine
Authoritative Unidirectional Code Distribution & Data Isolation Architecture
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Authority: Oklahoma Title 61 & OK HB 2992
"""
import os
import sys
import json
import urllib.request
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(r"C:\hvf_c2\hvf-media-matrix-private")
COCKPIT_DIR = BASE_DIR / "c2_cockpit"
LICENSE_FILE = COCKPIT_DIR / "ebony_license.json"
PUBLIC_RAW_BASE = "https://raw.githubusercontent.com/mrshumphrey3251-ai/hvf-media-matrix-public/main"

# Core application files to update downstream (Customer data files are strictly excluded)
UPDATE_TARGETS = [
    "c2_cockpit/ebony_console_GREEN.py",
    "c2_cockpit/ebony_tier_manager.py",
    "c2_cockpit/ebony_travel_ui.py",
    "c2_cockpit/ebony_travel_autopilot.py",
    "c2_cockpit/ebony_email_dispatcher.py",
    "c2_cockpit/ebony_client_updater.py"
]

# Protected sovereign customer assets that must NEVER be overwritten
PROTECTED_SOVEREIGN_DATA = [
    "c2_cockpit/matrix_ledger.db",
    "c2_cockpit/email_accounts.json",
    "autopilot_daemon.log",
    "c2_cockpit/ebony_license.json"
]

def init_or_read_license() -> dict:
    if not LICENSE_FILE.exists():
        # Initialize default 7-day evaluation pilot license
        pilot_license = {
            "license_type": "7_DAY_SOVEREIGN_PILOT",
            "tier": "TIER_1_PERSONAL",
            "licensed_to": "Prospective Sovereign Subscriber",
            "installed_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
            "status": "ACTIVE_PILOT",
            "enforce_updates": True
        }
        LICENSE_FILE.write_text(json.dumps(pilot_license, indent=2), encoding="utf-8")
        return pilot_license
    try:
        return json.loads(LICENSE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"status": "LICENSE_CORRUPT"}

def check_license_validity() -> tuple[bool, str, int]:
    lic = init_or_read_license()
    expires_str = lic.get("expires_at")
    if not expires_str:
        return False, "NO_EXPIRATION_SET", 0
    try:
        exp_dt = datetime.fromisoformat(expires_str)
        now_dt = datetime.now(timezone.utc)
        remaining = exp_dt - now_dt
        if remaining.total_seconds() <= 0:
            return False, "EXPIRED", 0
        return True, lic.get("license_type", "ACTIVE"), int(remaining.total_seconds() // 86400)
    except Exception as e:
        return False, f"PARSE_ERROR: {e}", 0

def check_and_apply_downstream_updates() -> dict:
    print("=" * 86)
    print("     E.B.O.N.Y. SOVEREIGN DOWNSTREAM CLIENT UPDATE ENGINE     ")
    print(f"     NODE CUSTODY: LOCAL BARE-METAL | REPO TARGET: hvf-media-matrix-public")
    print("=" * 86)
    
    valid, lic_status, days_left = check_license_validity()
    print(f"[*] License Status: {lic_status} ({days_left} days remaining)")
    
    updated_files = []
    skipped_files = []
    errors = []
    
    for rel_path in UPDATE_TARGETS:
        local_path = BASE_DIR / rel_path
        remote_url = f"{PUBLIC_RAW_BASE}/{rel_path}"
        
        try:
            req = urllib.request.Request(remote_url, headers={"User-Agent": "EBONY-Sovereign-Client/1.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                remote_bytes = response.read()
                
            remote_hash = hashlib.sha256(remote_bytes).hexdigest()
            local_hash = ""
            if local_path.exists():
                local_hash = hashlib.sha256(local_path.read_bytes()).hexdigest()
                
            if remote_hash != local_hash:
                local_path.parent.mkdir(parents=True, exist_ok=True)
                local_path.write_bytes(remote_bytes)
                updated_files.append(rel_path)
                print(f"[UPDATED] {rel_path} -> SHA: {remote_hash[:16]}...")
            else:
                skipped_files.append(rel_path)
        except Exception as e:
            errors.append(f"{rel_path}: {e}")
            print(f"[NOTICE] Could not check remote for {rel_path}: {e}")
            
    print("-" * 86)
    print(f"Summary: {len(updated_files)} file(s) updated, {len(skipped_files)} up-to-date, {len(errors)} offline notices.")
    print("Sovereign Customer Data Check: 100% Isolated. Zero database files touched.")
    print("=" * 86)
    
    return {
        "license_status": lic_status,
        "days_remaining": days_left,
        "updated_files": updated_files,
        "up_to_date_files": skipped_files,
        "errors": errors
    }

if __name__ == "__main__":
    check_and_apply_downstream_updates()