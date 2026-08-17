# Regulatory Obligations Register

Registered statutory filing/reporting obligations. A recurring obligation
that is not registered here is a latent fine: **missed monthly filings surface
only when the penalty arrives.** Every entry carries an owner, a cadence, and
a source. Unverified values are `[COUNSEL-TO-CONFIRM]`.

## Register

| ID | Obligation | Jurisdiction | Authority & channel | Cadence & deadline | Owner | Source |
|---|---|---|---|---|---|---|
| OBL-001 | **i.SAF — digital VAT invoice register (form FR0600)**: structured XML register of issued/received VAT invoices; **nil report required even with zero invoices** | LT | State Tax Inspectorate (VMI) via Mano VMI (vmi.lt) | **Monthly — by the 20th day of the following month** | Finance (filing) + Compliance (calendar & evidence) | VMI i.SAF specification (vmi.lt/evmi/i.saf); corroborated 2026-08-17 (STEP 26) |
| OBL-002 | VAT OSS declarations (cross-border B2C) | EU | `[COUNSEL-TO-CONFIRM]` channel per scheme | `[COUNSEL-TO-CONFIRM]` | Finance | RSK-011 routing to jol-m-legal + tax advisor |

Penalties for non-filing: `[COUNSEL-TO-CONFIRM]` amounts (do not assert).

## Recurring compliance calendar (monthly view)

| Day | Obligation | Evidence after completion |
|---|---|---|
| ≤ 20th (monthly) | OBL-001 i.SAF FR0600 submission for prior month (incl. nil report) | Submission confirmation archived by finance; ledger row below |
| Quarterly | Access review (workflow), DPO report | `audits/access-reviews/`, `management-review/dpo-reports/` |
| Monthly | Policy review reminder, DSR SLA monitor | workflow issues |

## i.SAF filing ledger (append-only)

| Period | Submitted | FR0600 version | Filings type | Submitted by | Confirmation ref |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## Engineering dependency

FR0600 export must be producible from the finance marts (jol-m-data):
issue tracked in jol-m-data — "i.SAF FR0600 export: monthly invoice-register
XML from finance marts" (spec against VMI schema; Lithuanian pilot scope
first). Source models: `fct_vat_oss`, invoice data.
