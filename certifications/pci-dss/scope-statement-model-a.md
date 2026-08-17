# SAQ-A scope statement — Model A single payment boundary

- **Issued:** 2026-08-17 (STEP 17 independent audit)
- **Upgraded:** 2026-08-17 (STEP 22c independent re-audit) — CONDITIONAL → **PROVEN**
- **Authority:** ADR-0005 (jol-m-infrastructure, ratified 2026-08-17),
  ADR-0004 Amendment 1, `docs/payment-api-contract.md` v1
- **Reconfirmation:** quarterly, with the PCI scope check in
  `jol-m-infrastructure/security/pci-dss-scope.md` and the access review

## Scope statement — PROVEN

SAQ-A scope is **the payment boundary only**: the `payments_app` of
`jol-m-marketplace`, its data stores, and its network segment. It is the
sole Stripe integrator, the sole holder of Stripe credentials, and the
sole receiver of Stripe webhooks.

**jol-hub (mission platform) is OUT of scope** per Model A: no Stripe SDK
server-side, no Stripe keys, no PAN, and no network path to
`api.stripe.com`. Hub consumes the boundary exclusively through the
internal payment API (HMAC-signed requests with TTL, mandatory
idempotency, service-account caller binding, PAN-free payloads). Card
data flows donor/customer browser → Stripe directly (Stripe Elements);
SAQ-A is preserved end-to-end.

This status was independently reproduced on 2026-08-17 by the STEP 22c
re-audit (zero inherited claims): PB-01…PB-06 residue re-grepped clean at
the original file:line locations; fleet entropy scan 0 real-looking keys;
server-side Stripe imports exist only in marketplace `payments_app`;
inverted Model A sentry tests green; a live negative-test PR (jol-hub #83)
was BLOCKED on both the normal and the admin merge path by the required
E1 check; a hub-plane workload holding a VALID Stripe test key was denied
egress at the network layer.

## Structural controls (ADR-0005 E1–E3)

| # | Control | Status 2026-08-17 (post-STEP 22c) |
| --- | --- | --- |
| E1 | CI grep guard in jol-hub (`check-payment-boundary.sh`) | ARMED — required merge-blocking check, sha256-pinned vendored copy `8fa2dd12…d47a5`, negative test blocked (PR #83) |
| E2 | dependency allow-list guard (`stripe` absent from hub deps) | ARMED — required merge-blocking check; SDK not installed, not importable, not declared |
| E3 | network egress denial hub → api.stripe.com | PROVEN at mechanism level — staging-plane reproduce (deny + both allow legs green); fail-closed helm row landed. GKE production deployment is a precondition for any production hub workload (RSK-012) |

Branch protection on jol-hub main: required checks
`Payment Boundary Guard (E1, ADR-0005)` + `Dependency Guard (E2,
ADR-0005)`, strict up-to-date, `enforce_admins: true` (admin bypass
closed and re-tested 2026-08-17).

## Residual conditions (do not affect hub's out-of-scope status today)

1. **RSK-012** — E3 rows must be deployed on the hub production k8s
   plane before hub runs as a production workload (no such deployment
   exists today; mechanism proof + manifests stand in).
2. **RSK-013** — wire the contract suite (`tests/contract`) into
   jol-m-marketplace CI as a required check; the boundary repo currently
   has no required checks.
3. **RSK-014** — internal refund endpoint updates the boundary ledger but
   does not yet invoke PSP-side refund execution; due at live PSP wiring.
4. G3 gate items 3–5 (DPIA-003 signature, VIES VAT evidence, Stripe
   TIA + AoC) remain open — see `audits/gate-evidence/G3-payments/`.

## Control mapping

| Framework | Control |
| --- | --- |
| PCI-DSS v4.0 | Req. 12.5.2 (this statement = scope confirmation, quarterly); Req. 1.x (segmentation per network-policy matrix); Req. 3.x (no CHD/SAD on platform — tokenization-first); Req. 10 (audit logging of boundary calls) |
| SOC 2 | CC6.1 (logical access to the boundary: signed requests + caller binding), CC8.1 (boundary changes are change-managed IaC/ADR) |
| ISO 27001:2022 | A.8.13 (segregation with a documented, controlled interface), A.5.2 (this policy) |
| GDPR | Art. 5(1)(b) purpose limitation preserved across the boundary; Art. 28/30 — ONE Stripe DPA, ONE RoPA entry (ROPA-003) covering both products' purposes |

## Invalidation rule

Any change that brings card data, Stripe SDK server-side usage, or Stripe
credentials into jol-hub (or any system outside the boundary) invalidates
this statement — treat as a CRITICAL change, re-assess immediately, and
re-run the STEP 22c audit suite.

## Evidence

- Re-audit of record:
  `audits/internal/2026-08-step22c-payment-boundary-reaudit/AUDIT_REPORT.md`
- Canonical re-audit: `jol-m-infrastructure/STEP22C_FINAL_REAUDIT.md`
- Prior audits: STEP 17 sha256 `86f028d2…c9f08`, STEP 22 sha256
  `91fa1a75…9a0a2c` (hash-verified unchanged 2026-08-17)
- Hash-pinned evidence bundle:
  `audits/gate-evidence/G3-payments/evidence-manifest.md`
- Residuals: `risk-register/register.md` RSK-011…RSK-014
