"""
HVF Unified Sovereign C2 & API Watchdog Supervisor (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)
Supervises both the Sovereign C2 Cockpit (127.0.0.1:8501) and the Sovereign Telemetry
Ingestion API (127.0.0.1:3000) with idempotent port checks, auto-recovery, and
extensible service hooks for future edge nodes.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Dict, Tuple
import urllib.error
import urllib.request

ROOT_DIR = Path(__file__).resolve().parent.parent


def probe_endpoint(url: str, timeout: float = 2.5) -> Tuple[bool, str]:
    """Return (is_healthy, status_detail) for a local sovereign HTTP endpoint."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="ignore").strip()
            return resp.status == 200, f"HTTP {resp.status} ({body[:48]})"
    except Exception as exc:
        return False, f"OFFLINE ({type(exc).__name__})"


def resolve_c2_entrypoint() -> Path:
    """Select the canonical C2 Cockpit Streamlit entrypoint."""
    for rel in ["c2_cockpit/app.py", "scada_engine/app.py", "app.py"]:
        cand = ROOT_DIR / rel
        if cand.exists():
            return cand
    raise FileNotFoundError("No C2 Cockpit entrypoint found in repository root.")


def resolve_api_entrypoint() -> Path:
    """Select the canonical Sovereign API server entrypoint."""
    for rel in ["scada_engine/hvf_core_server.py", "c2_cockpit/hvf_core_server.py", "hvf_core_server.py"]:
        cand = ROOT_DIR / rel
        if cand.exists():
            return cand
    raise FileNotFoundError("No hvf_core_server.py entrypoint found in repository root.")


def ensure_stack_online(wait_sec: float = 4.0) -> Dict[str, str]:
    """Ensure both C2 Cockpit (8501) and Ingestion API (3000) are running and healthy."""
    c2_url = "http://127.0.0.1:8501/_stcore/health"
    api_url = "http://127.0.0.1:3000/api/status"

    c2_ok, c2_msg = probe_endpoint(c2_url)
    if not c2_ok:
        c2_entry = resolve_c2_entrypoint()
        subprocess.Popen(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(c2_entry),
                "--server.port",
                "8501",
                "--server.address",
                "127.0.0.1",
                "--server.headless",
                "true",
            ],
            cwd=str(ROOT_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(wait_sec)
        c2_ok, c2_msg = probe_endpoint(c2_url)

    api_ok, api_msg = probe_endpoint(api_url)
    if not api_ok:
        api_entry = resolve_api_entrypoint()
        subprocess.Popen(
            [sys.executable, str(api_entry)],
            cwd=str(ROOT_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1.5)
        api_ok, api_msg = probe_endpoint(api_url)

    return {
        "c2_8501": f"{'ONLINE' if c2_ok else 'FAULT'} | {c2_msg}",
        "api_3000": f"{'ONLINE' if api_ok else 'FAULT'} | {api_msg}",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="HVF Unified Sovereign C2 & API Watchdog Supervisor")
    parser.add_argument("--watch", action="store_true", help="Run continuous 15-second health supervision loop")
    parser.add_argument("--interval", type=float, default=15.0, help="Watchdog poll interval in seconds")
    args = parser.parse_args()

    status = ensure_stack_online()
    print(f"[+] C2 Cockpit (8501): {status['c2_8501']}")
    print(f"[+] Sovereign API (3000): {status['api_3000']}")

    if args.watch:
        print(f"[*] Watchdog Supervision Armed (Interval: {args.interval:.1f}s) — Press Ctrl+C to stop.")
        while True:
            time.sleep(args.interval)
            st = ensure_stack_online(wait_sec=2.0)
            if "FAULT" in st["c2_8501"] or "FAULT" in st["api_3000"]:
                print(f"[WARN] Recovery triggered -> {json.dumps(st)}", flush=True)


if __name__ == "__main__":
    main()