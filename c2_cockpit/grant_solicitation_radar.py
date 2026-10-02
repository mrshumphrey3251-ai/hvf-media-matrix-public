import os
import sqlite3
from datetime import datetime

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")

conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)
conn.execute("""
    CREATE TABLE IF NOT EXISTS active_solicitation_intake (
        solicitation_id TEXT PRIMARY KEY,
        agency TEXT NOT NULL,
        title TEXT NOT NULL,
        sector TEXT NOT NULL,
        vehicle TEXT NOT NULL,
        max_award_usd REAL NOT NULL,
        mobilization_eligible INTEGER DEFAULT 1,
        brain_fit TEXT NOT NULL,
        urgency TEXT NOT NULL,
        submission_format TEXT NOT NULL,
        status TEXT NOT NULL,
        last_scanned TEXT NOT NULL
    )
""")

opportunities = [
    (
        "DIU-AOI-2026-AUTONOMY",
        "Defense Innovation Unit (DIU)",
        "Contested Logistics & Edge Autonomy Resiliency",
        "Defense / Autonomy",
        "10 U.S.C. 4022 Prototype OT",
        1650000.00,
        1,
        "Brain One (SCADA Interlocks) & Brain Two (Offline Cognitive AI)",
        "HIGH - Q4 2026",
        "5-Page Solution Brief",
        "READY_TO_SUBMIT",
        datetime.now().isoformat()
    ),
    (
        "DIU-AOI-2026-ENERGY",
        "Defense Innovation Unit (DIU)",
        "Tactical Microgrid Hardening & SCADA Cyber-Physical Defense",
        "Defense / Critical Infrastructure",
        "10 U.S.C. 4022 Prototype OT",
        2000000.00,
        1,
        "Brain One (Kinetic Guillotine) & Brain Three (Merkle DAG Vault)",
        "HIGH - Q4 2026",
        "5-Page Solution Brief",
        "READY_TO_SUBMIT",
        datetime.now().isoformat()
    ),
    (
        "NSF-SBIR-2026-P1",
        "National Science Foundation (NSF)",
        "America's Seed Fund: Trustworthy Cyber-Physical Systems & Edge AI",
        "Civilian / Deep Tech",
        "SBIR Phase I Grant",
        275000.00,
        1,
        "Brain Three (Air-Gapped Merkle Provenance & Byzantine Consensus)",
        "MEDIUM - Rolling Windows",
        "3-Page Project Pitch",
        "STAGED_DEVELOPMENT",
        datetime.now().isoformat()
    ),
    (
        "USDA-NIFA-8.12-2026",
        "USDA NIFA",
        "Small Business Innovation: Closed-Loop Automation for Controlled Environment Ag",
        "Civilian / AgTech",
        "SBIR Phase I Grant",
        175000.00,
        0,
        "Brain One (Nutrient SCADA) & Brain Two (Biological Drift Analysis)",
        "MEDIUM - Annual Cycle",
        "Technical Narrative + Dual-Use Commercialization Plan",
        "STAGED_DEVELOPMENT",
        datetime.now().isoformat()
    ),
    (
        "DOE-CESER-2026-GRID",
        "Department of Energy (CESER)",
        "Cybersecurity for Energy Delivery Systems: Air-Gapped Substations",
        "Civilian / Energy Utility",
        "SBIR / FOA Grant",
        250000.00,
        1,
        "Three-Brain Triad (Zero-Cloud Grid Edge SCADA Defense)",
        "HIGH - Q4 2026",
        "Project Narrative Volume",
        "TARGETING_CALL",
        datetime.now().isoformat()
    )
]

for opp in opportunities:
    conn.execute("""
        INSERT OR REPLACE INTO active_solicitation_intake 
        (solicitation_id, agency, title, sector, vehicle, max_award_usd, mobilization_eligible, brain_fit, urgency, submission_format, status, last_scanned)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, opp)

conn.close()

print("=" * 95)
print("PROJECT EBONY | ACTIVE SOLICITATION RADAR INITIALIZED")
print("HVF Omni-Industrial Matrix | CAGE: 1AHA8 | 100% Sovereign Prime")
print("=" * 95)
print(f"{'SOLICITATION ID':<23} | {'AGENCY':<12} | {'MAX AWARD':<12} | {'MOBILIZATION':<14} | {'STATUS'}")
print("-" * 95)
for o in opportunities:
    mob = "$150k Day 15-30" if o[6] == 1 else "Standard Payout"
    print(f"{o[0]:<23} | {o[1][:12]:<12} | ${o[5]:<11,.2f} | {mob:<14} | {o[10]}")
print("=" * 95)
print(f"[SUCCESS] 5 high-yield targets indexed in hvf_memory_vault.db.")

