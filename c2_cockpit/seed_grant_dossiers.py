import sqlite3
from datetime import datetime, timezone
from pathlib import Path

target_db = Path(r"C:\hvf_c2\hvf-media-matrix-private\matrix_ledger.db")
conn = sqlite3.connect(str(target_db))
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS grant_proposals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grant_acronym TEXT NOT NULL,
    full_program_name TEXT NOT NULL,
    funding_agency TEXT NOT NULL,
    targeted_allocation_usd REAL NOT NULL,
    statutory_focus TEXT NOT NULL,
    cage_code TEXT NOT NULL,
    status TEXT NOT NULL,
    dossier_timestamp_utc TEXT NOT NULL
)
""")

grants = [
    (
        "SEP",
        "State Energy Program // Kinetic Microgrid Resilience",
        "Oklahoma Department of Commerce / U.S. DOE",
        250000.00,
        "Sub-16ms Kinetic Islanding & Sovereign Battery Storage under OK Title 61",
        "1AHA8",
        "DOSSIER_STAGED_FOR_OMES_VENDOR_ACTIVATION",
        datetime.now(timezone.utc).isoformat()
    ),
    (
        "REAP",
        "Rural Energy for America Program (Section 9007)",
        "USDA Rural Development",
        500000.00,
        "Zero-Carbon Agricultural Facility Grain Aeration & Microgrid SCADA",
        "1AHA8",
        "DOSSIER_STAGED_FOR_OMES_VENDOR_ACTIVATION",
        datetime.now(timezone.utc).isoformat()
    ),
    (
        "OCAST_AGTECH",
        "Oklahoma Applied Research Program (OARP)",
        "Oklahoma Center for the Advancement of Science and Technology",
        150000.00,
        "Autonomous Edge UAS Diagnostics & Air-Gapped Canopy Computer Vision",
        "1AHA8",
        "DOSSIER_STAGED_FOR_OMES_VENDOR_ACTIVATION",
        datetime.now(timezone.utc).isoformat()
    ),
    (
        "NIFA_AFRI",
        "Agriculture and Food Research Initiative (AFRI)",
        "USDA National Institute of Food and Agriculture",
        650000.00,
        "Distributed Sovereign C2 Matrix for Resilient Food Supply & Storage",
        "1AHA8",
        "DOSSIER_STAGED_FOR_OMES_VENDOR_ACTIVATION",
        datetime.now(timezone.utc).isoformat()
    )
]

for g in grants:
    cur.execute("SELECT id FROM grant_proposals WHERE grant_acronym = ?", (g[0],))
    if not cur.fetchone():
        cur.execute("""
        INSERT INTO grant_proposals (
            grant_acronym, full_program_name, funding_agency, targeted_allocation_usd, statutory_focus, cage_code, status, dossier_timestamp_utc
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, g)
        print(f"[+] Staged Grant Dossier: {g[0]} (${g[3]:,.2f}) -> {g[1]}")
    else:
        print(f"[*] Grant Dossier already exists: {g[0]}")

conn.commit()
conn.close()