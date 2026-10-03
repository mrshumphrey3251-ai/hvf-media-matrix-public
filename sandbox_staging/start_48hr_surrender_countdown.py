import os
import sqlite3
from datetime import datetime, timezone, timedelta

DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\hvf_memory_vault.db"

# Hard deadline: Exactly 48 hours post-severance
execution_time = datetime(2026, 9, 22, 12, 0, 0)
deadline_time = execution_time + timedelta(hours=48)

conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)
conn.execute("""
    CREATE TABLE IF NOT EXISTS legal_surrender_tracker (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subcontractor TEXT NOT NULL,
        severance_timestamp TEXT NOT NULL,
        surrender_deadline TEXT NOT NULL,
        status TEXT NOT NULL,
        artifacts_received INTEGER DEFAULT 0,
        notes TEXT
    )
""")

conn.execute("""
    INSERT INTO legal_surrender_tracker (subcontractor, severance_timestamp, surrender_deadline, status, notes)
    VALUES (?, ?, ?, ?, ?)
""", (
    "Drew Phillips / SignalLink Protocol LLC",
    execution_time.isoformat(),
    deadline_time.isoformat(),
    "COUNTDOWN_ACTIVE",
    "Section 9.3 Demand: 48-hour key surrender, configuration artifacts, and work product return."
))

conn.execute("""
    INSERT INTO corporate_governance_log (authority, target_entity, action, details, timestamp, status)
    VALUES (?, ?, ?, ?, ?, ?)
""", (
    "Jeffery Humphrey, CEO",
    "Drew Phillips / SignalLink Protocol LLC",
    "SECTION_9_3_COUNTDOWN_ARMED",
    f"48-hour surrender window initiated. Expiration: {deadline_time.isoformat()} CDT.",
    datetime.now().isoformat(),
    "SURRENDER_WINDOW_OPEN"
))
conn.close()

print(f"[SUCCESS] 48-Hour Section 9.3 Surrender Window logged in hvf_memory_vault.db")
print(f"  Severance Executed : {execution_time.strftime('%Y-%m-%d %H:%M:%S')} CDT")
print(f"  Surrender Deadline : {deadline_time.strftime('%Y-%m-%d %H:%M:%S')} CDT")
print(f"  Surveillance State : RADIO SILENCE / MONITORING INBOX")
