# STEP 17 — Payment boundary audit (Model A): archived gate evidence

- **Date:** 2026-08-17
- **Auditor persona:** independent audit (paranoid, evidence-first)
- **Status:** IMMUTABLE once committed (G3 evidence rule). Corrections go
  into a NEW dated audit, never into this file.
- **Gate:** G3-payments — this report does NOT pass the gate; the G3
  checklist remains unchecked until remediation lands and a follow-up
  audit verifies it.

## Canonical report

The full audit with reproduced commands and outputs lives in the
infrastructure repository (custody of the boundary's IaC/security docs):

- `jol-m-infrastructure/STEP17_AUDIT.md`
- sha256: `86f028d28a74c954911edec023406ad5b5a0f7de4b297f0171b0e3dc370c9f08`

Verify: `sha256sum STEP17_AUDIT.md` in `jol-m-infrastructure` at the
audited commit. Any divergence = evidence-tampering finding (RSK-004
pattern).

## Verdict summary (as audited)

| Control | Verdict |
|---------|---------|
| C1 boundary ownership — code scan | PASS: payments_app is the only Stripe consumer; 0 real keys fleet-wide; 6 dormant Model-B residue findings in hub (PB-01…PB-06) |
| C1 boundary ownership — CI guard (E1/E2) | FAIL: guard not wired in hub CI |
| C1 boundary ownership — network (E3) | DECLARED, NOT IN FORCE |
| C2 SAQ-A + hostile hub→Stripe attempt | PASS with caveat: attempt blocked (AuthenticationError — hub holds no valid credential); defense rests on absence, not topology |
| C3 contract regression (Step 13 suite) | NOT EXECUTABLE: suite and `/internal/v1` API do not exist; Steps 13–16 reports never produced |
| C4 webhook integrity | PARTIAL: forge rejected (SDK-verified), dedup by unique event_id (code-verified); forwarding to hub unimplemented; defect: forgery → HTTP 500 not 400 |
| C5 revenue attribution | FAIL: no `product` field on PaymentRecord/metadata; contract §5 unimplemented |
| C6 degraded mode | PARTIAL: bypass structurally impossible (no code path, no credential); live drill owed |
| C7 scope statement | ISSUED: `certifications/pci-dss/scope-statement-model-a.md` |

## ONE-SENTENCE VERDICT

Model A single-payment-boundary is **NOT PROVEN** — ownership holds in
source today (payments_app is the only Stripe consumer; the hostile
hub→Stripe attempt failed for lack of any valid credential and any code
path), but two of three structural controls are not operational (E1/E2
guards absent from hub CI, E3 not deployed), six items of dormant Model-B
residue were found in jol-hub (PB-01…PB-06), and the contracted internal
API — including revenue attribution and hub webhook forwarding — is not
yet implemented; all findings are owned and registered (RSK-006…RSK-011).

## Follow-up obligations

1. Remediation per STEP17_AUDIT.md "Remediation order" (owners in
   `risk-register/register.md`).
2. Re-run this audit suite (hostile attempt included) against the LIVE
   boundary before the first hub donation and before the G3 gate decision.
3. Quarterly scope reconfirmation per the scope statement.
