# 03 — Access Control Policy

| | |
|---|---|
| Version | 0.1 (draft) |
| Owner | Compliance lead |
| Approved by | CISO equivalent |
| Next review | 2027-08-15 |
| ISO 27001 | Annex A.5.15–A.5.18, A.8.2–A.8.3 |
| SOC 2 | CC6 |

## Requirements

1. Least privilege by default; access granted per role, reviewed on need.
2. Joiner/mover/leaver (JML): access changes within 24h of role change;
   leaver revocation same day, logged.
3. MFA enforced on all human access to production, Vault, cloud IAM, and
   this repository.
4. Secrets only via Vault — never in code, env files, or chat.
5. Production access is break-glass or ticketed; all sessions logged.
6. Quarterly access review: repo, Vault, cloud IAM, support tooling
   (`access-review-due.yml` → evidence in `audits/access-reviews/`).
7. Shared accounts prohibited; service accounts inventoried and scoped.
8. This repo: CODEOWNERS dual control; branch protection on `main`;
   no force-push, no history rewrite — ever.

## Review history

| Version | Date | Author | Approved by |
|---|---|---|---|
| 0.1 | 2026-08-15 | Compliance | TBD |
