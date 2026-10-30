# Evidence ledger schema

A standalone JSON Schema format for records linking a claim in a work to its source evidence. Any tool can produce or validate a ledger; the schema does not require an MCP server.

**Current release: [schema v0.4.0](https://github.com/matthiaskloft/evidence-ledger-schema/releases/tag/schema-v0.4.0).**

The [evidence-ledger-mcp server](https://github.com/matthiaskloft/evidence-ledger-mcp) is a separate implementation with its own versions and MIT licence. This schema is licensed under **CC BY 4.0**, with attribution to Matthias Kloft; see [LICENSE](LICENSE). The licence does not cover ledger contents or third-party source material.

## Files and validation

[evidence-ledger.schema.json](evidence-ledger.schema.json) validates an individual record. Its `$defs/header` validates ledger metadata. A record links a claim and anchor to a source key, evidence locator, quote and hash, relation, justification and provenance. Contestable claims require full evidence; other claims require a reason.

The format is independent of serialization. JSON and YAML ledgers may contain an object with `ledger` and `records`; JSON Lines ledgers start with a `ledger` header line followed by one record per line. Headerless record lists are also supported by the specification. Validate parsed records individually with a JSON Schema 2020-12 validator, and validate an optional header against `$defs/header`.

Cross-field semantic rules, such as a unique whole-word `quote_focus` and verifying a quote hash, require additional application checks beyond JSON Schema validation. Schema v0.4.0 defines n2 hashes and keeps legacy n1 hashes checkable. See the field descriptions and [CHANGELOG.md](CHANGELOG.md).

## Versions and history

This repository was extracted from the original server repository using `git subtree split --prefix=schema`. It preserves the schema's commit history and the published `schema-v0.2.0`, `schema-v0.3.0` and `schema-v0.4.0` snapshots. Original releases in the server repository remain historical records.

Schema v0.4.0 is unchanged by the move. Its existing `$id` retains the original namespace to avoid silently changing a published schema. Use the versioned GitHub tag to retrieve this release; the `$id` is an identifier, not a promise that a hosted schema endpoint is available. Decide the stable hosting namespace before changing the identifier in a future version.

## Development and releases

```bash
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests -v
python tools/check_public.py
```

Enable the privacy hook with `git config core.hooksPath .githooks`. Private ledgers belong in the ignored `ledger/` directory and must never be published.

Future schema changes are developed here, with a version update to `$id`, `title`, the changelog and documentation. Coordinate the development repository's specification and private ledger headers when changing the schema version. Publish a `schema-vX.Y.Z` tag and a GitHub release after user approval; this repository has no Python package or PyPI publishing workflow. Server maintainers explicitly update their pinned vendored copy when adopting a schema release.
