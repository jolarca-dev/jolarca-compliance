# Vendor / Processor Register

Human-readable index. Machine-readable twin: `register.csv` (both updated in
the same PR). `scripts/vendor-review-dates.py` enforces parity between
`register.csv` and the vendor folders, and fails CI on drift.

| Vendor | Role | Data (ROPA) | DPA | TIA | Next review | Status |
|---|---|---|---|---|---|---|
| Stripe | Processor (payments) | ROPA-003 | pending | required (SCC) | 2027-08-15 | onboarding |
| Google Cloud | Processor (infra) | all | pending | EU-region commitment | 2027-08-15 | onboarding |
| DeepL | Processor (translation) | ROPA-005 | pending | required | 2027-08-15 | onboarding |
| OpenAI | Processor (LLM) | ROPA-005 | pending | required (SCC) | 2027-08-15 | onboarding |
| Anthropic | Processor (LLM) | ROPA-005 | pending | required (SCC) | 2027-08-15 | onboarding |
| DPD | Processor (shipping) | ROPA-003 | pending | EU-only | 2027-08-15 | onboarding |
| Omniva | Processor (shipping) | ROPA-003 | pending | EU-only | 2027-08-15 | onboarding |
| Bitrix24 | Processor (CRM/support) | support cases | pending | verify hosting region | 2027-08-15 | onboarding |
| Sentry/GlitchTip | Processor (error tracking) | scrubbed telemetry | pending | verify | 2027-08-15 | onboarding |

Status values: `onboarding`, `active`, `renewal-due`, `terminated`, `data-returned`.
