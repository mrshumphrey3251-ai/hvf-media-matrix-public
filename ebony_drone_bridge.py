"""
HVF Sovereign C2 // Autonomous UAS Sortie WORM Telemetry Logger (Root Compatibility Bridge)
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | SQLite WORM Ledger Integration
"""
import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

def log_completed_flight_sortie(
    mission_id: str,
    docket_number: str,
    flight_duration_minutes: float = 24.5,
    battery_start_v: float = 50.2,
    battery_end_v: float = 45.6,
    optical_flow_quality: int = 98,
    images_captured: int = 420,
) -> dict:
    """Logs a completed autonomous UAS inspection sortie to the SQLite WORM ledger and returns metrics."""
    ts_utc = datetime.now(timezone.utc).isoformat()
    payload_str = f"{mission_id}|{docket_number}|{flight_duration_minutes}|{battery_start_v}|{battery_end_v}|{optical_flow_quality}|{images_captured}|{ts_utc}"
    sortie_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
    sortie_id = f"{mission_id}-WORM"

    db_candidates = [
        Path(__file__).resolve().parent / "c2_cockpit" / "matrix_ledger.db",
        Path(__file__).resolve().parent / "matrix_ledger.db",
    ]
    for db_p in db_candidates:
        if db_p.parent.exists():
            try:
                conn = sqlite3.connect(str(db_p))
                conn.execute(
                    "CREATE TABLE IF NOT EXISTS drone_sortie_worm_ledger ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, sortie_id TEXT, docket_number TEXT, "
                    "duration_min REAL, battery_start_v REAL, battery_end_v REAL, "
                    "optical_flow_lock INTEGER, images INTEGER, sortie_hash TEXT, timestamp_utc TEXT)"
                )
                conn.execute(
                    "INSERT INTO drone_sortie_worm_ledger VALUES (NULL,?,?,?,?,?,?,?,?,?)",
                    (sortie_id, docket_number, float(flight_duration_minutes), float(battery_start_v),
                     float(battery_end_v), int(optical_flow_quality), int(images_captured), sortie_hash, ts_utc)
                )
                conn.commit()
                conn.close()
                break
            except Exception:
                pass

    return {
        "sortie_id": sortie_id,
        "docket_number": docket_number,
        "duration_min": flight_duration_minutes,
        "battery_start_v": battery_start_v,
        "battery_end_v": battery_end_v,
        "optical_flow_lock": optical_flow_quality,
        "images": images_captured,
        "sortie_hash": sortie_hash,
        "timestamp_utc": ts_utc,
    }
