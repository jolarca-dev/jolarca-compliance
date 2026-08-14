# RoPA — sellers-app (ROPA-002, ROPA-004)

| Field | Value |
|---|---|
| Purpose | Seller onboarding, KYC verification, VIES VAT validation |
| Lawful basis | Art. 6(1)(c) legal obligation; Art. 6(1)(b) contract |
| Data categories | Identity documents, business registry data, VAT ID |
| Subjects | Sellers |
| Retention | RC-KYC, RC-FINANCIAL — see `docs/retention-schedule.md` |
| Recipients | Verification provider, EU VIES service |
| Transfers | EU-only processing |
| Controls | Document encryption at rest; least-privilege reviewer role; erasure via anonymization (ADR-0001) |

Last reviewed: 2026-08-15 (draft skeleton — populate before G1).
