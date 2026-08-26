"""Scheduling + missed-run alerting.

State file: retention/runs/state.json — {"last_run": {"<class>:<domain>":
"YYYY-MM-DD"}}. A job that has not run within cadence + grace emits an
ALERT line (the schedule workflow turns these into a GitHub issue).
"""
from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

# Cadence per class (days). Daily for short-horizon classes, monthly for
# long-horizon ones. This is scheduling config; the RETENTION periods live
# only in matrix.yaml.
CLASS_CADENCE_DAYS = {
    "RC-AI": 1, "RC-LOCATION": 1, "RC-DSR-VERIFY": 1,
    "RC-ACCOUNT": 7, "RC-SUPPORT": 7, "RC-MARKETING-CONSENT": 7,
    "RC-KYC": 30, "RC-ACCT-10Y": 30, "RC-PAYROLL-50Y": 30,
    "RC-LOGS": 30, "RC-EVIDENCE": 365,
}
GRACE_DAYS = 3


class RunState:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.state = {"last_run": {}}
        if self.path.is_file():
            self.state = json.loads(self.path.read_text(encoding="utf-8"))

    def key(self, cls: str, domain: str) -> str:
        return f"{cls}:{domain}"

    def record_run(self, cls: str, domain: str, when: date) -> None:
        self.state["last_run"][self.key(cls, domain)] = when.isoformat()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.state, indent=2), encoding="utf-8")

    def last_run(self, cls: str, domain: str) -> date | None:
        raw = self.state["last_run"].get(self.key(cls, domain))
        return date.fromisoformat(raw) if raw else None

    def missed(self, cls: str, domain: str, today: date) -> int:
        """Days overdue (0 = fine, -1 = never ran and due)."""
        cadence = CLASS_CADENCE_DAYS.get(cls, 30)
        last = self.last_run(cls, domain)
        if last is None:
            return -1
        due = last + timedelta(days=cadence + GRACE_DAYS)
        return max(0, (today - due).days)


def alerts(state: RunState, jobs: list[tuple[str, str]],
           today: date) -> list[str]:
    out: list[str] = []
    for cls, domain in jobs:
        overdue = state.missed(cls, domain, today)
        if overdue == -1:
            out.append(f"ALERT {cls}:{domain} has NEVER run")
        elif overdue > 0:
            out.append(f"ALERT {cls}:{domain} missed its schedule by "
                       f"{overdue}d")
    return out
