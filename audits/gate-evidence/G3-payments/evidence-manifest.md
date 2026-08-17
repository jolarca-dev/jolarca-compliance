# G3 payment-boundary evidence manifest (hash-pinned, immutable)

- **Sealed:** 2026-08-17 by the STEP 22c independent re-audit
- **Rule:** files under `reports/` are immutable snapshots. Any change
  requires a NEW audit cycle and a new manifest generation — never an
  in-place edit. Verify with `sha256sum -c` against the table below.

## Reports (copies of the canonical repo files at seal time)

| File | Canonical source | sha256 |
|---|---|---|
| STEP17_AUDIT.md | jol-m-infrastructure @ STEP 17 | `86f028d28a74c954911edec023406ad5b5a0f7de4b297f0171b0e3dc370c9f08` |
| STEP22_REAUDIT.md | jol-m-infrastructure @ STEP 22 | `91fa1a75cafc1fed58eed65563d6bf6ef8ae85f156bf1fc1789625059d9a0a2c` |
| STEP22B_FINAL_REAUDIT.md | jol-m-infrastructure @ STEP 22b | `e1b9ed55b5f7f27798c9dd686190d53bec01b01e4821a57b6296f079e4c48bec` |
| STEP22C_FINAL_REAUDIT.md | jol-m-infrastructure @ STEP 22c | `b91c8556a5b5e99d24109d3cad3d4ea8cf179c9c9a3689522bff8d14e291dbed` |
| STEP18_EXECUTED.md | jol-hub @ `89c4812d` (PR #76) | `df1c3c1115ca55a8727c69c32072436f2ce3a80c58bb2fff3ffddc48465790b7` |
| STEP19_EXECUTED.md | jol-hub @ `07eed1ce` (PR #81) | `4f569ed3e54625c306e4ab72377436a793fd08c740c9c2c2cec6291c5e2051bd` |
| STEP20_EXECUTED.md | jol-m-marketplace @ `4faef0a3` (PR #18) | `804647f9db3ea333ad811b92ee3bccd21aa374cd07e03330c1b985c7e57909c9` |
| STEP21_EXECUTED.md | jol-m-infrastructure @ `90d589aa` (PR #10) | `374cd08614644051e59f5d76824b679cdc65a2ce4824a5a26b6cd438d1023334` |
| EXECUTION_BUNDLE_18-21.md | jol-m-infrastructure @ `90d589aa` (PR #10) | `9cb357f84d98b2609917d627d93bd92eaa53cd8196656789fd961244951bb1cd` |

## Merge-SHA ledger (GitHub-side anchors)

| Step | Repo | PR | Merge SHA |
|---|---|---|---|
| 18 | jol-hub | #76 | `89c4812d` |
| 19 | jol-hub | #77 / #81 (+incident #78→#79, probe #80) | `85d51489` / `07eed1ce` |
| 20 | jol-m-marketplace | #18 | `4faef0a3` |
| 21 | jol-hub / jol-m-infrastructure | #82 / #10 | `4f93c6b9` / `90d589aa` |
| 22c negative test | jol-hub | #83 (BLOCKED, closed unmerged) | — |

## Control-artifact pins

- E1 guard script (hub vendored == infra record):
  sha256 `8fa2dd12f12320dff268ee19d5b00422a1f5987203e34755c342e56068ed47a5`
- Hub main branch protection at seal time: required checks
  `Payment Boundary Guard (E1, ADR-0005)` + `Dependency Guard (E2,
  ADR-0005)`; `strict: true`; `enforce_admins: true`.
