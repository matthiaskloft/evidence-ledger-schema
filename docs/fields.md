# Field reference

This document lists every field of a record and of the ledger header. The [schema](../evidence-ledger.schema.json) is the normative source. [Ledger files](ledger-files.md) explains file shapes, quote hashing, and exports.

"Required" means required in every record. "If contestable" means required when `contestable` is `true`. Bibliographic identifier requirements apply to reference records only; analysis and code records instead require their artifact objects.

## Record

| Field | Required | Values | Meaning |
| --- | --- | --- | --- |
| `id` | yes | `R-` plus four or more digits | Unique ID of the record. |

## Claim

What is claimed, and where in the text.

| Field | Required | Values | Meaning |
| --- | --- | --- | --- |
| `claim_id` | yes | `C-` plus four or more digits | ID of the claim. Records backing the same claim share it. |
| `claim` | yes | text | The claim, in words. |
| `claim_type` | yes | `empirical`, `definition`, `method`, `background` | Kind of claim. Descriptive only. |
| `contestable` | yes | `true` or `false` | `true` means the claim needs full evidence: `quote`, `quote_hash`, and `justification`, plus the evidence location for its type. Use `true` unless the claim is clearly uncontested. Empirical and theoretical claims both count, for example a claim that another theory assumes something different. |
| `contestable_reason` | if `contestable` is `false` | text | Why the claim needs no full evidence. |
| `importance` | no | `critical`, `substantial`, `supporting` | How much the work depends on the claim. Omitted means not assessed. Records with the same `claim_id` must agree. |
| `importance_reason` | no, needs `importance` | text | Why the work depends on the claim to this degree. |
| `anchor` | yes | object | Finds the claim in the text. Needs `marker` or `exact`. |
| `anchor.marker` | one of the two | text | An ID marker placed in the text. |
| `anchor.exact` | one of the two | text | The exact wording of the claim in the text. |
| `anchor.prefix`, `anchor.suffix` | no | text | Text right before or after `exact`, to tell repeated passages apart. |

## Source

Which work is cited. A source can be any document, such as an article, a book, an internal report, or a preregistration. Use `no_identifier_reason` when it has no DOI, ISBN, or URL.

| Field | Required | Values | Meaning |
| --- | --- | --- | --- |
| `key` | yes | text | Citation key for a reference, or a local identifier for an analysis or implementation. |
| `doi` | one of the four | `10.` DOI | DOI of the source. |
| `isbn` | one of the four | ISBN | ISBN of the source. |
| `url` | one of the four | `http(s)://` link | Stable link, for example to a repository or archive. |
| `no_identifier_reason` | one of the four | text | Why the source has no DOI, ISBN, or URL. |
| `zotero_link` | no | `zotero://` link | Link to the item in Zotero. |

## Evidence

Where the source backs the claim, and how.

| Field | Required | Values | Meaning |
| --- | --- | --- | --- |
| `locator` | if contestable reference | object | Place in the source. Needs at least one of `page`, `section`, `figure`, or `table`. |
| `locator.page` | one of the four | number or text | Page, for example `4` or `"e12"`. |
| `locator.section`, `locator.figure`, `locator.table` | one of the four | text | Section, figure, or table. |
| `locator.chunk` | no | `index`, `sha256`, optional `attachment` | Lookup hint into a full-text index. Dropped from exports. |
| `quote` | if contestable | text | Exact reference passage, analysis result excerpt (a number or table row is valid), or code excerpt. |
| `quote_prefix`, `quote_suffix` | no, need `quote` | text | Source text right before or after the quote, to tell repeated passages apart. Removed from masked and locator exports. |
| `quote_focus` | no, needs `quote` | text | The phrase within `quote` that carries the claim. Occurs exactly once, covers whole words, at most 25 words. |
| `quote_hash` | if contestable | `sha256-n2:` plus 64 hex digits | Hash of the normalized quote, so the quote can be checked without being shared. See [quote hashing](ledger-files.md#quote-hashing). |
| `relation` | yes | `supports`, `partially_supports`, `background`, `method`, `contrasts` | How the source relates to the claim. Contradicting evidence is recorded as `contrasts`, not dropped. |
| `justification` | if contestable | text | Why the passage, result, or implementation backs the claim. |
| `note` | no | text | Free comment. Exported, so never source text. |

## Retrieval

How the source was found and read.

| Field | Required | Values | Meaning |
| --- | --- | --- | --- |
| `retrieved_via` | yes | `zotero-fulltext`, `pdf`, `web`, `human`, `memory`, `analysis_output`, `source_code` | How the quote was obtained. `memory` flags a quote that was not read from the source. |
| `found_via.route` | if `found_via` is present | `memory`, `web_search`, `database_search`, `cited_in`, `coauthor`, `other` | How the source was found. |
| `found_via.source` | no | text | The citing work, search query, or a note. |

## Provenance

Who wrote the record, and when.

| Field | Required | Values | Meaning |
| --- | --- | --- | --- |
| `provenance.by_type` | yes | `human`, `agent` | Whether a person or an agent wrote the record. |
| `provenance.by` | yes | text | Name of the person, or of the agent tool, for example Claude Code. |
| `provenance.model` | if `by_type` is `agent` | text | Model and version. |
| `provenance.date` | yes | `YYYY-MM-DD` | Date the record was written. |
| `provenance.manuscript_rev` | no | text | Revision of the text the record refers to. |

## Status

| Field | Required | Values | Meaning |
| --- | --- | --- | --- |
| `withdrawn` | no | text | Set when the authors withdraw the citation: the reason. Review status is kept in a review log, not here. |


## Ledger header

Optional metadata at the top of a ledger.

| Field | Required | Values | Meaning |
| --- | --- | --- | --- |
| `schema_version` | yes | `X.Y.Z` | Schema version the records follow. |
| `work.title` | yes | text | Title of the work the ledger covers. |
| `work.type` | yes | `manuscript`, `software`, `dataset`, `other` | Kind of work. |
| `work.location` | no | text | File, repository, or URL of the work. |
| `description` | no | text | Short description of the ledger. |
| `created` | no | `YYYY-MM-DD` | Date the ledger was created. |
| `notes` | no | text | Free comment on the whole ledger. Exported, so never source text. |
| `level` | no | `full`, `masked`, `locator` | Export level. Omitted in a private working ledger. See [exports](ledger-files.md#exports). |
| `max_words` | no, needs `level: masked` | 1 to 25, or `null` | Word budget for masked quotes. `null` means default masking. |

## Rules beyond the schema

Some rules need checks beyond JSON Schema, such as a matching `quote_hash`. [Checking a ledger](checking-a-ledger.md) describes them.

## Evidence types and artifacts (v0.5.0)

Choose according to what supports the claim, regardless of file format. A notebook can supply a reference passage, an analysis result, or implementation code.

| Field | Required | Values | Meaning |
| --- | --- | --- | --- |
| `evidence_type` | no | `reference`, `analysis_output`, `source_code` | Omission means `reference`; validators need not insert the default. `reference` means what a source states, including official documentation; `analysis_output` means a computed or observed result; `source_code` means the implementation itself. |
| `analysis` | for `analysis_output` only | object | Report and optional generating script. Required even for noncontestable analysis records. |
| `analysis.report` | with `analysis` | artifact object | Primary evidence. Prefer the rendered report; a notebook or machine-readable output is valid when no rendered report exists. |
| `analysis.report.path` | unless `url` | nonblank text | Local file path relative to the ledger file, or absolute path. Exactly one of `path` or `url` is required. |
| `analysis.report.url` | instead of `path` | HTTPS URL | Specific report or output file; prefer a versioned or immutable link. |
| `analysis.report.sha256` | yes | 64 lowercase hex digits | SHA-256 of the complete file's exact bytes, without normalization or prefix. |
| `analysis.report.locator` | yes | nonblank text | Place within the report, such as a section and table row, CSV row and column, or notebook cell. No source excerpt here. |
| `analysis.script` | no | object | Generating script. If omitted, the report must identify its source script. |
| `analysis.script.path` | unless `url` | nonblank text | Local script path, resolved like the report path. Exactly one of `path` or `url` is required. |
| `analysis.script.url` | instead of `path` | HTTPS URL | Specific generating script, preferably pinned to a commit or archive version. |
| `analysis.script.sha256` | no | 64 lowercase hex digits | Optional hash of the script's exact bytes. |
| `analysis.script.locator` | no | nonblank text | Location within the script, such as `estimate_treatment, lines 42–48` or a notebook cell ID. Location only, never a code excerpt. |
| `source_code` | for `source_code` only | artifact object | Implementation evidence; required even for noncontestable records. |
| `source_code.path` | unless `url` | nonblank text | Local code file path, resolved like the report path. Exactly one of `path` or `url` is required. |
| `source_code.url` | instead of `path` | HTTPS URL | Specific implementation file, preferably pinned to a commit. A repository homepage alone does not locate the file. |
| `source_code.sha256` | yes | 64 lowercase hex digits | Exact byte hash pinning the code file. |
| `source_code.locator` | yes | nonblank text | Symbol and optionally line range, for example `fit_model, lines 42–48`. No code excerpt here. |
| `derived_from` | no, analysis only | unique list of `R-` IDs | Evidence records used by this analysis; an empty list means no dependencies recorded, not that none exist. Check existence and cycles outside the schema. |

Analysis and code records use their artifact's locator; top-level `locator` is for references only. They need no bibliographic identifier or `no_identifier_reason`. Optional DOI, ISBN, or URL metadata may still identify an archived artifact. Their `retrieved_via` describes how evidence was read: use `analysis_output` or `source_code` for direct file inspection, or an existing route such as `pdf` or `web` where appropriate.

All types retain the contestability rules: contestable records need `quote`, `quote_hash`, and `justification`; noncontestable records need `contestable_reason`. Source excerpts belong only in the quote fields. Artifact objects cannot be mixed between types. Script links record provenance; they do not prove that a script produced the report.

### What `derived_from` means

`derived_from` links an analysis record to other evidence records used as inputs or premises. For example, `R-0001` records an estimate from study A, `R-0002` records an estimate from study B, and `R-0003` records a pooled estimate computed from those two estimates. The pooled-result record can contain:

```yaml
id: R-0003
evidence_type: analysis_output
derived_from: [R-0001, R-0002]
```

This is a partial record illustrating the links; the usual claim, report, excerpt, and provenance fields are still required. The values are record IDs in the same ledger, not file paths, citation keys, or claim IDs. Use `analysis.report` and `analysis.script` to locate the output and generating code. Merely citing a method or discussing related work does not make it an input to the analysis.

The field is optional and currently available only for `analysis_output`. Omission or an empty list means dependencies have not been recorded. IDs must be unique and resolve to existing records; self references and cycles are invalid. These links describe a dependency and do not prove that the script actually used it.

## Example values for every field

All values below are invented illustrations, not source evidence or resolvable citations. The rows show individual fields, not one record to copy: reference, analysis, and code fields belong to different evidence types, and `path` and `url` are alternatives. Object rows show their structure; the following rows illustrate every nested field. `HASH` stands for a computed 64-character lowercase SHA-256 digest and must be replaced before validation. `COMMIT` likewise stands for an actual pinned repository commit.

### Record fields

| Field | Example value | Context |
| --- | --- | --- |
| `id` | `R-0003` | This record's ID. |
| `claim_id` | `C-0002` | Shared by records about the same claim. |
| `claim` | `The estimated treatment effect was -0.25.` | Analysis claim. |
| `claim_type` | `empirical` | Describes the claim. |
| `contestable` | `true` | Requires full evidence. |
| `contestable_reason` | `Uncontested background terminology.` | Alternative example for a record with `contestable: false`. |
| `importance` | `critical` | The work depends on this claim. |
| `importance_reason` | `The main conclusion depends on this estimate.` | Explains the assessment. |
| `anchor` | `{exact: "The estimated treatment effect was -0.25."}` | Location in the manuscript. |
| `anchor.marker` | `claim-treatment-effect` | A marker placed next to the claim. |
| `anchor.exact` | `The estimated treatment effect was -0.25.` | Exact manuscript text. |
| `anchor.prefix` | `In our fitted model, ` | Text immediately before the exact anchor. |
| `anchor.suffix` | ` We next assessed uncertainty.` | Text immediately after it. |
| `key` | `treatment-analysis` | Local analysis identifier; use a citation key for references. |
| `doi` | `10.12345/example` | Illustrative syntax only; reference identifier. |
| `isbn` | `978-0-00-000000-2` | Invented illustrative book identifier. |
| `url` | `https://example.org/manual/v1/` | Reference URL or optional artifact archive metadata. |
| `no_identifier_reason` | `Internal report with no public identifier.` | Alternative to DOI, ISBN, or URL for a reference. |
| `zotero_link` | `zotero://select/library/items/ABCD1234` | Illustrative local library link. |
| `locator` | `{page: 4, table: "2"}` | Reference location; artifact records use nested locators instead. |
| `locator.page` | `4` | Reference page. |
| `locator.section` | `Results` | Reference section. |
| `locator.figure` | `1b` | Reference figure. |
| `locator.table` | `2` | Reference table. |
| `locator.chunk` | `{attachment: ABCD1234, index: 7, sha256: HASH}` | Optional reference lookup hint; removed from exports. |
| `locator.chunk.attachment` | `ABCD1234` | Attachment key. |
| `locator.chunk.index` | `7` | Zero-based index. |
| `locator.chunk.sha256` | `HASH` | Hash for the indexed chunk. |
| `quote` | `estimate = -0.25` | Exact result excerpt. |
| `quote_prefix` | `Treatment model: ` | Exact source text immediately before the excerpt, if present. |
| `quote_suffix` | `; standard error = 0.08` | Exact source text immediately after it, if present. |
| `quote_focus` | `-0.25` | One whole whitespace-delimited word in this quote. |
| `quote_hash` | `sha256-n2:HASH` | Compute from the normalized full quote, not the file. |
| `relation` | `supports` | How this evidence relates to the claim. |
| `justification` | `The located result gives the claimed estimate.` | Explains the support without copying source text. |
| `note` | `Check the sensitivity analysis before submission.` | Author comment, not source text. |
| `retrieved_via` | `analysis_output` | For direct inspection of this result. |
| `found_via` | `{route: coauthor, source: "Suggested during methods review"}` | Discovery metadata. |
| `found_via.route` | `coauthor` | How the source was found. |
| `found_via.source` | `Suggested during methods review` | Discovery context. |
| `provenance` | `{by_type: human, by: "Example author", date: "2026-11-05"}` | Who wrote the record. |
| `provenance.by_type` | `human` | Alternatively `agent`. |
| `provenance.by` | `Example author` | Person or agent tool name. |
| `provenance.model` | `example-model-v1` | Required for `by_type: agent`; illustrative model label only. |
| `provenance.date` | `"2026-11-05"` | Quoted date string. |
| `provenance.manuscript_rev` | `draft-3` | Manuscript revision. |
| `withdrawn` | `Superseded after correcting the input data.` | Only on a withdrawn record. |
| `evidence_type` | `analysis_output` | Alternatives: `reference` (also the omission default) and `source_code`. |
| `analysis` | `{report: {path: reports/treatment.html, sha256: HASH, locator: "Table 2"}}` | Analysis-only object. |
| `analysis.report` | `{path: reports/treatment.html, sha256: HASH, locator: "Table 2"}` | Primary evidence artifact. |
| `analysis.report.path` | `reports/treatment.html` | Local report; alternative to its URL. |
| `analysis.report.url` | `https://example.org/archive/v1/treatment.html` | Remote report; alternative to its path. |
| `analysis.report.sha256` | `HASH` | Hash of the complete report's exact bytes. |
| `analysis.report.locator` | `Table 2, treatment row, estimate column` | Result within the report. |
| `analysis.script` | `{path: analysis/treatment.py, locator: "estimate_treatment, lines 42–48"}` | Optional generating script. |
| `analysis.script.path` | `analysis/treatment.py` | Local script; alternative to its URL. |
| `analysis.script.url` | `https://github.com/example/project/blob/COMMIT/analysis/treatment.py` | Remote script at a pinned revision. |
| `analysis.script.sha256` | `HASH` | Optional exact file hash. |
| `analysis.script.locator` | `estimate_treatment, lines 42–48` | Optional function, cell, or line range. |
| `source_code` | `{path: src/model.py, sha256: HASH, locator: "fit_model, lines 42–48"}` | Alternative evidence object for `evidence_type: source_code`. |
| `source_code.path` | `src/model.py` | Local code; alternative to its URL. |
| `source_code.url` | `https://github.com/example/project/blob/COMMIT/src/model.py` | Remote code at a pinned revision. |
| `source_code.sha256` | `HASH` | Hash of the code file's raw contents, not the GitHub page. |
| `source_code.locator` | `fit_model, lines 42–48` | Symbol and line range. |
| `derived_from` | `[R-0001, R-0002]` | Analysis dependencies; those records must exist in this ledger. |

### Ledger header fields

These examples describe a masked export. In a working private ledger, omit `level` and `max_words`. Field names are relative to the header, which is stored under `ledger` in the file wrapper.

| Field | Example value | Context |
| --- | --- | --- |
| `schema_version` | `"0.5.0"` | Version used to validate the records. |
| `work` | `{title: "Treatment study", type: manuscript, location: manuscript.qmd}` | Work covered by the ledger. |
| `work.title` | `Treatment study` | Work title. |
| `work.type` | `manuscript` | Kind of work. |
| `work.location` | `manuscript.qmd` | File, repository, or URL of the work. |
| `description` | `Evidence for the treatment study manuscript.` | Ledger description. |
| `created` | `"2026-11-05"` | Quoted date string. |
| `notes` | `Prepared for co-author review.` | Ledger comment, never source text. |
| `level` | `masked` | Export level. |
| `max_words` | `10` | Masked quote budget; also permits `null` for default masking. |
