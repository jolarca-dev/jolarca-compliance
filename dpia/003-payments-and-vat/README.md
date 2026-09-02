# DPIA 003 — Payments and VAT

Status: **reviewed** — awaiting DPO signature.

Scope: Stripe as processor (SAQ-A scope), seller payouts and verification
documents, VIES VAT validation (live, not format-only), invoice data,
Baltic financial retention obligations vs. erasure rights (ADR-0001:
anonymize-don't-delete), i.SAF (SAF-T) monthly filing, OSS quarterly
returns, religious product category as indirect Art. 9 data.

- Full DPIA: `dpia.md` (251 lines, all 7 sections completed)
- Template: `../000-template.md`
- Linked RoPA: ROPA-003 (orders-payments), ROPA-004 (sellers VIES)
- Gate: G3 (SAQ-A validation, VIES live, replay-attack tests)
- Review date: 2027-01-15

## Blocking conditions (must be resolved before `signed`)

1. VIES live validation implemented and tested (P6 deliverable)
2. i.SAF FR0600 monthly export operational (P6 deliverable)
3. OSS registration initiated (P6 deliverable)
4. First backup restore drill passed (P4 deliverable)
5. DPO review and signature obtained

## Key findings

- **Art. 9 flag**: Purchase of sacred/religious goods indirectly reveals
  religious beliefs. Mitigated by pgcrypto encryption, no profiling,
  functional category tags only.
- **Reverse-charge**: Requires live VIES verification of BOTH buyer and
  seller VAT numbers before applying. Format-only check is insufficient.
- **Retention conflict**: Financial data must be retained 10 years (LT
  Law on Accounting) but erasure rights apply to non-financial data.
  Resolved via ADR-0001: anonymize-don't-delete.
