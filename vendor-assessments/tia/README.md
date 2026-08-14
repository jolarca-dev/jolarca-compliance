# Transfer Impact Assessments (Schrems II)

One TIA per non-EU/EEA transfer, following the EDPB Recommendations 01/2020
six-step methodology:

1. Know your transfers (map; from `ropa/master-register.csv`)
2. Identify the transfer tool (SCCs, adequacy, Art. 49 derogation)
3. Assess third-country law & practice (surveillance risk)
4. Identify supplementary measures (encryption, pseudonymization, egress limits)
5. Procedural steps (documented decision)
6. Re-evaluate at appropriate intervals (annual, or on legal change)

File naming: `TIA-<vendor>-v<N>.md`. Signed TIAs are hashed into
`audits/evidence-registry.csv`.

## Index

| ID | Vendor | Transfer | Tool | Status |
|---|---|---|---|---|
| TIA-stripe-01 | Stripe | Payment processing | SCC | draft |
| TIA-openai-01 | OpenAI | LLM inference (PII-filtered) | SCC | draft |
| TIA-anthropic-01 | Anthropic | LLM inference (PII-filtered) | SCC | draft |
| TIA-deepl-01 | DeepL | Translation | SCC | draft |
