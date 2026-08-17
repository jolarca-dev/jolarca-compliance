"""Append-only NDJSON audit trail — the record an auditor asks for.

Every decision (ANONYMIZED / DELETED / HELD / REPORT_ONLY / RETAINED_*)
is logged with class, country, record, age, mode and the reason that
drove the decision. The trail is append-only; rotation is out of scope
(RC-LOGS retention applies to the trail itself).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


class AuditTrail:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, run_id: str, domain: str, cls: str, country: str,
            record_id: str, age_days: int | None, decision: str,
            reason: str, mode: str = "") -> None:
        row = {
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "run_id": run_id, "domain": domain, "class": cls,
            "country": country, "record_id": record_id,
            "age_days": age_days, "decision": decision,
            "mode": mode, "reason": reason,
        }
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    def rows(self) -> list[dict]:
        if not self.path.is_file():
            return []
        return [json.loads(line) for line in
                self.path.read_text(encoding="utf-8").splitlines() if line]

    def summary(self, run_id: str) -> dict[str, int]:
        counts: dict[str, int] = {}
        for row in self.rows():
            if row["run_id"] == run_id:
                counts[row["decision"]] = counts.get(row["decision"], 0) + 1
        return counts
