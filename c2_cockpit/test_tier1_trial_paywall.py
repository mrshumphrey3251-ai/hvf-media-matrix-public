import sys
from pathlib import Path
import py_compile

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
sys.path.insert(0, str(cockpit_dir))

from ebony_tier_manager import (
    TIER_0_CEO,
    TIER_1_PERSONAL,
    TIER_COMMAND,
    TIER_EXPIRED,
    check_module_access,
    MODULE_TIER_MAPPING
)

from ebony_stripe_billing import get_checkout_url_for_tier

print("\n" + "=" * 90)
print("     E.B.O.N.Y. 7-DAY PILOT & TIER 1 PAYWALL VERIFICATION HARNESS     ")
print("=" * 90)

passed = 0
failed = 0

def test(name, condition, details=""):
    global passed, failed
    if condition:
        print(f"  [PASS] {name} {details}")
        passed += 1
    else:
        print(f"  [FAIL] {name} {details}")
        failed += 1

# TEST 1: Tier 1 Modules must be BLOCKED when Trial is Expired
tier1_mods = ["📨 Sovereign Dispatch Deck", "🚨 NOAA Radar", "📝 Feedback Hub"]
for mod in tier1_mods:
    allowed, req, is_m = check_module_access(TIER_EXPIRED, mod)
    test(f"Expired Trial Blocks '{mod}'", not allowed and "19.99" in req, f"-> Paywall target: {req}")

# TEST 2: System Overview MUST stay accessible so expired users can upgrade
ov_allowed, _, _ = check_module_access(TIER_EXPIRED, "📖 System Overview")
test("Expired Trial Allows '📖 System Overview'", ov_allowed, "-> Landing page accessible for checkout")

# TEST 3: Active Tier 1 subscriber has access to Tier 1 modules
for mod in tier1_mods:
    allowed, req, is_m = check_module_access(TIER_1_PERSONAL, mod)
    test(f"Paid Tier 1 Allows '{mod}'", allowed, "-> Entitled access granted")

# TEST 4: Paid Tier 1 subscriber is BLOCKED from Tier 1.5 Command
cmd_allowed, cmd_req, _ = check_module_access(TIER_1_PERSONAL, "💬 Sovereign Command")
test("Paid Tier 1 Blocks '💬 Sovereign Command'", not cmd_allowed and "39.99" in cmd_req, f"-> Paywall: {cmd_req}")

# TEST 5: Verify Live Tier 1 Checkout URL matches Stripe link
t1_url, is_live = get_checkout_url_for_tier(TIER_1_PERSONAL)
test("Tier 1 Paywall Routes to Live Stripe Link", is_live and "fZuaEXg9l00FdFK03N77O04" in t1_url, f"-> URL: {t1_url}")

# TEST 6: Bytecode Compilation
try:
    py_compile.compile(str(cockpit_dir / "ebony_tier_manager.py"), doraise=True)
    test("Compile ebony_tier_manager.py", True, "-> Exit Code 0")
except Exception as e:
    test("Compile ebony_tier_manager.py", False, f"-> Error: {e}")

print("\n" + "=" * 90)
print(f"VERIFICATION SUMMARY: {passed} PASSED | {failed} FAILED")
if failed == 0:
    print(">>> [SUCCESS] 7-DAY PILOT CLOCK & TIER 1 PAYWALL 100% OPERATIONAL. <<<")
else:
    print(">>> [CRITICAL] ONE OR MORE VERIFICATION ASSERTIONS FAILED. <<<")
    sys.exit(1)
print("=" * 90 + "\n")