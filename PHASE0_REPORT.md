# Phase 0 report

## Files
- COPY: 2,682,400 bytes; SHA-256 b170db74...7c5134bf.
- Reference: reference absent; no matching file.
- Colab downloads: none; no matching file.
- Backup before_block60: 2,739,578 bytes; ae0ccae2...a92ff944.
- Backup before_block61: 2,744,484 bytes; 953e5133...bcdce449.
- COPY cells: 165 verified (computed now); code cells: 68 verified.

## Integrity (step 2)
- NOT DONE: reference absent. Hash and cell counts not checked.
- Identical, reference-only, COPY-only, and changed counts:
  not checked because the reference is absent.
- Context gap: section 4 says COPY 165; section 5 says 161.
  Actual COPY is 165 verified; comparison counts unverified.

## Comparison table (step 3)
Colab comparison is not checked because its download is absent.
| Feature | COPY evidence | Status |
|---|---|---|
| demo_outputs_PREVIOUS (45a) | cells 118-119 | COPY present |
| Block 45b, 45c, gr.Interface | cells 120, 123-124 | COPY present |
| Blocks 56, 57, 58 | 56 absent; 57:150; 58:152 | COPY present |
| skip_name manifest fix | cell 153 | COPY present |
| Run history; RoBERTa weights note | cell 0; weights cell 68 | COPY present |
| Blocks 59-62; Summary; READ FIRST | 154,156,158,160,163,0 | COPY present |
| DEMO PARITY: PASS (output) | cell 117 | COPY present |
| Zipped 54 files (output) | cell 153 | COPY present |
| evaluations on record (output) | 2:57; 3:61,77,79,111,134 | COPY present |
Colab status for all rows: not checked (file absent).

## Risks (step 4)
- API/backend strings: cell 44; BACKEND = "local"; API branch and
  ANTHROPIC_API_KEY also appear. Cell 43 calls it dev-only.
- Code cells with no saved outputs: 67, 155, 157, 159, 161, 164.
- Blocks 59-62 appear; no other new number below 63 identified.
  Novelty cannot be checked without the reference.
- Explicit non-A write targets include: manifest_v1.json,
  question_bank_v1.csv, splits_v1.csv, rubrics_v1.json,
  sra_unified_splits_v1.parquet, combiner_v1.joblib,
  stack_features_v1.parquet, ft_probs_v1.parquet,
  abstain_config_v1.json, scored_dev_v1.parquet,
  test_results_v1.csv, test_access_log_v1.json, rb_probs_v2.parquet,
  ensemble_weights_dev_v2.csv, model_selection_dev_v2.csv,
  model_selection_bootstrap_v2.csv, final_scorer_choice_v2.json,
  needs_review_nd_v2_report.csv, demo_outputs.json,
  example_inputs.json, RESULTS_SUMMARY_v2.md, A_submission_v2.zip.
  Notebook source scan only; cells were not run.

## RECOMMENDATION
Needs Jigar's decision: COPY has new blocks and Summary; Colab evidence
cannot be checked because its download is absent.

## Claude summary
- Reference absent; integrity comparison not done.
- COPY has 165 cells and 68 code cells.
- Colab download absent; feature comparison unavailable.
- COPY contains parity PASS and zip output in saved outputs.
- Submission base needs Jigar's decision.
