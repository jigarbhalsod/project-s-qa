"""DRAFT ONLY. Count reviewer fields; never edit labels or the sample."""
import argparse, csv
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="Project_S_QA_Evidence/Phase_8_Accuracy_Max/E1_review_sample.csv")
    a = ap.parse_args()
    p = Path(a.input)
    if "test" in str(p).lower(): raise SystemExit("Refusing a test-named path")
    required = {"reviewer_name", "reviewer_judgement", "reviewer_note", "suggested_gold_correction"}
    with p.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows or not required.issubset(rows[0]): raise SystemExit("Missing reviewer columns or no rows")
    counts = {k: sum(bool((r.get("reviewer_judgement") or "").strip()) and r["reviewer_judgement"].strip() == k for r in rows) for k in ("gold_correct", "gold_questionable", "model_prediction_defensible", "ambiguous")}
    filled = sum(bool((r.get("reviewer_name") or "").strip()) for r in rows)
    print(f"rows={len(rows)} reviewed={filled} unreviewed={len(rows)-filled}")
    for k, v in counts.items(): print(f"{k}={v}")
    print("unvalidated heuristic: 12+ gold_questionable suggests a data ceiling; under 6 suggests model blind spots")

if __name__ == "__main__": main()
