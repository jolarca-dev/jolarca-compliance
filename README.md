# jol-m-compliance

**PRIVATE repository.** Single source of truth for GDPR / ISO 27001 / SOC 2 compliance
governance of the Journey Of Life marketplace platform (LT / LV / EE markets).

> Hard rule: this repository stores **governance artifacts only** — policies, registers,
> anonymized indexes, hashes, and evidence references. It must **never** contain raw
> personal data. DSR content, incident subject details, and identity documents remain in
> product systems or the encrypted evidence vault; here we keep pointers and hashes.

## Access

| Role | Access | Notes |
|---|---|---|
| DPO | Admin | Required reviewer on `policies/`, `dpia/`, `ropa/` |
| Compliance lead | Admin | Required reviewer on all registers |
| Engineering leads | Write | Via PR only; branch protection enforced |
| Everyone else | None | Requests via issue, SLA: 2 business days |

## Structure

| Path | Content |
|---|---|
| `dpia/` | Data Protection Impact Assessments (Art. 35) + register |
| `ropa/` | Record of Processing Activities (Art. 30) + machine-readable register |
| `lawful-basis/` | Versioned consent texts (lt/lv/et/en/ru), LIA registry |
| `policies/` | ISMS policy set (ISO 27001 Annex A mapped) + exceptions |
| `vendor-assessments/` | Processor register, DPAs, Transfer Impact Assessments |
| `incidents/` | Incident register, breach-notification templates, game days |
| `data-subject-requests/` | Anonymized DSR register, response templates, SLA reports |
| `management-review/` | ISO 9.3 minutes, DPO quarterly reports |
| `audits/` | Immutable gate evidence (G0–G4), hash registry, per-framework mapping |
| `certifications/` | SOC 2 Type 1, ISO 27001, PCI DSS SAQ-A tracks |
| `legal/` | Versioned legal texts per language, imprint |
| `risk-register/` | Risk register + treatment plans |
| `retention/` | Retention-as-code: matrix config, jobs, hold guard, adversarial proofs (STEP 30) |
| `training/` | Program materials + completion log |
| `docs/` | Compliance matrix, retention schedule, regulatory contacts, ADRs |
| `scripts/` | Integrity + SLA automation (see Makefile) |

## Evidence rules (non-negotiable)

1. Finalized evidence is **immutable**: never edit, only supersede with a new version.
2. Every finalized artifact is hashed into `audits/evidence-registry.csv`
   (`make hash-evidence`) and verified weekly by `evidence-integrity.yml`.
3. Signed PDF originals live in the encrypted evidence vault (Git LFS pointers here);
   git stores hashes, not bulk binaries.
4. All policy changes go through PR with DPO + compliance lead sign-off and a
   Conventional Commit entry in `CHANGELOG.md`.

## Key SLAs

| Obligation | Deadline | Monitor |
|---|---|---|
| Breach notification to SA (Art. 33) | 72 h | `policies/06-incident-response.md` |
| DSR response (Art. 12) | 30 days; DPO paged at day 21 | `dsr-sla-monitor.yml` |
| Policy annual review | review date + 14 days | `policy-review-reminder.yml` |
| Vendor re-assessment | annual | `vendor-review-due.yml` |
| i.SAF FR0600 filing (LT) | monthly, by the 20th (nil report included) | `docs/regulatory-obligations.md` OBL-001 |
| Access review | quarterly | `access-review-due.yml` |
| Critical CVE fix | ≤ 7 days | `policies/08-secure-development.md` |

## Contacts

- **DPO**: dpo@journeyoflife.example (see `docs/regulatory-contacts.md`)
- Security incidents: see `SECURITY.md` — compliance-repo incidents are highest severity.

## Setup (scripts)

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python main.py            # smoke-check of repository tooling
make check                # full static verification
```
