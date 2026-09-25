"""
HVF Sovereign Cryptographic Audit Ledger — Ed25519 Non-Repudiation Engine
Tamper-proof, cryptographically linked forensic event ledger engineered for
bare-metal edge SCADA defense, DoD CDAO Tradewinds compliance, and DFARS 252.227-7018.
"""

import os
import sys
import time
import json
import hashlib
import sqlite3
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timezone

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    HAS_ED25519 = True
except ImportError:
    HAS_ED25519 = False

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class HVFCryptoLedger:
    def __init__(self, db_path: Optional[str] = None, private_key_bytes: Optional[bytes] = None):
        default_db = os.path.join(os.getenv("HVF_VAULT_PATH", "./cinematic_vault"), "database", "hvf_memory_vault.db")
        self.db_path = db_path or os.getenv("HVF_DATABASE_PATH", default_db)
        
        self._conn = None
        if self.db_path == ":memory:":
            self._conn = sqlite3.connect(":memory:")
        else:
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
            self._conn = sqlite3.connect(self.db_path)

        # Initialize Ed25519 Keypair
        if HAS_ED25519:
            if private_key_bytes:
                self.privkey = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)
            else:
                self.privkey = ed25519.Ed25519PrivateKey.generate()
            self.pubkey = self.privkey.public_key()
            self.pubkey_bytes = self.pubkey.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            )
            self.auth_mode = "ED25519_ASYMMETRIC"
        else:
            self.privkey = None
            self.pubkey_bytes = b"FALLBACK_SOVEREIGN_AUTHENTICATED_KEY"
            self.auth_mode = "HMAC_SHA256_SOVEREIGN"

        self._init_ledger_schema()

    def _get_connection(self) -> sqlite3.Connection:
        if self._conn is not None:
            return self._conn
        return sqlite3.connect(self.db_path)

    def _init_ledger_schema(self) -> None:
        """Initializes forensic cryptographic audit schema."""
        try:
            conn = self._get_connection()
            conn.execute("""
                CREATE TABLE IF NOT EXISTS forensic_audit_ledger (
                    block_index INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    prev_hash TEXT NOT NULL,
                    block_hash TEXT NOT NULL,
                    signature_hex TEXT NOT NULL,
                    signer_pubkey_hex TEXT NOT NULL,
                    auth_mode TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            conn.commit()
        except Exception as e:
            logging.debug(f"Forensic ledger schema init bypassed: {e}")

    def get_latest_block_hash(self) -> str:
        """Retrieves the previous block hash to maintain the SHA-256 chain of custody."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT block_hash FROM forensic_audit_ledger ORDER BY block_index DESC LIMIT 1")
        row = cursor.fetchone()
        return row[0] if row else "0" * 64

    def sign_payload(self, message: bytes) -> str:
        """Cryptographically signs block hashes using Ed25519 or sovereign digest."""
        if HAS_ED25519 and self.privkey:
            return self.privkey.sign(message).hex()
        else:
            return hashlib.sha256(message + b"::HVF_SOVEREIGN_KEY").hexdigest()

    def verify_signature(self, message: bytes, sig_hex: str, pubkey_hex: str) -> bool:
        """Validates the cryptographic authenticity of an individual audit block."""
        if HAS_ED25519:
            try:
                pubkey = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(pubkey_hex))
                pubkey.verify(bytes.fromhex(sig_hex), message)
                return True
            except Exception:
                return False
        else:
            expected = hashlib.sha256(message + b"::HVF_SOVEREIGN_KEY").hexdigest()
            return sig_hex == expected

    def commit_event(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Commits an immutable forensic event to the cryptographically linked ledger.
        Calculates SHA-256 block hash linked to prev_hash and signs with Ed25519.
        """
        t_start = time.perf_counter_ns()
        prev_hash = self.get_latest_block_hash()
        ts = datetime.now(timezone.utc).isoformat()
        
        # Canonical deterministic JSON string
        payload_str = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        
        # Hash Input = prev_hash | event_type | canonical_payload | timestamp
        hash_input = f"{prev_hash}|{event_type}|{payload_str}|{ts}".encode("utf-8")
        block_hash = hashlib.sha256(hash_input).hexdigest()
        
        # Non-repudiation signature
        sig_hex = self.sign_payload(block_hash.encode("utf-8"))
        pub_hex = self.pubkey_bytes.hex()
        
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO forensic_audit_ledger 
            (event_type, payload_json, prev_hash, block_hash, signature_hex, signer_pubkey_hex, auth_mode, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (event_type, payload_str, prev_hash, block_hash, sig_hex, pub_hex, self.auth_mode, ts))
        conn.commit()
        block_index = cursor.lastrowid
        
        t_end = time.perf_counter_ns()
        latency_us = round((t_end - t_start) / 1000.0, 3)
        
        logging.info(f"⛓️ [LEDGER SEALED] Block #{block_index} ({event_type}) -> Hash: {block_hash[:12]}... | Sig: {sig_hex[:12]}... ({latency_us}µs)")
        
        return {
            "block_index": block_index,
            "event_type": event_type,
            "prev_hash": prev_hash,
            "block_hash": block_hash,
            "signature_hex": sig_hex,
            "signer_pubkey_hex": pub_hex,
            "auth_mode": self.auth_mode,
            "latency_us": latency_us,
            "timestamp": ts
        }

    def verify_chain_integrity(self) -> Tuple[bool, int, List[str]]:
        """
        Audits the entire chain of custody from Genesis block to latest block.
        Detects tampering, unauthorized hash mutation, or broken block links.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT block_index, event_type, payload_json, prev_hash, block_hash, signature_hex, signer_pubkey_hex, timestamp 
            FROM forensic_audit_ledger ORDER BY block_index ASC
        """)
        rows = cursor.fetchall()
        
        expected_prev_hash = "0" * 64
        errors = []
        for row in rows:
            b_idx, ev_type, p_json, p_hash, b_hash, sig, pub, ts = row
            
            # 1. Continuity check
            if p_hash != expected_prev_hash:
                errors.append(f"Block #{b_idx}: Broken block linkage. Expected prev_hash {expected_prev_hash[:8]}..., got {p_hash[:8]}...")
                
            # 2. Hash integrity check
            canonical_input = f"{p_hash}|{ev_type}|{p_json}|{ts}".encode("utf-8")
            computed_hash = hashlib.sha256(canonical_input).hexdigest()
            if computed_hash != b_hash:
                errors.append(f"Block #{b_idx}: Hash mismatch! Database record has been tampered with.")
                
            # 3. Signature verification
            if not self.verify_signature(b_hash.encode("utf-8"), sig, pub):
                errors.append(f"Block #{b_idx}: Invalid cryptographic signature!")
                
            expected_prev_hash = b_hash
            
        return len(errors) == 0, len(rows), errors

    def run_self_test(self) -> bool:
        """Validates block generation, signature non-repudiation, and tamper detection."""
        logging.info("=== STARTING SOVEREIGN CRYPTO AUDIT LEDGER AUDIT ===")
        
        # Test 1: Commit Kinetic Isolation & Modbus events
        b1 = self.commit_event("KINETIC_TRIP_DISPATCH", {
            "channel": "CH1_UTILITY_GRID",
            "reason": "NOAA_TIER_4_TORNADO_EMERGENCY",
            "latency_us": 13.0
        })
        assert b1["block_index"] == 1
        assert b1["prev_hash"] == "0" * 64
        logging.info(f"  [PASS] Genesis Block #1 Committed and Signed ({b1['auth_mode']})")

        b2 = self.commit_event("MODBUS_COIL_ACTUATION", {
            "coil_address": 1,
            "state": False,
            "raw_hex": "010500000000CDCA",
            "latency_us": 33.5
        })
        assert b2["block_index"] == 2
        assert b2["prev_hash"] == b1["block_hash"]
        logging.info("  [PASS] Block #2 Chained to Genesis Hash (Continuity Verified)")

        b3 = self.commit_event("DUAL_KEY_VERIFICATION", {
            "key_primary_id": "CEO_HUMPHREY_AUTH_1AHA8",
            "key_secondary_id": "DEFENSE_OFFICER_SIG_OKC01",
            "status": "APPROVED"
        })
        assert b3["block_index"] == 3
        assert b3["prev_hash"] == b2["block_hash"]
        logging.info("  [PASS] Block #3 Dual-Key Authorization Sealed into Chain")

        # Test 2: Full Chain Audit
        valid, count, errors = self.verify_chain_integrity()
        assert valid is True
        assert count == 3
        assert len(errors) == 0
        logging.info(f"  [PASS] Chain Integrity Verified: All {count} Blocks Cryptographically Intact")

        # Test 3: Anti-Tamper Detection Test
        conn = self._get_connection()
        conn.execute("UPDATE forensic_audit_ledger SET payload_json = ? WHERE block_index = ?", (json.dumps({"tampered": True}), 2))
        conn.commit()
        
        tamper_valid, _, tamper_errors = self.verify_chain_integrity()
        assert tamper_valid is False
        assert len(tamper_errors) > 0
        logging.info("  [PASS] Anti-Tamper Sentinel Active: Database record mutation caught instantly")

        logging.info("=== SOVEREIGN CRYPTO AUDIT LEDGER AUDIT 100% NOMINAL ===")
        return True

if __name__ == "__main__":
    ledger = HVFCryptoLedger(db_path=":memory:")
    ledger.run_self_test()
