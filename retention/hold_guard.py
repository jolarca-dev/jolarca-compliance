"""Legal-hold guard (Step 27 integration point).

Every retention job MUST consult the guard before acting; a held record is
never anonymized or deleted regardless of class or age. In production the
guard is the Step 27 legal-hold service; here the interface is identical and
backed by a JSON file so jobs and tests run against the same contract.

Hold record shape:
    {"record_id": str, "hold_id": str, "reason": str,
     "placed_by": str, "placed_at": "YYYY-MM-DD", "released_at": null|str}
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol


class HoldGuard(Protocol):
    def is_held(self, record_id: str) -> bool: ...
    def hold_info(self, record_id: str) -> dict | None: ...


class JsonHoldGuard:
    """File-backed implementation of the Step 27 hold contract."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._holds: dict[str, dict] = {}
        if self.path.is_file():
            for hold in json.loads(self.path.read_text(encoding="utf-8")):
                if not hold.get("released_at"):
                    self._holds[hold["record_id"]] = hold

    def is_held(self, record_id: str) -> bool:
        return record_id in self._holds

    def hold_info(self, record_id: str) -> dict | None:
        return self._holds.get(record_id)

    def place(self, record_id: str, hold_id: str, reason: str,
              placed_by: str, placed_at: str) -> None:
        self._holds[record_id] = {
            "record_id": record_id, "hold_id": hold_id, "reason": reason,
            "placed_by": placed_by, "placed_at": placed_at, "released_at": None,
        }

    def release(self, record_id: str, released_at: str) -> None:
        if record_id in self._holds:
            self._holds[record_id]["released_at"] = released_at
            del self._holds[record_id]


class NoHoldGuard:
    """Explicit no-holds guard — jobs still call it; absence is a fact,
    not an oversight (audit trail records guard=none)."""

    def is_held(self, record_id: str) -> bool:
        return False

    def hold_info(self, record_id: str) -> dict | None:
        return None
