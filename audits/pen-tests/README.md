# Penetration Tests

One folder per engagement: `YYYY-MM-DD-<scope>-<vendor>/` containing:

- Report (LFS pointer + hash in registry)
- Scope statement & rules of engagement
- Remediation tracker: every finding → owner, due date, fix evidence
- Re-test confirmation for critical/high findings

Rules:

- **Critical/high findings block launch (G4)** until closed or risk-accepted
  via `policies/exceptions/` with DPO sign-off.
- At least annual external pen test; critical-path re-tests after major changes.
- Reports are confidential: access limited to compliance + engineering leads.
