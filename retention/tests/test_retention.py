"""Retention engine test suite — acceptance proofs for STEP 30.

Run:  .venv/bin/python -m unittest retention.tests.test_retention -v
Every test re-executes the engine on copies of the fixtures; nothing here
is assertion-only — the hold-guard, report-only, adversarial and
propagation properties are demonstrated, not claimed.
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from retention import matrix as mx                    # noqa: E402
from retention.anonymize import KeyedAnonymizer        # noqa: E402
from retention.audit import AuditTrail                 # noqa: E402
from retention.hold_guard import JsonHoldGuard         # noqa: E402
from retention.retention_job import JsonRecordStore, run  # noqa: E402
from retention.scheduler import RunState, alerts       # noqa: E402
from retention.verify_anonymization import attempt_reidentification  # noqa: E402
from retention import warehouse                        # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
TODAY = date(2026, 8, 17)


class RetentionTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="retention-test-"))
        self.prod = self.tmp / "prod.json"
        self.wh = self.tmp / "warehouse.json"
        self.holds = self.tmp / "holds.json"
        shutil.copy(FIXTURES / "records_prod.json", self.prod)
        shutil.copy(FIXTURES / "records_warehouse.json", self.wh)
        shutil.copy(FIXTURES / "holds.json", self.holds)
        self.trail = AuditTrail(self.tmp / "audit.ndjson")
        self.matrix = mx.load_matrix()
        self.anonymizer = KeyedAnonymizer()
        self.run_id = "test-run"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def original(self, store_path, record_id):
        data = json.loads(Path(FIXTURES / store_path).read_text(encoding="utf-8"))
        return next(r for r in data["records"] if r["id"] == record_id)

    def run_prod(self):
        store = JsonRecordStore(self.prod)
        guard = JsonHoldGuard(self.holds)
        counts = run("prod", store, guard, self.trail, self.anonymizer,
                     self.run_id, TODAY, self.matrix)
        return store, counts


class TestMatrixModes(RetentionTestBase):
    def test_lt_accounting_active(self):
        mode, _ = mx.effective_mode(self.matrix["classes"]["RC-ACCT-10Y"], "LT")
        self.assertEqual(mode, "active")

    def test_lv_ee_report_only(self):
        for country in ("LV", "EE"):
            mode, reason = mx.effective_mode(
                self.matrix["classes"]["RC-ACCT-10Y"], country)
            self.assertEqual(mode, "report-only", country)
            self.assertIn("counsel", reason)

    def test_payroll50_step27_hold_forces_report_only(self):
        mode, reason = mx.effective_mode(
            self.matrix["classes"]["RC-PAYROLL-50Y"], "LT")
        self.assertEqual(mode, "report-only")
        self.assertIn("step27_hold", reason)

    def test_declared_mode_never_trusted(self):
        """Even if someone flips mode: active in YAML, unconfirmed counsel
        must still force report-only."""
        cfg = json.loads(json.dumps(self.matrix["classes"]["RC-ACCT-10Y"]))
        cfg["countries"]["LV"]["mode"] = "active"
        mode, _ = mx.effective_mode(cfg, "LV")
        self.assertEqual(mode, "report-only")


class TestHoldGuard(RetentionTestBase):
    def test_held_record_past_horizon_is_preserved(self):
        store, counts = self.run_prod()
        held = store.get("INV-2014-LT-HELD")          # 12y old, 10y horizon
        self.assertIsNotNone(held, "held record must still exist")
        self.assertEqual(held["fields"],
                         self.original("records_prod.json",
                                       "INV-2014-LT-HELD")["fields"],
                         "held record fields must be byte-identical")
        self.assertEqual(counts.get("HELD"), 2)

    def test_hold_precedes_class_hold(self):
        """PAY-1990-LT-HELD is both step27-held as a class AND individually
        held — the guard decision wins and is logged as HELD."""
        _, counts = self.run_prod()
        held_rows = [r for r in self.trail.rows()
                     if r["record_id"] == "PAY-1990-LT-HELD"]
        self.assertEqual(held_rows[0]["decision"], "HELD")


class TestReportOnly(RetentionTestBase):
    def test_counsel_pending_records_never_mutated(self):
        store, counts = self.run_prod()
        for rid in ("INV-2015-LV", "PAY-1974-LT", "MC-2020-LT", "ACC-2020-LV"):
            fixture = "records_prod.json"
            self.assertEqual(store.get(rid)["fields"],
                             self.original(fixture, rid)["fields"],
                             f"{rid} must be untouched (report-only)")
        self.assertEqual(counts.get("REPORT_ONLY"), 4)

    def test_report_only_logs_what_would_happen(self):
        self.run_prod()
        row = next(r for r in self.trail.rows()
                   if r["record_id"] == "PAY-1974-LT")
        self.assertEqual(row["decision"], "REPORT_ONLY")
        self.assertIn("would=", row["reason"])


class TestActiveActions(RetentionTestBase):
    def test_anonymize_keeps_fiscal_substance(self):
        store, _ = self.run_prod()
        rec = store.get("INV-2015-LT")
        self.assertTrue(rec["fields"]["customer_name"].startswith("anon$"))
        self.assertTrue(rec["fields"]["iban"].startswith("anon$"))
        self.assertEqual(rec["fields"]["amount"], "120.00")
        self.assertEqual(rec["fields"]["document_no"], "FA-2015-0042")

    def test_hard_delete_and_archive_and_never(self):
        store, counts = self.run_prod()
        for rid in ("ACC-2020-LT", "AI-OLD", "LOC-OLD", "SUP-2020"):
            self.assertIsNone(store.get(rid), f"{rid} should be deleted")
        archived = store.get("LOG-2019")
        self.assertEqual(archived["fields"]["actor_id"], "__ERASED__")
        self.assertIsNotNone(store.get("EVI-001"), "evidence is never-delete")
        self.assertIsNotNone(store.get("ACC-RECENT-LT"), "under horizon")
        self.assertEqual(counts.get("DELETED"), 4)
        self.assertEqual(counts.get("ARCHIVED_THEN_DELETED"), 1)
        self.assertEqual(counts.get("RETAINED_NEVER"), 1)
        self.assertEqual(counts.get("RETAINED_YOUNG"), 1)


class TestAdversarialAnonymization(RetentionTestBase):
    def test_reidentification_fails_without_key(self):
        store, _ = self.run_prod()
        candidates = {"Aiste Sintetine", "aiste@example.test", "SYN-1234560",
                      "LT00SYNTHETIC0001", "Iras Sintetinis", "SYN-3333330",
                      "SYNDOC-77", "LT00SYNTHETIC0006"}
        cohort = [r for r in store.records
                  if r["id"] in ("INV-2015-LT", "KYC-2018-LT")]
        leaks, _ = attempt_reidentification(cohort, candidates,
                                            self.matrix, None)
        self.assertEqual(leaks, [], "keyless re-identification must fail")

    def test_reidentification_succeeds_with_key(self):
        """Sanity: the anonymization is a keyed transform — with key custody
        the attack works, so irreversibility genuinely rests on the key."""
        store, _ = self.run_prod()
        candidates = {"Aiste Sintetine", "SYN-1234560"}
        cohort = [r for r in store.records if r["id"] == "INV-2015-LT"]
        _, keyed = attempt_reidentification(cohort, candidates,
                                            self.matrix, self.anonymizer)
        self.assertGreater(len(keyed), 0)


class TestWarehousePropagation(RetentionTestBase):
    def test_manifest_propagates_and_leak_scan_clean(self):
        wh_store = JsonRecordStore(self.wh)
        known_raw = {"Aiste Sintetine", "aiste@example.test",
                     "Frida Sintetine", "frida@example.test"}
        pre = warehouse.scan_for_raw_pii(wh_store, known_raw, self.matrix)
        self.assertGreater(len(pre), 0, "pre-propagation scan must find raw PII")

        manifest = [
            {"record_id": "INV-2015-LT", "class": "RC-ACCT-10Y",
             "action": "anonymize"},
            {"record_id": "ACC-2020-LT", "class": "RC-ACCOUNT",
             "action": "delete"},
            {"record_id": "GHOST-999", "class": "RC-ACCT-10Y",
             "action": "delete"},
        ]
        counts = warehouse.propagate_manifest(manifest, wh_store,
                                              self.anonymizer, self.trail,
                                              self.run_id, self.matrix, TODAY)
        self.assertEqual(counts["PROPAGATED_ANONYMIZED"], 1)
        self.assertEqual(counts["PROPAGATED_DELETED"], 1)
        self.assertEqual(counts["PROPAGATION_MISS"], 1)
        post = warehouse.scan_for_raw_pii(wh_store, known_raw, self.matrix)
        self.assertEqual(post, [], "post-propagation leak scan must be clean")


class TestSchedulerAndAudit(RetentionTestBase):
    def test_missed_run_alerts(self):
        state = RunState(self.tmp / "state.json")
        state.record_run("RC-ACCT-10Y", "prod", date(2026, 6, 1))
        overdue = alerts(state, [("RC-ACCT-10Y", "prod")], TODAY)
        self.assertEqual(len(overdue), 1)
        self.assertIn("missed its schedule", overdue[0])
        state.record_run("RC-ACCT-10Y", "prod", TODAY)
        self.assertEqual(alerts(state, [("RC-ACCT-10Y", "prod")], TODAY), [])
        fresh = RunState(self.tmp / "state2.json")
        self.assertIn("NEVER run",
                      alerts(fresh, [("RC-AI", "prod")], TODAY)[0])

    def test_audit_trail_matches_decisions(self):
        _, counts = self.run_prod()
        trail_counts = self.trail.summary(self.run_id)
        self.assertEqual(trail_counts, counts)
        for row in self.trail.rows():
            self.assertTrue(row["reason"], "every decision needs a reason")
            self.assertEqual(row["run_id"], self.run_id)


if __name__ == "__main__":
    unittest.main(verbosity=2)
