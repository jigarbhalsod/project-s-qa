"""Validation helpers for draft question and rubric bundles; not runtime scoring."""
from collections import Counter

QUESTION_FIELDS = ("question_id", "subject", "grade", "chapter", "topic", "question_text", "difficulty", "reference_answers", "required_concepts", "supporting_concepts", "accepted_answer_variants", "common_misconceptions", "contradictory_claims", "partial_credit_criteria", "source_provenance", "created_at", "review_status")
RUBRIC_FIELDS = ("question_id", "correctness_criteria", "completeness_criteria", "required_concepts", "supporting_concepts", "accepted_variants", "misconceptions", "contradictory_claims", "partial_credit_criteria", "source_provenance", "created_at", "review_status")
LABELS = {"incorrect": 0, "partial": 1, "correct": 2}

def validate_labels(labels):
    errors = []
    if labels != LABELS:
        errors.append("three-class contract must be Incorrect=0, Partial=1, Correct=2")
    return errors

def validate_bundle(question_doc, rubric_doc):
    errors = []
    errors.extend(validate_labels(question_doc.get("label_contract", {})))
    questions = question_doc.get("questions", [])
    rubrics = rubric_doc.get("rubrics", {})
    ids = [q.get("question_id") for q in questions]
    duplicates = [qid for qid, n in Counter(ids).items() if not qid or n > 1]
    if duplicates:
        errors.append(f"missing or duplicate question IDs: {duplicates}")
    by_id = {q.get("question_id"): q for q in questions}
    for i, q in enumerate(questions):
        missing = [field for field in QUESTION_FIELDS if field not in q]
        if missing:
            errors.append(f"question row {i}: missing fields {missing}")
        if q.get("grade") not in (4, 5, 6):
            errors.append(f"question row {i}: grade must be 4, 5 or 6")
        if q.get("difficulty") not in ("easy", "medium", "hard", "unknown"):
            errors.append(f"question row {i}: invalid difficulty")
        if q.get("review_status") not in ("draft_unreviewed", "reviewed", "approved", "rejected"):
            errors.append(f"question row {i}: invalid review status")
        if q.get("review_status") == "approved" and (q.get("chapter") is None or not q.get("required_concepts")):
            errors.append(f"question row {i}: approval requires chapter and reviewed required concepts")
        if not q.get("source_provenance"):
            errors.append(f"question row {i}: source provenance is required")
    for qid, rubric in rubrics.items():
        if qid not in by_id:
            errors.append(f"rubric references unknown question_id {qid}")
        missing = [field for field in RUBRIC_FIELDS if field not in rubric]
        if missing:
            errors.append(f"rubric {qid}: missing fields {missing}")
        if rubric.get("question_id") != qid:
            errors.append(f"rubric key/id mismatch for {qid}")
        if rubric.get("review_status") not in ("draft_unreviewed", "reviewed", "approved", "rejected"):
            errors.append(f"rubric {qid}: invalid review status")
        for record in (rubric, by_id.get(qid, {})):
            label = record.get("label")
            if label is not None and label not in (0, 1, 2):
                errors.append(f"{qid}: invalid three-class label {label!r}")
    for qid in by_id:
        if qid not in rubrics:
            errors.append(f"question {qid} has no linked rubric")
    return errors
