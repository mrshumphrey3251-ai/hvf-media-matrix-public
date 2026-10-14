import hmac
import hashlib
import json
from pathlib import Path

SIGNING_SALT = b"HUMPHREY_VIRTUAL_FARMS_SOVEREIGN_ROOT_1AHA8_OK_TITLE_61"

def compute_license_signature(license_data: dict) -> str:
    payload = f"{license_data.get('licensed_to')}|{license_data.get('tier')}|{license_data.get('max_nodes')}|{license_data.get('expires_at')}|{license_data.get('cage_code', '1AHA8')}"
    return hmac.new(SIGNING_SALT, payload.encode("utf-8"), hashlib.sha256).hexdigest()

def verify_license_integrity(license_data: dict) -> bool:
    stored_sig = license_data.get("integrity_signature", "")
    if not stored_sig:
        return False
    expected_sig = compute_license_signature(license_data)
    return hmac.compare_digest(stored_sig, expected_sig)

if __name__ == "__main__":
    test_lic = {
        "licensed_to": "Rob Teel",
        "tier": "TIER_1_PERSONAL",
        "max_nodes": 1,
        "expires_at": "2026-11-14T00:00:00Z",
        "cage_code": "1AHA8"
    }
    test_lic["integrity_signature"] = compute_license_signature(test_lic)
    assert verify_license_integrity(test_lic) == True, "Authentic license failed verification!"
    
    tampered_lic = test_lic.copy()
    tampered_lic["tier"] = "TIER_0_CEO"
    assert verify_license_integrity(tampered_lic) == False, "Tampered license was not rejected!"
    print("[SUCCESS] Cryptographic signature engine verified: Tampered licenses mathematically rejected!")