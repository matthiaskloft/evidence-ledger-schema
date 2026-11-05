# Evidence ledger schema

[![Release](https://img.shields.io/github/v/release/matthiaskloft/evidence-ledger-schema?filter=schema-v*&label=schema)](https://github.com/matthiaskloft/evidence-ledger-schema/releases)
[![Licence: CC BY 4.0](https://img.shields.io/badge/licence-CC%20BY%204.0-blue)](LICENSE)

> **Under active development.** The schema may change in breaking ways between versions until v1.0. Pin the version you use.

**A simple, tool-independent format that links every claim in a text to the evidence that supports it.**

## What is a ledger?

A ledger is a running record, like an accounting book, where each entry is written down once and can be checked later. An evidence ledger is such a record for claims and their evidence: one entry for each claim in a text, saying which source backs it and where. Evidence can come from a reference document, an analysis result, or source code.

## Transparent citations with LLMs

With LLMs, citing is often unstructured and differs between tools. As a result, it is often unclear where a statement comes from, and citations are hard to check.

Many journals and universities ask authors to disclose where an LLM helped write a text. We think the more important question is whether each claim is backed by its source. The ledger answers both. For every citation, it records the claim, the source, the supporting passage with a short quote, and why the source is cited. It also notes whether a person or an agent wrote the record. A source can be any document, such as an article, a book, an internal report, or a preregistration.

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

**You do not need to fill in every field.** Many fields are optional, including `evidence_type` (omission means `reference`), `importance`, `found_via`, and `note`. Other fields are required only in certain cases, such as `provenance.model` when an agent wrote the record. Omit unused optional fields rather than adding empty values. The [field reference](docs/fields.md#required-and-optional-fields) explains the requirements.

A ledger is a list of records, with an optional header, kept next to the text it covers. It can be written as JSON, JSON Lines or YAML.

## Analysis and implementation evidence

Schema v0.5.0 also supports analysis results and source code. Optional `evidence_type` selects what supports the claim: `reference` (the default, including official documentation), `analysis_output` (a computed or observed result), or `source_code` (the implementation itself). Choose by the evidence's role, regardless of file format. Existing server releases may support only earlier schema versions.

This invented analysis record points to a result file containing exactly `estimate = -0.25` followed by a newline. Prefer a rendered report when available; record the script separately:

```yaml
- id: R-0002
  claim_id: C-0002
  claim: "The estimated treatment effect was -0.25."
  claim_type: empirical
  contestable: true
  anchor: {exact: "The estimated treatment effect was -0.25."}
  key: treatment-analysis
  evidence_type: analysis_output
  analysis:
    report:
      path: reports/treatment.txt
      sha256: 3cc5d9484961a09579bdade694a64ca8d3b5ad66520dd930ec779d68bdee77bd
      locator: "Line 1, estimate"
    script:
      path: analysis/treatment.py
      locator: "estimate_treatment, lines 42–48"
  quote: "estimate = -0.25"
  quote_hash: sha256-n2:886d06ba0a15eef1bbd19c7eb9ffdd97669df64be2183ff8eec845ba692ee410
  relation: supports
  justification: "The result gives the claimed estimate."
  retrieved_via: analysis_output
  provenance: {by_type: human, by: Example author, date: "2026-11-05"}
```

For implementation evidence, use `evidence_type: source_code` with `source_code: {path: src/model.py, sha256: <64 lowercase hex digits>, locator: "fit_model, lines 42–48"}` instead of `analysis`. Put the exact code excerpt in `quote`. Each report, script, or code artifact accepts exactly one of local `path` or HTTPS `url`. A GitHub URL should identify a specific file at a pinned commit, rather than the repository homepage. Hash the raw file contents, not the GitHub page. A file hash verifies identity; it does not establish correctness or prove that a script generated a report. See the [field reference](docs/fields.md#evidence-types-and-artifacts-v050) and [verification rules](docs/checking-a-ledger.md#additional-v050-checks).

## Getting started

1. When you cite a source, write one record per claim and source into the ledger.
2. Validate the records against [evidence-ledger.schema.json](evidence-ledger.schema.json) with any JSON Schema 2020-12 validator.
3. Check the ledger with your own tools, following [Checking a ledger](docs/checking-a-ledger.md), or use the [evidence-ledger-mcp server](https://github.com/matthiaskloft/evidence-ledger-mcp).

Quotes from copyrighted sources belong in a private ledger. A public ledger should keep only locators and hashes.

## Learn more

- [Motivation](docs/motivation.md): the full argument, use cases, and where the fields come from
- [Field reference](docs/fields.md): every field, grouped by claim, source, evidence, and provenance
- [Ledger files](docs/ledger-files.md): file shapes, quote hashing, and exports
- [Checking a ledger](docs/checking-a-ledger.md): how to build your own checks
- [Versions](docs/versioning.md) and [changelog](CHANGELOG.md)

## Contributing

Ideas, questions, and feedback are welcome. [Open an issue](https://github.com/matthiaskloft/evidence-ledger-schema/issues/new), or see [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

The schema is licensed under [CC BY 4.0](LICENSE), with attribution to Matthias Kloft and Julien P. Irmer. The licence does not cover ledger contents or third-party source material. The MCP server is a separate project with its own MIT licence.
