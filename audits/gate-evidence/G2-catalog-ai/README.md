# G2 — Catalog & AI (gate evidence)

Immutable once the gate passes. Required artifacts:

- [ ] AI egress test results (PII pre-filter effectiveness; allowlist proof)
- [ ] MinIO/object-storage residency verification (EU regions)
- [ ] DPIA 002 signed + hash; TIAs for active LLM vendors
- [ ] No-training opt-out evidence per vendor (contract clause + API flag)
- [ ] Location-data handling test results (PostGIS, ROPA-006)

After pass: `make hash-evidence`, then archive the GO decision record.
