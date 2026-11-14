"""JSON/CSV/XLSX question-bank ingestion. PDF and semantic matching are deferred."""
import argparse, csv, hashlib, json, re, unicodedata
from datetime import date
from pathlib import Path
from validation.question_bank import validate_bundle

def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", str(text or "")).casefold().split())

def stable_id(subject, grade, question):
    raw = "|".join((normalize(subject), normalize(grade), normalize(question)))
    return "Q-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

def read_rows(path):
    suffix = path.suffix.casefold()
    if suffix == ".json":
        value = json.loads(path.read_text(encoding="utf-8-sig"))
        return value.get("questions", value) if isinstance(value, dict) else value
    if suffix == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    if suffix in (".xlsx", ".xls"):
        import pandas as pd
        return pd.read_excel(path).fillna("").to_dict("records")
    if suffix == ".pdf":
        raise NotImplementedError("PDF extraction is deferred; convert to reviewed CSV/JSON first")
    raise ValueError(f"Unsupported input format: {suffix}")

def normalize_row(row, source_path):
    get = lambda *names: next((row[n] for n in names if row.get(n) not in (None, "")), None)
    text = str(get("question_text", "question") or "").strip()
    subject, grade = get("subject"), get("grade", "class")
    if not text or not subject or grade is None:
        raise ValueError("required values missing: question_text, subject or grade/class")
    reference = get("reference_answers", "reference_answer")
    if isinstance(reference, str):
        try:
            reference = json.loads(reference) if reference.lstrip().startswith("[") else [reference]
        except json.JSONDecodeError:
            reference = [reference]
    if not reference:
        raise ValueError("at least one reference answer is required")
    qid = str(get("question_id", "id") or stable_id(subject, grade, text)).strip()
    status = str(get("review_status", "status") or "draft_unreviewed").strip()
    if status not in ("draft_unreviewed", "reviewed", "approved", "rejected"):
        status = "draft_unreviewed"
    missing = [name for name, value in (("chapter", get("chapter")), ("required_concepts", get("required_concepts")), ("accepted_answer_variants", get("accepted_answer_variants", "accepted_variants")), ("misconceptions", get("common_misconceptions", "misconceptions"))) if value in (None, "")]
    q = {"question_id": qid, "subject": str(subject).strip(), "grade": int(grade), "chapter": get("chapter"), "topic": str(get("topic", "topic_id") or ""), "question_text": text, "difficulty": str(get("difficulty") or "unknown").casefold(), "reference_answers": list(reference), "required_concepts": get("required_concepts") or [], "supporting_concepts": get("supporting_concepts") or [], "accepted_answer_variants": get("accepted_answer_variants", "accepted_variants") or [], "common_misconceptions": get("common_misconceptions", "misconceptions") or [], "contradictory_claims": get("contradictory_claims") or [], "partial_credit_criteria": get("partial_credit_criteria") or [], "source_provenance": {"source_file": str(source_path), "source_page": get("source_page"), "alignment": "unverified until human review"}, "created_at": date.today().isoformat(), "review_status": status, "needs_review": missing}
    return q

def draft_rubric(question):
    return {"question_id": question["question_id"], "correctness_criteria": [], "completeness_criteria": [], "required_concepts": list(question["required_concepts"]), "supporting_concepts": list(question["supporting_concepts"]), "accepted_variants": list(question["accepted_answer_variants"]), "misconceptions": list(question["common_misconceptions"]), "contradictory_claims": list(question["contradictory_claims"]), "partial_credit_criteria": list(question["partial_credit_criteria"]), "source_provenance": dict(question["source_provenance"]), "created_at": question["created_at"], "review_status": "draft_unreviewed", "needs_review": list(question["needs_review"])}

def ingest(source, existing_questions=None, existing_rubrics=None):
    existing_questions = existing_questions or {"schema_version": "1.0-draft", "questions": []}
    existing_rubrics = existing_rubrics or {"schema_version": "1.0-draft", "rubrics": {}}
    qs = list(existing_questions["questions"]); rs = dict(existing_rubrics["rubrics"])
    ids = {q["question_id"]: q for q in qs}; texts = {normalize(q["question_text"]): q["question_id"] for q in qs}
    added = duplicates = 0; errors = []
    for rowno, row in enumerate(read_rows(source), 2):
        try:
            q = normalize_row(row, source)
            norm = normalize(q["question_text"])
            if q["question_id"] in ids:
                if normalize(ids[q["question_id"]]["question_text"]) != norm: errors.append(f"row {rowno}: ID conflict {q['question_id']}")
                else: duplicates += 1
                continue
            if norm in texts:
                duplicates += 1; continue
            qs.append(q); ids[q["question_id"]] = q; texts[norm] = q["question_id"]
            if q["question_id"] not in rs: rs[q["question_id"]] = draft_rubric(q)
            added += 1
        except Exception as exc:
            errors.append(f"row {rowno}: {exc}")
    qdoc, rdoc = {"schema_version": "1.0-draft", "label_contract": {"incorrect": 0, "partial": 1, "correct": 2}, "questions": qs}, {"schema_version": "1.0-draft", "rubrics": rs}
    errors.extend(validate_bundle(qdoc, rdoc))
    return qdoc, rdoc, {"added": added, "duplicates_skipped": duplicates, "errors": errors}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--source", required=True); ap.add_argument("--questions-out", required=True); ap.add_argument("--rubrics-out", required=True); ap.add_argument("--existing-questions"); ap.add_argument("--existing-rubrics"); a = ap.parse_args()
    source, qo, ro = map(lambda x: Path(x).resolve(), (a.source, a.questions_out, a.rubrics_out))
    if qo.exists() or ro.exists(): raise FileExistsError("Refusing to overwrite either output")
    eq = json.loads(Path(a.existing_questions).read_text(encoding="utf-8-sig")) if a.existing_questions else None
    er = json.loads(Path(a.existing_rubrics).read_text(encoding="utf-8-sig")) if a.existing_rubrics else None
    qdoc, rdoc, summary = ingest(source, eq, er)
    if summary["errors"]: raise ValueError("Import blocked; see validation errors: " + repr(summary["errors"]))
    qo.parent.mkdir(parents=True, exist_ok=True); ro.parent.mkdir(parents=True, exist_ok=True)
    qo.write_text(json.dumps(qdoc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ro.write_text(json.dumps(rdoc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print({k: summary[k] for k in ("added", "duplicates_skipped")})

if __name__ == "__main__": main()
