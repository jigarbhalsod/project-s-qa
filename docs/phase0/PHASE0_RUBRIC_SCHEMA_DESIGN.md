# Rubric schema design

**Status: Drafted proposal. No rubric content is canonical or approved.**

| Field | Type | Rule |
|---|---|---|
| rubric_id | string | Stable unique ID for each immutable version |
| question_id | string | Required reference to the matching question |
| version | string | Substantive edits create a new version |
| required_concepts / optional_concepts | arrays | Observable required and supporting concepts, separated |
| full_credit_criteria | array | Evidence that establishes correctness |
| partial_credit_criteria | array | Valid partial reasoning and missing elements |
| incorrect_answer_criteria | array | Evidence for incorrectness, not lexical mismatch alone |
| contradiction_conditions | array | Passage/rubric-grounded contradiction conditions |
| irrelevant_answer_conditions | array | Question-relative evidence for off-topic answers |
| accepted_variants | array | Meaning-preserving alternatives with provenance |
| misconceptions | array | Common errors and their source/evidence |
| worked_examples | array | Example, rationale, provenance; synthetic examples labeled |
| source_provenance | object | Source, locator, version, author |
| review_status | enum | draft_unreviewed, in_review, revision_required, approved, rejected |
| reviewer_metadata | array | Identity, qualifications, dates, decisions, comments |
| adjudication | object/null | Resolution and rationale for disputed/high-impact records |

Criteria distinguish correct, partial, incorrect, contradictory, and
irrelevant responses. Do not award partial credit from keyword overlap or
answer length alone. Approval requires the sign-offs in
PHASE0_ASSESSMENT_REVIEW_TEMPLATE.md. Missing rubric data must not silently
become an approved generic rubric. Storage format, criterion IDs, and reviewer
metadata policy remain owner decisions.
