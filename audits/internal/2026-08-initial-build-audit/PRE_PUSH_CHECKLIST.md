# PRE-PUSH CHECKLIST — Operator Runbook (ordered)

Companion to `AUDIT_REPORT.md` (IA-2026-02). Execute in order; do not skip
steps. Steps marked **[BLOCKING]** gate the merge.

## 1. Rename repository → canonical `jol-compliance` (finding F-E1)

1. GitHub → repo Settings → rename `jol-m-compliance` → `jol-compliance`
   (GitHub preserves redirects for clone/push).
2. Local: `git remote set-url origin https://github.com/journeyoflife-org/jol-compliance.git`
3. Update every cross-repo reference in the portfolio (jol-marketplace,
   jol-infrastructure, jol-legal, org docs) — grep each repo for
   `jol-m-compliance`.
4. Verify: `git ls-remote origin` resolves; redirects work for the old URL.

## 2. Replace CODEOWNERS placeholder teams — **[BLOCKING]** (finding F-D1)

| Placeholder in `.github/CODEOWNERS` | Replace with real team | Verification |
|---|---|---|
| `@journeyoflife-org/dpo` | ______________ | team exists; members have 2FA |
| `@journeyoflife-org/compliance-leads` | ______________ | team exists; members have 2FA |
| `@journeyoflife-org/legal` | ______________ | team exists; members have 2FA |

Probe test: open a throwaway PR touching `policies/README.md`; confirm the
teams are pulled in as required reviewers. If no team is suggested, the
handle is wrong — branch protection would be unenforceable.

## 3. Remediate HIGH findings before the scaffold push

| Finding | Action |
|---|---|
| F-B1 | Assign `ROPA-007` to `ropa/by-system/bitrix24-crm.md` + add `master-register.csv` row (or merge under existing entry); re-run vendor/RoPA parity |
| F-B2 | Gate `evidence-hash.py --update` on an explicit finalization marker; add negative test (draft refuses registration) |
| F-B3 | Create all labels referenced by workflows (`dsr`, `sla-breach-risk`, `review-due`, `incident`, `critical`, `vendor`, `policy-change`, `access-review`, `audit`) |
| F-C1 | Add a gitleaks step to `.github/workflows/ci.yml` |

## 4. Push to scaffold branch (not directly to protected main)

```bash
git push origin HEAD:refs/heads/scaffold/initial-build
```

## 5. Enable repository security settings **[BLOCKING]**

- [ ] Confirm repository visibility: **private**
- [ ] Settings → Security → **Private vulnerability reporting**: ON
- [ ] Settings → Security → **Secret scanning + push protection**: ON (if entitlement allows; else rely on CI gitleaks from step 3)
- [ ] Settings → Branches → protect `main`:
  - [ ] Require pull request before merging (≥ 1 approving review)
  - [ ] Require review from Code Owners
  - [ ] Require status checks: `lint` (CI), `governance` (compliance-check), `analyze` (CodeQL)
  - [ ] Require branches to be up to date
  - [ ] **Do not allow force pushes**; **Do not allow deletions**
  - [ ] Include administrators
- [ ] Settings → General → disable "Allow merge commits" if linear history is
  policy (CONTRIBUTING.md says linear)

## 6. Open PR scaffold → main; let all 8 workflows run against the repo

- [ ] `ci.yml`, `compliance-check.yml`, `codeql.yml` green on the PR
- [ ] Manually trigger the 5 scheduled workflows (`workflow_dispatch`) and
      confirm each completes without label/reference errors (F-B3 regression check)
- [ ] Qodana: `make qodana` → 0 problems

## 7. Counsel sign-off **[BLOCKING for G3, recommended now]** (finding F-C4)

- [ ] LT/LV/EE accounting-retention variants confirmed per legal entity;
      sign-off rows added to `docs/retention-schedule.md` and ADR-0001
- [ ] Boundary decision recorded: canonical legal texts in `jol-legal/legal-texts/`
      vs. this repo (finding F-E2)

## 8. Merge and tag

- [ ] Merge PR (squash or rebase per linear-history policy)
- [ ] Tag `v0.1.0`; CHANGELOG `[0.1.0]` already carries the content
- [ ] Announce to management review; file next internal audit per
      `audits/audit-plan-2026.md` §4.3 (2026-Q3 access control)
