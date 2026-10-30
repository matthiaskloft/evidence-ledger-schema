# Evidence ledger schema

A standalone JSON Schema format for records linking a claim in a work to its source evidence. Any tool can produce or validate a ledger; the schema does not require an MCP server.

**Current release: [schema v0.4.0](https://github.com/matthiaskloft/evidence-ledger-schema/releases/tag/schema-v0.4.0).**

The [evidence-ledger-mcp server](https://github.com/matthiaskloft/evidence-ledger-mcp) is a separate implementation with its own versions and MIT licence. This schema is licensed under **CC BY 4.0**, with attribution to Matthias Kloft; see [LICENSE](LICENSE). The licence does not cover ledger contents or third-party source material.

## Files and validation

[evidence-ledger.schema.json](evidence-ledger.schema.json) validates an individual record. Its `$defs/header` validates ledger metadata. A record links a claim and anchor to a source key, evidence locator, quote and hash, relation, justification and provenance. Contestable claims require full evidence; other claims require a reason.

The format is independent of serialization. JSON and YAML ledgers may contain an object with `ledger` and `records`; JSON Lines ledgers start with a `ledger` header line followed by one record per line. Headerless record lists are also supported by the specification. Validate parsed records individually with a JSON Schema 2020-12 validator, and validate an optional header against `$defs/header`.

Cross-field semantic rules, such as a unique whole-word `quote_focus` and verifying a quote hash, require additional application checks beyond JSON Schema validation. Schema v0.4.0 defines n2 hashes and keeps legacy n1 hashes checkable. See the field descriptions and [CHANGELOG.md](CHANGELOG.md).

## Versions

Each release is published as a `schema-vX.Y.Z` tag with a GitHub release; see [CHANGELOG.md](CHANGELOG.md). Releases `schema-v0.2.0` to `schema-v0.4.0` were first published in the evidence-ledger-mcp repository and are preserved here unchanged.

The `$id` of schema v0.4.0 keeps its original namespace. It is an identifier, not a hosted endpoint: retrieve the schema from the versioned tag.
