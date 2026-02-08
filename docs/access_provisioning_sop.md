# Access Provisioning & Deprovisioning SOP (Mock)

## Purpose
Ensure accurate access provisioning/deprovisioning using least-privilege principles and auditable change records.

## Scope
- User/operator record changes
- Badge/credential assignment
- Access group assignment changes
- Deprovisioning on termination/role change

## SOP: Provisioning (high level)
1. Receive **approved request** (ticket/form with approver)
2. Validate identity fields (name, employee/contractor status, location, department)
3. Assign badge_id / credential record
4. Assign **minimum necessary** access groups
5. Document the change:
   - who approved
   - what was changed
   - effective date/time
6. Confirm expected function (as applicable) via standard checks
7. Close request with final notes

## SOP: Deprovisioning (high level)
1. Receive termination/role-change notice (approved source)
2. Disable credential / revoke access groups per procedure
3. Validate removal:
   - confirm user no longer appears in active access rosters
4. Record outcome and retain audit trail

## Common data integrity checks
- ACTIVE users must have badge_id
- INACTIVE users should not retain access groups
- No orphan badge assignments
