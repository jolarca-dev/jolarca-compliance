# Risk Register

Reviewed at every gate and quarterly. See `README.md` for scoring model.

## Active Risks

| ID | Category | Description | Likelihood | Impact | Score | Mitigation | Owner | Status |
|----|----------|-------------|-----------|--------|-------|------------|-------|--------|
| RSK-001 | Security | Payment data breach (Stripe token leak) | Low | Very High | High | SAQ-A scope; no PAN stored; Vault secrets; Gitleaks CI | CISO | Active |
| RSK-002 | Security | Vault unseal key compromise | Very Low | Critical | Critical | Split custody (3-of-5); offline storage; no electronic copies | CISO | Active |
| RSK-003 | Compliance | GDPR fine — Art. 9 religious data | Medium | High | High | pgcrypto FLE; no profiling; DPIA-002/003 reviewed | DPO | Active |
| RSK-004 | Compliance | VAT OSS non-compliance | Low | High | High | OSS registration initiated; automated quarterly returns | Finance | Active |
| RSK-005 | Availability | Single Proxmox host failure | Low | Very High | High | Daily backups; offsite copy; restore drill tested quarterly | Infra | Active |
| RSK-006 | Security | WireGuard mesh failure | Low | High | High | Monitoring alerts; incident runbook; <15min detection | Infra | Active |
| RSK-007 | Compliance | DSA Art. 30 — seller KYC incomplete | Medium | Medium | Medium | KYC-lite process; VIES live validation; annual review | Legal | Active |
| RSK-008 | Security | Supply chain attack (dependency) | Medium | High | High | pip-audit + npm audit CI; Dependabot; lockfile hashes | Infra | Active |
| RSK-009 | Availability | VIES gateway downtime | Medium | Low | Low | Format-only fallback; manual review flag; 24h cache | Backend | Active |
| RSK-010 | Compliance | i.SAF filing late | Low | Medium | Medium | Monthly automated export; calendar reminders | Finance | Active |
| RSK-011 | Security | LLM provider data leak (PII in prompts) | Medium | High | High | PII guardrail (fail-closed); no content stored; self-hosted preferred | AI Team | Active |
| RSK-012 | Availability | Backup failure (BorgBackup) | Low | High | High | Staleness alert (25h); weekly restore drill; offsite copy | Infra | Active |
| RSK-013 | Compliance | Cross-border data transfer (OpenAI/Anthropic) | Medium | Medium | Medium | SCCs + TIA; EU provider preferred; PII filtered before egress | DPO | Active |

## Risk Scoring Model

- **Likelihood**: Very Low (1) / Low (2) / Medium (3) / High (4) / Very High (5)
- **Impact**: Low (1) / Medium (2) / High (3) / Very High (4) / Critical (5)
- **Score**: Likelihood × Impact — Low (1-4) / Medium (5-9) / High (10-16) / Critical (17-25)

## Review History

| Date | Reviewer | Changes |
|------|----------|---------|
| 2026-09-02 | Compliance Team | Initial register populated (13 risks) |
