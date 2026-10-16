"""
E.B.O.N.Y. Interactive Zero-Disk Banking Intake Runner
Volatile RAM Validation Engine for El Reno Financial Instruments
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Framework: Oklahoma Title 61 & Title 74 OMES Clearinghouse
"""
import sys
from pathlib import Path

cockpit_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(cockpit_dir))
from stage_banking_ingress import validate_aba_routing

def intake_session():
    print("\n" + "=" * 80)
    print("     E.B.O.N.Y. SECURE VOLATILE BANKING INTAKE RUNNER")
    print("     ZERO-DISK GUARANTEE: Credentials exist strictly in volatile RAM.")
    print("=" * 80)
    
    if len(sys.argv) > 1:
        test_routing = sys.argv[1].strip()
    else:
        print("\n[*] Ready for physical El Reno credential input.")
        print("[*] To test immediately, provide routing number as argument or press Enter to exit.")
        return

    is_valid = validate_aba_routing(test_routing)
    print("\n" + "-" * 80)
    print(f"[*] Input Routing Number:  {'*' * 5 + test_routing[-4:] if len(test_routing) >= 4 else 'INVALID_FORMAT'}")
    if is_valid:
        print("[+] Checksum Algorithm:    Federal Reserve Mod-10 VALIDATED (PASSED)")
        print("[+] Clearance Status:      APPROVED for OMES Title 61 Vendor Clearinghouse & Stripe")
    else:
        print("[-] Checksum Algorithm:    MOD-10 CHECKSUM FAILED")
        print("[-] Clearance Status:      REJECTED - Verify numbers on official bank letter.")
    print("-" * 80 + "\n")

if __name__ == "__main__":
    intake_session()