# 06 — Incident Response Policy

| | |
|---|---|
| Version | 0.1 (draft) |
| Owner | Compliance lead |
| Approved by | Management + DPO |
| Next review | 2027-08-15 |
| ISO 27001 | Annex A.5.24–A.5.27 |
| SOC 2 | CC7 |

## Severity matrix

| Severity | Definition | Response SLA |
|---|---|---|
| Critical | Confirmed/suspected personal data breach; evidence tampering | Immediate; 72h assessment clock starts |
| High | Security incident, personal data impact possible | 24h triage |
| Medium | Policy violation, no data impact expected | Next business day |
| Near-miss | Control worked; nearly happened | Recorded; feeds game-day findings |

## Requirements

1. Intake via `incidents/` templates or the incident issue form; every report
   gets a register entry, including near-misses (SOC 2 CC7 evidence).
2. Assessment toward Art. 33 notification completed **within 72 hours** of
   awareness; decision (notify / not notify / high-risk to subjects) is
   documented either way.
3. Notification templates per authority & language in `incidents/templates/`;
   contacts in `docs/regulatory-contacts.md`.
4. Blameless postmortem mandatory for Critical/High; actions tracked with
   owners and due dates in the postmortem and risk register.
5. Quarterly game day (`incidents/game-days/`); findings become treatment items.
6. Evidence preserved: timeline, logs, decisions — hashed on closure.

## Review history

| Version | Date | Author | Approved by |
|---|---|---|---|
| 0.1 | 2026-08-15 | Compliance | TBD |
