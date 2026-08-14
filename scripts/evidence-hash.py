#!/usr/bin/env python3
"""Evidence integrity: hash finalized evidence into the registry / verify it.

--update  scan evidence roots, add/refresh rows in audits/evidence-registry.csv
--verify  recompute SHA-256 for every row with status=final and fail on any
          mismatch or missing file (treated as tampering until cleared).

Evidence roots are scanned recursively; README.md and .gitkeep markers are
excluded. Registry rows are append-only: a changed file gets a NEW row and
the previous row is marked superseded (history is never rewritten).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REGISTRY = REPO / "audits" / "evidence-registry.csv"
ROOTS = ["audits/gate-evidence", "incidents", "dpia", "management-review"]
HEADER = ["path", "sha256", "registered_at", "registered_by",
          "gate", "control_ref", "status"]
SKIP_NAMES = {"README.md", ".gitkeep"}
SKIP_SUFFIXES = {".gitkeep"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def evidence_files() -> list[Path]:
    files: list[Path] = []
    for root in ROOTS:
        base = REPO / root
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if p.is_file() and p.name not in SKIP_NAMES \
                    and p.suffix not in SKIP_SUFFIXES:
                files.append(p.relative_to(REPO))
    return files


def load_registry() -> list[dict[str, str]]:
    if not REGISTRY.is_file():
        return []
    with REGISTRY.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def save_registry(rows: list[dict[str, str]]) -> None:
    with REGISTRY.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=HEADER, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def update(registered_by: str) -> int:
    rows = load_registry()
    by_path: dict[str, dict[str, str]] = {
        r["path"]: r for r in rows if r.get("status") == "final"
    }
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    added = refreshed = 0
    for rel in evidence_files():
        digest = sha256(REPO / rel)
        existing = by_path.get(str(rel))
        if existing is None:
            rows.append({"path": str(rel), "sha256": digest,
                         "registered_at": now, "registered_by": registered_by,
                         "gate": "", "control_ref": "", "status": "final"})
            by_path[str(rel)] = rows[-1]
            added += 1
        elif existing["sha256"] != digest:
            existing["status"] = "superseded"
            rows.append({"path": str(rel), "sha256": digest,
                         "registered_at": now, "registered_by": registered_by,
                         "gate": existing["gate"],
                         "control_ref": existing["control_ref"],
                         "status": "final"})
            by_path[str(rel)] = rows[-1]
            refreshed += 1
    save_registry(rows)
    print(f"evidence-hash: {added} added, {refreshed} superseded+rehashed")
    return 0


def verify(machine: bool) -> int:
    rows = [r for r in load_registry() if r.get("status") == "final"]
    problems: list[str] = []
    for row in rows:
        path = REPO / row["path"]
        if not path.is_file():
            problems.append(f"MISSING {row['path']}")
        elif sha256(path) != row["sha256"]:
            problems.append(f"MISMATCH {row['path']}")
    if machine:
        for p in problems:
            print(p)
        if not problems:
            print(f"OK verified={len(rows)}")
    else:
        print(f"evidence-hash --verify: {len(rows)} final row(s)")
        for p in problems:
            print(f"  FAIL {p}")
        if not problems:
            print("  all hashes match")
    return 1 if problems else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--update", action="store_true")
    group.add_argument("--verify", action="store_true")
    ap.add_argument("--registered-by", default="automation")
    ap.add_argument("--machine", action="store_true")
    args = ap.parse_args()
    return update(args.registered_by) if args.update else verify(args.machine)


if __name__ == "__main__":
    sys.exit(main())
