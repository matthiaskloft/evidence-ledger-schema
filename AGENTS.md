# Agent instructions

This repository owns the evidence ledger schema, independently of the MCP server.

- Keep changes to the schema minimal. Breaking changes need a new schema version.
- Update the schema `$id` and title, README and changelog together when changing versions. Coordinate private ledger headers and the development repository's specification copy.
- When a field or rule changes, update the docs that describe it: `docs/fields.md` (every field), `docs/ledger-files.md` (file shapes, hashing, exports), `docs/checking-a-ledger.md` (checks and test vectors) and, if affected, the README example and `docs/motivation.md` (field sources).
- The README is for schema users only; keep development and release instructions here.
- Install test dependencies with `python -m pip install -r requirements-test.txt`. Run `python -m unittest discover -s tests -v` and `python tools/check_public.py` before committing.
- Releases are a `schema-vX.Y.Z` tag and a GitHub release; there is no package publishing. Never create or push release tags without the user's approval. Server maintainers update their pinned copy explicitly.
- Decide the stable hosting namespace before changing `$id` in a future version.
- Keep private evidence ledgers under ignored `ledger/`. Never publish ledgers, verbatim source evidence or exports without explicit human approval. New scholarly citations need records in the private ledger; never fabricate source quotes.
- Enable `.githooks` as the hooks path (`git config core.hooksPath .githooks`). Never bypass the privacy hook.
- Resolve addressed PR review conversations.

## Evidence types and version coordination

- v0.5.0 introduces evidence types. Keep `evidence_type` optional; omission means `reference`. Choose `reference`, `analysis_output`, or `source_code` by what supports the claim, regardless of file format. Official package documentation is a reference.
- Prefer rendered reports for analysis evidence; scripts are optional provenance. Keep result and code excerpts in existing quote fields so privacy checks and export redaction cover them. Artifact locators, including optional `analysis.script.locator` for functions, cells, or line ranges, must contain locations, not excerpts.
- Each artifact or script uses exactly one of local `path` or HTTPS `url`. Remote links identify specific files, preferably at immutable revisions; never hash a hosting HTML wrapper instead of the file. Artifact hashes cover exact bytes. Never execute referenced scripts during evidence verification. Numerical and code excerpt checks must preserve signs, punctuation, and case.
- Before release, coordinate the MCP repository's pinned `schema/evidence-ledger.schema.json` and `docs/schema.md` with its maintainers. Keep the old pin until its implementation supports v0.5.0. Migrate private ledger headers only after validating their records; never publish their contents.
