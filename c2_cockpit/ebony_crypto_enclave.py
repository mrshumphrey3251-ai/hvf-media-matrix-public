import os
import sys
import hmac
import hashlib
import json
from pathlib import Path

SIGNING_SALT = b"HUMPHREY_VIRTUAL_FARMS_SOVEREIGN_ROOT_1AHA8_OK_TITLE_61"

def compute_license_signature(license_data: dict) -> str:
    """Generates an authoritative HMAC-SHA256 signature across all license parameters."""
    payload = f"{license_data.get('licensed_to')}|{license_data.get('tier')}|{license_data.get('max_nodes')}|{license_data.get('expires_at')}|{license_data.get('cage_code', '1AHA8')}"
    return hmac.new(SIGNING_SALT, payload.encode("utf-8"), hashlib.sha256).hexdigest()

def verify_license_integrity(license_data: dict) -> bool:
    """Returns True only if the license file matches its cryptographic HMAC signature exactly."""
    stored_sig = license_data.get("integrity_signature", "")
    if not stored_sig:
        return False
    expected_sig = compute_license_signature(license_data)
    return hmac.compare_digest(stored_sig, expected_sig)

def execute_zeroize_protocol(enclave_path: Path, reason: str = "CRYPTOGRAPHIC_TAMPER_DETECTED"):
    """
    SOVEREIGN ZEROIZATION PROTOCOL (SELF-DESTRUCT)
    Securely shreds active cryptographic licenses, purges local credentials,
    drops a permanent hardware quarantine lock, and aborts execution immediately.
    """
    print(f"\n[CRITICAL ZEROIZE] TAMPER DETECTED: {reason}")
    print("[CRITICAL ZEROIZE] Executing multi-pass cryptographic zeroization...")
    
    # Target files to shred
    targets = [
        enclave_path / "ebony_license.json",
        enclave_path / "stripe_config.json"
    ]
    
    for t in targets:
        if t.exists():
            try:
                # Multi-pass secure overwrite (0xFF -> 0x00)
                file_size = t.stat().st_size
                with open(t, "wb") as f:
                    f.write(b"\xFF" * file_size)
                    f.flush()
                    f.seek(0)
                    f.write(b"\x00" * file_size)
                    f.flush()
                t.unlink()
                print(f"[ZEROIZED] Shredded and unlinked: {t.name}")
            except Exception as e:
                print(f"[!] Zeroize warning on {t.name}: {e}")
                
    # Place permanent tamper quarantine marker
    tamper_flag = enclave_path.parent / ".tamper_lockout"
    try:
        tamper_flag.write_text(f"NODE_COMPROMISED_ZEROIZE_EXECUTED:{reason}", encoding="utf-8")
        print(f"[QUARANTINE] Permanent tamper lockout written to: {tamper_flag.name}")
    except Exception:
        pass

def verify_and_enforce_node_security(enclave_path: Path) -> bool:
    """Verifies runtime integrity; triggers zeroize self-destruct if tampered."""
    tamper_flag = enclave_path.parent / ".tamper_lockout"
    if tamper_flag.exists():
        print("[HALT] Node is quarantined under permanent tamper lockout.")
        return False

    lic_file = enclave_path / "ebony_license.json"
    if not lic_file.exists():
        return False

    try:
        lic_data = json.loads(lic_file.read_text(encoding="utf-8"))
        if not verify_license_integrity(lic_data):
            execute_zeroize_protocol(enclave_path, "LICENSE_SIGNATURE_TAMPER")
            return False
        return True
    except Exception as e:
        execute_zeroize_protocol(enclave_path, f"JSON_CORRUPT_OR_TAMPERED:{e}")
        return False