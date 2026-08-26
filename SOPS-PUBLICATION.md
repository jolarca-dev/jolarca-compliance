# Marketplace SOPS Publication (Gate 7)

Marketplace-tree recipient publication per the jol-infrastructure ADR-003
amendment (journeyoflife-org/jol-infrastructure PR #35, CC8.1 issue #36).

- Recipient (PUBLIC, marketplace-only): age1h6knxanpsq332ufrh54mh5y0wgzhu43vgq8flh55hrnc2zvuwe8qjn4n47
- Creation rules: `*.enc.yaml|json`, `secrets/encrypted/**` only (R3).
- Segregation: this file MUST NOT list the church recipient age17ne7...
  and church repos MUST NOT list this recipient — cross-tree listing is a
  segregation incident (two PCI-DSS scopes, two DPIAs).
- Registry & rollout instructions (authoritative): jol-infrastructure
  `docs/security/sops-recipients-registry.md` + `sops-rollout-instructions.md`.
- Fleet enablement gated on Gate 8 round-trip (marketplace fixture).
