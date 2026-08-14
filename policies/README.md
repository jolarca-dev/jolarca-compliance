# Policies — ISMS (ISO 27001 Annex A mapped)

## Hierarchy

1. **Top-level**: `01-information-security-policy.md` (ISMS umbrella)
2. **Domain policies**: 02–12 (each maps to Annex A / SOC 2 TSC controls)
3. **Procedures & runbooks**: referenced from domain policies, live with the
   owning team's repo
4. **Exceptions**: `exceptions/` — the only lawful deviation path

## Review cycle

- Annual review of every policy; `Next review` date in each metadata block.
- `policy-review-reminder.yml` opens issues 30 days ahead; overdue > 14 days
  fails CI (`compliance-check.yml`).
- Material change = new minor version + CHANGELOG entry + DPO approval.

## Metadata block contract

Every policy starts with: Version, Owner, Approved by, Effective date,
Next review, ISO 27001 mapping, SOC 2 TSC mapping. `scripts/policy-review-dates.py`
parses the `Next review:` line — keep the format exact.

## Exception process

Deviations are filed in `exceptions/` as `EX-YYYY-NN.md`: justified, risk
accepted by an accountable owner, expiry-dated, and DPO-signed. Expired
exceptions are policy violations by default.
