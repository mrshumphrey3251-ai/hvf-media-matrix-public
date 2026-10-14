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

# Sovereign Commercial Price Catalog
STRIPE_TIER_CATALOG = {
    "TIER_1_PERSONAL": {
        "name": "E.B.O.N.Y. Personal Executive Comms & Radar",
        "tier_name": "Tier 1: Personal",
        "price_usd": 19.99,
        "amount_cents": 1999,
        "interval": "month",
        "nodes": 1,
        "default_payment_link": "https://buy.stripe.com/test_personal_1999",
        "stripe_price_id": "price_personal_1999"
    },
    "TIER_COMMAND": {
        "name": "E.B.O.N.Y. Sovereign Command & Optical Surveillance",
        "tier_name": "Tier 1.5: Sovereign Command",
        "price_usd": 39.99,
        "amount_cents": 3999,
        "interval": "month",
        "nodes": 3,
        "default_payment_link": "https://buy.stripe.com/test_command_3999",
        "stripe_price_id": "price_command_3999"
    },
    "TIER_2_VIP": {
        "name": "E.B.O.N.Y. VIP Operational, Drone & B2B Engine",
        "tier_name": "Tier 2: VIP Member",
        "price_usd": 249.00,
        "amount_cents": 24900,
        "interval": "month",
        "nodes": 5,
        "default_payment_link": "https://buy.stripe.com/test_vip_24900",
        "stripe_price_id": "price_vip_24900"
    },
    "TIER_3_ENTERPRISE": {
        "name": "E.B.O.N.Y. Enterprise Sovereign Infrastructure",
        "tier_name": "Tier 3: Enterprise CEO",
        "price_usd": 2499.00,
        "amount_cents": 249900,
        "interval": "year",
        "nodes": 10,
        "default_payment_link": "https://buy.stripe.com/test_enterprise_249900",
        "stripe_price_id": "price_enterprise_249900"
    },
    "TIER_APPLIANCE": {
        "name": "E.B.O.N.Y. Bare-Metal Hardware Appliance & Ongoing SLA",
        "tier_name": "Hardware Appliance",
        "price_usd": 4950.00,
        "amount_cents": 495000,
        "interval": "one_time",
        "nodes": 999,
        "default_payment_link": "https://buy.stripe.com/test_appliance_495000",
        "stripe_price_id": "price_appliance_495000"
    }
}

def init_or_read_stripe_config() -> dict:
    if not STRIPE_CONFIG_FILE.exists():
        default_cfg = {
            "stripe_publishable_key": "pk_live_placeholder_hvf_sovereign",
            "stripe_secret_key": "sk_live_placeholder_hvf_sovereign",
            "webhook_secret": "whsec_placeholder_hvf_sovereign",
            "custom_payment_links": {
                "TIER_1_PERSONAL": "https://buy.stripe.com/test_personal_1999",
                "TIER_COMMAND": "https://buy.stripe.com/test_command_3999",
                "TIER_2_VIP": "https://buy.stripe.com/test_vip_24900",
                "TIER_3_ENTERPRISE": "https://buy.stripe.com/test_enterprise_249900",
                "TIER_APPLIANCE": "https://buy.stripe.com/test_appliance_495000"
            }
        }
        STRIPE_CONFIG_FILE.write_text(json.dumps(default_cfg, indent=2), encoding="utf-8")
        return default_cfg
    try:
        return json.loads(STRIPE_CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def get_checkout_url_for_tier(tier_key: str) -> str:
    cfg = init_or_read_stripe_config()
    links = cfg.get("custom_payment_links", {})
    if tier_key in links and links[tier_key].startswith("http"):
        return links[tier_key]
    
    tier_info = STRIPE_TIER_CATALOG.get(tier_key, {})
    return tier_info.get("default_payment_link", "https://stripe.com")

def create_live_stripe_session(tier_key: str, customer_email: str = None) -> tuple:
    cfg = init_or_read_stripe_config()
    secret_key = cfg.get("stripe_secret_key", "")
    
    if not secret_key or "placeholder" in secret_key:
        return False, get_checkout_url_for_tier(tier_key)
        
    tier_info = STRIPE_TIER_CATALOG.get(tier_key)
    if not tier_info:
        return False, "Invalid Tier Selection"

    url = "https://api.stripe.com/v1/checkout/sessions"
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    mode = "payment" if tier_info["interval"] == "one_time" else "subscription"
    params = {
        "mode": mode,
        "success_url": "http://localhost:8501/?payment=success&session_id={CHECKOUT_SESSION_ID}",
        "cancel_url": "http://localhost:8501/?payment=cancelled",
        "line_items[0][price_data][currency]": "usd",
        "line_items[0][price_data][unit_amount]": str(tier_info["amount_cents"]),
        "line_items[0][price_data][product_data][name]": tier_info["name"],
        "line_items[0][quantity]": "1"
    }

    if mode == "subscription":
        params["line_items[0][price_data][recurring][interval]"] = tier_info["interval"]

    if customer_email:
        params["customer_email"] = customer_email

    try:
        data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return True, body.get("url")
    except Exception as e:
        return False, f"Stripe API Error: {e}"

if __name__ == "__main__":
    print("=" * 80)
    print("     E.B.O.N.Y. SOVEREIGN STRIPE BILLING & CATALOG VERIFICATION     ")
    print("=" * 80)
    for k, v in STRIPE_TIER_CATALOG.items():
        print(f"• {k:<18} | ${v['price_usd']:>7.2f}/{v['interval']} | Nodes: {v['nodes']:<3} | Link: {get_checkout_url_for_tier(k)}")
    print("=" * 80)