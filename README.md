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

## Quick-start
From the repo root:
```bash
python3 scripts/audit_access_integrity.py
