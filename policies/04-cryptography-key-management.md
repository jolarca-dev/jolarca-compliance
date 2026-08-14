# 04 — Cryptography & Key Management Policy

| | |
|---|---|
| Version | 0.1 (draft) |
| Owner | Platform lead |
| Approved by | CISO equivalent |
| Next review | 2027-08-15 |
| ISO 27001 | Annex A.8.24 (cryptography) |
| SOC 2 | CC6.1, CC6.7 |

## Requirements

1. Field-level encryption for sensitive columns via pgcrypto; algorithm and
   key length per current standard (AES-256-GCM or equivalent).
2. Keys managed in KMS/Vault with CMEK where the cloud provider supports it
   (see `vendor-assessments/google-cloud/`).
3. Key custody: two-person rule for master key operations; key material
   never leaves the KMS boundary.
4. Rotation: data keys ≤ 90 days; master keys per provider schedule and at
   least annually; rotation evidence archived per gate.
5. Revocation/compromise runbook: immediate rotation + incident opened;
   affected data classes identified within 24h.
6. TLS ≥ 1.2 everywhere; deprecated cipher suites blocked at edge.
7. Hashing of finalized evidence uses SHA-256 (`scripts/evidence-hash.py`);
   MD5/SHA-1 forbidden for integrity purposes.

## Review history

| Version | Date | Author | Approved by |
|---|---|---|---|
| 0.1 | 2026-08-15 | Platform | TBD |
