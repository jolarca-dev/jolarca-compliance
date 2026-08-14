# Consent version ledger

Which consent version was shown to users, when. This ties UI deployment to
`ConsentRecord` rows in the product database and is regulator-facing evidence.

| Version ID | Language(s) | Purpose | Shown from | Shown until | Deploy ref | Approved by |
|---|---|---|---|---|---|---|
| CT-marketing-v1 | lt/lv/et/en | Marketing communications | TBD | — | TBD | TBD |
| CT-location-v1 | lt/lv/et/en | Geolocation search (ROPA-006) | TBD | — | TBD | TBD |
| CT-ai-v1 | lt/lv/et/en | Optional AI features (ROPA-005) | TBD | — | TBD | TBD |

Rules:

- Append-only. Superseded rows keep their "Shown until" date forever.
- Gaps in coverage (any day with no active version for a purpose) are a
  compliance defect: report immediately per `SECURITY.md`.
