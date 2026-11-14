"""Draft JSON import test; not run by Codex."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ingestion.ingest import ingest

def test_valid_json_import_preserves_source_status_and_provenance(tmp_path):
    source = tmp_path / "bank.json"
    row = {"question_id": "json-q1", "subject": "Science", "grade": 4, "chapter": "draft chapter", "topic": "light", "question_text": "Why is a shadow formed?", "difficulty": "easy", "reference_answers": ["When light is blocked."], "status": "draft_unreviewed", "source_page": "source page"}
    source.write_text(json.dumps({"questions": [row]}), encoding="utf-8")
    questions, rubrics, summary = ingest(source)
    assert not summary["errors"] and summary["added"] == 1
    assert questions["questions"][0]["question_id"] == "json-q1"
    assert questions["questions"][0]["review_status"] == "draft_unreviewed"
    assert rubrics["rubrics"]["json-q1"]["review_status"] == "draft_unreviewed"
