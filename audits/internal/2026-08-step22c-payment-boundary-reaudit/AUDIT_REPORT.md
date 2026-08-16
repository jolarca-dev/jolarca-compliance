# STEP 22c — payment boundary re-audit (final)

- **Date:** 2026-08-17
- **Type:** independent internal audit (re-audit of STEP 17 scope)
- **Canonical report:** `jol-m-infrastructure/STEP22C_FINAL_REAUDIT.md`
  sha256 `b91c8556a5b5e99d24109d3cad3d4ea8cf179c9c9a3689522bff8d14e291dbed`
- **Archived evidence:** `audits/gate-evidence/G3-payments/`
  (hash-pinned manifest + immutable report copies)

## Outcome

- **Premise check:** PASSED — all four merge SHAs present; all
  STEPn_EXECUTED.md committed (verified via `git ls-files`, not
  worktree listing).
- **Controls:** C1-code, C1-CI (incl. fresh negative test PR jol-hub
  #83, blocked on normal AND admin paths), E3 mechanism-level, C2
  hostile attempt, C3 contract suite (14/14 reproduced live), C4, C5,
  C6 — all PROVEN. RSK-010 partial (routing proven; PSP execution
  residual → RSK-014).
- **New findings:** RSK-013 (boundary repo ungated; contract suite not
  in its CI), RSK-014 (refund PSP wiring), OBS-22C-1 (PayPal residue,
  watch), OBS-22C-2 (pre-existing red hub compliance test).
- **Scope statement:** upgraded CONDITIONAL → PROVEN
  (`certifications/pci-dss/scope-statement-model-a.md`).
- **Risk register:** RSK-006…010 closed with evidence; N1/N2/N3 closed;
  RSK-012/013/014 opened with owners; RSK-011 remains open.
- **G3:** CONDITIONAL CLEARANCE — payment-boundary controls cleared;
  first-real-donation authorization withheld on DPIA-003 signature,
  VIES VAT evidence, Stripe TIA + AoC, RSK-013, RSK-014
  (`audits/gate-evidence/G3-payments/G3_DECISION.md`).

## Method note

Zero inherited claims: every control was re-executed in this session
against live systems (GitHub API, hub/marketplace/infra repos, compose
topology, staging-plane network proof). This bundle also commits the
STEP 17/22 audit artifacts that remained untracked in this repo (N3
lesson applied to the compliance repo itself).
