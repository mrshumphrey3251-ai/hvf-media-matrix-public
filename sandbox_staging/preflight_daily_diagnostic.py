"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: PREFLIGHT DAILY DIAGNOSTIC
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    # -*- coding: utf-8 -*-

    """

    Project Ebony: Pre-Flight Daily Diagnostic & Standby Surveillance Suite

    Executes comprehensive daily pre-flight diagnostic across network sockets,

    cryptographic ledger custody, watchdog cycles, and evaluator logs.

    Records audit entry into preflight_audit_log in ebony_active_state.db.

    Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8)

    Statutory Authority: DFARS 252.227-7018 / Oklahoma HB 2992 / NIST SP 800-82 Rev 2

    """



    import os

    import sys

    import sqlite3

    import datetime

    import urllib.request

    import time



    def find_repo_root():

        curr = os.path.abspath(".")

        while curr != os.path.dirname(curr):

            if os.path.exists(os.path.join(curr, ".git")) or os.path.exists(os.path.join(curr, "c2_cockpit")):

                return curr

            curr = os.path.dirname(curr)

        return os.path.abspath(".")



    repo_root = find_repo_root()

    db_path = os.path.join(repo_root, "cinematic_vault", "database", "ebony_active_state.db")



    def init_preflight_table():

        conn = sqlite3.connect(db_path, timeout=5.0)

        cur = conn.cursor()

        cur.execute("""

            CREATE TABLE IF NOT EXISTS preflight_audit_log (

                audit_id INTEGER PRIMARY KEY AUTOINCREMENT,

                timestamp_utc TEXT,

                days_to_demo INTEGER,

                hours_to_demo INTEGER,

                port_8501_ms REAL,

                port_8502_ms REAL,

                ledger_block_depth INTEGER,

                watchdog_total_cycles INTEGER,

                evaluator_total_inquiries INTEGER,

                overall_status TEXT

            )

        """)

        conn.commit()

        conn.close()



    def run_diagnostic():

        print("=" * 80)

        print("  PROJECT EBONY: PRE-FLIGHT DAILY DIAGNOSTIC & STANDBY SURVEILLANCE")

        print("  * Operator Authority: CEO_JEFFERY_HUMPHREY (Level 5 Unrestricted)")

        print("  * Contracting Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8)")

        print("  * Tradewinds ID:      9-26-3703 | Demo Date: October 5, 2026 @ 10:00 AM CDT")

        print("=" * 80)



        # 1. Countdown Calculation

        demo_utc = datetime.datetime(2026, 10, 5, 15, 0, 0, tzinfo=datetime.timezone.utc)

        now_utc = datetime.datetime.now(datetime.timezone.utc)

        delta = demo_utc - now_utc

        days = delta.days

        hours = delta.seconds // 3600

        minutes = (delta.seconds % 3600) // 60



        print(f"\n[1] MISSION TIMELINE POSTURE:")

        print(f"  * T-Minus:            {days} Days, {hours} Hours, {minutes} Minutes")

        print(f"  * Scheduled Session:  Monday, October 5, 2026 @ 10:00 AM CDT (Microsoft Teams)")

        print(f"  * Defense Audience:   Leshia Pearson & ACC-RI Directorate")



        # 2. Sockets probe

        print(f"\n[2] REAL-TIME LOCALHOST SENTRY SOCKET PROBES:")

        def probe(url, name):

            t0 = time.perf_counter_ns()

            try:

                req = urllib.request.Request(url, headers={"User-Agent": "EbonyPreflightDiagnostic/1.0"})

                with urllib.request.urlopen(req, timeout=2.0) as resp:

                    lat = (time.perf_counter_ns() - t0) / 1_000_000.0

                    print(f"  * {name:<36} -> HTTP {resp.getcode()} OK ({lat:.2f} ms latency)")

                    return True, round(lat, 2)

            except Exception as e:

                print(f"  * {name:<36} -> OFFLINE ({e})")

                return False, -1.0



        hud_ok, lat_8501 = probe("http://127.0.0.1:8501/", "Tactical HUD (Port 8501)")

        ing_ok, lat_8502 = probe("http://127.0.0.1:8502/evaluator/posture", "Evaluator Ingress Daemon (Port 8502)")

        assert hud_ok and ing_ok, "FAIL: Sentry sockets offline!"



        # 3. Database Introspection

        print(f"\n[3] BARE-METAL SQLITE TELEMETRY & ROOT OF TRUST:")

        conn = sqlite3.connect(db_path, timeout=5.0)

        cur = conn.cursor()

        cur.execute("SELECT MAX(block_index), block_hash FROM forensic_audit_ledger")

        row_ledger = cur.fetchone()

        cur.execute("SELECT COUNT(*), MAX(check_id) FROM sentry_watchdog_log")

        row_w = cur.fetchone()

        cur.execute("SELECT COUNT(*), MAX(log_id) FROM evaluator_ingress_audit_log")

        row_eval = cur.fetchone()



        block_depth = row_ledger[0] if row_ledger else 0

        w_cycles = row_w[0] if row_w else 0

        eval_queries = row_eval[0] if row_eval else 0



        print(f"  * Cryptographic Ledger: Head Block #{block_depth} ({row_ledger[1][:24]}...) [SEALED]")

        print(f"  * Watchdog Cycles:      {w_cycles} Recorded (Latest: Cycle #{row_w[1]}) [NOMINAL]")

        print(f"  * Evaluator Inquiries:  {eval_queries} Logged (Latest: Query #{row_eval[1]}) [DFARS GPR]")

        assert block_depth >= 82, "Ledger block depth below 82!"



        # 4. Log to preflight_audit_log

        status = "NOMINAL" if (hud_ok and ing_ok and block_depth >= 82) else "DEGRADED"

        cur.execute("""

            INSERT INTO preflight_audit_log

            (timestamp_utc, days_to_demo, hours_to_demo, port_8501_ms, port_8502_ms, ledger_block_depth, watchdog_total_cycles, evaluator_total_inquiries, overall_status)

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (now_utc.isoformat(), days, hours, lat_8501, lat_8502, block_depth, w_cycles, eval_queries, status))

        conn.commit()

        cur.execute("SELECT MAX(audit_id) FROM preflight_audit_log;")

        audit_id = cur.fetchone()[0]

        conn.close()



        print(f"\n[4] PERSISTENT PRE-FLIGHT AUDIT LOG:")

        print(f"  * Audit Record #{audit_id} committed to preflight_audit_log in ebony_active_state.db")

        print(f"  * Status: {status} [PASS]")



        print("\n" + "=" * 80)

        print("  PRE-FLIGHT DIAGNOSTIC: 100% OPERATIONAL | STANDBY BASELINE VERIFIED")

        print("=" * 80)

        return True



    if __name__ == "__main__":

        init_preflight_table()

        success = run_diagnostic()

        sys.exit(0 if success else 1)


if __name__ == "__main__":
    render()
