#!/usr/bin/env python3

"""
Access Control Data Integrity Audit (mock data)

Purpose:
- Demonstrate operations-focused integrity checks for access control data.
- This script uses mock CSVs only and does not integrate with any live systems.

Checks:
1) Inactive users who still have access group assignments
2) Orphan badge assignments (badge_id in access_groups not present in users)
3) Active users missing badge_id (record hygiene issue)
4) High-risk access groups (simple policy examples) for visibility

Output:
- Human-readable findings and recommended actions.
"""


from __future__ import annotations
import csv
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Set, Tuple


DATA_DIR_DEFAULT = os.path.join(os.path.dirname(__file__), "..", "data")

HIGH_RISK_GROUPS = {
    "ALL_ACCESS",
    "DATA_CENTER",
    "SECOPS_ADMIN",
}

@dataclass(frozen=True)
class User:
    user_id: str
    full_name: str
    department: str
    location: str
    badge_id: str
    status: str
    last_day: str

def read_csv(path: str) -> List[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def load_users(path: str) -> Tuple[Dict[str, User], Dict[str, User]]:
    """return (users_by_user_id, users_by_badge_id)."""
    rows = read_csv(path)
    by_user_id: Dict[str, User] = {}
    by_badge: Dict[str, User] = {}
    for r in rows:
        user = User(
            user_id=r.get("user_id", "").strip(),
            full_name=r.get("full_name", "").strip(),
            department=r.get("department", "").strip(),
            location=r.get("location", "").strip(),
            badge_id=r.get("badge_id", "").strip(),
            status=r.get("status", "").strip().upper(),
            last_day=r.get("last_day", "").strip(),
        )
        if not user.user_id:
            continue
        by_user_id[user.user_id] = user
        if user.badge_id:
            by_badge[user.badge_id] = user
    return by_user_id, by_badge

def load_access_groups(path: str) -> List[dict]:
    rows = read_csv(path)
    # normalize fields
    norm = []
    for r in rows:
        norm.append({
            "badge_id": (r.get("badge_id") or "").strip(),
            "access_group": (r.get("access_group") or "").strip(),
            "assigned_by": (r.get("assigned_by") or "").strip(),
            "assigned_on": (r.get("assigned_on") or "").strip(),
        })
    return norm

def format_finding(title: str, items: List[str]) -> str:
    out = [f"\n{title}", "-" * len(title)]
    if not items:
        out.append("None found.")
        return "\n".join(out)
    for i, item in enumerate(items, start=1):
        out.append(f"{i}. {item}")
    return "\n".join(out)

def main() -> int:
    data_dir = sys.argv[1] if len(sys.argv) > 1 else DATA_DIR_DEFAULT
    users_path = os.path.join(data_dir, "users.csv")
    groups_path = os.path.join(data_dir, "access_groups.csv")

    if not os.path.exists(users_path) or not os.path.exists(groups_path):
        print("ERROR: Expected data/users.csv and data/access_groups.csv", file=sys.stderr)
        print(f"Looked in: {os.path.abspath(data_dir)}", file=sys.stderr)
        return 2

    users_by_id, users_by_badge = load_users(users_path)
    access_rows = load_access_groups(groups_path)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("ACCESS CONTROL DATA INTEGRITY AUDIT")
    print("=========================================")
    print(f"Run time: {now}")
    print(f"Data source: {os.path.abspath(data_dir)}")

    # build helper maps
    badges_in_users: Set[str] = set(users_by_badge.keys())
    badges_in_groups: Set[str] = set(r["badge_id"] for r in access_rows if r["badge_id"])

    groups_by_badge: Dict[str, List[str]] = {}
    for r in access_rows:
        b = r["badge_id"]
        g = r["access_group"]
        if not b or not g:
            continue
        groups_by_badge.setdefault(b, []).append(g)

    # 1) inactive users with access
    inactive_with_access: List[str] = []
    for badge_id, user in users_by_badge.items():
        if user.status == "INACTIVE" and badge_id in groups_by_badge:
            inactive_with_access.append(
                f"{user.full_name} ({user.user_id}) badge={badge_id} has groups={groups_by_badge[badge_id]} "
                f"(last_day={user.last_day or 'unknown'})"
            )

    # 2) orphan badge assignments
    orphan_badges: List[str] = []
    for badge_id in sorted(badges_in_groups - badges_in_users):
        orphan_badges.append(
            f"badge={badge_id} has groups={groups_by_badge.get(badge_id, [])} but no matching user record"
        )

    # 3) active users missing badge_id
    active_missing_badge: List[str] = []
    for u in users_by_id.values():
        if u.status == "ACTIVE" and not u.badge_id:
            active_missing_badge.append(
                f"{u.full_name} ({u.user_id}) is ACTIVE but has no badge_id on file"
            )

    # 4) high-risk groups visibility
    high_risk_assignments: List[str] = []
    for badge_id, groups in groups_by_badge.items():
        risky = sorted(set(groups).intersection(HIGH_RISK_GROUPS))
        if risky:
            owner = users_by_badge.get(badge_id)
            owner_str = f"{owner.full_name} ({owner.user_id})" if owner else "UNKNOWN OWNER"
            high_risk_assignments.append(
                f"{owner_str} badge={badge_id} high_risk_groups={risky}"
            )

    print(format_finding("FINDINGS: Inactive users retaining access", inactive_with_access))
    print(format_finding("FINDINGS: Orphan badge assignments", orphan_badges))
    print(format_finding("FINDINGS: Active users missing badge records", active_missing_badge))
    print(format_finding("VISIBILITY: High-risk access group assignments", high_risk_assignments))

    # recommendations section
    recs: List[str] = []
    if inactive_with_access:
        recs.append("Submit approved request to revoke access groups for inactive users; document changes and retain audit trail.")
    if orphan_badges:
        recs.append("Investigate orphan badge IDs: confirm issuance status, correct records, and remove invalid assignments per procedure.")
    if active_missing_badge:
        recs.append("Validate cardholder records for ACTIVE users missing badge_id; correct source-of-truth record per provisioning SOP.")
    if not recs:
        recs.append("No issues detected in mock dataset. Continue routine audits and spot checks per runbook.")

    print(format_finding("RECOMMENDED NEXT ACTIONS", recs))

    # exit code: nonzero if findings exist
    findings_count = len(inactive_with_access) + len(orphan_badges) + len(active_missing_badge)
    return 1 if findings_count > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
