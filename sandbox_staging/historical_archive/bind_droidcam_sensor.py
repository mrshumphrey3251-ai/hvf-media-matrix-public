import os
import sys
import json
import socket
import cv2

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
CONFIG_FILE = os.path.join(BASE_DIR, "tablet_config.json")
TABLET_IP = "100.65.79.106"
TABLET_PORT = 4747
STREAM_URL = f"http://{TABLET_IP}:{TABLET_PORT}/video"

print("=" * 80)
print("HVF Omni-Industrial Matrix | DROIDCAM TABLET OPTICAL INTERROGATION")
print(f"Target: Samsung Galaxy Tab Active5 (SM-X300) at {STREAM_URL}")
print("=" * 80)

# 1. Audit TCP Socket on Port 4747
print(f"[1/2] Auditing Tailscale route to {TABLET_IP}:{TABLET_PORT}...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3.0)
res = s.connect_ex((TABLET_IP, TABLET_PORT))
s.close()

if res != 0:
    print(f"[FAIL] Could not connect to {TABLET_IP}:{TABLET_PORT}. Result code: {res}")
    print("Ensure DroidCam is open and active on the Galaxy Tab Active5.")
    sys.exit(1)
print(f"[SUCCESS] Tailscale Port 4747 TCP route open and verified.")

# 2. Interrogate MJPEG Video Pipeline
print(f"\n[2/2] Interrogating DroidCam MJPEG video pipeline at {STREAM_URL}...")
cap = cv2.VideoCapture(STREAM_URL)
if not cap.isOpened():
    print(f"[FAIL] OpenCV could not bind to stream at: {STREAM_URL}")
    sys.exit(1)

ret, frame = cap.read()
cap.release()

if not ret or frame is None:
    print("[FAIL] Socket open, but failed to extract active video frame.")
    sys.exit(1)

h, w = frame.shape[:2]
print(f"[SUCCESS] Galaxy Tab Active5 Optical Feed Verified. Resolution: {w}x{h}")

# 3. Write Verified Configuration to Disk
cfg_data = {
    "device_model": "Samsung Galaxy Tab Active5 (SM-X300)",
    "app_engine": "DroidCam_Dev47Apps",
    "tailscale_ip": TABLET_IP,
    "port": TABLET_PORT,
    "stream_path": "/video",
    "full_url": STREAM_URL,
    "resolution": f"{w}x{h}",
    "status": "VERIFIED_ONLINE"
}

with open(CONFIG_FILE, "w", encoding="utf-8") as f:
    json.dump(cfg_data, f, indent=4)

print(f"[SUCCESS] Configuration committed to: {CONFIG_FILE}")
print("=" * 80)

