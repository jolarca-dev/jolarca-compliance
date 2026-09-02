---
title: "DPIA 003 — Payments and VAT Data Processing"
version: "1.0.0"
status: "reviewed"
owner: "Compliance Team"
dpo: "DPO — journeyoflife.org"
reviewers: ["Legal Counsel", "CISO"]
created: "2026-09-02"
review_date: "2027-01-15"
linked_ropa: ["ROPA-003", "ROPA-004"]
gate: "G3"
---

# DPIA 003 — Payments and VAT Data Processing

## 1. Processing Description

### Purpose of Processing

Processing of payment and VAT-related personal data for the Jolarca
marketplace to: (a) process buyer payments via Stripe, (b) validate seller
VAT numbers via the EU VIES gateway, (c) issue commercial invoices, and
(d) fulfill VAT OSS reporting and i.SAF (SAF-T) filing obligations.

### Categories of Data Subjects

- **Buyers**: individuals purchasing goods on the marketplace.
- **Sellers**: registered traders receiving payouts.
- **Tax authorities**: VMI (LT), VID (LV), EMTA (EE) — recipient-only.

### Categories of Personal Data

| Data Category | Subjects | Special Category (Art. 9)? |
|---------------|----------|---------------------------|
| Name, email, delivery address | Buyers | No |
| Payment token (Stripe `payment_method` ID) | Buyers | No |
| Shipping address, parcel-locker preference | Buyers | No |
| VAT identification number | Sellers | No |
| Bank account details (for payouts) | Sellers | No |
| Invoice data (amounts, VAT, dates) | Buyers + Sellers | No |
| Religious/sacred product category tags | Buyers | **Yes** — indirect Art. 9 (reveals religious beliefs via purchase of sacred goods) |

**Art. 9 flag**: The marketplace sells funeral, religious, and sacred goods.
Purchase of these items indirectly reveals religious beliefs (Art. 9(1) GDPR).
The product category is processed at the order-item level. This DPIA
explicitly assesses this as high-risk processing requiring enhanced safeguards.

### Data Flows

```
Buyer browser → [TLS] → nginx edge → Django backend
  ├── Stripe Elements (client-side tokenization) → Stripe API (PCI DSS SAQ-A)
  │     └── payment_method token → jol_marketplace.orders (no PAN stored)
  ├── Order data → jol_marketplace.orders + order_items
  │     └── product_category (may reveal religious belief) → encrypted at rest (pgcrypto)
  ├── Invoice → jol_marketplace.commercial_invoices (immutable, append-only)
  └── VAT check → VIES SOAP gateway (ec.europa.eu) → result cached 24h

Seller dashboard → Django backend
  ├── VAT number → VIES live check → stored as verified/unverified
  ├── Payout details → Stripe Connect (processor) → bank account token
  └── Invoice data → i.SAF FR0600 monthly export → VMI/VID/EMTA

Monthly: i.SAF FR0600 XML export → VMI (LT) / VID (LV) / EMTA (EE)
Quarterly: OSS return → VMI (identity member state)
```

### Legal Basis (Art. 6)

| Processing Activity | Lawful Basis | Reference |
|--------------------|-------------|-----------|
| Payment processing | Art. 6(1)(b) — contract performance | ToS §4 |
| Invoice issuance | Art. 6(1)(c) — legal obligation (Accounting Law) | LT Law on Accounting Art. 8 |
| VAT validation (VIES) | Art. 6(1)(c) — legal obligation (VAT Directive) | EU VAT Directive Art. 369a |
| i.SAF filing | Art. 6(1)(c) — legal obligation (SAF-T Law) | LT Minister of Finance Order V-135 |
| OSS reporting | Art. 6(1)(c) — legal obligation (VAT OSS) | EU VAT Directive Art. 369c |
| Religious product category | Art. 6(1)(b) — contract performance | ToS §4; Art. 9(2)(a) — explicit consent not required as processing is incidental to contract |

### Retention Period & Deletion Mechanism

| Data | Retention | Authority | Deletion Mechanism |
|------|-----------|-----------|-------------------|
| Order data (non-financial) | 5 years from order date | LT Civil Code limitation | Nightly retention sweep → anonymize |
| Commercial invoices | 10 years (LT), 10 years (LV), 10 years (EE) | Accounting Laws | ANONYMIZE, never delete (ADR-0001) |
| Payment tokens (Stripe) | Until order fulfilled + 30 days | Stripe DPA | Token deletion via Stripe API |
| VAT validation results | 24 hours (cache), then deleted | Minimization | Automatic cache expiry |
| i.SAF filings | 10 years | Tax authority retention | Archive → anonymize after period |
| OSS return data | 10 years | VAT OSS regulations | Archive → anonymize after period |

## 2. Necessity & Proportionality

### Why is each data element necessary?

| Data Element | Necessity | Proportionality |
|-------------|-----------|-----------------|
| Buyer name + address | Required for delivery and invoice | Proportional — no alternative for physical goods |
| Payment token | Required for payment processing | Proportional — Stripe tokenizes; no PAN stored |
| Product category (sacred) | Incidental to marketplace function | Proportional — category is functional, not profiling |
| Seller VAT number | Legally required for B2B validation | Proportional — VIES check is mandatory under VAT Directive |
| Bank account (payouts) | Required for seller payouts | Proportional — Stripe Connect handles; no raw IBAN stored |

### Minimization Measures

- **Payment data**: Stripe Elements performs client-side tokenization. No
  Primary Account Number (PAN) or CVC ever reaches the Jolarca backend.
  SAQ-A scope confirmed.
- **Religious product data**: Product category is stored as a functional
  tag (e.g., "funeral", "sacred"), not as a religious belief attribute.
  No profiling or inference is performed. Encrypted at rest via pgcrypto.
- **VAT validation**: VIES results cached for 24 hours only. No persistent
  storage of VIES responses beyond the verification status.
- **Invoices**: Immutable but anonymized after retention period. The
  buyer-seller linkage is severed; the financial evidence survives.

### Alternatives Considered and Rejected

| Alternative | Rejected Because |
|------------|-----------------|
| No VIES check (format-only) | Legally insufficient for reverse-charge; VAT fraud risk |
| Store full card numbers | PCI DSS SAQ-A would become SAQ-D; disproportionate compliance burden |
| Delete invoices after retention | Illegal under LT/LV/EE accounting laws (10-year mandatory retention) |
| Collect religious belief explicitly | Unnecessary — category is functional, not personal belief |

## 3. Risk Assessment (to Rights & Freedoms)

| Risk Scenario | Likelihood | Impact | Risk Level | Mitigation | Residual Risk |
|---------------|-----------|--------|-----------|------------|--------------|
| Payment token leakage (Stripe breach) | Low | High | **High** | Stripe PCI DSS Level 1; SAQ-A scope; no PAN stored | Medium |
| Religious product data reveals beliefs | Medium | High | **High** | pgcrypto encryption; no profiling; functional category only | Medium |
| VIES gateway compromise | Low | Medium | Medium | HTTPS only; 24h cache; no persistent storage | Low |
| Invoice data breach (10-year retention) | Low | High | **High** | Encryption at rest (pgcrypto); access logging; immutable store | Medium |
| i.SAF filing contains personal data | Medium | Medium | Medium | Filing contains VAT numbers only; encrypted in transit (TLS) | Low |
| Reverse-charge applied incorrectly | Medium | Medium | Medium | VIES live check required; dual verification (buyer + seller) | Low |
| OSS return data breach | Low | Medium | Medium | Encrypted at rest; access restricted to finance team | Low |

## 4. Technical & Organizational Measures

### Encryption

- **At rest**: pgcrypto field-level encryption for religious product
  categories and invoice buyer linkage. Full-disk encryption on DB host
  (LUKS). BorgBackup encryption (repokey-blake2).
- **In transit**: TLS 1.2+ everywhere. PostgreSQL requires `hostssl`
  connections. nginx enforces HSTS with preload. WireGuard mesh for
  service-to-service traffic.

### Access Control

| Role | Access | Grant Mechanism | Review Cadence |
|------|--------|----------------|----------------|
| App user (jol_app) | Read/write marketplace DB | Vault credentials | Quarterly |
| Readonly user (jol_readonly) | SELECT only | Vault credentials | Quarterly |
| Finance team | Invoice data, OSS returns | RBAC in Django admin | Quarterly |
| DPO | All processing records | Read-only access to audit logs | Ongoing |
| Stripe | Payment tokens only | API key (scoped) | Per Stripe DPA |

### Residency

All personal data resides in the EU:
- **Primary**: Proxmox bare metal in EU datacenter (LT)
- **Backup**: EU-based offsite storage (Hetzner or equivalent)
- **Stripe**: EU entity (Stripe Payments Europe Ltd, Dublin)
- **No third-country transfers** except Stripe US (covered by SCC + TIA)

### Breach Detection & Notification

- **Detection**: AuditLog (append-only), backup staleness monitor,
  CodeQL + Trivy on every PR, Gitleaks secret scanning.
- **Notification path**: See `SECURITY.md` → Incident Response Plan.
- **72-hour SLA**: Art. 33 notification to VDAI (lead SA) within 72 hours
  of breach awareness. DPO notified immediately.

## 5. Processor/Sub-processor Check

| Processor | DPA Status | Location | Sub-processors |
|-----------|-----------|----------|----------------|
| Stripe (payments) | Signed DPA (controller-processor) | IE (EU) | See Stripe sub-processor list |
| DPD (shipping) | Signed DPA | LT | None disclosed |
| Omniva (shipping) | Signed DPA | LT | None disclosed |
| VMI/VID/EMTA (tax) | Statutory recipient (not processor) | LT/LV/EE | N/A |

**Stripe as processor**: Stripe Payments Europe Ltd (Dublin, IE) is the
EU entity. SCCs + TIA documented in `vendor-assessments/tia/`. Stripe
sub-processor list reviewed quarterly.

## 6. Legal-Text Impact

| Legal Text | Impact | Version Bump |
|-----------|--------|-------------|
| Terms of Service | §4 (payments) updated to reference VIES live check | MINOR |
| Privacy Policy | §3 (payment processing) updated with VIES + i.SAF recipients | MINOR |
| Seller Agreement | §5 (VAT validation) updated with live VIES requirement | MINOR |
| Cookie Policy | No change | — |
| Buyer Terms | No change | — |

**Consent re-evaluation**: Not required. The VIES check and i.SAF filing
are legal obligations (Art. 6(1)(c)), not consent-based. The religious
product category processing is incidental to contract performance.

## 7. Conclusion & Sign-off

### Residual Risk Assessment

**Residual risk acceptable: YES, with conditions.**

The high-risk items (payment token leakage, religious data exposure,
invoice breach) are mitigated by:
- Stripe SAQ-A (no PAN stored)
- pgcrypto encryption for religious product data
- Immutable, encrypted invoice storage with access logging
- Backup encryption (BorgBackup repokey-blake2)

The conditions for acceptance:
1. VIES live validation must be implemented (this DPIA blocks until done)
2. i.SAF monthly export must be operational
3. First restore drill must pass (P4 deliverable)
4. CodeQL + Trivy must be green across all repos

### DPO Consultation (Art. 35.2)

- **DPO consulted**: Yes
- **Date**: [PENDING — route to DPO for signature]
- **DPO name**: [DPO name]
- **DPO opinion**: [PENDING]

### Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Compliance Lead | [name] | [PENDING] | [date] |
| DPO | [name] | **[PENDING — REQUIRED]** | [date] |
| CISO | [name] | [PENDING] | [date] |
| Legal Counsel | [name] | [PENDING] | [date] |

### Hash Pinning

Upon DPO signature, compute SHA-256 of this document and record in
`audits/evidence-registry.csv`. The signed DPIA is immutable; any
amendment requires a new version with a new hash.

```
SHA-256: [COMPUTE AFTER SIGNATURE]
```

### Linked Artifacts

- RoPA: ROPA-003 (orders-payments), ROPA-004 (sellers VIES)
- Gate: G3 (SAQ-A validation, VIES live, replay-attack tests)
- Retention: `docs/retention-schedule.md` R1 (contracts + 10y)
- DPA: `contracts/00-templates/dpa-controller-processor.md` (Stripe)
- ADR: ADR-0001 (anonymize-don't-delete), ADR-0005 (single payment boundary)
