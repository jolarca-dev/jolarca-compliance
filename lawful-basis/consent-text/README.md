# Consent texts

One folder per language: `lt/ lv/ et/ en/` (+ `ru/` where offered).

File naming: `CT-<purpose>-v<N>.md` (e.g. `CT-marketing-v2.md`).

Each file must contain:

1. Version ID and effective date
2. Full consent string exactly as displayed in the UI
3. Purpose + lawful basis reference
4. Withdrawal path (where and how to withdraw)
5. Approval: legal counsel + DPO sign-off lines

A consent text is **final** once deployed; corrections require a new version
and a `consent-versions.md` ledger entry.
