# 12 — AI Usage Policy

| | |
|---|---|
| Version | 0.1 (draft) |
| Owner | DPO + Engineering lead |
| Approved by | Management |
| Next review | 2027-08-15 |
| ISO 27001 | Annex A.5.19 (third-party AI), A.8.28 secure coding |
| SOC 2 | CC8, CC9.2 |

## Requirements

1. **PII egress ban**: no personal data may leave the platform boundary to
   external LLM endpoints without passing the PII pre-filter; the egress
   allowlist is enforced at network level and tested at G2.
2. Vendor selection limited to processors with DPA + TIA on file
   (`vendor-assessments/tia/`); self-hosted endpoints preferred for
   sensitive content.
3. No training of third-party models on user data; opt-outs configured and
   evidenced (contract + API flags).
4. AI-assisted features disclose AI involvement in the UI where required;
   consent ledger tracks acceptance (`lawful-basis/`).
5. Internal staff use of external AI coding assistants: no production
   secrets, no personal data in prompts; violation = incident.
6. Human review required for AI output that affects user rights or payments.
7. Prompt/output retention limited to RC-AI class; no long-term storage.

## Review history

| Version | Date | Author | Approved by |
|---|---|---|---|
| 0.1 | 2026-08-15 | DPO | TBD |
