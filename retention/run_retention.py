"""Retention job CLI — runs one domain against the matrix.

Usage:
  python -m retention.run_retention --domain prod \
      --store retention/tests/fixtures/records_prod.json \
      --holds retention/tests/fixtures/holds.json \
      --trail retention/runs/audit.ndjson \
      --key-file retention/runs/anon.key [--today 2026-08-17]

Exit codes: 0 = run completed (report-only included), 1 = config/alert error.
Missed-schedule ALERTs are printed; the workflow turns them into issues.
"""
from __future__ import annotations

import argparse
import sys
import uuid
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from retention import matrix as mx                      # noqa: E402
from retention.anonymize import KeyedAnonymizer         # noqa: E402
from retention.audit import AuditTrail                  # noqa: E402
from retention.hold_guard import JsonHoldGuard, NoHoldGuard  # noqa: E402
from retention.retention_job import JsonRecordStore, run     # noqa: E402
from retention.scheduler import RunState, alerts             # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--domain", required=True, choices=["prod", "warehouse"])
    ap.add_argument("--store", required=True)
    ap.add_argument("--holds", default=None, help="legal-hold JSON (Step 27)")
    ap.add_argument("--trail", required=True)
    ap.add_argument("--key-file", required=True)
    ap.add_argument("--state", default="retention/runs/state.json")
    ap.add_argument("--today", default=None)
    args = ap.parse_args()

    today = date.fromisoformat(args.today) if args.today else date.today()
    matrix = mx.load_matrix()
    store = JsonRecordStore(args.store)
    guard = JsonHoldGuard(args.holds) if args.holds else NoHoldGuard()
    trail = AuditTrail(args.trail)
    anonymizer = KeyedAnonymizer.from_key_file(args.key_file)
    anonymizer.save_key(args.key_file)  # persist generated key to custody file
    run_id = f"{args.domain}-{today.isoformat()}-{uuid.uuid4().hex[:8]}"

    counts = run(args.domain, store, guard, trail, anonymizer, run_id,
                 today, matrix)
    print(f"run_id={run_id} domain={args.domain}")
    for decision, n in sorted(counts.items()):
        print(f"  {decision}: {n}")

    state = RunState(args.state)
    jobs = [(c, args.domain) for c in mx.classes_for_domain(matrix, args.domain)]
    for cls, domain in jobs:
        state.record_run(cls, domain, today)
    for line in alerts(state, jobs, today):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
