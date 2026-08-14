# Contributing to jol-m-compliance

This repository has stricter rules than a code repository. Evidence integrity
is the product.

## Evidence-handling rules

1. **Version, never overwrite.** Documents progress `draft → vN → vN-signed`.
   A finalized (signed) document is immutable: to change it, create the next
   version and reference the superseded one.
2. **No deletion of finalized artifacts.** Deletion is only possible via a
   documented retention decision (see `docs/retention-schedule.md`) executed
   by the DPO. Git history must never be rewritten for this repo
   (`--force-push`, history rewrite = Critical incident, see SECURITY.md).
3. **Sign-off is recorded, not implied.** Every finalized document carries a
   metadata block: `Owner`, `Approved by`, `Date`, `Version`.
4. **No personal data.** Never commit DSR content, incident subject details,
   identity documents, or unredacted exports. `scripts/redact-pii.py` runs in
   pre-commit as a backstop, not as a license to be careless.
5. **Commits are audit history.** Use Conventional Commits
   (`policy:`, `evidence:`, `register:`, `dpia:`, `legal:`, `chore:`). Every
   policy change must appear in `CHANGELOG.md`.

## Pull request requirements

- PR template checklist fully answered: evidence class, retention class,
  lawful basis impact (if any).
- CODEOWNERS approval: `policies/`, `dpia/`, `ropa/` require DPO + compliance
  lead. Registers require compliance lead.
- CI green: markdown lint, YAML validation, signature/hash verification.

## Branching

- `main` is protected: no direct pushes, no force pushes, linear history.
- Long-lived evidence branches are forbidden; finalize via merge.

## Classification labels

| Label | Meaning | Extra requirement |
|---|---|---|
| `evidence:final` | Becomes immutable evidence | Hash into `audits/evidence-registry.csv` in the same PR |
| `evidence:draft` | Work in progress | redact-pii must pass |
| `policy-change` | Alters an ISMS policy | DPO approval + CHANGELOG entry |
