"""Draft tests; not run by Codex."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from validation.question_bank import validate_bundle, validate_labels

def q(qid="q1"):
    return {"question_id": qid, "subject": "Science", "grade": 5, "chapter": None, "topic": "topic", "question_text": "Why?", "difficulty": "easy", "reference_answers": ["Because."], "required_concepts": [], "supporting_concepts": [], "accepted_answer_variants": [], "common_misconceptions": [], "contradictory_claims": [], "partial_credit_criteria": [], "source_provenance": {"source": "fixture"}, "created_at": "2026-11-10", "review_status": "draft_unreviewed"}

def r(qid="q1"):
    return {"question_id": qid, "correctness_criteria": [], "completeness_criteria": [], "required_concepts": [], "supporting_concepts": [], "accepted_variants": [], "misconceptions": [], "contradictory_claims": [], "partial_credit_criteria": [], "source_provenance": {"source": "fixture"}, "created_at": "2026-11-10", "review_status": "draft_unreviewed"}

def test_label_contract_rejects_changed_mapping():
    assert not validate_labels({"incorrect": 0, "partial": 1, "correct": 2})
    assert validate_labels({"incorrect": 1, "partial": 1, "correct": 2})

def test_duplicate_question_ids_are_reported():
    qdoc = {"label_contract": {"incorrect": 0, "partial": 1, "correct": 2}, "questions": [q(), q()]}
    assert any("duplicate" in e for e in validate_bundle(qdoc, {"rubrics": {"q1": r()}}))

def test_missing_rubric_is_reported():
    qdoc = {"label_contract": {"incorrect": 0, "partial": 1, "correct": 2}, "questions": [q()]}
    assert any("no linked rubric" in e for e in validate_bundle(qdoc, {"rubrics": {}}))

def test_unknown_rubric_reference_is_reported():
    qdoc = {"label_contract": {"incorrect": 0, "partial": 1, "correct": 2}, "questions": [q()]}
    assert any("unknown question_id" in e for e in validate_bundle(qdoc, {"rubrics": {"q2": r("q2")}}))

def test_required_fields_and_invalid_label_are_reported():
    question = q(); question.pop("source_provenance"); question["label"] = 3
    qdoc = {"label_contract": {"incorrect": 0, "partial": 1, "correct": 2}, "questions": [question]}
    errors = validate_bundle(qdoc, {"rubrics": {"q1": r()}})
    assert any("source_provenance" in e for e in errors)
    assert any("invalid three-class label" in e for e in errors)
