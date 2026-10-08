"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: LAUNCH HISTORICAL EBONY
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    # -*- coding: utf-8 -*-

    """

    Project Ebony: Master Sovereign Live Launcher & C2 Service Controller

    Streamlit Native Interface + Persistent Background Daemon Architecture.

    Supports:

      python launch_historical_ebony.py --start   (Starts managed background daemon & opens browser)

      python launch_historical_ebony.py --status  (Queries PID, port 8501 health & active telemetry)

      python launch_historical_ebony.py --stop    (Gracefully terminates daemon & releases port)

      python launch_historical_ebony.py           (Standard interactive foreground console)

    Sole Controlling Authority: CEO Jeffery Humphrey (Level 5 Unrestricted).

    CAGE: 1AHA8 | DFARS 252.227-7018 / Oklahoma HB 2992 Compliant.

    """



    import os

    import sys

    import subprocess

    import time

    import argparse

    import urllib.request

    import urllib.error

    import webbrowser



    repo_root = os.path.dirname(os.path.abspath(__file__))

    pid_file = os.path.join(repo_root, "c2_cockpit", "ebony_c2_daemon.pid")

    console_script = os.path.join(repo_root, "c2_cockpit", "ebony_console.py")

    target_url = "http://127.0.0.1:8501/"



    def is_daemon_running(pid):

        if sys.platform == "win32":

            try:

                out = subprocess.check_output(["tasklist", "/FI", f"PID eq {pid}"], text=True)

                return str(pid) in out

            except Exception:

                return False

        else:

            try:

                os.kill(pid, 0)

                return True

            except OSError:

                return False



    def get_active_pid():

        if os.path.exists(pid_file):

            try:

                with open(pid_file, "r") as f:

                    return int(f.read().strip())

            except Exception:

                return None

        return None



    def check_http_status():

        try:

            req = urllib.request.Request(target_url, headers={"User-Agent": "ProjectEbonyC2/1.0"})

            with urllib.request.urlopen(req, timeout=2.5) as resp:

                return resp.getcode() == 200

        except Exception:

            return False



    def start_daemon(open_browser=True):

        print("=" * 72)

        print("  PROJECT EBONY: SOVEREIGN C2 SERVICE CONTROLLER -- DAEMON START")

        print("  * Operator Authority: CEO_JEFFERY_HUMPHREY (Level 5 Unrestricted)")

        print("  * Authority CAGE:     1AHA8 (Humphrey Virtual Farms LLC)")

        print("=" * 72)



        existing_pid = get_active_pid()

        if existing_pid and is_daemon_running(existing_pid):

            print(f"[!] C2 Cockpit daemon is already active under PID {existing_pid}.")

            if check_http_status():

                print(f"  * [PASS] Endpoint online and responding: {target_url}")

                if open_browser:

                    print(f"  * Launching browser to {target_url}...")

                    webbrowser.open(target_url)

                return

            else:

                print("[*] Port 8501 not responding yet; awaiting stabilization...")



        cmd = [

            sys.executable, "-m", "streamlit", "run",

            console_script,

            "--server.port=8501",

            "--server.headless=true",

            "--browser.gatherUsageStats=false"

        ]



        print(f"[*] Igniting C2 Cockpit background daemon on port 8501...")

        proc = subprocess.Popen(

            cmd,

            cwd=repo_root,

            stdout=subprocess.DEVNULL,

            stderr=subprocess.DEVNULL,

            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0

        )



        with open(pid_file, "w") as f:

            f.write(str(proc.pid))



        print(f"[*] Daemon spawned with PID {proc.pid}. Polling endpoint for HTTP 200 readiness...")

        start_t = time.time()

        online = False

        while time.time() - start_t < 25.0:

            if check_http_status():

                online = True

                break

            time.sleep(1.0)



        if online:

            print(f"[PASS] C2 Cockpit successfully online at {target_url}")

            print(f"  * PID Lockfile: {pid_file} (PID: {proc.pid})")

            if open_browser:

                print(f"  * Directing default browser to {target_url}...")

                webbrowser.open(target_url)

        else:

            print(f"[FAIL] Daemon did not respond with HTTP 200 within timeout.")



    def stop_daemon():

        print("=" * 72)

        print("  PROJECT EBONY: SOVEREIGN C2 SERVICE CONTROLLER -- DAEMON STOP")

        print("=" * 72)

        pid = get_active_pid()

        if not pid:

            print("[!] No active PID file found.")

            return



        print(f"[*] Terminating C2 Cockpit daemon (PID {pid})...")

        if sys.platform == "win32":

            subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True)

        else:

            try:

                os.kill(pid, 15)

            except OSError:

                pass



        time.sleep(1.0)

        if os.path.exists(pid_file):

            try:

                os.remove(pid_file)

            except Exception:

                pass



        print("[PASS] C2 Cockpit daemon terminated and port 8501 released.")



    def status_daemon():

        print("=" * 72)

        print("  PROJECT EBONY: SOVEREIGN C2 SERVICE CONTROLLER -- STATUS AUDIT")

        print("=" * 72)

        pid = get_active_pid()

        running = is_daemon_running(pid) if pid else False

        http_ok = check_http_status()



        print(f"  * Daemon PID:       {pid if pid else 'None'}")

        print(f"  * Process Running:  {'ACTIVE' if running else 'INACTIVE'}")

        print(f"  * Endpoint Health:  {'HTTP 200 OK' if http_ok else 'UNAVAILABLE'}")

        print(f"  * Cockpit Access:   {target_url if http_ok else 'OFFLINE'}")



    def main():

        parser = argparse.ArgumentParser(description="Project Ebony Sovereign C2 Controller")

        parser.add_argument("--start", action="store_true", help="Launch C2 Cockpit as persistent background daemon")

        parser.add_argument("--stop", action="store_true", help="Stop persistent background daemon")

        parser.add_argument("--status", action="store_true", help="Check C2 Cockpit daemon and endpoint status")

        parser.add_argument("--no-browser", action="store_true", help="Do not auto-open browser on start")

        args = parser.parse_args()



        if args.start:

            start_daemon(open_browser=not args.no_browser)

        elif args.stop:

            stop_daemon()

        elif args.status:

            status_daemon()

        else:

            print("=" * 72)

            print("  PROJECT EBONY // HISTORICAL C2 CONSOLE LAUNCHER (INTERACTIVE)")

            print("  Sole Authority: CEO Jeffery Humphrey (100% Absolute Authority)")

            print("=" * 72)

            cmd = [sys.executable, "-m", "streamlit", "run", console_script, "--server.port=8501", "--server.headless=false"]

            subprocess.run(cmd)



    if __name__ == "__main__":

        main()


if __name__ == "__main__":
    render()
