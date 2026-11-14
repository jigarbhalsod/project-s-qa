"""Question/rubric lookup; it does not score answers or modify the scorer."""
import json
from pathlib import Path
from validation.question_bank import validate_bundle

def load_bank(directory):
    directory = Path(directory)
    questions = json.loads((directory / "questions.json").read_text(encoding="utf-8-sig"))
    rubrics = json.loads((directory / "rubrics.json").read_text(encoding="utf-8-sig"))
    errors = validate_bundle(questions, rubrics)
    if errors:
        raise ValueError("Question bank validation failed: " + "; ".join(errors))
    return {q["question_id"]: q for q in questions["questions"]}, rubrics["rubrics"]

def available_subjects(bank):
    return sorted({q["subject"] for q in bank.values()})

def available_grades(bank, subject):
    return sorted({q["grade"] for q in bank.values() if q["subject"] == subject})

def question_choices(bank, subject=None, grade=None):
    rows = [q for q in bank.values() if (subject is None or q["subject"] == subject) and (grade is None or q["grade"] == grade)]
    return [(f"{q['question_id']} — {q['question_text']}", q["question_id"]) for q in rows]

def retrieve(question_id, bank, rubrics):
    if question_id not in bank:
        raise KeyError(f"Question not found: {question_id}")
    q = bank[question_id]
    rubric = rubrics.get(question_id)
    if rubric is None:
        raise KeyError(f"Rubric missing for question: {question_id}")
    return q, rubric
