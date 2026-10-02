import json
import requests
from datetime import datetime, timezone

class EbonyEdgeClient:
    def __init__(self, endpoint_url: str, api_key: str):
        self.endpoint = endpoint_url
        self.headers = {
            "Authorization": f"Bearer {api_key}", 
            "Content-Type": "application/json"
        }

    def push_telemetry(self, sensor_id: str, r: float, g: float, b: float, moisture: float):
        """
        Packages RGB and dielectric moisture payloads for automated routing 
        to the Ebony unified data ingestion layer.
        """
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sensor_id": sensor_id,
            "metrics": {
                "R": r, 
                "G": g, 
                "B": b, 
                "dielectric_moisture": moisture
            }
        }
        
        # Executes secure push to the ingest endpoint
        response = requests.post(f"{self.endpoint}/ingest", headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    print("HVF Executive Command: Python Edge-Device SDK Initialized for Q1 Deployment.")
