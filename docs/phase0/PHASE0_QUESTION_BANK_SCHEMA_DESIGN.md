# Question-bank schema design

**Status: Drafted proposal. Not canonical content; no bank records created.**
Unknown metadata stays null or absent; it must not be inferred from wording.

## Bundle and record

Bundle fields: `schema_version`, `bank_id`, `bank_version`, `created_at`,
`source_manifest`, and `questions[]`. Each question record proposes:

| Field | Type | Rule |
|---|---|---|
| question_id | string | Required, stable, unique within the bank |
| passage_id | string/null | Required key; null only for documented passage-independent items |
| subject | enum | Science, Social Science, Mathematics, English |
| topic | string/null | Source-backed when known |
| grade_level | integer/string/null | Do not infer curriculum or age equivalence |
| difficulty | object/null | Requires an approved repeatable rubric; otherwise null |
| question_text | string | Exact authored text |
| expected_answer | string | Reference response with source/version |
| accepted_answer_variants | array | Meaning-preserving alternatives with provenance |
| required_concepts / optional_concepts | arrays | Stable concept IDs, kept distinct |
| common_misconceptions | array | Explicit misconception IDs/descriptions and sources |
| contradiction_indicators | array | Passage- or criterion-grounded contradiction evidence |
| reference_evidence | array | Passage ID and stable span/paragraph locator |
| rubric_id | string | Required foreign key to one rubric version |
| provenance | object | Source, author, date, version, and locator |
| version | string | Immutable record version |
| review_status | enum | draft_unreviewed, in_review, revision_required, approved, rejected |
| review_metadata | array | Reviewer identity, qualification reference, dates, decisions, adjudication |

`approved` requires actual qualified review evidence. A `reviewed` timestamp or
AI review does not imply approval. Keep student answers and labels in separate
datasets. The owner must decide ID namespaces, difficulty scale, permitted
passage-independent items, and version compatibility before this becomes a
schema. No existing bank is selected.
