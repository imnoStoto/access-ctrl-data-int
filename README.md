# Physical Security Data Integrity (Mock)

This is an exploration into basic security-oriented data parsing and sanitation.

## Core ideas
Enterprise physical security systems are only as reliable as the integrity of their data:
- incorrect access assignments can create security gaps
- stale or orphan credential records can undermine audits
- inconsistent inventories and naming conventions slow incident response

This repository demonstrates a Tier-1 / operations-focused approach to data hygiene and validation using mock datasets only.

## What this project is
A small, documented toolkit that:
- audits access-control record integrity (mock users, badges, access groups)
- flags common least-privilege and lifecycle violations (inactive users retaining access, orphan badge assignments)
- models runbook-driven operational workflows (documentation-first)

## Repository structure
<pre>
physical-security-data-integrity/
├── data/
│   ├── access_groups.csv
│   ├── device_inventory.csv
│   └── users.csv
├── docs/
│   ├── access_provisioning_sop.md
│   ├── alarm_response_runbook.md
│   └── escalation_guidelines.md
├── README.md
└── scripts/
    ├── audit_least_privilege.py
    ├── detect_orphaned_badges.py
    ├── legacy/
    │   └── audit_access_integrity.py
    ├── lib_io.py
    ├── run_all_audits.py
    ├── validate_device_inventory.py
    └── validate_user_records.py
</pre>    

## Scripts
- `scripts/validate_user_records.py` - checks for active users without a badge id and for duplicate badge assignments across users
- `scripts/detect_orphaned_badges.py` — flags badge assignments not tied to valid/active user records
- `scripts/audit_least_privilege.py` — highlights high-risk groups and review-worthy combinations
- `scripts/validate_device_inventory.py` — validates device inventory completeness/integrity (required fields, IPs, naming flags)
- `scripts/run_all_audits.py` — runs all audits sequentially

## Quick-start
From the repo root:
```bash
python3 scripts/run_all_audits.py
```
**This runs all audit scripts sequentially**
