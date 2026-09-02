---
title: "DPIA 002 — AI Processing (LLM Egress)"
version: "1.0.0"
status: "reviewed"
owner: "Compliance Team"
dpo: "DPO — journeyoflife.org"
reviewers: ["Legal Counsel", "CISO"]
created: "2026-09-02"
review_date: "2027-01-15"
linked_ropa: ["ROPA-005"]
gate: "G2"
---

# DPIA 002 — AI Processing (LLM Egress)

## 1. Processing Description

### Purpose
AI-assisted catalog translation, product description generation, and
search embedding. Outbound calls to LLM providers (self-hosted, DeepL,
OpenAI, Anthropic) with PII guardrails.

### Data Subjects
- **Sellers**: product data submitted for translation/enrichment.
- **Buyers**: search queries (if AI-enhanced search is enabled).

### Personal Data Categories

| Data Category | Subjects | Special Category (Art. 9)? |
|---------------|----------|---------------------------|
| Product titles/descriptions | Sellers | **Potentially** — sacred/religious goods |
| Product images (URLs) | Sellers | No |
| Search queries | Buyers | **Potentially** — religious intent |
| Seller business name | Sellers | No |

**Art. 9 flag**: Product descriptions for sacred/religious goods may
reveal religious beliefs when sent to LLM providers. The PII guardrail
filters personal data but does NOT filter religious content indicators.

### Data Flows
```
Seller dashboard → Django backend → ai_service_app
  ├── PII guardrail check (filters names, emails, phones)
  ├── Provider routing (self-hosted → DeepL → OpenAI → Anthropic)
  ├── Outbound HTTPS to provider API
  └── AIRequestLog (append-only audit — NO prompt/response content stored)
```

### Legal Basis

| Processing | Lawful Basis | Reference |
|-----------|-------------|-----------|
| Translation | Art. 6(1)(b) — contract performance | Seller Agreement §6 |
| Search embedding | Art. 6(1)(f) — legitimate interest | Privacy Policy §7 |

### Retention

| Data | Retention | Deletion |
|------|-----------|----------|
| AIRequestLog (metadata only) | 2 years | Nightly retention sweep |
| Prompt/response content | NOT STORED | N/A — deliberately excluded |

## 2. Necessity & Proportionality

- **Product data to LLM**: Necessary for translation service. Proportional —
  sellers opt in explicitly.
- **PII guardrail**: Filters personal data before egress. Mandatory — no
  outbound call without passing the guardrail.
- **No content storage**: Prompt/response content is deliberately NOT stored
  to avoid retaining residual PII or religious belief data.

## 3. Risk Assessment

| Risk Scenario | Likelihood | Impact | Mitigation | Residual |
|---------------|-----------|--------|------------|----------|
| PII leak to LLM provider | Medium | High | PII guardrail (fail-closed); no content stored | Medium |
| Religious data in prompts | High | Medium | Seller informed consent; self-hosted preferred | Medium |
| Provider data breach | Low | High | SCCs + TIA for non-EU providers; self-hosted fallback | Medium |
| Model hallucination in descriptions | Medium | Low | Human review required before publishing | Low |

## 4. Technical & Organizational Measures

- **PII guardrail**: Fail-closed — if guardrail fails, call is blocked.
  Regex + NER filtering for names, emails, phones, addresses.
- **Provider preference**: Self-hosted (Qwen) preferred over third-party.
  DeepL (EU) preferred over OpenAI/Anthropic (US).
- **No content retention**: AIRequestLog stores only metadata (purpose,
  provider, char counts, latency, status). Prompt/response content is
  deliberately excluded.
- **Audit trail**: Every outbound call logged with timestamp, purpose,
  provider, and guardrail status.

## 5. Processor Check

| Processor | DPA Status | Location | Sub-processors |
|-----------|-----------|----------|----------------|
| Self-hosted (Qwen) | N/A (internal) | EU (Proxmox) | None |
| DeepL | Signed DPA | DE (EU) | None disclosed |
| OpenAI | SCC + TIA | US | See OpenAI sub-processor list |
| Anthropic | SCC + TIA | US | See Anthropic sub-processor list |

## 6. Legal-Text Impact

| Text | Impact | Version Bump |
|------|--------|-------------|
| Privacy Policy | §7 (AI processing) | MINOR |
| Seller Agreement | §6 (AI translation) | MINOR |

## 7. Conclusion & Sign-off

**Residual risk acceptable: YES, with conditions.**
1. PII guardrail must remain fail-closed (AI_PII_FILTER_ENABLED=true)
2. Self-hosted provider preferred for religious/sensitive content
3. No prompt/response content stored (verified by code review)

- DPO consulted: [PENDING]
- Approved by: [PENDING]
- Date: [PENDING]
- SHA-256: [COMPUTE AFTER SIGNATURE]
