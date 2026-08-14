# 11 — Logging & Monitoring Policy

| | |
|---|---|
| Version | 0.1 (draft) |
| Owner | Platform lead |
| Approved by | CISO equivalent |
| Next review | 2027-08-15 |
| ISO 27001 | Annex A.8.15–A.8.16 |
| SOC 2 | CC7.1–CC7.2 |

## Requirements

1. Audit log standard: who, what, when, where, outcome — for authentication,
   authorization changes, personal-data access, admin actions, and this
   repository's protected-branch events.
2. Tamper evidence: logs shipped to append-only storage; retention per
   `docs/retention-schedule.md` (RC-LOGS); integrity spot-checked quarterly.
3. Monitoring: alerting on anomalous access patterns, bulk exports, and
   privilege escalation; alerts route to on-call with escalation to DPO for
   personal-data-relevant anomalies.
4. Log access itself is logged; log data containing personal data follows
   the same protection level as the source data.
5. Sentry/GlitchTip choice governed by `vendor-assessments/`: error payloads
   scrubbed of personal data before egress.
6. Evidence: monitoring config exports archived per gate.

## Review history

| Version | Date | Author | Approved by |
|---|---|---|---|
| 0.1 | 2026-08-15 | Platform | TBD |
