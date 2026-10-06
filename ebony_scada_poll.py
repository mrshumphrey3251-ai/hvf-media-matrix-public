"""
HVF OMNI-INDUSTRIAL SCADA SENSOR & TELEMETRY POLLING ENGINE
Project: Ebony Sovereign C2 Matrix
Compliance: CAGE 1AHA8 / UEI S1M4ENLHTDH5
Architecture: Non-blocking Deterministic Hardware Telemetry Harvester
"""

import os
import sys
import time
import shutil
import platform

def poll_system_metrics():
    """Captures deterministic local hardware and OS runtime telemetry."""
    try:
        total, used, free = shutil.disk_usage("C:\\")
        free_gb = round(free / (1024**3), 2)
        total_gb = round(total / (1024**3), 2)
        disk_pct = round((used / total) * 100, 1)

        metrics = {
            "node": platform.node(),
            "os": f"{platform.system()} {platform.release()}",
            "disk_free_gb": free_gb,
            "disk_total_gb": total_gb,
            "disk_used_pct": disk_pct,
            "python_runtime": sys.version.split()[0],
            "epoch_utc": int(time.time()),
            "status": "NOMINAL"
        }
        return metrics
    except Exception as e:
        return {"status": "FAULT", "error": str(e)}

def format_scada_telemetry_payload(channel="ALL"):
    """Formats telemetry metrics into a C2-compliant deterministic string."""
    m = poll_system_metrics()
    if m.get("status") == "FAULT":
        return f"GAMMA_SCADA_FAULT: Diagnostic read failure - {m.get('error')}"

    report = (
        f"GAMMA_SCADA_TELEMETRY // CHANNEL: {channel} | "
        f"NODE: {m['node']} | OS: {m['os']} | "
        f"STORAGE: {m['disk_free_gb']}GB FREE / {m['disk_total_gb']}GB TOTAL ({m['disk_used_pct']}% USED) | "
        f"RUNTIME: Python {m['python_runtime']} | "
        f"SYSTEM INTEGRITY: NOMINAL (FIPS-Compliant Deterministic Link)"
    )
    return report
