# G3 decision record — payment boundary

- **Date:** 2026-08-17
- **Decider role:** independent audit persona (STEP 22c re-audit)
- **Inputs:** `reports/STEP22C_FINAL_REAUDIT.md`, `evidence-manifest.md`,
  `certifications/pci-dss/scope-statement-model-a.md`,
  `risk-register/register.md` closure record

## Decision: CONDITIONAL CLEARANCE

**CLEARED:** the Model A payment boundary passes G3's payment controls.
SAQ-A scope validation and replay-attack testing are PROVEN with
independently reproduced evidence (no inherited claims). jol-hub is out
of PCI scope; the scope statement is upgraded CONDITIONAL → PROVEN.

**WITHHELD:** authorization of the FIRST REAL DONATION, pending:

| # | Item | Owner | Class |
|---|---|---|---|
| 1 | DPIA 003 signed + hash (currently draft skeleton) | DPO | compliance |
| 2 | VIES VAT reconciliation evidence (i.SAF FR0600 source data included — see `docs/regulatory-obligations.md` OBL-001; corrected source map: STEP 26) | Compliance/Legal | compliance |
| 3 | Stripe TIA (JOL-self-authored) + AoC in vendor register — retrieval procedure corrected 2026-08-17 (STEP 26 C3): AoC = Stripe Dashboard → Compliance Settings, else support request; NOT a public download | Compliance | compliance |
| 4 | RSK-013: contract suite wired into jolarca CI as a REQUIRED check (boundary repo currently ungated) | Marketplace | engineering |
| 5 | RSK-014: internal refund endpoint wired to PSP-side execution | Marketplace | engineering |
| 6 | RSK-012: E3 rows deployed on the hub production k8s plane | Infra | engineering (gates hub production go-live, not the donation itself) |

## Rationale

Items 1–3 are G3 checklist items with no evidence in existence; clearing
them is compliance workstream work, not engineering. Items 4–5 are
boundary-integrity preconditions found by this re-audit (the boundary
repo's own CI does not enforce the contract that protects SAQ-A, and
refund money movement is ledger-only until PSP wiring). Item 6 does not
block the first donation (no production hub plane exists; donations do
not depend on hub egress topology) but gates any production hub
workload.

## Re-open rule

Any item closing requires evidence committed under this directory and a
note in `audits/evidence-registry.csv`. Any invalidation trigger from
the scope statement (Stripe footprint outside the boundary) re-opens G3
immediately.

> **STEP 26 note (2026-08-17):** withheld rows 2–3 now reference the corrected
> procedures/sources in `STEP26_CORRECTIONS.md` (C1/C3). Evidence gathering
> itself still happens in Step 25b; this step fixes the map it follows.
