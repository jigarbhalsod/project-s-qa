# Subject and metadata design

**Status: Drafted proposal. No curriculum mapping or grade standard is
asserted.** Use common metadata for Science, Social Science, Mathematics, and
English; subject extensions require domain review.

- `subject`: required enum with those four subjects.
- `topic`: optional source-backed string or controlled ID.
- `grade_level` and `age_range`: recorded independently; no conversion
  without an approved source.
- `curriculum_system`, `curriculum_version`, `standard_id`: nullable until a
  source is named and verified.
- `language`, `locale`, `reading_level`: optional with source and method; do
  not infer from the question alone.
- `difficulty`: nullable until a repeatable classification rubric is
  approved; record its version and rationale when assigned.
- `passage_id`, `question_id`, `rubric_id`: stable references.
- `provenance`: source, locator, author, dates, and version.
- `review_status`: lifecycle state; reviewer decisions are separate evidence.

Potential extensions to review: Science concepts/phenomena; Social Science
place, time, and source perspective; Mathematics notation, units, tolerance,
and valid method; English language objective and meaning-preserving variants.
These are design candidates, not claims about existing content or curriculum.
The owner must choose vocabularies, grade representation, curriculum sources,
and extension compatibility.
