# Setup and controlled use

## Environment evidence

`project_s_qa/A_submission_v2/reports_v2/A_run_manifest_v2.json` records a
historical run environment: Python 3.13.16, NumPy 2.1.3, pandas 2.2.3,
scikit-learn 1.6.1, PyTorch 2.11.0+cu130, Transformers 5.20.2, and
sentence-transformers 5.7.0. These are recorded values, not a verified current
environment or a tested lock. Joblib, Gradio, datasets, pyarrow and accelerate
versions were not specified there. `requirements.txt` reflects this distinction.

## Local question-bank tools

The basic JSON/CSV ingestion path uses the Python standard library. XLSX/XLS
requires pandas and an installed Excel reader. PDF ingestion is not implemented.
From the handover directory, the intended user-run pattern is:

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) 'src')
python -m ingestion.ingest --source INPUT.csv `
  --questions-out OUTPUT/questions.json `
  --rubrics-out OUTPUT/rubrics.json
```

The command refuses existing outputs. To preserve existing records, pass both
`--existing-questions` and `--existing-rubrics`; output paths must be new.
Human review is required before changing any draft status to reviewed or
approved. No `pip install` command was run or validated by Codex.

## Drive project and frozen scorer

The prior Colab runbook uses `/content/drive/MyDrive/project_s_qa`. Verify the
actual mounted folder before using it. Set `PROJECT_S_ROOT` to that verified
root; the scorer builds its `interim/` and `reports_v2/` paths from the root.
Expected files include:

- `reports_v2/A_predict.py`, `A_abstain_policy_v2.json`,
  `A_predict_contract_v2.json`, and reference/scorer metadata;
- `interim/pooled_lr_v2.joblib`;
- `interim/ft_distilroberta_v1/{config.json,model.safetensors,tokenizer_config.json,tokenizer.json}`;
- cached or otherwise authorized access to
  `cross-encoder/nli-deberta-v3-base` and
  `sentence-transformers/all-MiniLM-L6-v2`.

Do not use the copy under this package as a replacement for the live scorer.
Verify hashes against `docs/frozen_files_manifest.csv`. The local root
`project_s_qa/reports_v2/` currently lacks `A_abstain_policy_v2.json`; the
policy exists under `project_s_qa/A_submission_v2/reports_v2/`. Live Drive
availability is unverified. Do not proceed with a runtime whose policy path is
uncertain.

## Notebook and demo order

No Run All. Never run Block 49 or cell 166 (Summary). The Phase 2 run copy
record lists Block 59 cell 157, Block 60 cell 159, Block 61 cell 161, and
Block 62 cell 163. Follow the copied Phase 3 runbook for demo evidence. Save a
new executed notebook under a new name; do not overwrite either included
notebook.

Block 64 is supplied separately. Before using it, place the handover package
in an authorized Drive folder and set `PROJECT_S_HANDOVER_ROOT` to that actual
path. The run copy and the `PROJECT_S_HANDOVER_ROOT` location were not
uploaded or verified by this task. Paste Block 64 only into a separate new
run copy after Jigar approves and selects D versus the executed run copy.

## User-run validation

The `tests/` directory contains drafted unit tests. They were not run. After
Jigar selects an isolated environment and approves, the intended user command
is `python -m pytest tests/`. Capture the environment and output; do not mark
tests passed until that command is run successfully by the user.
