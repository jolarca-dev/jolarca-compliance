# Cross-Service DSAR Runbook — 30-Day Deadline

| | |
|---|---|
| Document type | Operational runbook (Art. 12–22 GDPR) |
| Scope | All personal-data systems under controller's responsibility |
| Owner | DPO |
| Effective date | 2026-09-28 |
| Next review | 2027-09-28 (annual) |
| Supersedes | — |

> **Hard rule:** This runbook contains **no personal data**. All case content,
> requester identity, and fulfillment payloads live in the DSR system — never
> in this repository. The register (`register.md`) stores anonymized indexes
> only.

---

## 1. Systems in scope

Every system that stores personal data must be queried, and where applicable,
acted upon, within the 30-day clock. The table below is derived from
`ropa/master-register.csv` and `ropa/by-system/`.

| # | System | ROPA ID | Data categories | Subjects | Retention class | Erasure design |
|---|---|---|---|---|---|---|
| S1 | **users-app** | ROPA-001 | Identity, contact, auth credentials, session metadata | Users (buyers) | RC-ACCOUNT | Hard delete after expiry |
| S2 | **sellers-app** | ROPA-002 | Identity documents, business registry data, VAT ID | Sellers | RC-KYC | Anonymize per ADR-0001 |
| S3 | **orders-payments** | ROPA-003 | Order data, payment references, delivery address | Buyers, sellers | RC-FINANCIAL | Anonymize; keep fiscal fields (ADR-0001) |
| S4 | **sellers-vies** | ROPA-004 | VAT ID, business name | Sellers | RC-FINANCIAL | Anonymize; keep fiscal fields (ADR-0001) |
| S5 | **ai-service** | ROPA-005 | Listing text, messages (PII pre-filtered) | Users, sellers | RC-AI | Hard delete (≤ 30d retention) |
| S6 | **geolocation-search** | ROPA-006 | Coarse location | Users | RC-LOCATION | Hard delete (≤ 90d retention) |
| S7 | **shipping** | ROPA-003 (part) | Delivery address, recipient name, phone | Buyers | RC-FINANCIAL-linked | Per carrier DPA; courier consignment data |
| S8 | **bitrix24-crm** | (support) | Support interactions, contact details | Users, sellers | RC-SUPPORT | Hard delete after 3y closure |
| S9 | **consent-registry** | ROPA-007 | User ID, consent version ID, timestamp, purpose tag, grant/withdrawal status | Users, sellers | RC-CONSENT | Hard delete after expiry; withdrawal proof retained |

### Processors to cascade (erasure / restriction / portability)

When a request requires action at a processor, notify via the DPA contact
channel within **5 business days** of request receipt (leaving ≥ 15 days for
processor response before the 30-day deadline).

| Processor | Systems | DPA status | Cascade channel |
|---|---|---|---|
| Identity provider | S1 | pending | Per DPA § notification clause |
| Bitrix24 | S1 (support), S8 | pending | Per DPA § notification clause |
| Verification provider | S2 | pending | Per DPA § notification clause |
| Stripe | S3 | pending (SCC) | Per DPA § notification clause |
| DPD | S3, S7 | pending | Per DPA § notification clause |
| Omniva | S3, S7 | pending | Per DPA § notification clause |
| DeepL | S5 | pending (SCC) | Per DPA § notification clause |
| OpenAI | S5 | pending (SCC) | Per DPA § notification clause |
| Anthropic | S5 | pending (SCC) | Per DPA § notification clause |
| Sentry/GlitchTip | all (scrubbed telemetry) | pending | Per DPA § notification clause |
| Google Cloud | all (infra) | pending | Per DPA § notification clause |

---

## 2. Request types and applicable articles

| Type | Article | What the data subject is entitled to |
|---|---|---|
| Access | Art. 15 | Copy of all personal data held + purposes, categories, recipients, retention periods, rights |
| Rectification | Art. 16 | Correction of inaccurate data; notification to recipients |
| Erasure ("right to be forgotten") | Art. 17 | Deletion / anonymization; cascaded to all recipients |
| Restriction | Art. 18 | Flag data — no processing except storage until restriction lifted |
| Portability | Art. 20 | Machine-readable export (structured, commonly used format) |
| Objection | Art. 21 | Stop processing based on legitimate interest (Art. 6(1)(f)) |
| Automated decision-making | Art. 22 | Not applicable currently (no profiling); document if N/A |

---

## 3. Day-by-day timeline

The 30-day clock starts at **receipt** (Art. 12(3)). Calendar days, not
business days. The DPO is paged at day 21 (`dsr-sla-monitor.yml`).

```text
Day 0        Receipt — log in DSR system, assign DSR-YYYY-NNN
Day 0–1      Identity verification initiated (request ID document)
Day 1–3      Identity verified; verification material deleted (RC-DSR-VERIFY)
Day 3        Scope assessment: which systems (S1–S9) hold data for this subject
Day 3–5      System queries dispatched to all in-scope systems
Day 5        Processor cascade notifications sent (erasure/restriction/portability)
Day 5–15     Data collected from systems; processor responses received
Day 15       Compilation: all data gathered, reviewed for completeness
Day 15–20    Response prepared (access letter / erasure confirmation / export)
Day 20–21    DPO review and sign-off on response
Day 21       ⚠️ DPO auto-paged if register not updated (dsr-sla-monitor.yml)
Day 21–25    Response sent to data subject
Day 25–28    Register updated; processor confirmations archived
Day 30       DEADLINE — case closed in register
```

### Extension (max +2 months)

Only if the request is **complex** or the subject has submitted **numerous**
requests (Art. 12(3)). Must:

1. Notify the data subject **within 30 days** of receipt, stating reasons for
   delay and the expected completion date.
2. Log the extension in the register with justification.
3. DPO approval required before extension is communicated.

---

## 4. Step-by-step procedure

### Step 1 — Intake (Day 0)

1. Receive request via any channel (email to `dpo@journeyoflife.example`,
   in-app form, support ticket, postal mail).
2. Create case in DSR system: assign `DSR-YYYY-NNN`.
3. Determine request type (access / rectification / erasure / restriction /
   portability / objection). If unclear, treat as **access** (broadest scope)
   and clarify with the subject.
4. Log in `data-subject-requests/register.md`:
   - Case ID, Type, Received date, Status = `open`.
5. Determine subject's market (LT / LV / EE) for language-specific response.

### Step 2 — Identity verification (Day 0–3)

1. Request identification proportional to the data held (Art. 12(6)).
   - Existing customers: match against account email + one secondary factor
     (e.g., last order reference, registered phone).
   - Former customers / unknown: request government-issued ID (copy redacted
     to minimum fields by the requester before submission).
2. Verify identity against S1 (users-app) or S2 (sellers-app) records.
3. **Delete verification material immediately after check** (RC-DSR-VERIFY).
4. If identity cannot be verified: send "unable to verify" letter; do not
   disclose any data. Clock pauses until identity confirmed.
5. Log: `Identity verified` column = date of verification.

### Step 3 — Scope assessment (Day 3)

Determine which systems hold personal data for this subject. Use the decision
matrix:

| Subject type | Likely systems | Always check |
|---|---|---|
| Buyer (active account) | S1, S3, S5, S6, S7, S8, S9 | S1 → S3 → S5 → S6 → S7 → S8 → S9 |
| Buyer (deleted account) | S3, S5 (expired), S6 (expired), S7, S9 | S3 → S7 → S9 |
| Seller (active) | S2, S3, S4, S5, S7, S8, S9 | S2 → S3 → S4 → S5 → S7 → S8 → S9 |
| Seller (offboarded) | S2, S3, S4, S9 | S2 → S3 → S4 → S9 |
| Both buyer and seller | All systems | S1–S9 full sweep |

**Never skip a system.** If a system returns "no data found," document the
negative result with the system owner's confirmation.

### Step 4 — System queries (Day 3–15)

For each in-scope system, execute the appropriate query:

#### S1 — users-app (ROPA-001)

- **Access:** Query user profile, auth metadata, session logs by user ID.
- **Rectification:** Update fields via admin API; log before/after.
- **Erasure:** Hard delete account + credentials (RC-ACCOUNT: account
  lifetime + 2y only if legal hold applies; otherwise immediate).
- **Portability:** Export profile JSON via admin API.
- **Restriction:** Set account to "restricted" flag — no processing except
  storage.

#### S2 — sellers-app (ROPA-002)

- **Access:** Query seller profile, KYC documents, business registry data.
- **Erasure:** Anonymize per ADR-0001 — remove identifiers, retain fiscal
  fields. KYC documents: anonymize after verification status is no longer
  needed (RC-KYC: 5y after offboarding).
- **Portability:** Export seller business data (excluding third-party data).

#### S3 — orders-payments (ROPA-003)

- **Access:** Query orders, invoices, payment references by subject ID.
- **Erasure:** **Anonymize-don't-delete** (ADR-0001, RC-FINANCIAL). Remove
  direct/indirect identifiers; retain fiscal fields (amounts, dates, VAT,
  counterparty VAT codes). Use cryptographic erasure (pgcrypto key deletion)
  where applicable. Document the anonymization act.
- **Portability:** Export order history in CSV/JSON.
- **Restriction:** Flag records — no processing except storage + legal
  obligations.

#### S4 — sellers-vies (ROPA-004)

- **Access:** Query VAT validation records.
- **Erasure:** VAT IDs on invoices are legally required (RC-FINANCIAL);
  anonymize per ADR-0001. VIES query logs: delete if no longer needed.

#### S5 — ai-service (ROPA-005)

- **Access:** Query stored prompts/outputs linked to subject (≤ 30d window).
- **Erasure:** Hard delete (RC-AI: ≤ 30d retention). If data already expired,
  confirm deletion. PII pre-filter logs: check for subject data.
- **Note:** AI processors (DeepL, OpenAI, Anthropic) confirm no training on
  user data per DPA — but cascade erasure request for completeness.

#### S6 — geolocation-search (ROPA-006)

- **Access:** Query location history (≤ 90d window).
- **Erasure:** Hard delete (RC-LOCATION: ≤ 90d retention). If expired, confirm.
- **Note:** Consent-based processing — objection (Art. 21) = withdraw consent
  - delete.

#### S7 — shipping (ROPA-003 part)

- **Access:** Query delivery records by recipient name/address/phone.
- **Erasure:** Request carriers (DPD, Omniva) to delete per DPA cascade.
  Retain consignment references in order records (RC-FINANCIAL, anonymized).
- **Restriction:** Notify carriers to flag data — no further processing.

#### S8 — bitrix24-crm (support)

- **Access:** Query support cases by contact details / pseudonymized case ID.
- **Erasure:** Delete support cases (RC-SUPPORT: 3y after closure). If within
  retention, anonymize case content.
- **Restriction:** Flag cases — no outbound contact.

#### S9 — consent-registry (ROPA-007)

- **Access:** Query ConsentRecord rows by user ID — all consent grants,
  withdrawals, version IDs, timestamps, purpose tags.
- **Rectification:** Correct inaccurate consent metadata (e.g., wrong version
  ID); log before/after.
- **Erasure:** Hard delete consent records after RC-CONSENT expiry (consent
  lifetime + 3y). Withdrawal records retained as proof of Art. 7(3)
  compliance — the withdrawal act itself cannot be erased while demonstrability
  is required.
- **Portability:** Export consent history in JSON.
- **Restriction:** Flag records — no downstream consent-dependent processing.
- **Note:** Erasure of active consent records for consent-dependent systems
  (ROPA-005, ROPA-006) must trigger cessation of that processing.

### Step 5 — Processor cascade (Day 5)

For requests requiring processor action (erasure, restriction, portability,
rectification with recipient notification):

1. Send cascade notification to each in-scope processor via DPA contact
   channel.
2. Include: case reference, subject identifier (pseudonymized where possible),
   request type, specific action required, deadline (15 days from notification
   to leave buffer before Day 30).
3. Log processor notifications in case file.
4. Follow up at Day 12 if no response received.

### Step 6 — Response compilation (Day 15–20)

1. Aggregate data from all systems into a single response package.
2. For **access** requests: compile per-system data inventory, format per
   template (`data-subject-requests/templates/<lang>/DSR-access-<lang>.md`).
3. For **erasure** requests: compile confirmation per system (deleted /
   anonymized with legal basis / pending processor confirmation).
4. For **portability** requests: export in machine-readable format (JSON
   preferred, CSV acceptable).
5. Review for:
   - No third-party data included (redact if present).
   - No data beyond scope of request (for targeted requests).
   - Financial records properly anonymized (not raw-deleted) per ADR-0001.
   - All processor responses received and documented.

### Step 7 — DPO review (Day 20–21)

1. DPO reviews response for:
   - Completeness (all in-scope systems covered).
   - Legal accuracy (correct basis citations, no over-disclosure).
   - ADR-0001 compliance (financial data anonymized, not raw-deleted).
   - Processor cascade completeness.
2. DPO signs off or returns with corrections (max 1 revision cycle).

### Step 8 — Response delivery (Day 21–25)

1. Send response to data subject via verified contact channel.
2. Use language-appropriate template.
3. Include:
   - Summary of actions taken per system.
   - Right to lodge complaint with supervisory authority
     (`docs/regulatory-contacts.md`).
   - For partial erasure: explanation of legal hold (ADR-0001) with statutory
     basis citation.
   - For extension: notice already sent within Day 30.
4. Log: `Responded` column = delivery date.

### Step 9 — Closure (Day 25–30)

1. Update `data-subject-requests/register.md`:
   - `Responded` date.
   - `On time` = `yes` if delivered ≤ Day 30.
   - `Status` = `fulfilled` / `refused` / `withdrawn`.
2. Archive processor confirmation emails in DSR system (not in git).
3. If erasure: verify anonymization acts logged per system.
4. If extension was granted: log original deadline, extension date, and
   justification.

---

## 5. Special cases

### 5.1 Erasure vs. legal retention conflicts (ADR-0001)

When an erasure request covers RC-FINANCIAL or RC-KYC data:

1. **Do NOT hard-delete.** Apply anonymize-don't-delete per ADR-0001.
2. Remove all direct and indirect identifiers.
3. Retain fiscal fields (amounts, dates, VAT codes) as legally required.
4. For RC-PAYROLL-50Y candidates: apply do-not-delete flag; DPO review
   required before any action. Cite Art. 17(3)(b) legal obligation in
   response.
5. Response letter must explain partial erasure with legal basis
   (`templates/<lang>/DSR-erasure-<lang>.md` — partial variant).

### 5.2 Manifestly unfounded or excessive requests

Per Art. 12(4)–(5):

1. DPO assesses whether the request is manifestly unfounded or excessive.
2. If so, may **refuse** or **charge a reasonable fee** (cost recovery).
3. Refusal must: cite specific ground, be approved by DPO, use refusal
   template, inform subject of right to complain to SA.
4. Burden of proof is on the controller — document reasoning.

### 5.3 Requests from children

If the subject appears to be under 16 (or under 14 in LT per national law):

1. Verify age.
2. If child: process with parental consent verification.
3. Escalate to DPO immediately — heightened scrutiny.

### 5.4 Third-party data in scope

If the requested data includes information about other identifiable persons:

1. Balance the requester's right of access against the third party's rights.
2. Redact third-party identifiers unless the third party has consented or
   there is another lawful basis.
3. Document the balancing test.

### 5.5 Cross-border requests (LT / LV / EE)

1. Determine the subject's market from account registration.
2. Respond in the subject's preferred language (templates available in
   `lt/`, `lv/`, `et/`, `en/`).
3. If the request is forwarded from a supervisory authority, acknowledge
   within 72 hours and escalate to DPO immediately.

---

## 6. Refusal procedure

1. DPO reviews and approves refusal decision.
2. Use refusal template: `DSR-refusal-<lang>.md`.
3. Must cite: specific legal ground (Art. 12(4), Art. 17(3)(a)–(d), Art. 23,
   or national derogation).
4. Inform data subject of:
   - Reason for refusal.
   - Right to lodge complaint with supervisory authority
     (`docs/regulatory-contacts.md`).
   - Right to judicial remedy.
5. Log in register: Status = `refused`, `On time` = per deadline.

---

## 7. Escalation matrix

| Situation | Action | Escalate to |
|---|---|---|
| Identity unverifiable after 2 attempts | Send "unable to verify" letter; pause clock | DPO |
| System returns unexpected data volume | Assess complexity; consider extension | DPO |
| Processor non-responsive by Day 12 | Follow up; if Day 17 still silent, escalate | DPO → processor management |
| Request spans all 8 systems + processors | Assess for extension (+2 months) | DPO approval required |
| SA forwards request on behalf of subject | Immediate DPO escalation; 72h acknowledgment | DPO → management |
| Subject threatens legal action | Do not engage; route through DPO | DPO → legal counsel |
| DSR SLA monitor pages (Day 21) | Immediate triage; assess remaining days | DPO + compliance lead |

---

## 8. Evidence and audit trail

Every DSAR generates the following evidence (stored in DSR system, not git):

| Evidence | Retention | Purpose |
|---|---|---|
| Request intake record | Case lifetime + 3y | Proof of receipt (clock start) |
| Identity verification log (no ID material) | Case lifetime | Proof of verification (Art. 12(6)) |
| System query results (per system) | Case lifetime + 3y | Proof of completeness |
| Processor cascade notifications + confirmations | Case lifetime + 3y | Proof of cascade |
| Response letter (sent version) | Case lifetime + 3y | Proof of fulfillment |
| Extension notice (if applicable) | Case lifetime + 3y | Proof of timely notification |
| Refusal decision + reasoning (if applicable) | Case lifetime + 5y | Defense against SA challenge |
| Anonymization act log (erasure cases) | Case lifetime + 10y | ADR-0001 compliance |

The anonymized index in `data-subject-requests/register.md` is parsed by
`scripts/dsr-sla-report.py` for monthly SLA reporting and feeds into
management review (`management-review/dpo-reports/`).

---

## 9. Monitoring and SLA

| Metric | Target | Monitor |
|---|---|---|
| On-time response rate | 100% | `scripts/dsr-sla-report.py` |
| DPO page threshold | Day 21 | `dsr-sla-monitor.yml` |
| Processor response SLA | 15 days from cascade | Manual follow-up |
| Monthly SLA report | Generated by 5th of following month | `sla-reports/` |
| Management review | Quarterly DPO report includes DSR stats | `management-review/` |

---

## 10. References

- GDPR Art. 12–22 (data subject rights)
- `data-subject-requests/README.md` — process overview
- `data-subject-requests/register.md` — anonymized case index
- `data-subject-requests/templates/` — response letter templates
- `ropa/master-register.csv` — system inventory
- `ropa/by-system/` — per-system data processing details
- `docs/adr/ADR-0001-anonymize-dont-delete.md` — erasure vs. retention
- `docs/retention-schedule.md` — per-country retention matrix
- `docs/regulatory-contacts.md` — supervisory authority contacts
- `policies/02-data-protection-privacy.md` — DPO role and GDPR program
- `vendor-assessments/register.md` — processor register + DPA status
