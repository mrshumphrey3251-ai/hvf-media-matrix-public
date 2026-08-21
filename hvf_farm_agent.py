import os
import json
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# 1. Sovereign Configuration
load_dotenv(override=True)
GROQ_KEY = os.getenv("GROQ_API_KEY")
ACTIVE_MODEL = "openai/gpt-oss-120b"
DB_PATH = os.path.abspath(r"C:\HVF_Repos\hvf-media-matrix-private\hvf_memory_vault.db")

class HVFFarmAgent:
    """
    Sovereign Agronomy & Sensor-Fusion Agent
    Orchestrates real-time telemetry, offline RAG memory, and local agronomic decision loops.
    """
    def __init__(self):
        self.client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None
        self._init_sensor_vault()

    def _init_sensor_vault(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS iot_telemetry_vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id TEXT NOT NULL,
                zone_id TEXT NOT NULL,
                soil_moisture REAL,
                temp_c REAL,
                humidity REAL,
                raw_payload TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def ingest_telemetry(self, sensor_id: str, zone_id: str, soil_moisture: float, temp_c: float, humidity: float, extra_data: dict = None):
        """Persists IoT sensor streams into the sovereign vault."""
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO iot_telemetry_vault (sensor_id, zone_id, soil_moisture, temp_c, humidity, raw_payload)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (sensor_id, zone_id, soil_moisture, temp_c, humidity, json.dumps(extra_data or {})))
        conn.commit()
        conn.close()
        print(f"[HVF TELEMETRY]: Ingested reading for {sensor_id} in {zone_id}.")

    def diagnose_zone(self, zone_id: str, question: str) -> str:
        """RAG-augmented reasoning over recent IoT sensor streams."""
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            SELECT sensor_id, soil_moisture, temp_c, humidity, recorded_at 
            FROM iot_telemetry_vault 
            WHERE zone_id=? 
            ORDER BY id DESC LIMIT 5
        """, (zone_id,))
        readings = cur.fetchall()
        conn.close()

        context_str = "\n".join([
            f"- Sensor: {r[0]} | Moisture: {r[1]}% | Temp: {r[2]}C | Humidity: {r[3]}% | Timestamp: {r[4]}"
            for r in readings
        ]) if readings else "No telemetry recorded for this zone yet."

        system_prompt = f"""
You are the HVF Sovereign Agronomy Diagnostic Engine for Humphrey Virtual Farm.
Active Knowledge: Agronomy, Irrigation Optimization, Soil Chemistry, and Climate Resilience.

LIVE TELEMETRY CONTEXT (ZONE {zone_id}):
{context_str}

Provide a concise, decisive executive recommendation based strictly on data.
"""
        if not self.client:
            return "Groq Neural Link offline."

        response = self.client.chat.completions.create(
            model=ACTIVE_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    agent = HVFFarmAgent()
    # Sample Test Telemetry Ingestion
    agent.ingest_telemetry("SOIL-Z1-001", "ZONE-1-NORTH", soil_moisture=21.4, temp_c=27.5, humidity=48.0)
    print("\n--- Diagnostic Output ---")
    print(agent.diagnose_zone("ZONE-1-NORTH", "Is automated irrigation recommended for Zone 1 right now?"))