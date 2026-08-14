# DSR Register (anonymized index)

> **No personal data here.** Case IDs, types, dates, and statuses only.
> Parsed by `scripts/dsr-sla-report.py` — keep the table format exact.

| Case ID | Type | Received | Identity verified | Deadline | Responded | On time | Status |
|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — |

Field rules:

- Case ID mirrors the DSR system (`DSR-YYYY-NNN`); content lives there.
- Deadline = received + 30 days (extension recorded separately if granted).
- Status values: `open`, `info-requested`, `fulfilled`, `refused`, `withdrawn`.
- Closed rows are never removed.
