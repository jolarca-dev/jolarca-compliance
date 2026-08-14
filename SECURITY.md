# Security Policy

## Scope

This repository contains compliance evidence. A compromise here is a
**compliance incident of the highest severity**: integrity of evidence,
exposure of governance gaps, or leaked incident/DSR metadata can themselves
become reportable events.

## Reporting

Report any suspected issue (access anomaly, leaked secret, tampered evidence,
unauthorized fork) **immediately** to:

- **Email**: security@journeyoflife.example (PGP key published on the org page)
- **GitHub**: private vulnerability reporting is enabled for this repository

Do **not** open a public issue. Do **not** discuss findings outside the
incident channel.

## Severity classification

| Class | Examples | Response |
|---|---|---|
| Critical | Evidence tampering, repo content leaked, unauthorized admin access | 72h breach assessment clock starts (`policies/06-incident-response.md`) |
| High | Secrets committed, CODEOWNERS bypassed, branch protection disabled | 24h triage, DPO informed |
| Medium | Workflow misconfiguration, stale access not yet exercised | Next business day |

## What to include

1. What was observed and when (timestamps, commit SHAs where relevant).
2. Which artifacts may be affected (paths, registers).
3. Whether personal data may have been exposed.

## Commitments

- Acknowledgement within **24 hours**.
- Incident record opened in `incidents/` for every confirmed report, including
  near-misses.
- No retaliation for good-faith reporting.
