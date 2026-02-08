from __future__ import annotations
import csv
from dataclasses import dataclass
from typing import Dict, List, Tuple


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
        return list(csv.DictReader(f))


def load_users(users_path: str) -> Tuple[Dict[str, User], Dict[str, User]]:
    """return (users_by_user_id, users_by_badge_id)."""
    rows = read_csv(users_path)
    by_user: Dict[str, User] = {}
    by_badge: Dict[str, User] = {}

    for r in rows:
        u = User(
            user_id=(r.get("user_id") or "").strip(),
            full_name=(r.get("full_name") or "").strip(),
            department=(r.get("department") or "").strip(),
            location=(r.get("location") or "").strip(),
            badge_id=(r.get("badge_id") or "").strip(),
            status=(r.get("status") or "").strip().upper(),
            last_day=(r.get("last_day") or "").strip(),
        )
        if not u.user_id:
            continue

        by_user[u.user_id] = u
        if u.badge_id:
            by_badge[u.badge_id] = u

    return by_user, by_badge


def load_access_groups(groups_path: str) -> List[dict]:
    rows = read_csv(groups_path)
    norm = []
    for r in rows:
        norm.append({
            "badge_id": (r.get("badge_id") or "").strip(),
            "access_group": (r.get("access_group") or "").strip(),
            "assigned_by": (r.get("assigned_by") or "").strip(),
            "assigned_on": (r.get("assigned_on") or "").strip(),
        })
    return norm


def load_device_inventory(inv_path: str) -> List[dict]:
    return read_csv(inv_path)
