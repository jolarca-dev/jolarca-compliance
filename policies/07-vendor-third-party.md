# 07 — Vendor & Third-Party Management Policy

| | |
|---|---|
| Version | 0.1 (draft) |
| Owner | DPO |
| Approved by | Management |
| Next review | 2027-08-15 |
| ISO 27001 | Annex A.5.19–A.5.22 |
| SOC 2 | CC9.2 |

## Requirements

1. No processor engaged without: security questionnaire, DPA (Art. 28), and —
   for any non-EU/EEA transfer — a Transfer Impact Assessment (Schrems II)
   filed in `vendor-assessments/tia/`.
2. All processors/sub-processors listed in `vendor-assessments/register.md`
   + `register.csv` with DPA status, expiry, and next review date.
3. Annual re-assessment of every active processor (`vendor-review-due.yml`);
   DPA renewals start ≥ 60 days before expiry.
4. Sub-processor changes from vendors are reviewed within 14 days; objection
   rights exercised per contract where needed.
5. Vendor incidents affecting our data are triaged like our own
   (`policies/06`); contractual notification clauses enforced.
6. Exit strategy documented per critical processor (data return/erasure).

## Review history

| Version | Date | Author | Approved by |
|---|---|---|---|
| 0.1 | 2026-08-15 | DPO | TBD |
