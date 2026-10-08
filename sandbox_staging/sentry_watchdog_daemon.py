"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: SENTRY WATCHDOG DAEMON
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    # -*- coding: utf-8 -*-

    """

    Project Ebony: Continuous Watchdog Sentinel Daemon

    Monitors Port 8501 Tactical HUD, Port 8502 Evaluator Ingress Daemon,

    and SQLite forensic ledger integrity on a 60-second loop.

    Logs health metrics directly to ebony_active_state.db.

    Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8)

    Statutory Standard: DFARS 252.227-7018 / NIST SP 800-82 Rev 2

    """



    import os

    import sys

    import time

    import sqlite3

    import datetime

    import urllib.request



    def find_repo_root():

        curr = os.path.abspath(".")

        while curr != os.path.dirname(curr):

            if os.path.exists(os.path.join(curr, ".git")) or os.path.exists(os.path.join(curr, "c2_cockpit")):

                return curr

            curr = os.path.dirname(curr)

        return os.path.abspath(".")



    repo_root = find_repo_root()

    db_path = os.path.join(repo_root, "cinematic_vault", "database", "ebony_active_state.db")



    def check_endpoint(url):

        try:

            t0 = time.perf_counter_ns()

            req = urllib.request.Request(url, headers={"User-Agent": "EbonyWatchdog/1.0"})

            with urllib.request.urlopen(req, timeout=2.0) as resp:

                lat = (time.perf_counter_ns() - t0) / 1_000_000.0

                return resp.getcode(), round(lat, 2)

        except Exception as e:

            return 0, -1.0



    def get_ledger_depth():

        try:

            conn = sqlite3.connect(db_path, timeout=3.0)

            cur = conn.cursor()

            cur.execute("SELECT MAX(block_index), block_hash FROM forensic_audit_ledger")

            row = cur.fetchone()

            conn.close()

            return row[0], row[1]

        except Exception:

            return -1, "ERROR"



    def init_watchdog_table():

        conn = sqlite3.connect(db_path, timeout=5.0)

        cur = conn.cursor()

        cur.execute("""

            CREATE TABLE IF NOT EXISTS sentry_watchdog_log (

                check_id INTEGER PRIMARY KEY AUTOINCREMENT,

                timestamp_utc TEXT,

                port_8501_status INTEGER,

                port_8501_latency_ms REAL,

                port_8502_status INTEGER,

                port_8502_latency_ms REAL,

                ledger_block_depth INTEGER,

                ledger_head_hash TEXT,

                system_status TEXT

            )

        """)

        conn.commit()

        conn.close()



    def log_check(code_8501, lat_8501, code_8502, lat_8502, blocks, head_hash):

        status = "NOMINAL" if (code_8501 == 200 and code_8502 == 200 and blocks >= 82) else "DEGRADED"

        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

        try:

            conn = sqlite3.connect(db_path, timeout=5.0)

            cur = conn.cursor()

            cur.execute("""

                INSERT INTO sentry_watchdog_log

                (timestamp_utc, port_8501_status, port_8501_latency_ms, port_8502_status, port_8502_latency_ms, ledger_block_depth, ledger_head_hash, system_status)

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)

            """, (now_utc, code_8501, lat_8501, code_8502, lat_8502, blocks, head_hash, status))

            conn.commit()

            conn.close()

        except Exception:

            pass

        return status



    def run_single_pass():

        code_8501, lat_8501 = check_endpoint("http://127.0.0.1:8501/")

        code_8502, lat_8502 = check_endpoint("http://127.0.0.1:8502/evaluator/posture")

        blocks, head_hash = get_ledger_depth()

        status = log_check(code_8501, lat_8501, code_8502, lat_8502, blocks, head_hash)

        return {

            "port_8501": {"code": code_8501, "latency_ms": lat_8501},

            "port_8502": {"code": code_8502, "latency_ms": lat_8502},

            "ledger": {"blocks": blocks, "head": head_hash[:16]},

            "overall_status": status

        }



    if __name__ == "__main__":

        init_watchdog_table()

        if len(sys.argv) > 1 and sys.argv[1] == "--single-pass":

            res = run_single_pass()

            print(f"WATCHDOG_PASS: {res}")

            sys.exit(0)



        while True:

            run_single_pass()

            time.sleep(60)


if __name__ == "__main__":
    render()
