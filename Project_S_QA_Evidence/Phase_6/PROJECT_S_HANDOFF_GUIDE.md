# Project S Q&A Handoff Guide

## Start here
1. Read `AGENTS.md` for safety rules.
2. Read `PROJECT_CONTEXT.md`, but note it is dated 3 Nov and contains stale 165-cell/reference-status details. Use the Phase 4 and Phase 5 evidence plus this guide for the later state; reconcile the stale root docs in a separately approved task.
3. Read `Project_S_QA_Evidence/Phase_4/PHASE_4_FINAL_CHECKLIST.md` and the three Phase 5 reports.
4. The active notebook is `notebooks/Jigar_Q&A_Branch_Baseline_COPY.ipynb` (167 cells). The attachment's `project_s_qa/notebooks/` path is not the current location.
5. Never use Run All. Do not train, overwrite frozen artifacts, or execute cells outside an explicitly approved order.

## Directory map
```text
Project 4/
  AGENTS.md, PROJECT_CONTEXT.md, README.md, README_FILES.txt
  notebooks/
    Jigar_Q&A_Branch_Baseline_COPY.ipynb
    Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb
    backups/                 preserved notebook snapshots
    reference/               historical notebook(s); confirm availability
  project_s_qa/
    processed/               source/split data and demo CSV
    interim/                 model and feature artifacts
    reports_v2/              deployed scorer, reference JSON, stage manifest
    A_submission_v2/         extracted submission snapshot
    A_submission_v2.zip      verified archive of the snapshot
  Project_S_QA_Evidence/
    Phase_3/, Phase_4/, Phase_5/, Phase_6/
  block60/, tools/, archive/
```

`A_submission_v2.zip` was CRC-checked and compared with the extracted folder: 55 files, zero path/size/hash differences. Its `A_submission_manifest_v2.json` lists 54 payload files; the 55th ZIP entry is the manifest itself.

## Important files
| Path | Purpose |
| --- | --- |
| `notebooks/Jigar_Q&A_Branch_Baseline_COPY.ipynb` | Authoritative editable notebook; 167 cells. |
| `notebooks/backups/` | Preserved source snapshots; do not edit or replace. |
| `project_s_qa/reports_v2/A_predict.py` | Inference implementation; pooled mode is the deployed scorer. |
| `project_s_qa/reports_v2/A_demo_reference_outputs_v2.json` | 15 reference cases, pooled mode and expected scorer hash. |
| `project_s_qa/reports_v2/A_runtime_stage_manifest_v2.json` | Local staging manifest for eight runtime assets. |
| `project_s_qa/interim/pooled_lr_v2.joblib` | Pooled SBERT/NLI logistic-regression assets. |
| `project_s_qa/interim/combiner_v1.joblib` | Earlier stacking/base-model artifact; not another pooled ensemble component. |
| `project_s_qa/interim/ft_distilroberta_v1/` | Fine-tuned model and tokenizer files. |
| `project_s_qa/processed/cbse_demo_questions_v1.csv` | Block 60 dropdown data; draft questions, not validation data. |
| `project_s_qa/A_submission_v2/reports_v2/` | Archived metrics, final policy, scorer manifests and diagnostics. |
| `Project_S_QA_Evidence/Phase_4/` | Freeze, parity and archive verification records. |
| `Project_S_QA_Evidence/Phase_5/` | Notebook docs, limitations and reproduction guide. |
| `Project_S_QA_Evidence/Phase_6/` | Master docs, architecture, experiment log, handoff and import guide. |

The local README_FILES and PROJECT_CONTEXT have stale inventory/status entries. Do not assume their 165-cell and reference-absent statements describe the current Phase 4/5 state.

## Scorer and runtime assets
Colab root is `/content/drive/MyDrive/project_s_qa`; `PROJECT_S_ROOT` overrides this default. Verify actual mount paths and cloud contents before execution.

Required scorer assets include `reports_v2/A_predict.py`, `reports_v2/A_abstain_policy_v2.json`, `reports_v2/A_deployed_scorer_v2.json`, the fine-tuned DistilRoBERTa directory, `interim/pooled_lr_v2.joblib`, and the supporting `interim/combiner_v1.joblib` used by the loader for non-pooled modes. Block 45 additionally needs `A_demo_reference_outputs_v2.json`; Block 60 needs `processed/cbse_demo_questions_v1.csv` with `question_id`, `question_text`, `reference_answer`. The reference JSON and A_predict hashes match in the local Phase 4 check. Local staging does not prove Drive sync.

Model identifiers: `cross-encoder/nli-deberta-v3-base`, `sentence-transformers/all-MiniLM-L6-v2`, fine-tuned DistilRoBERTa checkpoint, and `openai/whisper-small` for voice. Cache availability is unverified. Do not substitute a model silently.

## Environment
The archived run manifest recorded Python 3.13.16, NumPy 2.1.3, pandas 2.2.3, scikit-learn 1.6.1, torch 2.11.0+cu130, Transformers 5.20.2, sentence-transformers 5.7.0. Treat these as a historical snapshot, not a lockfile or current Colab guarantee. Versions for Gradio, joblib, datasets, pyarrow and accelerate are not recorded. No pinned requirements file was found.

## Execution guidance
- Follow the notebook READ FIRST instructions and the current project safety rules.
- Do not run all or repeat historical producers/training/frozen-test blocks.
- The notebook's documented diagnostic order is Summary, then Block 59, Block 60, Block 61, Block 62, one at a time, after paths and dependencies are checked.
- Block 45 is a parity check and Block 58 writes a fixed-name manifest and ZIP. Both have side effects; use only under a specific approved plan and preserve existing targets first.
- For a single inference request, use `A_predict.predict(question, reference_answer, student_answer, dataset="pooled")`. It returns label/score, confidence, probabilities, NLI evidence and review status.
- Block 60 launches the Gradio demo. The question dropdown comes from the CSV. Voice input uses Whisper-small; adult-only testing is the documented boundary. The temporary share URL is not a permanent deployment.

## Current state and priorities
- Phase 4: PASS WITH LIMITATIONS; archive and extracted files match locally.
- Phase 5: documentation changes validated; no notebook cells were run.
- Phase 6: local documentation package prepared; Notion pages were inspected but not changed.
- The 85% accuracy at 30% coverage target remains unmet; grouped-CV estimate is 74.77% at 31.33% coverage.
- Test metrics remain exploratory, with test sets seen in v1.
- No pilot student-answer validation or validated CBSE/Indian schoolchildren evaluation.
- No separate executed notebook or authenticated execution counts; Blocks 59-62 have no saved local outputs. Drive sync and model-cache availability remain unverified.

Next development priorities, in order: verify runtime provenance and cloud assets; obtain teacher-reviewed student answers and a proper held-out evaluation; improve unseen-question and negation/contradiction behavior; evaluate unrelated-answer handling and teacher-review calibration. Keep this separate from frozen artifacts and record all new experiments in new versioned outputs.

