# X0 export static review and Colab run sheet

**Verified (source):** Reviewed `x0_export_component_probs_v7.py` and
`project_s_qa/reports_v2/A_predict.py` as text only. No cell, model, or script
was run. Findings about unseen rows are **dev-only, optimistic**.

## Export interface and status

| Argument | Must point to |
|---|---|
| `--dev-text` | Dev-only text parquet, expected at `/content/dev_text_2049.parquet`; not opened here. |
| `--dev-probs` | `A_deployed_dev_probs_v2.parquet`, expected in `project_s_qa/reports_v2/`. **BLOCKED:** absent locally, so its column names and row count are unavailable. Drive availability is Unverified. |
| `--a-predict-dir` | Directory containing the paired `A_predict.py`, normally `.../project_s_qa/reports_v2`. |
| `--project-root` | Project S root containing `reports_v2/` and `interim/`; the v7 script requires `--a-predict-dir == <root>/reports_v2`. |
| `--output` | New parquet output outside `reports_v2`, preferably under `/content/phase8_tmp/`; must not already exist. |
| `--limit` | `16` for a no-write smoke run; `0` for all rows and the only mode that writes the normal parquet. |

**BLOCKED — exact expected command, once the missing dev-probability file is
available in Drive:**

```text
!python /content/x0_export_component_probs_v7.py --dev-text /content/dev_text_2049.parquet --dev-probs /content/drive/MyDrive/project_s_qa/reports_v2/A_deployed_dev_probs_v2.parquet --a-predict-dir /content/drive/MyDrive/project_s_qa/reports_v2 --project-root /content/drive/MyDrive/project_s_qa --output /content/phase8_tmp/A_component_probs_v7.parquet --limit 16
!python /content/x0_export_component_probs_v7.py --dev-text /content/dev_text_2049.parquet --dev-probs /content/drive/MyDrive/project_s_qa/reports_v2/A_deployed_dev_probs_v2.parquet --a-predict-dir /content/drive/MyDrive/project_s_qa/reports_v2 --project-root /content/drive/MyDrive/project_s_qa --output /content/phase8_tmp/A_component_probs_v7.parquet --limit 0
```

The current file is not locally available at the specified path. Do not run
either command until the dev parquet, model artifacts, and paired scorer are
confirmed present. A nonzero exit, assertion, `FAIL` parity tier, or missing
input means STOP; save the full console error. A parity-failure run writes
only the named quarantine parquet, not a valid result.

## Export contents and signal

**Verified (v7 source):** Output metadata columns are `uid`, `dataset`,
`split`, `question_id`, `label5`; component columns are `ft_p0`–`ft_p4`,
`sb_p0`–`sb_p4`, and `nl_p0`–`nl_p4`; NLI feature columns are
`nli_f_ent_mean`, `nli_f_ent_min`, `nli_f_con_max`, `nli_f_neu_mean`,
`nli_r_ent`, `nli_r_con`, `nli_r_neu`; pooled three-class columns are
`p_incorrect`, `p_partial`, `p_correct`. It includes all three component
probability arrays and the pooled probabilities, but does not write a separate
confidence column; confidence is derivable as the maximum pooled probability.

**Verified:** The demo's displayed contradiction is `c["feats"][i][2]`
(`A_predict.py:160,170`). That same value is the maximum forward concept
contradiction (`A_predict.py:117-125`) and is saved by v7 as
`nli_f_con_max`. The threshold analysis signal is therefore present. Per-
concept contradiction records in `c["concepts"]` (`A_predict.py:126-129,171`)
are not exported; only their max is. Per-concept review is BLOCKED unless
those records are separately exported under an approved task.

## Static findings

- **Verified:** `A_predict.component_probs(items, dataset="pooled")` returns
  `ft`, `sb`, `nl`, `feats`, and `concepts` (`A_predict.py:110-136`). Its
  NLI-LR consumes the seven aggregate features (`:122-135`), not the raw
  displayed contradiction alone.
- **Unverified:** The source does not establish why Block 61 showed NLI-LR
  values near `0.5070` on its 12 cases. The classifier is fed seven features;
  no constant is assigned to its output in the inspected path. Identical or
  near-identical feature vectors, learned coefficients, or rounded display
  could explain similar values, but the saved case feature vectors and model
  outputs were not analyzed here.
- **Verified:** The v7 assertion expects index 0 `correct`, index 2
  `partially_correct_incomplete`, and indices 1/3/4 `contradictory`,
  `irrelevant`, `non_domain`. `A_predict.py:13` uses exactly that order, so
  the assertion matches the scorer's order.
- **Verified:** `_to3` maps five-way probabilities as incorrect = indices
  1/3/4, partial = index 2, correct = index 0 (`A_predict.py:56-57`).
  The deployed pooled prediction averages components then collapses and may
  temperature-scale (`:152-157`).
- **Verified:** The demo review flag uses confidence below the loaded policy
  threshold, and can also flag a Correct prediction with contradiction above
  the policy threshold (`A_predict.py:160-170`). The requested analysis
  separately reports the fixed 0.64 confidence-only baseline; it does not
  alter either policy or threshold.

## Drafted Colab run sheet

These are Colab command cells for Jigar; no export was run here.

1. **Setup cell:** select T4; mount Drive; place the v7 script and the
   approved dev-text file in `/content/`; create `/content/phase8_tmp/`.
   Confirm `A_predict.py`, its interim artifacts, and the dev-probability
   parquet exist under `/content/drive/MyDrive/project_s_qa/`. The dev
   parquet is currently BLOCKED locally; do not substitute another file.
2. **Smoke cell:** run the first command above with `--limit 16`. It scores
   only 16 aligned dev rows and writes no parquet. Stop on any error or
   assertion. Do not interpret the partial output as a metric.
3. **Full export cell:** only after the smoke run passes and the full dev
   input is confirmed, run the second command with `--limit 0`. Stop on
   parity FAIL or assertion failure. Keep any parity quarantine separate.
4. **Download:** on pass, download
   `/content/phase8_tmp/A_component_probs_v7.parquet` into
   `Project_S_QA_Evidence/Phase_8_Accuracy_Max/`. If parity fails, download
   the `_QUARANTINE_PARITY_FAILED.parquet` only for diagnosis and label it
   invalid. Keep console output with the file. Do not upload outputs to Drive.
5. The analysis script below is drafted only. Running it is outside this
   drafting approval; if later approved, download its CSV and Markdown outputs
   from the Colab temp directory into the same Phase 8 folder.
