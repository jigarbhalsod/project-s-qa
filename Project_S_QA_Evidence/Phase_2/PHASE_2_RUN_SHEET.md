# Project S ? Phase 2 Colab run sheet

**Drafted ? no cells have been run.** Use only the verified notebook D copy
provided to Jigar. Never select ?Run all?. The Summary cell pair is blocked as
written because its code reads `reports_v2/A_test_results_v2.csv` (cell 166,
source line 46). Skip Summary; do not open that artifact.

## Before opening cells

1. **Drafted:** Upload/open the approved notebook in Colab; select a T4 GPU.
2. **Drafted:** Mount Drive and confirm the root is
   `/content/drive/MyDrive/project_s_qa`.
3. **Drafted:** Confirm required package imports and cached model assets before
   running. Do not install or fetch anything under the current no-install / no-
   download restriction. Cache availability is **Unverified**.
4. **BLOCKED pending approval:** Block 59's proposed policy-hash check is not
   present in D. Do not treat its current scorer-hash check as policy
   verification. Apply only through the separately approved new run-copy step.
5. **Drafted:** Confirm the uncorrected `draft_unreviewed` CBSE CSV is approved
   for a demo run; the corrections list was not received.

## Individual run order (after blockers are resolved)

| Order | Cell(s) | Action and expected source output | On any failure |
|---:|---:|---|---|
| 1 | 157 | **Drafted:** Run Block 59 once. Expected anchors: `Colab Runtime Hardware`, `Single-answer latency (median of 20 runs)`, and `Batch latency for 15 items (median of 20 runs)`. | **Drafted:** Stop; copy the full error; do not run the next block. |
| 2 | 159 | **Drafted:** Run Block 60 once. Expected: Gradio renders the Q&A interface; dropdown, microphone, editable transcript, and Score button are available. | **Drafted:** Stop; copy the full error; do not run the next block. |
| 3 | 161 | **Drafted:** Run Block 61 once. Expected: per-negation rows showing ft, sb, and nl predicted label/probability. | **Drafted:** Stop; copy the full error; do not run the next block. |
| 4 | 163 | **Drafted:** Run Block 62 once. Expected: median stage timings for `single` and `batch15`, including DistilRoBERTa, NLI, SBERT, component total, and predict_batch. | **Drafted:** Stop; copy the full error; do not run further cells. |

**Verified source limitation:** Block 62 reports medians over 20 runs for one
case and a 15-case batch; it does not print batch-32 timings or p95. Block 59
also reports median single and batch-15 latency only.

## Evidence to record

| Block | Ran (yes/no) | Full error text | Output summary | Batch-1 median / p95 | Batch-32 median / p95 | Frozen-file mtime check | Screenshot filename(s) |
|---|---|---|---|---|---|---|---|
| Summary (blocked) |  |  |  |  |  |  |  |
| 59 / cell 157 |  |  |  |  |  |  |  |
| 60 / cell 159 |  |  |  |  |  |  |  |
| 61 / cell 161 |  |  |  |  |  |  |  |
| 62 / cell 163 |  |  |  |  |  |  |  |

**Verified source limitation:** batch-32 and p95 are not printed by the current
Block 62 code; mark those fields ?not printed? unless other approved evidence
provides them. Block 59/62 timing medians should be copied exactly, not
recomputed or rounded.

## Frozen-file safety check

**Drafted:** Compare timestamps before and after the run for the protected
Drive project files: `reports_v2/A_predict.py`,
`reports_v2/A_demo_reference_outputs_v2.json`,
`reports_v2/A_abstain_policy_v2.json`, `reports_v2/A_demo_parity_v2.json`,
`interim/combiner_v1.joblib`, `interim/pooled_lr_v2.joblib`, all four files in
`interim/ft_distilroberta_v1/`, frozen v1 outputs
`interim/ft_probs_v1.parquet`, `interim/stack_features_v1.parquet`,
`interim/abstain_config_v1.json`, `interim/scored_dev_v1.parquet`, and
`processed/question_bank_v1.csv`. Also preserve all datasets, split files,
gold labels, and backups. The runtime may write model-cache/temp files outside
these project artifacts.

**Drafted PowerShell template:** substitute the actual Google Drive for
Desktop root only after confirming it locally; this does not verify cloud sync.
Run once before and once after, saving the two outputs for comparison:

```powershell
$root = (Read-Host 'Full local My Drive path ending in project_s_qa')
$rel = @('reports_v2\A_predict.py','reports_v2\A_demo_reference_outputs_v2.json','reports_v2\A_abstain_policy_v2.json','reports_v2\A_demo_parity_v2.json','interim\combiner_v1.joblib','interim\pooled_lr_v2.joblib','interim\ft_distilroberta_v1\config.json','interim\ft_distilroberta_v1\model.safetensors','interim\ft_distilroberta_v1\tokenizer_config.json','interim\ft_distilroberta_v1\tokenizer.json','interim\ft_probs_v1.parquet','interim\stack_features_v1.parquet','interim\abstain_config_v1.json','interim\scored_dev_v1.parquet','processed\question_bank_v1.csv')
$rel | ForEach-Object { $p = Join-Path $root $_; if (Test-Path -LiteralPath $p) { Get-Item -LiteralPath $p | Select-Object FullName,Length,LastWriteTime } else { [pscustomobject]@{FullName=$p;Length='MISSING';LastWriteTime=''} } }
```

**Unverified:** local timestamp changes do not prove Google Drive cloud
synchronization status.
