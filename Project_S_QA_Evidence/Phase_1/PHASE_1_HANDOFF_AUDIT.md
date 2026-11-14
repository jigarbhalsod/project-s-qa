# Project S ? Phase 1 handoff audit

Scope: local read-only inspection. No notebook, model, training, or Project S
script was run. No test split/output was opened. Labels below distinguish
filesystem/source evidence from missing or reported information.

## Part 1 ? Artifact inventory

| Item | Finding |
|---|---|
| Vishwajeet notebook | **Verified** ? `C:\Users\Jigar\OneDrive\Desktop\Vishwajeet_QA_Branch.ipynb`; 1,750,118 bytes; mtime 2026-11-05 18:25:03 +05:30; SHA-256 `d9e81c9ce1369c58e2738e2742cf0df1f40a6277ed77d54d0ce9cc20a1e71197`. |
| Requested `V_rb_probs_v2.parquet` | **BLOCKED** ? exact filename not found. Alternate `drive_backup_20261107/project_s_qa/interim/rb_probs_v2.parquet` found; 72,707 bytes; mtime 2026-11-07 16:19:25 +05:30; SHA-256 `2df9948368f300c13df4ea14d13b96473a941deb79087bd389eeb4f86550e3a8`. |
| Three-seed metrics CSV | **BLOCKED** ? `V_roberta_three_seed_metrics_v2.csv` and matching RoBERTa seed-metrics CSV not found in Project 4. |
| Per-seed prediction/metric files | **BLOCKED** ? `seed_42`, `seed_123`, `seed_2026` `dev_predictions.parquet` / `dev_metrics.json` not found in the inspected project tree. |
| Vishwajeet RoBERTa weights | **BLOCKED** ? no RoBERTa-base checkpoint weight file found. Config/tokenizer files under `drive_backup_20261107/project_s_qa/interim/ft_roberta_base_v2/` are not model weights. |
| CBSE questions and corrections | **Verified** ? `block60/cbse_demo_questions_v1.csv`; 2,888 bytes; mtime 2026-11-02 02:35:42 +05:30; SHA-256 `78852eb405819de017fa99a3839cc47912ed1bd40acd0bd0a3966be4b6987e3b`; header has `question_id`, `question_text`, `reference_answer` and 12 data rows. **BLOCKED** ? separate corrections list not found. |

## Part 2 ? Notebook hygiene

| Check | Result |
|---|---|
| Restored headings | **Verified** ? Block 34 cell 91; Block 37 cell 97; Block 40 cell 103; Block 43 cell 110. Each expected heading text is present. |
| Empty code cells | **Verified** ? 5: indices 76, 109, 112, 116, 136. |
| ?23 removed? expectation | **Unverified** ? current empty-cell count is verified; the prior version needed to verify removals was not compared in this task. |

## Part 3 ? Fine-tuning evidence

| Check | Result |
|---|---|
| Method in source | **Verified** ? Block 40 source initializes `AutoModelForSequenceClassification.from_pretrained("roberta-base", num_labels=5)`, calls `model.train()`, and specifies seeds 42, 123, 2026. This is code for fine-tuning a pretrained RoBERTa-base model, not training from scratch. |
| Completed run evidence | **Unverified** ? Block 40 has no saved outputs or execution count in the supplied notebook. |
| Checkpoint weights | **BLOCKED** ? not found in inspected local project files. |

## Part 4 ? Shared probability artifact checks

| Check | Result |
|---|---|
| Shape/schema | **Verified** ? alternate `rb_probs_v2.parquet`: 2,049 rows; columns `uid`, `rb_p0`..`rb_p4`; five-class probabilities. |
| Nulls and row sums | **Verified** ? 2,049 unique non-null UIDs; zero nulls in probability columns; all 2,049 row sums within 1e-5 of 1. Min 0.9999998346; max 1.0000001636. |
| UID alignment | **Verified** ? UID set equals the 2,049 UIDs in the development rows of `A_deployed_dev_probs_v2.parquet`; matched 2,049, missing 0, extra 0. Test rows were excluded immediately and not inspected. |
| Split/label columns | **Unverified** ? the Vish probability file itself has no split or gold-label column. Its exact UID match to the dev UID set establishes dev alignment for these rows. |
| Probability label order | **Verified** ? Block 40 source maps `rb_p0`..`rb_p4` by `LABELS` order: `correct`, `contradictory`, `partially_correct_incomplete`, `irrelevant`, `non_domain`. |
| Artifact status | **Verified** ? dev-only by UID-set equality; no extra UID was present. |

## Part 5 ? Metric reconciliation

| Vishwajeet result | Definition / split / N | Comparability |
|---|---|---|
| Numeric RoBERTa accuracy | **Unverified** ? no stored Block 40 output or seed metrics file was available; source defines `accuracy_5` on dev cohorts, but provides no saved numeric result. | **BLOCKED** ? no value/N to compare. |
| Numeric RoBERTa Macro-F1 | **Unverified** ? source defines five-class `macro_f1_5` and `mean_dev_macro_f1_5`; no saved numeric result or N available. | **BLOCKED** ? no value/N to compare. |
| Numeric RoBERTa QWK | **Unverified** ? no numeric QWK found in available Block 40 source/output or seed files. | **BLOCKED** ? no value/N to compare. |
| Seeds | **Verified** ? source specifies 42, 123, 2026; per-seed completed results are **not found**. | Not a metric. |
| Our baseline | **Reported** ? dev pooled v2: accuracy 56.37%, Macro-F1 52.70%, QWK 0.4015, N=2,049. | Comparison remains **BLOCKED** until Vishwajeet values, UID/split, label mapping, and metric definitions are available and matched. |

## Part 6 ? Blocks 42 and 49 plan only

| Block | Static source behavior | Preconditions / overwrite and safety |
|---|---|---|
| Block 42 | **Verified** ? canonical D notebook source scans `ROOT/**/*.csv` for basenames containing `seed`, reads matching CSVs, and writes `reports_v2/A_seed_summary_v2.csv`; if no seed rows, writes `reports_v2/A_seed_summary_v2.json`. | **Proposed** ? before any later run, make and verify a fresh complete backup of `project_s_qa`; confirm the intended seed CSVs and output targets. It can overwrite either summary output. Do not run until separately approved. |
| Block 49 | **Verified** ? source reads v2 policy/scorer/metrics/parity/seed-summary artifacts and names `A_test_results_v2.csv`, `A_test_scored_v2.parquet`, and `A_test_access_log_v2.json`; writes `RESULTS_SUMMARY_v2.md`, package files/manifest, and a reports manifest. | **BLOCKED** ? current instruction forbids opening test artifacts; this block reads them. It may overwrite summary/package/manifest outputs. A verified full backup would be necessary but does not lift the test-data restriction. Do not run under this task. |

## Part 7 ? Cutoff proposal

**Proposed:** Jigar should choose a handoff cutoff date. If Vishwajeet's probability and metric artifacts are not UID-aligned and fully specified by that date, report only the Project S v2 metrics; do not combine or compare the two systems. Keep five-class and three-class results separate.

## Part 8 ? Request to Vishwajeet

**Drafted:** Could you please share: (1) `V_roberta_three_seed_metrics_v2.csv` with seed, dataset, split, N, label space, and metric definitions; (2) confirm whether `rb_probs_v2.parquet` is your intended file or provide `V_rb_probs_v2.parquet`, with UID and explicit p0-p4 label order; (3) each seed's `dev_predictions.parquet` and `dev_metrics.json`, plus checkpoint weights if you are claiming a saved fine-tuned model; and (4) the 12-question corrections list keyed by `question_id`, with corrected text or a clear ?no change? entry. Please identify the exact dev UID/split used and confirm no test rows are included.

## Phase 1 checkbox mapping

| Part | Status |
|---|---|
| 1 Artifact inventory | PARTIAL ? alternate probability file found; metrics, per-seed files, weights, and correction list missing. |
| 2 Notebook hygiene | DONE-evidenced ? headings and five empty code cells recorded. |
| 3 Fine-tuning evidence | PARTIAL ? source shows fine-tuning procedure; no run outputs or checkpoint weights found. |
| 4 Artifact checks | PARTIAL ? schema and full dev UID alignment verified; file lacks split/gold columns. |
| 5 Metric reconciliation | BLOCKED ? no numeric seed metrics or run outputs available. |
| 6 Block 42/49 plan | PARTIAL ? static plan prepared; neither block executed. |
| 7 Cutoff proposal | DONE-drafted ? awaits Jigar's cutoff date. |
| 8 Vishwajeet request | DONE-drafted ? checklist included above. |

**Remaining blockers:** obtain the seed metrics and predictions, saved checkpoint weights if claimed, and the 12-question correction list; confirm artifact ownership and exact label/metric definitions. Block 49 also remains blocked by the prohibition on opening test artifacts.
