# Retention Schedule

Retention classes referenced by `ropa/master-register.csv`, policies 05, and
erasure automation. Baltic legal holds apply; where erasure conflicts with a
legal hold, apply ADR-0001 (anonymize-don't-delete).

## Classes

| Class | Data | Retention | Legal basis (indicative) | Erasure rule |
|---|---|---|---|---|
| RC-ACCOUNT | Identity, contact, auth | Account lifetime + 2y | Contract; LT Civil Code limitation | Hard delete after expiry |
| RC-KYC | Seller verification docs | 5y after offboarding | AML/KYC obligations (LT/LV/EE) | Anonymize per ADR-0001 |
| RC-FINANCIAL | Orders, invoices, payment refs | **10y** (LT Accounting Act; LV/EE variants to verify per entity) | Accounting law | Anonymize; keep fiscal fields |
| RC-AI | Prompts/outputs | ≤ 30 days | Consent/purpose | Hard delete |
| RC-LOCATION | Geolocation history | ≤ 90 days | Consent | Hard delete |
| RC-SUPPORT | Support cases | 3y after closure | Legitimate interest (LIA) | Hard delete |
| RC-LOGS | Audit logs | 5y | ISO A.8.15 / forensics | Archive then delete |
| RC-DSR-VERIFY | Identity verification material for DSRs | Deleted after verification | Art. 12(6) minimization | Immediate |
| RC-EVIDENCE | Finalized compliance evidence | 10y minimum / per legal advice | Audit defense | Never delete; archive |

## Rules

1. Classes are exhaustive: any new data flow must map to a class before go-live.
2. Legal hold suspends expiry; hold release documented by legal.
3. Erasure automation is tested quarterly (evidence → gate folders).
4. LT/LV/EE accounting variants must be confirmed per legal entity by local
   counsel before G3 — do not assume uniformity.
