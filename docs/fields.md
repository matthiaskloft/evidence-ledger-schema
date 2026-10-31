# Field reference

This document lists every field of a record and of the ledger header. The [schema](../evidence-ledger.schema.json) is the normative source. [Ledger files](ledger-files.md) explains file shapes, quote hashing, and exports.

"Required" means required in every record. "If contestable" means required when `contestable` is `true`.

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
| `contestable` | yes | `true` or `false` | `true` means the claim needs full evidence: `locator`, `quote`, `quote_hash`, and `justification`. Use `true` unless the claim is clearly uncontested. |
| `contestable_reason` | if `contestable` is `false` | text | Why the claim needs no full evidence. |
| `importance` | no | `critical`, `substantial`, `supporting` | How much the work depends on the claim. Omitted means not assessed. Records with the same `claim_id` must agree. |
| `importance_reason` | no, needs `importance` | text | Why the work depends on the claim to this degree. |
| `anchor` | yes | object | Finds the claim in the text. Needs `marker` or `exact`. |
| `anchor.marker` | one of the two | text | An ID marker placed in the text. |
| `anchor.exact` | one of the two | text | The exact wording of the claim in the text. |
| `anchor.prefix`, `anchor.suffix` | no | text | Text right before or after `exact`, to tell repeated passages apart. |

## Source

Which work is cited.

| Field | Required | Values | Meaning |
| --- | --- | --- | --- |
| `key` | yes | text | Citation key, for example from BibTeX. |
| `doi` | one of the four | `10.` DOI | DOI of the source. |
| `isbn` | one of the four | ISBN | ISBN of the source. |
| `url` | one of the four | `http(s)://` link | Stable link, for example to a repository or archive. |
| `no_identifier_reason` | one of the four | text | Why the source has no DOI, ISBN, or URL. |
| `zotero_link` | no | `zotero://` link | Link to the item in Zotero. |

## Evidence

Where the source backs the claim, and how.

| Field | Required | Values | Meaning |
| --- | --- | --- | --- |
| `locator` | if contestable | object | Place in the source. Needs at least one of `page`, `section`, `figure`, or `table`. |
| `locator.page` | one of the four | number or text | Page, for example `4` or `"e12"`. |
| `locator.section`, `locator.figure`, `locator.table` | one of the four | text | Section, figure, or table. |
| `locator.chunk` | no | `index`, `sha256`, optional `attachment` | Lookup hint into a full-text index. Dropped from exports. |
| `quote` | if contestable | text | Verbatim passage from the source. |
| `quote_prefix`, `quote_suffix` | no, need `quote` | text | Source text right before or after the quote, to tell repeated passages apart. |
| `quote_focus` | no, needs `quote` | text | The phrase within `quote` that carries the claim. Occurs exactly once, covers whole words, at most 25 words. |
| `quote_hash` | if contestable | `sha256-n2:` plus 64 hex digits | Hash of the normalized quote, so the quote can be checked without being shared. See [quote hashing](ledger-files.md#quote-hashing). |
| `relation` | yes | `supports`, `partially_supports`, `background`, `method`, `contrasts` | How the source relates to the claim. Contradicting evidence is recorded as `contrasts`, not dropped. |
| `justification` | if contestable | text | Why the passage backs the claim. |
| `note` | no | text | Free comment. Exported, so never source text. |

## Retrieval

How the source was found and read.

| Field | Required | Values | Meaning |
| --- | --- | --- | --- |
| `retrieved_via` | yes | `zotero-fulltext`, `pdf`, `web`, `human`, `memory` | How the quote was obtained. `memory` flags a quote that was not read from the source. |
| `found_via.route` | no | `memory`, `web_search`, `database_search`, `cited_in`, `coauthor`, `other` | How the source was found. |
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

## Status and reserved fields

| Field | Required | Values | Meaning |
| --- | --- | --- | --- |
| `withdrawn` | no | text | Set when the authors withdraw the citation: the reason. Review status is kept in a review log, not here. |
| `evidence_kind` | no | `literature`, `analysis_output` | Reserved for claims about the authors' own results. |
| `derived_from` | no | list of text | Reserved for the authors' own inferences. |

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
