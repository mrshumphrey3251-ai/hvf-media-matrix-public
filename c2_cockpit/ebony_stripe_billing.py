"""
E.B.O.N.Y. Sovereign Commercial Billing & Stripe Integration Engine
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Authority: Oklahoma Title 61 & OK HB 2992
"""
import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

COCKPIT_DIR = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
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
    """
    Returns (checkout_url, is_live_stripe).
    If no registered live Stripe Payment Link is present, returns an in-cockpit
    sovereign activation URL that fulfills the license directly on glass with zero XML errors.
    """
    cfg = init_or_read_stripe_config()
    links = cfg.get("custom_payment_links", {})
    custom = links.get(tier_key, "").strip()
    
    if custom.startswith("https://buy.stripe.com/") and "test_" not in custom and "placeholder" not in custom:
        return custom, True
        
    simulation_url = f"{base_url}/?payment=success&tier={tier_key}&email=ceo@humphreyfarms.org"
    return simulation_url, False
