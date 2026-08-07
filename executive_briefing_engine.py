import os
from datetime import datetime

print("[HVF NEXUS] Compiling Executive Telemetry Briefing...")
date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
report_name = f"Executive_Brief_{datetime.now().strftime('%Y%m%d')}.md"
report_path = os.path.join(os.getcwd(), report_name)

with open(report_path, 'w') as report:
    report.write("# PROJECT EBONY: EXECUTIVE TELEMETRY BRIEFING\n")
    report.write(f"**Generated:** {date_str}\n\n")
    report.write("## 1. HIGH-VALUE OSINT TARGETS\n")
    try:
        with open("/home/mrshumphrey3251/HVF_INTEL_SCRAPER/osint_targets.log", "r") as f:
            lines = f.readlines()[-15:] # Extract the latest sweeps
            report.writelines(lines)
    except Exception:
        report.write("> [!] OSINT Data offline or pending sweep.\n")
    
    report.write("\n## 2. COMMERCIAL INTAKE GRID\n")
    try:
        with open("/home/mrshumphrey3251/HVF_MEDIA_MATRIX/autoresponder_cron.log", "r") as f:
            lines = f.readlines()[-10:]
            report.writelines(lines)
    except Exception:
        report.write("> [!] Intake Data offline or pending sweep.\n")

print(f"[HVF NEXUS] Briefing mathematically compiled and secured at: {report_path}")
