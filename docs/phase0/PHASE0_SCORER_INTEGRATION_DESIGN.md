# Frozen scorer integration design

**Status: Drafted interface proposal only. No integration implemented.**
The existing A_predict.py, notebook, policy, model artifacts, thresholds, and
prediction outputs remain frozen.

A future separate adapter could accept `question_id`, `question_text`,
`passage_id`/context reference, `reference_answer`, `student_answer`, and
exact `bank_version`, `rubric_id`, and `rubric_version`. It must resolve
approved content and validate identifiers before invoking a scorer. Return
the frozen scorer result unchanged, with context/rubric metadata separately
attributed; do not silently change probabilities, mapping, confidence, or the
0.64 threshold.

If required rubric evidence is missing or unapproved, fail closed for
rubric-dependent claims and identify the missing version. Do not infer a
question from the answer. Keep the frozen baseline result as comparator. Any
later scoring logic requires separate approval, versioning, and independent
evaluation.

API ownership, compatibility, error behavior, privacy/logging, and teacher
review presentation remain open. This proposal does not claim the current
scorer reads rubric fields.
