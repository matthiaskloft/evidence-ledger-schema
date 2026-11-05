# Ledger files

This document describes how a ledger file is put together: its shapes, how quotes are hashed, and how ledgers are exported. The [field reference](fields.md) explains each field.

## File shapes

[evidence-ledger.schema.json](../evidence-ledger.schema.json) (JSON Schema 2020-12) describes one record and, in `$defs/header`, the ledger header. A ledger is a list of records, kept next to the work it covers. It can start with a header that describes the work and the schema version.

The schema validates parsed records, so a ledger can be JSON, JSON Lines, or YAML. The file takes one of these shapes:

- JSON or YAML: an object `{"ledger": <header>, "records": [<record>, ...]}`.
- JSON Lines: the first line is `{"ledger": <header>}`; every following line is one record.
- A plain list of records, without header, stays valid.

In YAML, quote dates (`date: "2026-10-30"`), since unquoted dates are not read as text.

## Quote hashing

`quote_hash` is `sha256-n2:` plus the SHA-256 of the UTF-8 quote after normalization n2: Unicode NFKC, casefold, NFKC again, keep only letters and digits. The hash then survives differences between copies of a source, such as whitespace, hyphenation, and quote styles. Legacy `sha256-n1:` hashes omit the second NFKC and remain valid and checkable.

## Exports

An exported ledger records its export level in the header. `level` is `full`, `masked`, or `locator`. At the masked level, `max_words` sets the word budget for masked quotes; `null` means default masking. How quotes are masked is up to the exporting tool.

Source text belongs only in `quote`, `quote_prefix`, `quote_suffix`, and `quote_focus`. Masked and locator exports remove or shorten these fields and drop `locator.chunk`. A public ledger then keeps only locators and hashes. `note` and `notes` are exported unchanged, so they must never contain source text.

## Checks beyond the schema

Some rules span several fields, such as a matching quote hash and a unique whole-word `quote_focus`. JSON Schema cannot express them. [Checking a ledger](checking-a-ledger.md) describes these checks.

## Analysis and code artifacts

In v0.5.0, optional `evidence_type` selects `reference` (the default), `analysis_output`, or `source_code`. File shapes are unchanged. Analysis records store their primary evidence in `analysis.report`, with an optional `analysis.script`; code records use `source_code`. Each primary artifact has exactly one of `path` or `url`, plus `sha256` and `locator`. Scripts also use exactly one of `path` or `url`, and may include a `locator` naming a function, notebook cell, or line range. Script locators are retained in exports and must not contain code excerpts. Prefer a rendered report to its generating script for analysis evidence.

Resolve relative artifact paths against the directory containing the ledger file, not the current working directory or manuscript. An absolute path is also valid. Moving a ledger may require updating its paths. Paths are file references, never commands or instructions to fetch resources. A checker must obtain access to files explicitly and safely.

For remote files, use `url` with an HTTPS link to the specific file. Prefer a commit-pinned GitHub file link or an immutable archive version; a repository homepage alone is insufficient. For GitHub browser file links, obtain the corresponding raw file at the same revision before hashing. Hash the underlying file contents, never the GitHub HTML wrapper. For a rendered HTML report, the HTML report itself is the artifact. Resolve redirects and HTTP transfer/content encodings before hashing the resulting file bytes; do not decode text or convert newlines. URL fragments are navigation hints, not part of the hashed bytes. Record locations within the file in `locator`. Network retrieval is a separate, explicitly authorized step; a checker can use a trusted local copy and report unavailable artifacts as “not checked”.

Artifact `sha256` is the SHA-256 of the entire file read as bytes: no decoding, Unicode normalization, newline conversion, or prefix. The same rule applies to optional script hashes. Re-rendering a report can change its byte hash even when results remain the same. A hash verifies file identity, not correctness or reproducibility.

`quote` contains the exact relevant result or code excerpt. Keep its existing normalized `quote_hash`, but verify numerical and code excerpts exactly: normalization discards signs, decimal points, operators, and case. The artifact hash complements, rather than replaces, excerpt verification.

Export rules apply equally to reference text, result excerpts, and code excerpts. Remove or shorten quote fields as specified above; keep artifact paths or URLs, locators, hashes, and dependency IDs. Never paste excerpts into locators, keys, notes, or justifications to evade redaction. Paths can disclose private directory names, and URLs can contain credentials or private access tokens. Never store authenticated or signed access URLs in the ledger; use a stable URL without credentials and authenticate separately. As with other metadata, inspect export metadata before sharing. Masked and locator exports are redacted views, not complete contestable records; checks needing omitted excerpts must report “not checked”, not fail solely because of redaction or claim a match.

Masked and locator exports retain `quote_hash` for the original full excerpt; never replace it with a hash of the shortened text. Remove `quote_prefix`, `quote_suffix`, and `quote_focus` from both export levels. A masked `quote` may be shortened according to the export budget; a locator export removes `quote` entirely. A checker without the original full excerpt reports hash and focus verification as “not checked”, including when a shortened quote remains.
