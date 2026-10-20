import sys
from pathlib import Path
import py_compile

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
sys.path.insert(0, str(cockpit_dir))

from ebony_tier_manager import (
    TIER_1_COMMS,
    TIER_COMMAND,
    TIER_2_SCADA,
    TIER_3_DRONE,
    TIER_0_CEO,
    check_module_access
)

# Test 1: Tier 1 user accessing NOAA Radar (MUST BE ALLOWED)
allowed, req, _ = check_module_access(TIER_1_COMMS, "🚨 NOAA Radar")
assert allowed, "FAILED: Tier 1 should have access to NOAA Radar!"
print("[+] VERIFIED: Tier 1 subscriber ($19.99/mo) granted access to 🚨 NOAA Radar.")

# Test 2: Tier 1 user accessing Sovereign Command (MUST BE BLOCKED FOR $39.99 TIER)
allowed, req, _ = check_module_access(TIER_1_COMMS, "💬 Sovereign Command")
assert not allowed and "39.99" in req, f"FAILED: Tier 1 should be blocked from Sovereign Command, got req={req}"
print(f"[+] VERIFIED: Tier 1 subscriber blocked from 💬 Sovereign Command -> Requires: {req}")

# Test 3: Tier Command user ($39.99) accessing Sovereign Command (MUST BE ALLOWED)
allowed, req, _ = check_module_access(TIER_COMMAND, "💬 Sovereign Command")
assert allowed, "FAILED: Tier Command ($39.99) should have access to Sovereign Command!"
print("[+] VERIFIED: Tier 1.5 subscriber ($39.99/mo) granted access to 💬 Sovereign Command.")

# Test 4: Tier Command user ($39.99) accessing Master Cockpit ($299) (MUST BE BLOCKED)
allowed, req, _ = check_module_access(TIER_COMMAND, "🎛️ Master C2 Cockpit")
assert not allowed and "299" in req, f"FAILED: Tier Command should be blocked from Cockpit, got req={req}"
print(f"[+] VERIFIED: Tier 1.5 subscriber blocked from 🎛️ Master C2 Cockpit -> Requires: {req}")

# Compile both console and tier manager
py_compile.compile(str(cockpit_dir / "ebony_tier_manager.py"), doraise=True)
py_compile.compile(str(cockpit_dir / "ebony_console_GREEN.py"), doraise=True)
print("\n[SUCCESS] ebony_tier_manager.py and console compiled with ZERO errors (Exit Code 0)!")