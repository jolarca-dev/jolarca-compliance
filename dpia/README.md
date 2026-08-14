# DPIA — Data Protection Impact Assessments (GDPR Art. 35)

## When a DPIA is mandatory

1. Processing on a large scale of special categories (Art. 9) or criminal data.
2. Systematic monitoring of publicly accessible areas.
3. Automated decision-making with legal/significant effects (Art. 22).
4. Any case in EDPB/WP248 criteria list (≥ 2 criteria met), including:
   AI/LLM processing of user content, geolocation services, payment risk scoring.
5. Whenever a new product feature touches personal data and the RoPA entry
   changes materially — the RoPA gate (`ropa/README.md`) triggers DPIA review.

## Scoring model

Likelihood (1–5) × Impact (1–5) per risk, before/after mitigations.
Residual score ≥ 12 → mandatory DPO escalation + supervisory-authority
consultation check (Art. 36). Full model: `docs/compliance-matrix.md` §risk.

## Lifecycle & sign-off

`draft → vN (reviewed) → vN-signed (DPO + product owner)`

- Versions are immutable once signed; changes create the next version.
- Signed versions are hashed into `audits/evidence-registry.csv`.
- Every DPIA lists linked RoPA entries and risk-register IDs.

## Contents

| Folder | Scope |
|---|---|
| `000-template.md` | Master template (inherits `docs/DPIA-template.md`) |
| `001-identity-and-consent/` | Identity spine, pgcrypto, consent engine |
| `002-ai-processing/` | LLM egress, PII pre-filter, DeepL / self-hosted |
| `003-payments-and-vat/` | Stripe, VIES, financial retention |
| `004-geolocation-search/` | PostGIS location data |
| `register.md` | Index: status, owner, review date, linked RoPA |
