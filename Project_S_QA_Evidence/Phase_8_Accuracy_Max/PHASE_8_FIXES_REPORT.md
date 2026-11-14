# Phase 8 fixes report

All measured results are **dev-only, optimistic**. This work was static
preparation; Stage 1 remains unapproved.

## Part 1 — Training pool

| Candidate | Metadata / schema | Result |
|---|---|---|
| `project_s_qa/processed/cbse_demo_questions_v1.csv` | 2,888 bytes; mtime 2026-11-06 01:08:29; header: `question_id,dataset,topic_id,subject,class,question_text,reference_answer,question_type,difficulty,language,source_page,drafted_by,reviewer,status,version`; no split column. | Not a training text file; no student responses or labels in the header. |
| `Project_S_QA_Evidence/Phase_3/dev_text_2049.parquet` | 107,715 bytes; mtime 2026-11-08 01:09:46; columns: `uid,dataset,split,question_id,label5,question,reference_answer,student_answer`; splits `dev_ua`, `dev_uq`; 2,049 rows. | Available, but dev-only. SHA-256 `21e7305557825b392a297fc4558b73e1161fcefb07d82c9f802e33c877836ea2`. |
| `Project_S_QA_Evidence/Phase_8_Accuracy_Max/A_component_probs_v7.parquet` | 444,822 bytes; mtime 2026-11-09 16:23:12; 30 columns including UID, dev split/labels and component probabilities; splits `dev_ua`, `dev_uq`. | Dev probabilities, no question/reference/student text training pool. SHA-256 `71dd07621bb838b38af1932f43d985059a6a69e61d39361e6a5063eb5bdc5f88`. |
| `project_s_qa/processed/sra_unified_splits_v1.parquet` | Not present in the scoped directories. | No content opened. A mixed split file, if found elsewhere, remains protected. |
| `raw/`, notebook standalone CSV/Parquet exports, Phase 1 | No train-named text data candidate found in the searched locations. | No file contents opened for this conclusion. |

**Verified outcome (b):** no train-only text file was found in the scoped
working-tree search. The available model-development pool is the 2,049 dev
rows, about 1,640 rows in each outer training fold. Any resulting DeBERTa
score must be labelled **“exploratory, smaller training pool, not comparable
with v2.”** The comparison point that v2 used the full training pool is
**Reported** from Jigar's task context. Archives, backups, cloud locations,
and excluded test-named files were not searched or opened. No candidate
train-named data contents were opened. `nested_cv_folds_v1.csv` was not
modified; no v2 fold file was warranted.

## Part 2 — Unseen-QWK margin

**Tested, dev-only:** deployed Path A QWK on `dev_uq` is 0.294900 (1,296
rows, 27 question groups). The 10,000-resample seed-42 question-group
bootstrap 95% interval is 0.206416-0.377733; standard error is 0.043863.
The input hashes matched the supplied expected hashes.

**Proposed approximate MDD:** 0.122816 QWK, calculated as 2.80 x baseline
SE for a two-sided 5% test at 80% power. This substitutes baseline SE for
the unavailable paired-difference SE. It is approximate and not an observed
power result; candidate predictions and paired covariance are unavailable.
Three seeds do not increase the 27 question groups.

**Proposed:** use 0.0219 (half baseline SE) as a descriptive margin: it means
allowing at most a 0.0219 absolute QWK decrease. Keep unseen QWK as a reported
secondary result, not a hard gate, because the sample is too small for a
strong non-inferiority decision. The 0.01, 0.0439, and 0.1228 alternatives
and their meanings are recorded in `E4_DEBERTA_EXPERIMENT_SPECIFICATION_v3.md`.
All other E4 gates remain unchanged.

## Part 3 — Script diff and checks

`x1_gate_check_v3.py` is a new copy of v2. Functional diff:

```diff
+ --unseen-qwk-margin (default 0.021931457953841245)
+ EXPLORATORY banner: outcome (b), smaller training pool; not comparable with v2
- unseen QWK margin derived as min(0.01, half bootstrap interval width)
+ unseen QWK margin comes from the CLI argument
- unseen-QWK pass/fail gate
+ unseen-QWK difference and within-margin comparison, labelled secondary only
  all other metric gates and bootstrap logic remain unchanged
```

**Tested:** static AST parsing passed for `x1_gate_check_v3.py`. The script was
not run. No candidate result, margin pass, or model comparison is claimed.

## Remaining blockers and approvals

- **Reported:** the Phase 2 final status marks Phase 3 evidence partial;
  complete that evidence before Stage 1.
- **BLOCKED:** no train-only text file was found. Any future result from the
  current dev-only folds is not comparable with v2.
- **Unverified:** checkpoint availability and T4 runtime/memory behavior.
- **Unapproved:** Stage 1 requires Jigar's explicit `approved Stage 1` after
  Phase 3; Stages 2 and 3 each require separate approval.
- No clean locked test is available; no test split was opened.

No model, notebook, or Project S script was executed. No download, install,
move, overwrite, or deletion occurred. Only the three new files listed in
this report were created.
