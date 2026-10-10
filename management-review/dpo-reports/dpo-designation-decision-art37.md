# DPO Designation Decision — Art. 37 GDPR Assessment

| | |
|---|---|
| Document type | Art. 37(1)–(3) necessity assessment + voluntary designation record |
| Controller | Journey Of Life marketplace (sole proprietorship) |
| Prepared by | Compliance lead |
| Approved by | Management |
| Date | 2026-09-28 |
| Review date | 2027-09-28 (annual, or upon material change in processing) |
| Supersedes | — |

## 1. Purpose

Article 37(1) GDPR requires the designation of a Data Protection Officer only when
at least one of three mandatory conditions is met. This document records the
assessment of each condition and the resulting decision.

## 2. Art. 37(1) — Mandatory designation criteria

### 2.1 Criterion (a): public authority or body

> "processing is carried out by a public authority or body"

**Assessment:** The controller is a private sole proprietorship operating a
commercial marketplace platform. It is not a public authority or body within the
meaning of national law.

**Result:** Not met.

### 2.2 Criterion (b): large-scale regular and systematic monitoring

> "core activities consist of processing operations which require regular and
> systematic monitoring of data subjects on a large scale"

**Assessment:**

- **Core activity** of the controller is operating a peer-to-peer marketplace
  (listing, ordering, payment facilitation, shipping coordination). Data
  processing is incidental to service delivery, not monitoring of data subjects.
- **Scale:** The platform serves a niche market across three EU Member States
  (LT, LV, EE). Current data subject population is limited (see
  `ropa/master-register.csv` — six processing activities, all operational).
  User base is well below the thresholds referenced in WP29 guidelines
  (Rev. 01/2017, p. 9): no thousands of data subjects per day, no cross-border
  monitoring of behaviour.
- **Regular and systematic:** No behavioural profiling, no tracking of
  off-platform behaviour, no automated decision-making with legal or similarly
  significant effects (Art. 22). Geolocation search (ROPA-006) is consent-based
  and initiated by the data subject — not systematic monitoring.

**Result:** Not met.

### 2.3 Criterion (c): large-scale processing of special categories

> "core activities consist of processing on a large scale of special categories
> of data pursuant to Article 9 and personal data relating to criminal
> convictions and offences referred to in Article 10"

**Assessment:**

- No processing of Art. 9 special categories (racial/ethnic origin, political
  opinions, religious/philosophical beliefs, trade union membership, genetic
  data, biometric data for identification, health data, sex life/sexual
  orientation data).
- No processing of Art. 10 criminal conviction data.
- KYC verification (ROPA-002) processes identity documents and business registry
  data — these are ordinary personal data, not special categories.

**Result:** Not met.

## 3. Decision

None of the three mandatory conditions under Art. 37(1) GDPR are met.
**Mandatory designation of a DPO is not required.**

## 4. Voluntary designation

Although not legally required, the controller has **voluntarily designated** a
data protection function to demonstrate accountability (Art. 5(2)) and to
provide an independent oversight point for GDPR compliance. This is consistent
with WP29 guidance encouraging voluntary designation.

| Field | Value |
|---|---|
| Designation type | Voluntary (Art. 37(4) GDPR) |
| Contact point | dpo@journeyoflife.example |
| Published in | `docs/regulatory-contacts.md`, privacy policy, imprint |
| Tasks | As set out in Art. 39(1): monitor compliance, advise on DPIAs, cooperate with supervisory authorities, act as contact point |
| Position | Reports directly to management; independent in exercise of tasks (Art. 38(3)); no instructions regarding task execution; may not be dismissed or penalised for performing tasks (Art. 38(3)) |
| Resources | Adequate time, budget, and access to processing operations as required by Art. 38(2) |

## 5. Obligations that still apply

Per Art. 37(4), when a voluntary DPO is designated, **all provisions of
Section 4 (Art. 37–39) apply** as if the designation were mandatory:

- Independence and reporting line (Art. 38(3)–(4))
- Tasks listed in Art. 39
- Data subjects may contact the DPO regarding processing of their data and
  exercise of their rights (Art. 38(4))
- DPO bound by secrecy/confidentiality (Art. 38(5))

## 6. Reassessment triggers

This assessment must be revisited when any of the following occurs:

1. Processing scale increases materially (e.g., expansion beyond 3 markets,
   user base exceeding thresholds in WP29 guidelines).
2. New processing activities introduce systematic monitoring (e.g., behavioural
   advertising, automated profiling).
3. Special category or criminal conviction data processing is introduced.
4. Regulatory guidance or supervisory authority interpretation changes the
   scope of Art. 37(1).
5. Material change in the nature of core activities.

## 7. References

- GDPR Art. 37(1)–(5), Art. 38, Art. 39
- WP29 Guidelines on Data Protection Officers (Rev. 01, adopted 5 April 2017)
- `docs/regulatory-contacts.md` — published DPO contact
- `policies/02-data-protection-privacy.md` — DPO role in ISMS
- `management-review/README.md` — DPO reporting cadence
- `audits/gate-evidence/G0-foundation/README.md` — G0 artifact checklist

## 8. Approval

| Role | Name / Identifier | Date | Signature |
|---|---|---|---|
| Management (controller) | _sole proprietor_ | 2026-09-28 | _pending_ |
| Compliance lead | — | 2026-09-28 | _pending_ |

---

> **Professional opinion:** Given the current scale and nature of processing
> (niche marketplace, 3 Baltic markets, 6 processing activities, no special
> categories, no systematic monitoring), the "not required" conclusion is
> defensible and well-supported. The voluntary designation provides
> accountability benefits and satisfies auditor expectations without the full
> regulatory burden. Should the platform scale significantly or introduce
> behavioural profiling, this assessment must be revisited immediately.
