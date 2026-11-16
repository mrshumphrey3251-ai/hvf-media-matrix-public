"""
HVF Sovereign WORM-Protected SHA-256 Merkle Ingestion Bridge (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)
Extensible, thread-safe cryptographic ledger bridge that seals every authenticated
telemetry ingestion event into an append-only, WORM-enforced SQLite Merkle chain.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
import threading
from typing import Any, Dict, Optional

_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_LEDGER_DB = _ROOT / "matrix_ledger.db"
_GENESIS_SEED = "HVF-1AHA8-EBONY-SOVEREIGN-MERKLE-GENESIS-2026"
_DB_LOCK = threading.RLock()


class SovereignMerkleLedger:
    """Thread-safe, WORM-enforced sequential SHA-256 Merkle chain backed by SQLite WAL."""

    def __init__(self, db_path: Optional[Path] = None) -> None:
        self.db_path = Path(db_path) if db_path else _DEFAULT_LEDGER_DB
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA busy_timeout = 30000;")
        return conn

    def _init_schema(self) -> None:
        with _DB_LOCK:
            conn = self._connect()
            try:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS sovereign_merkle_ingest_ledger (
                        block_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp_utc TEXT NOT NULL,
                        source_node TEXT NOT NULL,
                        payload_sha256 TEXT NOT NULL,
                        prev_hash TEXT NOT NULL,
                        block_hash TEXT NOT NULL UNIQUE,
                        payload_bytes INTEGER NOT NULL
                    );
                    """
                )
                conn.execute(
                    """
                    CREATE TRIGGER IF NOT EXISTS trg_merkle_worm_no_update
                    BEFORE UPDATE ON sovereign_merkle_ingest_ledger
                    BEGIN
                        SELECT RAISE(ABORT, 'WORM VIOLATION: UPDATE prohibited on sovereign_merkle_ingest_ledger');
                    END;
                    """
                )
                conn.execute(
                    """
                    CREATE TRIGGER IF NOT EXISTS trg_merkle_worm_no_delete
                    BEFORE DELETE ON sovereign_merkle_ingest_ledger
                    BEGIN
                        SELECT RAISE(ABORT, 'WORM VIOLATION: DELETE prohibited on sovereign_merkle_ingest_ledger');
                    END;
                    """
                )
                conn.commit()
            finally:
                conn.close()

    def seal_payload(self, payload: Any, source_node: str = "API_PORT_3000") -> Dict[str, Any]:
        """Seal an authenticated telemetry payload into the next sequential SHA-256 Merkle block."""
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
        raw_bytes = canonical.encode("utf-8")
        payload_hash = hashlib.sha256(raw_bytes).hexdigest()
        ts_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        with _DB_LOCK:
            conn = self._connect()
            try:
                row = conn.execute(
                    "SELECT block_id, block_hash FROM sovereign_merkle_ingest_ledger ORDER BY block_id DESC LIMIT 1;"
                ).fetchone()
                if row is None:
                    next_id = 1
                    prev_hash = hashlib.sha256(_GENESIS_SEED.encode("utf-8")).hexdigest()
                else:
                    next_id = int(row[0]) + 1
                    prev_hash = str(row[1])

                block_material = f"{next_id}|{ts_utc}|{source_node}|{payload_hash}|{prev_hash}".encode("utf-8")
                block_hash = hashlib.sha256(block_material).hexdigest()

                conn.execute(
                    """
                    INSERT INTO sovereign_merkle_ingest_ledger
                    (block_id, timestamp_utc, source_node, payload_sha256, prev_hash, block_hash, payload_bytes)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                    """,
                    (next_id, ts_utc, source_node, payload_hash, prev_hash, block_hash, len(raw_bytes)),
                )
                conn.commit()
                return {
                    "block_id": next_id,
                    "timestamp_utc": ts_utc,
                    "source_node": source_node,
                    "payload_sha256": payload_hash,
                    "prev_hash": prev_hash,
                    "block_hash": block_hash,
                }
            finally:
                conn.close()

    def audit_chain(self) -> Dict[str, Any]:
        """Verify mathematical SHA-256 hash continuity across every block in the ledger."""
        with _DB_LOCK:
            conn = self._connect()
            try:
                rows = conn.execute(
                    """
                    SELECT block_id, timestamp_utc, source_node, payload_sha256, prev_hash, block_hash
                    FROM sovereign_merkle_ingest_ledger
                    ORDER BY block_id ASC;
                    """
                ).fetchall()
            finally:
                conn.close()

        expected_prev = hashlib.sha256(_GENESIS_SEED.encode("utf-8")).hexdigest()
        for block_id, ts_utc, source_node, payload_hash, prev_hash, block_hash in rows:
            if prev_hash != expected_prev:
                return {"valid": False, "broken_at_block": block_id, "chain_height": len(rows)}
            recomputed = hashlib.sha256(
                f"{block_id}|{ts_utc}|{source_node}|{payload_hash}|{prev_hash}".encode("utf-8")
            ).hexdigest()
            if recomputed != block_hash:
                return {"valid": False, "broken_at_block": block_id, "chain_height": len(rows)}
            expected_prev = block_hash

        return {
            "valid": True,
            "chain_height": len(rows),
            "merkle_head": expected_prev,
        }