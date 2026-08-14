# 09 — Business Continuity & Disaster Recovery Policy

| | |
|---|---|
| Version | 0.1 (draft) |
| Owner | Platform lead |
| Approved by | Management |
| Next review | 2027-08-15 |
| ISO 27001 | Annex A.5.29–A.5.30 |
| SOC 2 | A1 |

## Requirements

1. Targets: **RTO ≤ 4h**, **RPO ≤ 15 min** for platform-critical services;
   per-system classification table maintained with the DR plan.
2. Backups: encrypted, versioned, at least one copy outside the primary
   region; restore not assumed until tested.
3. Restore drills at least quarterly; results (measured RTO/RPO) filed as
   evidence in `audits/gate-evidence/` and reviewed in management review.
4. Failover runbooks exist for: database, object storage, search, AI service
   degradation path (platform operates without AI).
5. This repository: recoverable from origin remote + LFS vault; evidence
   registry allows integrity re-verification after restore.
6. DR test failures and missed targets become risk-register entries.

## Review history

| Version | Date | Author | Approved by |
|---|---|---|---|
| 0.1 | 2026-08-15 | Platform | TBD |
