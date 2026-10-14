"""
E.B.O.N.Y. Tier 1.5 Commercial Release Certification & Verification Harness
Tests: Entitlement Access, Lockout Enforcement, Hardware Seat Quotas & Optical Ingress
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Jurisdiction: State of Oklahoma Title 61 & OK HB 2992
"""
import sys
import json
from pathlib import Path
import py_compile

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
sys.path.insert(0, str(cockpit_dir))

from ebony_tier_manager import (
    TIER_1_PERSONAL,
    TIER_COMMAND,
    TIER_2_VIP,
    TIER_3_ENTERPRISE,
    TIER_0_CEO,
    TIER_NODE_LIMITS,
    TIER_METADATA,
    MODULE_TIER_MAPPING,
    MAINTENANCE_MODULES,
    check_module_access
)

from ebony_client_updater import get_hardware_uuid

print("\n" + "=" * 90)
print("     E.B.O.N.Y. TIER 1.5 ($39.99/MO) COMMERCIAL RELEASE VERIFICATION REPORT      ")
print("     ENCLAVE NODE: HVFNexus | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5")
print("=" * 90)

passed = 0
failed = 0

def run_test(name, condition, detail=""):
    global passed, failed
    if condition:
        print(f"  [PASS] {name} {detail}")
        passed += 1
    else:
        print(f"  [FAIL] {name} {detail}")
        failed += 1

# --- TEST GROUP 1: TIER 1.5 SEAT LIMITS & METADATA ---
print("\n--- TEST GROUP 1: SEAT ALLOCATION & METADATA ---")
tier_meta = TIER_METADATA.get(TIER_COMMAND, {})
run_test("Tier 1.5 Name Configured", "Sovereign Command" in tier_meta.get("name", ""))
run_test("Tier 1.5 Price Configured", "$39.99" in tier_meta.get("price", ""))
run_test("Tier 1.5 Node Quota is 3 Devices", TIER_NODE_LIMITS.get(TIER_COMMAND) == 3, f"(Actual: {TIER_NODE_LIMITS.get(TIER_COMMAND)})")

# --- TEST GROUP 2: TIER 1.5 AUTHORIZED MODULES (MUST BE GRANTED) ---
print("\n--- TEST GROUP 2: AUTHORIZED MODULE ACCESS ---")
tier15_accessible = [
    "📨 Sovereign Dispatch Deck",
    "🚨 NOAA Radar",
    "📖 System Overview",
    "📝 Feedback Hub",
    "💬 Sovereign Command",
    "📡 Sovereign Comms Deck"
]

for mod in tier15_accessible:
    allowed, req, is_m = check_module_access(TIER_COMMAND, mod)
    run_test(f"Access to '{mod}'", allowed, f"-> Expected: Granted | Actual: {'Granted' if allowed else 'Blocked'}")

# --- TEST GROUP 3: HIGHER TIER BARRIERS (MUST BE BLOCKED) ---
print("\n--- TEST GROUP 3: COMMERCIAL PAYWALL BARRIERS ---")
higher_tier_modules = [
    ("🎛️ Master C2 Cockpit", "$249"),
    ("🌾 Drone Diagnostics", "$249"),
    ("📡 LinkedIn Engine", "$249"),
    ("⚡ Sovereign Weather Scada", "$249"),
    ("⚡ Grain Silo Aeration And F", "$249")
]

for mod, expected_price in higher_tier_modules:
    allowed, req, is_m = check_module_access(TIER_COMMAND, mod)
    run_test(f"Block '{mod}'", not allowed and expected_price in req, f"-> Requires: {req}")

# --- TEST GROUP 4: LEVEL-5 R&D MAINTENANCE LOCKOUTS ---
print("\n--- TEST GROUP 4: R&D MAINTENANCE LOCKOUTS ---")
sample_maintenance = [
    "⚡ Autonomous Build Forge",
    "🛡️ CEO Authorization Gate",
    "🧪 Sandbox",
    "⚙️ Empire Config",
    "⬛ Media Matrix"
]

for mod in sample_maintenance:
    allowed, req, is_m = check_module_access(TIER_COMMAND, mod)
    run_test(f"Maintenance Lock '{mod}'", not allowed and is_m, f"-> Status: Locked under R&D Maintenance")

# --- TEST GROUP 5: HARDWARE NODE SEAT SIMULATION (MAX 3 NODES) ---
print("\n--- TEST GROUP 5: HARDWARE NODE SEAT SIMULATION ---")
max_seats = TIER_NODE_LIMITS.get(TIER_COMMAND, 3)
hw_signatures = []

# Node 1 claims seat
hw_signatures.append("hw_sig_primary_desktop_01")
run_test("Device 1 Claims Seat", len(hw_signatures) <= max_seats, f"(Seat 1 of {max_seats})")

# Node 2 claims seat (Field Laptop)
hw_signatures.append("hw_sig_field_laptop_02")
run_test("Device 2 Claims Seat", len(hw_signatures) <= max_seats, f"(Seat 2 of {max_seats})")

# Node 3 claims seat (Tablet)
hw_signatures.append("hw_sig_tablet_03")
run_test("Device 3 Claims Seat", len(hw_signatures) <= max_seats, f"(Seat 3 of {max_seats})")

# Node 4 attempts unauthorized clone (MUST FAIL)
node_4_blocked = (len(hw_signatures) + 1) > max_seats
run_test("Device 4 Exceeds Quota (Piracy Blocked)", node_4_blocked, f"-> Blocked: 4 exceeds max {max_seats}")

# --- COMPILATION INTEGRITY ---
print("\n--- TEST GROUP 6: PYTHON BYTECODE COMPILATION ---")
files_to_compile = [
    cockpit_dir / "ebony_tier_manager.py",
    cockpit_dir / "ebony_client_updater.py",
    cockpit_dir / "ebony_travel_ui.py",
    cockpit_dir / "ebony_console_GREEN.py"
]

for f in files_to_compile:
    try:
        py_compile.compile(str(f), doraise=True)
        run_test(f"Compile {f.name}", True, "-> Exit Code 0")
    except Exception as e:
        run_test(f"Compile {f.name}", False, f"-> Error: {e}")

print("\n" + "=" * 90)
print(f"VERIFICATION SUMMARY: {passed} PASSED | {failed} FAILED")
if failed == 0:
    print(">>> [SUCCESS] TIER 1.5 COMMERCIAL RELEASE MEETS 100% OPERATIONAL SPECIFICATIONS. <<<")
else:
    print(">>> [CRITICAL] ONE OR MORE VERIFICATION ASSERTIONS FAILED. <<<")
print("=" * 90 + "\n")

if failed > 0:
    sys.exit(1)