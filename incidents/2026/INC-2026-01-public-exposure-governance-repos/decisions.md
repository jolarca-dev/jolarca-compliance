# INC-2026-01 — Decisions Log

> **DRAFT — UNSIGNED.** Per `incidents/README.md` the 72-hour assessment must
> conclude with a **documented** decision. This file records the recommended
> decision and the reasoning, and is the artifact the natural person signs.
> An unsigned decisions log is not a decision.

## D1 — Is this a personal data breach requiring Art. 33 notification?

**Recommended decision: NO. Do not notify.**

| Element | Finding |
|---|---|
| Was there a security breach? | Yes — unauthorised public readability of repositories intended to be private |
| Did it lead to disclosure of, or access to, **personal data**? | **No.** Evidence at §3.2 of `report.md`: no DSR case records exist; 0 Baltic personal codes; 0 IBANs; the 19 email-shaped strings are test fixtures and two role addresses already published in the imprint and privacy policy |
| Is a risk to data subjects likely? | No risk arises, because no data-subject personal data was exposed |
| Conclusion | Art. 33(1) is not engaged. The "unless unlikely to result in a risk" exemption is not even reached, because the threshold condition — a personal data breach — is not met |

**Independent corroboration.** The 2026-08 initial build audit reached the same
conclusion by a different method: E11 PII sweep "zero real PII", E12
`redact-pii.py --all` clean, E13 `gitleaks detect` no leaks.

**Falsification condition.** If any data-subject record is later identified in the
exposed content, this decision is void and Art. 33 must be reassessed against the
**2026-09-17 awareness date**, not the date of discovery.

## D2 — Is Art. 34 communication to data subjects required?

**Recommended decision: NO. Not engaged.**

Art. 34 requires communication where a personal data breach is likely to result in
a **high risk** to individuals. D1 establishes there was no personal data breach,
so Art. 34 does not arise. No communication is made.

## D3 — Was this nevertheless an incident worth recording?

**Decision: YES. Severity High.**

The absence of a notification duty is not the absence of an incident. What was
exposed for up to approximately six weeks was the organisation's **compliance
posture**: the RoPA, DPIAs, seven vendor assessments, the contract register, and
DPA/NDA/employment templates. That discloses supplier relationships, data
categories, transfer positions and control gaps to any reader — commercially
damaging and regulatorily unflattering, and useful reconnaissance for an adversary
choosing which supplier relationship to attack.

Recording it as High rather than closing it as a non-event is deliberate.
Under-grading an incident because it turns out not to be notifiable is how an
organisation loses the ability to see its own pattern: the root cause here —
declared configuration never checked against live configuration — is the same class
as D-20 and D-22, and this is the third instance.

## D4 — Is containment complete?

**Decision: YES, verified 2026-09-28 against the live API.**

All four affected repositories report `visibility=private`, `private=true`,
`forks_count=0`. Verification used the live API rather than the declared
configuration, because the entire incident is a divergence between the two.

Containment is complete but the **root cause is not fixed**: nothing prevents the
divergence recurring. Action A5.

## D5 — Should the exposure window be recorded as six weeks, or as indeterminate?

**Decision: INDETERMINATE, with a six-week working bound.**

Recording a confident six-week window would overstate the precision of the
evidence; recording only "indeterminate" would understate what is known. Both
sources are named in `timeline.md` with their provenance, and the conflict between
the events API (`"public": false` on 2026-09-09) and D-31 (public contents
enumerated 2026-09-25) is stated rather than resolved by preference.

This matters because the residual "unknown third-party copy" risk scales with the
window. Choosing the shorter reading would flatter the assessment; the conservative
bound is used.

## D6 — Does anything need revocation or rotation?

**Decision: NO credentials require rotation on the evidence gathered.**

High-signal secret patterns across tracked files: `jolarca-compliance` 1 (a planted
dummy documented as audit evidence E14), `jolarca-legal` 0, `jolarca-data` 0,
`jolarca-infrastructure` 0 tracked (23 matches under a gitignored cache directory),
`terraform.tfstate` and `terraform.tfvars` 0. `jolarca` and `jolarca-identity`
remain public and show 0 literal secrets.

This decision is **conditional on the scan's coverage**. The patterns tested were
AWS key IDs, private key blocks, GitHub classic and fine-grained tokens, Slack
tokens, age secret keys, Google API keys and Stripe keys. Credential classes
outside that set — database connection strings, basic-auth URLs, SMTP credentials,
custom bearer tokens — were not exhaustively tested across all four repositories.
Action A7 adds repository-level secret scanning so this question is answered by a
gate rather than by a one-off manual sweep.

## Sign-off

| Capacity | Natural person | Decision | Date | Commit |
|---|---|---|---|---|
| Data protection lead | | D1 no-notify / D2 not engaged | | |
| Vendor management owner | | D3 severity High / D4 containment complete | | |
| Risk owner | | D5 window indeterminate / D6 no rotation | | |

Per `jolarca-vendor/docs/solo-operator-controls.md`, one natural person may hold
all three capacities. What is **not** acceptable is recording a role title with no
holder — "DPO" or "Management" as an approver is not evidence that anyone decided
anything. Enter the person's name, the capacity acted in, and the signed commit
hash. The signature is the control; the table above is where it is recorded.
