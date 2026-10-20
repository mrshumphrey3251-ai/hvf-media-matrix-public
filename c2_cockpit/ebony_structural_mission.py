"""
E.B.O.N.Y. Civil Infrastructure Inspection Mission & Docketing Engine
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Framework: Oklahoma Title 61 Public Works, Title 74 & ODOT/CED Standards
"""
import os
import sys
import json
import sqlite3
import hashlib
from datetime import datetime, timezone
from pathlib import Path

base_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private")
cockpit_dir = base_dir / "c2_cockpit"
db_candidates = [cockpit_dir / "matrix_ledger.db", base_dir / "matrix_ledger.db"]
target_db = next((p for p in db_candidates if p.exists()), cockpit_dir / "matrix_ledger.db")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS civil_inspection_dockets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    docket_number TEXT UNIQUE NOT NULL,
    asset_name TEXT NOT NULL,
    sector_type TEXT NOT NULL,
    governing_agency TEXT NOT NULL,
    location_county TEXT NOT NULL,
    gps_coordinates TEXT NOT NULL,
    sensor_payloads TEXT NOT NULL,
    inspection_focus TEXT NOT NULL,
    statutory_authority TEXT NOT NULL,
    mission_status TEXT NOT NULL,
    cage_code TEXT NOT NULL,
    sha256_docket_seal TEXT NOT NULL,
    timestamp_utc TEXT NOT NULL
);
"""

def init_civil_docket_schema(db_path: Path):
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()

def generate_inspection_docket(
    asset_name: str,
    sector_type: str,
    governing_agency: str,
    location_county: str,
    gps_coordinates: str,
    sensor_payloads: list,
    inspection_focus: str,
    statutory_authority: str = "Oklahoma Title 61 & ODOT Element-Level Standards"
) -> dict:
    timestamp = datetime.now(timezone.utc).isoformat()
    docket_seed = f"{asset_name}|{sector_type}|{governing_agency}|{location_county}|{gps_coordinates}|{timestamp}"
    docket_hash = hashlib.sha256(docket_seed.encode("utf-8")).hexdigest()
    docket_num = f"HVF-CIV-{sector_type[:3].upper()}-{docket_hash[:8].upper()}"

    docket_record = {
        "docket_number": docket_num,
        "asset_name": asset_name,
        "sector_type": sector_type,
        "governing_agency": governing_agency,
        "location_county": location_county,
        "gps_coordinates": gps_coordinates,
        "sensor_payloads": json.dumps(sensor_payloads),
        "inspection_focus": inspection_focus,
        "statutory_authority": statutory_authority,
        "mission_status": "MISSION_STAGED_READY_FOR_DEPLOYMENT",
        "cage_code": "1AHA8",
        "sha256_docket_seal": docket_hash,
        "timestamp_utc": timestamp
    }

    # Persist to database
    conn = sqlite3.connect(str(target_db))
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO civil_inspection_dockets (
        docket_number, asset_name, sector_type, governing_agency, location_county,
        gps_coordinates, sensor_payloads, inspection_focus, statutory_authority,
        mission_status, cage_code, sha256_docket_seal, timestamp_utc
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        docket_record["docket_number"],
        docket_record["asset_name"],
        docket_record["sector_type"],
        docket_record["governing_agency"],
        docket_record["location_county"],
        docket_record["gps_coordinates"],
        docket_record["sensor_payloads"],
        docket_record["inspection_focus"],
        docket_record["statutory_authority"],
        docket_record["mission_status"],
        docket_record["cage_code"],
        docket_record["sha256_docket_seal"],
        docket_record["timestamp_utc"]
    ))
    conn.commit()
    conn.close()
    return docket_record

if __name__ == "__main__":
    init_civil_docket_schema(target_db)
    print("=" * 90)
    print("     E.B.O.N.Y. CIVIL INSPECTION MISSION ENGINE INITIALIZED     ")
    print(f"     TARGET LEDGER: {target_db.name} | CAGE: 1AHA8 | JURISDICTION: OK Title 61")
    print("=" * 90)

    # Deploy Baseline Lead Inspection: Canadian County ODOT Bridge Corridor
    lead_bridge = generate_inspection_docket(
        asset_name="Historic Route 66 Canadian River Bridge Complex (ODOT Bridge NBI-04221)",
        sector_type="BRIDGE_STRUCTURAL",
        governing_agency="Oklahoma Department of Transportation (ODOT Division 4) & CED 5",
        location_county="Canadian County, Oklahoma",
        gps_coordinates="35.5342° N, 98.0583° W",
        sensor_payloads=[
            "48MP Sub-Millimeter Radiometric Optical",
            "FLIR Radiometric LWIR Thermal",
            "LiDAR Surface Deflection Profilometer",
            "Down-Look Sonar Pier Scour Bathymetry"
        ],
        inspection_focus="Fracture-critical member fatigue evaluation, substructure pier concrete spalling, deck delamination, and sub-surface hydrologic pier scour."
    )

    print(f"[+] Staged Lead Mission Docket: {lead_bridge['docket_number']}")
    print(f"    • Asset:     {lead_bridge['asset_name']}")
    print(f"    • Sector:    {lead_bridge['sector_type']}")
    print(f"    • Agency:    {lead_bridge['governing_agency']}")
    print(f"    • Location:  {lead_bridge['location_county']} ({lead_bridge['gps_coordinates']})")
    print(f"    • Status:    {lead_bridge['mission_status']}")
    print(f"    • SHA-256:   {lead_bridge['sha256_docket_seal'][:16]}...")
    print("=" * 90)