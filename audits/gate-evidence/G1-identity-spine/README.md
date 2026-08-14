# G1 — Identity spine (gate evidence)

Immutable once the gate passes. Required artifacts:

- [ ] pgcrypto field-encryption test evidence (queries + output)
- [ ] Erasure E2E run logs (all systems incl. processors)
- [ ] DPIA 001 v2 signature + hash
- [ ] Consent engine ledger linkage proof (`ConsentRecord` ↔ `consent-versions.md`)
- [ ] Access control baseline export (roles, MFA enforcement)

After pass: `make hash-evidence`, then archive the GO decision record.
