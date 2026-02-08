#!/usr/bin/env python3
from __future__ import annotations
import os
import sys
from collections import defaultdict
from datetime import datetime
from lib_io import load_access_groups, load_users

DATA_DIR_DEFAULT = os.path.join(os.path.dirname(__file__), "..", "data")


def main() -> int:
    data_dir = sys.argv[1] if len(sys.argv) > 1 else DATA_DIR_DEFAULT
    users_path = os.path.join(data_dir, "users.csv")
    groups_path = os.path.join(data_dir, "access_groups.csv")

    _, users_by_badge = load_users(users_path)
    access_rows = load_access_groups(groups_path)

    valid_badges = set(users_by_badge.keys())
    active_badges = {b for b, u in users_by_badge.items() if u.status == "ACTIVE"}

    groups_by_badge = defaultdict(set)
    for r in access_rows:
        b, g = r["badge_id"], r["access_group"]
        if b and g:
            groups_by_badge[b].add(g)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("ORPHAN BADGE DETECTION (MOCK)")
    print("=============================")
    print(f"Run time: {now}\n")

    orphan = []
    non_active = []

    for badge, gs in sorted(groups_by_badge.items()):
        if badge not in valid_badges:
            orphan.append(f"badge={badge} has groups={sorted(gs)} but no matching user record")
        elif badge not in active_badges:
            non_active.append(f"badge={badge} has groups={sorted(gs)} but is not tied to an ACTIVE user (review)")

    if not orphan and not non_active:
        print("No orphaned or non-active badge assignments detected in mock data.")
        return 0

    if orphan:
        print("Findings: Orphan badge IDs")
        print("-------------------------")
        for i, x in enumerate(orphan, 1):
            print(f"{i}. {x}")
        print()

    if non_active:
        print("Findings: Badge IDs not tied to ACTIVE users")
        print("-------------------------------------------")
        for i, x in enumerate(non_active, 1):
            print(f"{i}. {x}")
        print()

    print("Recommended next actions (Tier-1 / Ops)")
    print("--------------------------------------")
    print("1. Investigate whether orphan badge IDs represent data entry errors or stale records.")
    print("2. Submit approved change request to correct/remove invalid assignments per SOP.")
    print("3. Document outcome and retain audit trail.")

    return 1 if orphan else 0


if __name__ == "__main__":
    raise SystemExit(main())
