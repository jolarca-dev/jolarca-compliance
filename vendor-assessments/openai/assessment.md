# Vendor Assessment — OpenAI

> **Status: onboarding. No production data flows to this supplier and no
> credentials are issued until every `PENDING` field below is populated from
> evidence and the onboarding procedure step 8 is merged.**
> (`jolarca-vendor/docs/procedures/onboarding.md` §Gate.)

**Category:** `ai-llm`
**Assessment date:** [PENDING — must be **on or before** the date any production
data first flows. Never backdated to make the sequence look correct: backdating
converts a process finding into an integrity finding.]
**Assessor (natural person, capacity):** [PENDING — `@JourneyOfLife`, acting as
vendor management owner. A role title with no named holder is not an approver —
see `jolarca-vendor/docs/solo-operator-controls.md` and the failure mode named
in `jolarca-vendor/assessments/README.md` §Structural rule 3.]
**Methodology of record:** `jolarca-vendor/docs/methodology/` (scoring),
`jolarca-vendor/assessments/README.md` (structure).
**Register schema version in force:** `1.0` (Group C scoring columns are **not
yet** present in `register.csv`; scoring fields below are recorded in this
assessment and migrate to the register when the schema migration lands — see
`jolarca-vendor/docs/ASSUMPTIONS.md` §Open items 2).

---

## 1. Supplier identity

| Field | Value |
|---|---|
| Trading name | OpenAI |
| Contracted legal entity | [PENDING — confirm the contracted legal entity, not the trading name. A DPA binds an entity.] |
| Jurisdiction of incorporation | [PENDING] |
| Ultimate parent / different jurisdiction | [PENDING] |
| Service model | [PENDING — `saas` / `iaas` / `paas`; drives ISO A.5.23] |
| Role | LLM inference (generation tier) for Hermes `content`, `seo`; `translation` generation |

## 2. Scope of engagement

What the supplier does for us, and the data categories it receives, mapped to
RoPA identifiers.

- **RoPA reference:** `ROPA-005`
- **Hermes agent fleet use:** [PENDING — which agents call this supplier, with
  which data categories, per `jolarca-hermes-agents/policies/model-policy.md`
  §Per-Agent Model Assignment.]

## 3. Alternatives considered (SOC 2 CC9.2)

Two or three sentences, recorded **before** engagement, stating what else was
examined — including not engaging and absorbing the work internally — and why
this supplier was selected.

- **Alternatives examined:** [PENDING]
- **Why selected:** [PENDING — if selection was driven by an existing
  relationship or a framework's vendor affinity, say so; it must be visible, not
  inferred. See `jolarca-vendor/docs/adr/VEN-0001-llm-vendor-selection.md`
  §Ordering constraint: the DPIA must precede framework selection, not follow it.]

## 4. Data processing

| Field | Value |
|---|---|
| Data categories received | [PENDING] |
| Purpose | [PENDING] |
| Secondary use / model training | [PENDING] |
| Retention | [PENDING] |
| Storage + backup locations | [PENDING] |
| Used for training? | [PENDING — Art. 5(1)(b); see §LLM questions below] |

## 5. LLM-specific due diligence

Answers are recorded against the evidence class **E** (evidenced), **A**
(asserted, caps CE at 0.5) or **N** (not addressed, scores 0.0) per
`jolarca-vendor/docs/methodology/due-diligence.md` §1. The question set is
`jolarca-vendor/docs/methodology/ai-llm-suppliers.md` §4 (20 questions across 6
groups); they are reproduced here as the checklist to complete.

### 5.1 Zero-retention and no-training

| # | Question | Answer | Class |
|---|---|---|---|
| 1 | Zero-retention API tier (no prompt/response storage beyond inference)? | [PENDING] | |
| 2 | Contractual no-training commitment (cite clause)? | [PENDING] | |
| 3 | No-training is technical (API tier) or contractual only? | [PENDING] | |
| 4 | Retention for abuse monitoring / billing / analytics? Period + basis? | [PENDING] | |

### 5.2 Prompt isolation and tenant separation

| # | Question | Answer | Class |
|---|---|---|---|
| 5 | How is prompt data isolated between tenants during inference? | [PENDING] | |
| 6 | Demonstrable non-visibility to other tenants / personnel / sub-processors? | [PENDING] | |
| 7 | Prompt-data access logged; retrievable on request? | [PENDING] | |

### 5.3 Model version and change management

| # | Question | Answer | Class |
|---|---|---|---|
| 8 | Model version pinning policy; deprecation notice? | [PENDING] | |
| 9 | Notification of version / capability / infra changes? | [PENDING] | |
| 10 | Minimum notice period before deprecating a pinned version? | [PENDING] | |

### 5.4 Sub-processor chain for inference

| # | Question | Answer | Class |
|---|---|---|---|
| 11 | Every sub-processor touching prompt data (name, jurisdiction, function, data)? | [PENDING] | |
| 12 | Third-party GPU / hosting / inference-infra providers enumerated? | [PENDING] | |
| 13 | ≥ 30-day notice before adding/replacing a prompt-data sub-processor? | [PENDING] | |

### 5.5 Transfer and inference residency

| # | Question | Answer | Class |
|---|---|---|---|
| 14 | Where do model weights live and where does inference compute run? | [PENDING] | |
| 15 | Inference residency contractual or default configuration only? | [PENDING] | |
| 16 | EU/EEA-only processing commitment? Else mechanism? | [PENDING] | |
| 17 | Government-access policy for prompt data (notify / challenge / minimise)? | [PENDING] | |

### 5.6 Incident history and fallback

| # | Question | Answer | Class |
|---|---|---|---|
| 18 | Incident affecting prompt data / model integrity / availability (36 mo)? | [PENDING] | |
| 19 | RTO / RPO for inference — contractual or best-effort? | [PENDING] | |
| 20 | Switching cost to named alternative (API compatible vs proprietary format)? | [PENDING] | |

### 5.7 Zero-retention DS reduction (only if all three elements present)

Effective DS may drop one level **only** where the vendor has, together:
(i) contractual no-storage beyond inference, (ii) contractual no-training, and
(iii) **technical evidence** of the zero-retention configuration. Without all
three, raw DS stands. (`jolarca-vendor/docs/methodology/ai-llm-suppliers.md`
§2.1.)

- Zero-retention DS reduction claimed: [PENDING]
- Contractual clause(s): [PENDING]
- Technical evidence (class E required): [PENDING]

## 6. Sub-processors

Complete list with legal name, jurisdiction, function and data categories.
"See vendor documentation" is recorded as **N** and caps CE (A.5.21).

- [PENDING]

## 7. Transfer position

Every country of processing, storage, backup and **support access**, with the
mechanism for each.

- **Countries:** [PENDING — enumerate every country of processing, storage, backup AND support access]
- **Mechanism:** [PENDING — `adequacy` / `scc` / `bcr` / `none`]
- **TIA:** [PENDING — required where mechanism is SCCs; self-authored, filed in
  `vendor-assessments/tia/`]

## 8. Legal framework

| Item | Status |
|---|---|
| DPA (Art. 28) | [PENDING — not signed while `onboarding`] |
| SCCs (module + annexes) | [PENDING] |
| TIA | [PENDING] |
| Security requirements schedule | [PENDING — required for Tier 1/2] |
| Responsibilities matrix | [PENDING — required for Tier 1] |

## 9. Inherent risk (DS / BC / AB)

Factors per `jolarca-vendor/docs/methodology/risk-scoring.md` §1; cite the rubric
row for each. **Scores are assigned from evidence at assessment time, never
estimated in advance.** An invented score is worse than an absent one.

| Factor | Value | Rubric row cited | Working |
|---|---|---|---|
| DS | [PENDING] | | |
| BC | [PENDING] | | |
| AB | [PENDING] | | |

`IRS = (DS x 0.50) + (BC x 0.30) + (AB x 0.20)` = [PENDING — show arithmetic]

## 10. Control effectiveness (C1–C5)

Domains scored 0.0 / 0.5 / 1.0 from evidence class; for LLM suppliers the
extended criteria in `jolarca-vendor/docs/methodology/ai-llm-suppliers.md` §3
govern.

| Domain | Score | Evidence relied upon |
|---|---|---|
| C1 Contractual | [PENDING] | |
| C2 Certification | [PENDING] | |
| C3 Technical | [PENDING] | |
| C4 Operational | [PENDING] | |
| C5 Transfer | [PENDING] | |

`CE = mean(C1..C5)` = [PENDING]

## 11. Residual risk

`RRS = IRS x (1 - (CE x 0.60))` — show the arithmetic. The 0.60 cap is deliberate
and must not be raised.

- **RRS:** [PENDING]
- **Band:** [PENDING — low / moderate / high / critical]
- **Narrative:** [PENDING — must refer to THIS supplier's actual data flows; no
  text carried from another supplier's assessment]

## 12. Tier

- `tier_from_rrs`: [PENDING]
- `tier_floor_from_ds`: [PENDING]
- **Tier** = max(tier_from_rrs, tier_floor_from_ds): [PENDING]
- `tier_override` (none / upward only — downward is invalid): [PENDING]
- `cadence_months` (12 / 24 / 36 from tier): [PENDING]

## 13. Conditions

Every **A** or **N** answer in a mandatory section, every refused clause, and
every CE domain below 1.0, each with an owner (natural person) and a due date.

| # | Condition | Owner | Due | Control |
|---|---|---|---|---|
| — | [PENDING] | | | |

## 14. Exit position

- Data export capability + format: [PENDING]
- Deletion guarantee (incl. backups) + written erasure certification: [PENDING]
- Named alternative + switching effort: [PENDING]
- `exit_plan` (documented / tested / not-required / absent): [PENDING]
  — `absent` for Tier 1/2 is a hard failure.

## 15. PCI position

Applicable only if DS = 5. [PENDING — determine whether any cardholder data
reaches this supplier. If not, record "not in PCI scope" with the reason.]

## 16. Approval

- Approver (natural person + capacity): [PENDING]
- Date: [PENDING]
- Signed commit hash (`approved_commit`): [PENDING]

Approval is the signed commit; it is not pending on an active supplier. While
this supplier is `onboarding`, no approval is recorded and none should be
invented.

## 17. Review history

| Cycle | Date | Trigger | Deltas from prior | Prior conditions disposition |
|---|---|---|---|---|
| 0 | [onboarding, not yet assessed] | new supplier | — | — |
