# PCI DSS Track (SAQ-A)

- SAQ-A annual self-assessment questionnaire + attestation
- Scope statement: platform never stores/processes/transmits card data
  (Stripe-hosted fields / Checkout only) — this is the G3 proof burden
- Stripe AoC (kept current in `vendor-assessments/stripe/`): NOT a public
  download — Stripe Dashboard → Compliance Settings, else Stripe support
  request; retrieval recorded with who/when/version (STEP 26 correction)
- Quarterly external scan vendor confirmation (ASV) where applicable

Any change that brings card data onto platform infrastructure invalidates
SAQ-A scope: treat as Critical change, re-assess immediately.
