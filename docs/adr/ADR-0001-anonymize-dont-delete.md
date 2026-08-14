# ADR-0001 — Anonymize-don't-delete for financial records

- Status: accepted (draft text — sign-off pending)
- Date: 2026-08-15
- Deciders: DPO, Legal, Platform lead

## Context

Baltic accounting law (LT Accounting Act; LV/EE equivalents) requires keeping
accounting documents ~10 years. GDPR Art. 17 erasure requests conflict with
these records when they contain personal data (buyer/seller identifiers on
invoices and orders).

## Decision

For RC-FINANCIAL data under legal hold we **anonymize instead of deleting**:

1. On a valid erasure request, remove/cryptographically erase all direct and
   indirect identifiers from fiscal records (name, contact, account links),
   retaining fiscal fields (amounts, dates, VAT, counterparty VAT codes where
   legally required) so the accounting obligation remains fulfilled.
2. Cryptographic erasure (key deletion for pgcrypto-encrypted fields) is an
   accepted anonymization technique; documented per run.
3. Records post-anonymization are outside GDPR scope; no further erasure
   obligation applies.

## Consequences

- Erasure pipeline needs an anonymization branch for RC-FINANCIAL (tested in
  G1 erasure E2E evidence).
- Response letters must explain partial erasure with legal basis citation
  (DSR refusal/partial templates).
- LT/LV/EE variants verified per entity before G3 (see retention-schedule).

## Alternatives rejected

- Blanket refusal of erasure for financial data (regulator-hostile, weak basis).
- Full deletion in violation of accounting law (unacceptable legal risk).
