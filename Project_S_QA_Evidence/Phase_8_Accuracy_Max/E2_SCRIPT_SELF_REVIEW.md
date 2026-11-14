# E2 script static self-review

**[Verified] Scope:** Reviewed the text of `e2_deberta_nli_train.py` and
`e2_gate_check.py`, the working notebook as JSON, A_predict.py as text, and
non-test rows from the archived source split. Neither script was run; no model
was loaded or trained. Line numbers below refer to the current draft files.

**[Verified] Scope note:** A preliminary read-only source metadata check loaded
the complete archived split, including test rows, while checking label mapping
and reference uniqueness. Those full-split counts were discarded; all reported
metrics and mapping/reference checks were recomputed on dev or train+dev only.
No test metric was calculated or used for selection.

| Status | Check | Finding | Draft reference |
|---|---|---|---|
| Verified | Test splits | Training read uses a split filter containing only train, dev_ua, dev_uq; gate asserts all rows are dev_ua/dev_uq. No test metric or test tuning is present. | train:6; gate:6 |
| Drafted | UID alignment | Gate merges by uid, dataset, split, question_id with one-to-one validation and asserts 2,049 rows and equality to baseline UID set. Candidate output does not exist yet, so actual future alignment is Unverified. | gate:6-7 |
| Tested | 5-to-3 label mapping | Script maps correct->2, partial->1, other labels->0. Against `label3_ours`, this had 0 mismatches on 8,910 train/dev rows; no test rows were used in this check. | train:6; gate:7 |
| Tested | Train/dev question separation | Train overlaps 150 question IDs with dev_ua and 0 with dev_uq. The script selects only dev_uq for checkpoint selection; dev_ua is not question-disjoint. | train:6 |
| Drafted | Fixed seeds | `set_seed(20261106)` plus Trainer seed/data_seed; gate bootstrap seed is 20261106. Bitwise reproducibility across devices/libraries is Unverified. | train:5,16; gate:8 |
| Drafted | Input format | Tokenizer receives `[QUESTION] question [REFERENCE] reference` as the first sequence and student answer as the second sequence. | train:15 |
| Drafted | Max length/truncation | MAXLEN=256; code counts examples exceeding that length over train, dev, and the 12 controls. The measured truncation percentage is Unverified because the script was not run. | train:5,10 |
| Tested | Beetle references | In the archived train/dev rows, no `(dataset, question_id)` group has multiple distinct reference answers (maximum one). Code handles each row's reference directly; it has no multi-reference aggregation if future data differs. | train:6,15 |
| Drafted | Negation controls | Code statically reads the notebook FACTS literal, creates 12 negation-only examples with expected class 0, and writes their probabilities; gate requires 12 rows and computes exact accuracy. The controls are not in the training dataset. | train:7-9,19; gate:10 |
| Verified / BLOCKED | Latency | A timer and reported ms/row exist. The timer currently includes DataFrame creation and CSV writing, and no warm-up or same-runtime pooled baseline is measured; this is not a clean model-latency comparison. | train:18,20; gate:10-11 |
| Drafted | Group bootstrap | Gate samples combined `dataset|question_id` groups with replacement for 2,000 paired Macro-F1 differences. There are 177 dev groups. | gate:8 |
| Unverified / BLOCKED | T4 batch safety | fp16 is enabled. Train/eval batch sizes are not specified, so library defaults apply; T4 memory safety has not been established. | train:16 |
| Verified / Unverified | Colab paths | Scripts point to `/content/drive/MyDrive/project_s_qa` and the Phase 8 output folder. They do not mount Drive; a prior mount is required. Remote path availability is Unverified. | train:4,6; gate:5-6 |
| Unverified / BLOCKED | Inputs/checkpoint | The loose source parquet is absent locally (it is in the archive); Colab availability is Unverified. Checkpoint ID is `cross-encoder/nli-deberta-v3-base`, loaded with `local_files_only=True`; cache/Drive availability is Unverified. | train:4,6,9 |
| Unverified | Runtime compatibility | Package versions are not pinned. `TrainingArguments` API compatibility, checkpoint loading, and actual GPU memory use were not tested. | train:2-3,9,16 |

## Defects and blockers

- **[BLOCKED]** Before execution, mount Drive and verify the source parquet,
  baseline pooled parquet, notebook JSON, and local checkpoint are at the
  referenced paths. Current local source parquet is only in the ZIP archive.
- **[BLOCKED]** Set explicit per-device train/eval batch sizes appropriate for
  the T4 and pin/confirm compatible package versions before approval. This
  review does not change the scripts.
- **[Verified / BLOCKED]** Move the timer stop to immediately after prediction
  and measure pooled baseline under the same device, warm-up, and batch
  protocol before comparing latency. Current timing includes CSV output.
- **[Unverified]** The training script reads Block 51 FACTS as a Python literal
  from the notebook JSON (without executing it). Its expected source marker
  and 12-row construction have not been exercised.

**[Verified] L8:** A_predict.py names the local NLI and SBERT encoders; the
deployed scorer uses local components and no hosted LLM/external inference
API. The proposed E2 checkpoint is local-only by design. Its availability is
Unverified; no network access or download was attempted.

