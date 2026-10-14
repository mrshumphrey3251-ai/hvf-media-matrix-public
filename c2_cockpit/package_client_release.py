import os
import sys
import shutil
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

base_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private")
cockpit_dir = base_dir / "c2_cockpit"
release_root = Path(r"C:\hvf_c2\releases\ebony_client_rob_teel")
release_cockpit = release_root / "c2_cockpit"

sys.path.insert(0, str(cockpit_dir))
from ebony_crypto_enclave import compute_license_signature, verify_license_integrity

print("\n" + "=" * 90)
print("     E.B.O.N.Y. TURNKEY COMMERCIAL CLIENT PACKAGING ENGINE     ")
print("     RECIPIENT: Rob Teel | TIER: 1 & 1.5 Sovereign Pilot (3 Nodes)     ")
print("=" * 90)

if release_root.exists():
    shutil.rmtree(release_root)
release_cockpit.mkdir(parents=True, exist_ok=True)

DIST_FILES = [
    "ebony_console_GREEN.py",
    "ebony_tier_manager.py",
    "ebony_client_updater.py",
    "ebony_email_dispatcher.py",
    "ebony_travel_ui.py",
    "ebony_travel_autopilot.py",
    "ebony_stripe_billing.py",
    "ebony_crypto_enclave.py"
]

for fname in DIST_FILES:
    src = cockpit_dir / fname
    dst = release_cockpit / fname
    shutil.copy2(src, dst)
    print(f"[EXTRACTED] {fname:<30} -> Staged in release enclave.")

# Live checkout config
sanitized_cfg = {
    "stripe_publishable_key": "",
    "stripe_secret_key": "",
    "webhook_secret": "",
    "custom_payment_links": {
        "TIER_1_PERSONAL": "https://buy.stripe.com/fZuaEXg9l00FdFK03N77O04",
        "TIER_COMMAND": "https://buy.stripe.com/eVqaEX1er6p3eJO4k377O03",
        "TIER_2_VIP": "https://buy.stripe.com/5kQ3cv5uH5kZ59ebMv77O02",
        "TIER_3_ENTERPRISE": "https://buy.stripe.com/6oU7sL8GT3cR59ebMv77O01",
        "TIER_APPLIANCE": "https://buy.stripe.com/aFa9ATbT58xbdFKeYH77O00"
    }
}
(release_cockpit / "stripe_config.json").write_text(json.dumps(sanitized_cfg, indent=2), encoding="utf-8")

# Generate HMAC-signed 7-day pilot license for Rob Teel
now_utc = datetime.now(timezone.utc)
exp_utc = now_utc + timedelta(days=7)

rob_license = {
    "entity": "Humphrey Virtual Farms LLC",
    "cage_code": "1AHA8",
    "uei": "S1M4ENLHTDH5",
    "statutory_authority": "Oklahoma Title 61 & OK HB 2992",
    "license_type": "7_DAY_SOVEREIGN_PILOT",
    "tier": "TIER_COMMAND",
    "licensed_to": "Rob Teel",
    "customer_email": "rob.teel@client-enclave.org",
    "max_nodes": 3,
    "hardware_signatures": [],
    "issued_at": now_utc.isoformat(),
    "expires_at": exp_utc.isoformat(),
    "status": "ACTIVE_PILOT",
    "enforce_updates": True
}
rob_license["integrity_signature"] = compute_license_signature(rob_license)

lic_file = release_cockpit / "ebony_license.json"
lic_file.write_text(json.dumps(rob_license, indent=2), encoding="utf-8")
print(f"[SIGNED] ebony_license.json -> Cryptographic HMAC signature embedded.")

# Turnkey Windows Launcher
bat_content = """@echo off
title E.B.O.N.Y. Sovereign Command Console // Humphrey Virtual Farms LLC
color 0A
set PYTHONIOENCODING=utf-8

echo ==============================================================================
echo     E.B.O.N.Y. SOVEREIGN BARE-METAL C2 CONSOLE // INITIALIZATION
echo     Entity: Humphrey Virtual Farms LLC ^| CAGE: 1AHA8 ^| UEI: S1M4ENLHTDH5
echo     Licensed To: Rob Teel ^| Status: Active Sovereign Pilot
echo ==============================================================================
echo.

python -m streamlit run c2_cockpit\\ebony_console_GREEN.py --server.port 8501 --server.address 0.0.0.0 --server.headless false
pause
"""
(release_root / "run_ebony.bat").write_text(bat_content, encoding="utf-8")

manual_src = base_dir / "EBONY_USER_MANUAL_AND_LEGAL_DISCLAIMER.md"
if manual_src.exists():
    shutil.copy2(manual_src, release_root / "EBONY_USER_MANUAL_AND_LEGAL_DISCLAIMER.md")

print(f">>> [SUCCESS] CLIENT PACKAGE GENERATED AT: {release_root} <<<")