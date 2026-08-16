#!/usr/bin/env python3
"""DSR SLA report: on-time % vs the 30-day GDPR deadline (Art. 12(3)).

Parses the markdown table in data-subject-requests/register.md.
Open requests past --warn-days are emitted as AT_RISK lines (consumed by
dsr-sla-monitor.yml to page the DPO). Stdlib only.
"""
from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path


def parse_rows(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    header: list[str] = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not header:
            header = [c.lower() for c in cells]
            continue
        if all(set(c) <= {"-", ":", " "} for c in cells):
            continue
        if len(cells) != len(header) or set(cells[0]) <= {"—", "-", ""}:
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def as_date(value: str) -> Optional[date]:
    try:
        return date.fromisoformat(value.strip())
    except (ValueError, AttributeError):
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("register", help="path to data-subject-requests/register.md")
    ap.add_argument("--warn-days", type=int, default=21,
                    help="page the DPO when an open DSR passes this age")
    ap.add_argument("--today", default=None, help="override today (YYYY-MM-DD, testing)")
    ap.add_argument("--machine", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    today = as_date(args.today) if args.today else date.today()
    text = Path(args.register).read_text(encoding="utf-8")
    rows = parse_rows(text)

    closed_on_time = closed_total = 0
    at_risk: list[str] = []
    for row in rows:
        received = as_date(row.get("received", ""))
        if received is None:
            continue
        status = row.get("status", "open").lower()
        responded = as_date(row.get("responded", ""))
        if status in {"fulfilled", "refused", "withdrawn"} and responded:
            closed_total += 1
            deadline = received + timedelta(days=30)
            if responded <= deadline:
                closed_on_time += 1
        elif status in {"open", "info-requested"}:
            age = (today - received).days
            if age >= args.warn_days:
                at_risk.append(
                    f"AT_RISK {row.get('case id', '?')} age={age}d "
                    f"status={status} received={received.isoformat()}"
                )

    pct = (100.0 * closed_on_time / closed_total) if closed_total else None
    if args.machine:
        if pct is not None:
            print(f"ON_TIME_PCT {pct:.1f} closed={closed_total}")
        for line in at_risk:
            print(line)
    else:
        print(f"DSR SLA report — {today.isoformat()}")
        if pct is not None:
            print(f"  on-time: {pct:.1f}% ({closed_on_time}/{closed_total} closed)")
        else:
            print("  no closed DSRs yet")
        for line in at_risk:
            print(f"  {line}")
        if not at_risk:
            print("  no open DSRs past the warn threshold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
