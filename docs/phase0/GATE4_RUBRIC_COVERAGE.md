# Gate 4 — Rubric coverage

**Status: BLOCKED.** Counts and fields are structural facts from the local
candidate JSON files. They do not establish correctness or approval.

- Packaged rubric JSON: 251 records; required_concepts is populated in the
  records, but concepts_status is unreviewed (248 auto-draft, 3 hand-written
  unreviewed). Subject and grade are absent from the record schema; no
  verified_by identity is populated.
- Handover question/rubric prototype: 12 Science items, grades 4–6; all
  question and rubric records are draft_unreviewed. required_concepts is
  empty in all 12 questions and all 12 rubric entries.
- No source is canonical. The Q&A scorer does not become rubric-aware merely
  because rubric JSON exists; scorer integration is outside this gate.

**Needed:** select a source and schema; preserve provenance and immutable
versions; fill only evidence-backed metadata; conduct qualified review and
record decisions. AI/static review is not expert approval.
