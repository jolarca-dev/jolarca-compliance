# 08 — Secure Development Policy

| | |
|---|---|
| Version | 0.1 (draft) |
| Owner | Engineering lead |
| Approved by | CISO equivalent |
| Next review | 2027-08-15 |
| ISO 27001 | Annex A.8.25–A.8.31 |
| SOC 2 | CC8 |

## Requirements

1. CI gates mandatory: tests, SAST, dependency scan, secret scan; no merge
   with failing gates, no gate-bypass without filed exception.
2. Code review required for all changes (≥ 1 reviewer; security-sensitive
   paths require a security champion).
3. Vulnerability SLAs from detection: **Critical ≤ 7 days**, High ≤ 30 days,
   Medium ≤ 90 days; SLA breaches tracked in the risk register.
4. Dependencies pinned; updates via Dependabot; new dependencies reviewed for
   supply-chain risk (maintainer, license, data egress).
5. Privacy by design: new personal-data flows require RoPA + DPIA check
   before merge (`ropa/README.md`).
6. Production data never used in tests; synthetic or anonymized sets only.
7. Secrets never in code; pre-commit + CI scanning enforce this.

## Review history

| Version | Date | Author | Approved by |
|---|---|---|---|
| 0.1 | 2026-08-15 | Engineering | TBD |
