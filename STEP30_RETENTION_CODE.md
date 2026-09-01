# STEP 30 — Retention as executable code

- **Date:** 2026-08-17
- **Role:** Senior Data Engineer — "retention policy is only real if a job
  runs it and a test proves it"
- **Inputs:** STEP 26 per-country matrix (`docs/retention-schedule.md`),
  ADR-0001 (anonymize-don't-delete), Step 27 legal-hold guard contract
- **Code:** `retention/` (stdlib + PyYAML only) · **Proofs:**
  `retention/tests/test_retention.py` (15 tests) · **CI gate:**
  `.github/workflows/retention-ci.yml` (daily)

## 1. Matrix as data — `retention/matrix.yaml`

Single source of truth; every job reads it, nothing is hardcoded. The
declared `mode` field is **never trusted**: `retention/matrix.py` re-derives
the effective mode — report-only wins whenever counsel status is
unconfirmed, the period is unset, or a Step 27 hold stands. Test
`test_declared_mode_never_trusted` proves a hostile `mode: active` flip in
YAML still cannot go destructive.

| Class | Action | LT | LV | EE |
|---|---|---|---|---|
| RC-ACCT-10Y | anonymize-dont-delete | **active** 10y (Law on Accounting of the Republic of Lithuania) | report-only `[COUNSEL-TO-CONFIRM]` | report-only `[COUNSEL-TO-CONFIRM]` |
| RC-PAYROLL-50Y | anonymize-dont-delete | **report-only** — step27_hold until counsel releases the class (50y) | report-only | report-only |
| RC-ACCOUNT | hard-delete | active 2y (limitation, confirmed) | report-only | report-only |
| RC-KYC | anonymize-dont-delete | active 5y operational | report-only | report-only |
| RC-AI / RC-LOCATION / RC-DSR-VERIFY | hard-delete | active 30d / 90d / immediate | same (ALL) | same (ALL) |
| RC-SUPPORT | hard-delete | active 3y | same (ALL) | same (ALL) |
| RC-LOGS | archive-then-delete | active 5y | same (ALL) | same (ALL) |
| RC-MARKETING-CONSENT | hard-delete | report-only | report-only | report-only |
| RC-EVIDENCE | never-delete | short-circuits before any horizon math | same | same |

## 2. Jobs per class — one engine, five-step decision order

`retention/retention_job.py` — per record, non-negotiable order:
**1) hold guard → 2) never-delete → 3) effective mode → 4) horizon → 5) action.**

| Class | Job | Domain owner | Cadence (`scheduler.py`) |
|---|---|---|---|
| RC-AI, RC-LOCATION, RC-DSR-VERIFY | `run_retention --domain prod` | marketplace DB | daily |
| RC-ACCOUNT, RC-SUPPORT, RC-MARKETING-CONSENT | same | marketplace DB | weekly |
| RC-KYC, RC-ACCT-10Y, RC-PAYROLL-50Y, RC-LOGS | same | marketplace DB + warehouse-native | monthly |
| RC-EVIDENCE | same | all domains | yearly (verification only) |
| Warehouse propagation | `run_propagation` | warehouse (jolarca-data) | after every prod run (manifest-driven) |

### Hold-guard integration (critical) — PROVEN

`retention/hold_guard.py` implements the Step 27 contract
(`is_held` / `hold_info`); production plugs the Step 27 service, jobs and
tests use the same interface. The guard is consulted **before any other
decision**, including report-only.

Proof (E2E run, 2026-08-17): `INV-2014-LT-HELD` — age **4597d**, horizon
3650d, class LT **active** — decision `HELD`, fields byte-identical after
the run; `PAY-1990-LT-HELD` likewise. Unit test
`test_held_record_past_horizon_is_preserved` asserts field equality against
the pristine fixture. Audit rows carry the hold ID and reason:

```json
{"record_id": "INV-2014-LT-HELD", "age_days": 4597, "decision": "HELD",
 "reason": "legal hold HLD-2026-001: Active litigation — Step 27 hold"}
```

### Adversarial anonymization — PROVEN, not asserted

`retention/verify_anonymization.py` runs three attacks on anonymized
records: direct match, linkage/substring scan, and keyed re-hash. E2E on the
post-run cohort (2 records, 10 attacker-known candidates):

```text
ADVERSARIAL PASS — 0 re-identification paths across 2 records, 10 candidates
sanity (with key): keyed re-id matches = 8
SANITY PASS — attack succeeds only with key custody
```

The sanity run is the honest half: with key custody the attack works, so
irreversibility demonstrably rests on **key destruction/custody** (Vault in
production; the demo key never enters the repo — `.gitignore` hygiene
applies to `retention/runs/`).

### Report-only for counsel-pending classes — PROVEN

RC-PAYROLL-50Y record with age **19101d (52 years — past even the 50-year
horizon)**: decision `REPORT_ONLY`, reason `step27_hold: class held until
counsel releases it; would=anonymize-dont-delete`, zero mutation. LV/EE and
RC-MARKETING-CONSENT behave identically. Test
`test_counsel_pending_records_never_mutated` asserts byte-equality for all
four report-only records. **Nothing destructive is possible on unconfirmed
retention — enforced in code, not in prose.**

## 3. Audit trail + scheduling

Every decision appends an NDJSON row (`retention/audit.py`): run_id, domain,
class, country, record, age, decision, mode, **reason**. E2E run produced 18
rows for 15 records (decisions: ANONYMIZED 2, ARCHIVED_THEN_DELETED 1,
DELETED 4, HELD 2, REPORT_ONLY 4, RETAINED_NEVER 1, RETAINED_YOUNG 1).
`test_audit_trail_matches_decisions` proves trail ≡ engine counts and that
no row lacks a reason.

`scheduler.py` tracks last-run per class:domain with cadence + 3-day grace;
overdue jobs emit `ALERT` lines (tested: 40-day-old monthly job alerts;
never-run job alerts). Production runs under the platform CronJob;
`retention-ci.yml` re-proves the engine daily and opens an incident issue if
the proofs go red.

## 4. Warehouse vs. prod split

- **Prod job** (`--domain prod`) owns marketplace DB retention.
- **Warehouse-native** (`--domain warehouse`) owns mart rows with their own
  horizons — same `matrix.yaml`.
- **Propagation** (`run_propagation`): the warehouse applies the prod
  erasure/anonymization manifest — the warehouse never retains what prod has
  lawfully erased (lifecycle design). E2E: `PROPAGATED_ANONYMIZED: 1,
  PROPAGATED_DELETED: 1, PROPAGATION_MISS: 1` (deliberate ghost row —
  misses are reconciliation findings, logged, not ignored), followed by
  `LEAK SCAN CLEAN` (no known raw identifier survives in any PII field;
  pre-propagation scan found leaks — the scan demonstrably works).

## 5. Reproduce

```bash
.venv/bin/python -m unittest retention.tests.test_retention -v   # 15 proofs
.venv/bin/python -m retention.run_retention --domain prod \
    --store <store.json> --holds <holds.json> --trail <audit.ndjson> \
    --key-file <vault-managed-key> --today YYYY-MM-DD
.venv/bin/python -m retention.verify_anonymization \
    --dataset <post-run-store.json> --candidates <raw-values.txt>
```

## 6. Open items (not done — honestly)

1. **Prod adapters**: `JsonRecordStore` stands in for the marketplace DB and
   warehouse marts; the real adapters (Postgres erasure queries, dbt models
   in jolarca-data) are the next step — the engine and proofs carry over.
2. **Key custody**: production key lives in Vault with two-person rule
   (policy 04); demo keys are ephemeral.
3. **Counsel releases**: RC-PAYROLL-50Y goes active only when counsel scopes
   the 50-year class (STEP 26 open item #2); LV/EE rows on counsel sign-off.
   Both are config flips in `matrix.yaml` — no code change.
4. **Step 27 wiring**: swap `JsonHoldGuard` for the Step 27 service client
   behind the same `HoldGuard` protocol.
