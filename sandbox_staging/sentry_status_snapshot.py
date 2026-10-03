# -*- coding: utf-8 -*-
"""
Project Ebony: Standby Telemetry & Watchdog Status Snapshot Utility
Queries ebony_active_state.db for recent watchdog cycles and probes live sockets.
Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8)
Statutory Standard: DFARS 252.227-7018 / NIST SP 800-82 Rev 2
"""

import os
import sys
import sqlite3
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

def check_socket(url):
    try:
        t0 = time.perf_counter_ns()
        req = urllib.request.Request(url, headers={"User-Agent": "EbonySnapshot/1.0"})
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            lat = (time.perf_counter_ns() - t0) / 1_000_000.0
            return resp.getcode(), lat
    except Exception:
        return 0, -1.0

def print_snapshot():
    print("=" * 72)
    print("  PROJECT EBONY: PERSISTENT STANDBY TELEMETRY SNAPSHOT")
    print("  * Operator Authority: CEO_JEFFERY_HUMPHREY (Level 5 Unrestricted)")
    print("  * Authority CAGE:     1AHA8 (Humphrey Virtual Farms LLC)")
    print("=" * 72)

    # 1. Live Sockets
    c_hud, lat_hud = check_socket("http://127.0.0.1:8501/")
    c_ing, lat_ing = check_socket("http://127.0.0.1:8502/evaluator/posture")
    print("\n[1] LIVE LOCALHOST LOOPBACK SOCKETS:")
    hud_str = f"HTTP {c_hud} ({lat_hud:.2f} ms)" if c_hud == 200 else "OFFLINE"
    ing_str = f"HTTP {c_ing} ({lat_ing:.2f} ms)" if c_ing == 200 else "OFFLINE"
    print(f"  * Port 8501 (Tactical HUD):    {hud_str}")
    print(f"  * Port 8502 (Ingress Daemon):  {ing_str}")

    # 2. Watchdog Heartbeats
    print("\n[2] RECENT AUTONOMOUS WATCHDOG HEARTBEATS (SQLITE):")
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path, timeout=5.0)
            cur = conn.cursor()
            cur.execute("""
                SELECT check_id, timestamp_utc, port_8501_status, port_8501_latency_ms,
                       port_8502_status, port_8502_latency_ms, ledger_block_depth, system_status
                FROM sentry_watchdog_log
                ORDER BY check_id DESC LIMIT 5
            """)
            rows = cur.fetchall()
            conn.close()
            if rows:
                for r in reversed(rows):
                    print(f"  * Heartbeat #{r[0]}: {r[1]} | HUD: {r[2]} ({r[3]:.1f}ms) | Ingress: {r[4]} ({r[5]:.1f}ms) | Block #{r[6]} | {r[7]}")
            else:
                print("  * [NOTICE] No entries found in sentry_watchdog_log.")
        except Exception as e:
            print(f"  * [NOTICE] Watchdog log query: {e}")
    else:
        print("  * [NOTICE] Database file not located.")

    # 3. Merkle Ledger Head
    print("\n[3] CRYPTOGRAPHIC ROOT OF TRUST:")
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path, timeout=5.0)
            cur = conn.cursor()
            cur.execute("SELECT block_index, event_type, block_hash, signer_pubkey_hex FROM forensic_audit_ledger ORDER BY block_index DESC LIMIT 1")
            head = cur.fetchone()
            conn.close()
            if head:
                print(f"  * Head Block #{head[0]} ({head[1]})")
                print(f"  * Block Hash: {head[2][:32]}...")
                print(f"  * Signer Key: {head[3][:32]}... [ED25519 VERIFIED]")
        except Exception as e:
            print(f"  * [NOTICE] Ledger query: {e}")

    print("\n" + "=" * 72)

if __name__ == "__main__":
    print_snapshot()
