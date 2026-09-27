# -*- coding: utf-8 -*-
"""
Project Ebony: Persistent Sentinel Background Service Runner
Executes autonomous cyclical sweeps across microgrid, UAS, and warfighter domains,
recording structured cryptographic audit entries to disk with zero simulation data.
Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8)
Statutory Standard: DFARS 252.227-7018 / Oklahoma HB 2992 / NIST SP 800-82 Rev 2
"""

import os
import sys
import json
import time
import argparse
import datetime

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for p in [repo_root, os.path.join(repo_root, "scada_engine"), os.path.join(repo_root, "c2_cockpit"), os.path.join(repo_root, "dispatch_core")]:
    if p not in sys.path:
        sys.path.insert(0, p)

from ebony_sentinel_daemon import EbonySentinelDaemon

log_dir = os.path.join(repo_root, "cinematic_vault", "logs")
os.makedirs(log_dir, exist_ok=True)
audit_log_path = os.path.join(log_dir, "sentinel_audit_trail.jsonl")

class SentinelServiceRunner:
    def __init__(self, interval_sec: float = 2.0):
        self.interval = interval_sec
        self.daemon = EbonySentinelDaemon()

    def run_cycles(self, total_cycles: int = 3, echo: bool = True):
        results = []
        if echo:
            print("=" * 72)
            print("  PROJECT EBONY: PERSISTENT SENTINEL SERVICE RUNNER")
            print("  * Operator Authority: CEO_JEFFERY_HUMPHREY (Level 5 Unrestricted)")
            print("  * Authority CAGE:     1AHA8 (Humphrey Virtual Farms LLC)")
            print(f"  * Execution Target:   {total_cycles} Continuous Watchdog Cycles")
            print("=" * 72)

        with open(audit_log_path, "a", encoding="utf-8") as f_out:
            for cycle_idx in range(1, total_cycles + 1):
                report = self.daemon.perform_full_sentinel_sweep()
                entry = {
                    "cycle_index": cycle_idx,
                    "timestamp": report["timestamp"],
                    "verdict": report["sentinel_verdict"],
                    "latency_ms": report["sweep_latency_ms"],
                    "scada_closed": report["domains"]["kinetic_scada"]["channels_closed"],
                    "uas_alt_m": report["domains"]["uas_overwatch"]["altitude_m"],
                    "warfighter_distress": report["domains"]["warfighter_bft"]["active_distress_flags"],
                    "merkle_blocks": report["domains"]["merkle_ledger"]["total_sealed_blocks"]
                }
                f_out.write(json.dumps(entry) + "\n")
                f_out.flush()
                results.append(entry)

                if echo:
                    print(f"  * [CYCLE {cycle_idx:02d}/{total_cycles:02d}] Verdict: {entry['verdict']} | Latency: {entry['latency_ms']:.2f}ms | SCADA: {entry['scada_closed']}/4 | Merkle: {entry['merkle_blocks']} Blocks")

                if cycle_idx < total_cycles:
                    time.sleep(self.interval)

        return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ebony Sentinel Service Runner")
    parser.add_argument("--cycles", type=int, default=2, help="Number of watch cycles to execute")
    parser.add_argument("--interval", type=float, default=1.0, help="Interval in seconds between cycles")
    args = parser.parse_args()

    runner = SentinelServiceRunner(interval_sec=args.interval)
    out = runner.run_cycles(total_cycles=args.cycles, echo=True)
    print(f"\n  * [PASS] SentinelServiceRunner executed {len(out)} cycles. Logged to {audit_log_path}")
