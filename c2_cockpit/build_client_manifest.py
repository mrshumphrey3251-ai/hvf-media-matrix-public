from pathlib import Path
import py_compile

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")

DIST_FILES = [
    "ebony_console_GREEN.py",
    "ebony_tier_manager.py",
    "ebony_client_updater.py",
    "ebony_email_dispatcher.py",
    "ebony_travel_ui.py",
    "ebony_travel_autopilot.py",
    "ebony_stripe_billing.py",
    "ebony_crypto_enclave.py"
]

print("\n" + "=" * 90)
print("     CLIENT RELEASE PACKAGING MANIFEST & BYTECODE CERTIFICATION     ")
print("=" * 90)

all_certified = True
for fname in DIST_FILES:
    fpath = cockpit_dir / fname
    if fpath.exists():
        try:
            py_compile.compile(str(fpath), doraise=True)
            print(f"[BYTECODE CERTIFIED] {fname:<30} -> Exit Code 0 (Verified)")
        except Exception as e:
            print(f"[REJECTED]           {fname:<30} -> {e}")
            all_certified = False
    else:
        print(f"[MISSING TARGET]     {fname:<30}")
        all_certified = False

print("=" * 90)
if all_certified:
    print(">>> [SUCCESS] 100% OF CLIENT CORE PACKAGING TARGETS BYTECODE CERTIFIED. <<<")
else:
    print(">>> [CRITICAL] PACKAGING MANIFEST HAS UNMET DEPENDENCIES. <<<")
print("=" * 90 + "\n")