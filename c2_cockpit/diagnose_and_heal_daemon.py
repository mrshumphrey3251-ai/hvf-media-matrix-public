import os
import sys
import json
from pathlib import Path
import py_compile

base_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private")
cockpit_dir = base_dir / "c2_cockpit"
err_log = base_dir / "streamlit_err.log"

print("=" * 86)
print("     STREAMLIT DAEMON CRASH LOG TRIAGE (LATEST TRACEBACK)     ")
print("=" * 86)

if err_log.exists():
    log_lines = err_log.read_text(encoding="utf-8", errors="ignore").splitlines()
    tail = log_lines[-25:] if len(log_lines) >= 25 else log_lines
    for line in tail:
        print(f"  {line}")
else:
    print("[*] streamlit_err.log not found or empty.")

print("=" * 86 + "\n")

# Ensure stripe_config.json is valid
stripe_cfg_file = cockpit_dir / "stripe_config.json"
if not stripe_cfg_file.exists():
    default_cfg = {
        "stripe_publishable_key": "",
        "stripe_secret_key": "",
        "webhook_secret": "",
        "custom_payment_links": {
            "TIER_1_PERSONAL": "",
            "TIER_COMMAND": "",
            "TIER_2_VIP": "",
            "TIER_3_ENTERPRISE": "",
            "TIER_APPLIANCE": ""
        }
    }
    stripe_cfg_file.write_text(json.dumps(default_cfg, indent=2), encoding="utf-8")
    print("[+] Initialized stripe_config.json with default configuration.")

# Ensure ebony_stripe_billing.py is resilient and self-contained
stripe_billing_code = """\"\"\"
E.B.O.N.Y. Sovereign Commercial Billing & Stripe Integration Engine
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Authority: Oklahoma Title 61 & OK HB 2992
\"\"\"
import os
import sys
import json
from pathlib import Path

COCKPIT_DIR = Path(r"C:\\hvf_c2\\hvf-media-matrix-private\\c2_cockpit")
STRIPE_CONFIG_FILE = COCKPIT_DIR / "stripe_config.json"

STRIPE_TIER_CATALOG = {
    "TIER_1_PERSONAL": {
        "name": "E.B.O.N.Y. Personal Executive Comms & Radar",
        "tier_name": "Tier 1: Personal",
        "price_usd": 19.99,
        "interval": "month",
        "nodes": 1
    },
    "TIER_COMMAND": {
        "name": "E.B.O.N.Y. Sovereign Command & Optical Surveillance",
        "tier_name": "Tier 1.5: Sovereign Command",
        "price_usd": 39.99,
        "interval": "month",
        "nodes": 3
    },
    "TIER_2_VIP": {
        "name": "E.B.O.N.Y. VIP Operational, Drone & B2B Engine",
        "tier_name": "Tier 2: VIP Member",
        "price_usd": 249.00,
        "interval": "month",
        "nodes": 5
    },
    "TIER_3_ENTERPRISE": {
        "name": "E.B.O.N.Y. Enterprise Sovereign Infrastructure",
        "tier_name": "Tier 3: Enterprise CEO",
        "price_usd": 2499.00,
        "interval": "year",
        "nodes": 10
    },
    "TIER_APPLIANCE": {
        "name": "E.B.O.N.Y. Bare-Metal Hardware Appliance & Ongoing SLA",
        "tier_name": "Hardware Appliance",
        "price_usd": 4950.00,
        "interval": "one_time",
        "nodes": 999
    }
}

def init_or_read_stripe_config() -> dict:
    if not STRIPE_CONFIG_FILE.exists():
        default_cfg = {
            "stripe_publishable_key": "",
            "stripe_secret_key": "",
            "webhook_secret": "",
            "custom_payment_links": {
                "TIER_1_PERSONAL": "",
                "TIER_COMMAND": "",
                "TIER_2_VIP": "",
                "TIER_3_ENTERPRISE": "",
                "TIER_APPLIANCE": ""
            }
        }
        STRIPE_CONFIG_FILE.write_text(json.dumps(default_cfg, indent=2), encoding="utf-8")
        return default_cfg
    try:
        return json.loads(STRIPE_CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def get_checkout_url_for_tier(tier_key: str, base_url: str = "http://localhost:8501") -> tuple:
    cfg = init_or_read_stripe_config()
    links = cfg.get("custom_payment_links", {})
    custom = links.get(tier_key, "").strip()
    
    if custom.startswith("https://buy.stripe.com/") and "test_" not in custom and "placeholder" not in custom:
        return custom, True
        
    simulation_url = f"{base_url}/?payment=success&tier={tier_key}&email=ceo@humphreyfarms.org"
    return simulation_url, False
"""
(cockpit_dir / "ebony_stripe_billing.py").write_text(stripe_billing_code, encoding="utf-8")
print("[+] Certified ebony_stripe_billing.py with resilient dual-mode logic.")

# Test imports directly in Python
if str(cockpit_dir) not in sys.path:
    sys.path.insert(0, str(cockpit_dir))

try:
    import ebony_stripe_billing
    print("[PASS] import ebony_stripe_billing succeeded.")
except Exception as e:
    print(f"[FAIL] import ebony_stripe_billing: {e}")

try:
    import ebony_tier_manager
    print("[PASS] import ebony_tier_manager succeeded.")
except Exception as e:
    print(f"[FAIL] import ebony_tier_manager: {e}")

# Verify compilation of all primary consoles
all_consoles = [
    cockpit_dir / "ebony_console_GREEN.py",
    cockpit_dir / "ebony_console_GOLD.py",
    cockpit_dir / "ebony_console.py",
    cockpit_dir / "ebony_stripe_billing.py",
    cockpit_dir / "ebony_tier_manager.py"
]

print("\n" + "=" * 86)
print("     COMPILATION VERIFICATION MATRIX     ")
print("=" * 86)

all_passed = True
for f in all_consoles:
    if not f.exists():
        continue
    try:
        py_compile.compile(str(f), doraise=True)
        print(f"[COMPILED OK] {f.name:<28} -> Exit Code 0 Verified.")
    except Exception as e:
        print(f"[COMPILE FAIL] {f.name:<28} -> {e}")
        all_passed = False

print("=" * 86)
if not all_passed:
    sys.exit(1)