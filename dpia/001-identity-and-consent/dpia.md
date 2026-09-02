---
version: "1.0.0"
status: "reviewed"
owner: "Compliance Team"
dpo: "DPO — journeyoflife.org"
reviewers: ["Legal Counsel", "CISO"]
created: "2026-09-02"
review_date: "2027-01-15"
linked_ropa: ["ROPA-001", "ROPA-002"]
gate: "G1"
---

# DPIA 001 — Identity and Consent

## 1. Processing Description

### Purpose

Processing of user identity data for registration, authentication,
identity verification (KYC-lite for sellers), and consent management.

### Data Subjects

- **Buyers**: individuals registering accounts to purchase goods.
- **Sellers**: traders registering to sell on the marketplace (KYC-lite).

### Personal Data Categories

| Data Category | Subjects | Special Category (Art. 9)? |
|---------------|----------|---------------------------|
| Email address | Buyers + Sellers | No |
| Password hash (argon2) | Buyers + Sellers | No |
| Full name | Sellers | No |
| Identity document scan | Sellers | No (but high-risk) |
| Business registration number | Sellers | No |
| Consent records | Buyers + Sellers | No |
| Login IP + timestamp | Buyers + Sellers | No |

### Data Flows

```text
User browser → [TLS] → nginx edge → Django backend
  ├── Registration → jol_marketplace.users_user (pgcrypto encrypted fields)
  ├── Authentication → Django auth + django-axes (brute-force protection)
  ├── Seller KYC → jol_marketplace.sellers_app_seller (document scan in MinIO)
  ├── Consent → jol_marketplace.consent_records (append-only)
  └── Audit → jol_marketplace.compliance_app_auditlog (append-only)
```

### Legal Basis

| Processing | Lawful Basis | Reference |
|-----------|-------------|-----------|
| Registration | Art. 6(1)(b) — contract performance | ToS §2 |
| Authentication | Art. 6(1)(b) — contract performance | ToS §2 |
| Seller KYC | Art. 6(1)(c) — legal obligation (DSA Art. 30) | Seller Agreement §3 |
| Consent records | Art. 6(1)(c) — legal obligation (GDPR Art. 7) | Privacy Policy §5 |

### Retention

| Data | Retention | Deletion Mechanism |
|------|-----------|-------------------|
| User account | Until erasure request | Anonymize (ADR-0001) |
| Identity documents | 5 years after relationship ends | Delete from MinIO |
| Consent records | Duration of consent + 5 years | Anonymize |
| Login audit log | 2 years | Nightly retention sweep |

## 2. Necessity & Proportionality

- **Email**: Required for account recovery and communication. Proportional.
- **Password hash**: Required for authentication. Argon2 is state-of-the-art.
- **Identity documents**: Required by DSA Art. 30 for trader verification. Proportional — stored encrypted in MinIO, access restricted.
- **Consent records**: Required by GDPR Art. 7 for accountability. Proportional.

## 3. Risk Assessment

| Risk Scenario | Likelihood | Impact | Mitigation | Residual |
|---------------|-----------|--------|------------|----------|
| Identity document leak | Low | Very High | MinIO encrypted at rest; access logging; pgcrypto FLE | Medium |
| Credential stuffing | Medium | Medium | django-axes brute-force protection; rate limiting at edge | Low |
| Consent record tampering | Low | High | Append-only audit log; DB-level restrictions | Low |
| Seller impersonation | Low | High | KYC-lite verification; VIES for VAT numbers | Low |

## 4. Technical & Organizational Measures

- **Encryption at rest**: pgcrypto for sensitive user fields; MinIO SSE for documents
- **Encryption in transit**: TLS 1.2+ everywhere; PostgreSQL sslmode=verify-full
- **Access control**: Django RBAC; seller docs accessible only to compliance team
- **Breach detection**: django-axes, audit log, Alertmanager alerts
- **Residency**: EU-only (Proxmox bare metal + EU offsite backup)

## 5. Processor Check

No new processors introduced. Existing: Stripe (payments), DPD/Omniva (shipping).

## 6. Legal-Text Impact

| Text | Impact | Version Bump |
|------|--------|-------------|
| Privacy Policy | §3 (identity processing) | MINOR |
| Terms of Service | §2 (registration) | MINOR |
| Seller Agreement | §3 (KYC) | MINOR |

## 7. Conclusion & Sign-off

**Residual risk acceptable: YES.** Identity document risk is mitigated by
encryption + access control. Credential risk is mitigated by axes + rate limiting.

- DPO consulted: [PENDING]
- Approved by: [PENDING]
- Date: [PENDING]
- SHA-256: [COMPUTE AFTER SIGNATURE]
