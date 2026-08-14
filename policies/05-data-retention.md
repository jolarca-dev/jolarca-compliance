# 05 — Data Retention Policy

| | |
|---|---|
| Version | 0.1 (draft) |
| Owner | DPO |
| Approved by | Legal + Management |
| Next review | 2027-08-15 |
| ISO 27001 | Annex A.5.33 |
| SOC 2 | P4.3 |

## Requirements

1. Every data category has a retention class defined in
   `docs/retention-schedule.md`; nothing is kept "just in case".
2. Legal holds override erasure: Baltic accounting obligations (10y, with
   LT/LV/EE variants) are implemented as anonymization where erasure is
   impossible (ADR-0001: anonymize-don't-delete).
3. Erasure requests (Art. 17) execute within the DSR clock across all
   systems incl. processors; completion recorded in the DSR register.
4. Automated expiry: retention jobs per class, tested quarterly, logs kept
   as erasure evidence.
5. Backups: personal data in backups follows the same schedule; restore
   tests must not resurrect expired data into live systems.
6. This repository: finalized evidence is retained per its class and never
   deleted — superseded, hashed, and archived instead.

## Review history

| Version | Date | Author | Approved by |
|---|---|---|---|
| 0.1 | 2026-08-15 | DPO | TBD |
