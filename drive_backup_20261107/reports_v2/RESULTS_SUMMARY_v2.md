# Project S, Q&A branch: v2 results summary
Status: FINAL (demo parity: pass; 3-seed summary: pending)
Created: 2026-10-31T06:47:59

## System
Pooled scorer (pooled): average of a fine-tuned DistilRoBERTa, an SBERT pair-feature logistic regression and an NLI-feature
logistic regression, mapped to 3 levels (incorrect, partial, correct). Teacher-review flag when confidence is below
0.64 (temperature 1.00; contradiction flag off).
It does not need the dataset name, so it can score a new question.

## Dev results (selection was done on dev, so these are optimistic; 95% question-bootstrap CI)
- All dev: QWK 0.432 [0.358, 0.509], macro-F1 0.579 [0.523, 0.629]
- Seen answers: QWK 0.630 [0.562, 0.692], macro-F1 0.730 [0.689, 0.766]
- Unseen questions: QWK 0.317 [0.199, 0.412], macro-F1 0.490 [0.406, 0.544]

## Exploratory test (test sets were already scored once in v1; evaluations on record: 3)
- All test: macro-F1 0.576 [0.543, 0.606], QWK 0.454 [0.392, 0.515]
- Review rule: coverage 0.288, accuracy on auto-scored answers 0.790 [0.747, 0.834]
- The 85% accuracy target at 30% coverage is NOT met.

## Limitations
- Public English science and electricity answers only. Nothing here shows performance on CBSE answers or Indian children.
- The 3-level scheme is custom, so QWK is not comparable with published 3-way results.
- Unseen-question results rest on few questions (27 dev, 24 test), so intervals are wide.
- The pooled scorer is weaker than the dataset-aware ensemble (paired dev difference about -0.025 macro-F1).
- NLI "concepts" are reference-answer sentences, not expert-written concepts; a negation of one item in a list can be missed.
- The 15 hand-written demo cases are a sanity check, not an evaluation.
- Dev numbers are optimistic because the scorer, calibration and threshold were chosen on dev.
