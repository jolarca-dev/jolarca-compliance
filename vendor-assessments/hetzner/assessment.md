# Vendor Assessment — Hetzner Online GmbH

**Assessment date:** 2026-09-02
**Assessor:** Compliance Team
**Review date:** 2027-09-02

## Vendor Details

| Field | Value |
|-------|-------|
| Legal name | Hetzner Online GmbH |
| Location | Falkenstein, DE |
| Website | https://hetzner.com |
| Service used | hetzner marketplace integration |

## Data Processing

| Field | Value |
|-------|-------|
| Data categories | Encrypted BorgBackup archives (repokey-blake2) |
| Purpose | Marketplace operations |
| Retention | Per vendor DPA |
| Sub-processors | See vendor documentation |

## Legal Framework

| Document | Status | Location |
|----------|--------|----------|
| DPA | Signed (processor) | contracts/vendors/ |
| SCCs | N/A (EU-EU) | contracts/vendors/ |
| TIA | N/A | vendor-assessments/tia/ |

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Data breach by vendor | Low | High | DPA with breach notification; annual review |
| Sub-processor change | Medium | Medium | Contract requires notice; right to object |
| Service discontinuation | Low | Medium | Alternative vendor identified |

## Residual Risk

**Acceptable:** YES — DPA in place; EU-based (except ISRG which processes domain names only).

## Approval

- **Assessor:** Compliance Team — 2026-09-02
- **DPO:** [PENDING]
- **Next review:** 2027-09-02
