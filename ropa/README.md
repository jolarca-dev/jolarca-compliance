# ROPA — Record of Processing Activities (GDPR Art. 30)

## Maintenance rules

1. **Update on ANY new data flow.** No feature ships that adds, changes, or
   removes personal-data processing without a RoPA PR in the same release.
2. **Reviewed at every gate** (G0–G4) and at least annually.
3. One file per system under `by-system/`; the machine-readable
   `master-register.csv` is the authoritative index for regulator requests —
   it must be answerable in hours, not weeks.
4. Every row must name: purpose, categories of subjects & data, lawful basis,
   retention period/class, recipients, and international transfers.
5. RoPA change = trigger to check DPIA necessity (`dpia/README.md`).

## Contents

| Path | Content |
|---|---|
| `by-system/*.md` | Narrative record per system |
| `diagrams/` | Data-flow diagrams (Mermaid), kept in sync with records |
| `master-register.csv` | Machine-readable index (ROPA-NNN IDs) |

## Schema (master-register.csv)

`id, system, purpose, lawful_basis, data_categories, subjects, retention_class, recipients, transfer_mechanism, last_reviewed`

Retention classes resolve via `docs/retention-schedule.md`.
