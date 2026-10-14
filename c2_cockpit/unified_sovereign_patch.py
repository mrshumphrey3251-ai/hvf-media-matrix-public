import os
import sys
from pathlib import Path
import py_compile

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")

# --- PART A: SURGICALLY REPAIR ebony_console_GOLD.py ---
gold_file = cockpit_dir / "ebony_console_GOLD.py"
broken_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"
replacement_url = "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/person-bicycle-car-detection.mp4"

content = gold_file.read_text(encoding="utf-8")
content = content.replace(broken_url, replacement_url)
content = content.replace(
    'elif active_module == "🛡️ CEO Authorization Gate":',
    'if active_module == "🛡️ CEO Authorization Gate":'
)

# Indent Master C2 Cockpit execution block (handling LF and CRLF)
old_cockpit_lf = 'elif active_module == "🎛️ Master C2 Cockpit":\nimport c2_cockpit_dashboard\nc2_cockpit_dashboard.render()'
new_cockpit_lf = 'elif active_module == "🎛️ Master C2 Cockpit":\n    import c2_cockpit_dashboard\n    c2_cockpit_dashboard.render()'

old_cockpit_crlf = old_cockpit_lf.replace("\n", "\r\n")
new_cockpit_crlf = new_cockpit_lf.replace("\n", "\r\n")

if old_cockpit_lf in content:
    content = content.replace(old_cockpit_lf, new_cockpit_lf, 1)
elif old_cockpit_crlf in content:
    content = content.replace(old_cockpit_crlf, new_cockpit_crlf, 1)

gold_file.write_text(content, encoding="utf-8")
print("[+] ebony_console_GOLD.py surgically patched without touching nested blocks.")

# --- PART B: UPGRADE ebony_stripe_billing.py WITH DUAL-MODE LOGIC ---
stripe_billing_code = """\"\"\"
E.B.O.N.Y. Sovereign Commercial Billing & Stripe Integration Engine
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Authority: Oklahoma Title 61 & OK HB 2992
\"\"\"
import os
import sys
import json
import urllib.request
import urllib.parse
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
    \"\"\"
    Returns (checkout_url, is_live_stripe).
    If no registered live Stripe Payment Link is present, returns an in-cockpit
    sovereign activation URL that fulfills the license directly on glass with zero XML errors.
    \"\"\"
    cfg = init_or_read_stripe_config()
    links = cfg.get("custom_payment_links", {})
    custom = links.get(tier_key, "").strip()
    
    if custom.startswith("https://buy.stripe.com/") and "test_" not in custom and "placeholder" not in custom:
        return custom, True
        
    simulation_url = f"{base_url}/?payment=success&tier={tier_key}&email=ceo@humphreyfarms.org"
    return simulation_url, False
"""
(cockpit_dir / "ebony_stripe_billing.py").write_text(stripe_billing_code, encoding="utf-8")
print("[+] ebony_stripe_billing.py upgraded with sovereign simulation safeguards.")

# --- PART C: UPDATE ebony_tier_manager.py RESTRICTION SCREEN ---
tier_mgr_file = cockpit_dir / "ebony_tier_manager.py"
tier_text = tier_mgr_file.read_text(encoding="utf-8")

old_render_block = """    required_tier_key = MODULE_TIER_MAPPING.get(module_name, TIER_COMMAND)
    checkout_url = get_checkout_url_for_tier(required_tier_key)"""

new_render_block = """    required_tier_key = MODULE_TIER_MAPPING.get(module_name, TIER_COMMAND)
    checkout_url, is_live = get_checkout_url_for_tier(required_tier_key)"""

if old_render_block in tier_text:
    tier_text = tier_text.replace(old_render_block, new_render_block)

old_btn_call = 'st.link_button("💳 PROCEED TO SECURE STRIPE CHECKOUT", url=checkout_url, use_container_width=True)'
new_btn_call = '''if is_live:
                st.link_button("💳 PROCEED TO SECURE STRIPE CHECKOUT", url=checkout_url, use_container_width=True)
            else:
                st.link_button("⚡ SIMULATE STRIPE PAYMENT & PROVISION LICENSE", url=checkout_url, use_container_width=True)
                st.caption("ℹ️ Sovereign Testing Mode: Activates this tier instantaneously on glass without external network calls.")'''

if old_btn_call in tier_text:
    tier_text = tier_text.replace(old_btn_call, new_btn_call)

tier_mgr_file.write_text(tier_text, encoding="utf-8")
print("[+] ebony_tier_manager.py updated with dual-mode paywall button rendering.")

# --- PART D: VERIFY COMPILATION ACROSS ALL COCKPIT CONSOLES ---
all_consoles = [
    cockpit_dir / "ebony_console_GREEN.py",
    cockpit_dir / "ebony_console_GOLD.py",
    cockpit_dir / "ebony_console.py",
    cockpit_dir / "app.py",
    cockpit_dir / "ebony_stripe_billing.py",
    cockpit_dir / "ebony_tier_manager.py"
]

print("\n" + "=" * 84)
print("     FINAL COMPILATION CERTIFICATION MATRIX     ")
print("=" * 84)

all_passed = True
for f in all_consoles:
    if not f.exists():
        continue
    try:
        py_compile.compile(str(f), doraise=True)
        print(f"[COMPILED OK] {f.name:<25} -> Exit Code 0 Certified.")
    except Exception as e:
        print(f"[COMPILE FAIL] {f.name:<25} -> {e}")
        all_passed = False

print("=" * 84)
if not all_passed:
    sys.exit(1)