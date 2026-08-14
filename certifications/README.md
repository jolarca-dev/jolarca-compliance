# Certifications — Strategy & Sequencing

Sequencing rationale: evidence is shared across frameworks; build once,
map many times (`docs/compliance-matrix.md` is the single mapping).

| Track | When | Why this order |
|---|---|---|
| PCI DSS SAQ-A | Pre-launch | Small scope, gates payments launch (G3) |
| SOC 2 Type 1 | Post-launch + ~6 months | Point-in-time; validates control design |
| ISO 27001 | After SOC 2 Type 1 | Annex A mapping reuses SOC 2 evidence; SoA ready |
| SOC 2 Type 2 | After ISO gap closure | Observation period evidence already collected |

Each track folder holds: readiness/gap assessments, scope statements,
control narratives, auditor correspondence. Auditor correspondence is
confidential and hashed on finalization.
