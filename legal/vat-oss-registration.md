---
title: "VAT OSS Registration Status"
version: "1.0.0"
status: "initiated"
created: "2026-09-02"
owner: "Compliance Team"
---

# VAT OSS (One-Stop-Shop) Registration

## Status: INITIATED — Registration in Progress

The VAT OSS registration is a long-lead legal item. This document tracks
the registration process and provides evidence for audit purposes.

## What is VAT OSS?

The VAT One-Stop-Shop (OSS) is an EU scheme that allows businesses selling
goods/services to consumers in other EU member states to account for VAT
in a single return, filed in their identity member state (LT for Jolarca).

Without OSS, Jolarca would need to register for VAT in every EU country
where it has customers — a massive compliance burden.

## Registration Details

| Field | Value |
|-------|-------|
| Identity Member State | Lithuania (LT) |
| Tax Authority | Valstybinė mokesčių inspekcija (VMI) |
| Registration Form | FR0600 (OSS registration section) |
| Applicant | [Company name — from corporate/formation.md] |
| Company Code | [Company code] |
| VAT Number | LT[company VAT number] |
| Date Initiated | [DATE — when registration was submitted to VMI] |
| Expected Approval | [DATE — typically 4-8 weeks] |
| Registration Number | [PENDING — assigned by VMI upon approval] |

## Registration Steps

1. **[ ] Prepare OSS registration documentation**
   - Company registration certificate
   - VAT registration certificate
   - Proof of business activity (marketplace ToS, seller agreements)
   - List of destination member states (LT, LV, EE initially)

2. **[ ] Submit FR0600 to VMI**
   - Via VMI portal (https://vas.vmi.lt) or in-person
   - Include OSS election section
   - Reference: EU VAT Directive Art. 369c

3. **[ ] Receive OSS registration number**
   - VMI processes within 4-8 weeks
   - Registration number format: LT-OSS-XXXXXX
   - Effective date = date of registration

4. **[ ] Configure OSS in marketplace**
   - Set identity member state (LT) in settings
   - Enable OSS return generation (quarterly)
   - Configure VAT rate snapshots for all destination countries

5. **[ ] First OSS return**
   - Due: end of month following the quarter
   - Q1 (Jan-Mar): due April 30
   - Q2 (Apr-Jun): due July 31
   - Q3 (Jul-Sep): due October 31
   - Q4 (Oct-Dec): due January 31

## OSS Return Process

The `prepare_oss_return` Celery task aggregates taxable amounts and VAT
due per member state for each quarter. The output is stored in
`OssReturnData` for review by the finance team.

**The OSS return is NEVER auto-submitted.** The finance team reviews the
aggregated data and submits via the VMI portal manually.

## Linked Artifacts

- VAT OSS analysis: `jolarca-legal/platform-regulation/vat-oss/`
- Deemed-supplier analysis: `vat-oss/deemed-supplier-analysis.md`
- OSS mechanics: `vat-oss/oss-mechanics.md`
- VAT rate table: `vat-oss/vat-rate-table.md`
- DPIA-003: `jolarca-compliance/dpia/003-payments-and-vat/dpia.md`
- RoPA-003: `jolarca-compliance/ropa/by-system/orders-payments.md`

## Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| OSS registration delayed | Must register in each destination country | Start early; engage tax counsel |
| VAT rate change mid-quarter | Incorrect OSS return | VatRateSnapshot model captures point-in-time rates |
| OSS return filed late | Penalties from VMI | Calendar reminders; quarterly Celery beat task |
| Destination country disputes | Double taxation | Document place-of-supply rules; engage counsel |

## Action Items

- [ ] Submit OSS registration to VMI (long-lead: 4-8 weeks)
- [ ] Configure `OSS_IDENTITY_MEMBER_STATE` in settings
- [ ] Seed VatRateSnapshot for all EU countries
- [ ] Test OSS return generation with sample data
- [ ] File first OSS return (quarter after registration approved)
