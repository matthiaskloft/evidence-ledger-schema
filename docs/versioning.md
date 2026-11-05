# Schema versions

Each release is published as a `schema-vX.Y.Z` tag with a GitHub release; see [CHANGELOG.md](../CHANGELOG.md). Releases `schema-v0.2.0` to `schema-v0.4.0` were first published in the evidence-ledger-mcp repository and are preserved here unchanged.

The `$id` of schema v0.4.0 keeps its original namespace. It is an identifier, not a hosted endpoint: retrieve the schema from the versioned tag.

Version 0.5.0 uses this repository's versioned raw GitHub namespace for `$id`: `https://raw.githubusercontent.com/matthiaskloft/evidence-ledger-schema/schema-v0.5.0/evidence-ledger.schema.json`. It resolves when the release tag exists; until release, use the checked-out schema. No GitHub Pages deployment or release attachment is required.

To migrate from v0.4.0, remove reserved `evidence_kind`; map `literature` to `evidence_type: reference` (or omit it). Convert reserved `analysis_output` records to the report structure and supply exact file hashes. Replace any free-form `derived_from` entries with record IDs and use it only for analysis records. Existing reference records without reserved fields remain valid. Change a private ledger's header to `0.5.0` only after all its records pass the new checks; do not bulk relabel older ledgers.

Server maintainers must explicitly update their pinned schema and implementation before accepting the new evidence types. A schema update alone does not add server support.
