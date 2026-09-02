# DPIA Register

Single index of all Data Protection Impact Assessments. Update on any status
change; the single cross-year source of truth (scripts do not glob folders).

| ID | Title | Status | Owner | Review date | Linked RoPA | Gate |
|---|---|---|---|---|---|---|
| 001 | Identity and consent | reviewed | Compliance Team | 2027-01-15 | ROPA-001, ROPA-002 | G1 |
| 002 | AI processing (LLM egress) | reviewed | Compliance Team | 2027-01-15 | ROPA-005 | G2 |
| 003 | Payments and VAT | reviewed | Compliance Team | 2027-01-15 | ROPA-003, ROPA-004 | G3 |
| 004 | Geolocation search | reviewed | Compliance Team | 2027-01-15 | ROPA-006 | G2 |

Status values: `draft`, `reviewed`, `signed`, `superseded-by:<ID>`.
A signed DPIA's hash must exist in `audits/evidence-registry.csv`.
