#!/usr/bin/env python3
from __future__ import annotations
import os
import subprocess
import sys

SCRIPTS = [
    "validate_user_records.py",
    "detect_orphaned_badges.py",
    "audit_least_privilege.py",
    "validate_device_inventory.py",
]

def main() -> int:
    data_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "data")
    script_dir = os.path.dirname(__file__)

    print("RUN ALL AUDITS (MOCK)")
    print("=====================\n")

    worst = 0
    for s in SCRIPTS:
        path = os.path.join(script_dir, s)
        print(f"--- Running: {s} ---")
        rc = subprocess.call([sys.executable, path, data_dir])
        print()
        worst = max(worst, rc)

    print("Done.")
    return worst

if __name__ == "__main__":
    raise SystemExit(main())
