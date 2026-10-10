# INC-2026-01 — Public exposure of governance repositories

> **DRAFT — NOT YET ACCEPTED.** Prepared 2026-09-28 by the vendor management
> owner's assistant. The Art. 33 conclusion in §3.4 is a regulatory determination
> that must be reviewed and signed by the natural person acting in the data
> protection lead capacity before this record is treated as the incident decision.
> Do not hash into `audits/evidence-registry.csv` until §8 closure criteria are met.

| | |
|---|---|
| ID | INC-2026-01 |
| Slug | `public-exposure-governance-repos` |
| Detected | 2026-09-17 (delivery-chain audit observation, per `jolarca-control/docs/drift-findings.md` D-01/D-08) |
| Recorded | 2026-09-28 |
| Severity | **High** — confidentiality of regulated governance records |
| Personal data breach? | **No** — see §3 |
| Art. 33 notification | **Not required** (draft conclusion, unsigned) |
| Art. 34 notification | **Not engaged** |
| Containment | **Complete** — affected repositories verified private on 2026-09-28 |
| Status | Open pending actions A2, A3, A4, A5 |
| Related | `drift-findings.md` D-01, D-08, D-18, D-31, D-33 |

No personal data appears in this record. Repositories are identified by name;
individuals by role only.

## 1. What happened

Four repositories holding regulated compliance, legal, data and infrastructure
governance records were declared `visibility: private` in
`jolarca-control/repos/*.yml` while their live GitHub setting was `public`. The
declared-versus-live divergence is recorded in the estate deviation register as
D-01 and assessed as blocking and unremediated in D-31.

Content enumerated as exposed in D-31 includes the RoPA master register
(populated, carrying data-category columns), per-system RoPA entries, seven vendor
assessments, the vendor contract register, and DPA/NDA/employment contract
templates.

The divergence has been remediated: all four repositories now report
`visibility=private`. Containment was verified independently on 2026-09-28 (§4).

## 2. Exposure window — NOT PRECISELY DETERMINABLE

Recorded as uncertain rather than resolved by assumption, because the window
bounds the residual risk in §6.

| Bound | Value | Source |
|---|---|---|
| Earliest possible start | 2026-08-14 / 2026-08-15 | Repository `created_at`, GitHub API |
| Latest possible end | 2026-09-26 | D-08 correction, dated 2026-09-26, states the repositories "were flipped private" |
| **Working window** | **≈ 2026-08-14 → 2026-09-25/26 (about 6 weeks)** | Adopted for this assessment |

The exact transition timestamp **cannot be established**, because two available
sources conflict and the authoritative one is inaccessible:

1. **Conflicting sources.** `repos/jolarca-dev/jolarca-compliance/events` returns
   events dated 2026-09-09T11:13:49Z and 2026-09-25T16:59:48Z / 17:01:58Z, each
   carrying `"public": false` — implying the repository was already private on
   2026-09-09. D-31 states public contents were enumerated on 2026-09-25. Both
   cannot be correct.
2. **Authoritative source unavailable.** `orgs/jolarca-dev/audit-log` returns
   **HTTP 404**; the organisation audit log requires a paid plan. Verified
   2026-09-28.

Consequence: whether the window was six weeks or materially shorter is unknown.
Action A2 addresses this. The §3 conclusion does not depend on the window's
length, because it turns on the *nature* of the content rather than the duration
of exposure — but the unknown-third-party-copy residual in §6 does scale with it,
and is therefore stated at the conservative bound.

## 3. Personal data assessment — Art. 33 / Art. 34

### 3.1 Test applied

A notifiable personal data breach requires a security breach leading to
accidental or unlawful destruction, loss, alteration, or **unauthorised disclosure
of, or access to, personal data**. The question is factual: did the exposed
content contain personal data?

### 3.2 Evidence gathered 2026-09-28

Matched values were never printed during this investigation; pattern matching
reported counts and file names only, so that the assessment did not itself create
a fresh disclosure.

| Check | Result |
|---|---|
| `data-subject-requests/` inventory | 8 files: `README.md`, `register.md`, four language template directories containing `.gitkeep`, `sla-reports/.gitkeep`. **No case records exist** |
| Personal-data patterns in `data-subject-requests/` | Email-shaped 0; Baltic personal codes 0; `name/surname/address/passport/id_number` assignments 0 |
| Baltic personal codes, whole repository | **0** |
| IBAN patterns, whole repository | **0** |
| Email-shaped lines, whole repository | 19, confined to `README.md`, `SECURITY.md`, `docs/regulatory-contacts.md`, `retention/tests/fixtures/*.json`, `retention/tests/test_retention.py` |
| Nature of `docs/regulatory-contacts.md` | Two **role** addresses (DPO, Security), stated in the file to be already named in the imprint and privacy policy — intentionally public, not data-subject data |
| Nature of remaining email matches | Synthetic values in retention **test fixtures** |
| High-signal secret patterns, tracked files | `jolarca-compliance` 1 (planted dummy, §3.3); `jolarca-legal` 0; `jolarca-data` 0; `jolarca-infrastructure` 0 tracked — its 23 matches were under `ansible/.ansible/`, which is gitignored with **0 tracked files** |
| `terraform.tfstate` / `terraform.tfvars` token patterns | 0 |
| Forks and watchers, all affected repositories | `forks_count = 0`, `watchers_count = 0` |

### 3.3 The single secret-pattern match

`audits/internal/2026-08-initial-build-audit/AUDIT_REPORT.md:108` matched an AWS
access-key-ID shape. Reading the line establishes it as **evidence item E14** of
that audit: a negative control in which dummy credentials were deliberately
planted to prove the secret scanner detects them ("3/3 detected"). It is a
documented test artifact, not a credential.

This is corroborating, not merely exculpatory. The same audit records E11 "PII
sweep: emails, 11-digit codes, LV codes, IBAN, phones — only `.example`
placeholders; **zero real PII**", E12 `redact-pii.py --all` clean, and E13
`gitleaks detect` over the full tree with no leaks. An independent prior
assessment reached the same conclusion by a different method.

### 3.4 Conclusion — DRAFT, REQUIRES SIGNATURE

**The exposed content did not contain personal data.** It contained governance
records *about* processing — data categories, lawful bases, retention classes,
recipient names, DPIAs, vendor assessments and contract templates — together with
synthetic test fixtures and role-based contact addresses already published.

Accordingly:

- **Art. 33** notification to VDAI / DVI / AKI is **not required**. There was no
  personal data breach.
- **Art. 34** communication to data subjects is **not engaged**.
- **Art. 33(5)** documentation of the facts **is** required and is discharged by
  this record. The duty to document survives a conclusion that no notification is
  due, which is why this record exists rather than the assessment remaining
  verbal.

This conclusion rests on the evidence in §3.2 and is **falsifiable**: if any
data-subject record is later found in the exposed content, §3 must be reopened and
Art. 33 reassessed against the original awareness date of 2026-09-17 — not against
the date of discovery. Reassessing from the later date would understate the delay
and is the specific error this sentence exists to prevent.

## 4. Containment verification — 2026-09-28

Live GitHub API, not the declared configuration.

| Repository | `visibility` | `private` | forks |
|---|---|---|---|
| jolarca-compliance | private | true | 0 |
| jolarca-legal | private | true | 0 |
| jolarca-data | private | true | 0 |
| jolarca-infrastructure | private | true | 0 |
| jolarca-control | private | true | 0 |
| jolarca-security | private | true | 0 |

Still public, each verified rather than assumed:

| Repository | Size | Assessment |
|---|---|---|
| `jolarca` | 1187 KB | Public by design. Secret scan over **tracked** files: 0 high-signal matches. `ssl/`, `backups/`, `logs/`, `node_modules/`, `.idea/` all gitignored; only `secrets/encrypted/README.md` tracked under `secrets/`. See A6 — `secrets/` itself is **not** gitignored |
| `jolarca-identity` | 27 KB | Public. Method only — access-control policy, authentication standards, RBAC, role definitions, joiner-mover-leaver, access-review procedure. 0 emails, 0 personal codes, 0 literal secrets; the 12 keyword matches are policy prose on token rotation and RBAC scope names |
| `jolarca-vendor` | 0 KB | Public by design, unborn. Classified `internal`, method only |
| `jolarca-payments`, `jolarca-consent`, `jolarca-observability`, `jolarca-runbooks`, `jolarca-docs`, `jolarca-dr` | 0 KB | Public and unborn. No content to expose |
| `.github` | 17 KB | Public organisation profile, by design |

## 5. Procedural failures — recorded against us

Omitting these would make the record self-serving.

1. **The 72-hour assessment was not documented within the clock.** Awareness dates
   from 2026-09-17 at the latest. `incidents/README.md` requires a register entry
   "created immediately". This entry was created on **2026-09-28** — eleven days
   later, against a register that was still empty. Containment happened promptly;
   the **documentation** did not, and Art. 33(5) and SOC 2 CC7.3 concern
   documentation.
2. **The deviation register carried a stale factual claim.** D-31 asserted a live
   public state that the API contradicted on 2026-09-28, and the events API
   suggests the repository may have been private considerably earlier. A blocking
   S1 finding left open after remediation trains readers to treat blocking
   findings as background — which defeats the register's purpose. Action A3.

## 6. Residual risk

| Risk | Position |
|---|---|
| Unknown third-party copies | **Cannot be excluded.** `forks_count = 0` proves no public fork exists now; it does not prove nobody cloned during the window. Cloning leaves no server-side trace. This is the principal irreducible residual and scales with the window §2 cannot bound |
| Search-engine and archive caching | Public repositories are indexed by third-party mirrors and archive services. Whether this one was captured during the window is unknown and not determinable retrospectively without the audit log |
| Compliance-posture disclosure | During the window a reader could enumerate supplier relationships, data categories, transfer positions and control gaps. No personal data, but commercially and regulatorily sensitive. Materially mitigated by containment |
| Recurrence | **Root cause not fixed.** Declared visibility can again diverge from live visibility with no gate asserting they agree — `validate_repos.py` validates the declaration only. Action A5 |
| Related open exposure | D-18: organisation-wide two-factor authentication is **not** enforced; the API returns `two_factor: null` as of 2026-09-28. Materially weakens the account protection this containment depends on. Action A4 |

## 7. Actions

| Ref | Action | Owner | Due | Status |
|---|---|---|---|---|
| A1 | Record this incident; create register entry and folder | Data protection lead (capacity) | 2026-09-28 | Draft prepared |
| A2 | Establish exact visibility-change timestamps. Blocked on the organisation audit log, which requires a paid plan — resolve via the plan decision or accept the uncertainty in writing | Vendor management owner | 2026-10-12 | Open — blocked |
| A3 | Correct D-31 and D-01 in `drift-findings.md` to the verified private state, using that register's dated-correction convention; close or re-grade D-31 | Vendor management owner | 2026-10-05 | Open |
| A4 | Enforce organisation-wide two-factor authentication (D-18) | Organisation owner | 2026-10-05 | Open |
| A5 | Add a gate asserting **live** visibility matches declared visibility, so the divergence cannot recur undetected | Vendor management owner | 2026-10-19 | Open |
| A6 | Add `secrets/` to `.gitignore` in `jolarca`. Only `secrets/encrypted/README.md` is tracked today, but the directory is not ignored, so a future `git add -A` in a **public** repository could stage unencrypted material | Owner, `jolarca` | 2026-10-05 | Open |
| A7 | Add secret scanning to `jolarca-compliance` CI — audit finding F-C1 ("no CI secret scanning") remains open | Owner, `jolarca-compliance` | 2026-10-19 | Open |

A5 matters most. A1–A4 close this incident; A5 is the only action that prevents
the next one. A declared-configuration validator that never queries the live
setting is the same defect class as a gate that is configured and never fires —
which this estate has already recorded twice against itself (D-20, D-22).

## 8. Closure criteria

Per `incidents/README.md`: decision documented (§3.4 and `decisions.md`,
**signed**), actions owned and dated (§7), evidence hashed into
`audits/evidence-registry.csv` (`evidence.md`), register updated
(`../../register.md`).

A2 and A5 must close, or be formally accepted with a written reason and a review
date, before this incident closes. A3 and A4 are tracked in the deviation register
and do not block closure here provided their references are recorded.
