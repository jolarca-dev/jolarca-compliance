# Risk Register

## Scoring model

`Risk = Likelihood (1–5) × Impact (1–5)`

| Band | Score | Action |
|---|---|---|
| Critical | ≥ 20 | Immediate treatment; management informed; launch blocker |
| High | 12–19 | Treatment plan mandatory within 30 days |
| Medium | 6–11 | Treat or formally accept with owner |
| Low | ≤ 5 | Monitor; revisit at gates |

Impact dimensions: regulatory (fines, Art. 83), data subjects, financial,
reputational, operational. Regulatory impact is capped at nothing less than
"High" for any personal-data risk by policy choice.

## Appetite statement

We accept **no** appetite for risks of unlawful processing of personal data.
Financial and operational risks are accepted only with named owner,
mitigation path, and expiry review.

## Process

- Register reviewed at every gate (G0–G4), quarterly, and after any
  Critical incident.
- Every accepted/mitigated risk with score ≥ 6 gets a treatment plan in
  `treatment-plans/` (owner, actions, due dates, residual score target).
- Risk IDs (`RSK-NNN`) are referenced from exceptions, postmortems, and
  treatment plans — never duplicated, never deleted (status changes only).
