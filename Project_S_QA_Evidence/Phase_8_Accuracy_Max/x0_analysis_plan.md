# X0 dev-only diagnostic plan

**Drafted.** No analysis below has been run. Dev results are optimistic; the
script is intended to select only `dev_ua` and `dev_uq` rows, never test rows.

## Source inventory

**Verified from notebook source:** `drive_backup_20261107/processed/sra_unified_splits_v1.parquet`
is the source table referenced by the notebook. Its source-used columns are
`uid, dataset, split, question_id, label5, score_ours, question,
reference_answer, student_answer`. It is a split-bearing file, was not opened,
and is not a verified dev-only artifact. The script uses Parquet split filters
and checks that the returned rows are exactly the 2,049 dev rows.

**Verified from notebook source:** the dev-only probability file is
`project_s_qa/reports_v2/A_deployed_dev_probs_v2.parquet`, with columns
`uid, dataset, split, question_id, label5, score_ours, f_con_max, d_p0-d_p4`.
It does not contain the three answer texts or component probabilities, so it
cannot serve alone as `component_probs()` input. Live Drive availability is
**Unverified**.

## Analyses unlocked (dev only)

1. For DistilRoBERTa, SBERT-LR, NLI-LR and pooled: report five-class accuracy
   and Macro-F1 against `label5`; report three-class Partial recall and QWK
   against `score_ours`, using the deployed five-to-three mapping. Give N for
   every metric and keep `dev_ua`/`dev_uq` as descriptive strata.
2. Count per component the rows where that component is correct and pooled is
   wrong, and the reverse. Join strictly by UID; do not retune on dev.
3. Count rows where pooled predicts Correct and maximum concept contradiction
   is at least 0.9; report the count and share whose gold is not Correct. This
   describes the disabled contradiction-review rule; it does not change it.
4. For the 12 `kind=negation` controls in
   `reports_v2/A_negation_paraphrase_v2.csv`, inspect variance of all seven NLI
   features across cases. This is diagnostic only; do not train on controls.
5. Count errors where all three component argmax labels agree with one
   another and disagree with gold. Report count and denominator explicitly.

## Draft only: Block 60 question/reference safety diff

The executed notebook is `Project_S_QA_Evidence/Phase_2/Jigar_QA_PHASE2_RUN_COPY_EXECUTED.ipynb`,
Block 60 code cell 159. Proposed UI/data-flow change only; not applied:

```diff
-LOOKUP = {f"{r['question_id']}: {r['question_text']}": (r['question_text'], r['reference_answer']) for _, r in qb.iterrows()}
+LOOKUP = {str(r['question_id']): (r['question_text'], r['reference_answer']) for _, r in qb.iterrows()}
+mode = gr.Radio(["Question bank", "Custom question"], value="Question bank")
+dd = gr.Dropdown(choices=[(f"{qid}: {v[0]}", qid) for qid, v in LOOKUP.items()])
+q = gr.Textbox(label="Question", interactive=False)
+ref = gr.Textbox(label="Reference answer", interactive=False)
+warning = gr.Markdown("Custom question/reference: not verified against the bank.", visible=False)
+def pick(qid): return LOOKUP.get(qid, ("", ""))
+def set_mode(value): return gr.update(interactive=value == "Custom question"), gr.update(interactive=value == "Custom question"), gr.update(visible=value == "Custom question")
+mode.change(set_mode, mode, [q, ref, warning])
+ref.change(lambda value, m: gr.update(visible=(m == "Custom question")), [ref, mode], warning)
+dd.change(pick, dd, [q, ref])
```

In bank mode, the selected question ID retrieves its paired reference and the
reference is read-only. Custom mode explicitly unlocks the reference and shows
a warning. The scorer itself remains unchanged.

## Blockers and limits

- **BLOCKED pending source availability:** no verified dev-only raw-answer
  table was found in the working `project_s_qa/` folder. The available
  `sra_unified_splits_v1.parquet` is split-bearing; the draft filters to dev,
  but must not be run unless Jigar confirms the filtered read is acceptable.
- **Unverified:** live Drive paths, Colab T4 memory/runtime, and whether the
  strict `1e-6` pooled parity assertion passes on that runtime.
- Exporting probabilities yields no accuracy gain by itself. Any gain from a
  later change is unknown until measured on an approved evaluation protocol.
