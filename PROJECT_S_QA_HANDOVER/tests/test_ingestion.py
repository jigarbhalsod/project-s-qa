"""Draft tests; not run by Codex."""
import csv, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ingestion.ingest import ingest, stable_id

FIELDS = ["question_id", "subject", "class", "topic_id", "question_text", "reference_answer", "difficulty", "source_page", "status"]

def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS); writer.writeheader(); writer.writerows(rows)

def row(qid="q1", text="Why does a shadow form?"):
    return {"question_id": qid, "subject": "Science", "class": "5", "topic_id": "light", "question_text": text, "reference_answer": "Light is blocked.", "difficulty": "easy", "source_page": "local source", "status": "draft_unreviewed"}

def test_stable_id_repeats_for_same_normalized_input():
    assert stable_id("Science", 5, "A  question?") == stable_id(" science ", "5", "a question?")

def test_csv_import_creates_draft_and_missing_rubric(tmp_path):
    source = tmp_path / "bank.csv"; write_csv(source, [row()]); qdoc, rdoc, summary = ingest(source)
    assert summary["added"] == 1 and not summary["errors"]
    qid = qdoc["questions"][0]["question_id"]
    assert qdoc["questions"][0]["review_status"] == "draft_unreviewed"
    assert rdoc["rubrics"][qid]["review_status"] == "draft_unreviewed"
    assert "chapter" in qdoc["questions"][0]["needs_review"]

def test_normalized_duplicate_is_skipped(tmp_path):
    source = tmp_path / "bank.csv"; write_csv(source, [row(), row("q2", " WHY DOES A SHADOW FORM? ")]); _, _, summary = ingest(source)
    assert summary["added"] == 1 and summary["duplicates_skipped"] == 1

def test_existing_records_are_preserved(tmp_path):
    source = tmp_path / "bank.csv"; write_csv(source, [row()]); old = {"question_id": "old", "subject": "Science", "grade": 4, "chapter": "x", "topic": "x", "question_text": "old text", "difficulty": "easy", "reference_answers": ["old"], "required_concepts": [], "supporting_concepts": [], "accepted_answer_variants": [], "common_misconceptions": [], "contradictory_claims": [], "partial_credit_criteria": [], "source_provenance": {"source": "old"}, "created_at": "2026-11-10", "review_status": "draft_unreviewed"}; old_rubric = {"question_id": "old", "correctness_criteria": [], "completeness_criteria": [], "required_concepts": [], "supporting_concepts": [], "accepted_variants": [], "misconceptions": [], "contradictory_claims": [], "partial_credit_criteria": [], "source_provenance": {"source": "old"}, "created_at": "2026-11-10", "review_status": "draft_unreviewed"}
    qdoc, rdoc, _ = ingest(source, {"questions": [old]}, {"rubrics": {"old": old_rubric}})
    assert qdoc["questions"][0] == old and "old" in rdoc["rubrics"]

def test_malformed_row_is_reported(tmp_path):
    source = tmp_path / "bank.csv"; write_csv(source, [{"question_id": "bad", "subject": "", "class": "", "topic_id": "", "question_text": "", "reference_answer": ""}]); _, _, summary = ingest(source)
    assert summary["errors"]
