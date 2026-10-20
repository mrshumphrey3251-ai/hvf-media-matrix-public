import sys
from pathlib import Path
import py_compile

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
sys.path.insert(0, str(cockpit_dir))

from ebony_tier_manager import (
    TIER_0_CEO,
    TIER_1_PERSONAL,
    TIER_COMMAND,
    TIER_2_VIP,
    TIER_EXPIRED,
    check_module_access,
    MAINTENANCE_MODULES
)

from ebony_stripe_billing import get_checkout_url_for_tier

print("\n" + "=" * 90)
print("     E.B.O.N.Y. TIER 1 & 1.5 PILOT & OPTICAL SENSOR MAINTENANCE AUDIT     ")
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

# TEST 1: Optical Sensors Bus (Sovereign Comms Deck) cordoned behind Maintenance Wall for non-CEO
comms_allowed, comms_req, is_m = check_module_access(TIER_COMMAND, "📡 Sovereign Comms Deck")
test("Sovereign Comms Deck Locked in Maintenance", not comms_allowed and is_m, "-> Status: Level-5 R&D Lockout")

# TEST 2: CEO maintains root access to Sovereign Comms Deck for ongoing calibration
ceo_comms_allowed, _, _ = check_module_access(TIER_0_CEO, "📡 Sovereign Comms Deck")
test("CEO Access to Sovereign Comms Deck", ceo_comms_allowed, "-> Status: CEO Root Authorized")

# TEST 3: Active Pilot (Tier 1.5) has access to Tier 1 Modules
tier1_mods = ["📨 Sovereign Dispatch Deck", "🚨 NOAA Radar", "📝 Feedback Hub"]
for mod in tier1_mods:
    allowed, _, _ = check_module_access(TIER_COMMAND, mod)
    test(f"Pilot Allows Tier 1 '{mod}'", allowed, "-> Access Granted")

# TEST 4: Active Pilot (Tier 1.5) has access to Tier 1.5 Sovereign Command
cmd_allowed, _, _ = check_module_access(TIER_COMMAND, "💬 Sovereign Command")
test("Pilot Allows Tier 1.5 '💬 Sovereign Command'", cmd_allowed, "-> Access Granted")

# TEST 5: Active Pilot (Tier 1.5) blocked from Tier 2 VIP ($249/mo)
vip_allowed, vip_req, _ = check_module_access(TIER_COMMAND, "🎛️ Master C2 Cockpit")
test("Pilot Blocks Tier 2 '🎛️ Master C2 Cockpit'", not vip_allowed and "$249" in vip_req, f"-> Requires: {vip_req}")

# TEST 6: Expired Pilot blocks Tier 1 and Tier 1.5 modules
exp_t1_allowed, _, _ = check_module_access(TIER_EXPIRED, "📨 Sovereign Dispatch Deck")
exp_cmd_allowed, _, _ = check_module_access(TIER_EXPIRED, "💬 Sovereign Command")
test("Expired Pilot Blocks Tier 1 Dispatch", not exp_t1_allowed, "-> Paywall Triggered")
test("Expired Pilot Blocks Tier 1.5 Command", not exp_cmd_allowed, "-> Paywall Triggered")

# TEST 7: Expired Pilot allows System Overview for checkout
ov_allowed, _, _ = check_module_access(TIER_EXPIRED, "📖 System Overview")
test("Expired Pilot Allows System Overview", ov_allowed, "-> Commercial Store Accessible")

# TEST 8: Live Stripe links configured for both Tier 1 and Tier 1.5
t1_url, is_live_t1 = get_checkout_url_for_tier(TIER_1_PERSONAL)
cmd_url, is_live_cmd = get_checkout_url_for_tier(TIER_COMMAND)
test("Tier 1 Live Stripe Link", is_live_t1 and "fZuaEXg9l00FdFK03N77O04" in t1_url, f"-> {t1_url}")
test("Tier 1.5 Live Stripe Link", is_live_cmd and "eVqaEX1er6p3eJO4k377O03" in cmd_url, f"-> {cmd_url}")

# TEST 9: Compilation of both modified files
try:
    py_compile.compile(str(cockpit_dir / "ebony_tier_manager.py"), doraise=True)
    test("Compile ebony_tier_manager.py", True, "-> Exit Code 0")
except Exception as e:
    test("Compile ebony_tier_manager.py", False, f"-> Error: {e}")

try:
    py_compile.compile(str(cockpit_dir / "ebony_client_updater.py"), doraise=True)
    test("Compile ebony_client_updater.py", True, "-> Exit Code 0")
except Exception as e:
    test("Compile ebony_client_updater.py", False, f"-> Error: {e}")

print("\n" + "=" * 90)
print(f"VERIFICATION SUMMARY: {passed} PASSED | {failed} FAILED")
if failed == 0:
    print(">>> [SUCCESS] 7-DAY PILOT (TIER 1 & 1.5) + OPTICAL MAINTENANCE ENCLAVE CERTIFIED. <<<")
else:
    print(">>> [CRITICAL] ONE OR MORE VERIFICATION ASSERTIONS FAILED. <<<")
    sys.exit(1)
print("=" * 90 + "\n")