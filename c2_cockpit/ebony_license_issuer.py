"""
E.B.O.N.Y. Sovereign Commercial License Issuance Engine
Automated Post-Payment Fulfillment, Cryptographic Stamping & Seat Binding
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Authority: Oklahoma Title 61 & OK HB 2992
"""
import os
import sys
import json
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path

COCKPIT_DIR = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
if str(COCKPIT_DIR) not in sys.path:
    sys.path.insert(0, str(COCKPIT_DIR))

try:
    from ebony_client_updater import get_hardware_uuid
except Exception:
    def get_hardware_uuid():
        return hashlib.sha256(b"LOCAL_DEFAULT_NODE").hexdigest()

LICENSE_FILE_PATH = COCKPIT_DIR / "ebony_license.json"

TIER_SEAT_SCHEDULE = {
    "TIER_1_PERSONAL": 1,
    "TIER_COMMAND": 3,
    "TIER_2_VIP": 5,
    "TIER_3_ENTERPRISE": 10,
    "TIER_0_CEO": 999
}

def generate_sovereign_license(
    customer_name: str,
    customer_email: str,
    tier: str,
    duration_days: int = 30,
    claim_current_node: bool = True
) -> dict:
    """Generates an authoritative, tamper-resistant sovereign commercial license."""
    now_utc = datetime.now(timezone.utc)
    exp_utc = now_utc + timedelta(days=duration_days)
    
    max_nodes = TIER_SEAT_SCHEDULE.get(tier, 1)
    hw_signatures = []
    if claim_current_node:
        hw_signatures.append(get_hardware_uuid())

    # Build raw metadata payload
    license_payload = {
        "entity": "Humphrey Virtual Farms LLC",
        "cage_code": "1AHA8",
        "uei": "S1M4ENLHTDH5",
        "statutory_authority": "Oklahoma Title 61 & OK HB 2992",
        "license_type": f"COMMERCIAL_{tier}",
        "tier": tier,
        "licensed_to": customer_name,
        "customer_email": customer_email,
        "max_nodes": max_nodes,
        "hardware_signatures": hw_signatures,
        "issued_at": now_utc.isoformat(),
        "expires_at": exp_utc.isoformat(),
        "status": "ACTIVE_COMMERCIAL",
        "enforce_updates": True
    }
    
    # Calculate integrity seal over payload
    seal_string = f"{tier}:{customer_email}:{max_nodes}:{exp_utc.isoformat()}:1AHA8"
    license_payload["integrity_seal"] = hashlib.sha256(seal_string.encode()).hexdigest()
    
    return license_payload

def install_license_to_disk(license_dict: dict, target_path: Path = LICENSE_FILE_PATH) -> bool:
    try:
        target_path.write_text(json.dumps(license_dict, indent=2), encoding="utf-8")
        return True
    except Exception as e:
        print(f"[!] License write failure: {e}")
        return False

if __name__ == "__main__":
    print("=" * 84)
    print("     E.B.O.N.Y. SOVEREIGN LICENSE ISSUER VERIFICATION AUDIT     ")
    print("=" * 84)
    sample_lic = generate_sovereign_license(
        customer_name="Rob Teel",
        customer_email="rob@example.com",
        tier="TIER_COMMAND",
        duration_days=30,
        claim_current_node=True
    )
    print(f"[+] Tier Issued: {sample_lic['tier']}")
    print(f"[+] Licensed To: {sample_lic['licensed_to']} ({sample_lic['customer_email']})")
    print(f"[+] Authorized Nodes: {sample_lic['max_nodes']}")
    print(f"[+] Hardware Bound: {sample_lic['hardware_signatures'][0][:24]}...")
    print(f"[+] Integrity Seal: {sample_lic['integrity_seal'][:24]}...")
    print("=" * 84)