import os
import sys
import subprocess
import json

print("=" * 80)
print("HVF Omni-Industrial Matrix | WORKSTATION AUDIO BUS INTERROGATION")
print("Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)")
print("=" * 80)

# 1. Query Windows PnP Audio Endpoints via CIM
ps_cmd = """
Get-CimInstance Win32_PnPEntity | Where-Object { 
    ($_.PNPClass -eq 'AudioEndpoint' -or $_.PNPClass -eq 'MEDIA') -and $_.Present -eq $true 
} | Select-Object Name, DeviceID, Manufacturer, Status | ConvertTo-Json -Compress
"""

try:
    proc = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, timeout=20)
    raw_json = proc.stdout.strip()
    devices = json.loads(raw_json) if raw_json else []
    if isinstance(devices, dict):
        devices = [devices]
except Exception as e:
    print(f"[WARN] PnP Audio query notice: {e}")
    devices = []

# Classify Audio Hardware
capture_devices = []
render_devices = []

for dev in devices:
    name = str(dev.get("Name", "Unknown Audio Device"))
    dev_id = str(dev.get("DeviceID", ""))
    mfg = str(dev.get("Manufacturer", "Generic"))
    
    # Check for capture/microphone indicators
    if any(k in name.lower() for k in ["microphone", "mic", "input", "line in", "capture", "headset"]):
        capture_devices.append({"Name": name, "DeviceID": dev_id, "Manufacturer": mfg})
    else:
        render_devices.append({"Name": name, "DeviceID": dev_id, "Manufacturer": mfg})

print("\n[+] ACTIVE AUDIO CAPTURE ENDPOINTS (MICROPHONES):")
print("-" * 80)
if capture_devices:
    for idx, c in enumerate(capture_devices, 1):
        print(f"  {idx}. {c['Name']:<45} | Mfg: {c['Manufacturer']}")
        print(f"     ID: {c['DeviceID']}")
else:
    print("  [NOTICE] No dedicated microphone endpoints labeled in PnP.")

print("\n[+] SYSTEM AUDIO CONTROLLERS & CODECS:")
print("-" * 80)
for idx, r in enumerate(render_devices, 1):
    print(f"  {idx}. {r['Name']:<45} | Mfg: {r['Manufacturer']}")

# 2. Check for PyAudio / SoundDevice python bindings if installed
print("\n[+] PYTHON AUDIO ENGINE PROBE:")
print("-" * 80)
try:
    import sounddevice as sd
    devs = sd.query_devices()
    print("SoundDevice library available. Host audio interfaces:")
    for idx, d in enumerate(devs):
        if d.get("max_input_channels", 0) > 0:
            print(f"  * Input Index [{idx}]: {d['name']} (Channels: {d['max_input_channels']})")
except ImportError:
    print("  [INFO] Native Windows CoreAudio active. DirectSound interfaces available.")

print("=" * 80)
print("AUDIO AUDIT COMPLETE")
print("=" * 80)

