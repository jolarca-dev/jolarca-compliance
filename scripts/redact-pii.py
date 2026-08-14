#!/usr/bin/env python3
"""PII redaction backstop: flag unredacted personal-data patterns in drafts.

A pre-commit/CI backstop — not a license to be careless. Governance artifacts
must never contain raw personal data (README hard rule).

Usage:
    redact-pii.py FILE...   # scan specific files (pre-commit passes these)
    redact-pii.py --all     # scan the compliance-sensitive directories

Exit 1 on any hit. Addresses under *.example domains are internal placeholders
and are allowed. Stdlib only.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCAN_DIRS = ["incidents", "data-subject-requests", "audits", "dpia",
             "vendor-assessments", "management-review"]
SCAN_SUFFIXES = {".md", ".csv", ".txt", ".yml", ".yaml"}

PATTERNS = {
    # email addresses, except internal *.example placeholders
    "email": re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}\b"),
    # IBAN (country check digits + 11–30 alnum)
    "iban": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b"),
    # LT/EE 11-digit personal identification codes
    "personal-code-11": re.compile(r"(?<![\d-])\d{11}(?![\d-])"),
    # LV personal code dddddd-ddddd
    "personal-code-lv": re.compile(r"(?<!\d)\d{6}-\d{5}(?!\d)"),
    # card-like PAN (13–19 digits, optionally spaced)
    "pan": re.compile(r"(?<![\d-])(?:\d[ -]?){12,18}\d(?![\d-])"),
}


def mask(match: str) -> str:
    return match[:2] + "…" + match[-2:] if len(match) > 6 else "***"


def scan_file(path: Path) -> list[str]:
    hits: list[str] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return hits
    for lineno, line in enumerate(text.splitlines(), start=1):
        for name, pattern in PATTERNS.items():
            for m in pattern.finditer(line):
                value = m.group(0)
                if name == "email" and value.lower().endswith(".example"):
                    continue
                rel = path.relative_to(REPO) if path.is_absolute() else path
                hits.append(f"{rel}:{lineno}: {name} {mask(value)}")
    return hits


def collect(files: list[str]) -> list[Path]:
    if files:
        return [Path(f) for f in files]
    found: list[Path] = []
    for d in SCAN_DIRS:
        base = REPO / d
        if base.is_dir():
            found.extend(p for p in sorted(base.rglob("*"))
                         if p.is_file() and p.suffix in SCAN_SUFFIXES)
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="*", help="files to scan (else --all)")
    ap.add_argument("--all", action="store_true",
                    help="scan the compliance-sensitive directories")
    args = ap.parse_args()
    if not args.all and not args.files:
        ap.error("pass files or --all")

    hits: list[str] = []
    for path in collect(args.files):
        hits.extend(scan_file(path))
    for hit in hits:
        print(f"PII {hit}")
    if hits:
        print(f"redact-pii: {len(hits)} potential PII hit(s) — redact before commit")
        return 1
    print("redact-pii: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
