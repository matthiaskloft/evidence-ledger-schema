# Evidence ledger schema

[![Release](https://img.shields.io/github/v/release/matthiaskloft/evidence-ledger-schema?filter=schema-v*&label=schema)](https://github.com/matthiaskloft/evidence-ledger-schema/releases)
[![Licence: CC BY 4.0](https://img.shields.io/badge/licence-CC%20BY%204.0-blue)](LICENSE)

> **Under active development.** The schema may change in breaking ways between versions until v1.0. Pin the version you use.

**A simple, tool-independent format that links every claim in a text to the evidence that supports it.**

## Transparent citations with LLMs

With LLMs, citing is often unstructured and differs between tools. As a result, it is often unclear where a statement comes from, and citations are hard to check.

Many journals and universities ask authors to disclose where an LLM helped write a text. We think the more important question is whether each claim is backed by its source. The ledger answers both. For every citation, it records the claim, the source, the supporting passage with a short quote, and why the source is cited. It also notes whether a person or an agent wrote the record.

This makes citations transparent. Co-authors, reviewers or a script can check each claim against its source, whichever tool wrote the text. If a text meets this standard, it matters less who drafted it. The author stays responsible for every claim.

The idea follows Moravcsik's *active citation* (2014): contestable claims come with the evidence that supports them.

## Use cases

- **Authors** check their own manuscripts. Every citation can be traced to its source, whether a journal asks for it or not.
- **Journals** could require a ledger with a submission, either this schema or their own standard built on it.
- **Universities** could ask for a ledger with a thesis, so supervisors can check the citations. The schema can also be used in teaching, to discuss transparent research with AI.

## What a record looks like

One record links one claim to one source:

```yaml
- id: R-0001
  claim_id: C-0001
  claim: "Keeping a ledger cut unchecked citations from 40 to 3 per manuscript."
  claim_type: empirical
  contestable: true
  anchor: {exact: "cut unchecked citations from 40 to 3"}
  key: exampleLedgerStudy2026
  no_identifier_reason: "Invented source for this example"
  locator: {page: 4}
  quote: "Ledger records reduced unchecked citations from 40 to 3 per manuscript"
  quote_hash: sha256-n2:3b8d67a25018dccc865ee88b24c10aa4a5b553e41ff28ebc46936a71eee7db3c
  relation: supports
  justification: "The quoted sentence states both counts."
  retrieved_via: pdf
  provenance: {by_type: agent, by: Claude Code, model: claude-opus-5-5, date: "2026-10-30"}
```

| Group | Key fields |
| --- | --- |
| Claim | `claim`, `claim_id`, `claim_type`, `anchor` (where the claim is in the text) |
| Source | `key`, and a `doi`, `isbn` or `url` |
| Evidence | `locator`, `quote`, `quote_hash`, `relation`, `justification` |
| Provenance | who wrote the record, a person or an agent, which model, and when |

A ledger is a list of records, with an optional header, kept next to the text it covers. It can be written as JSON, JSON Lines or YAML.

## Getting started

1. When you cite a source, write one record per claim and source into the ledger.
2. Validate the records against [evidence-ledger.schema.json](evidence-ledger.schema.json) with any JSON Schema 2020-12 validator.
3. Check the ledger with your own tools, following [Checking a ledger](docs/checking-a-ledger.md), or use the [evidence-ledger-mcp server](https://github.com/matthiaskloft/evidence-ledger-mcp).

Quotes from copyrighted sources belong in a private ledger. A public ledger should keep only locators and hashes.

## Learn more

- [Motivation](docs/motivation.md): the full argument, use cases, and where the fields come from
- [Format](docs/format.md): header, file formats, hashing, and exports in detail
- [Checking a ledger](docs/checking-a-ledger.md): how to build your own checks
- [Versions](docs/versioning.md) and [changelog](CHANGELOG.md)

## Contributing

Ideas, questions, and feedback are welcome. [Open an issue](https://github.com/matthiaskloft/evidence-ledger-schema/issues/new), or see [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

The schema is licensed under [CC BY 4.0](LICENSE), with attribution to Matthias Kloft and Julien P. Irmer. The licence does not cover ledger contents or third-party source material. The MCP server is a separate project with its own MIT licence.
