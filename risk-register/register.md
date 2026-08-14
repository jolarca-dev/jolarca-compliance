# Risk Register (living)

Reviewed at every gate and quarterly. See `README.md` for scoring model.

| ID | Risk | Likelihood | Impact | Score | Treatment | Owner | Status | Review |
|---|---|---|---|---|---|---|---|---|
| RSK-001 | LLM vendor receives personal data via egress path | 3 | 4 | 12 | PII pre-filter + allowlist + TIAs (G2 evidence) | Platform | open | 2026-11-15 |
| RSK-002 | Baltic retention obligations conflict with erasure requests | 2 | 4 | 8 | Anonymize-don't-delete pattern (ADR-0001) | DPO | open | 2026-11-15 |
| RSK-003 | Vendor DPA gap during onboarding rush | 2 | 4 | 8 | Onboarding checklist as merge gate; register parity check | Compliance | open | 2026-11-15 |
| RSK-004 | Evidence integrity undetected tampering | 1 | 5 | 5 | Weekly hash verification + branch protection + audit log | Compliance | open | 2026-11-15 |
| RSK-005 | DSR clock breach due to unverified identity loop | 2 | 3 | 6 | Verification SLA (5 days) + day-21 paging | DPO | open | 2026-11-15 |

Status values: `open`, `mitigating`, `accepted`, `closed`.
Accepted risks require a signed acceptance note in the treatment plan.
