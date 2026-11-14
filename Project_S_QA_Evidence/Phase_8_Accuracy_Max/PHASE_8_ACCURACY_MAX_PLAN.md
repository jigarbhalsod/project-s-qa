# Phase 8 — Accuracy Max (Track E, optional)

**Status: Draft only. No model was trained or run.** Track E is time-boxed and
must wait until the Colab demo (Blocks 59–62), parity, freeze, and required
documentation are complete. If the demo is incomplete, defer Track E.

**Scope disclosure:** Test rows were exposed in a prior metadata check. No test
metric was computed or used for selection. Existing test results remain
exploratory; no locked-test result is claimed.

## Read-only evidence from saved rows

- **[Verified] Current component arrays:** no saved current-v2 per-row
  DistilRoBERTa, SBERT-LR, or NLI-LR probabilities were found in the Project 4
  tree, submission package, or inspected ZIP exports. No inference was run.
- **[Verified] Pooled dev array:**
  `project_s_qa/A_submission_v2/reports_v2/A_deployed_dev_probs_v2.parquet`,
  SHA-256 `2e29a708152b288019a9fa50b55b9d823781e4bbe0144cd5ee533fee9ddb5b0e`.
  It has pooled p0-p4, not current per-component rows.
- **[Verified] Legacy components:**
  `archive/project_s_qa_phase1_v1.zip:interim/stack_features_v1.parquet`,
  SHA-256 `c51e1f04ca181a44bf6d952131c6dfb9d73255612253eb1a99f7f67acec0857a`.
  It contains v1 component probabilities aligned to the same 2,049 dev UIDs;
  it is not current-v2 component output.
- **[Verified]** The saved `A_component_check_v2.json` records model-load
  checks, not per-row component probabilities. Hash:
  `0f91c8644349df4e93f10904b3c0c7bc87e25a70f819ee9a09061341a6d5dc51`.

### Aggregation reconciliation (same 2,049 dev rows; dev, optimistic)

| [Tested] Path | Accuracy | Macro-F1 | Partial recall | Predicted Incorrect / Partial / Correct | QWK | Disagree rows vs pooled-collapse |
|---|---:|---:|---:|---:|---:|---:|
| Pooled five-way probabilities collapsed, then argmax | 0.563690 | 0.527046 | 0.263359 | 1,095 / 268 / 686 | 0.401530 | 0 |
| Five-way argmax, then map to three-way | 0.580283 | 0.556598 | 0.385496 | 759 / 436 / 854 | 0.431834 | 336 |

Gold class counts are 659 Incorrect, 524 Partial, and 866 Correct. The second
aggregation is an alternative calculation, not the deployed pooled rule.

### The 110 high-confidence errors

**[Tested, legacy cross-generation only]** Among 156 pooled dev errors with
collapsed pooled confidence >=0.64, the 110 reported consensus rows reproduce
when each legacy component uses five-class argmax then maps to three classes:
DistilRoBERTa, SBERT-LR, NLI-LR, and current pooled all predict the same wrong
three-way label on those 110. On another 21 rows all three legacy components
are wrong but do not share one wrong label. On 25 rows, not all three legacy
components are wrong. These counts do not establish current-v2 component
agreement.

High-confidence pooled errors by gold five-way label: contradictory 2,
correct 68, irrelevant 2, partial 84, non-domain 0 (N=156). By dataset:
Beetle 65; SciEntsBank 91. By split: seen dev_ua 40; unseen dev_uq 116.
Dataset x split: Beetle/dev_ua 15, Beetle/dev_uq 50,
SciEntsBank/dev_ua 25, SciEntsBank/dev_uq 66.

## Draft experiment and gates

`e2_deberta_nli_train.py` is a one-seed, local-only experiment. It fine-tunes
`cross-encoder/nli-deberta-v3-base` on the existing train split. Input pairs
are `[QUESTION] question [REFERENCE] reference` and `student_answer`.
Five labels collapse to 0=Incorrect, 1=Partial, 2=Correct. The question-
disjoint `dev_uq` split selects the checkpoint by evaluation loss; test rows
are never loaded. The script resets the classifier head, uses seed 20261106,
max length 256, fp16 on a Colab GPU, and reports truncation percentage. It
exports UID-keyed dev probabilities and the 12 negation-control probabilities
to this Phase 8 folder. The negation controls are evaluation-only, never train
examples. It statically reads the notebook's FACTS literal as JSON text; it
does not execute the notebook.

`e2_gate_check.py` aligns exactly the same 2,049 dev UIDs with the frozen
pooled probabilities. It computes Macro-F1 gain and a paired 2,000-resample
question-grouped bootstrap CI (seed 20261106), unseen-question QWK, dev
Partial recall, negation exact accuracy, and candidate dev prediction latency.
No test split or test tuning is used. Gates: Macro-F1 gain >=0.01 and CI lower
bound >0; unseen QWK not lower; negation exact >3/12; Partial recall higher.
Latency is reported, with no invented latency pass threshold.

## Checkpoint IDs and L8

| Model | Exact ID/path | L8 status | Availability |
|---|---|---|---|
| Deployed DistilRoBERTa | `project_s_qa/interim/ft_distilroberta_v1` (Hub origin not recorded) | Local model; no hosted LLM/API | Local weights verified by prior package inventory; origin ID Unverified |
| Deployed SBERT encoder | `sentence-transformers/all-MiniLM-L6-v2` | Local open weights; no hosted inference API | Referenced in A_predict.py; runtime cache Unverified |
| Deployed NLI encoder | `cross-encoder/nli-deberta-v3-base` | Local open weights; no hosted inference API | Referenced in A_predict.py; runtime cache Unverified |
| Proposed E2 NLI checkpoint | `cross-encoder/nli-deberta-v3-base` | Compliant by design: local-only loading, no API calls | **Unverified** in Colab cache/Drive |

**[Verified] L8 policy:** all inference in the deployed scorer is local; no
hosted LLM or external inference API is part of the scorer. The proposed E2
script uses `local_files_only=True`; if the checkpoint is absent, stop and
stage it through the approved process rather than downloading during this
task.

## Risks and stop rule

- Current-v2 component probabilities are absent; legacy agreement is only a
  diagnostic and cannot prove complementarity or explain current errors.
- A single seed and dev_uq checkpoint selection leave substantial uncertainty;
  dev metrics remain optimistic. The 85% accuracy at 30% coverage goal is not
  promised and remains unmet.
- Truncation, T4 memory, package/API compatibility, and checkpoint availability
  are Unverified. The local loose source parquet is absent; Colab must have
  `processed/sra_unified_splits_v1.parquet` before starting.
- No threshold change, test access, label edits, training on the 36 controls,
  notebook edits, or frozen-artifact writes are allowed.
- **Stop rule:** if any metric gate fails, or the demo/parity prerequisites
  fail, discard the experiment for submission and use frozen v2. Do not tune
  against test or weaken a gate to obtain a pass.

## Colab checklist (future run; approval required)

1. Confirm Blocks 59–62 and parity are complete before considering Track E.
2. Confirm the source parquet, frozen pooled dev probabilities, notebook FACTS
   cell, and local checkpoint files are present; verify the 2,049 UID set.
3. Confirm a T4 GPU and installed compatible torch/transformers/pandas/numpy/
   scikit-learn versions. Do not install or download during this draft task.
4. Run only `e2_deberta_nli_train.py`; review logs, truncation %, UID count,
   and output hashes. Do not run a notebook cell or use test data.
5. Run only `e2_gate_check.py`; record each gate and latency. Any failed gate
   means fallback to frozen v2. Keep every E2 output inside this folder.

**[Unverified]** No runtime, package-version, checkpoint-cache, or Colab result
has been checked here. No execution is authorized by this draft.
