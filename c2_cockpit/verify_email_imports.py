import sys
from pathlib import Path
cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
sys.path.insert(0, str(cockpit_dir))
try:
    from ebony_email_dispatcher import (
        save_account_credentials,
        test_account_connection,
        detect_servers,
        poll_and_auto_dispatch,
        get_on_demand_communications_report
    )
    print("\n" + "=" * 80)
    print(">>> [VERIFIED] All routines successfully imported from ebony_email_dispatcher. <<<")
    print("  - save_account_credentials: OK")
    print("  - test_account_connection:  OK (Direct TLS/SSL IMAP socket validator)")
    print("  - detect_servers:           OK")
    print("  - poll_and_auto_dispatch:   OK")
    print("  - get_report:               OK")
    print("=" * 80 + "\n")
except Exception as e:
    print(f"[CRITICAL IMPORT ERROR] {e}")
    sys.exit(1)
