# STEP 22 — Payment boundary re-audit (Model A): archived record

- **Date:** 2026-08-17
- **Auditor persona:** independent audit (paranoid, evidence-first)
- **Status:** IMMUTABLE once committed (G3 evidence rule). Corrections go
  into a NEW dated audit, never into this file.
- **Gate:** G3-payments — **NOT CLEARED** by this re-audit. The gate
  checklist remains unchecked; the first real hub donation stays
  UNAUTHORIZED.

## Canonical report

- `jolarca-infrastructure/STEP22_REAUDIT.md`
- sha256: `91fa1a75cafc1fed58eed65563d6bf6ef8ae85f156bf1fc1789625059d9a0a2c`
- Prior audit hash (unchanged): STEP17_AUDIT.md sha256
  `86f028d28a74c954911edec023406ad5b5a0f7de4b297f0171b0e3dc370c9f08`

## Summary of record

Premise tested: "Steps 18–21 implemented the boundary." Reproduced
evidence shows the premise is FALSE — no STEP18–21 artifacts exist in
any fleet repo, no remediation commits exist in any repo's git history,
and no application is running (marketplace test-db/redis only; no app
listener; no cluster reachable). Every Step-17 finding reproduces
byte-identically (PB-01…PB-06 at the same file:line locations; webhook
500-vs-400 defect unfixed; no `product` field; no `/internal/v1`; no
contract tests; hostile attempt still blocked by credential absence, not
topology). Only deltas since Step 17: hub gained correct-but-undeployed
default-deny NetworkPolicy manifests (E3-shaped, no external egress
rows), and the fleet entropy scan remains at 0 real keys.

New findings: N1 (hub branch protection has ZERO required status
checks), N2 (hub NetworkPolicy egress lacks the sanctioned
hub→payment-API 443 row), N3 (Step-17 compliance artifacts were never
committed — no archive is actually immutable yet).

## ONE-SENTENCE VERDICT

Model A single-payment-boundary remains **NOT PROVEN** — Steps 18–21
were never executed, no live boundary exists on which contract, webhook,
or degraded-mode controls could be verified, E3 exists only as
correct-but-undeployed manifests, and G3 stays BLOCKED — the first real
donation is NOT authorized until blockers B1–B8 (see canonical report)
are closed and this audit is re-run against the live system.

## Certification hygiene note

The scope statement (`certifications/pci-dss/scope-statement-model-a.md`)
and risk register were deliberately NOT changed by this re-audit: the
statement's condition (E1–E3 operational) is unmet and RSK-006…RSK-011
all reproduce. Certifying PROVEN now would be a false attestation under
PCI-DSS Req. 12.5.2 / SOC 2 CC6.1.
