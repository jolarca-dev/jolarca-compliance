# Retention Schedule — per-country matrix

Retention classes referenced by `ropa/master-register.csv`, policies 05, and
erasure automation. Statutory retention differs per jurisdiction: **there is
no single Baltic number.** Where erasure conflicts with a legal hold, apply
ADR-0001 (anonymize-don't-delete).

Sourcing rule: every statutory value below cites its source. Values not yet
confirmed against the primary source are `[COUNSEL-TO-CONFIRM]` and must
never be asserted as fact in downstream artifacts.

## 1. Product retention classes (jurisdiction-independent)

| Class | Data | Operational retention | Erasure rule |
|---|---|---|---|
| RC-ACCOUNT | Identity, contact, auth | Account lifetime + 2y (contract; limitation periods `[COUNSEL-TO-CONFIRM]` per country) | Hard delete after expiry |
| RC-KYC | Seller verification docs | 5y after offboarding (AML/KYC basis `[COUNSEL-TO-CONFIRM]` per country) | Anonymize per ADR-0001 |
| RC-FINANCIAL | Orders, invoices, payment refs | **Per-country statutory matrix (§2)** — not a flat period | Anonymize; keep fiscal fields |
| RC-PAYROLL-50Y | Employment-adjacent personal data in payout/verification records (where applicable) | **Per-country statutory matrix (§2)** | Anonymize; legal-hold override; **DPO review required** |
| RC-AI | Prompts/outputs | ≤ 30 days | Hard delete |
| RC-LOCATION | Geolocation history | ≤ 90 days | Hard delete |
| RC-SUPPORT | Support cases | 3y after closure | Hard delete |
| RC-LOGS | Audit logs | 5y | Archive then delete |
| RC-DSR-VERIFY | DSR identity verification material | Deleted after verification (GDPR Art. 12(6) minimization) | Immediate |
| RC-EVIDENCE | Finalized compliance evidence | 10y minimum / per legal advice | Never delete; archive |

## 2. Statutory retention matrix (country × record class)

| Country | Accounting / financial documents | Payroll / personnel-adjacent records | Other statutory holds |
|---|---|---|---|
| **LT** | **10 years** — Law on Accounting of the Republic of Lithuania (*Lietuvos Respublikos apskaitos įstatymas*; the law defines storage of accounting documents — Ministry of Finance of the Republic of Lithuania, finmin.lrv.lt). Exact article `[COUNSEL-TO-CONFIRM]` | **Up to 50 years** (distinct class — NOT part of the accounting row; applies to designated payroll/personnel documentation) — Lithuanian archival rules for personnel documents; exact instrument & scope `[COUNSEL-TO-CONFIRM]` | `[COUNSEL-TO-CONFIRM]` |
| **LV** | `[COUNSEL-TO-CONFIRM]` | `[COUNSEL-TO-CONFIRM]` | `[COUNSEL-TO-CONFIRM]` |
| **EE** | `[COUNSEL-TO-CONFIRM]` | `[COUNSEL-TO-CONFIRM]` | `[COUNSEL-TO-CONFIRM]` |

Verification state: LT rows corroborated 2026-08-17 (STEP 26) against the
Ministry of Finance instrument listing and practitioner sources; article
numbers and LV/EE values await local counsel. Do not quote periods from this
file in regulator-facing documents until counsel signs off (§4).

## 3. Impact analysis — product artifacts → classes (STEP 26, 2026-08-17)

| Product artifact | Class | LT period | Erasure design |
|---|---|---|---|
| Order records, invoices, payment references | RC-FINANCIAL | 10y | Anonymize-don't-delete (ADR-0001) — **holds** |
| i.SAF FR0600 invoice-register filings & source data | RC-FINANCIAL | 10y | Same as invoices (register mirrors them) |
| Seller KYC/verification dossiers (business data only) | RC-KYC | 5y operational | Anonymize per ADR-0001 |
| Seller payout / verification records touching **employment-adjacent personal data** (e.g., individual-activity sellers, worker-like arrangements) | RC-PAYROLL-50Y candidate | up to 50y if class confirmed | Anonymize still technically applicable, but the legal-hold window extends decades: **legal-hold override of GDPR Art. 17 erasure (Art. 17(3)(b) legal obligation) documented; flagged for DPO review** |
| Buyer-side personal data on invoices | RC-FINANCIAL | 10y | Identifiers anonymized; fiscal fields retained |

Collision note: for RC-PAYROLL-50Y, anonymize-don't-delete remains the
mechanism, but response letters must cite the overriding legal obligation and
the extended hold; the 30-day DSR clock is met by the anonymization act, not
by full deletion. Counsel must confirm which payout/verification records
actually fall in the 50-year class — until then, treat candidates as
RC-FINANCIAL (10y) with a **do-not-delete flag** `[COUNSEL-TO-CONFIRM]`.

## 4. Rules

1. Classes are exhaustive: any new data flow must map to a class before go-live.
2. Legal hold suspends expiry; hold release documented by legal.
3. Erasure automation is tested quarterly (evidence → gate folders).
4. Per-country statutory values require counsel sign-off rows below before
   regulator-facing use — do not assume uniformity across LT/LV/EE.
5. Flat-period citations ("10 years Baltic-wide") are prohibited in all
   artifacts; cite this matrix. (Prior flat citations corrected 2026-08-17,
   STEP 26 — see `STEP26_CORRECTIONS.md`.)

## Counsel sign-off ledger

| Country | Confirmed by | Date | Scope |
|---|---|---|---|
| LT (10y accounting) | `[COUNSEL-TO-CONFIRM]` | — | article number |
| LT (up to 50y payroll) | `[COUNSEL-TO-CONFIRM]` | — | instrument + record scope |
| LV | `[COUNSEL-TO-CONFIRM]` | — | all classes |
| EE | `[COUNSEL-TO-CONFIRM]` | — | all classes |
