# RoPA — consent-registry (ROPA-007)

| Field | Value |
|---|---|
| Purpose | Consent grant & withdrawal ledger — records and manages per-user, per-purpose consent lifecycle |
| Lawful basis | Art. 6(1)(c) legal obligation — Art. 7(1) GDPR requires the controller to be able to demonstrate that consent was given |
| Data categories | User ID, consent version ID, timestamp, purpose tag, grant/withdrawal status |
| Subjects | Users, sellers |
| Retention | RC-CONSENT — see `docs/retention-schedule.md` |
| Recipients | None (internal system only; no external recipients) |
| Transfers | EU-only processing |
| Controls | Append-only ledger; immutable consent text versions; pgcrypto field-level encryption; audit logging; no consent data exposed to processors |

## Relationship to other RoPA entries

The consent registry is a **cross-cutting** processing activity that underpins
the lawful basis of consent-dependent entries:

- **ROPA-005** (ai-service): consent for optional AI features (`CT-ai-v*`)
- **ROPA-006** (geolocation-search): consent for location processing (`CT-location-v*`)
- Marketing communications: consent tracked in registry (`CT-marketing-v*`)
  — not a separate RoPA entry (marketing is not a distinct processing system
  in the platform; it is an output channel driven by the consent flag)

The registry itself does **not** process the content of consent texts — those
are versioned under `lawful-basis/consent-text/`. The registry stores only
the linkage: which user was shown which version, when, and whether consent
is active or withdrawn.

## Consent version ledger

Consent text versions are tracked in `lawful-basis/consent-versions.md`.
Each version ID maps 1:1 to `ConsentRecord.consent_version` values in the
product database. The ledger is append-only; superseded versions retain
their "Shown until" date permanently.

## Withdrawal

Withdrawal must be as easy as grant (Art. 7(3)). Withdrawal paths are
documented in each consent text (`lawful-basis/consent-text/<lang>/`).
On withdrawal:

1. Consent status set to `withdrawn` with timestamp.
2. Downstream processing for that purpose must cease (ROPA-005/006).
3. The withdrawal record itself is retained (proof of compliance with
   Art. 7(3); the registry must demonstrate that withdrawal was honored).

## Why a separate RoPA entry

The consent registry was previously implicit — referenced as a lawful basis
component of ROPA-005 and ROPA-006 but not registered as a distinct
processing activity. It processes personal data (user identifiers,
timestamps, consent metadata) for its own purpose (demonstrability of
consent under Art. 7(1)), has its own retention requirements, and is
subject to its own DSAR obligations. Registering it separately ensures:

- Completeness of the Art. 30 record.
- Clear retention class assignment (RC-CONSENT).
- Explicit DSAR scope in the cross-service runbook
  (`data-subject-requests/cross-service-dsar-runbook.md`).
- Auditor traceability from consent text → version ledger → registry entry
  → downstream processing.

Last reviewed: 2026-09-28 (initial registration).
