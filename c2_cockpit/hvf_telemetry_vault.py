"""
=============================================================================
HVF MEDIA MATRIX : TELEMETRY VAULT ROUTER (TARGET CHARLIE)
CLASSIFICATION   : PRIVATE_UNREDACTED
VERSION          : 1.0.1 (PATCHED)
AUTHOR           : JEFFERY HUMPHREY (CEO / FOUNDER)
=============================================================================
DIRECTIVE:
Intercepts live GLI (Green Leaf Index) scores and environmental telemetry,
cryptographically hashes the payload for immutability, and permanently 
writes it to the sovereign time-series ledger for predictive AI analysis.
=============================================================================
"""

import os
import sqlite3
import hashlib
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TELEMETRY_DB = os.path.join(BASE_DIR, "hvf_telemetry_ledger.db")

def ensure_telemetry_ledger():
    """Initializes the secure SQL ledger for all incoming field telemetry."""
    conn = sqlite3.connect(TELEMETRY_DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS gli_time_series (
            telemetry_id TEXT PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            farm_sector TEXT NOT NULL,
            gli_score REAL NOT NULL,
            health_status TEXT NOT NULL,
            cryptographic_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def generate_telemetry_hash(sector: str, gli: float, timestamp: str) -> str:
    """Generates an immutable cryptographic hash of the sensor reading."""
    raw_payload = f"{sector}|{gli}|{timestamp}|HVF_SENSOR_ROOT"
    return hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()

def ingest_gli_telemetry(farm_sector: str, gli_score: float):
    """
    Ingests live GLI data, categorizes crop health, and locks it into the vault.
    """
    ensure_telemetry_ledger()
    
    # omni-industrial Baseline Categorization
    if gli_score >= 0.15:
        health_status = "OPTIMAL_VIGOR"
    elif 0.05 <= gli_score < 0.15:
        health_status = "MODERATE_STRESS"
    else:
        health_status = "CRITICAL_DEGRADATION"

    timestamp = datetime.utcnow().isoformat()
    tel_hash = generate_telemetry_hash(farm_sector, gli_score, timestamp)
    tel_id = f"TEL-{tel_hash[:12].upper()}"

    # Log to Sovereign Telemetry Database (PATCHED: Farm Sector injected)
    conn = sqlite3.connect(TELEMETRY_DB)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO gli_time_series (telemetry_id, timestamp, farm_sector, gli_score, health_status, cryptographic_hash) VALUES (?, ?, ?, ?, ?, ?)",
        (tel_id, timestamp, farm_sector, float(gli_score), health_status, tel_hash)
    )
    conn.commit()
    conn.close()

    # Generate Executive Telemetry Receipt
    receipt = {
        "TELEMETRY_ID": tel_id,
        "STATUS": "LOGGED & SECURED",
        "SECTOR": farm_sector,
        "GLI_SCORE": round(gli_score, 3),
        "ASSESSMENT": health_status,
        "HASH": tel_hash
    }
    
    return receipt

if __name__ == "__main__":
    # Internal Diagnostic Test
    print("==================================================")
    print(" HVF TELEMETRY VAULT ROUTER : DIAGNOSTIC TEST RUN")
    print("==================================================")
    
    test_sector = "SECTOR_7G_NORTH_FIELD"
    test_gli = 0.185  # Simulating a healthy crop reading
    
    print(f"Simulating Optical Ingest -> Sector: {test_sector} | GLI: {test_gli}")
    result = ingest_gli_telemetry(test_sector, test_gli)
    print(json.dumps(result, indent=4))
    print("==================================================")
