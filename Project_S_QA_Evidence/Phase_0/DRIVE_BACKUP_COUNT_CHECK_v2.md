# Drive Backup Count Check v2

## Root check

- [Verified] A root: `drive_backup_20261107/project_s_qa`; 170 files.
- [Verified] B root: `project_s_qa_backup_20261106_1957`; it directly contains `reports_v2/`, `interim/`, `processed/`, `A_submission_v2/`, and `A_submission_v2.zip`. No extra wrapper root is needed. `A_submission_v2/` is a nested package, not B's project root.
- [Verified] The earlier relative-path split (159 only A / 56 only B) is not caused by choosing the wrong B root. Relative paths differ substantially; name+size comparison below collapses files found at different paths.

## Name and size comparison

- [Verified] A files: 170; B files: 67.
- [Verified] Matched by basename + size (multiset): 66.
- [Verified] Only in B by basename + size: 1.
- [Verified] Only in A by basename + size: 104.

### Only in B (name + size)

- `A_runtime_stage_manifest_v2.json` — 3911 bytes

### Only in A (name + size)

- `A_abstain_policy_v2.json` — 784 bytes
- `A_bootstrap_ci_v2.csv` — 4987 bytes
- `A_demo_cases_summary_v2.csv` — 1820 bytes
- `A_demo_parity_v2.csv` — 1006 bytes
- `A_demo_parity_v2.json` — 113 bytes
- `A_deployed_metrics_ci_v2.csv` — 627 bytes
- `A_deployed_scorer_v2.json` — 222 bytes
- `A_final_tables_v2.md` — 4675 bytes
- `A_negation_paraphrase_v2.csv` — 3658 bytes
- `A_predict.cpython-313.pyc` — 14877 bytes
- `A_predict.py` — 7626 bytes
- `A_predict_contract_v2.json` — 1217 bytes
- `A_seed_summary_v2.json` — 154 bytes
- `A_stats.cpython-313.pyc` — 3471 bytes
- `A_stats.py` — 1215 bytes
- `A_table_dev_ci_v2.csv` — 268 bytes
- `A_table_paired_v2.csv` — 1916 bytes
- `A_table_risk_coverage_v2.csv` — 311 bytes
- `A_table_test_v2.csv` — 667 bytes
- `A_table_v1_vs_deployed_v2.csv` — 360 bytes
- `A_test_access_log_v2.json` — 393 bytes
- `A_test_results_v2.csv` — 2287 bytes
- `A_test_scored_v2.parquet` — 195541 bytes
- `A_v2_manifest.json` — 5063 bytes
- `Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb` — 2471126 bytes
- `RESULTS_SUMMARY_v1.md` — 9566 bytes
- `RESULTS_SUMMARY_v2.md` — 1823 bytes
- `RESULTS_SUMMARY_v2.md` — 1823 bytes
- `UPLOAD_MANIFEST_SHA256.txt` — 968 bytes
- `abstain_config_v1.json` — 369 bytes
- `abstain_test_v1.csv` — 746 bytes
- `baseline_predictions_v1.parquet` — 144101 bytes
- `baseline_results_v1.csv` — 8775 bytes
- `cbse_demo_questions_v1.csv` — 2888 bytes
- `cbse_question_bank_template.csv` — 155 bytes
- `combiner_v1.joblib` — 129270 bytes
- `combiner_v1.joblib` — 129270 bytes
- `config.json` — 919 bytes
- `config.json` — 920 bytes
- `demo_outputs.json` — 1672 bytes
- `ensemble_weights_dev_v2.csv` — 1510 bytes
- `example_inputs.json` — 3940 bytes
- `fig1_paired_differences.png` — 82861 bytes
- `fig1_paired_differences.png` — 82861 bytes
- `fig2_seen_vs_unseen.png` — 44405 bytes
- `fig2_seen_vs_unseen.png` — 44405 bytes
- `fig3_risk_coverage.png` — 98606 bytes
- `fig3_risk_coverage.png` — 98606 bytes
- `fig4_reliability.png` — 77405 bytes
- `fig4_reliability.png` — 77405 bytes
- `final_scorer_choice_v2.json` — 231 bytes
- `freeze_record_v1.json` — 933 bytes
- `ft_probs_v1.parquet` — 321131 bytes
- `llm_Qwen2.5-3B-Instruct_beetle_dev_ua_n250.parquet` — 8152 bytes
- `llm_Qwen2.5-3B-Instruct_beetle_dev_uq_n250.parquet` — 8136 bytes
- `llm_Qwen2.5-3B-Instruct_beetle_test_ua_n100.parquet` — 4809 bytes
- `llm_Qwen2.5-3B-Instruct_beetle_test_uq_n100.parquet` — 4790 bytes
- `llm_Qwen2.5-3B-Instruct_scientsbank_dev_ua_n250.parquet` — 8194 bytes
- `llm_Qwen2.5-3B-Instruct_scientsbank_dev_uq_n250.parquet` — 8016 bytes
- `llm_Qwen2.5-3B-Instruct_scientsbank_test_ua_n100.parquet` — 4814 bytes
- `llm_Qwen2.5-3B-Instruct_scientsbank_test_ud_n100.parquet` — 4841 bytes
- `llm_Qwen2.5-3B-Instruct_scientsbank_test_uq_n100.parquet` — 4799 bytes
- `llm_predictions_v1.parquet` — 38690 bytes
- `manifest_v1.json` — 6923 bytes
- `minilm_emb.npy` — 23341184 bytes
- `minilm_texts.json` — 980018 bytes
- `model.safetensors` — 328501508 bytes
- `model_selection_bootstrap_v2.csv` — 359 bytes
- `model_selection_dev_v2.csv` — 2379 bytes
- `needs_review_nd_v2_report.csv` — 164 bytes
- `nli_features_v1.parquet` — 739730 bytes
- `per_question_beetle_dev_uq_v1.csv` — 237 bytes
- `per_question_scientsbank_dev_uq_v1.csv` — 693 bytes
- `per_question_test_v1.csv` — 59851 bytes
- `phase3a_results_v1.csv` — 11351 bytes
- `phase3a_same_answers_comparison_v1.csv` — 5319 bytes
- `phase3b_combiner_comparison_v1.csv` — 2870 bytes
- `pooled_lr_v2.joblib` — 63625 bytes
- `pooled_lr_v2.joblib` — 63625 bytes
- `project_s_qa_v2_package.zip` — 423133 bytes
- `question_bank.csv` — 124536 bytes
- `question_bank_v1.csv` — 128553 bytes
- `rb_probs_v2.parquet` — 72707 bytes
- `risk_coverage_ensemble_dev_v2.csv` — 599 bytes
- `rubrics.json` — 394665 bytes
- `rubrics_v1.json` — 381325 bytes
- `scored_dev_v1.parquet` — 77365 bytes
- `scored_dev_v2.parquet` — 81425 bytes
- `scored_test_v1.parquet` — 94316 bytes
- `scored_test_v2.parquet` — 97401 bytes
- `split_report_v1.json` — 1485 bytes
- `splits_v1.csv` — 1247319 bytes
- `sra_unified_labeled.parquet` — 718960 bytes
- `sra_unified_raw.parquet` — 691143 bytes
- `sra_unified_splits_v1.parquet` — 1173152 bytes
- `stack_features_v1.parquet` — 1644342 bytes
- `test_access_log_v1.json` — 3884 bytes
- `test_ci_v1.csv` — 2235 bytes
- `test_llm_comparison_v1.csv` — 1797 bytes
- `test_results_v1.csv` — 7802 bytes
- `tokenizer.json` — 3558895 bytes
- `tokenizer.json` — 3558895 bytes
- `tokenizer_config.json` — 388 bytes
- `tokenizer_config.json` — 388 bytes


## SHA-256 of matched non-test name+size files

- [Verified] Hashed matched non-test pairs: 61. Exact hash matches by name+size: 60. Test-named pairs skipped: 5.
- [Verified] Test artifacts were size/name only; no hash or file content was read.

### Hash variants with the same name and size

- [Verified] B-side variant `A_demo_reference_outputs_v2.json` (16474 bytes), SHA-256 `c99b7d84d000046c9629708d5ee440d5a20ab28fd298f63708e2e8c13f89dc92`; path(s): `reports_v2/A_demo_reference_outputs_v2.json`
- [Verified] A-side variant `combiner_v1.joblib` (129270 bytes), SHA-256 `e6341f87f06fb4225f30751556c09cccc3351ce08444f02722dfb01ef1d6b21d`; path(s): `conflict_backup_20261105_202222/interim/combiner_v1.joblib`
- [Verified] A-side variant `pooled_lr_v2.joblib` (63625 bytes), SHA-256 `0a142d1cbb4e07e45afb2d894b17d8d6572c776e9fba82185ee6ef1251836189`; path(s): `conflict_backup_20261105_202222/interim/pooled_lr_v2.joblib`

## B-only item and submission relevance

- [Verified] B-only item: `A_runtime_stage_manifest_v2.json` (3,911 bytes). Its name indicates runtime-staging metadata; it is not a model or input required by the notebook inference path. It may matter for staging provenance. The file was not opened.

## Conclusion

- [Verified] Not every B file is present in A by name and size: `A_runtime_stage_manifest_v2.json` is absent from A.
- [Verified] B has the staged reference JSON hash variant `c99b7d84...` not found in A; A's matching-name/size reference JSON is the packaged hash `ea5288e9...`. A also contains conflict-backup combiner and pooled-LR variants with same names/sizes but hashes absent from B.
- [Verified] Comparison used relative paths only to identify each folder; matching was by basename and size. No files were modified or moved. Test artifacts were not opened or hashed.
