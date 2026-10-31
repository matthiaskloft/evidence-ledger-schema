# Ledger format

This document describes the format in detail. The [README](../README.md) gives an overview.

[evidence-ledger.schema.json](../evidence-ledger.schema.json) (JSON Schema 2020-12) describes one record and, in `$defs/header`, the ledger header. A ledger is a list of records, kept next to the work it covers.

**Header.** A ledger can start with a header that records `schema_version`, the `work` it covers (`title`, `type`: `manuscript`, `software`, `dataset` or `other`, and an optional `location`), and optional `description`, `created` and `notes`. The ledger file then takes one of these shapes:

- JSON or YAML: an object `{"ledger": <header>, "records": [<record>, ...]}`.
- JSON Lines: the first line is `{"ledger": <header>}`; every following line is one record.
- A plain list of records, without header, stays valid.

**File format.** The schema is format-neutral: it validates parsed records, so a ledger can be JSON, JSON Lines or YAML. When writing YAML, quote dates (`date: "2026-10-30"`), since unquoted dates are not read as text.

Each record contains the groups below. The [field reference](fields.md) lists every field.

- **Claim:** `claim`, `claim_id` (records backing the same claim share it), `claim_type`, and an `anchor` that finds the claim in the work (an ID marker, or the exact text).
- **Source:** a citation `key`, and a `doi`, `isbn` or `url` (or `no_identifier_reason`).
- **Evidence:** `locator` (page, section, figure or table), `quote`, `quote_hash`, `relation` (`supports`, `partially_supports`, `background`, `method`, `contrasts`), a `justification` and an optional `note`.
- **Provenance:** who wrote the record (person or agent, and which model) and when.

Every claim counts as `contestable` by default and then needs locator, quote, hash and justification. Marking a claim as not contestable needs a `contestable_reason`. Evidence that contradicts a claim is recorded with `relation: contrasts`, not dropped.

`note` (per record) and `notes` (in the header) are free-text comments, the JSON counterpart of comments in a YAML file. They are exported with the ledger, so they must never contain source text; source text belongs only in `quote`, `quote_prefix`, `quote_suffix` and `quote_focus`.

`quote_hash` is `sha256-n2:` plus the SHA-256 of the UTF-8 quote after normalization n2: Unicode NFKC, casefold, NFKC again, keep only letters and digits. Legacy `sha256-n1:` hashes omit the second NFKC and remain valid and checkable. The hash then survives differences between copies of a source, such as whitespace, hyphenation and quote styles.

`quote_focus` optionally marks the phrase within `quote` that carries the claim. It must occur exactly once, cover whole whitespace-delimited words, and contain at most 25 words. It is source text and is removed from masked and locator exports.

An exported ledger records its export level in the header: `level` is `full`, `masked` or `locator`, and `max_words` (1–25, masked level only) is the word budget for masked quotes; `null` means default masking. How quotes are masked is up to the exporting tool.

Cross-field rules, such as a unique whole-word `quote_focus` and a matching quote hash, need checks beyond JSON Schema validation.
