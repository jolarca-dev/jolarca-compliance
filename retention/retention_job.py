"""Retention job engine — one pipeline, every class, both domains.

Decision order per record (deliberate, non-negotiable):
  1. HOLD GUARD — held records are never touched, regardless of class/age
  2. NEVER-DELETE — RC-EVIDENCE-style classes short-circuit before any horizon
  3. EFFECTIVE MODE — report-only classes log what WOULD happen; no mutation
  4. HORIZON — under-age records are retained
  5. ACTION — anonymize-dont-delete / hard-delete / archive-then-delete

Record shape (JSON store):
  {"id": str, "class": str, "country": str,
   "anchor_date": "YYYY-MM-DD", "fields": {...}}
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from retention import matrix as mx
from retention.anonymize import KeyedAnonymizer, TOMBSTONE
from retention.audit import AuditTrail
from retention.hold_guard import HoldGuard


class JsonRecordStore:
    """File-backed record store standing in for prod DB / warehouse marts."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.records: list[dict] = data["records"]

    def by_class(self, cls: str) -> list[dict]:
        return [r for r in self.records if r["class"] == cls]

    def get(self, record_id: str) -> dict | None:
        for r in self.records:
            if r["id"] == record_id:
                return r
        return None

    def replace(self, record_id: str, new_fields: dict) -> None:
        rec = self.get(record_id)
        if rec is not None:
            rec["fields"] = new_fields

    def delete(self, record_id: str) -> None:
        self.records = [r for r in self.records if r["id"] != record_id]

    def save(self) -> None:
        self.path.write_text(json.dumps({"records": self.records},
                                        indent=2, ensure_ascii=False),
                             encoding="utf-8")


def _age_days(record: dict, today: date) -> int | None:
    anchor = record.get("anchor_date")
    if not anchor:
        return None
    return (today - date.fromisoformat(anchor)).days


def run(domain: str, store: JsonRecordStore, guard: HoldGuard,
        trail: AuditTrail, anonymizer: KeyedAnonymizer, run_id: str,
        today: date, matrix: dict | None = None) -> dict[str, int]:
    matrix = matrix or mx.load_matrix()
    counts: dict[str, int] = {}

    def bump(decision: str) -> None:
        counts[decision] = counts.get(decision, 0) + 1

    for cls_name in mx.classes_for_domain(matrix, domain):
        cls_cfg = matrix["classes"][cls_name]
        for record in store.by_class(cls_name):
            rid, country = record["id"], record.get("country", "ALL")
            age = _age_days(record, today)

            # 1) hold guard — before anything else, always
            if guard.is_held(rid):
                info = guard.hold_info(rid) or {}
                trail.log(run_id, domain, cls_name, country, rid, age,
                          "HELD", f"legal hold {info.get('hold_id', '?')}: "
                                  f"{info.get('reason', 'no reason')}",
                          mode="hold")
                bump("HELD")
                continue

            # 2) never-delete short-circuits before any horizon math
            if cls_cfg["action"] == "never-delete":
                trail.log(run_id, domain, cls_name, country, rid, age,
                          "RETAINED_NEVER", "class is never-delete", mode="")
                bump("RETAINED_NEVER")
                continue

            # 3) effective mode — untrusted, re-derived
            mode, mode_reason = mx.effective_mode(cls_cfg, country)
            horizon = mx.horizon_days(cls_cfg, country)
            past = horizon is not None and age is not None and age >= horizon

            if mode == "report-only":
                would = cls_cfg["action"] if past else "retain (under horizon)"
                trail.log(run_id, domain, cls_name, country, rid, age,
                          "REPORT_ONLY", f"{mode_reason}; would={would}",
                          mode=mode)
                bump("REPORT_ONLY")
                continue

            # 4) horizon
            if not past:
                trail.log(run_id, domain, cls_name, country, rid, age,
                          "RETAINED_YOUNG",
                          f"age {age}d < horizon {horizon}d", mode=mode)
                bump("RETAINED_YOUNG")
                continue

            # 5) action
            action = cls_cfg["action"]
            pii = cls_cfg.get("pii_fields", [])
            if action == "anonymize-dont-delete":
                new_fields = anonymizer.anonymize_record(record["fields"], pii)
                store.replace(rid, new_fields)
                trail.log(run_id, domain, cls_name, country, rid, age,
                          "ANONYMIZED",
                          f"past horizon ({horizon}d); PII {pii} → keyed "
                          f"digests; fiscal fields retained (ADR-0001)",
                          mode=mode)
                bump("ANONYMIZED")
            elif action == "hard-delete":
                store.delete(rid)
                trail.log(run_id, domain, cls_name, country, rid, age,
                          "DELETED", f"past horizon ({horizon}d)", mode=mode)
                bump("DELETED")
            elif action == "archive-then-delete":
                archived = {k: (TOMBSTONE if k in pii else v)
                            for k, v in record["fields"].items()}
                archived["__archived__"] = today.isoformat()
                store.replace(rid, archived)
                trail.log(run_id, domain, cls_name, country, rid, age,
                          "ARCHIVED_THEN_DELETED",
                          f"past horizon ({horizon}d); archived copy, PII "
                          f"tombstoned", mode=mode)
                bump("ARCHIVED_THEN_DELETED")

    store.save()
    return counts
