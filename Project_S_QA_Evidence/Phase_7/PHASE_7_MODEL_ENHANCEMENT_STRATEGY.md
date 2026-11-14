# Phase 7 model enhancement strategy

Audit date: 6 Nov 2026. [Verified] This is a strategy, not implementation.
Recommendations use only audited local evidence; no literature comparison was
checked offline. All proposed validation uses question-grouped folds and
keeps test data out of tuning.

## Ranked next work

| Rank | Experiment | Evidence and status | Expected benefit | Risks | Effort / compute | Validation |
|---:|---|---|---|---|---|---|
| 1 | Reproduce the Jigar/Vishwajeet comparison on matched UIDs | [BLOCKED-DEPENDENT] All requested V row-level predictions and comparison exports are absent; Jigar pooled baseline is locally reproduced | Resolve the metric disagreement and establish a valid comparator | UID/label mismatch, different mappings or splits | Medium; low if exports are supplied, no retraining | Exact UID intersection, one mapping, paired question bootstrap; do not tune on test |
| 2 | Grouped out-of-fold risk/coverage | [Tested] Dev threshold 0.64 gives 75.12% at 30.60%; saved grouped-CV summary gives 74.77% at 31.33%; no row-level OOF curve | Estimate review-policy performance without same-dev optimism | Threshold selection and question leakage | Medium; low to medium compute | Generate grouped OOF predictions, fixed policy, question bootstrap intervals |
| 3 | Component agreement as review signal | [Verified] Legacy-only: v1 components plus current pooled output agree wrong on 197/894 pooled errors; exact current v2 component rows are [BLOCKED] | Identify cases for teacher review without changing the deployed score | Cross-generation proxy may not transfer; agreement can be wrong | Medium; existing model components, future controlled inference | On the same question-grouped OOF rows compare disagreement with confidence at equal coverage; no Vish files required |
| 4 | Human review, then label cleaning | [Tested] Partial recall is 26.34%; 57.72% of current errors involve Partial; [Verified] exact normalized conflicts are absent in dev, and completed review count is zero | Separate model failures from rubric/reference/gold ambiguity | Reviewer disagreement; unsupported label edits | Medium human effort; no model compute | Blind dual review, adjudication and agreement; preserve original labels and store suggestions separately |
| 5 | Partial-targeted loss or ordinal objective | [Tested] Partial recall is 26.34%, with 255 partial-to-incorrect and 131 partial-to-correct errors | Improve partial recall or reduce distant ordinal errors | Precision/calibration tradeoff; label ambiguity; dev overfit | Medium; GPU training | Only after label review; grouped CV, classwise P/R/F1, QWK and risk/coverage |
| 6 | RoBERTa confidence ranking | [BLOCKED-DEPENDENT] Seed prediction/probability files and matched UID exports are absent | Determine whether its confidence ranks errors better | User-reported results are unverified; cannot compare without rows | Medium; low with exports, GPU if fresh inference is required | Equal coverage on grouped OOF rows, paired question bootstrap; no test tuning |

## Evidence boundaries

[Verified] A_predict.py uses three components in its pooled score, but saved v2
dev probabilities do not contain per-component rows. The archive contains
legacy v1 component probabilities; they are not a substitute for current v2
OOF component scores.

[Pending] The agreement experiment is not dependent on Vishwajeet's files, but
current component probabilities must be produced from existing local
components in a separately approved analysis. No inference was run here.

[Pending] Label cleaning is not justified by exact duplicate conflicts alone:
the normalized dev duplicate check found none. Human review is needed before
changing labels or creating corrected training data.

[Unverified] Cross-encoder, DeBERTa, contrastive learning, synthetic
augmentation and more architecture changes are not ranked: the current audit
does not isolate a failure that requires those additions, and label/reference
quality is unresolved. Do not add model complexity before baseline and review
gates pass.

## Freeze and validation gates

[Pending] Keep the deployed threshold and test protocol frozen. Use fixed
seeds, question-grouped splits, and the same label mapping and row population
for every comparison. Report overall accuracy separately from accepted-answer
accuracy and coverage. Keep 36 negation controls out of training. Retain
test values only as exploratory (test seen in v1).