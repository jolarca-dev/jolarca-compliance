# STEP 26 — Regulatory baseline corrections

- **Date:** 2026-08-17
- **Role:** Compliance Officer correcting the regulatory baseline against
  verified primary sources
- **Creed applied:** a compliance document that misstates a statute is worse
  than no document — it gets relied on. Every corrected line carries its
  source; anything unverified stays `[COUNSEL-TO-CONFIRM]`, never asserted.
- **Repos touched:** jol-m-compliance, jol-m-legal, jol-m-data (issue #4)

## Correction 1 — Retention schedule becomes a per-country matrix

**What was wrong:** `docs/retention-schedule.md` asserted a flat
"**10y** (LT Accounting Act; LV/EE variants to verify)" for RC-FINANCIAL, and
downstream artifacts quoted "10y LT/LV/EE" as one number.

**What is now true** (`docs/retention-schedule.md` §1–§4, rewritten):

| Claim | Source |
|---|---|
| LT accounting/financial documents = **10 years** | Law on Accounting of the Republic of Lithuania (*Lietuvos Respublikos apskaitos įstatymas*) — the law defines storage of accounting documents (Ministry of Finance of the Republic of Lithuania, finmin.lrv.lt); period corroborated by practitioner sources. Exact article `[COUNSEL-TO-CONFIRM]` |
| LT payroll/personnel-adjacent records = **up to 50 years** — distinct row, not folded into accounting | Lithuanian archival rules for personnel documentation (practitioner corroboration); exact instrument & record scope `[COUNSEL-TO-CONFIRM]` |
| LV / EE all classes | `[COUNSEL-TO-CONFIRM]` — original flag preserved, kept honest |

**Impact analysis** (matrix §3):

- Order/invoice/payment-reference records → RC-FINANCIAL → LT 10y;
  anonymize-don't-delete **holds**.
- Seller payout/verification records touching employment-adjacent personal
  data → RC-PAYROLL-50Y candidates (LT up to 50y): anonymization remains the
  mechanism, but GDPR Art. 17 erasure is overridden by the legal obligation
  (Art. 17(3)(b)) for decades — **legal-hold override documented, flagged for
  DPO review**; candidates carry a do-not-delete flag until counsel classifies.
- Downstream references updated: `ropa/by-system/orders-payments.md`
  (retention row → matrix; VMI/i.SAF recipient added), ADR-0001
  (Amendment 1 annotated; original text preserved — evidence hygiene:
  annotate, don't rewrite), `risk-register/register.md` RSK-002 annotated.

## Correction 2 — i.SAF obligation registered

| Claim | Source |
|---|---|
| Lithuania i.MAS/i.SAF: structured XML VAT invoice register, **form FR0600**, via **Mano VMI** | State Tax Inspectorate (VMI), i.SAF specification (vmi.lt/evmi/i.saf); corroborated by multiple practitioner references, 2026-08-17 |
| **Monthly, by the 20th** of the following month | same |
| **Nil report required** even with zero invoices | same |
| Penalties for non-filing | `[COUNSEL-TO-CONFIRM]` amounts — not asserted |

**Artifacts:**

- `docs/regulatory-obligations.md` — new register; **OBL-001** with owner
  (Finance + Compliance), recurring calendar row (≤ 20th monthly), filing
  ledger. Root README SLA table extended.
- jol-m-legal: `regulatory/tax-authorities/vmi-lt/2026-08-17-obligation-isaf-fr0600.md`
  (obligation, channel, deadlines, penalty note flagged, open items for the
  tax advisor).
- jol-m-data: **issue #4** — "i.SAF FR0600 export: monthly invoice-register
  XML from finance marts" (spec vs VMI schema; `fct_vat_oss` + invoice
  models; Lithuanian pilot first; nil-month acceptance case).
- `risk-register/register.md` — **RSK-015** added: missed/late monthly filing
  risk (recurring obligations surface only when the penalty arrives).

## Correction 3 — Stripe AoC retrieval + TIA authorship

**What was wrong:** artifacts implied the PCI AoC was a link/public download
and left the TIA's origin ambiguous.

**Corrected everywhere it appears** (`vendor-assessments/stripe/README.md`
artifact map, `vendor-assessments/README.md` onboarding flow + annual cycle,
`audits/gate-evidence/G3-payments/README.md`, `G3_DECISION.md` rows 2–3 +
STEP 26 note, `certifications/pci-dss/README.md`):

| Artifact | Correct statement |
|---|---|
| DPA | Issued by Stripe (Art. 28) |
| SCCs | Referenced within the Stripe DPA (not a standalone download) |
| AoC | **Not a public download.** Stripe Dashboard → **Compliance Settings** → download AoC for the JOL account; if unavailable, **Stripe support request**. Retrieval record: who / when / document version-date (`vendor-assessments/stripe/README.md`) |
| TIA | **Self-authored by JOL**; Stripe supplies DPA/SCCs as inputs only |

Both artifacts join the vendor-review cadence: **annual, or on Stripe
compliance-program update**.

## Close the loop

- `G3_DECISION.md` withheld rows 2–3 now point at these corrected sources;
  evidence gathering remains Step 25b — this step fixes the map it follows.
- Flat-retention assumption corrected **by annotation** (RSK-002, ADR-0001
  Amendment 1) — history preserved, correction visible.
- CHANGELOG `[Unreleased]` records this change set.

## Remaining `[COUNSEL-TO-CONFIRM]` items (open for tax advisor / DPO)

1. LT 10y accounting retention — exact article of the Law on Accounting
2. LT up-to-50y payroll class — exact instrument + which payout/verification
   records fall in scope (drives RC-PAYROLL-50Y classification & DPO review)
3. LV & EE retention for all classes (accounting, payroll/personnel, other)
4. i.SAF: FR0600 schema version in force; penalty regime incl. nil-report
   lapses; marketplace commission line-level identifier requirements
5. VAT OSS channel/cadence (OBL-002) — RSK-011 routing
