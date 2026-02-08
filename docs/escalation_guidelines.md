# Escalation Guidelines (Mock)

## Purpose
Provide consistent thresholds for escalating incidents/issues to an application administrator, local IT, installers, or vendors.

## Escalate immediately
- High severity alarms (life safety, forced entry, critical perimeter alarms)
- Repeated alarms indicating systemic failure (e.g., multiple devices offline)
- Suspected unauthorized access or credential misuse indicators
- Any incident requiring incident response procedures

## Escalate to Local IT (coordination)
- Persistent connectivity symptoms impacting multiple endpoints
- DNS/DHCP/IP addressing anomalies confirmed by basic checks
- VLAN/port configuration dependencies (Tier-1 should not change network config)

## Escalate to Application Administrator / Vendor
- Reproducible application errors after basic client verification
- Server/service dependency failures
- Configuration or enrollment issues requiring admin privileges
- Issues requiring logs/config exports for diagnosis

## What to include in escalation notes
- Timestamp(s) and site/location
- Device IDs and event types
- What you checked (and results)
- Screenshots/log excerpts (when permitted)
- Frequency/recurrence and business impact
