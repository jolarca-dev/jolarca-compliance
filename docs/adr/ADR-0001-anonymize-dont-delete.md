# ADR-0001 — Anonymize-don't-delete for financial records

- Status: accepted (draft text — sign-off pending)
- Date: 2026-08-15
- Deciders: DPO, Legal, Platform lead

## Context

Baltic accounting law (LT Accounting Act; LV/EE equivalents) requires keeping
accounting documents ~10 years. GDPR Art. 17 erasure requests conflict with
these records when they contain personal data (buyer/seller identifiers on
invoices and orders).

> **Amendment 1 — 2026-08-17 (STEP 26), annotated, original text preserved:**
> the "~10 years" framing above is superseded by the per-country matrix in
> `docs/retention-schedule.md` §2. Lithuania distinguishes TWO statutory
> classes: accounting/financial documents (10 years — Law on Accounting of
> the Republic of Lithuania) and payroll/personnel-adjacent records (up to
> 50 years — distinct class). LV/EE values remain `[COUNSEL-TO-CONFIRM]`.

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

### Amendment 1 consequences (STEP 26)

- The same anonymize-don't-delete mechanism extends to the new
  **RC-PAYROLL-50Y** class, but the collision window with GDPR Art. 17
  extends to decades: erasure is overridden by the legal obligation of
  Art. 17(3)(b); the override, the hold period, and the anonymization act
  must be documented per record class and **reviewed by the DPO**.
- Erasure-response templates need a long-hold variant citing the statutory
  class (pending counsel confirmation of scope `[COUNSEL-TO-CONFIRM]`).
- Records only CANDIDATE for the 50-year class carry a do-not-delete flag
  until counsel classifies them.

## Alternatives rejected

- Blanket refusal of erasure for financial data (regulator-hostile, weak basis).
- Full deletion in violation of accounting law (unacceptable legal risk).
