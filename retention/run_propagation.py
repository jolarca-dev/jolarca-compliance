"""Warehouse propagation CLI — applies the prod erasure/anonymization
manifest to the warehouse (lifecycle design: warehouse never retains what
prod has lawfully erased), then runs the raw-PII leak scan.

Usage:
  python -m retention.run_propagation --store <warehouse.json> \
      --manifest <manifest.json> --candidates <raw-values.txt> \
      --trail <audit.ndjson> --key-file <key>
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from retention import matrix as mx                       # noqa: E402
from retention.anonymize import KeyedAnonymizer          # noqa: E402
from retention.audit import AuditTrail                   # noqa: E402
from retention.retention_job import JsonRecordStore      # noqa: E402
from retention import warehouse                          # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--store", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--trail", required=True)
    ap.add_argument("--key-file", required=True)
    ap.add_argument("--today", default=None)
    args = ap.parse_args()

    today = date.fromisoformat(args.today) if args.today else date.today()
    matrix = mx.load_matrix()
    store = JsonRecordStore(args.store)
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    trail = AuditTrail(args.trail)
    anonymizer = KeyedAnonymizer.from_key_file(args.key_file)
    run_id = f"warehouse-prop-{today.isoformat()}-{uuid.uuid4().hex[:8]}"

    counts = warehouse.propagate_manifest(manifest, store, anonymizer,
                                          trail, run_id, matrix, today)
    print(f"run_id={run_id}")
    for k, v in counts.items():
        print(f"  {k}: {v}")

    known_raw = {ln.strip() for ln in
                 Path(args.candidates).read_text(encoding="utf-8").splitlines()
                 if ln.strip()}
    leaks = warehouse.scan_for_raw_pii(store, known_raw, matrix)
    for leak in leaks:
        print(f"LEAK {leak}")
    print("LEAK SCAN CLEAN" if not leaks else f"LEAK SCAN FAIL ({len(leaks)})")
    return 1 if leaks else 0


if __name__ == "__main__":
    sys.exit(main())
