"""Keyed anonymization (ADR-0001 mechanism).

PII fields become salted, keyed SHA-256 digests: deterministic for a given
key (joins still work inside the retention window's analytics), but
irreversible once the key is destroyed — the adversarial verifier proves
that property. Fiscal/retained fields are never touched.
"""
from __future__ import annotations

import hashlib
import os
import secrets

TOMBSTONE = "__ERASED__"


class KeyedAnonymizer:
    def __init__(self, key: bytes | None = None):
        self.key = key if key is not None else secrets.token_bytes(32)

    @classmethod
    def from_key_file(cls, path) -> "KeyedAnonymizer":
        p = __import__("pathlib").Path(path)
        if p.is_file():
            return cls(bytes.fromhex(p.read_text(encoding="utf-8").strip()))
        return cls()

    def save_key(self, path) -> None:
        """Key custody: the key lives OUTSIDE the dataset (Vault in prod)."""
        p = __import__("pathlib").Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.key.hex(), encoding="utf-8")
        os.chmod(p, 0o600)

    def digest(self, field: str, value: str) -> str:
        material = self.key + field.encode() + b"\x1f" + value.encode()
        return "anon$" + hashlib.sha256(material).hexdigest()[:32]

    def anonymize_record(self, record: dict, pii_fields: list[str]) -> dict:
        """Return a NEW record: PII → keyed digests, everything else intact."""
        out = dict(record)
        for field in pii_fields:
            if field in out and out[field] not in (None, "", TOMBSTONE):
                out[field] = self.digest(field, str(out[field]))
        return out
