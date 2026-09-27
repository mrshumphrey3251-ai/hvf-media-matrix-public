@echo off
cd /d "%~dp0\.."
python c2_cockpit\sentinel_service_runner.py --cycles 1 --interval 1.0
