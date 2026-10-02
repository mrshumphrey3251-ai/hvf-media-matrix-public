#!/usr/bin/env python3
"""
sys_check.py - Prints the current date and time.

Usage:
    python sys_check.py
"""

from datetime import datetime
import sys


def get_current_datetime() -> str:
    """Return the current date and time as an ISO 8601 formatted string."""
    return datetime.now().isoformat(sep=' ', timespec='seconds')


def main() -> None:
    """Entry point for the script."""
    current_dt = get_current_datetime()
    print(f"Current date and time: {current_dt}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)