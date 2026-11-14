# Experiment 3 — component provenance, leakage and evaluation integrity

Audit date: 10 Nov 2026. Labels distinguish verified static evidence, measurements on safe dev artifacts, reported historical values, and unresolved claims.

## Executive conclusion

**Overall: PARTIAL PASS — SOME PROVENANCE UNVERIFIED.** [Verified] The three saved dev artifacts each contain 2,049 unique UIDs; their UID sets match, and dataset, split, question_id and label5 agree by UID. The split values are dev_ua/dev_uq only. Component and deployed probabilities are finite and normalized within 1e-5. Path A labels from the saved component export agree with deployed Path A labels on all 2,049 rows.

**[Unverified] It cannot be established that all 2,049 dev UIDs were excluded from fitting every exact component artifact that generated the saved probabilities.** No verified training UID manifest, pooled-LR fit record, or per-row prediction-generation manifest was found. Notebook recipes use train rows for model fitting but use dev for epoch/C selection. The actual deployed pooled_lr_v2.joblib provenance is not connected to those recipes.

**[Verified] No confirmed development-label fitting leakage was found in the inspected source.** That does not establish absence of leakage. The legacy combiner_v1 final meta-model is fit on all dev rows, but A_predict pooled mode uses a separate pooled_lr_v2 artifact. The policy temperature and confidence threshold are dev-derived and evaluated on the same dev population, so selective metrics are optimistic.

## Scope and boundaries

- [Verified] Read AGENTS.md, PROJECT_CONTEXT.md, architecture/reproducibility docs, Phase 7/8 evidence, Exp1/Exp2 reports/manifests, A_predict.py and notebook source cells.
- [Verified] Notebook source was read as JSON source fields only; no notebook ran and stored outputs were not used. A_predict.py was read as text only. Joblib and safetensors were hashed, never deserialized or loaded.
- [Verified] Read only dev_text_2049.parquet, A_component_probs_v7.parquet and A_deployed_dev_probs_v2.parquet as data. No raw mixed split was opened.
- [Verified] A Phase 7 report read during the requested documentation review contained previously published exploratory-test prose. It was not used, copied or expanded. No test split or test-output artifact was opened.
- [Reported / Unverified] The Notion roadmap is a proposed plan and marks its own status unverified; it does not establish that a training run occurred.
- [Verified] Exp2 records the approved 2,049-row primary population and 2,030-row content-unique sensitivity population. Raw-source lineage remains unverified.

## Input artifacts and validation

| Artifact | Bytes | SHA-256 | Finding |
|---|---:|---|---|
| Project_S_QA_Evidence/Phase_3/dev_text_2049.parquet | 107,715 | 21e7305557825b392a297fc4558b73e1161fcefb07d82c9f802e33c877836ea2 | [Verified] 2,049 rows/UIDs; dev_ua/dev_uq only |
| Project_S_QA_Evidence/Phase_8_Accuracy_Max/A_component_probs_v7.parquet | 444,822 | 71dd07621bb838b38af1932f43d985059a6a69e61d39361e6a5063eb5bdc5f88 | [Verified] 2,049 aligned rows; ft/sb/nl p0-p4, seven NLI features, pooled p3 |
| project_s_qa/A_submission_v2/reports_v2/A_deployed_dev_probs_v2.parquet | 131,382 | 2e29a708152b288019a9fa50b55b9d823781e4bbe0144cd5ee533fee9ddb5b0e | [Verified] 2,049 aligned rows; deployed d_p0-p4 |
| project_s_qa/A_submission_v2/reports_v2/A_predict.py | 7,626 | ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053 | [Verified] identical hash in three local copies |

[Verified] All three UID sets match; dataset, split, question_id and label5 agree by UID. Probability columns have no nulls and row sums are within floating-point tolerance of one. A_predict.py:13 defines LABEL5_ORDER; lines 56-57 map indices 1/3/4 to Incorrect, 2 to Partial, 0 to Correct. Gold mapping agrees with stored score_ours.

[Reported / Verified-source] Exp1 records 17 exact-content groups and 19 excess rows, with the approved 2,030-row sensitivity set retaining the lexicographically smallest UID per group. [Unverified] The train/dev cross-content comparison cannot be done without a verified train-only manifest.

## Component provenance

### DistilRoBERTa

- [Verified source] Working notebook Block 19, code cell 50: when the checkpoint directory is absent, training rows are selected by split=train. Recipe: distilroberta-base, 5 labels, seed 42, 3 epochs, LR 3e-5, batch 32, max length 160, weight decay 0.01, warmup 10%. Each epoch is selected using mean dev Macro-F1. If a checkpoint directory exists, the cell loads it instead of training; source alone does not identify the current weights' origin.
- [Verified source] Inference forms question + delimiter + reference as the first tokenizer sequence and student answer as the second; max_length=160 (A_predict.py:60-75). The base identifier is distilroberta-base in cell 50; inference loads the local FT directory (A_predict.py:30-31).
- [Verified metadata] Current model.safetensors exists and hashes to 671e70acf931c6dedd28ebff73baccfa3acf3b07dba13cb3eb15fc39f04761fd. Config says five labels and Transformers 5.20.1. We did not load it.
- [Unverified] No training UID list or generation log ties this hash to the dev probabilities. The 30 Oct run manifest did not hash the >100 MB weights; local model files are dated 6 Nov. Timestamps do not prove continuity or replacement.

### SBERT-LR

- [Verified source] Notebook cells 40 and 52 use frozen sentence-transformers/all-MiniLM-L6-v2 embeddings. Legacy fit_select fits Logistic Regression on train rows and selects C from 0.3, 1, 3 on dev Macro-F1.
- [Verified source] Deployed inference embeds only reference_answer and student_answer; features include absolute difference, product, cosine and log length ratio (A_predict.py:92-101). Pooled mode uses the estimator from pooled_lr_v2.joblib (104-107, 130-135).
- [Verified metadata] pooled_lr_v2.joblib exists, size 63,625 bytes, SHA-256 216493152a1b7ae2143f0fc60ce2eed6ffc735f40676e308455225b1b55aa96f.
- [Unverified] It was not deserialized. No fit script, UID list, chosen C, seed or generation manifest proves it followed the legacy recipe.

### NLI-LR

- [Verified source] A_predict.py loads cross-encoder/nli-deberta-v3-base (lines 11, 26, 32). NLI features use student/reference sentence pairs plus a reverse reference/student pair (43-45, 78-89, 110-129). Pooled mode loads the LR estimators from pooled_lr_v2.joblib (104-107, 130-135).
- [Verified source] Notebook cell 43 extracts NLI features; cell 52 fits the legacy NLI-LR on train and selects C on dev.
- [Unverified] The deployed estimator is not tied to the legacy recipe, training UIDs, feature-generation version, hub revision or seed. Its internals were not loaded.

## Leakage and fitting review

| Mechanism | Finding |
|---|---|
| Training/dev UID overlap | [Unverified] No independently verified train UID manifest was found. The development UID set is verified, but overlap size and percentage cannot be reported; do not call it zero. |
| DistilRoBERTa | [Verified source] Supervised update rows use split=train. Dev is used for epoch selection, so dev metrics are selection-biased. Actual checkpoint provenance is unverified. |
| SBERT/NLI Logistic Regression | [Verified source] Legacy recipes fit on train and select C on dev. [Unverified] Exact fit data for deployed pooled_lr_v2 is unknown. |
| Legacy stacker | [Verified source] Block 20 (cell 52) creates grouped 5-fold OOF predictions for stacker evaluation, then fits the final combiner_v1 on all dev rows. This is a dev-fitted legacy meta-model, not the deployed pooled score path. |
| Fitted preprocessing | [Verified source] Legacy TF-IDF is fit on train only (cell 38), and is not a deployed component. The deployed joblib internals cannot be inspected, so any scaler or fitted transform inside pooled_lr_v2 is unverified. |
| Frozen feature extraction | [Verified source] Notebook cells 40 and 43 build cached embeddings/NLI features from the in-memory data table. The encoder weights are not updated and the features do not use labels. Historical execution scope is unverified; this is not proof of no data exposure. |
| Calibration and review threshold | [Verified] Temperature and 0.64 threshold are derived from dev and then reported on dev (notebook cell 102 and policy files). Selective metrics are optimistic; this is not evidence of supervised fitting leakage in the main argmax labels. |
| Duplicate contamination | [Unverified] Exp1 verifies dev duplicate policy; no train UID/content manifest is available for a cross-split comparison. |

## OOF, prediction chain and probability discrepancy

- [Verified source] Legacy stacker OOF predictions are generated with question-grouped folds in notebook cell 52; the final saved stacker is fit on all dev rows. Do not confuse that with independent evaluation of its final fitted estimator.
- [Verified source] A_predict dataset=pooled averages ft/sb/nl five-class vectors and collapses them; it does not use combiner_v1 as a meta-model (lines 130-157). No pre-registration proves this rule was fixed before looking at dev.
- [Unverified] No OOF fit history was found for the pooled_lr_v2 estimators. Training predictions, if any, cannot be characterized for the deployed LR models.
- [Partially verified] Saved probability outputs align with exact dev UIDs, but contain no component hashes, code revision or run environment linking rows to exact weights.
- [Verified calculation] Raw mean of saved ft/sb/nl probabilities differs from deployed d_p0-d_p4 by max absolute 0.001141848285589997. Exported p3 differs from collapse of that raw mean by 4.094218253314352e-08. Path A labels agree on all 2,049 rows.
- [Unverified] Available files do not explain the 0.001142 probability discrepancy. Rounding or floating-point order is not established as the cause; artifact-generation differences are possible but unproven.

## Evaluation integrity and reproducibility

- [Verified] Exp1/Exp2 use identical UID-aligned dev rows and the approved 2,049 primary / 2,030 sensitivity populations. The audit independently checked dev schemas, splits, UID sets and metadata; it did not rerun the reproduction scripts.
- [Verified source] Exp2 reproduction code uses 10,000 paired row and question-group bootstrap draws with seed 20261110; groups are dataset::question_id. It was inspected, not executed.
- [Reported from saved dev reports] Path A: accuracy 56.37%, Macro-F1 52.70%, QWK 0.4015. Path B: accuracy 58.03%, Macro-F1 55.66%, QWK 0.4318. These are dev, optimistic, not independent confirmation.
- [Verified] The saved policy threshold 0.64 and temperature were derived on dev and reported on dev. The threshold does not define full-population argmax accuracy.
- [Unverified] No untouched locked confirmation set was verified in scope.
- [Partially verified] Experiment 2 metrics can be recomputed from saved dev predictions and its script; regenerating the exact component probabilities from training is not fully reproducible.

## Direct answers and final status

| Question | Answer |
|---|---|
| Can we trust 56-58% as a valid held-out evaluation? | [Partially verified] Saved-dev arithmetic and UID alignment pass. [Unverified] Exact fit UID exclusion and artifact identity are not established. Present only as dev, optimistic. |
| Were all dev UIDs excluded from fitting? | [Unverified] No overlap count can be established. |
| Were fitted preprocessing steps trained on dev? | [Unverified] Deployed LR internals. [Verified source] Legacy TF-IDF is train-fit; legacy final stacker is fit on all dev. |
| Were training predictions used to train the ensemble, and were they OOF? | [Unverified] Deployed pooled LR history. [Verified source] Legacy stacker evaluation uses grouped OOF predictions, then fits final estimator on all dev. |
| Are all component outputs tied to exact model versions? | [Unverified] Current source/artifact hashes exist; saved probabilities do not record them. |
| Is the 0.001142 difference explained? | [Unverified] No; the mapped labels still agree. |
| Does every component receive question/reference/student? | [Verified] Only DistilRoBERTa receives question text; all three receive reference and student text. |
| Are rubrics used at inference? | [Verified] No. A_predict does not load rubric fields; NLI “concepts” are sentences split from the supplied reference (lines 43-45). |
| Can Exp2 be reproduced? | [Partially verified] Metric calculations can be reproduced from saved dev files; component regeneration is not traceable to exact training artifacts. |
| Evidence needed next | [Proposed] Train UID lists; training configs/logs; exact estimator/checkpoint hashes and revisions; probability-generation code/manifest; pinned environment; raw-data lineage; independent confirmation protocol. |
| Is Experiment 4 safe? | [Proposed] **BLOCKED UNTIL PROVENANCE IS RESOLVED.** Resolve artifacts and approve an evaluation protocol before training or scorer changes. |

| Component | Training provenance | Dev exclusion | Checkpoint identity | Prediction provenance | Reproducibility |
|---|---|---|---|---|---|
| DistilRoBERTa | PARTIALLY VERIFIED | UNVERIFIED | UNVERIFIED linkage | PARTIALLY VERIFIED | PARTIAL |
| SBERT-LR | UNVERIFIED for deployed pooled estimator | UNVERIFIED | estimator hashed; fit unknown | PARTIALLY VERIFIED | PARTIAL |
| NLI-LR | UNVERIFIED for deployed pooled estimator | UNVERIFIED | estimator hashed; fit unknown | PARTIALLY VERIFIED | PARTIAL |

**Overall Experiment 3: PARTIAL PASS — SOME PROVENANCE UNVERIFIED.**
**Experiment 4 readiness: BLOCKED UNTIL PROVENANCE IS RESOLVED.** This is a
provenance gate, not evidence of confirmed leakage.

