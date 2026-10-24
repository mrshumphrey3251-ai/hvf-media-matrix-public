"""
HVF Sovereign C2 // Ebony Chronos Public Production CLI Interface (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)
"""
import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Ebony Chronos Public CLI")
    parser.add_argument("--mode", default="report")
    parser.add_argument("--terminal", default="atak")
    args, _ = parser.parse_known_args()
    payload = {
        "cage_code": "1AHA8",
        "uei": "S1M4ENLHTDH5",
        "status": "PUBLIC_CLI_ACTIVE",
        "mode": args.mode,
        "terminal": args.terminal,
        "data_rights": "DFARS 252.227-7018 (GPR)",
    }
    print(json.dumps(payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
