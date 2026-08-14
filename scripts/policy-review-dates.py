#!/usr/bin/env python3
"""Policy review dates: find ISMS policies due for annual review.

Parses the "| Next review | YYYY-MM-DD |" metadata row in policies/*.md.
Exit 1 if any policy is already overdue (compliance-check gate); upcoming
reviews are reported as DUE lines (consumed by policy-review-reminder.yml).
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NEXT_REVIEW = re.compile(r"\|\s*Next review\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-days", type=int, default=30,
                    help="report reviews due within this many days")
    ap.add_argument("--today", default=None, help="override today (testing)")
    ap.add_argument("--machine", action="store_true")
    args = ap.parse_args()

    today = date.fromisoformat(args.today) if args.today else date.today()
    overdue: list[str] = []
    due: list[str] = []
    missing: list[str] = []

    for path in sorted((REPO / "policies").glob("[0-9][0-9]-*.md")):
        match = NEXT_REVIEW.search(path.read_text(encoding="utf-8"))
        rel = path.relative_to(REPO)
        if not match:
            missing.append(str(rel))
            continue
        review = date.fromisoformat(match.group(1))
        days_left = (review - today).days
        if days_left < 0:
            overdue.append(f"OVERDUE {rel} next_review={review.isoformat()} "
                           f"days_overdue={-days_left}")
        elif days_left <= args.max_days:
            due.append(f"DUE {rel} next_review={review.isoformat()} "
                       f"days_left={days_left}")

    if args.machine:
        for line in overdue + due:
            print(line)
        for rel in missing:
            print(f"MISSING_REVIEW_DATE {rel}")
    else:
        print(f"policy review check — today={today.isoformat()} "
              f"window={args.max_days}d")
        for line in overdue:
            print(f"  FAIL {line}")
        for line in due:
            print(f"  {line}")
        for rel in missing:
            print(f"  FAIL MISSING_REVIEW_DATE {rel}")
        if not (overdue or due or missing):
            print("  no policies due for review")

    return 1 if (overdue or missing) else 0


if __name__ == "__main__":
    sys.exit(main())
