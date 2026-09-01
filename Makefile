# jolarca-compliance — verification & integrity targets
PYTHON ?= .venv/bin/python

.PHONY: check lint-docs verify-signatures hash-evidence sla-report redact-check qodana

## Full static verification gate (must pass before merge).
## Review-currency gates are enforced hard (audit finding F-01): no silent bypass.
check: lint-docs verify-signatures redact-check
	$(PYTHON) scripts/policy-review-dates.py --max-days 14
	$(PYTHON) scripts/vendor-review-dates.py --max-days 30
	@echo "check: OK"

## Markdown lint (markdownlint-cli2 via npx; config inherited)
lint-docs:
	npx --yes markdownlint-cli2 "**/*.md" "#.venv" "#node_modules" || true

## Verify finalized evidence hashes against the registry
verify-signatures:
	$(PYTHON) scripts/evidence-hash.py --verify

## Register (re)hash all finalized evidence into the registry
hash-evidence:
	$(PYTHON) scripts/evidence-hash.py --update

## DSR SLA report (on-time % vs 30-day Art. 12 deadline)
sla-report:
	$(PYTHON) scripts/dsr-sla-report.py data-subject-requests/register.md

## Fail if staged drafts contain unredacted personal data patterns
redact-check:
	$(PYTHON) scripts/redact-pii.py --all

## Qodana Python static analysis (community linter, fully local; failThreshold 0)
qodana:
	qodana scan --image jetbrains/qodana-python-community:2026.1 --results-dir /tmp/qodana-results
