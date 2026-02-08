#!/usr/bin/env python3
from __future__ import annotations
import os
import sys
from collections import defaultdict
from datetime import datetime
from lib_io import load_users

DATA_DIR_DEFAULT = os.path.join(os.path.dirname(__file__), "..", "data")


def main() -> int:
    data_dir = sys.argv[1] if len(sys.argv) > 1 else DATA_DIR_DEFAULT
    users_path = os.path.join(data_dir, "users.csv")

    users_by_id, users_by_badge = load_users(users_path)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("USER RECORD INTEGRITY VALIDATION (MOCK)")
    print("=======================================")
    print(f"Run time: {now}\n")

    active_missing_badge = []
    duplicate_badges = []

    badge_to_users = defaultdict(list)
    for u in users_by_id.values():
        if u.badge_id:
            badge_to_users[u.badge_id].append(u)

    for u in users_by_id.values():
        if u.status == "ACTIVE" and not u.badge_id:
            active_missing_badge.append(
                f"{u.full_name} ({u.user_id}) is ACTIVE but has no badge_id on file"
            )

    for badge, users in badge_to_users.items():
        if len(users) > 1:
            duplicate_badges.append(
                f"badge_id={badge} assigned to multiple users: "
                + ", ".join(f"{u.full_name} ({u.user_id})" for u in users)
            )

    def section(title, items):
        print(title)
        print("-" * len(title))
        if not items:
            print("None found.\n")
            return
        for i, x in enumerate(items, 1):
            print(f"{i}. {x}")
        print()

    section("Findings: ACTIVE users missing badge_id", active_missing_badge)
    section("Findings: Duplicate badge assignments", duplicate_badges)

    any_findings = bool(active_missing_badge or duplicate_badges)

    print("Recommended next actions (Tier-1 / Ops)")
    print("--------------------------------------")
    print("1. Validate source-of-truth records for affected users (HR vs Security system).")
    print("2. Correct badge assignments via approved provisioning workflow.")
    print("3. Document changes and retain audit trail.\n")

    return 1 if any_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
