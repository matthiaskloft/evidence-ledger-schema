# Motivation

This document explains why we developed the evidence ledger and how we think it can be used. The [README](../README.md) gives the short version.

## The problem

LLMs make writing faster, but they also change how sources enter a text. With LLMs, citing is often unstructured. One tool leaves a comment, another writes a bibliography entry, and a third cites from memory without any record. How sources are handled depends on the model and on the workflow around it. As a result, it is often unclear where a statement comes from. Citations are then hard to check, for co-authors and reviewers as well as for the authors themselves.

## Disclosure and evidence

Many journals and universities respond to LLMs with disclosure rules. Authors should write the text themselves and state where an LLM helped with writing or editing. We think this puts the focus in the wrong place. Whether a person or an LLM drafted a sentence says little about whether the sentence is correct. The more important question is whether each claim is backed by its source.

The evidence ledger addresses this question directly. For every citation, it records the claim, the source, the supporting passage with a short quote, and why the source is cited. Hence, each claim can be checked against its evidence.

Disclosure follows as a side effect. Every record notes whether a person or an agent wrote it, and which model was used. The ledger therefore attributes LLM use per citation, which is more precise than a single statement for the whole text.

## Responsibility

We think authors who write with LLMs should be held to a higher standard, namely that their text can be checked at the level of claims and evidence. If a text meets this standard, it matters less whether a person or an agent drafted it. What matters is that the citations are transparent and correct. The human author still takes responsibility for every claim, and the ledger is how they can do so in practice.

## Use cases

### Authors

The primary use is for authors of manuscripts. The ledger works as a transparency check for the authors themselves, whether or not a journal or another recipient asks for it. Co-authors can check the citations before submission, and a script or a second model can check each quote against its source.

### Journals

Journals could require a ledger with a submission. They could adopt this schema directly or develop their own standard based on it. Reviewers and editors could then check contestable claims against their sources without searching for each passage.

### Universities

Universities could use the ledger in two ways. First, supervisors could require a ledger as additional material with a thesis. They could then check the citations in the thesis against their sources. Second, the schema can support teaching. Students need to learn good scientific practice, including transparency and open science. The ledger offers a concrete example to base lectures on and to discuss with students how transparent research can work when AI is part of the workflow.

## Roots

The idea follows Moravcsik's *active citation* (2014): contestable claims come with the evidence that supports them. Many tools for checking citations already exist or are in development. With the ledger, we wanted to make a focused contribution to our own community, psychological science. However, the schema does not depend on a discipline, and other fields can use it as well.

The table below lists the sources for the individual fields.

### Where the fields come from

| Field or rule | Basis |
| --- | --- |
| `contestable` (full evidence for contestable claims) | Active citation: only citations that support contestable empirical points need full documentation, not background references or uncontested facts (Moravcsik, 2014, pp. 50–51) |
| `anchor.exact`, `anchor.prefix`, `anchor.suffix`, `quote_prefix`, `quote_suffix` | W3C Web Annotation Text Quote Selector: a passage is identified by an exact copy plus the text before and after it (Sanderson et al., 2017, §4.2.4) |
| `relation` | Loosely follows CiTO, the Citation Typing Ontology (Peroni & Shotton, 2012); the mapping onto CiTO terms is not yet checked. `supports` and `contrasts` also match scite's citation classes (Nicholson et al., 2021) |
| Claim, passage and justification in one record | Annotation for Transparent Inquiry links passages in a publication to annotations and underlying sources (Karcher & Weber, 2019) |
| `provenance` | Records who asserted what and when, in the spirit of nanopublications (Groth et al., 2010); a record could be exported in that form |
| `claim_id`, `importance`, `retrieved_via`, `found_via`, `quote_hash`, `no_identifier_reason`, `withdrawn` | Our own proposals; to the best of our knowledge they do not follow an earlier source |

#### References

- Groth, P., Gibson, A., & Velterop, J. (2010). The anatomy of a nanopublication. *Information Services & Use, 30*(1–2), 51–56. https://doi.org/10.3233/ISU-2010-0613
- Karcher, S., & Weber, N. (2019). Annotation for transparent inquiry: Transparent data and analysis for qualitative research. *IASSIST Quarterly, 43*(2), 1–9. https://doi.org/10.29173/iq959
- Moravcsik, A. (2014). Transparency: The revolution in qualitative research. *PS: Political Science & Politics, 47*(1), 48–53. https://doi.org/10.1017/S1049096513001789
- Nicholson, J. M., Mordaunt, M., Lopez, P., Uppala, A., Rosati, D., Rodrigues, N. P., Grabitz, P., & Rife, S. C. (2021). scite: A smart citation index that displays the context of citations and classifies their intent using deep learning. *Quantitative Science Studies, 2*(3), 882–898. https://doi.org/10.1162/qss_a_00146
- Peroni, S., & Shotton, D. (2012). FaBiO and CiTO: Ontologies for describing bibliographic resources and citations. *Journal of Web Semantics, 17*, 33–43. https://doi.org/10.1016/j.websem.2012.08.001
- Sanderson, R., Ciccarese, P., & Young, B. (Eds.). (2017). *Web Annotation Data Model*. W3C Recommendation. https://www.w3.org/TR/2017/REC-annotation-model-20170223/
