"""Draft tests; not run by Codex."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from question_bank import available_subjects, question_choices, retrieve

def test_question_id_retrieves_linked_rubric():
    question = {"q1": {"question_id": "q1", "subject": "Science", "grade": 5, "question_text": "Why?", "reference_answers": ["Because."]}}
    rubric = {"q1": {"question_id": "q1", "review_status": "draft_unreviewed"}}
    q, r = retrieve("q1", question, rubric)
    assert q["question_id"] == r["question_id"] == "q1"

def test_missing_question_or_rubric_fails_clearly():
    try:
        retrieve("missing", {}, {})
    except KeyError as e:
        assert "Question not found" in str(e)
    else:
        raise AssertionError("Missing question was accepted")

def test_subject_and_question_selection_are_traceable():
    bank = {"q1": {"question_id": "q1", "subject": "Science", "grade": 5, "question_text": "Why?"}}
    assert available_subjects(bank) == ["Science"]
    assert question_choices(bank, "Science", 5)[0][1] == "q1"
