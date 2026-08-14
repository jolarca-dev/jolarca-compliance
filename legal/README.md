# Legal Texts

Versioned, per-language, regulator-facing. The highest version with recorded
sign-off is the authoritative text.

| Path | Content |
|---|---|
| `terms-of-service/` | ToS per language (lt/lv/et/en) |
| `privacy-policy/` | Privacy policy per language + diff log |
| `cookie-policy/` | Cookie policy + consent banner spec |
| `seller-agreement/` | Marketplace commission terms, Stripe Connected flow |
| `imprint/` | Legal entity disclosures per LT/LV/EE |

## Versioning contract (all subfolders)

1. Files: `<doc>-v<N>.md`; deployed texts are immutable.
2. Each file carries: effective date, approved by (legal + DPO for privacy),
   publication channel (URL/app screen).
3. Changes ship only via PR with DPO approval (`legal/` CODEOWNERS) and a
   CHANGELOG entry; the deployment ledger (which version shown when) is
   kept in the product release notes and referenced here.
4. Privacy policy versions additionally maintain a diff log (what changed,
   why, re-consent impact assessment).
