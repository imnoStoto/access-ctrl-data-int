# Physical Security Data Integrity (Mock)

## Why this exists
Enterprise physical security systems are only as reliable as the integrity of their data:
- incorrect access assignments can create security gaps
- stale or orphan credential records can undermine audits
- inconsistent inventories and naming conventions slow incident response

This repository demonstrates a **Tier-1 / operations-focused** approach to data hygiene and validation using **mock datasets only**.

## What this project is
A small, documented toolkit that:
- audits access-control record integrity (mock users, badges, access groups)
- flags common least-privilege and lifecycle violations (inactive users retaining access, orphan badge assignments)
- models runbook-driven operational workflows (documentation-first)

## What this project is NOT
- No integration with live systems
- No vendor API usage
- No configuration changes to any production environment
- No security “bypass” content (this is strictly operational validation)

## Repository layout
- `data/` — mock CSV datasets (users, access_groups, device_inventory)
- `scripts/` — audit scripts that produce human-readable findings
- `docs/` — runbooks and SOPs for incident response and access integrity

## Scripts
- `scripts/detect_orphaned_badges.py` — flags badge assignments not tied to valid/active user records
- `scripts/audit_least_privilege.py` — highlights high-risk groups and review-worthy combinations
- `scripts/validate_device_inventory.py` — validates device inventory completeness/integrity (required fields, IPs, naming flags)
- `scripts/run_all_audits.py` — runs all audits sequentially

## Quick-start
From the repo root:
```bash
python3 scripts/run_all_audits.py *This runs all 3 audit scripts sequentially individually*
python3 scripts/detect_orphaned_badges.py *This runs the badge orphan check individually*
python3 scripts/audit_least_privilege.py *This runs the privilege check individually*
python3 scripts/validate_device_inventory.py *This runs the device inventory check individually*
