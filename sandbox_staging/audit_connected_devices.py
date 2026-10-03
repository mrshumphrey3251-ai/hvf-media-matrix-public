import os
import sys
import subprocess
import json
import re

print("=" * 90)
print("HVF Omni-Industrial Matrix | SOVEREIGN HARDWARE INTERROGATION AUDIT")
print("Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)")
print("=" * 90)

# 1. Interrogate Windows PnP Entity Tree via PowerShell CIM
ps_cmd = """
Get-CimInstance Win32_PnPEntity | Where-Object { $_.Present -eq $true } | 
Select-Object Name, DeviceID, PNPClass, Manufacturer, Status | 
ConvertTo-Json -Compress
"""

try:
    proc = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, timeout=30)
    raw_json = proc.stdout.strip()
    devices = json.loads(raw_json) if raw_json else []
except Exception as e:
    print(f"[ERROR] Failed to query PnP Entity tree: {e}")
    devices = []

# Categorization buckets
categories = {
    "CAMERAS & IMAGING DEVICES": [],
    "PORTS (COM & SERIAL)": [],
    "USB CONTROLLERS & PERIPHERALS": [],
    "AUDIO & MEDIA CONTROLLERS": [],
    "NETWORK ADAPTERS": [],
    "OTHER CONNECTED PNP HARDWARE": []
}

for dev in devices:
    pnp_class = str(dev.get("PNPClass", "")).upper()
    name = str(dev.get("Name", "Unknown Device"))
    dev_id = str(dev.get("DeviceID", ""))
    mfg = str(dev.get("Manufacturer", "Generic"))
    status = str(dev.get("Status", "OK"))

    entry = {"Name": name, "DeviceID": dev_id, "Manufacturer": mfg, "Status": status}

    if pnp_class in ["CAMERA", "IMAGE"]:
        categories["CAMERAS & IMAGING DEVICES"].append(entry)
    elif pnp_class in ["PORTS"]:
        categories["PORTS (COM & SERIAL)"].append(entry)
    elif "USB" in dev_id or pnp_class in ["USB"]:
        categories["USB CONTROLLERS & PERIPHERALS"].append(entry)
    elif pnp_class in ["MEDIA", "AUDIOENDPOINT"]:
        categories["AUDIO & MEDIA CONTROLLERS"].append(entry)
    elif pnp_class in ["NET"]:
        categories["NETWORK ADAPTERS"].append(entry)
    else:
        if any(keyword in name.lower() for keyword in ["tapo", "camera", "video", "tp-link"]):
            categories["CAMERAS & IMAGING DEVICES"].append(entry)

# Print Classified Results
for cat_name, items in categories.items():
    if not items:
        continue
    print(f"\n[+] {cat_name} ({len(items)} Detected):")
    print("-" * 90)
    for idx, item in enumerate(items, 1):
        name = item["Name"]
        dev_id = item["DeviceID"]
        mfg = item["Manufacturer"]
        print(f"  {idx:2d}. {name:<45} | Mfg: {mfg}")
        print(f"      Hardware ID: {dev_id}")
    print("-" * 90)

# 2. Check DirectShow Hardware Video Capture Indices
print("\n[+] DIRECTSHOW VIDEO CAPTURE INDEX PROBE:")
print("-" * 90)
try:
    import cv2
    opened_cams = []
    for idx in range(6):
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                opened_cams.append((idx, w, h))
            cap.release()
    if opened_cams:
        for cam in opened_cams:
            print(f"  >>> DirectShow Video Device active at INDEX [{cam[0]}] - Resolution: {cam[1]}x{cam[2]}")
    else:
        print("  [INFO] Zero active DirectShow UVC video streams detected.")
except ImportError:
    print("  [INFO] opencv-python not installed. DirectShow frame probe skipped.")

print("=" * 90)
print("AUDIT COMPLETE")
print("=" * 90)

