# Incident Management

## Lifecycle

`intake → triage (severity) → 72h assessment → notification decision →
containment/eradication → postmortem → register closed (evidence hashed)`

1. Intake: incident issue template or `templates/` documents; register entry
   created immediately (`register.md`), including near-misses.
2. 72-hour clock: starts at awareness. Assessment concludes with a
   **documented** decision — notify / not notify / notify data subjects.
3. Notifications: authority template (Art. 33) per LT/LV/EE DPA; data-subject
   template (Art. 34) per language, only where high risk.
4. Postmortems: blameless, action-tracked; Critical/High mandatory.
5. One folder per incident under the detection year (`2026/INC-YYYY-NN-slug/`)
   containing: report, timeline, evidence references (hashes), decisions log.
6. **No personal data in incident records** — pseudonyms and case IDs only.
7. Quarterly game days in `game-days/` — logs + findings.

Closure criteria: decision documented, actions owned & dated, evidence hashed
into `audits/evidence-registry.csv`, register updated.
