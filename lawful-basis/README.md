# Lawful basis & consent registry

The authoritative link between what users were shown, when, and what the
product database records (`ConsentRecord`). Any change to consent UX must
update this registry **in the same release**.

| Path | Content |
|---|---|
| `consent-text/<lang>/` | Versioned consent strings: `lt/ lv/ et/ en/ ru/` |
| `consent-versions.md` | Which version was shown when (deployment ledger) |
| `legitimate-interest-assessments/` | LIA per Art. 6(1)(f) use case |

Rules:

1. Consent strings are immutable once shipped; new text = new version ID.
2. Every version ID maps 1:1 to `ConsentRecord.consent_version` values.
3. Marketing consent is separate from contractual processing — never bundle.
4. Withdrawal must be as easy as grant; withdrawal paths documented per text.
