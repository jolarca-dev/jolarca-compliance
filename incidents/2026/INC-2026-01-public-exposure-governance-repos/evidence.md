# INC-2026-01 — Evidence and Reproduction

> **DRAFT — see `report.md`.** Nothing here is hashed into
> `audits/evidence-registry.csv` yet. Per `incidents/README.md`, hashing happens at
> closure, once the decisions log is signed. Hashing a draft would register an
> unfinalized document as final — the exact defect recorded as F-B2 in the 2026-08
> initial build audit.

## Principle

Every factual claim in `report.md` is reproducible from the commands below. Where a
claim rests on a value that must not be disclosed, the command reports a **count or
a file name**, never the value — so that reproducing the evidence does not itself
become a disclosure.

## E1 — Live repository visibility (containment verification)

```sh
for r in jolarca jolarca-compliance jolarca-legal jolarca-data jolarca-infrastructure \
         jolarca-vendor jolarca-control jolarca-security jolarca-payments \
         jolarca-identity jolarca-consent jolarca-observability jolarca-runbooks \
         jolarca-docs jolarca-dr .github; do
  printf '%-24s ' "$r"
  gh api "repos/jolarca-dev/$r" --jq \
    '"visibility=\(.visibility) private=\(.private) forks=\(.forks_count) created=\(.created_at) size=\(.size)KB"'
done
```

Result recorded in `report.md` §4. Six repositories private, ten public, all with
`forks_count=0`.

## E2 — Organisation plan and 2FA state

```sh
gh api orgs/jolarca-dev --jq '{plan: .plan.name, two_factor: .two_factor_permission_required}'
```

Result: `plan: free`, `two_factor: null`. Supports §6 (D-18 open) and §2 (audit log
unavailable).

## E3 — Audit log unavailable (why the window is indeterminate)

```sh
gh api 'orgs/jolarca-dev/audit-log?per_page=5'
```

Result: **HTTP 404**. Supports `report.md` §2.

## E4 — Conflicting visibility evidence

```sh
gh api 'repos/jolarca-dev/jolarca-compliance/events?per_page=3' \
  --jq '.[] | "\(.created_at) \(.type) public=\(.public)"'
```

Result: three events, all `public=false`, dated 2026-09-09 and 2026-09-25.
Conflicts with D-31's statement that public contents were enumerated on 2026-09-25.
Supports `report.md` §2 and `timeline.md`.

## E5 — Personal-data census, counts only

```sh
cd jolarca-compliance
# DSR directory: does any case record exist?
find data-subject-requests -type f | sort
# Pattern census — reports counts, never values
for re in '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' '\b[3-6][0-9]{10}\b' '\b(LT|LV|EE)[0-9]{2}\b'; do
  printf '%-46s %s\n' "$re" "$(grep -rIE --exclude-dir=.git --exclude-dir=.venv -e "$re" . | wc -l)"
done
# Which files contain email-shaped strings (names only)
grep -rlIE --exclude-dir=.git --exclude-dir=.venv \
  -e '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' .
```

Result: `data-subject-requests/` contains 8 files, all README/register/`.gitkeep`
templates. Personal codes 0, IBAN 0, email-shaped 19 lines confined to README,
SECURITY, `docs/regulatory-contacts.md` and `retention/tests/` fixtures. Supports
`report.md` §3.2.

The `[3-6][0-9]{10}` pattern is the shape of Lithuanian and Estonian personal
codes; its zero count is the single most probative result in this assessment,
because those are the identifiers most likely to appear in KYC-adjacent records.

## E6 — Secret census, high-signal patterns, counts only

```sh
for r in jolarca-compliance jolarca-legal jolarca-data jolarca-infrastructure; do
  printf '%-26s %s\n' "$r" "$(grep -rIE --exclude-dir=.git --exclude-dir=.venv \
    --exclude-dir=node_modules \
    -e 'AKIA[A-Z0-9]{16}' -e '-----BEGIN [A-Z ]*PRIVATE KEY-----' \
    -e 'gh[pousr]_[A-Za-z0-9]{36,}' -e 'xox[baprs]-[A-Za-z0-9-]{10,}' \
    -e 'AGE-SECRET-KEY-1[02-9A-HJ-NP-Z]{58}' -e 'AIza[0-9A-Za-z_-]{35}' \
    -e 'github_pat_[A-Za-z0-9_]{20,}' -e 'sk-(live|test)-[A-Za-z0-9]{20,}' \
    "$r" | wc -l)"
done
```

Result: compliance 1, legal 0, data 0, infrastructure 23.

## E7 — The 23 infrastructure matches are untracked cache

```sh
cd jolarca-infrastructure
git ls-files 'ansible/.ansible' | wc -l          # -> 0
git check-ignore -q ansible/.ansible && echo IGNORED
git ls-files | wc -l                             # -> 319 tracked files total
git ls-files -z | xargs -0 grep -lIE '<high-signal patterns>' | wc -l   # -> 0
```

Result: `ansible/.ansible` is gitignored with **0 tracked files**; the 23 matches
are upstream Ansible collection **test fixtures** (`community/general` and
`community/crypto` dummy PEM keys and Slack module docstrings). They were never
committed and therefore never public. Supports `report.md` §3.2 and §4.

This distinction is the whole finding: a whole-tree grep over a working directory
counts vendored and ignored content, while only tracked content was ever exposed.
Assessments that skip this step report 23 leaked private keys where there are none.

## E8 — The single compliance match is a planted dummy

```sh
cd jolarca-compliance
grep -rInE 'AKIA[A-Z0-9]{16}' --exclude-dir=.git . | cut -d: -f1,2
```

Result: `audits/internal/2026-08-initial-build-audit/AUDIT_REPORT.md:108`. Reading
that line shows evidence item **E14** of the audit: "gitleaks on planted dummies …
3/3 detected". A documented negative control, not a credential. Supports
`report.md` §3.3.

## E9 — Public repositories remain clean

```sh
cd jolarca && git ls-files -z | xargs -0 grep -InE '<high-signal patterns>' | wc -l   # -> 0
git ls-files secrets ssl | head        # -> secrets/encrypted/README.md only
for d in secrets ssl backups logs node_modules .idea; do
  git check-ignore -q "$d" && echo "$d IGNORED" || echo "$d NOT-ignored"
done
```

Result: `jolarca` 0 tracked secret matches; `ssl/`, `backups/`, `logs/`,
`node_modules/`, `.idea/` ignored; **`secrets/` NOT ignored** → action A6.
`jolarca-identity`: 0 literal secrets, 12 keyword matches all policy prose.
Supports `report.md` §4.

## E10 — Independent corroboration

`audits/internal/2026-08-initial-build-audit/AUDIT_REPORT.md`, items E11 (PII sweep
— "zero real PII"), E12 (`redact-pii.py --all` clean), E13 (`gitleaks detect` — no
leaks). A prior assessment by a different method reaching the same conclusion.
Supports `report.md` §3.3 and `decisions.md` D1.

## E11 — Negative control on the scanning method

The scanner used here is `jolarca-vendor/scripts/scan-secrets.sh`, whose own
negative control (`make selftest`) plants a synthetic credential and asserts the
scan rejects it. Result on 2026-09-27: **pass** — the gate fires.

This matters for interpreting every zero in this file. A clean scan is only
evidence if the scanner is known to detect a positive case; otherwise "0 findings"
means "not looking". The estate applies the same discipline at E14 of the 2026-08
audit.

## Hashing at closure

On closure, hash the signed versions of `report.md`, `timeline.md`,
`decisions.md` and this file:

```sh
cd jolarca-compliance && make hash-evidence && make verify-signatures
```

Do not hash while these files remain DRAFT.

## Proposed register row

For `incidents/register.md`, to replace the empty placeholder row. **Not applied** —
the register is a controlled record and the row should be committed together with
the signed decision.

```text
| INC-2026-01 | 2026-09-17 | High | Governance repositories publicly readable while
declared private (compliance, legal, data, infrastructure); contained 2026-09-25/26 |
No — verified 2026-09-28, see INC-2026-01/report.md §3 |
N/A — decision documented in incidents/2026/INC-2026-01-public-exposure-governance-repos/decisions.md |
N/A — Art. 34 not engaged | Open — pending A2, A3, A4, A5 |
2026/INC-2026-01-public-exposure-governance-repos/ |
```

The "Notified SA" cell uses the register's own field rule — a timestamp or
"N/A — decision documented in <link>" — rather than being left blank, because a
blank cell is indistinguishable from an unassessed one.
