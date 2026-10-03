import os
import sys
import subprocess
import json
import cv2

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

print("=" * 80)
print("HVF Omni-Industrial Matrix | OPTICAL DEVICE IDENTIFICATION PROBE")
print("=" * 80)

# 1. Query Windows PnP for Camera & Imaging Device Names
ps_cmd = """
Get-CimInstance Win32_PnPEntity | Where-Object { $_.PNPClass -in @('Camera', 'Image') -and $_.Present -eq $true } | 
Select-Object Name, DeviceID, Manufacturer | ConvertTo-Json -Compress
"""

try:
    proc = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, timeout=20)
    raw_json = proc.stdout.strip()
    cams = json.loads(raw_json) if raw_json else []
    if isinstance(cams, dict):
        cams = [cams]
    print(f"Windows PnP Registered Camera Devices ({len(cams)} Found):")
    for i, c in enumerate(cams, 1):
        print(f"  {i}. {c.get('Name')} | Mfg: {c.get('Manufacturer')}")
        print(f"     ID: {c.get('DeviceID')}")
except Exception as e:
    print(f"[WARN] PnP camera query failed: {e}")

# 2. Probe DirectShow Video Capture Indexes 0 and 1
print("\n" + "-" * 80)
print("PROBING DIRECTSHOW VIDEO STREAMS:")
print("-" * 80)

for idx in [0, 1]:
    cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret and frame is not None:
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out_file = os.path.join(BASE_DIR, f"camera_{idx}_test.jpg")
            cv2.imwrite(out_file, frame)
            print(f"  [SUCCESS] INDEX [{idx}]: Active Stream Verified ({w}x{h}).")
            print(f"            Snapshot written to: {out_file}")
        else:
            print(f"  [WARN] INDEX [{idx}]: Device opened but returned blank frame.")
        cap.release()
    else:
        print(f"  [FAIL] INDEX [{idx}]: Could not open DirectShow video device.")

print("=" * 80)
print("PROBE COMPLETE: INSPECT SNAPSHOTS IN BASE DIRECTORY")
print("=" * 80)

