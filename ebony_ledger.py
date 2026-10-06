"""
HVF OMNI-INDUSTRIAL PERSISTENT AUDIT LEDGER
Project: Ebony Sovereign C2 Matrix
Compliance: CAGE 1AHA8 / UEI S1M4ENLHTDH5
Storage: Local SQLite Append-Only Deterministic Datastore
"""

import sqlite3
import datetime
import os

DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\matrix_ledger.db"

def init_ledger(db_path=DB_PATH):
    """Initializes the database schema if not present."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            model_core TEXT,
            latency_sec REAL DEFAULT 0.0
        )
    """)
    conn.commit()
    conn.close()

def record_entry(role, content, model_core="NONE", latency_sec=0.0, session_id="SOVEREIGN_ROOT", db_path=DB_PATH):
    """Appends an immutable audit event to the ledger."""
    try:
        init_ledger(db_path)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        cursor.execute("""
            INSERT INTO audit_ledger (timestamp, session_id, role, content, model_core, latency_sec)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (now, session_id, role, content, model_core, latency_sec))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[-] LEDGER WRITE ERROR: {str(e)}")
        return False

def get_recent_entries(limit=5, db_path=DB_PATH):
    """Retrieves the most recent records from the ledger."""
    try:
        init_ledger(db_path)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, timestamp, role, content, model_core, latency_sec FROM audit_ledger ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"[-] LEDGER READ ERROR: {str(e)}")
        return []
