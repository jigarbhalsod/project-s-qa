# Phase 1 Vishwajeet notebook check

Source checked: C:/Users/Jigar/OneDrive/Desktop/Vishwajeet_QA_Branch.ipynb
Method: JSON source/output inspection only; no notebook cells were run.

## 1. Block headings - verified
All four exact expected headings are present as standalone markdown cells.
No note replaced the heading; no note follows in the same heading cell.
- Block 34: cell 91 | Block 34: Create Final v2 Development Scoring File
- Block 37: cell 97 | Block 37: Seen vs Unseen Evaluation with Paired Bootstrap Confidence Intervals
- Block 40: cell 103 | Block 40: Three-Seed RoBERTa Stability Experiment
- Block 43: cell 110 | Block 43: NLI Feature Ablation (Question-Grouped OOF)

## 2. Block 40 wording - verified
The phrase "mean macro-F1 over four dev splits" is not present in
Block 40 source or saved outputs (Block 40 heading cell 103, code cell 104).

## 3. Cell counts - verified (computed now)
- Total cells: 137.
- Code cells: 75.
- Empty code cells: 5 (indices 76, 109, 112, 116, 136).
- Code cells with error outputs: 1 (cell 68).
  Evidence: cell 68 | import os, gc, json import numpy as np, pandas as pd, torch

## 4. Drive writes without V_ filename - verified by source scan
The notebook contains Drive write targets not prefixed V_. Cell indices and
named targets found in source:
- 10: sra_unified_raw.parquet
- 16: label5_distribution.csv; label3_ours_distribution.csv;
  per_question_stats.csv
- 18: sra_unified_labeled.parquet; data_quality_report.json
- 21: syllabus_with_ids.csv; source_register.csv
- 23: cbse_question_bank_template.csv; question_bank.csv
- 25: rubrics.json; 28: sra_unified_raw.parquet; sra_unified_labeled.parquet
- 32: split_report_v1.json
- 34: sra_unified_splits_v1.parquet; question_bank_v1.csv;
  rubrics_v1.json; manifest_v1.json
- 41: minilm cache; baseline_results_v1.csv; baseline_predictions_v1.parquet;
  per_question_{ds}_dev_uq_v1.csv
- 44: nli_features_v1.parquet
- 46: per-split model parquet; llm_predictions_v1.parquet
- 48: phase3a_results_v1.csv; phase3a_same_answers_comparison_v1.csv
- 51: ft_probs_v1.parquet
- 53: combiner_v1.joblib; phase3b_combiner_comparison_v1.csv;
  stack_features_v1.parquet
- 55: scored_dev_v1.parquet; abstain_config_v1.json
- 59: freeze_record_v1.json; test_access_log_v1.json
- 61: test_results_v1.csv; test_ci_v1.csv; abstain_test_v1.csv;
  scored_test_v1.parquet
- 63: per_question_test_v1.csv; test_llm_comparison_v1.csv;
  RESULTS_SUMMARY_v1.md; MANIFEST_final_v1.json
- 66: ensemble_weights_dev_v2.csv; risk_coverage_ensemble_dev_v2.csv
- 68: rb_probs_v2.parquet
- 78: comparison, weight-grid, and per-set CSV outputs
- 84: roberta_dev_errors_v2.csv; roberta_dev_confusions_v2.csv
- 88: error-patterns CSV; 90: answer-length CSV
- 92: scored_dev_v2.parquet; scored_dev_v2.csv
- 96: v2_handoff_metrics_by_split.csv; v2_handoff_prediction_counts.csv;
  v2_handoff_summary.txt
- 98: seen_unseen_bootstrap_ci_v2.csv
- 104: per-seed dev_predictions.parquet, dev_metrics.json, epoch_history.csv;
  roberta_three_seed_metrics_v2.csv; roberta_three_seed_epoch_history_v2.csv
- 108: nli_feature_coverage_v2.csv
- 111: nli_ablation_oof_v2.csv; nli_ablation_oof_predictions_v2.parquet
- 121, 125, 126: demo/example_inputs.json; demo/demo_outputs.json

## 5. Run-all and v1 writes - verified by source scan
- "Run all": no matching source cell.
- v1 files are written in cells 32, 34, 41, 44, 46, 48, 51, 53,
  55, 59, 61, and 63. Cell 66 reads v1 features and writes v2 outputs.

## 4-line summary
- Verified current Desktop notebook by the exact path Jigar supplied.
- Exact Block 34, 37, 40, and 43 headings are present; none was replaced.
- 137 cells, 75 code, 5 empty code, and 1 code error output verified.
- Block 40 phrase absent; non-V_ Drive writes and v1 writes are listed.
