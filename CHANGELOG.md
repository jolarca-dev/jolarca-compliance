# Changelog

All notable changes to this compliance repository are documented here.
Format: [Conventional Commits](https://www.conventionalcommits.org). Every
policy change, register mutation, and evidence finalization must appear here.

## [Unreleased]

### Added

- audits: detailed internal audit program plan (`audits/audit-plan-2026.md`).
- audits: internal self-audit report 2026-08-15 (findings F-01–F-06,
  all fixed and verified).

### Fixed

- fix: `make check` enforces policy & vendor review-currency gates hard
  (removed silent `|| true` bypass; finding F-01).
- fix: vendor register/folder parity is now actually enforced by
  `scripts/vendor-review-dates.py` (finding F-04).
- fix: `qodana.yaml` rewritten to a valid Qodana schema (finding F-02).
- chore: removed dead code in `scripts/dsr-sla-report.py` (finding F-03).

## [0.1.0] - 2026-08-15

### Added

- chore: repository skeleton per compliance architecture review
  (GDPR core artifacts, ISMS policies, vendor governance, incident & DSR
  management, audit evidence gates G0–G4, certification tracks).
- policy: initial draft set 01–12 mapped to ISO 27001 Annex A.
- register: RoPA `master-register.csv`, vendor `register.csv`,
  evidence `audits/evidence-registry.csv` (empty, schema locked).
- ci: integrity workflows — DSR SLA monitor, policy review reminders,
  evidence hash verification, vendor review tracker, access review scheduler.
- docs: compliance matrix, retention schedule, regulatory contacts, ADR-0001.
