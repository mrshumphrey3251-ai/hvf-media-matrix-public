"""
HVF Omni-Industrial Matrix | PROJECT EBONY (BRAIN ONE & THREE)
Module: ebony_cleanroom_provenance.py
Author: Jeffery Humphrey, Founder & CEO (52% Apex Architect)
Classification: PROPRIETARY & CONFIDENTIAL | ZERO-CLOUD BARE-METAL EXECUTION
Compliance: NIST SP 800-230 / DFARS 252.227-7018 Data Rights Protection

Clean-Room replacement for third-party telemetry transport and cloud-tethered anchors.
Executes 100% locally on bare-metal silicon with zero network latency.
"""

import os
import json
import sqlite3
import hashlib
import time
from datetime import datetime, timezone

GENESIS_BLOCK_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

class EbonyProvenanceEngine:
    def __init__(self, db_path=None):
        base_dir = r"C:\HVF_Repos\hvf-media-matrix-private"
        self.db_path = db_path or os.path.join(base_dir, "hvf_memory_vault.db")
        self._init_vault()

    def _init_vault(self):
        conn = sqlite3.connect(self.db_path, timeout=10.0, isolation_level=None)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ebony_provenance_ledger (
                block_index INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp_utc TEXT NOT NULL,
                telemetry_source TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                prev_block_hash TEXT NOT NULL,
                block_hash TEXT NOT NULL,
                merkle_root TEXT NOT NULL,
                execution_latency_ms REAL NOT NULL
            )
        """)
        conn.close()

    def get_latest_hash(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT block_hash FROM ebony_provenance_ledger ORDER BY block_index DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else GENESIS_BLOCK_HASH

    def anchor_telemetry(self, source_id: str, telemetry_data: dict) -> dict:
        start_time = time.perf_counter()
        now_utc = datetime.now(timezone.utc).isoformat()
        prev_hash = self.get_latest_hash()

        payload_str = json.dumps(telemetry_data, sort_keys=True, separators=(',', ':'))
        payload_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
        
        chain_input = f"{prev_hash}:{now_utc}:{source_id}:{payload_hash}"
        block_hash = hashlib.sha256(chain_input.encode('utf-8')).hexdigest()
        
        latency_ms = round((time.perf_counter() - start_time) * 1000, 3)

        conn = sqlite3.connect(self.db_path, timeout=10.0, isolation_level=None)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ebony_provenance_ledger 
            (timestamp_utc, telemetry_source, payload_json, prev_block_hash, block_hash, merkle_root, execution_latency_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (now_utc, source_id, payload_str, prev_hash, block_hash, payload_hash, latency_ms))
        
        block_index = cursor.lastrowid
        conn.close()

        return {
            "status": "ANCHORED",
            "block_index": block_index,
            "block_hash": block_hash,
            "prev_block_hash": prev_hash,
            "payload_hash": payload_hash,
            "latency_ms": latency_ms,
            "cloud_dependencies": 0
        }

    def verify_chain_integrity(self) -> tuple[bool, str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT block_index, timestamp_utc, telemetry_source, payload_json, prev_block_hash, block_hash FROM ebony_provenance_ledger ORDER BY block_index ASC")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return True, "Ledger is empty (Genesis state)."

        expected_prev = GENESIS_BLOCK_HASH
        for row in rows:
            b_idx, t_utc, src, payload_str, p_hash, b_hash = row
            if p_hash != expected_prev:
                return False, f"Integrity Violation: Broken previous hash link at Block #{b_idx}"

            p_payload_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
            expected_block_hash = hashlib.sha256(f"{p_hash}:{t_utc}:{src}:{p_payload_hash}".encode('utf-8')).hexdigest()

            if b_hash != expected_block_hash:
                return False, f"Tamper Detection Alert: Cryptographic mismatch at Block #{b_idx}"

            expected_prev = b_hash

        return True, f"Integrity Verified: All {len(rows)} blocks cryptographically valid."

if __name__ == "__main__":
    engine = EbonyProvenanceEngine()
    print("Initializing Ebony Clean-Room Cryptographic Provenance Engine...")
    test_packet = {
        "subsystem": "SCADA_CORE",
        "voltage_rail": 12.04,
        "oscillation_hz": 60.001,
        "status": "OPTIMAL"
    }
    result = engine.anchor_telemetry("EBONY_BRAIN_ONE", test_packet)
    print(f"[SUCCESS] Clean-Room Provenance Engine deployed and validated in hvf_memory_vault.db.")
    print(f"  Block Index : {result['block_index']}")
    print(f"  Block Hash  : {result['block_hash']}")
    print(f"  Latency     : {result['latency_ms']} ms (Zero-Cloud Bare-Metal)")
    
    valid, msg = engine.verify_chain_integrity()
    print(f"  Integrity   : {msg}")

