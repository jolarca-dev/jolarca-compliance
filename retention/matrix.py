"""Matrix loader + effective-mode resolution.

The declared `mode` in matrix.yaml is NEVER trusted: effective mode is
re-derived here so destructive action on unconfirmed classes is impossible
by construction.
"""
from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

REPO = Path(__file__).resolve().parent.parent
MATRIX_PATH = REPO / "retention" / "matrix.yaml"

CONFIRMED_STATUSES = {"confirmed", "confirmed-limitation", "confirmed-operational"}


class MatrixError(ValueError):
    pass


def load_matrix(path: Path = MATRIX_PATH) -> dict:
    if yaml is None:
        raise MatrixError("PyYAML required: python -m pip install pyyaml")
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict) or "classes" not in data:
        raise MatrixError(f"invalid matrix at {path}: missing 'classes'")
    return data


def country_entry(cls_cfg: dict, country: str) -> dict:
    countries = cls_cfg["countries"]
    return countries.get(country, countries.get("ALL"))


def effective_mode(cls_cfg: dict, country: str) -> tuple[str, str]:
    """Return (mode, reason). Report-only wins whenever the law is unconfirmed.

    Order of checks matters and is deliberate: hold → counsel → period.
    """
    entry = country_entry(cls_cfg, country)
    if entry is None:
        return "report-only", f"no matrix entry for country={country}"
    if entry.get("step27_hold"):
        return "report-only", "step27_hold: class held until counsel releases it"
    if entry.get("counsel_status") not in CONFIRMED_STATUSES:
        return ("report-only",
                f"counsel_status={entry.get('counsel_status')!r} — unconfirmed "
                f"retention is never destructive")
    if entry.get("period_years") is None and entry.get("period_days") is None:
        return "report-only", "no retention period defined"
    declared = entry.get("mode", "active")
    return declared, f"counsel confirmed ({entry.get('counsel_status')})"


def horizon_days(cls_cfg: dict, country: str) -> int | None:
    entry = country_entry(cls_cfg, country)
    if entry is None:
        return None
    if entry.get("period_days") is not None:
        return int(entry["period_days"])
    if entry.get("period_years") is not None:
        return int(entry["period_years"]) * 365
    return None


def classes_for_domain(matrix: dict, domain: str) -> list[str]:
    return [name for name, cfg in matrix["classes"].items()
            if domain in cfg.get("domain", [])]
