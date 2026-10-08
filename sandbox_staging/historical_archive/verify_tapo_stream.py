import os
import sys
import json
import socket
import urllib.parse
import cv2

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
CONFIG_PATH = os.path.join(BASE_DIR, "tapo_credentials.json")

TARGET_IP = "192.168.1.165"
TARGET_PORT = 554
USERNAME = "ebony_cam"
RAW_PASSWORD = "Mina@2014"

# Percent-encode '@' to '%40' for standard RFC 2326 URI compliance
ENCODED_PASSWORD = urllib.parse.quote(RAW_PASSWORD, safe="")
RTSP_URL_ENCODED = f"rtsp://{USERNAME}:{ENCODED_PASSWORD}@{TARGET_IP}:{TARGET_PORT}/stream1"
RTSP_URL_RAW = f"rtsp://{USERNAME}:{RAW_PASSWORD}@{TARGET_IP}:{TARGET_PORT}/stream1"

print("=" * 80)
print("HVF Omni-Industrial Matrix | TAPO OPTICAL STREAM INTERROGATION")
print(f"Target Node: {TARGET_IP}:{TARGET_PORT}")
print(f"Service Account: {USERNAME}")
print("=" * 80)

# 1. Audit TCP Socket
print(f"[1/2] Auditing TCP handshake to {TARGET_IP}:{TARGET_PORT}...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3.0)
res = s.connect_ex((TARGET_IP, TARGET_PORT))
s.close()

if res != 0:
    print(f"[FAIL] Port 554 unreachable on {TARGET_IP}. Ensure camera is powered.")
    sys.exit(1)
print(f"[SUCCESS] Port 554 open and reachable.")

# 2. Interrogate RTSP Video Pipeline
print(f"\n[2/2] Connecting to RTSP video pipeline via OpenCV FFmpeg backend...")
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp|analyzeduration;1000000|probesize;1000000"

verified_url = None
for test_url, label in [(RTSP_URL_ENCODED, "URI-Encoded"), (RTSP_URL_RAW, "Raw-URI")]:
    print(f"  * Testing handshake via {label} endpoint...")
    cap = cv2.VideoCapture(test_url, cv2.CAP_FFMPEG)
    if cap.isOpened():
        ret, frame = cap.read()
        cap.release()
        if ret and frame is not None:
            h, w = frame.shape[:2]
            print(f"[SUCCESS] Tapo Optical Stream Verified via {label}. Resolution: {w}x{h}")
            verified_url = test_url
            break

if not verified_url:
    print("[FAIL] Handshake failed on both endpoint variants. Verify camera password in Tapo app.")
    sys.exit(1)

# 3. Write Verified Configuration to Disk
cfg_data = {
    "camera_ip": TARGET_IP,
    "port": TARGET_PORT,
    "username": USERNAME,
    "password": RAW_PASSWORD,
    "rtsp_url": verified_url,
    "resolution": f"{w}x{h}",
    "status": "VERIFIED_ONLINE"
}

with open(CONFIG_PATH, "w", encoding="utf-8") as f:
    json.dump(cfg_data, f, indent=4)

print(f"[SUCCESS] Validated configuration committed to: {CONFIG_PATH}")
print("=" * 80)

