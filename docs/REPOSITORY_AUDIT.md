# Project S Q&A Branch — Repository Audit

## Scope and evidence

Static audit of the local checkout at commit `8bd4723272307cebc01104b94b48734175cba5a8` (2026-11-15). The checkout has 527 tracked paths. No notebook, script, model, training job, test suite, or inference was run. No test-named file, test split, test output, ZIP, or PDF was opened. Statements tagged **Verified** come from source, metadata, or file hashes; **Reported** means an existing project report says so; **Unverified** means the audit could not establish it.

The tree is snapshot-heavy: the preceding Git-object inventory found 316 unique file contents among 527 tracked paths. File-type counts from that inventory were 64 Python files, 16 notebooks, 26 parquet files, 12 joblib files, 153 CSV files, and 115 JSON files; these categories do not cover every extension.

`git status --short` showed pre-existing untracked paths: `Jigar_QA_PHASE3_SETUP_SCRATCH_files/`, `archive/`, `drive_backup_20261107/A_submission_v2.zip`, `drive_backup_20261107/project_s_qa_v2_package.zip`, `project_s_qa/A_submission_v2.zip`, and `project_s_qa_backup_20261106_1957/A_submission_v2.zip`. They were left untouched. No tracked modifications were present before this audit.

## Repository map

| Area | Role and current state |
|---|---|
| `AGENTS.md`, `PROJECT_CONTEXT.md`, `README_FILES.txt` | Project restrictions and context. **Verified:** context and file guide describe an older November 3, 165-cell layout; the inspected updated notebook is 169 cells. |
| `notebooks/` | Original, working copies, backups, and updated notebook candidates. Source contains data preparation, training, evaluation, inference, demo, and historical artifact-writing cells. Never use Run All. |
| `project_s_qa/reports_v2/` | Operational scorer/config/report path used by the notebook. Contains `A_predict.py` and the root reference JSON; the root policy JSON is absent. |
| `project_s_qa/interim/` | Local DistilRoBERTa checkpoint and joblib artifacts. Hashes were inspected, artifacts were not loaded. |
| `project_s_qa/processed/` | Input banks and processed data, including the demo CSV. |
| `project_s_qa/A_submission_v2/` | Packaged submission snapshot with its own `reports_v2/`, policy, scorer metadata, rubric file, and artifact bundle. It is not the path Block 60 inserts by default. |
| `drive_backup_20261107/`, `project_s_qa_backup_20261106_1957/`, `_backups/` | Historical snapshots. Keep separate; do not treat them as live Drive state. ZIPs were not opened. |
| `block60/` | Standalone Block 60 source and draft demo questions; the notebook reads the CSV from the project Drive root. |
| `tools/` | `extracted_A_predict.py` is an older implementation; `comparison_table.json` is inventory/comparison data, not runtime code. |
| `PROJECT_S_QA_HANDOVER/` | Static handover package: inspection scorer mirror, draft question-bank/ingestion/validation modules, Block 64 demo wrapper, manifests and instructions. Block 64 is separate from the current Block 60 notebook. |
| `Project_S_QA_Evidence/` | Phase reports, experiment scripts, saved analysis outputs and runbooks. Evidence files do not replace source/runtime artifacts. |
| `.AI/`, `drive_backup_*`, `some files to fix`, `Session_Upload_8Nov` | Additional tracked context, snapshots and uploads. No cleanup or relocation was attempted. |

## Scorer and decision flow

**Verified:** operational import target is `project_s_qa/reports_v2/A_predict.py`; the file is 7,626 bytes, SHA-256 `ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053`. Thirteen local `A_predict.py` copies have identical bytes. The matching copy at `PROJECT_S_QA_HANDOVER/src/A_predict.py` is an inspection mirror, not Block 60's import target.

At inference (`A_predict.py`):

1. DistilRoBERTa receives `(question + " | " + reference_answer, student_answer)` (lines 61–75).
2. SBERT encodes reference and student answer, then uses cosine, embeddings, elementwise interactions and a length ratio as LR features (lines 92–101).
3. NLI scores student/reference-clause pairs plus the whole reference/student pair; the question is absent (lines 43–45, 115–129).
4. `component_probs()` returns 5-class component probabilities (`ft`, `sb`, `nl`) and NLI evidence (lines 110–136). Pooled SBERT/NLI LR models come from `pooled_lr_v2.joblib` (lines 104–106, 130–132).
5. `predict_batch()` equally averages the three 5-class outputs and collapses them to Incorrect/Partial/Correct (`_to3`, lines 56–57, 153). Optional temperature scaling follows (lines 154–157); the packaged policy records temperature 1.
6. Prediction is the 3-class argmax; confidence is the maximum 3-class probability. The policy threshold adds `low_confidence`; contradiction review can add `possible_contradiction` (lines 159–170).

There is no rubric lookup, question-ID validation, explicit relevance/on-topic gate, or concept-count Partial rule in `A_predict.py`. The classes “contradictory”, “irrelevant”, and “non_domain” all collapse into Incorrect. Partial is a learned class probability. The code does not guarantee that a semantically similar answer is relevant to the selected question.

`_load()` also loads `combiner_v1.joblib` at line 35 even on the pooled path, although pooled SBERT/NLI predictions use `pooled_lr_v2.joblib`. This makes the legacy artifact a startup dependency without using its LR heads for pooled output.

## Important file map

| File or group | Purpose / effect | Role |
|---|---|---|
| `project_s_qa/reports_v2/A_predict.py` | Frozen inference functions, model loading, probability pooling and review flags. | Runtime target; protected. |
| `project_s_qa/reports_v2/A_demo_reference_outputs_v2.json` | Stores scorer mode/hash, policy hash and reference demo cases. | Root runtime reference; internally inconsistent policy hash. |
| `project_s_qa/A_submission_v2/reports_v2/A_abstain_policy_v2.json` | Packaged policy: threshold 0.64, contradiction flag disabled, temperature 1. | Package config; not found at root runtime path. |
| `project_s_qa/A_submission_v2/reports_v2/A_predict_contract_v2.json` | Describes function/options. | Metadata; defaults/options conflict with actual scorer signature. |
| `project_s_qa/interim/ft_distilroberta_v1/` | Local FT model/tokenizer files. | Runtime artifact; frozen. |
| `project_s_qa/interim/pooled_lr_v2.joblib` | Pooled SBERT-LR and NLI-LR heads. | Runtime artifact; frozen. |
| `project_s_qa/interim/combiner_v1.joblib` | Loaded by `_load()` for base models. | Legacy startup dependency; frozen. |
| `notebooks/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb` | Current updated notebook candidate, 169 cells. Cell 159 contains Block 60. | Candidate; do not edit under this audit. |
| `Project_S_QA_Evidence/Phase_2/Jigar_QA_PHASE2_RUN_COPY_EXECUTED.ipynb` | Saved executed copy. Cell 157 includes policy hash validation absent from current updated copy and dated D. | Evidence candidate; source differs. Outputs not audited here. |
| `block60/block_60_voice_demo_cell.py` | Standalone source mirror for the demo. | Reference only. |
| `PROJECT_S_QA_HANDOVER/src/question_bank.py` | Loads/validates JSON question and rubric banks; retrieves by question ID (lines 6–32). | Draft infrastructure. |
| `PROJECT_S_QA_HANDOVER/src/ingestion/ingest.py` | JSON/CSV/XLSX ingestion, IDs, deduplication, draft rubric creation and no-overwrite outputs. PDF is deferred. | Draft infrastructure; not run. |
| `PROJECT_S_QA_HANDOVER/src/validation/question_bank.py` | Structural schema, label, ID, status and linkage checks. | Draft infrastructure; not run. |
| `PROJECT_S_QA_HANDOVER/src/block64_demo_bank.py` | Displays question/rubric and calls frozen scorer without rubric; reports `rubric_used_for_score=False` (lines 14–30). | Separate prototype, not integrated. |
| `tools/extracted_A_predict.py` | Older scorer copy, SHA-256 `11e897c74ec415737423fe35a3e1f61fcdc9f1668702fbc98a83e08cfd5d216b`; defaults to `scientsbank`, lacks pooled behavior. | Stale; not runtime. |

## Question-bank and rubric capability

The deployed scorer never reads a rubric. The package rubric file `project_s_qa/A_submission_v2/reports_v2/A_rubrics_v2.json` contains 251 records; all have non-empty `required_concepts`, with 248 `auto_draft` and 3 `demo` statuses. This is metadata only and does not establish educational correctness. The separate handover bank contains 12 linked Science questions and 12 rubrics, all `draft_unreviewed`; its questions have no populated `required_concepts`. Block 64 retrieves and displays rubric fields but does not pass them to the scorer.

Structural validation checks required keys, IDs, grade/difficulty/status, provenance, rubric linkage and label ranges. It does not determine whether an answer key is correct, concepts are sufficient, variants are equivalent, or subject alignment is educationally valid. The 12-question bank does not establish readiness for Social Science, Mathematics or English. Math needs notation/equivalence/unit criteria; English needs acceptable-language and meaning criteria; these remain proposed requirements.

## Evaluation and experiment map

| Experiment | Current evidence and limits |
|---|---|
| Baseline / Phase 7 | Existing reports describe saved development results as optimistic. Reported values include 56.37% accuracy, 52.70% Macro-F1 and QWK 0.4015 on 2,049 dev rows. They were not recomputed in this audit. Existing reports say 85% accuracy at 30% coverage was not achieved. |
| Experiment 1 | `Experiment_1_Path_Comparison/EXP1_REPRODUCE_v2.py` uses saved dev artifacts, validates UID/split alignment, compares Path A/B, and writes reports/CSVs. Existing v2 outputs are present. The code requests row and question-grouped bootstrap; the saved report describes the results as dev-only/optimistic. No script was run in this audit. |
| Experiment 2 | `Experiment_2_Component_Analysis/EXP2_REPRODUCE_v1.py` uses saved dev probabilities and alignment checks; its report/results are present. It is not model inference. The reproduction script was not run here. |
| Experiment 3 | `Experiment_3_Provenance_Audit/EXP3_REPRODUCE_AUDIT_v1.py` and its report are static provenance/leakage materials. Training UID overlap and pooled-LR fit provenance remain unresolved in the existing report. |
| Phase 8 | E1/E3 analyses and x0 export/analysis artifacts exist. `x1_deberta_train_v2.py` is a candidate training script; `x1_gate_check_v3.py` expects candidate dev predictions. They are not approval to train. Existing Phase 8 recommendation says Stage 1 is not approved/run and locked evaluation is blocked. |

Test files and splits were not opened. Existing project documentation records historical test exposure; any prior test numbers remain exploratory, and a clean locked-test result is not established.

## Dependencies and reproducibility

Static imports/source show Python with NumPy, joblib, PyTorch, Transformers, sentence-transformers, pandas/scikit-learn for analysis, and Gradio for the demo. Deployed scorer references hub IDs `cross-encoder/nli-deberta-v3-base` and `sentence-transformers/all-MiniLM-L6-v2`; cache/network availability is **Unverified**. Local DistilRoBERTa and LR artifacts are present by filename/hash, not loaded. Handover `docs/setup.md` records a historical environment, not a current lock. No tested lock file or clean-room reproduction was established.

## Priority risks

1. **High — policy/config drift:** root reference JSON's policy hash is `babf76f460d2a6516d9ef11d317f69ceddb0958dd67a2ce06d3b67496163ad25`; no matching local policy was found. Root policy is absent. Packaged JSON hash `ea5288e9…20aeb9` names available policy hash `b6548ede…f7e9ef9b`. If root policy is absent, scorer silently falls back to threshold 0.60 and contradiction review defaults enabled, unlike the packaged 0.64/disabled policy.
2. **High — evaluation optimism:** dev rows are used for analysis/model selection; only 27 dev questions are reported unseen. Historical test exposure prevents a clean locked-test claim.
3. **High — assessment validity:** no CBSE/student-answer or child pilot validation; the demo bank is draft-only.
4. **High — rubric gap:** rubrics are not used by the deployed scorer; the demo interface can pair a question with a manually edited reference.
5. **Medium — source duplication:** 13 same-hash scorer copies, stale extracted scorer, multiple notebooks and packages create import ambiguity.
6. **Medium — hidden dependency:** pooled path initializes `combiner_v1.joblib`.
7. **Medium — provenance:** FT model origin, hub caches, current Drive synchronization, and model-training provenance are not established by static source.
8. **High — execution safety:** historical notebook blocks write frozen artifacts; AGENTS.md forbids rerunning named blocks and says never Run All. Block 49 and Summary/cell 166 are prohibited by project records because they access test-related artifacts.

## Inspection limits

This is a static audit, not a runtime certification. Live Google Drive/cloud state, package/model cache, notebook execution provenance, educational correctness, and data-origin history are unverified. No source, notebook, data, model, backup or existing report was changed.
