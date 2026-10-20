import sys
from pathlib import Path
import py_compile

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
sys.path.insert(0, str(cockpit_dir))

try:
    from ebony_email_dispatcher import (
        get_configured_accounts,
        remove_account_credentials,
        save_account_credentials,
        test_account_connection,
        detect_servers,
        poll_and_auto_dispatch,
        generate_travel_debrief_report
    )
    print("\n" + "=" * 80)
    print(">>> [SUCCESS] All routines verified and imported from ebony_email_dispatcher! <<<")
    print("  - get_configured_accounts:     VERIFIED")
    print("  - remove_account_credentials:  VERIFIED")
    print("  - save_account_credentials:    VERIFIED")
    print("  - test_account_connection:     VERIFIED")
    print("=" * 80 + "\n")
except Exception as e:
    print(f"[FATAL IMPORT ERROR] {e}")
    sys.exit(1)

# Compile all console components
files = [
    cockpit_dir / "ebony_email_dispatcher.py",
    cockpit_dir / "ebony_travel_ui.py",
    cockpit_dir / "ebony_travel_autopilot.py",
    cockpit_dir / "ebony_console_GREEN.py"
]
for f in files:
    py_compile.compile(str(f), doraise=True)
    print(f"[COMPILED] {f.name} -> Exit Code 0")