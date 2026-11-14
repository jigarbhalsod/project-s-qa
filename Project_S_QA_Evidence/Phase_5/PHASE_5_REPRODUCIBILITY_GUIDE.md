# Phase 5 Reproducibility Guide

## Scope and safe use
The working notebook is `notebooks/Jigar_Q&A_Branch_Baseline_COPY.ipynb` (167 cells). Read `AGENTS.md`, `PROJECT_CONTEXT.md`, and the notebook's READ FIRST cell before work. Never use Run All. Most earlier cells are one-time artifact producers; re-running them can rewrite frozen outputs. This guide documents the existing pipeline and does not certify a clean-room reproduction.

## Project and Drive layout
Colab project root: `/content/drive/MyDrive/project_s_qa`.

- `processed/`: unified labeled/split data, rubrics, final review policy inputs; Block 60 also reads `cbse_demo_questions_v1.csv`.
- `interim/`: `combiner_v1.joblib`, `pooled_lr_v2.joblib`, and `ft_distilroberta_v1/{config.json,model.safetensors,tokenizer_config.json,tokenizer.json}`.
- `reports_v2/`: deployed `A_predict.py`, `A_demo_reference_outputs_v2.json`, `A_deployed_scorer_v2.json`, `A_abstain_policy_v2.json`, evaluation outputs and `A_*` diagnostics.
- `demo/`: reference inputs/outputs and demo-local scorer used by Block 45.
- `notebooks/`: the working copy and preserved backups.

The scorer defaults to the Drive root above. `PROJECT_S_ROOT` can override the root for a differently named mounted folder. Check the actual location before execution; local staging does not prove Drive synchronization.

## Recorded environment and packages
The archived `A_run_manifest_v2.json` records this environment snapshot: Python 3.13.16 on Linux x86_64; NumPy 2.1.3; pandas 2.2.3; scikit-learn 1.6.1; torch 2.11.0+cu130; Transformers 5.20.2; sentence-transformers 5.7.0. These are historical recorded values, not a pinned requirements file or a statement about the current Colab image.

The notebook/scorer imports or uses NumPy, pandas, scikit-learn, joblib, PyTorch, Transformers, sentence-transformers and Gradio. Data preparation also uses datasets and pyarrow; some training cells use accelerate. Whisper inference uses Transformers. The archived manifest does not specify versions for joblib, Gradio, datasets, pyarrow or accelerate. Do not infer or install unrecorded versions as part of this guide.

## Model files and caches
- Fine-tuned checkpoint: `interim/ft_distilroberta_v1/` (config, safetensors weights, tokenizer configuration and tokenizer JSON).
- Logistic-regression assets: `interim/combiner_v1.joblib` and `interim/pooled_lr_v2.joblib`.
- Model identifiers used by the scorer/demo: `cross-encoder/nli-deberta-v3-base`, `sentence-transformers/all-MiniLM-L6-v2`, `distilroberta-base` for fine-tuning, and `openai/whisper-small` for voice input.
- A fresh runtime needs these models available in its cache or a permitted model-download path. Cache availability was not verified in this documentation task. Missing assets should be treated as a blocker, not silently replaced.

## Data and scorer contract
The scorer accepts nonempty strings for `question`, `reference_answer`, and `student_answer`; `dataset` defaults to `pooled`. It returns `pred_label`, `pred_score` (0 incorrect, 1 partial, 2 correct), `confidence`, class probabilities, NLI/concept evidence, `needs_teacher_review`, and review reasons. The deployed pooled path averages the 5-way probabilities from DistilRoBERTa, SBERT-LR and NLI-LR, then maps to the 3-level score and applies the saved temperature/review policy.

The final policy file is `reports_v2/A_abstain_policy_v2.json`; its confidence threshold is 0.64 and its separate contradiction flag is disabled. Verify this file and `reports_v2/A_deployed_scorer_v2.json` exist before interpreting final decisions. A_predict may fall back to a provisional policy if the final file is absent.

## Controlled execution order
1. Confirm the mounted Drive root and required artifact paths; inspect the READ FIRST cell.
2. The notebook's documented saved-results workflow starts with the final Summary cells, then runs Block 59, Block 60, Block 61 and Block 62 one at a time, in that order. Do not run other cells unless a separate plan authorizes them.
3. Block 59 measures scorer latency; it is not a training step.
4. Block 60 launches the Gradio question/voice demo. It requires `processed/cbse_demo_questions_v1.csv` with `question_id`, `question_text`, and `reference_answer`; it uses the pooled scorer and Whisper-small. Voice testing should use consenting adults only.
5. Blocks 61-62 are diagnostics/timing cells. They print evidence and are not training or validation.
6. Save a separate executed notebook and capture outputs if execution is authorized. Do not overwrite the source notebook or backups.

For the historical model-building pipeline, the recorded order in `A_run_manifest_v2.json` is Blocks 1-12 once, then 13-24 in the listed dependency order, followed by self-contained later blocks that load saved Drive artifacts. This is provenance documentation, not permission to rerun frozen producers. In particular, do not repeat training, locked-test, or freeze-writing cells without a new approved plan.

## Demo and expected outputs
- `A_predict.predict(question, reference_answer, student_answer, dataset="pooled")` returns one result dictionary as described above.
- Block 45 compares the 15 stored reference cases: predictions and review flags must match and confidence differences must be at most 0.001. Parity is not an accuracy estimate.
- Block 60 loads the question dropdown from the CSV and provides typed and microphone audio inputs. Audio transcription and scoring are separate steps; the demo is not a pilot or curriculum validation.
- Keep execution output, errors, and environment notes with a separate executed notebook. Current local saved outputs do not establish a complete execution history.

## Common blockers
- Drive not mounted, wrong root, or required files missing.
- CSV missing one of the required columns.
- Missing final scorer/policy or pooled model artifact; provisional policy fallback can alter review behavior.
- Missing pretrained model cache, incompatible package/runtime, or unavailable GPU for NLI-heavy work.
- Gradio microphone API differences or browser microphone permissions. Do not install packages or change Gradio arguments without an approved patch.
- No pinned environment file and no independent confirmation that current Drive content matches local files.
