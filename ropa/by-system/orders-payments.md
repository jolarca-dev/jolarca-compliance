# RoPA — orders-payments (ROPA-003)

| Field | Value |
|---|---|
| Purpose | Order & payment processing, invoicing |
| Lawful basis | Art. 6(1)(b) contract; Art. 6(1)(c) accounting obligations |
| Data categories | Order data, payment references, delivery address |
| Subjects | Buyers, sellers |
| Retention | RC-FINANCIAL — Baltic accounting holds (10y LT/LV/EE variants) |
| Recipients | Stripe (processor, PCI DSS), DPD, Omniva |
| Transfers | Stripe — SCC + TIA (see `vendor-assessments/tia/`) |
| Controls | SAQ-A scope (no card data on platform); idempotency keys; replay protection |

Last reviewed: 2026-08-15 (draft skeleton — populate before G3).
