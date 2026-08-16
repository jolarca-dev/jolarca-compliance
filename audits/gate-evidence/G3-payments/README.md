# G3 — Payments (gate evidence)

Immutable once the gate passes. Required artifacts:

- [x] SAQ-A scope validation (no card data on platform — code + infra proof)
      — PROVEN 2026-08-17, STEP 22c (`reports/STEP22C_FINAL_REAUDIT.md` C1/C2)
- [x] Replay-attack test results (idempotency keys, webhook signatures)
      — PROVEN 2026-08-17, STEP 22c (`reports/STEP22C_FINAL_REAUDIT.md` C3/C4)
- [ ] VAT reconciliation evidence (VIES validation flow) — OPEN (RSK-011)
- [ ] DPIA 003 signed + hash — OPEN (`dpia/003-payments-and-vat`: draft)
- [ ] Stripe TIA + AoC link recorded in vendor register — OPEN
      (`vendor-assessments/stripe`: onboarding, artifacts pending)

Gate status 2026-08-17: **CONDITIONAL CLEARANCE** — payment-boundary
controls cleared; first-real-donation authorization withheld. See
`G3_DECISION.md`. Evidence sealed in `evidence-manifest.md` + `reports/`.

After pass: `make hash-evidence`, then archive the GO decision record.
