import json
import sys
from pathlib import Path

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
sys.path.insert(0, str(cockpit_dir))

config_file = cockpit_dir / "stripe_config.json"

live_catalog = {
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

config_file.write_text(json.dumps(live_catalog, indent=2), encoding="utf-8")
print(f"[+] Wrote verified live Stripe endpoints directly to: {config_file}")

from ebony_stripe_billing import get_checkout_url_for_tier, STRIPE_TIER_CATALOG

print("\n" + "=" * 92)
print("     E.B.O.N.Y. SOVEREIGN COMMERCIAL STRIPE PRODUCTION AUDIT (5 TIERS)     ")
print("     MERCHANT ACCOUNT: acct_1U7KW1DYh3ZQm4hd | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5")
print("=" * 92)

all_live = True
for tier_key, meta in STRIPE_TIER_CATALOG.items():
    url, is_live = get_checkout_url_for_tier(tier_key)
    status = "LIVE STRIPE CHECKOUT" if is_live else "SOVEREIGN SIMULATION FALLBACK"
    print(f"[*] {meta['tier_name']:<28} | ${meta['price_usd']:>7.2f}/{meta['interval']:<8} | Nodes: {meta['nodes']:<3}")
    print(f"    Status: [{status}]")
    print(f"    Target: {url}")
    print("-" * 92)
    if not is_live:
        all_live = False

if all_live:
    print(">>> [SUCCESS] 100% OF TIERS ROUTING TO LIVE STRIPE PRODUCTION CHECKOUT. <<<")
else:
    print(">>> [CRITICAL] ONE OR MORE TIERS FAILED TO RESOLVE AS LIVE. <<<")
    sys.exit(1)
print("=" * 92 + "\n")