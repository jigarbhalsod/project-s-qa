# JSON validation specification

**Status: Drafted specification; no validator implemented or run.**

Validation layers:

1. Parse UTF-8 JSON; reject duplicate keys where supported; report file and
   JSON path.
2. Validate `schema_version`, required fields, types, nullability, and
   enumerated values.
3. Enforce unique question/rubric IDs and both directions of rubric/question
   references; resolve passage/evidence references when required.
4. Check completeness: non-empty question and expected answer; required
   concepts and criteria follow the approved subject schema. This cannot
   establish factual correctness.
5. Check provenance/review consistency. An `approved` record without required
   reviewer evidence is an error.
6. Check schema compatibility. Unsupported versions fail with migration
   guidance; no automatic rewrite.

Report all findings with JSON-pointer-like path, stable ID, rule ID, and
severity. Do not fill missing values, rewrite statuses, drop records, or
normalize source text silently. Structural PASS is not educational approval.
Review states follow the current template: `draft_unreviewed`, `in_review`,
`revision_required`, `approved`, and `rejected`. Owner decisions remain on
unknown-field policy, duplicate-key handling, compatibility window, and
warning release policy.
