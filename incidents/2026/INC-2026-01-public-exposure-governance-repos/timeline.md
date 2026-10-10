# INC-2026-01 — Timeline

> **DRAFT — see `report.md`.** All times UTC. Sources are named per row because
> the two authoritative sources conflict (§2 of `report.md`) and an unstated
> provenance would hide that.

| When | Event | Source |
|---|---|---|
| 2026-08-14 | `jolarca-compliance` created (21:29:32Z); `jolarca-legal` created (22:01:37Z); `jolarca-infrastructure` created (20:00:58Z) | GitHub API `created_at` |
| 2026-08-15 | `jolarca-data` created (18:35:07Z); `jolarca` created (18:35:15Z) | GitHub API `created_at` |
| 2026-08-14 → 2026-09 | Repositories declared `visibility: private` in `jolarca-control/repos/*.yml` while live setting was `public` | `drift-findings.md` D-01 |
| 2026-09-09 11:13:49 | Branch delete event on `jolarca-compliance` recorded with `"public": false` — **conflicts** with D-31's claim of a public state on 2026-09-25 | GitHub repo events API |
| 2026-09-17 | **Awareness.** Delivery-chain audit observes the declared-versus-live visibility drift | `drift-findings.md` D-01, D-08 |
| 2026-09-17 → 2026-09-25 | Drift remains unremediated; recorded as blocking | `drift-findings.md` D-01 |
| 2026-09-25 | D-31 records that live public contents were enumerated: RoPA master register (1 150 B, populated), `ropa/by-system/{users-app,shipping}.md`, seven vendor assessments, `jolarca-legal/contracts/vendors/_register.csv`, DPA/NDA/employment templates | `drift-findings.md` D-31 |
| 2026-09-25 16:48:06 | `jolarca-control` created — now private | GitHub API `created_at` |
| 2026-09-25 16:59:48 | Push event on `jolarca-compliance` recorded with `"public": false` | GitHub repo events API |
| 2026-09-25 17:01:58 | Push event on `jolarca-compliance` recorded with `"public": false`; repository `pushed_at` | GitHub repo events API |
| 2026-09-25 → 2026-09-26 | **Containment.** The four affected repositories are flipped to private | `drift-findings.md` D-08 correction |
| 2026-09-26 | D-08 correction records that, since the flip, protection on those repositories is "neither readable (HTTP 403) nor enforced (`.protected = false`)" — the consequence now tracked as D-33 | `drift-findings.md` D-08, D-33 |
| 2026-09-27 | `jolarca-vendor` established as the vendor management governance layer; classified `internal`, method only, no supplier records | `jolarca-vendor/docs/ASSUMPTIONS.md` |
| **2026-09-28** | **This assessment performed.** Live visibility verified for all 16 repositories; personal-data and secret census run across the affected repositories; exposure window found indeterminate; record drafted | GitHub API; pattern census |

## Clock analysis

| Milestone | Date | Within requirement? |
|---|---|---|
| Awareness | 2026-09-17 | — |
| Art. 33 deadline had notification been due | 2026-09-20 | — |
| Containment complete | 2026-09-25/26 | Prompt relative to detection |
| Documented assessment | **2026-09-28** | **No — 11 days after awareness** |

The Art. 33 clock was never engaged, because the conclusion is that no personal
data breach occurred (§3.4 of `report.md`). The Art. 33(5) **documentation** duty
was nevertheless engaged from awareness, and it was met eleven days late. That
delay is recorded as a procedural failure rather than excused by the favourable
conclusion: had the conclusion gone the other way, the same delay would have been
a missed statutory deadline.

## Gaps in this timeline

1. The precise moment each repository became public is unknown — none of the
   available sources records it, and `created_at` bounds it only from above.
2. The precise moment each became private is unknown to the hour. The events API
   and D-08 disagree about whether `jolarca-compliance` was already private on
   2026-09-09.
3. Whether any third party cloned, mirrored or archived the content during the
   window is unknowable from server-side data. `forks_count = 0` excludes public
   forks only.

These gaps are the reason action A2 exists and why the residual risk in §6 of
`report.md` is stated at the conservative bound rather than the optimistic one.
