"""
================================================================================
HVF SOVEREIGN MEDIA MATRIX - STRATEGIC MEMORY VAULT (SQLITE)
Purpose: Long-Term Context Retention & Directive Storage for Ebony Core
================================================================================
"""

import sqlite3
import os
import json
from datetime import datetime

DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\hvf_memory_vault.db"

def init_vault():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ceo_directives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            category TEXT NOT NULL,
            directive TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS conversation_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def log_directive(category: str, directive: str, status: str = "ACTIVE"):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO ceo_directives (timestamp, category, directive, status) VALUES (?, ?, ?, ?)",
        (datetime.utcnow().isoformat(), category, directive, status)
    )
    conn.commit()
    conn.close()

def get_active_directives() -> list:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT timestamp, category, directive FROM ceo_directives WHERE status='ACTIVE' ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_vault()
    log_directive("FOUNDATION", "CEO: Mr. Humphrey. Organization: Humphrey Virtual Farm (HVF). Core Mandate: Sovereign AI Execution.", "ACTIVE")
    print("[HVF VAULT]: SQLite Strategic Memory Vault Initialized Successfully.")