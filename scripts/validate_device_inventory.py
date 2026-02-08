#!/usr/bin/env python3
from __future__ import annotations
import os
import sys
from collections import defaultdict
from datetime import datetime
from lib_io import load_device_inventory

DATA_DIR_DEFAULT = os.path.join(os.path.dirname(__file__), "..", "data")
REQUIRED_FIELDS = ["device_id", "device_type", "site", "location", "status"]


def main() -> int:
    data_dir = sys.argv[1] if len(sys.argv) > 1 else DATA_DIR_DEFAULT
    inv_path = os.path.join(data_dir, "device_inventory.csv")

    devices = load_device_inventory(inv_path)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("DEVICE INVENTORY VALIDATION (MOCK)")
    print("==================================")
    print(f"Run time: {now}\n")

    missing_fields = []
    missing_ip_active = []
    duplicate_ips = []
    naming_issues = []

    ip_map = defaultdict(list)

    for d in devices:
        device_id = (d.get("device_id") or "").strip() or "UNKNOWN"
        status = (d.get("status") or "").strip().upper()
        ip = (d.get("ip_address") or "").strip()
        naming_ok = (d.get("naming_convention_ok") or "").strip().lower()

        for f in REQUIRED_FIELDS:
            if not (d.get(f) or "").strip():
                missing_fields.append(f"device_id={device_id} missing field={f}")

        if status == "ACTIVE" and not ip:
            missing_ip_active.append(f"{device_id} is ACTIVE but ip_address is blank")

        if ip:
            ip_map[ip].append(device_id)

        if naming_ok in {"false", "0", "no"}:
            naming_issues.append(f"{device_id} naming_convention_ok=false (review naming/labeling standard)")

    for ip, devs in ip_map.items():
        if len(devs) > 1:
            duplicate_ips.append(f"ip_address={ip} used by devices={devs} (possible record error/conflict)")

    def section(title, items):
        print(title)
        print("-" * len(title))
        if not items:
            print("None found.\n")
            return
        for i, x in enumerate(items, 1):
            print(f"{i}. {x}")
        print()

    section("Findings: Missing required fields", missing_fields)
    section("Findings: ACTIVE devices missing IP", missing_ip_active)
    section("Findings: Duplicate IPs", duplicate_ips)
    section("Findings: Naming/labeling issues", naming_issues)

    any_findings = any([missing_fields, missing_ip_active, duplicate_ips, naming_issues])

    print("Recommended next actions (Tier-1 / Ops)")
    print("--------------------------------------")
    print("1. Correct inventory records via approved workflow; retain audit trail.")
    print("2. For missing IPs, verify enrollment/connectivity and update source-of-truth.")
    print("3. For duplicates, coordinate with local IT/installer to confirm addressing.\n")

    return 1 if any_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
