"""
E.B.O.N.Y. Master C2 Daemon Health & Telemetry Verification Engine
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Authority: Oklahoma Title 61 & OK HB 2992
"""
import os
import sys
import socket
from pathlib import Path

base_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private")
err_log = base_dir / "streamlit_err.log"
out_log = base_dir / "streamlit_out.log"

print("\n" + "=" * 86)
print("     E.B.O.N.Y. MASTER C2 DAEMON HEALTH & TELEMETRY AUDIT     ")
print("     NODE: HVFNexus | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5")
print("=" * 86)

# 1. Direct Socket Verification
def check_port(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False

lh_ok = check_port("127.0.0.1", 8501)
ts_ok = check_port("100.87.162.117", 8501)
print(f"[*] Loopback Socket (127.0.0.1:8501):        {'ONLINE (ACTIVE)' if lh_ok else 'OFFLINE'}")
print(f"[*] Tailscale Socket (100.87.162.117:8501):    {'ONLINE (ACTIVE)' if ts_ok else 'OFFLINE'}")

# 2. Stderr Operational Error Audit (filtering benign library deprecation advisories)
KNOWN_DEPRECATION_PATTERNS = [
    "st.components.v1.html",
    "st.components.v1.iframe",
    "use_container_width",
    "Please replace",
    "will be removed after"
]

if err_log.exists():
    raw_lines = err_log.read_text(encoding="utf-8", errors="ignore").splitlines()
    actionable_errors = []
    advisories = []
    
    for l in raw_lines:
        s = l.strip()
        if not s:
            continue
        if any(pat in s for pat in KNOWN_DEPRECATION_PATTERNS):
            advisories.append(s)
        else:
            actionable_errors.append(s)
            
    if actionable_errors:
        print("\n[!] ACTIONABLE OPERATIONAL CRASHES DETECTED:")
        for l in actionable_errors[-10:]:
            print(f"    {l}")
    else:
        print("\n[+] OPERATIONAL HEALTH: 100% CLEAN. Zero runtime crashes or missing-file errors.")
        
    if advisories:
        print(f"[*] Informational Framework Advisories Noted: {len(advisories)} (Non-blocking)")
else:
    print("\n[*] streamlit_err.log is unpopulated.")

# 3. Stdout Stream
if out_log.exists():
    out_lines = out_log.read_text(encoding="utf-8", errors="ignore").splitlines()
    print("\n[*] Active Network Bindings:")
    for l in out_lines[-3:]:
        print(f"    {l}")

print("=" * 86 + "\n")
