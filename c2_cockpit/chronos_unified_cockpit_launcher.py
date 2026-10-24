"""
HVF Sovereign C2 // Unified Cockpit Launcher Interface (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)
"""
from pathlib import Path


def get_cockpit_html_path() -> str:
    return str(Path(__file__).resolve().parent / "chronos_unified_cockpit.html")


def launch_cockpit(dry_run: bool = True) -> dict:
    return {
        "cage_code": "1AHA8",
        "status": "PUBLIC_UNIFIED_COCKPIT_READY",
        "html_path": get_cockpit_html_path(),
        "dry_run": dry_run,
    }


launch_unified_cockpit = launch_cockpit
