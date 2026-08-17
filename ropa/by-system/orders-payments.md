# RoPA — orders-payments (ROPA-003)

| Field | Value |
|---|---|
| Purpose | Order & payment processing, invoicing |
| Lawful basis | Art. 6(1)(b) contract; Art. 6(1)(c) accounting obligations |
| Data categories | Order data, payment references, delivery address |
| Subjects | Buyers, sellers |
| Retention | RC-FINANCIAL — per-country statutory matrix in `docs/retention-schedule.md` §2 (LT: 10y accounting, Law on Accounting of the Republic of Lithuania; LV/EE `[COUNSEL-TO-CONFIRM]`). Payout/verification records touching employment-adjacent personal data: RC-PAYROLL-50Y candidate (LT up to 50y) — do-not-delete flag, DPO review |
| Recipients | Stripe (processor, PCI DSS), DPD, Omniva; VMI via i.SAF FR0600 monthly filing (`docs/regulatory-obligations.md` OBL-001) |
| Transfers | Stripe — SCC + TIA (see `vendor-assessments/tia/`) |
| Controls | SAQ-A scope (no card data on platform); idempotency keys; replay protection |

Last reviewed: 2026-08-17 (STEP 26: flat retention period replaced by the
per-country matrix; i.SAF recipient added). Draft skeleton — populate before G3.
