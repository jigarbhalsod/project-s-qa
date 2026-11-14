# E4 — DeBERTa experiment specification (v2)

**Drafted.** Single source for the proposed Stage 1 settings. Nothing was
trained or loaded. Any dev-based result remains **dev-only, optimistic** and
is not independent confirmation.

## Hyperparameters

| Setting | Value | Source / status |
|---|---|---|
| Seed | 20261106 | `x1_deberta_train.py:3`, gate `:3`; Notion 8.4 says 42 (Reported). Flag discrepancy; Jigar to align Notion. |
| Learning rate | 2e-5 | Notion 8.4 (Reported/Proposed); script `:19` matches. |
| Epochs | 3 | Notion 8.4 proposes 3–4 (Reported); 3 is the script value and the selected proposal. |
| Warmup ratio | 0.10 | Notion 8.4 (Reported/Proposed); script `:19` matches. |
| Weight decay | Not explicitly set | Script `:19`; library default would apply; value Unverified. |
| Maximum sequence length | 256 | Script `:3`; code counts truncation but the rate is Unverified until run. |
| Train batch | Per-device 4 × gradient accumulation 4 = effective 16 | Script `:19`. |
| Evaluation batch | 8 per device | Script `:19`. |
| Precision | fp16 enabled; bf16 not selected | Script `:19`; T4 memory safety Unverified. |
| Loss | Three-class sequence-classification loss (cross-entropy expected) | Labels are integer class IDs in script `:7, :22`; no explicit loss setting. Treat cross-entropy as the model default, not a separately configured option. |
| Checkpoint selection | Validation Macro-F1, higher is better; load best at end | Script `:19`; compute metric at `:19`. |
| Checkpoint order | `MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli`, then `cross-encoder/nli-deberta-v3-base` | Script `:3`; availability of both Unverified. |
| Input | `[QUESTION] question [REFERENCE] reference` as first sequence; student answer as second | Script `:18`. |
| Selection split | `dev_uq` | Script `:7`; same split is later used by the gate, so not independent confirmation. |

**Verified source comparison:** The script matches seed, LR, epochs, warmup,
max length, train/eval batches, accumulation, fp16, selection metric, and
checkpoint order shown above. Proposed adjustments: explicitly set and record
weight decay; make loss choice explicit if library-default ambiguity is not
acceptable. No script was edited.

## Preregistered gates — proposed

| Gate | Proposed decision rule | Existing `x1_gate_check.py` comparison |
|---|---|---|
| Three-seed Macro-F1 | Mean gain ≥0.01 and paired question-group bootstrap 95% CI lower bound >0 | **Mismatch:** script evaluates one candidate seed and bootstraps that one comparison (`:8, :11`); it does not aggregate three seeds. |
| Accuracy | Candidate accuracy > 56.37% (Reported baseline in E1) | **Mismatch:** not computed by the gate; no test result is used here. |
| Overall QWK | Candidate QWK > 0.4015 (Reported baseline in E1) | **Mismatch:** gate computes unseen-split QWK only (`:9`). |
| Unseen QWK non-inferiority | **Proposed:** candidate QWK may be at most 0.01 below frozen QWK. A 0.01 absolute QWK margin caps tolerated degradation tightly while allowing a small sampling fluctuation; confirm before use. | Script requires candidate ≥ baseline (zero margin), which is stricter (`:9, :11`). |
| Partial metrics | Partial recall and Partial F1 both higher | **Mismatch:** gate checks recall only (`:9, :11`); it does not check Partial F1. |
| Negation controls | Diagnostic only; no pass gate | Script computes exact score for 12 cases and labels it diagnostic (`:10-11`); retain that interpretation. |
| Latency | Report batch-1 and batch-32 median and p95 | **Mismatch:** script reports one full-dev prediction elapsed time and ms/row (`x1_deberta_train.py:20`; gate `:11`); it has no batch-1/32 median or p95. Timer stops after `trainer.predict`, before output writes. |

The gate script also uses only one seed and one 2,000-resample paired
question-group bootstrap (`x1_gate_check.py:8`). The train script sets seed
20261106. A one-seed pilot cannot pass the three-seed gate. No target is
promised; no threshold changes.

## Protocol decision

**Verified:** Existing dev splits are `dev_ua` (753 rows) and `dev_uq`
(1,296 rows across 27 questions). The script uses `dev_uq` for checkpoint
selection (`x1_deberta_train.py:7`) and the gate evaluates on that same split
(`x1_gate_check.py:9`). That route needs fewer new fold artifacts but cannot
serve as independent confirmation after selection.

**Proposed recommendation:** use nested question-grouped cross-validation on
dev if Stage 1 proceeds and the goal is a less selection-biased gate estimate.
It requires fold assignments, per-fold/per-seed checkpoints and predictions,
more compute, and revised evaluation code. Dev remains optimistic even then;
a separate clean confirmation set is still needed. Use existing `dev_uq` only
for an exploratory single-seed pilot, not as an independent gate.
