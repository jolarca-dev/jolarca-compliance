# Audits & Certification Evidence

## Evidence rules (immutable by default)

1. Every piece of evidence is linked to a control (Annex A / TSC / PCI req)
   and to a gate where applicable (`docs/compliance-matrix.md`).
2. Finalized evidence is hashed into `evidence-registry.csv` and verified
   weekly (`evidence-integrity.yml`). A hash mismatch is a Critical incident.
3. Evidence is never edited after finalization — supersede with a new file
   and a new registry row; the old row stays with status `superseded`.
4. Binary originals (signed PDFs, reports) live in the encrypted vault /
   Git LFS; this repo stores pointers + hashes.

## Layout

| Path | Content |
|---|---|
| `audit-plan-2026.md` | Internal audit program plan (types, calendar, SLAs) |
| `evidence-registry.csv` | THE hash registry (schema locked) |
| `gate-evidence/G0–G4/` | Roadmap gates — archived at each pass, immutable |
| `internal-audit-*.md` | Internal audit reports: findings, remediation, verification |
| `soc2/` | Evidence mapped per Trust Services Criterion (CC1–CC9) |
| `iso27001/` | Evidence per Annex A control + Statement of Applicability |
| `pen-tests/` | Reports + remediation tracking (critical/high = launch blockers) |
| `access-reviews/` | Quarterly reviews with sign-offs |

## Registry schema

`path, sha256, registered_at, registered_by, gate, control_ref, status`

Manage exclusively via `scripts/evidence-hash.py` (`--update` / `--verify`).
