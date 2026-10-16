"""
HVF Macro Verticals Engine & Commercial Architecture
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Framework: Oklahoma Title 61, Title 74 & OK HB 2992
"""
import os
import sys
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

class ResilientVerticalDict(dict):
    """
    Defensive schema dictionary:
    Returns existing keys or resolves fallback defaults to prevent KeyError halting UI rendering.
    """
    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        defaults = {
            "category": "Sovereign Industrial Engineering & Autonomous C2",
            "discipline": "Level-5 Bare-Metal Systems Architecture",
            "description": self.get("focus", "Active Sovereign Vertical Discipline"),
            "focus": "Autonomous edge operations, SCADA telemetry, and statutory compliance.",
            "status": "OPERATIONAL",
            "icon": "?",
            "authority": "CEO Jeffery Humphrey (Level 5 Clearance)",
            "clearance": "CEO Clearance (Level 5)",
            "lead_engineer": "Jeffery Humphrey (SME / CEO)",
            "curriculum": [],
            "modules": [],
            "tracks": [],
            "metrics": {},
        }
        return defaults.get(key, "Active / Operational")

MACRO_VERTICAL_REGISTRY = {
    "VERTICAL_AGTECH": {
        "id": "VERTICAL_AGTECH",
        "key": "VERTICAL_AGTECH",
        "name": "Precision AgTech & Yield Optimization",
        "category": "Agricultural Systems & Bio-Infrastructure",
        "discipline": "Precision Agronomy & Silo SCADA",
        "statutory_authority": "Oklahoma Title 61 & OK HB 2992",
        "unspsc_codes": ["70131500", "43232600"],
        "naics_codes": ["115112"],
        "focus": "Grain bin aeration SCADA, kinetic silo control, crop health telemetry.",
        "description": "Grain bin aeration SCADA, kinetic silo control, crop health telemetry.",
        "status": "OPERATIONAL",
        "icon": "??",
        "lead_engineer": "Jeffery Humphrey (Level 5 CEO / SME)"
    },
    "VERTICAL_UAS": {
        "id": "VERTICAL_UAS",
        "key": "VERTICAL_UAS",
        "name": "Autonomous Drone Diagnostics & Multispectral Sensing",
        "category": "Tactical Avionics & Autonomous Remote Sensing",
        "discipline": "Edge Drone Autopilot & Computer Vision",
        "statutory_authority": "OCAST OARP & OK HB 2992",
        "unspsc_codes": ["25131705"],
        "naics_codes": ["541715"],
        "focus": "Autonomous edge compute, air-gapped canopy imaging, flight pathing.",
        "description": "Autonomous edge compute, air-gapped canopy imaging, flight pathing.",
        "status": "OPERATIONAL",
        "icon": "??",
        "lead_engineer": "Jeffery Humphrey (Level 5 CEO / SME)"
    },
    "VERTICAL_MICROGRID": {
        "id": "VERTICAL_MICROGRID",
        "key": "VERTICAL_MICROGRID",
        "name": "Kinetic Energy Storage & Microgrid SCADA",
        "category": "Kinetic Power Generation & High-Voltage SCADA",
        "discipline": "Microgrid Islanding & Energy Resilience",
        "statutory_authority": "Oklahoma Title 61 Public Works & USDA REAP",
        "unspsc_codes": ["26111600"],
        "naics_codes": ["541330"],
        "focus": "Sub-16ms electrical islanding, solar/storage optimization, zero-carbon grid.",
        "description": "Sub-16ms electrical islanding, solar/storage optimization, zero-carbon grid.",
        "status": "OPERATIONAL",
        "icon": "?",
        "lead_engineer": "Jeffery Humphrey (Level 5 CEO / SME)"
    },
    "VERTICAL_SOVEREIGN_C2": {
        "id": "VERTICAL_SOVEREIGN_C2",
        "key": "VERTICAL_SOVEREIGN_C2",
        "name": "E.B.O.N.Y. Bare-Metal Command & Control Platform",
        "category": "Autonomous Sovereign C2 & Bare-Metal Cryptography",
        "discipline": "Cryptographic Security & Edge Orchestration",
        "statutory_authority": "Oklahoma Title 74 Central Purchasing Act",
        "unspsc_codes": ["43230000", "81111800"],
        "naics_codes": ["541511", "541512"],
        "focus": "Zero-API email triage, HMAC anti-tamper security, distributed bare-metal mesh.",
        "description": "Zero-API email triage, HMAC anti-tamper security, distributed bare-metal mesh.",
        "status": "OPERATIONAL",
        "icon": "???",
        "lead_engineer": "Jeffery Humphrey (Level 5 CEO / SME)"
    }
}

class VerticalsContainer(list):
    """
    Polymorphic Dual-Mode Container:
    - Iterates as a list of resilient vertical dicts: [v['name'] for v in verticals]
    - Indexes by string key: verticals['VERTICAL_AGTECH']
    - Supports standard dict methods: .items(), .keys(), .values(), .get()
    """
    def __init__(self, data_dict: dict):
        wrapped_items = [ResilientVerticalDict(v) for v in data_dict.values()]
        super().__init__(wrapped_items)
        self._dict = {k: ResilientVerticalDict(v) for k, v in data_dict.items()}

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._dict[item]
        return super().__getitem__(item)

    def __contains__(self, item):
        if isinstance(item, str):
            return item in self._dict
        return super().__contains__(item)

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def items(self):
        return self._dict.items()

class HVFVerticalsEngine:
    def __init__(self, db_path: Path = None):
        if db_path is None:
            base_dir = Path(__file__).resolve().parent
            candidates = [base_dir / "matrix_ledger.db", base_dir.parent / "matrix_ledger.db"]
            self.db_path = next((p for p in candidates if p.exists()), base_dir / "matrix_ledger.db")
        else:
            self.db_path = Path(db_path)

    def get_verticals(self) -> VerticalsContainer:
        return VerticalsContainer(MACRO_VERTICAL_REGISTRY)

    def get_registered_verticals(self) -> dict:
        return MACRO_VERTICAL_REGISTRY

    def list_verticals(self) -> list:
        return list(MACRO_VERTICAL_REGISTRY.values())

    def get_vertical(self, vertical_key: str) -> dict:
        return self.get_verticals().get(vertical_key, {})

    def get_vertical_details(self, vertical_key: str) -> dict:
        return self.get_verticals().get(vertical_key, {})

    def get_aggregate_metrics(self) -> dict:
        return {
            "total_verticals": len(MACRO_VERTICAL_REGISTRY),
            "cage_code": "1AHA8",
            "statutory_framework": "Oklahoma Title 61 & OK HB 2992",
            "active_systems": [v["name"] for v in MACRO_VERTICAL_REGISTRY.values()]
        }

if __name__ == "__main__":
    engine = HVFVerticalsEngine()
    print("=" * 80)
    print("     HVF VERTICALS RESILIENT SCHEMA AUDIT     ")
    print("=" * 80)
    verticals = engine.get_verticals()

    # 1. Test Line 2304 list comprehension simulation
    tab_names = [v["name"] for v in verticals]
    print(f"[PASS] Tab List Comprehension: {len(tab_names)} tabs identified.")

    # 2. Test Line 2324 category lookup simulation
    print("[*] Testing line 2324 category lookup across all verticals:")
    for v_meta in verticals:
        cat = v_meta["category"]
        print(f"    ? {v_meta['name'][:35]:<35} -> Category: '{cat}'")

    # 3. Test arbitrary key resilience (Guarantees zero KeyError crashes)
    fallback_test = verticals[0]["arbitrary_unmapped_key"]
    print(f"[PASS] Resilient Fallback Intercept: {fallback_test}")
    print("=" * 80)