# Certifications & Audit Tracker

## Active Certifications

| Certification | Scope | Status | Auditor | Issue Date | Expiry | Report |
|--------------|-------|--------|---------|-----------|--------|--------|
| SOC 2 Type II | Marketplace platform | **Planned** | [TBD] | — | — | — |
| ISO 27001:2022 | Marketplace platform | **Planned** | [TBD] | — | — | — |
| PCI DSS SAQ-A | Payment processing (Stripe) | **In Progress** | Self-assessment | — | Annual | — |

## Planned Audit Timeline

| Quarter | Activity | Owner | Status |
|---------|----------|-------|--------|
| Q4 2026 | SOC 2 Type I readiness assessment | CISO | Planned |
| Q1 2027 | SOC 2 Type I audit | External auditor | Planned |
| Q2 2027 | ISO 27001 Stage 1 audit | External auditor | Planned |
| Q3 2027 | ISO 27001 Stage 2 audit (certification) | External auditor | Planned |
| Q4 2027 | SOC 2 Type II audit (6-month observation) | External auditor | Planned |
| Q2 2028 | PCI DSS SAQ-A annual re-validation | CISO | Planned |

## Pre-Requisites (Before External Audit)

- [x] All DPIAs reviewed (001-004)
- [x] Risk register populated
- [x] Vendor assessments completed
- [x] Incident response plan documented
- [x] Backup + restore drill operational
- [x] Monitoring stack deployed
- [x] CodeQL + Trivy CI gates active
- [ ] 3-month evidence collection period
- [ ] Internal audit completed
- [ ] Management review completed

## Evidence Collection

Evidence for certifications is collected continuously:

| Control Area | Evidence Source | Collection Frequency |
|-------------|----------------|---------------------|
| Access control | Vault audit log, Proxmox auth log | Continuous |
| Change management | Git history, PR reviews | Per commit |
| Incident response | Incident runbook execution logs | Per incident |
| Backup/DR | Restore drill logs | Quarterly |
| Vulnerability management | CodeQL + Trivy scan results | Per PR + weekly |
| Encryption | TLS cert inventory, pgcrypto config | Monthly |

## Document References

- `policies/` — 12 ISO 27001-aligned policies
- `risk-register/register.md` — Active risk register
- `dpia/` — All DPIAs (001-004)
- `vendor-assessments/` — Vendor risk assessments
