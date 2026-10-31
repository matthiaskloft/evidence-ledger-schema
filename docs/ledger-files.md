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
