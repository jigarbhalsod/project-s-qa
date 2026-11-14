# NLI contradiction and pooled prediction

**Drafted.** No scorer, notebook, model, or analysis script was run. Any
analysis described here is **dev-only, optimistic; the rule was chosen on
these rows**. It cannot establish generalization or validate a new review rule.

## Decision memo

The proposed analysis compares the deployed pooled prediction with the
exported maximum forward concept-contradiction feature and measures what a
review rule at 0.90, 0.95, or 0.99 would have changed on the same dev rows.
The 0.64 confidence threshold remains fixed and is used only for the baseline
review flag. An added contradiction rule changes review coverage, not the
model's underlying predictions; overall accuracy is therefore reported as
unchanged by definition.

No contradiction rule may enter `A_predict.py` in this task. Before a scorer
change, preserve the current frozen scorer and artifacts with a verified
backup, obtain Jigar's explicit approval for a separately reviewed patch, and
evaluate the rule on a clean independent confirmation set not used to select
the threshold. This task makes no change to `A_predict.py` or the 0.64
threshold.

**Proposed only:** compare the rule with a meta-model trained on out-of-fold
component probabilities. **Proposed only:** evaluate an NLI-initialized
DeBERTa model as a separate experiment. Neither option is approved or tested.

## Readiness

**BLOCKED:** `project_s_qa/reports_v2/A_deployed_dev_probs_v2.parquet` was not
present locally during static inspection. Its columns and row count could not
be verified. Drive availability is Unverified. The export must first pass its
UID, dev-split, label, scorer-hash, and parity assertions. The drafted analysis
then requires a full 2,049-row export and matching dev gold file; it asserts
unique aligned UIDs and dev-only split values before producing results.

The report will include question-grouped bootstrap intervals with 2,000
resamples and a fixed seed. Results remain dev-only and optimistic; choosing
among thresholds using these same dev rows is not independent confirmation.
