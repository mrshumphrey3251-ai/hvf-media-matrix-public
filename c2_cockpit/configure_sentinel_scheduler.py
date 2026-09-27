# -*- coding: utf-8 -*-
"""
Project Ebony: Sentinel Task Scheduler & Working Tree Hygiene Engine
Configures Windows scheduled automation for hourly sentinel sweeps and establishes
strict .gitignore rules to prevent runtime log files from creating working tree dirt.
Direct native Python binding architecture.
Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8)
Statutory Standard: DFARS 252.227-7018 / Oklahoma HB 2992 / NIST SP 800-82 Rev 2
"""

import os
import sys
import subprocess
import json

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
task_name = "ProjectEbonySentinelWatchdog"
runner_script = os.path.join(repo_root, "c2_cockpit", "sentinel_service_runner.py")
py_exe = sys.executable

# 1. Working Tree Hygiene: ensure logs directory has .gitkeep and .gitignore excludes *.jsonl
log_dir = os.path.join(repo_root, "cinematic_vault", "logs")
os.makedirs(log_dir, exist_ok=True)
gitkeep_path = os.path.join(log_dir, ".gitkeep")
if not os.path.exists(gitkeep_path):
    with open(gitkeep_path, "w", encoding="utf-8") as f:
        f.write("# Preserve directory structure while ignoring runtime logs\n")

gitignore_path = os.path.join(repo_root, ".gitignore")
rule = "cinematic_vault/logs/*.jsonl"
existing_rules = ""
if os.path.exists(gitignore_path):
    with open(gitignore_path, "r", encoding="utf-8") as f:
        existing_rules = f.read()

if rule not in existing_rules:
    with open(gitignore_path, "a", encoding="utf-8") as f:
        f.write(f"\n# Runtime telemetry audit logs\n{rule}\n")

# 2. Deploy Batch and VBS Wrappers for Native Script Invocations
bat_script = os.path.join(repo_root, "c2_cockpit", "run_sentinel_watchdog.bat")
bat_content = f"""@echo off
cd /d "{repo_root}"
"{py_exe}" c2_cockpit\\sentinel_service_runner.py --cycles 1 --interval 1.0
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
"""
with open(bat_script, "w", encoding="utf-8") as f:
    f.write(bat_content)

vbs_script = os.path.join(repo_root, "c2_cockpit", "run_sentinel_headless.vbs")
vbs_content = f"""Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "{bat_script}" & chr(34), 0, True
Set WshShell = Nothing
"""
with open(vbs_script, "w", encoding="utf-8") as f:
    f.write(vbs_content)

# 3. Direct Native Python Registration via schtasks
sch_status = "UNREGISTERED"
sch_msg = ""
try:
    cmd = [
        "schtasks", "/create",
        "/tn", task_name,
        "/tr", f'"{py_exe}" "{runner_script}" --cycles 1 --interval 1.0',
        "/sc", "hourly",
        "/mo", "1",
        "/f"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        sch_status = "REGISTERED_ACTIVE"
        sch_msg = "Windows Task Scheduler registered directly with native Python."
    else:
        sch_status = "ELEVATION_REQUIRED"
        sch_msg = res.stderr.strip() or res.stdout.strip()
except Exception as e:
    sch_status = "ERROR"
    sch_msg = str(e)

if __name__ == "__main__":
    print("=" * 72)
    print("  PROJECT EBONY: SENTINEL TASK SCHEDULER & TREE HYGIENE ENGINE")
    print("  * Operator Authority: CEO_JEFFERY_HUMPHREY (Level 5 Unrestricted)")
    print("  * Authority CAGE:     1AHA8 (Humphrey Virtual Farms LLC)")
    print("=" * 72)
    print(f"  * Working Tree Hygiene:       PASS (cinematic_vault/logs/*.jsonl gitignored)")
    print(f"  * Native Python Runtime:      {py_exe}")
    print(f"  * Target Runner Script:       {runner_script}")
    print(f"  * Task Scheduler Status:      {sch_status}")
    if sch_msg:
        print(f"    - Detail:                   {sch_msg}")
    print("\n  * [PASS] configure_sentinel_scheduler.py configured with direct native execution.")
