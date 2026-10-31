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

The idea follows Moravcsik's *active citation* (2014): contestable claims come with the evidence that supports them. The README lists the sources for the individual fields.
