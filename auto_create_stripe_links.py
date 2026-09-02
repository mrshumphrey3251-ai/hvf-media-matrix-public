import os
import sys
import subprocess

try:
    import stripe
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "stripe"])
    import stripe

# 1. INJECT SECRET KEY
STRIPE_KEY = "PASTE_YOUR_SK_TEST_KEY_HERE"  # <-- Paste your sk_test_... key here
stripe.api_key = STRIPE_KEY.strip()

print("⚡ Connecting to Stripe API...")

# Product 1: Already created
personal_link = "https://buy.stripe.com/test_fZueVfbmx9lH4rB8yx1RC00"

# Product 2: VIP Farm Member ($249/mo)
vip_prod = stripe.Product.create(
    name="VIP Farm Member",
    description="Live universal drone stream, Green Leaf Index canopy scoring, multi-zone IoT sensor mesh."
)
vip_price = stripe.Price.create(
    product=vip_prod.id,
    unit_amount=24900,  # $249.00
    currency="usd",
    recurring={"interval": "month"}
)
vip_pl = stripe.PaymentLink.create(
    line_items=[{"price": vip_price.id, "quantity": 1}]
)
print(f"✅ Created VIP Member Link: {vip_pl.url}")

# Product 3: Enterprise Farm CEO ($2,499/yr)
corp_prod = stripe.Product.create(
    name="Enterprise Farm CEO (Annual)",
    description="Client CEO dashboard, staff sub-key provisioning, multi-ranch analytics."
)
corp_price = stripe.Price.create(
    product=corp_prod.id,
    unit_amount=249900,  # $2,499.00
    currency="usd",
    recurring={"interval": "year"}
)
corp_pl = stripe.PaymentLink.create(
    line_items=[{"price": corp_price.id, "quantity": 1}]
)
print(f"✅ Created Enterprise CEO Link: {corp_pl.url}")

# 2. Write directly into .env vault
env_path = r"C:\HVF_Repos\hvf-media-matrix-private\.env"
lines = []
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

new_lines = []
keys_to_update = {
    "STRIPE_SECRET_KEY": stripe.api_key,
    "STRIPE_PERSONAL_LINK": personal_link,
    "STRIPE_MONTHLY_LINK": vip_pl.url,
    "STRIPE_ANNUAL_LINK": corp_pl.url,
    "PAYPAL_PAY_LINK": "https://www.paypal.com/paypalme/humphreyvirtualfarm"
}

updated_keys = set()
for line in lines:
    matched = False
    for k, v in keys_to_update.items():
        if line.startswith(f"{k}="):
            new_lines.append(f"{k}={v}\n")
            updated_keys.add(k)
            matched = True
            break
    if not matched:
        new_lines.append(line)

for k, v in keys_to_update.items():
    if k not in updated_keys:
        new_lines.append(f"{k}={v}\n")

with open(env_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("🎉 [STEP 2 COMPLETE]: All 3 Stripe Links generated and locked into .env private vault!")