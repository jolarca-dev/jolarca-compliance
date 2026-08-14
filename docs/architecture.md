# Architecture (template-inherited, compliance-extended)

## Purpose of this document

Maps the compliance repository to the product and infrastructure controls it
governs. Product repos implement controls; this repo records obligations,
evidence, and decisions about them.

## Repo ↔ product/infra control map

| Compliance artifact | Enforced by (product/infra) | Evidence path |
|---|---|---|
| `policies/03-access-control.md` | GitHub org policy, Vault, GCP IAM | `audits/access-reviews/` |
| `policies/04-cryptography...` | pgcrypto (users/sellers DB), GCP KMS CMEK, Vault | gate-evidence G1 |
| `policies/05-data-retention.md` | retention jobs per class; anonymization (ADR-0001) | erasure E2E logs (G1) |
| `policies/12-ai-usage.md` | PII pre-filter service + egress allowlist in ai-service | gate-evidence G2 |
| `ropa/` ROPA-003 | Stripe Checkout (SAQ-A), idempotency keys | gate-evidence G3 |
| `legal/cookie-policy/banner-spec.md` | consent banner server-side enforcement | G4 acceptance tests |
| `data-subject-requests/` | DSR system + erasure APIs across services | DSR SLA reports |

## Boundaries

- No personal data in this repo (hard rule, README).
- Evidence binaries in the encrypted vault/LFS; git holds hashes.
- Automation (scripts/, workflows) is stdlib-only to keep the evidence
  supply chain minimal.

This document is updated whenever a new control mapping is added; reviewed at
every gate.
