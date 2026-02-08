# Alarm Response Runbook (Mock)

## Purpose
Provide a consistent Tier-1 operational workflow for monitoring alarms/events and documenting actions taken.  
This document is an example runbook and does not describe any live Ford systems.

## Guiding principles
- Follow established procedures and escalation paths
- Prioritize safety and operational continuity
- Document actions taken in a clear, time-ordered manner
- Do not improvise configuration changes during an incident

## Tier-1 response checklist
1. **Acknowledge / record**
   - Capture timestamp, device ID, location, event type, severity
2. **Verify context**
   - Check if the device is known/active in inventory
   - Check for correlated alarms (same area/site)
3. **Perform safe, non-invasive checks**
   - Confirm operator login/session health
   - Confirm client connectivity (if applicable)
   - Confirm basic network symptoms via standard checks (no firewall changes)
4. **Escalate when appropriate**
   - Escalate high-severity or recurring alarms with complete notes
5. **Close the loop**
   - Record final outcome and next steps
   - Link ticket/service request references

## Documentation minimums
- What happened
- What you checked
- What you found
- Who you notified / escalation path
- Outcome / next action
