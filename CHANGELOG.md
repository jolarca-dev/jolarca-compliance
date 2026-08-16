# Changelog

All notable changes to this compliance repository are documented here.
Format: [Conventional Commits](https://www.conventionalcommits.org). Every
policy change, register mutation, and evidence finalization must appear here.

## [Unreleased]

### Added

- audits: detailed internal audit program plan (`audits/audit-plan-2026.md`).
- audits: internal self-audit report 2026-08-15 (findings F-01–F-06,
  all fixed and verified).
- STEP 17 payment-boundary audit (Model A): archived gate evidence
  (`audits/internal/2026-08-step17-payment-boundary-audit/`, immutable,
  sha256-pinned to the canonical `jol-m-infrastructure/STEP17_AUDIT.md`),
  SAQ-A scope statement for the single payment boundary
  (`certifications/pci-dss/scope-statement-model-a.md`, PCI-DSS 12.5.2 /
  SOC 2 CC6.1 / ISO 27001 A.8.13 mapped), and residual risks RSK-006…
  RSK-011 (hub Model-B residue, unwired CI guards, undeployed E3,
  unimplemented internal API, refund edge cases, donation VAT/receipt
  routed to jol-m-legal + tax advisor). Verdict: Model A NOT PROVEN yet
  — re-audit owed before the G3 gate.
- STEP 22 payment-boundary RE-AUDIT (Model A): premise "Steps 18–21
  implemented" tested and REJECTED with reproduced evidence — no step
  artifacts, no remediation commits, no live boundary; all STEP-17
  findings (PB-01…PB-06) reproduce byte-identically; new findings N1
  (hub branch protection has zero required checks), N2 (hub NetworkPolicy
  lacks the hub→payment-API egress row), N3 (STEP-17 evidence never
  committed). Archived hash-pinned under
  `audits/internal/2026-08-step22-payment-boundary-reaudit/`. Scope
  statement and RSK-006…RSK-011 deliberately UNCHANGED; G3 NOT cleared;
  first real donation remains UNAUTHORIZED (blockers B1–B8).
- STEP 22c payment-boundary FINAL RE-AUDIT (Model A): premise PASSED
  (all four merge SHAs + STEPn_EXECUTED.md committed); every control
  independently reproduced — PB-01…PB-06 clean, 0 real-looking keys,
  fresh negative-test PR blocked on normal AND admin merge paths,
  credential-independent network deny, contract suite 14/14 live.
  Scope statement upgraded CONDITIONAL → PROVEN; RSK-006…RSK-010 and
  N1/N2/N3 CLOSED with evidence; new RSK-012 (E3 k8s deployment),
  RSK-013 (boundary repo ungated), RSK-014 (refund PSP wiring);
  RSK-011 stays open. G3: CONDITIONAL CLEARANCE — payment-boundary
  controls cleared, first-real-donation authorization withheld
  (DPIA-003 signature, VIES VAT evidence, Stripe TIA + AoC, RSK-013,
  RSK-014). Evidence sealed hash-pinned under
  `audits/gate-evidence/G3-payments/` and registered in
  `audits/evidence-registry.csv`. This bundle also commits the
  previously-untracked STEP 17/22 audit artifacts (N3 lesson).

### Fixed

- fix: `make check` enforces policy & vendor review-currency gates hard
  (removed silent `|| true` bypass; finding F-01).
- fix: vendor register/folder parity is now actually enforced by
  `scripts/vendor-review-dates.py` (finding F-04).
- fix: `qodana.yaml` rewritten to a valid Qodana schema (finding F-02).
- chore: removed dead code in `scripts/dsr-sla-report.py` (finding F-03).

## [0.1.0] - 2026-08-15

### Added

- chore: repository skeleton per compliance architecture review
  (GDPR core artifacts, ISMS policies, vendor governance, incident & DSR
  management, audit evidence gates G0–G4, certification tracks).
- policy: initial draft set 01–12 mapped to ISO 27001 Annex A.
- register: RoPA `master-register.csv`, vendor `register.csv`,
  evidence `audits/evidence-registry.csv` (empty, schema locked).
- ci: integrity workflows — DSR SLA monitor, policy review reminders,
  evidence hash verification, vendor review tracker, access review scheduler.
- docs: compliance matrix, retention schedule, regulatory contacts, ADR-0001.
