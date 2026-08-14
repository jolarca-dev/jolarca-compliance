# RoPA — ai-service (ROPA-005)

| Field | Value |
|---|---|
| Purpose | Translation, embeddings, listing enrichment |
| Lawful basis | Art. 6(1)(b) contract + consent for optional AI features |
| Data categories | Listing text, messages (PII pre-filtered) |
| Subjects | Users, sellers |
| Retention | RC-AI — prompts/outputs short-term only |
| Recipients | DeepL, OpenAI, Anthropic (processors), self-hosted endpoints |
| Transfers | SCC + TIA per vendor (`vendor-assessments/tia/`) |
| Controls | PII pre-filter before egress; egress allowlist; no training on user data; disclosure in UI |

Last reviewed: 2026-08-15 (draft skeleton — populate before G2).
