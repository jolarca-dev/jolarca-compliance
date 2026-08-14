# G3 — Payments (gate evidence)

Immutable once the gate passes. Required artifacts:

- [ ] SAQ-A scope validation (no card data on platform — code + infra proof)
- [ ] Replay-attack test results (idempotency keys, webhook signatures)
- [ ] VAT reconciliation evidence (VIES validation flow)
- [ ] DPIA 003 signed + hash
- [ ] Stripe TIA + AoC link recorded in vendor register

After pass: `make hash-evidence`, then archive the GO decision record.
