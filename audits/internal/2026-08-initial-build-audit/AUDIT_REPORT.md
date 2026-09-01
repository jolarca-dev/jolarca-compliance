# Initial Build Audit — jolarca-compliance ("The Evidence Vault")

| | |
|---|---|
| Audit ID | IA-2026-02 (initial build audit) |
| Date | 2026-08-15 |
| Audit team | Lead ISMS Auditor (ISO 27001:2022 / SOC 2) · Senior Data Protection Auditor (GDPR) · Staff DevSecOps Engineer |
| Object | Local repository `jolarca-compliance`, branch `main` @ `d91701c`, plus uncommitted Qodana fixes |
| Method | Evidence-first re-execution: every claim re-run; negative tests mandatory; no silent fixes |
| Design basis | `JOL_Compliance_Repo_File_Tree.md` NOT present locally — audited against the structure documented in `README.md` + `CHANGELOG.md` |

## 1. Executive summary

The repository is **structurally faithful to the approved design** and its
automation genuinely works: tampering and deletion of hashed evidence are
detected (exit 1), the DSR day-21 paging logic is correct on synthetic dated
cases, registers parse, YAML is valid, and **no personal data exists anywhere
in the tree** (three independent sweeps). Secret-scanning *capability* was
proven with dummy secrets.

However, four HIGH findings and one CRITICAL block the "100% done" claim:

1. **CRITICAL** — CODEOWNERS names three team handles whose existence is
   unverified; branch protection would have no enforceable reviewers.
2. **HIGH** — five GitHub labels used by four workflows do not exist;
   `gh issue create` fails at runtime, so DSO paging and incident
   escalation **fail silently when they matter most**.
3. **HIGH** — `evidence-hash.py --update` has no finalization gate: it
   registered **six draft files as `final` evidence** in the scratch test.
4. **HIGH** — `bitrix24-crm` processing has a RoPA narrative but **no ROPA
   ID and no register row** (Art. 30 defect).
5. **HIGH** — secret scanning is absent from CI (gitleaks is pre-commit only;
   pre-commit is not even installed in the audited environment).

## 2. Verdict per dimension

| Dimension | Verdict | Basis |
|---|---|---|
| A. Conformance | **PASS-WITH-FINDINGS** | All designed components PRESENT; 4 named docs MISSING (F-A2); template provenance unproven (F-A1) |
| B. Functional | **PASS-WITH-FINDINGS** | All make targets exit 0; tamper/delete negative tests PASS; DSR math verified; RoPA orphan (F-B1); finalization gap (F-B2); label gap (F-B3) |
| C. Compliance-truth | **PASS-WITH-FINDINGS** | No-PII proven; immutability logic sound (with LFS caveat F-C2); statutory clocks correct; retention markers intact; gitleaks missing from CI (F-C1) |
| D. Security & operability | **FAIL** | CODEOWNERS placeholders (F-D1, push-blocking); access matrix vs CODEOWNERS disagree (F-D2) |
| E. Cross-repo consistency | **PASS-WITH-FINDINGS** | Naming violation vs canonical `jol-compliance` (F-E1); legal/ design conflicts with `jol-legal` boundary doctrine (F-E2); no broken cross-repo references |

## 3. Dimension A — Conformance (tree diff)

Inventory: **133 files / 83 directories** (owner self-reported 131/83 — stale
count, noted, no action).

| Designed component | Verdict |
|---|---|
| Root governance set (README, LICENSE, SECURITY, CONTRIBUTING, CHANGELOG, Makefile, pyproject, qodana, pre-commit, .editorconfig, .gitignore, .gitattributes) | PRESENT (12/12) |
| `.github/` CODEOWNERS, dependabot, PR template, 5 issue templates, 8 workflows | PRESENT (16/16) |
| `dpia/` README, 000-template, 001–004, register | PRESENT (7/7) |
| `ropa/` README, 6 by-system records, diagrams/, master-register.csv | PRESENT (9/9), but content defect F-B1 |
| `lawful-basis/` README, consent-text 5 langs, consent-versions, LIA | PRESENT (4/4 + dirs) |
| `policies/` README, 01–12, exceptions | PRESENT (14/14) |
| `vendor-assessments/` README, register.md/.csv, 9 vendors, tia | PRESENT (13/13) |
| `incidents/` README, register, 2026/, 3 templates, game-days | PRESENT (6/6) |
| `data-subject-requests/` README, register, templates 4 langs, sla-reports | PRESENT (7/7) |
| `management-review/` README, minutes/, dpo-reports/ | PRESENT |
| `audits/` README, evidence-registry.csv, G0–G4, soc2, iso27001, pen-tests, access-reviews | PRESENT; `soa.md` named in `audits/iso27001/README.md` is MISSING (F-A2) |
| `certifications/` README + 3 tracks | PRESENT (4/4) |
| `legal/` README + 5 domains with language dirs | PRESENT; named artifacts `banner-spec.md`, `cookie-policy.md`, `diff-log.md` MISSING (F-A2) |
| `risk-register/`, `training/`, `docs/` (incl. ADR-0001), `scripts/` (5) | PRESENT |
| EXTRA: `audits/audit-plan-2026.md`, `audits/internal-audit-2026-08-15.md`, `make qodana` | Justified in CHANGELOG `[Unreleased]` — acceptable |
| DEVIATED: qodana.yaml schema rewrite, Makefile gate hardening | Justified in CHANGELOG (F-01/F-02 of IA-2026-01) — acceptable |

Template-inheritance baseline: **15/15 files PRESENT**, but provenance
unprovable — see F-A1.

## 4. Findings register

| ID | Dim | Severity | Location | Claim vs. Evidence | Recommended remediation | Owner |
|---|---|---|---|---|---|---|
| F-D1 | D | **CRITICAL** | `.github/CODEOWNERS` (whole file) | Claim: DPO + compliance lead required reviewers. Evidence: handles `@journeyoflife-org/{dpo,compliance-leads,legal}` existence unverified; if absent, required reviews are unenforceable | Create/verify the three org teams; replace handles; test with a probe PR before enabling protection | Org admin |
| F-B3 | B | **HIGH** | `.github/workflows/{dsr-sla-monitor,policy-review-reminder,evidence-integrity,vendor-review-due,access-review-due}.yml` | Claim: workflows page DPO / open tracking issues. Evidence: labels `sla-breach-risk, review-due, critical, audit, dsr, vendor, policy-change, incident, access-review` are referenced by `gh issue create` but not defined; `gh` errors on unknown labels → automation fails at the moment of need | Create all labels (or switch to `gh label create --force` in workflow) before first scheduled run | Compliance lead |
| F-C1 | C | **HIGH** | `.github/workflows/ci.yml` | Claim (README/pre-commit): secrets/PII blocked. Evidence: `grep gitleaks .github/workflows/` → no matches; secret scanning exists only in local pre-commit; pre-commit NOT installed in audited env → a direct push bypasses all secret scanning | Add gitleaks step to `ci.yml`; enable GitHub push protection as second layer | DevSecOps |
| F-B2 | B | **HIGH** | `scripts/evidence-hash.py` (`--update`) | Claim: finalized evidence is immutable & distinguished from drafts. Evidence (NEG-1): `--update` on the current tree registered 6 DRAFT files (incl. `dpia/register.md`, incident templates) as `status=final` — no finalization marker consulted | Gate `--update` on an explicit marker (e.g. `status: final` front-matter or a manifest file); refuse to hash unmarked files | Compliance lead |
| F-B1 | B | **HIGH** | `ropa/by-system/bitrix24-crm.md` / `ropa/master-register.csv` | Claim: RoPA complete per Art. 30. Evidence: narrative exists with no ROPA ID; no register row; bidirectional parity broken | Assign ROPA-007, add register row, or document CRM processing under an existing entry with lawful basis | DPO |
| F-A2 | A | MEDIUM | `legal/cookie-policy/README.md`, `legal/privacy-policy/README.md`, `audits/iso27001/README.md` | Claim: named artifacts exist (`banner-spec.md`, `cookie-policy.md`, `diff-log.md`, `soa.md`). Evidence: all four MISSING | Create stubs or remove the promises; no ADR justifies absence | Compliance lead |
| F-A1 | A | MEDIUM | `qodana.yaml:1`, `docs/DPIA-template.md:3` vs git history | Claim: baseline "inherited from jol-repo-template". Evidence: history begins "Initial commit: PyCharm project scaffold"; no provenance artifact | Record template provenance (ADR or CHANGELOG note: which template commit was mirrored) | Compliance lead |
| F-E1 | E | MEDIUM | Repo name | Claim (portfolio doctrine): canonical name `jol-compliance`. Evidence: repo is `jolarca-compliance` locally and on origin | Execute rename runbook (§ runbook step 1) | Org admin |
| F-E2 | E | MEDIUM | `legal/**` | Claim (boundary doctrine): canonical legal texts live in `jol-legal/legal-texts/`; this repo holds references + consent ledger. Evidence: no full texts present (no current breach), but `legal/` READMEs are designed to store versioned full texts; zero references to `jol-legal` | Amend design: legal/ keeps version ledges & references only; texts move to jol-legal; add cross-references | DPO + legal |
| F-D2 | D | MEDIUM | `README.md` access matrix vs `.github/CODEOWNERS:23` | Claim: "Compliance lead required reviewer on all registers". Evidence: `/data-subject-requests/` (holds the DSR register) owned by DPO only; last-match-wins overrides the `*` rule | Add compliance-leads to the DSR pattern, or amend the README claim | Compliance lead |
| F-C2 | C | LOW | `.gitattributes` / `evidence-integrity.yml` | Claim: immutability via hashes. Evidence: hashes are over resolved bytes (correct with `lfs: true` checkout); any pointer-only checkout would verify as MISMATCH (false tamper alarm); LFS never initialized/demonstrated in this repo | Document LFS checkout requirement in audits/README; verify `git lfs install` state before first PDF evidence | DevSecOps |
| F-B4 | B | LOW | `.github/workflows/vendor-review-due.yml` | `--machine` also emits `PARITY` failures, but the weekly monitor counts only `^DUE` → parity breakage on main never pages (caught per-PR only) | Count PARITY lines too, or fail the job | Compliance lead |
| F-C3 | C | LOW | gitleaks default ruleset | Evidence (NEG-5b): dummy `vault_password = "…"` NOT detected; only patterned secrets are caught | Note in SECURITY.md; treat redact-pii + review as co-controls | DevSecOps |
| F-C4 | C | LOW | `docs/retention-schedule.md` RC-FINANCIAL | 10y asserted for LT on internal citation; counsel-confirmation markers exist for LV/EE variants and rule 4 — criteria met, but extend counsel sign-off to the LT figure too | Counsel sign-off row per jurisdiction before G3 | Legal |

## 5. Evidence appendix (commands executed this session)

| # | Command | Result |
|---|---|---|
| E1 | `find . -type f … \| wc -l` / dirs | 133 files / 83 dirs |
| E2 | Baseline file existence loop (15 files) | 15/15 PRESENT |
| E3 | Named-doc existence loop | 5 MISSING (4 findings + 1 skeleton-expected) |
| E4 | `make check` | exit 0 (all gates pass) |
| E5 | `make verify-signatures` | exit 0 — **0 rows verified (vacuously green pre-G0; expected, noted)** |
| E6 | `make sla-report` / `make redact-check` | exit 0 / clean |
| E7 | NEG-1: scratch `evidence-hash --update` | 6 draft files registered as `final` → F-B2 |
| E8 | NEG-2: tamper `dpia/register.md` → `--verify` | `FAIL MISMATCH`, exit 1 → detection PROVEN |
| E9 | NEG-3: delete `postmortem.md` → `--verify` | `MISSING`, exit 1 → detection PROVEN |
| E10 | NEG-4: synthetic DSR register (on-time, late, open@25d, open@5d) `--today 2026-08-15 --machine` | `ON_TIME_PCT 50.0 closed=2`; `AT_RISK DSR-2026-003 age=25d`; day-5 case NOT flagged → day-21 logic CORRECT |
| E11 | PII sweep: emails, 11-digit codes, LV codes, IBAN, phones | Only `.example` placeholders; zero real PII |
| E12 | `redact-pii.py --all` | clean |
| E13 | `gitleaks detect --source . --no-git` (full tree) | no leaks |
| E14 | NEG-5: gitleaks on planted dummies (`AKIAQ3EGFCLVW9YX7B2M`, RSA PEM, `ghp_…`) | 3/3 detected (`generic-api-key`, `private-key`, `github-pat`) — first attempt used AWS's allowlisted example key, correctly NOT flagged |
| E15 | NEG-5b: dummy `vault_password="…"` | NOT detected → F-C3 |
| E16 | `grep gitleaks .github/workflows/` | no matches → F-C1 |
| E17 | Workflow→script reference check | 5/5 scripts PRESENT |
| E18 | Label reference extraction | 5 label sets referenced; none defined → F-B3 |
| E19 | YAML validation (16 files, python yaml) | all valid |
| E20 | RoPA parity: register IDs vs by-system | 6 IDs; `bitrix24-crm.md` ORPHAN → F-B1 |
| E21 | `git log --oneline` | scaffold-first history; no template provenance → F-A1 |
| E22 | Statutory-clock read: incident issue template requires detection timestamp; Art. 33 template carries assessment reference; DSR day-21 paging per E10 | PASS |
| E23 | Retention markers read (`retention-schedule.md` rule 4, ADR-0001) | counsel-to-confirm markers intact; no uniform-10y assertion → PASS (with F-C4 note) |

## 6. Final verdict

> **"Is jol-compliance 100% done?" — NO.**
> Structurally faithful and functionally sound, but blocked by 1 CRITICAL
> (F-D1 unverified CODEOWNERS) and 4 HIGH findings (F-B1 RoPA orphan, F-B2
> evidence finalization gap, F-B3 undefined workflow labels, F-C1 no CI
> secret scanning), plus the rename runbook (F-E1) — see
> `PRE_PUSH_CHECKLIST.md` for the ordered remediation.

---
Audit performed on branch `audit/2026-08-initial-build`. Scratch artifacts
kept under `/tmp/audit-scratch` for re-inspection. No findings below TRIVIAL
were auto-fixed; `CHANGES.md` records this.
