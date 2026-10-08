"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: SETUP TAPO SENSOR
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import os

    import sys

    import socket

    import subprocess

    import json

    import re

    import cv2



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    CONFIG_FILE = os.path.join(BASE_DIR, "tapo_config.json")



    print("=" * 80)

    print("HVF Omni-Industrial Matrix | TAPO IP CAMERA DISCOVERY PROBE")

    print("=" * 80)



    # 1. Scan ARP Table for local active IP addresses

    arp_output = subprocess.check_output("arp -a", shell=True).decode("utf-8", errors="ignore")

    candidates = []

    for line in arp_output.splitlines():

        match = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]+)\s+dynamic", line)

        if match:

            ip = match.group(1)

            if not ip.endswith(".255") and not ip.startswith("224.") and not ip.startswith("127."):

                candidates.append(ip)



    print(f"Scanning {len(candidates)} local network devices for open RTSP port 554...")

    found_ips = []

    for ip in candidates:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(0.35)

        if s.connect_ex((ip, 554)) == 0:

            found_ips.append(ip)

            print(f"  >>> [TARGET FOUND] Active RTSP stream detected at IP: {ip}")

        s.close()



    target_ip = ""

    if found_ips:

        target_ip = found_ips[0]

        print(f"\nDefaulting to discovered Tapo node: {target_ip}")

    else:

        print("\n[INFO] Auto-discovery did not find an open port 554.")

        target_ip = input("Enter Tapo Camera IP manually (from Tapo app Device Info): ").strip()



    username = input("Enter Tapo Camera Account Username [default: hvf_admin]: ").strip()

    if not username:

        username = "hvf_admin"



    password = input("Enter Tapo Camera Account Password: ").strip()



    # Test RTSP Feed

    rtsp_url = f"rtsp://{username}:{password}@{target_ip}:554/stream1"

    print(f"\nValidating stream connection to {target_ip}:554...")



    cap = cv2.VideoCapture(rtsp_url)

    connected = False

    if cap.isOpened():

        ret, frame = cap.read()

        if ret and frame is not None:

            connected = True

            h, w = frame.shape[:2]

            print(f"[SUCCESS] Tapo Camera Online. Resolution verified: {w}x{h}")

        cap.release()



    config_data = {

        "ip": target_ip,

        "port": 554,

        "username": username,

        "password": password,

        "rtsp_url": rtsp_url,

        "verified": connected

    }



    with open(CONFIG_FILE, "w", encoding="utf-8") as f:

        json.dump(config_data, f, indent=4)



    print(f"[SUCCESS] Configuration saved to: {CONFIG_FILE}")

    print("=" * 80)




if __name__ == "__main__":
    render()
