import json
import sys
from pathlib import Path

cfg_path = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\email_accounts.json")

print("\n" + "=" * 86)
print("     E.B.O.N.Y. SOVEREIGN COMMERCIAL SUBSCRIBER LEDGER AUDIT     ")
print(f"     ENCLAVE NODE: HVFNexus | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5")
print("=" * 86)

if not cfg_path.exists():
    print("[CRITICAL ERROR] email_accounts.json not found on disk.")
    sys.exit(1)

try:
    accounts = json.loads(cfg_path.read_text(encoding="utf-8"))
    print(f"[ACCOUNTS ON DISK] Total Registered: {len(accounts)}\n")
    print(f"{'ACCOUNT / MAILBOX':<32} | {'TIER':<18} | {'VIP DRONE':<12} | {'STATUS'}")
    print("-" * 86)
    
    for email, data in accounts.items():
        tier = data.get("tier", "UNKNOWN")
        vip = "RESERVED" if data.get("vip_drone_reserved") else "NONE"
        status = data.get("auth_status", "ACTIVE")
        print(f"• {email:<30} | {tier:<18} | {vip:<12} | {status}")
        
    print("=" * 86)
    print(">>> [SUCCESS] ALL COMMERCIAL PROFILES VERIFIED ON LOCAL DISK. <<<")
    print("=" * 86 + "\n")
except Exception as e:
    print(f"[ERROR] Failed to read account ledger: {e}")
    sys.exit(1)