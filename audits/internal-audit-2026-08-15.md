# Internal Audit Report — Repository Self-Audit

| | |
|---|---|
| Audit ID | IA-2026-01 |
| Date | 2026-08-15 |
| Auditor | Compliance automation + compliance lead (independent of control owners) |
| Scope | jol-m-compliance repository controls: gates, registers, integrity tooling, workflows |
| Criteria | Policies 01–12, `CONTRIBUTING.md` evidence rules, audit-plan-2026 §4.1/§6 |
| Method | Re-performance (scripts executed, exit codes asserted), document review |
| Status | **All findings fixed and verified** |

## Findings

| ID | Class | Finding | Root cause | Corrective action | Verified |
|---|---|---|---|---|---|
| F-01 | Major | `make check` neutralized the policy review gate with `\|\| true` — an overdue policy could not fail CI | Copy-paste of advisory pattern onto a mandatory gate | Gate enforced hard; vendor review gate added to `make check` | Yes — script runs bare; overdue path returns exit 1 (re-performed with `--today` override) |
| F-02 | Minor | `qodana.yaml` used a non-existent schema (`version: "2"`, `failRules`) — inherited-tooling claim unverifiable | Fabricated config during scaffolding | Rewritten to valid Qodana schema (`version: "1.0"`, linter/profile/exclude/failThreshold) | Yes — YAML parses; schema matches Qodana contract |
| F-03 | Observation | Dead code in `scripts/dsr-sla-report.py` (unused `ROW` regex + `re` import) | Leftover from refactor | Removed | Yes — module compiles, report output unchanged |
| F-04 | Major | `vendor-assessments/register.md` claimed "CI spot-checks row parity" but **no such check existed** — an unassessed vendor folder could exist off-register | Control documented before it was implemented | Implemented `register_parity()` in `scripts/vendor-review-dates.py` (folder ↔ register.csv bidirectional), failing CI on drift; documentation corrected to match reality | Yes — parity passes on current state; mismatch path returns exit 1 |
| F-05 | Observation | `audits/README.md` layout table did not reference the audit plan / internal audit reports | New artifacts added after table written | Layout table updated | Yes |
| F-06 | Observation | CHANGELOG had no entry for the audit program addition | Process lapse (own rule: every change is auditable) | Unreleased section updated with Added/Fixed entries | Yes |

## Re-performance evidence (verification suite)

All commands executed with the repository venv (Python 3.12.3):

| Check | Command | Result |
|---|---|---|
| Evidence integrity | `evidence-hash.py --verify` | PASS (0 final rows; registry empty pre-G0 as expected) |
| Policy currency gate | `policy-review-dates.py --max-days 14` | PASS — none due |
| Policy gate failure path | same script, `--today 2028-01-01` | exit 1 as required (F-01 verified) |
| Vendor currency + parity | `vendor-review-dates.py --max-days 30` | PASS — parity OK, none due |
| Vendor failure path | same script, `--today 2029-01-01` | exit 1 as required |
| DSR SLA | `dsr-sla-report.py register.md` | PASS — no closed/at-risk DSRs |
| PII scan | `redact-pii.py --all` | PASS — clean |
| YAML validity | all 16 workflow/config YAML files | PASS |

## Professional opinion

- F-01 and F-04 were the only Major findings; both are the classic audit
  failure mode — *a documented control with no operating mechanism*. The fix
  pattern (re-perform the negative path, not just the happy path) is now part
  of the gate procedure in `audit-plan-2026.md` §6.
- The repository is structurally audit-ready: every register is
  machine-readable, every date-bearing artifact is parseable, and evidence
  integrity is continuously verifiable. Remaining risk is **populating** the
  artifacts with real sign-offs before G0 — skeletons are not evidence.
- Recommend this report be hashed into `audits/evidence-registry.csv` at G0
  finalization (RC-EVIDENCE).

## Sign-off

| Role | Name | Date |
|---|---|---|
| Auditor (compliance lead) | ____ | ____ |
| DPO | ____ | ____ |
