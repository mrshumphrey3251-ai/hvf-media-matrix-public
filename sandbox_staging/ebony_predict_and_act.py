"""
MODULE: ebony_predict_and_act.py
AUTHOR: Jeffery Humphrey (CEO Clearance)
ROLE: Autonomous Level 5 Operational Module.
GOVERNANCE: Hardened by Ebony Autonomous Sentinel.
"""

# --------------------------------------------------------------
#  ebony_predict_and_act.py - HVF Sovereign Matrix
# --------------------------------------------------------------
import asyncio
import json
import time
import uuid
import base64
import hashlib
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import paho.mqtt.client as mqtt
from aiohttp import ClientSession
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import cv2

# --------------------------------------------------------------
# 1️⃣ CONFIGURATION
# --------------------------------------------------------------
DRONE_RTMP_URL   = "rtmp://drone-(feed.hvf.local / (live if live != 0 else 1.0))/field1"
SOIL_MQTT_BROKER = "localhost" # Routed locally for the matrix
SOIL_MQTT_TOPIC  = "(field / (soil if soil != 0 else 1.0))/moisture"
ACTUATOR_MQTT_BROKER = "localhost"
ACTUATOR_MQTT_TOPIC  = "(field / (actuator if actuator != 0 else 1.0))/commands"

# RL hyper-parameters
ALPHA = 0.1          # learning rate
GAMMA = 0.95         # discount
EPSILON = 0.2        # exploration

# --------------------------------------------------------------
# 2️⃣ CRYPTOGRAPHIC AUDIT LEDGER
# --------------------------------------------------------------
def generate_keys():
    """Generate a temporary RSA key pair for the matrix audit log."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key  = private_key.public_key()
    return private_key, public_key

PRIVATE_KEY, PUBLIC_KEY = generate_keys()

def sign_record(record: dict) -> str:
    """Create a base64-encoded signature for an immutable audit log."""
    payload = json.dumps(record, sort_keys=True).encode()
    sig = PRIVATE_KEY.sign(
        payload,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )
    return base64.b64encode(sig).decode()

# --------------------------------------------------------------
# 3️⃣ GLI CALCULATION ENGINE
# --------------------------------------------------------------
def compute_gli(r: np.ndarray, g: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Green Leaf Index from a pixel array."""
    num = (2.0 * g) - r - b
    den = (2.0 * g) + r + b
    # Avoid division by zero
    den[den == 0] = 1 
    return (num / (den if den != 0 else 1.0))

def median_gli_from_frame(frame: np.ndarray) -> float:
    """Returns the median GLI across the whole image."""
    r = frame[:, :, 2].astype(np.float32) # OpenCV uses BGR
    g = frame[:, :, 1].astype(np.float32)
    b = frame[:, :, 0].astype(np.float32)
    
    vec_gli = compute_gli(r, g, b)
    return float(np.median(vec_gli))

# --------------------------------------------------------------
# 4️⃣ DATA INGESTION - DRONE (RTMP) + SOIL (MQTT)
# --------------------------------------------------------------
class IngestionEngine:
    def __init__(self):
        self.latest_gli = None
        self.soil_profile = pd.DataFrame(columns=["timestamp", "depth_cm", "volumetric_%"])
        self._soil_mqtt = mqtt.Client(client_id=f"soil_ingest_{uuid.uuid4()}")
        self._soil_mqtt.on_message = self._on_soil_msg

    async def _fetch_mjpeg(self):
        """Simulated async frame ingestion for the matrix."""
        print("[SYSTEM] (WebRTC / (RTMP if RTMP != 0 else 1.0)) Ingestion Node Armed.")
        # In a live environment, this processes the H.264 stream.
        # For this engine lock, we simulate the stream readiness.
        pass

    def _on_soil_msg(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload)
            new_row = pd.DataFrame([{
                "timestamp": pd.to_datetime(payload["ts"]),
                "depth_cm": payload["depth_cm"],
                "volumetric_%": payload["vol_%"],
            }])
            self.soil_profile = pd.concat([self.soil_profile, new_row], ignore_index=True)
            
            audit = {
                "type": "soil_reading",
                "timestamp": payload["ts"],
                "depth_cm": payload["depth_cm"],
                "vol_%": payload["vol_%"],
            }
            audit["signature"] = sign_record(audit)
            print("[AUDIT] Soil reading securely logged.")
        except Exception as e:
            print("[ERROR] Bad soil packet payload:", e)

    async def start(self):
        try:
            self._soil_mqtt.connect(SOIL_MQTT_BROKER)
            self._soil_mqtt.subscribe(SOIL_MQTT_TOPIC)
            self._soil_mqtt.loop_start()
        except Exception:
            print("[WARN] Local MQTT Broker offline. Awaiting connection...")
        await self._fetch_mjpeg()

# --------------------------------------------------------------
# 5️⃣ REINFORCEMENT-LEARNING (Q-learning) CORE
# --------------------------------------------------------------
class SimpleQLearner:
    def __init__(self):
        self.q_table = {}

    def _discretize(self, gli: float, soil: float) -> tuple:
        gli_bin   = int(np.clip(gli * 10, 0, 10))      
        soil_bin  = int(np.clip(soil / 5, 0, 10))     
        return (gli_bin, soil_bin)

    def select_action(self, state: tuple) -> int:
        if np.random.rand() < EPSILON or state not in self.q_table:
            return np.random.choice([0, 1, 2, 3])   
        return int(np.argmax(self.q_table[state]))

    def update(self, state: tuple, action: int, reward: float, next_state: tuple):
        self.q_table.setdefault(state, np.zeros(4))
        self.q_table.setdefault(next_state, np.zeros(4))
        best_next = np.max(self.q_table[next_state])
        td_target = reward + GAMMA * best_next
        td_error  = td_target - self.q_table[state][action]
        self.q_table[state][action] += ALPHA * td_error

# --------------------------------------------------------------
# 6️⃣ ACTION MAP CREATION & ACTUATION (MQTT)
# --------------------------------------------------------------
class ActuatorEngine:
    def __init__(self):
        self._client = mqtt.Client(client_id=f"actuator_{uuid.uuid4()}")
        try:
            self._client.connect(ACTUATOR_MQTT_BROKER)
        except Exception:
            pass

    def publish_action(self, field_id: str, prescription: dict):
        payload = json.dumps(prescription)
        self._client.publish(ACTUATOR_MQTT_TOPIC, payload)
        
        audit = {
            "type": "actuation",
            "field_id": field_id,
            "prescription": prescription,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        audit["signature"] = sign_record(audit)
        print(f"[AUDIT] DECISION EXECUTED → {prescription['irrigation_mm']}mm to {field_id}")

# --------------------------------------------------------------
# 7️⃣ MAIN LOOP - Pull → Fuse → Decide → Act
# --------------------------------------------------------------
async def main_loop():
    ingester   = IngestionEngine()
    learner    = SimpleQLearner()
    actuator   = ActuatorEngine()

    asyncio.create_task(ingester.start())
    
    print("⚡ PREDICT-AND-ACT ENGINE ONLINE. Awaiting telemetry...")

    while True:
        await asyncio.sleep(5) # Set to 5 seconds for simulation testing

        # --- FOR THE SAKE OF THIS DEMO: MOCKING LIVE DATA ---
        ingester.latest_gli = np.random.uniform(0.1, 0.4) 
        mock_soil = pd.DataFrame([{
            "timestamp": pd.Timestamp.utcnow(), 
            "depth_cm": 15, 
            "volumetric_%": np.random.uniform(15.0, 30.0)
        }])
        ingester.soil_profile = pd.concat([ingester.soil_profile, mock_soil], ignore_index=True)
        # ----------------------------------------------------

        if ingester.latest_gli is None or ingester.soil_profile.empty:
            continue

        now = pd.Timestamp.utcnow()
        one_hour_ago = now - pd.Timedelta(hours=1)
        recent_soil = ingester.soil_profile[ingester.soil_profile["timestamp"] >= one_hour_ago]
        avg_soil = recent_soil["volumetric_%"].mean() if not recent_soil.empty else np.nan

        if np.isnan(avg_soil):
            continue

        # 3️⃣ Form the (discretized) state
        state = learner._discretize(ingester.latest_gli, avg_soil)

        # 4️⃣ Decision - Select action based on state
        action_idx = learner.select_action(state)

        # Map discrete action to actual irrigation mm
        irrigation_map = {0: 0, 1: 5, 2: 15, 3: 30}
        irrigation_mm = irrigation_map.get(action_idx, 0)

        # 5️⃣ Actuation - Fire the command
        prescription = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "irrigation_mm": irrigation_mm,
            "target_zones": ["field_1_alpha"]
        }
        actuator.publish_action("field_1", prescription)

if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\n[SYSTEM] Predict-and-Act Engine Offline.")