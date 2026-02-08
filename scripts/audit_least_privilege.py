#!/usr/bin/env python3
from __future__ import annotations
import os
import sys
from collections import defaultdict
from datetime import datetime
from lib_io import load_access_groups, load_users

DATA_DIR_DEFAULT = os.path.join(os.path.dirname(__file__), "..", "data")

HIGH_RISK_GROUPS = {"ALL_ACCESS", "DATA_CENTER", "SECOPS_ADMIN"}
REVIEW_COMBOS = [
    {"ALL_ACCESS"},
    {"DATA_CENTER", "ENG_MAIN"},
]


def main() -> int:
    data_dir = sys.argv[1] if len(sys.argv) > 1 else DATA_DIR_DEFAULT
    users_path = os.path.join(data_dir, "users.csv")
    groups_path = os.path.join(data_dir, "access_groups.csv")

    _, users_by_badge = load_users(users_path)
    access_rows = load_access_groups(groups_path)

    groups_by_badge = defaultdict(set)
    for r in access_rows:
        b, g = r["badge_id"], r["access_group"]
        if b and g:
            groups_by_badge[b].add(g)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("LEAST PRIVILEGE AUDIT (MOCK)")
    print("===========================")
    print(f"Run time: {now}\n")

    findings = []

    for badge, gs in sorted(groups_by_badge.items()):
        owner = users_by_badge.get(badge)
        owner_str = f"{owner.full_name} ({owner.user_id}, status={owner.status})" if owner else "UNKNOWN OWNER"

        risky = sorted(gs & HIGH_RISK_GROUPS)
        if risky:
            findings.append(f"{owner_str} badge={badge} has HIGH-RISK groups: {risky}")

        for combo in REVIEW_COMBOS:
            if combo.issubset(gs):
                findings.append(f"{owner_str} badge={badge} has REVIEW combo={sorted(combo)} (current={sorted(gs)})")

    if not findings:
        print("No least-privilege findings detected in mock data.")
        return 0

    print("Findings")
    print("--------")
    for i, x in enumerate(findings, 1):
        print(f"{i}. {x}")

    print("\nRecommended next actions (Tier-1 / Ops)")
    print("--------------------------------------")
    print("1. Verify approvals exist for high-risk access groups.")
    print("2. If approvals are missing/stale, submit change request per SOP.")
    print("3. Document review outcome and retain audit trail.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
