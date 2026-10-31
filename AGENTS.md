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
