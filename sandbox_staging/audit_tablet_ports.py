"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: AUDIT TABLET PORTS
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import os

    import sys

    import json

    import socket

    import cv2



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    CONFIG_FILE = os.path.join(BASE_DIR, "tablet_config.json")

    TAILSCALE_IP = "100.65.79.106"

    PORT = 4747



    print("=" * 80)

    print("HVF Omni-Industrial Matrix | DROIDCAM MULTI-INTERFACE PROBE")

    print("Target Node: Samsung Galaxy Tab Active5 (SM-X300)")

    print("=" * 80)



    def test_socket(ip, port):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(2.5)

        result = s.connect_ex((ip, port))

        s.close()

        return result == 0



    # 1. Test Tailscale Interface

    print(f"[1/3] Testing Tailscale WireGuard socket at {TAILSCALE_IP}:{PORT}...")

    target_ip = None

    if test_socket(TAILSCALE_IP, PORT):

        print(f"  >>> [SUCCESS] Tailscale port 4747 is open.")

        target_ip = TAILSCALE_IP

    else:

        print(f"  >>> [REFUSED] Port 4747 not answering on Tailscale IP {TAILSCALE_IP}.")

        print("      DroidCam is likely bound to the tablet's physical Wi-Fi interface.")



    # 2. Test Local Wi-Fi Interface if Tailscale refused

    if not target_ip:

        print("\n[2/3] Checking tablet physical Wi-Fi IP address...")

        wifi_ip = input("Enter the 'WiFi IP' displayed on your Galaxy Tab Active5 screen: ").strip()

        if wifi_ip:

            if test_socket(wifi_ip, PORT):

                print(f"  >>> [SUCCESS] Physical Wi-Fi port 4747 is open on {wifi_ip}.")

                target_ip = wifi_ip

            else:

                print(f"  >>> [FAIL] Could not connect to {wifi_ip}:{PORT}. Ensure DroidCam is running.")

                sys.exit(1)

        else:

            print("[FAIL] No IP provided. Aborting probe.")

            sys.exit(1)



    # 3. Validate OpenCV Stream Acquisition

    print(f"\n[3/3] Validating video frame acquisition from http://{target_ip}:{PORT}/video...")

    stream_url = f"http://{target_ip}:{PORT}/video"

    cap = cv2.VideoCapture(stream_url)



    if not cap.isOpened():

        # Fallback endpoint for DroidCam

        stream_url = f"http://{target_ip}:{PORT}/mjpegfeed"

        cap = cv2.VideoCapture(stream_url)



    if not cap.isOpened():

        print(f"[FAIL] OpenCV could not bind to DroidCam video pipeline at: {stream_url}")

        sys.exit(1)



    ret, frame = cap.read()

    cap.release()



    if not ret or frame is None:

        print("[FAIL] Socket open, but failed to extract active video frame.")

        sys.exit(1)



    h, w = frame.shape[:2]

    print(f"[SUCCESS] Optical Feed Verified. Resolution: {w}x{h}")



    # Save working configuration

    cfg_data = {

        "device_model": "Samsung Galaxy Tab Active5 (SM-X300)",

        "app_engine": "DroidCam_Dev47Apps",

        "active_ip": target_ip,

        "port": PORT,

        "full_url": stream_url,

        "resolution": f"{w}x{h}",

        "status": "VERIFIED_ONLINE"

    }



    with open(CONFIG_FILE, "w", encoding="utf-8") as f:

        json.dump(cfg_data, f, indent=4)



    print(f"[SUCCESS] Operational route saved to: {CONFIG_FILE}")

    print("=" * 80)




if __name__ == "__main__":
    render()
