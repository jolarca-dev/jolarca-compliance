# Compliance Matrix (MASTER)

Single mapping: **control → product module → infra control → evidence path**.
Build once, map many times — this file is the source for SOC 2, ISO 27001,
and PCI DSS evidence folders. Update with any new control or evidence.

Legend: framework refs — ISO = 27001:2022 Annex A, TSC = SOC 2 CC, PCI = DSS 4.0.

| ID | Control / obligation | Policy | Product module | Infra control | Evidence path | Frameworks |
|---|---|---|---|---|---|---|
| CM-01 | Access control & least privilege | 03 | users-app RBAC | GitHub + IAM + Vault | audits/access-reviews/ | ISO A.5.15–18, TSC CC6 |
| CM-02 | Encryption of personal data | 04 | pgcrypto columns | GCP KMS CMEK | gate-evidence/G1 | ISO A.8.24, TSC CC6.1 |
| CM-03 | Erasure & retention enforcement | 05 | retention jobs | DB policies + vault | gate-evidence/G1, ADR-0001 | ISO A.5.33, TSC P4.3 |
| CM-04 | Incident & breach readiness (72h) | 06 | alerting/on-call | monitoring stack | incidents/, game-days | ISO A.5.24–27, TSC CC7 |
| CM-05 | Vendor/processor governance | 07 | n/a | n/a | vendor-assessments/, tia/ | ISO A.5.19–22, TSC CC9.2 |
| CM-06 | Secure SDLC & vuln SLAs | 08 | CI gates | Dependabot + scanners | audits/ (CI exports) | ISO A.8.25–31, TSC CC8 |
| CM-07 | BCP/DR RTO ≤ 4h RPO ≤ 15 min | 09 | n/a | backups + failover | gate-evidence/ (drills) | ISO A.5.29–30, TSC A1 |
| CM-08 | Training & awareness | 10 | n/a | n/a | training/completion-log.md | ISO A.6.3, TSC CC1.4 |
| CM-09 | Logging & tamper evidence | 11 | audit log service | append-only store | audits/ (log exports) | ISO A.8.15–16, TSC CC7.1 |
| CM-10 | AI egress control (PII ban) | 12 | PII pre-filter | egress allowlist | gate-evidence/G2 | ISO A.5.19, TSC CC9.2 |
| CM-11 | SAQ-A scope (no card data) | 08 | Stripe Checkout | hosted fields only | gate-evidence/G3 | PCI Req 2–4 scope |
| CM-12 | DSR rights within 30 days | 02 | DSR system | erasure APIs | data-subject-requests/sla-reports/ | GDPR Art. 12–22 |
