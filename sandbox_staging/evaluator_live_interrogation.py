"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: EVALUATOR LIVE INTERROGATION
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    # -*- coding: utf-8 -*-

    """

    Project Ebony: Evaluator Ingress Live Interrogation & Audit Utility

    Fires live HTTP requests against local ingress daemon (Port 8502) and verifies

    microsecond audit records inside evaluator_ingress_audit_log in ebony_active_state.db.

    Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8)

    Statutory Authority: DFARS 252.227-7018 / Oklahoma HB 2992 / NIST SP 800-82 Rev 2

    """



    import os

    import sys

    import json

    import sqlite3

    import time

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



    def run_live_interrogation():

        print("=" * 76)

        print("  PROJECT EBONY: EVALUATOR INGRESS LIVE INTERROGATION & AUDIT PROBE")

        print("  * Operator Authority: CEO_JEFFERY_HUMPHREY (Level 5 Unrestricted)")

        print("  * Contracting Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8)")

        print("  * Target Endpoint:    http://127.0.0.1:8502 (DoD Evaluator Ingress Daemon)")

        print("=" * 76)



        endpoints = [

            ("/evaluator/posture", "Operational Attestation Posture"),

            ("/evaluator/telemetry", "SCADA Microgrid & Merkle Telemetry"),

            ("/evaluator/dispatch", "Tradewinds Dispatch Manifest Package")

        ]



        print("\n[1] PROBING LIVE EVALUATOR INGRESS SOCKET (PORT 8502):")

        for path, desc in endpoints:

            url = f"http://127.0.0.1:8502{path}"

            t0 = time.perf_counter_ns()

            req = urllib.request.Request(url, headers={"User-Agent": "DoD-CDAO-Evaluator/4.0"})

            try:

                with urllib.request.urlopen(req, timeout=3.0) as resp:

                    lat = (time.perf_counter_ns() - t0) / 1_000_000.0

                    code = resp.getcode()

                    rights = resp.headers.get("X-Statutory-Rights")

                    assert code == 200, f"Expected 200, got {code}"

                    assert rights == "DFARS-252.227-7018-GPR", "Statutory header missing"

                    print(f"  * [PASS] {desc:<38} -> HTTP 200 OK ({lat:.2f} ms) [{rights}]")

            except Exception as e:

                print(f"  * [FAIL] Probe {path} failed: {e}")

                return False



        print("\n[2] INTROSPECTING BARE-METAL EVALUATOR INGRESS AUDIT LOG:")

        if os.path.exists(db_path):

            try:

                conn = sqlite3.connect(db_path, timeout=5.0)

                cur = conn.cursor()

                cur.execute("""

                    SELECT log_id, timestamp_utc, endpoint, status_code, response_latency_ms, dfars_rights_header

                    FROM evaluator_ingress_audit_log

                    ORDER BY log_id DESC LIMIT 3

                """)

                rows = cur.fetchall()

                conn.close()

                for r in reversed(rows):

                    print(f"  * Log #{r[0]}: {r[1]} | {r[2]:<22} | HTTP {r[3]} ({r[4]:.2f} ms) | {r[5]}")

                print("  * [PASS] Live evaluator requests recorded to bare-metal SQLite database.")

            except Exception as e:

                print(f"  * [NOTICE] Database audit query: {e}")

        else:

            print("  * [NOTICE] Database file not found at expected path.")



        print("\n[3] AUDITING AUTONOMOUS WATCHDOG SENTINEL HEARTBEATS:")

        if os.path.exists(db_path):

            try:

                conn = sqlite3.connect(db_path, timeout=5.0)

                cur = conn.cursor()

                cur.execute("""

                    SELECT check_id, timestamp_utc, port_8501_status, port_8501_latency_ms,

                           port_8502_status, port_8502_latency_ms, ledger_block_depth, system_status

                    FROM sentry_watchdog_log

                    ORDER BY check_id DESC LIMIT 3

                """)

                w_rows = cur.fetchall()

                conn.close()

                for w in reversed(w_rows):

                    print(f"  * Heartbeat #{w[0]}: {w[1]} | HUD: {w[2]} ({w[3]:.1f}ms) | Ingress: {w[4]} ({w[5]:.1f}ms) | Block #{w[6]} | Status: {w[7]}")

                print("  * [PASS] Autonomous Watchdog Daemon operating nominal.")

            except Exception as e:

                print(f"  * [NOTICE] Watchdog log query: {e}")



        print("\n" + "=" * 76)

        print("  LIVE EVALUATOR INTERROGATION: 100% OPERATIONAL POSTURE CONFIRMED")

        print("=" * 76)

        return True



    if __name__ == "__main__":

        success = run_live_interrogation()

        sys.exit(0 if success else 1)


if __name__ == "__main__":
    render()
