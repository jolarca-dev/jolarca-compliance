"""Adversarial anonymization verification — proof, not assertion.

After a retention run, an attacker model attempts re-identification on the
anonymized records:

  Attack 1  direct match     — raw candidate value found verbatim in a PII field
  Attack 2  linkage scan     — raw candidate found anywhere in any string field
  Attack 3  keyed re-hash    — ONLY possible with the anonymization key
                               (sanity mode: with the key the attack MUST
                               succeed; without it MUST fail — proving the
                               anonymization's irreversibility rests on key
                               destruction, which is the ADR-0001 doctrine)

CLI: verify-anonymization --dataset store.json --candidates cands.txt
     [--key-file key]   → PASS requires zero keyless leaks.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from retention.anonymize import KeyedAnonymizer  # noqa: E402
from retention import matrix as mx                # noqa: E402


def attempt_reidentification(records: list[dict], candidates: set[str],
                             matrix: dict, anonymizer: KeyedAnonymizer | None):
    """Returns (keyless_leaks, keyed_matches)."""
    keyless_leaks: list[str] = []
    keyed_matches: list[str] = []
    for rec in records:
        cls_cfg = matrix["classes"].get(rec["class"], {})
        pii_fields = cls_cfg.get("pii_fields", [])
        fields = rec.get("fields", {})
        # Attack 1: direct match on PII fields
        for f in pii_fields:
            v = fields.get(f)
            if isinstance(v, str) and v in candidates:
                keyless_leaks.append(f"direct:{rec['id']}:{f}")
        # Attack 2: linkage/substring scan across ALL string fields
        for f, v in fields.items():
            if isinstance(v, str):
                for cand in candidates:
                    if cand and cand in v and f not in pii_fields:
                        keyless_leaks.append(f"linkage:{rec['id']}:{f}")
        # Attack 3: keyed re-hash (requires key custody breach)
        if anonymizer is not None:
            for f in pii_fields:
                v = fields.get(f)
                for cand in candidates:
                    if isinstance(v, str) and v == anonymizer.digest(f, cand):
                        keyed_matches.append(f"keyed:{rec['id']}:{f}")
    return keyless_leaks, keyed_matches


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dataset", required=True, help="JSON record store")
    ap.add_argument("--candidates", required=True,
                    help="newline file of attacker-known raw identifiers")
    ap.add_argument("--key-file", default=None,
                    help="sanity mode: proves attack succeeds WITH the key")
    args = ap.parse_args()

    dataset = json.loads(Path(args.dataset).read_text(encoding="utf-8"))
    candidates = {ln.strip() for ln in
                  Path(args.candidates).read_text(encoding="utf-8").splitlines()
                  if ln.strip()}
    matrix = mx.load_matrix()
    anonymizer = (KeyedAnonymizer.from_key_file(args.key_file)
                  if args.key_file else None)

    leaks, keyed = attempt_reidentification(dataset["records"], candidates,
                                            matrix, anonymizer)
    if args.key_file:
        print(f"sanity (with key): keyed re-id matches = {len(keyed)}")
        print("SANITY PASS — attack succeeds only with key custody"
              if keyed else "SANITY FAIL — keyed attack found nothing "
                            "(test harness broken)")
        return 0 if keyed else 1

    for leak in leaks:
        print(f"LEAK {leak}")
    if leaks:
        print(f"ADVERSARIAL FAIL — {len(leaks)} re-identification path(s)")
        return 1
    print(f"ADVERSARIAL PASS — 0 re-identification paths across "
          f"{len(dataset['records'])} records, {len(candidates)} candidates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
