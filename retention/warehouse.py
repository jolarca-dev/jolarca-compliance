"""Warehouse retention — propagates from prod erasure per the lifecycle design.

Ownership split (documented contract):
  - retention_job.py --domain prod      owns marketplace DB retention
  - retention_job.py --domain warehouse owns warehouse-native retention
    (mart rows with their own horizons), reading the SAME matrix.yaml
  - THIS module applies the prod erasure/anonymization MANIFEST to the
    warehouse: warehouse never retains what prod has lawfully erased.
"""
from __future__ import annotations

from datetime import date

from retention.anonymize import KeyedAnonymizer
from retention.audit import AuditTrail
from retention.retention_job import JsonRecordStore


def propagate_manifest(manifest: list[dict], wh_store: JsonRecordStore,
                       anonymizer: KeyedAnonymizer, trail: AuditTrail,
                       run_id: str, matrix: dict,
                       today: date) -> dict[str, int]:
    """Apply prod decisions to warehouse rows.

    Manifest entries: {"record_id": str, "class": str,
                       "action": "anonymize"|"delete"}
    """
    counts = {"PROPAGATED_ANONYMIZED": 0, "PROPAGATED_DELETED": 0,
              "PROPAGATION_MISS": 0}
    for entry in manifest:
        rid, cls_name = entry["record_id"], entry["class"]
        rec = wh_store.get(rid)
        if rec is None:
            trail.log(run_id, "warehouse", cls_name, "-", rid, None,
                      "PROPAGATION_MISS",
                      "prod manifest row has no warehouse counterpart — "
                      "reconciliation finding")
            counts["PROPAGATION_MISS"] += 1
            continue
        pii = matrix["classes"][cls_name].get("pii_fields", [])
        if entry["action"] == "anonymize":
            wh_store.replace(rid, anonymizer.anonymize_record(rec["fields"], pii))
            trail.log(run_id, "warehouse", cls_name, rec.get("country", "-"),
                      rid, None, "PROPAGATED_ANONYMIZED",
                      "prod erasure propagation (lifecycle design)")
            counts["PROPAGATED_ANONYMIZED"] += 1
        elif entry["action"] == "delete":
            wh_store.delete(rid)
            trail.log(run_id, "warehouse", cls_name, rec.get("country", "-"),
                      rid, None, "PROPAGATED_DELETED",
                      "prod erasure propagation (lifecycle design)")
            counts["PROPAGATED_DELETED"] += 1
    wh_store.save()
    return counts


def scan_for_raw_pii(wh_store: JsonRecordStore, known_raw_values: set[str],
                     matrix: dict) -> list[str]:
    """Leak scan: any warehouse field still carrying a known raw identifier
    is a propagation failure."""
    leaks: list[str] = []
    for rec in wh_store.records:
        cls_cfg = matrix["classes"].get(rec["class"], {})
        for field in cls_cfg.get("pii_fields", []):
            value = rec.get("fields", {}).get(field)
            if isinstance(value, str) and value in known_raw_values:
                leaks.append(f"{rec['id']}:{field}")
    return leaks
