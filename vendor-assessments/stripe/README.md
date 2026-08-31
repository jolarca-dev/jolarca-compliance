# Stripe (processor — payments)

- Role: payment processing under SAQ-A scope (no card data touches platform)
- Status: onboarding — artifacts pending
- Next review: 2027-08-15

## Artifact map (corrected 2026-08-17, STEP 26 — see `STEP26_CORRECTIONS.md`)

| Artifact | Origin | Retrieval procedure |
|---|---|---|
| DPA | **Issued by Stripe** (Art. 28) | Counter-signed contract; file signed copy here |
| SCCs | **Referenced within the Stripe DPA** (not a standalone Stripe download) | Cite the DPA clause; file the module text with the DPA |
| PCI DSS AoC | **NOT a public download.** Stripe Dashboard → **Compliance Settings** → download the AoC for the JOL account; if not available there, open a **Stripe support request** for the current AoC | Record below: who retrieved, when, document version/date |
| TIA | **Self-authored by JOL** (Schrems II; Stripe supplies the DPA/SCCs as *inputs* — Stripe does not issue the TIA) | Author via `../tia/` template; file as `TIA-stripe-01-vN.md` |
| SAQ-A scope letter | JOL-authored (scope defense) | `certifications/pci-dss/` |
| Sub-processor list | Issued by Stripe | Refresh at each vendor review |

## AoC retrieval record (append-only)

| Retrieved by | Date | Document version/date | Channel | Filed |
|---|---|---|---|---|
| — | — | — | — | — |

## Review cadence

AoC retrieval/refresh and TIA re-assessment join the vendor-review cadence:
**annually, or immediately on any Stripe compliance-program update**
(new PCI DSS version, new Attestation of Compliance cycle, sub-processor
change notice). See `../README.md` annual cycle.
