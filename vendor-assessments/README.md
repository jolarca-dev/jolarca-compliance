# Vendor & Transfer Governance

## Onboarding flow (mandatory order)

1. **Security questionnaire** → filed in `<vendor>/questionnaire.md`
2. **DPA** signed (Art. 28) or SCC basis documented → `<vendor>/dpa.md`
3. **Transfer Impact Assessment** for any non-EU/EEA transfer → `tia/`
   — the TIA is **self-authored by JOL**; the vendor supplies the DPA/SCCs
   as inputs, it does not issue the TIA (restated 2026-08-17, STEP 26)
4. **Register entry** → `register.md` + `register.csv` (both, same PR)
5. **RoPA updated** with the new recipient (`ropa/master-register.csv`)

No production data flows before step 4 is merged.

## Annual cycle

- Every active processor re-assessed annually (`vendor-review-due.yml`).
- DPA renewals start ≥ 60 days before expiry; sub-processor change notices
  reviewed within 14 days.
- Attestation refresh: where a processor holds certifications (e.g., Stripe
  PCI DSS AoC), re-retrieve the current document each cycle **or on vendor
  compliance-program update**. PCI AoCs are NOT public downloads: Stripe
  Dashboard → Compliance Settings, else Stripe support request; record who
  retrieved it, when, and the document version/date (see `stripe/README.md`).
- Evidence of each review is hashed into `audits/evidence-registry.csv`.

## Layout

| Path | Content |
|---|---|
| `register.md` / `register.csv` | Human + machine-readable processor index |
| `<vendor>/` | DPA, questionnaire, attestations, correspondence |
| `tia/` | Transfer Impact Assessments (Schrems II) per non-EU transfer |
