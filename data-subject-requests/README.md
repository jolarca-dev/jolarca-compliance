# Data Subject Requests (Art. 15–22)

## Process

`intake (DSR issue form) → identity verification → scope assessment →
30-day clock → fulfillment → response letter → register closure`

1. Clock starts at **receipt** (Art. 12(3)); DPO paged at day 21
   (`dsr-sla-monitor.yml`); extension max +2 months only with documented
   complexity/volume justification and subject notification within 30 days.
2. Identity verification before any disclosure; verification material is
   deleted after the check (retention class RC-DSR-VERIFY).
3. **The register stores only anonymized indexes.** Request content, requester
   identity, and fulfillment payloads stay in the DSR system — never in git.
4. Response letters from `templates/<lang>/` per request type.
5. Erasure requests cascade to all recipients/processors (RoPA-driven).
6. Monthly SLA report generated into `sla-reports/` and reviewed in
   management review.

## Refusal / partial fulfillment

Must cite the specific legal ground, be approved by the DPO, and use the
refusal letter template for the market language.
