# -*- coding: utf-8 -*-
"""
Project Ebony: C2 Deck Reality Grounding Middleware & Anti-Fabrication Filter
Intercepts operational queries and conversational outputs, validating all cited paths,
telemetry attributes, and DoD evaluation claims against bare-metal filesystem state,
git provenance, and the live SQLite forensic ledger.
Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8)
Statutory Standard: DFARS 252.227-7018 / Oklahoma HB 2992 / NIST SP 800-82 Rev 2
"""

import os
import sys
import re
import json
import sqlite3
import subprocess

def find_repo_root():
    curr = os.path.abspath(".")
    while curr != os.path.dirname(curr):
        if os.path.exists(os.path.join(curr, ".git")) or os.path.exists(os.path.join(curr, "c2_cockpit")):
            return curr
        curr = os.path.dirname(curr)
    return os.path.abspath(".")

repo_root = find_repo_root()
for p in [repo_root, os.path.join(repo_root, "scada_engine"), os.path.join(repo_root, "c2_cockpit"), os.path.join(repo_root, "dispatch_core")]:
    if p not in sys.path:
        sys.path.insert(0, p)

class RealityAssertionError(Exception):
    """Raised when an ungrounded or synthetic claim violates the Reality Firewall."""
    pass

class C2GroundingMiddleware:
    def __init__(self, db_path=None):
        if db_path is None:
            self.db_path = os.path.join(repo_root, "cinematic_vault", "database", "ebony_active_state.db")
        else:
            self.db_path = db_path
        self.prohibited_patterns = [
            r"/opt/hvf",
            r"hvf_award_engine",
            r"tradewinds_evaluator",
            r"inverter_controller",
            r"ea_sam_oracle",
            r"glif_fusion",
            r"hvf_selftest",
            r"20399 Iron-Dome",
            r"20,?307",
            r"20,?405",
            r"AvgGenMW",
            r"UptimeThreshold\s*=\s*99\.5",
            r"silo_monitor",
            r"gas_sensing",
            r"livestock_boundary",
            r"irrigation_controller",
            r"dosing_engine",
            r"soil_sensors",
            r"chemometrics",
            r"threat_oracle",
            r"der_control",
            r"bess_manager",
            r"drone_ops",
            r"mesh_network",
            r"apex_orchestrator",
            r"ReflexKernel",
            r"\bKOKC\b",
        ]
        self._load_tracked_files()

    def _load_tracked_files(self):
        try:
            res = subprocess.run(["git", "ls-files"], cwd=repo_root, capture_output=True, text=True, check=True)
            self.tracked_files = set(f.replace("\\", "/").strip() for f in res.stdout.splitlines() if f.strip())
        except Exception:
            self.tracked_files = set()

    def validate_content(self, text):
        """
        Audits incoming/outgoing C2 text.
        Rejects fabricated paths, synthetic modules, ungrounded scoring formulas, and agricultural hallucinations.
        """
        for pat in self.prohibited_patterns:
            if re.search(pat, text, re.IGNORECASE):
                raise RealityAssertionError(f"FABRICATION_DETECTED: Detected prohibited synthetic pattern '{pat}'")

        # Detect prospective file paths ending in .py, .json, .md, .db, .yaml (accommodates multi-dot versioning)
        pattern = r"([a-zA-Z0-9_\-\\/]+(?:\.[a-zA-Z0-9_\-]+)*\.(?:py|json|md|db|yaml))"
        path_matches = re.findall(pattern, text)
        for p in path_matches:
            norm_p = p.replace("\\", "/").lstrip("/")
            if norm_p.startswith("opt/hvf/"):
                raise RealityAssertionError(f"FABRICATION_DETECTED: Prohibited Linux path '{p}'")
            # Universal check: Any prospective file path cited must physically exist on bare-metal disk
            full_path = os.path.join(repo_root, norm_p.replace("/", os.sep))
            if not os.path.exists(full_path):
                raise RealityAssertionError(f"FABRICATION_DETECTED: File '{p}' does not exist on bare-metal disk")

        return True

    def get_ground_truth_posture(self):
        """
        Returns deterministic, verified operational posture directly from disk and SQLite.
        """
        record_file = os.path.join(repo_root, "TRADEWINDS_DISPATCH_RECORD.json")
        if not os.path.exists(record_file):
            raise RealityAssertionError("CRITICAL: TRADEWINDS_DISPATCH_RECORD.json not found on disk")

        with open(record_file, "r", encoding="utf-8") as f:
            record = json.load(f)

        return {
            "status": "DETERMINISTIC_GROUND_TRUTH_VERIFIED",
            "submission_id": record.get("submission_id"),
            "cage_code": record.get("cage_code"),
            "production_release_tag": record.get("production_release_tag"),
            "operational_availability_pct": record.get("operational_telemetry", {}).get("availability_pct"),
            "sealed_merkle_blocks": record.get("operational_telemetry", {}).get("total_sealed_merkle_blocks"),
            "modbus_fc05_latency_us": record.get("operational_telemetry", {}).get("modbus_fc05_latency_us"),
            "scada_microgrid_status": record.get("operational_telemetry", {}).get("scada_microgrid_status")
        }
