#!/usr/bin/env python3
"""Vendor review dates: processors nearing annual re-assessment or DPA expiry.

Reads vendor-assessments/register.csv. Exit 1 if any next_review/dpa_expiry
is already overdue, or if register/folder parity is broken (every register.csv
vendor must have a vendor-assessments/<vendor>/ folder and vice versa — audit
finding F-04). Upcoming items are emitted as DUE lines (consumed by
vendor-review-due.yml).
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path
from typing import Optional

REPO = Path(__file__).resolve().parent.parent
BASE = REPO / "vendor-assessments"
REGISTER = BASE / "register.csv"


def as_date(value: str) -> Optional[date]:
    try:
        return date.fromisoformat(value.strip())
    except (ValueError, AttributeError):
        return None


def register_parity() -> list[str]:
    """Every register.csv vendor needs a folder, every folder a csv row."""
    problems: list[str] = []
    with REGISTER.open(newline="", encoding="utf-8") as fh:
        csv_vendors = {row["vendor"].strip() for row in csv.DictReader(fh)}
    folders = {p.name for p in BASE.iterdir()
               if p.is_dir() and p.name != "tia"}
    for vendor in sorted(csv_vendors - folders):
        problems.append(f"PARITY register.csv vendor '{vendor}' has no folder")
    for folder in sorted(folders - csv_vendors):
        problems.append(f"PARITY folder '{folder}' missing from register.csv")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-days", type=int, default=60,
                    help="report items due within this many days")
    ap.add_argument("--today", default=None, help="override today (testing)")
    ap.add_argument("--machine", action="store_true")
    args = ap.parse_args()

    today = date.fromisoformat(args.today) if args.today else date.today()
    parity = register_parity()
    overdue: list[str] = []
    due: list[str] = []

    with REGISTER.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row.get("status") in {"terminated", "data-returned"}:
                continue
            vendor = row.get("vendor", "?")
            for field, kind in (("next_review", "re-assessment"),
                                ("dpa_expiry", "DPA-expiry")):
                when = as_date(row.get(field, ""))
                if when is None:
                    continue
                days_left = (when - today).days
                line = f"{vendor} {kind} date={when.isoformat()}"
                if days_left < 0:
                    overdue.append(f"OVERDUE {line} days_overdue={-days_left}")
                elif days_left <= args.max_days:
                    due.append(f"DUE {line} days_left={days_left}")

    if args.machine:
        for line in parity + overdue + due:
            print(line)
    else:
        print(f"vendor review check — today={today.isoformat()} "
              f"window={args.max_days}d")
        for line in parity:
            print(f"  FAIL {line}")
        for line in overdue:
            print(f"  FAIL {line}")
        for line in due:
            print(f"  {line}")
        if not (parity or overdue or due):
            print("  no vendor reviews due; register/folder parity OK")

    return 1 if (overdue or parity) else 0


if __name__ == "__main__":
    sys.exit(main())
