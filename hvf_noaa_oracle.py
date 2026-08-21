import os
import json
import sqlite3
import requests
from datetime import datetime
from dotenv import load_dotenv

# 1. Configuration & Persistence
load_dotenv(override=True)
DB_PATH = os.path.abspath(r"C:\HVF_Repos\hvf-media-matrix-private\hvf_memory_vault.db")

# Default Location: Hinton / Caddo / Kingfisher County Region (Lat: 35.47, Lon: -98.35)
DEFAULT_LAT = os.getenv("HVF_LATITUDE", "35.47")
DEFAULT_LON = os.getenv("HVF_LONGITUDE", "-98.35")
USER_AGENT = "HumphreyVirtualFarm/2026.1 (humphreyvirtualfarm@gmail.com)"

class NOAAWeatherOracle:
    """
    Sovereign NOAA NWS Active Alert & Live Radar Telemetry Engine.
    Queries official National Weather Service API endpoints for active warnings.
    """
    def __init__(self, lat=DEFAULT_LAT, lon=DEFAULT_LON):
        self.lat = lat
        self.lon = lon
        self.headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
        self._init_vault()

    def _init_vault(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS weather_alerts_vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_id TEXT UNIQUE NOT NULL,
                event TEXT NOT NULL,
                severity TEXT NOT NULL,
                headline TEXT,
                description TEXT,
                instruction TEXT,
                area_desc TEXT,
                effective TEXT,
                expires TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def fetch_active_alerts(self):
        """Fetches active NOAA weather alerts for the specified coordinates."""
        url = f"https://api.weather.gov/alerts/active?point={self.lat},{self.lon}"
        try:
            resp = requests.get(url, headers=self.headers, timeout=8)
            if resp.status_code != 200:
                # Fallback to Oklahoma state-wide active query
                url = "https://api.weather.gov/alerts/active?area=OK"
                resp = requests.get(url, headers=self.headers, timeout=8)

            data = resp.json()
            features = data.get("features", [])
            
            active_alerts = []
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            for f in features:
                props = f.get("properties", {})
                alert_id = props.get("id", "")
                event = props.get("event", "Weather Alert")
                severity = props.get("severity", "Unknown")
                headline = props.get("headline", "")
                description = props.get("description", "")
                instruction = props.get("instruction", "")
                area_desc = props.get("areaDesc", "")
                effective = props.get("effective", "")
                expires = props.get("expires", "")

                # Store in SQLite vault
                try:
                    cur.execute("""
                        INSERT OR REPLACE INTO weather_alerts_vault 
                        (alert_id, event, severity, headline, description, instruction, area_desc, effective, expires)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (alert_id, event, severity, headline, description, instruction, area_desc, effective, expires))
                except Exception:
                    pass

                active_alerts.append({
                    "id": alert_id,
                    "event": event,
                    "severity": severity,
                    "headline": headline,
                    "description": description,
                    "instruction": instruction,
                    "area": area_desc,
                    "expires": expires
                })

            conn.commit()
            conn.close()
            return active_alerts
        except Exception as e:
            return [{"event": "NWS Link Offline", "severity": "Unknown", "headline": f"NOAA query error: {str(e)}", "description": "", "instruction": "", "area": "", "expires": ""}]

if __name__ == "__main__":
    oracle = NOAAWeatherOracle()
    alerts = oracle.fetch_active_alerts()
    print(f"\n--- NOAA Active Emergency Weather Alerts ({len(alerts)} Active) ---")
    for a in alerts:
        print(f"[{a['severity'].upper()}] {a['event']}: {a['headline']}")
        if a['instruction']:
            print(f"Action: {a['instruction'][:200]}...")