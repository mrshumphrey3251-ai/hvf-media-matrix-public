import os
import sqlite3
import json

DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\hvf_memory_vault.db"
PROP_DIR = r"C:\HVF_Repos\hvf-media-matrix-private\proposals"
os.makedirs(PROP_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)
conn.execute("""
    CREATE TABLE IF NOT EXISTS sovereign_grant_pipeline (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agency TEXT NOT NULL,
        sector TEXT NOT NULL,
        program_vehicle TEXT NOT NULL,
        entry_funding TEXT NOT NULL,
        scaling_ceiling TEXT NOT NULL,
        turnaround_days TEXT NOT NULL,
        ebony_brain_alignment TEXT NOT NULL,
        submission_requirement TEXT NOT NULL,
        status TEXT NOT NULL
    )
""")

# Wipe previous records for clean sync
conn.execute("DELETE FROM sovereign_grant_pipeline")

pipelines = [
    (
        "Defense Innovation Unit (DIU)",
        "Defense / Edge Cyber-Physical",
        "Commercial Solutions Opening (Prototype OT)",
        "$500K - $1.65M",
        "$10M+ (Sole-Source Production OT)",
        "60-90 Days",
        "Brain One (SCADA Interlocks) & Brain Three (Merkle Vault)",
        "5-Page Solution Brief against active Area of Interest (AOI)",
        "STAGED_READY"
    ),
    (
        "Department of the Air Force (AFWERX)",
        "Defense / Autonomous Systems",
        "Open Topic SBIR / D2P2",
        "$75K (Phase I) / $1.25M (Phase II)",
        "$15M+ (STRATFI / Phase III)",
        "90 Days",
        "Brain Two (Offline Neural Drift) & Brain One (Safety Limits)",
        "15-Slide Commercialization Deck + Capability White Paper",
        "TARGETING_CYCLE"
    ),
    (
        "National Science Foundation (NSF)",
        "Foundational Deep Tech / Cyber",
        "America's Seed Fund SBIR Phase I",
        "$275,000",
        "$1,150,000 (Phase II)",
        "90-120 Days",
        "Brain Three (Air-Gapped Merkle Provenance & Byzantine Consensus)",
        "3-Page Project Pitch (Rolling Submission / Zero Sponsor Needed)",
        "ACTIVE_DEVELOPMENT"
    ),
    (
        "USDA NIFA (AgTech)",
        "Controlled Environment Agriculture",
        "Small Business Innovation Research (8.12)",
        "$175,000",
        "$600,000 (Phase II)",
        "120 Days",
        "Brain One (Nutrient SCADA) & Brain Two (Phenotypic Drift)",
        "Technical Narrative on Autonomous Food Production Resilience",
        "TARGETING_ANNUAL"
    ),
    (
        "Department of Energy (DOE EERE/CESER)",
        "Critical Infrastructure / Microgrids",
        "Clean Energy & Cybersecurity SBIR",
        "$200,000",
        "$1,100,000 (Phase II)",
        "90-120 Days",
        "Three-Brain Triad (Zero-Cloud Industrial Energy Management)",
        "Project Narrative on Grid Edge SCADA Defense & Islanding",
        "TARGETING_SOLICITATION"
    )
]

for p in pipelines:
    conn.execute("""
        INSERT INTO sovereign_grant_pipeline 
        (agency, sector, program_vehicle, entry_funding, scaling_ceiling, turnaround_days, ebony_brain_alignment, submission_requirement, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, p)

conn.close()

print("=" * 85)
print("HVF Omni-Industrial Matrix | SOVEREIGN MULTI-INDUSTRY GRANT PORTFOLIO")
print("CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | 100% UNENCUMBERED PRIME")
print("=" * 85)
print(f"{'AGENCY':<18} | {'SECTOR':<22} | {'ENTRY FUNDING':<15} | {'LEAD TIME':<10} | {'STATUS'}")
print("-" * 85)
for p in pipelines:
    print(f"{p[0]:<18} | {p[1]:<22} | {p[3]:<15} | {p[5]:<10} | {p[8]}")
print("=" * 85)
print("[CONFIRMED] Multi-industry pipeline logged in hvf_memory_vault.db.")

