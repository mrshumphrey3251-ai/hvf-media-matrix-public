import json
from datetime import datetime, timezone

def simulate_drone_stream():
    print("Initializing Drone RGB Adapter...")
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sensor_id": "drone_alpha_01",
        "metrics": {"R": 110.5, "G": 145.2, "B": 75.8, "dielectric_moisture": 22.4}
    }
    print(f"Routing to ingestion matrix: {json.dumps(payload)}")

if __name__ == '__main__':
    simulate_drone_stream()
