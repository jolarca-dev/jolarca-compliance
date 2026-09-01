# Risk Register (living)

Reviewed at every gate and quarterly. See `README.md` for scoring model.

| ID | Risk | Likelihood | Impact | Score | Treatment | Owner | Status | Review |
|---|---|---|---|---|---|---|---|---|
| RSK-001 | LLM vendor receives personal data via egress path | 3 | 4 | 12 | PII pre-filter + allowlist + TIAs (G2 evidence) | Platform | open | 2026-11-15 |
| RSK-002 | Baltic retention obligations conflict with erasure requests. **Annotation 2026-08-17 (STEP 26):** prior flat "10y" framing corrected — Lithuania has two distinct statutory classes (10y accounting; up-to-50y payroll/personnel-adjacent); LV/EE `[COUNSEL-TO-CONFIRM]`. See `docs/retention-schedule.md` §2 | 2 | 4 | 8 | Anonymize-don't-delete pattern (ADR-0001, amended) + per-country matrix; RC-PAYROLL-50Y candidates carry do-not-delete flag, DPO review | DPO | open | 2026-11-15 |
| RSK-003 | Vendor DPA gap during onboarding rush | 2 | 4 | 8 | Onboarding checklist as merge gate; register parity check | Compliance | open | 2026-11-15 |
| RSK-004 | Evidence integrity undetected tampering | 1 | 5 | 5 | Weekly hash verification + branch protection + audit log | Compliance | open | 2026-11-15 |
| RSK-005 | DSR clock breach due to unverified identity loop | 2 | 3 | 6 | Verification SLA (5 days) + day-21 paging | DPO | open | 2026-11-15 |
| RSK-006 | Hub Model-B residue (STEP 17 PB-01…PB-06): stripe dep declared, STRIPE_SECRET_KEY plumbing in settings/secrets/vault/infra, direct-integration provider config, inverted compliance test | 3 | 5 | 15 | Purge all residue in one jol-hub PR; re-run STEP 17 scans green | Platform | closed | 2026-08-17 |
| RSK-007 | E1/E2 boundary guards not wired in hub CI — allowed RSK-006 to accumulate silently | 3 | 4 | 12 | Wire check-payment-boundary.sh + dependency-guard test as hub PR gates before next payment work | Platform | closed | 2026-08-17 |
| RSK-008 | E3 network control undeployed; hostile hub→Stripe defense rests on credential absence, not topology | 2 | 4 | 8 | Deploy network-policy.md payment-boundary rows with the payment workstream; re-run hostile test against live boundary | Infra | closed | 2026-08-17 |
| RSK-009 | Internal payment API (/internal/v1) unimplemented; hub donation flow dead-ended → schedule pressure to re-integrate Stripe directly in hub | 2 | 5 | 10 | Implement contract §2–§4 with product attribution + caller binding, gated by consumer-driven contract tests | Marketplace | closed | 2026-08-17 |
| RSK-010 | Refund edge cases: hub refund view flips DB status only (no money movement via boundary); partial/duplicate-refund paths undefined | 2 | 3 | 6 | Route refunds through contract POST /internal/v1/refunds; define partial-refund + idempotent-replay behavior | Marketplace | closed | 2026-08-17 |
| RSK-011 | Donation VAT/tax-receipt handling unresolved (receipt endpoints are stubs); recurring donations undesigned against contract v1 | 2 | 3 | 6 | Route VAT/receipt question to jolarca-legal + tax advisor (flagged, not assumed); recurring = contract amendment | Compliance/Legal | open | 2026-11-15 |
| RSK-012 | E3 proven at mechanism level only (staging plane); no GKE/k8s production deployment exists, so network denial is not yet enforced where hub would run in production | 2 | 4 | 8 | Deploy E3 rows + N2 payment-API row with the hub production rollout; re-run e3-network-deny-test.sh on the cluster plane before hub production go-live | Infra | open | 2026-11-15 |
| RSK-013 | Boundary repo (jolarca) has NO required checks and the contract suite (tests/contract) is not wired into its CI — the contract guarantee rests on ad-hoc runs | 2 | 5 | 10 | Wire tests/contract into marketplace CI (compose parity topology) and set it required on main before first live donation | Marketplace | open | 2026-11-15 |
| RSK-014 | Internal refund endpoint updates the boundary ledger (gates, partial accounting, idempotency proven) but does not invoke PSP-side refund execution; live money movement lands with PSP wiring | 2 | 3 | 6 | Wire RefundCreateView → services.refund (stripe.Refund.create) at live PSP wiring, test-mode first | Marketplace | open | 2026-11-15 |
| RSK-015 | Missed/late i.SAF FR0600 monthly filing (nil reports included) — recurring obligations surface only when the penalty arrives | 2 | 3 | 6 | Registered as OBL-001 (`docs/regulatory-obligations.md`) with owner + calendar row; FR0600 export spec in jol-m-data; filing ledger append-only; penalties `[COUNSEL-TO-CONFIRM]` | Finance + Compliance | open | 2026-11-15 |

Status values: `open`, `mitigating`, `accepted`, `closed`.
Accepted risks require a signed acceptance note in the treatment plan.

## Closure record — STEP 22c re-audit (2026-08-17, independent)

All closures below rest on evidence reproduced by the STEP 22c re-audit
(canonical report: `jolarca-infrastructure/STEP22C_FINAL_REAUDIT.md`), not
on execution self-attestation.

- **RSK-006 / PB-01…PB-06 — CLOSED.** Purge merged in jol-hub PR #76
  (`89c4812d`); STEP 22c re-grepped every original file:line clean;
  fleet entropy scan 0 real-looking keys; hub venv cannot import stripe.
- **RSK-007 / N1 — CLOSED.** E1+E2 are required merge-blocking checks on
  jol-hub main (`enforce_admins: true`, strict up-to-date). Negative test
  PR jol-hub #83: E1 FAILED; merge blocked on the normal path AND on the
  admin REST path (HTTP 405 "Repository rule violations found"); PR
  closed unmerged; main SHA unchanged.
- **RSK-008 — CLOSED (mechanism), residual → RSK-012.** Staging-plane
  reproduce: hub-plane workload WITH a valid Stripe test key denied at
  the network layer (topology, not credential absence); both sanctioned
  legs green. C2 caveat from STEP 17/22 closed.
- **RSK-009 — CLOSED.** Marketplace PR #18 (`4faef0a3`); STEP 22c ran the
  contract suite itself: 14/14 green on the live compose topology.
- **RSK-010 — CLOSED for routing, residual → RSK-014.** Refunds flow only
  through the boundary (422 gating, partial accounting, idempotent replay
  proven); PSP-side execution pending live wiring.
- **N2 — CLOSED.** Fail-closed hub→payment-API egress row merged in
  jol-hub PR #82 (`4f93c6b9`); renders only when `paymentsApi.cidr` set.
- **N3 — CLOSED.** All four STEPn_EXECUTED.md + EXECUTION_BUNDLE_18-21.md
  verified COMMITTED via `git ls-files` in their repos (this closure
  bundle commits the previously-untracked STEP 17/22 audit artifacts).
- **OBS-19-1 — ACCEPTABLE, closed.** Admin bypass re-tested and blocked
  2026-08-17 (PR #83, HTTP 405). Incident record in STEP19_EXECUTED.md.
- **OBS-18-3 — RESIDUAL, owner hub team.** Hub legacy CI red (incl.
  pre-existing `test_secrets_module_exists` failure — verified failing
  before STEP 18; `infra/terraform/modules/secrets` never existed in
  history). Not part of the required check set; not PCI-relevant.
- **OBS-20-1 — RESIDUAL, escalated to RSK-013.** Marketplace CI red
  pre-existing (GDAL install + frontend E2E) and no required checks.
- **OBS-22C-1 (new) — WATCH.** Hub holds PayPal-era residue: unused
  `get_paypal_credentials()` vault reader + `METHOD_PAYPAL` enum label;
  no callers, no live client. Any future PSP must enter via the boundary
  (ADR-0005 intent extends beyond Stripe).
