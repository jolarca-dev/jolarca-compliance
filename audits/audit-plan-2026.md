# Internal Audit Program Plan — 2026

| | |
|---|---|
| Version | 1.0 |
| Owner | Compliance lead |
| Approved by | DPO + Management |
| Effective date | 2026-08-15 |
| Next review | 2027-08-15 |
| Retention class | RC-EVIDENCE (never delete; supersede only) |
| Frameworks | GDPR, ISO/IEC 27001:2022, SOC 2 TSC, PCI DSS 4.0 (SAQ-A) |

## 1. Purpose & objectives

Provide a risk-based, independent, evidence-grade audit program that:

1. Proves control operating effectiveness to regulators (VDAI/DVI/AKI) and
   external auditors — evidence answerable in hours, not weeks.
2. Detects control drift before it becomes a breach (72h-clock event).
3. Gates the roadmap (G0–G4) with immutable, hash-verified evidence.
4. Feeds management review (ISO cl. 9.3) with quantitative findings.

## 2. Scope

**In scope:** all Journey Of Life marketplace systems (users-app, sellers-app,
orders-payments, ai-service, shipping integrations, CRM), infrastructure
(GCP, Vault, CI/CD), this compliance repository, and all processors per
`vendor-assessments/register.csv`. Jurisdictions: LT, LV, EE.

**Out of scope:** none by default. Any exclusion requires a written, DPO-signed
scope statement (ISO 4.3) — silence is not exclusion.

## 3. Audit criteria

| Framework | Primary artifacts |
|---|---|
| GDPR | `ropa/`, `dpia/`, `lawful-basis/`, `data-subject-requests/`, `incidents/` |
| ISO 27001:2022 | `policies/` (Annex A mapped), `audits/iso27001/` (SoA) |
| SOC 2 | `audits/soc2/` (CC1–CC9), `docs/compliance-matrix.md` |
| PCI DSS 4.0 | `certifications/pci-dss/` (SAQ-A scope defense) |
| Internal | Policies 01–12, retention schedule, SLA table in root README |

## 4. Audit types

### 4.1 Continuous automated assurance (always on)

| Control | Mechanism | Frequency |
|---|---|---|
| Evidence integrity | `evidence-integrity.yml` vs `evidence-registry.csv` | weekly |
| DSR 30-day clock | `dsr-sla-monitor.yml` (day-21 paging) | daily |
| Policy review currency | `policy-review-reminder.yml` + CI gate | monthly / per PR |
| Vendor re-assessment currency | `vendor-review-due.yml` + register/folder parity | weekly / per PR |
| PII in governance artifacts | `redact-pii.py` pre-commit + CI | per commit |
| Secrets / key material | gitleaks + detect-private-key | per commit |

### 4.2 Gate audits (G0–G4)

Per-gate checklist lives in `audits/gate-evidence/GN-*/README.md`. Gate audit
procedure: (a) verify every checklist item has an artifact; (b) hash all
artifacts (`make hash-evidence`); (c) independent reviewer (not the control
owner) signs the gate record; (d) GO decision recorded in minutes.
**A gate cannot pass on promise of evidence — only on finalized, hashed evidence.**

### 4.3 Quarterly internal audits

| Quarter | Theme | Population & sampling |
|---|---|---|
| 2026-Q3 | Access control (policy 03): JML, MFA, service accounts | 100% of leavers since last review; sample ≥ 25 or 10% of access grants |
| 2026-Q4 | DSR & retention (policies 02/05) | 100% of DSRs; sample of retention job runs; erasure re-test |
| 2027-Q1 | Vendor & transfers (policy 07) | 100% of processors; 100% of TIAs; sub-processor change log |
| 2027-Q2 | Logging, DR, incident readiness (06/09/11) | restore drill observation; game-day; log integrity spot-check |

### 4.4 External audits & attestations

| Engagement | Window | Preconditions |
|---|---|---|
| PCI DSS SAQ-A self-assessment | pre-G3 | SAQ-A scope proof finalized at G3 |
| External penetration test | pre-G4 | scope statement + RoE signed; criticals/highs closed before launch |
| SOC 2 Type 1 | launch + ~6 months | G4 passed; control narratives drafted |
| ISO 27001 certification | after SOC 2 Type 1 | SoA finalized; internal audit cycle ≥ 1 complete |

## 5. Roles & independence

- **Internal auditor**: compliance lead or appointed auditor; must not audit
  controls they own (e.g., policy owner ≠ auditor for that domain).
- **DPO**: independent oversight; receives all findings; may escalate directly
  to management and supervisory authorities.
- **Control owners**: provide evidence, remediate findings; never close their
  own findings.
- **External auditors**: selected by management with DPO input; engagement
  letters archived in `certifications/<track>/`.

## 6. Fieldwork procedure (all audits)

1. **Planning**: scope memo, criteria, sampling plan, requested evidence list.
2. **Evidence collection**: only from authoritative sources (registers,
   exports, signed artifacts); every artifact captured with SHA-256 into
   `audits/evidence-registry.csv` at collection time.
3. **Testing**: re-performance preferred over inquiry; inquiry alone is an
   observation, never proof of operating effectiveness.
4. **Findings classification**:
   - **Major** — control absent/ineffective, or legal obligation at risk
     (e.g., DSR clock breach, unhashed finalized evidence, transfer without TIA)
   - **Minor** — isolated lapse or documentation gap with compensating control
   - **Observation** — improvement opportunity, no control failure
5. **Reporting**: report within 10 business days of fieldwork end; filed under
   `audits/internal-audits/` (or gate folder), hashed on finalization.

## 7. Remediation & verification SLAs

| Class | Corrective action plan | Verification |
|---|---|---|
| Major | ≤ 30 days; owner + due date in `risk-register/treatment-plans/` | re-test by auditor (effectiveness, not just completion) |
| Minor | ≤ 90 days | re-test or evidence review |
| Observation | next review cycle | tracked in management review |

Overdue majors are reported to management review and block the next gate.

## 8. Evidence integrity requirements (audit-wide)

- All finalized audit artifacts: hashed, registered, immutable.
- Weekly integrity verification is itself audit evidence (SOC 2 CC7).
- Auditor working papers with personal data: never in this repo (hard rule).
- Retention: RC-EVIDENCE — minimum 10 years; supersede, never delete.

## 9. Metrics reported to management review

- DSR on-time % (target 100%), policy/vendor review currency %,
  evidence integrity verification pass rate (target 100%),
  findings closure on-time %, exception count & expiry drift.

## 10. Plan governance

Amendments require compliance lead + DPO sign-off and a CHANGELOG entry.
Annual review of this plan occurs with the policy review cycle. Deviations
from the calendar require documented justification in management review minutes.
