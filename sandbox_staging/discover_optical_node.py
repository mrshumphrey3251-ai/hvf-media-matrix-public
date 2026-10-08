"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: DISCOVER OPTICAL NODE
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

    import re



    print("=" * 80)

    print("HVF Omni-Industrial Matrix | OPTICAL FEED HARDWARE & NETWORK AUDIT")

    print("=" * 80)



    # 1. Audit DirectShow / USB Capture Devices

    print("[1/2] Auditing direct USB video capture interfaces...")

    try:

        import cv2

        usb_found = []

        for idx in range(4):

            cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)

            if cap.isOpened():

                ret, _ = cap.read()

                if ret:

                    usb_found.append(idx)

                cap.release()

        if usb_found:

            print(f"  [SUCCESS] Detected {len(usb_found)} direct USB video device(s) at index: {usb_found}")

        else:

            print("  [INFO] No direct USB UVC video capture devices detected on host.")

    except ImportError:

        print("  [WARN] opencv-python not installed. Skipping direct DirectShow check.")



    # 2. Subnet Audit for Tapo IP & Port 554 (RTSP)

    print("\n[2/2] Scanning local ARP table and network sockets for Tapo/RTSP nodes...")

    try:

        arp_output = subprocess.check_output("arp -a", shell=True).decode("utf-8", errors="ignore")

        lines = arp_output.splitlines()

        candidates = []



        for line in lines:

            match = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]+)\s+dynamic", line)

            if match:

                ip, mac = match.group(1), match.group(2)

                if not ip.endswith(".255") and not ip.startswith("224.") and not ip.startswith("239."):

                    candidates.append((ip, mac))



        print(f"  Probing {len(candidates)} active network endpoints for RTSP (Port 554)...")

        found_rtsp = []

        for ip, mac in candidates:

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            s.settimeout(0.3)

            result = s.connect_ex((ip, 554))

            if result == 0:

                found_rtsp.append((ip, mac))

                print(f"  >>> [TARGET IDENTIFIED] RTSP Optical Stream open at IP: {ip} (MAC: {mac})")

            s.close()



        if not found_rtsp:

            print("  [INFO] No open RTSP port 554 detected yet.")

            print("  Ensure camera is powered on and connected to the same Wi-Fi/Ethernet network.")

        else:

            print(f"\n[SUCCESS] Discovered {len(found_rtsp)} active optical node(s) available for ingest.")

    except Exception as e:

        print(f"  [ERROR] Network probe failed: {e}")



    print("=" * 80)




if __name__ == "__main__":
    render()
