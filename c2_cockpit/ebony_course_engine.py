import sqlite3
import hashlib
from datetime import datetime, timezone
from pathlib import Path

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
target_db = cockpit_dir / "matrix_ledger.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS student_course_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    full_name TEXT NOT NULL,
    course_code TEXT NOT NULL,
    course_title TEXT NOT NULL,
    hours_completed INTEGER NOT NULL,
    total_hours_required INTEGER NOT NULL,
    practicum_score_pct REAL NOT NULL,
    exam_score_pct REAL NOT NULL,
    certification_status TEXT NOT NULL,
    lead_evaluator TEXT NOT NULL,
    sha256_record_seal TEXT NOT NULL,
    timestamp_utc TEXT NOT NULL
);
"""

conn = sqlite3.connect(str(target_db))
cur = conn.cursor()
cur.executescript(SCHEMA_SQL)

courses = [
    ("STR-01", "Bridge Deck, Pier & Fracture-Critical Member Inspection", 40, 100.0),
    ("STR-02", "Commercial Building Envelope, Roof Membrane Moisture & Facade NDT", 40, 100.0),
    ("STR-03", "Roadway Pavement Distress, Rutting & ASTM D6433 PCI Survey", 40, 100.0)
]

now_utc = datetime.now(timezone.utc).isoformat()
for code, title, hrs, score in courses:
    rec_hash = hashlib.sha256(f"HVF-TECH-001|{code}|{hrs}|{score}|{now_utc}".encode()).hexdigest()
    cur.execute("SELECT id FROM student_course_records WHERE student_id = ? AND course_code = ?", ("HVF-TECH-001", code))
    if not cur.fetchone():
        cur.execute("""
        INSERT INTO student_course_records (
            student_id, full_name, course_code, course_title, hours_completed,
            total_hours_required, practicum_score_pct, exam_score_pct,
            certification_status, lead_evaluator, sha256_record_seal, timestamp_utc
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "HVF-TECH-001", "Jeffery Humphrey", code, title, hrs, hrs, score, score,
            "CERTIFIED_MASTER_INSPECTOR", "Humphrey Virtual Farms LLC (CAGE: 1AHA8)", rec_hash, now_utc
        ))
        print(f"[+] Certified Credential Logged: {code} (40 Hours) -> {title}")

conn.commit()

cur.execute("SELECT COUNT(*), SUM(hours_completed) FROM student_course_records WHERE student_id = 'HVF-TECH-001'")
count, total_hrs = cur.fetchone()
print(f"\n[+] Lead SME Record: {count} Courses Certified | {total_hrs} Total Accredited Hours")
conn.close()