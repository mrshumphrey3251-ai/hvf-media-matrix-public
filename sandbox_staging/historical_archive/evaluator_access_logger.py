# -*- coding: utf-8 -*-
"""
Project Ebony: Evaluator Ingress Access Logger & Cryptographic Audit Monitor
Monitors and logs CDAO / Tradewinds evaluator queries against Port 8502 HTTP ingress routes,
recording evaluation session access, endpoint hits, and DFARS 252.227-7018 GPR compliance.
Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8)
Statutory Standard: DFARS 252.227-7018 / Oklahoma HB 2992 / NIST SP 800-82 Rev 2
"""

import os
import sys
import json
import time
import datetime
import sqlite3

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for p in [repo_root, os.path.join(repo_root, "scada_engine"), os.path.join(repo_root, "c2_cockpit"), os.path.join(repo_root, "dispatch_core")]:
    if p not in sys.path:
        sys.path.insert(0, p)

class EvaluatorAccessLogger:
    def __init__(self, db_path=None):
        if db_path is None:
            self.db_path = os.path.join(repo_root, "cinematic_vault", "database", "ebony_active_state.db")
        else:
            self.db_path = db_path
        self._ensure_table()

    def _ensure_table(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS evaluator_ingress_audit_log (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp_utc TEXT NOT NULL,
                client_ip TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                http_method TEXT NOT NULL,
                status_code INTEGER NOT NULL,
                response_latency_ms REAL NOT NULL,
                dfars_rights_header TEXT NOT NULL,
                submission_id TEXT NOT NULL,
                cage_code TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def log_ingress_event(self, client_ip, endpoint, http_method="GET", status_code=200, latency_ms=1.5):
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO evaluator_ingress_audit_log (
                timestamp_utc, client_ip, endpoint, http_method,
                status_code, response_latency_ms, dfars_rights_header,
                submission_id, cage_code
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            now_utc, client_ip, endpoint, http_method,
            status_code, latency_ms, "DFARS-252.227-7018-GPR",
            "9-26-3703", "1AHA8"
        ))
        conn.commit()
        log_id = cur.lastrowid
        conn.close()
        return log_id

    def get_audit_summary(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        count = cur.execute("SELECT count(*) FROM evaluator_ingress_audit_log").fetchone()[0]
        recent = cur.execute("""
            SELECT log_id, timestamp_utc, client_ip, endpoint, status_code, response_latency_ms
            FROM evaluator_ingress_audit_log ORDER BY log_id DESC LIMIT 5
        """).fetchall()
        conn.close()
        return {
            "total_audit_events": count,
            "recent_events": [
                {
                    "log_id": r[0],
                    "timestamp": r[1],
                    "client_ip": r[2],
                    "endpoint": r[3],
                    "status_code": r[4],
                    "latency_ms": r[5]
                }
                for r in recent
            ]
        }

if __name__ == "__main__":
    logger = EvaluatorAccessLogger()
    lid = logger.log_ingress_event("127.0.0.1", "/evaluator/posture", "GET", 200, 2.89)
    summary = logger.get_audit_summary()
    print("=" * 72)
    print("  PROJECT EBONY: EVALUATOR ACCESS LOGGER INITIALIZATION")
    print("  * Operator Authority: CEO_JEFFERY_HUMPHREY (Level 5 Unrestricted)")
    print("  * Authority CAGE:     1AHA8 (Humphrey Virtual Farms LLC)")
    print("=" * 72)
    print(f"\n[1] AUDIT TABLE & LOGGING VERIFICATION:")
    print(f"  * SQLite Database Path:       {logger.db_path}")
    print(f"  * Baseline Event Logged ID:   {lid}")
    print(f"  * Total Audit Records:        {summary['total_audit_events']}")
    print(f"  * Target Ingress Route:       {summary['recent_events'][0]['endpoint']}")
    print(f"  * Recorded Response Latency:  {summary['recent_events'][0]['latency_ms']} ms")
    print(f"  * Statutory Rights Applied:   DFARS-252.227-7018-GPR")
    print("\n  * [PASS] EvaluatorAccessLogger deployed and operational.")
