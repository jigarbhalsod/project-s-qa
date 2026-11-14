# E1b aggregation and risk/coverage (dev only)

## Scope and definitions

- **[Verified]** Input: `project_s_qa/A_submission_v2/reports_v2/A_deployed_dev_probs_v2.parquet`, 2,049 dev rows and 177 unique question IDs. No test rows were used.
- **[Tested]** Gold three-way order is 0=Incorrect, 1=Partial, 2=Correct; counts are 659 / 524 / 866.
- **[Tested]** Path (i): collapse p0-p4 to `[p1+p3+p4, p2, p0]`, then argmax. Confidence is the maximum collapsed score.
- **[Tested]** Path (ii): five-way argmax, then map correct->2, partial->1, all other five-way classes->0. Confidence is the winning five-way probability.
- **[Tested]** Path (iii): multiply the collapsed Partial score by w, renormalize the three scores, then argmax. Confidence is the maximum renormalized score.
- **[Tested]** Fixed-coverage n is `ceil(target * 2,049)`. Rows are ranked by confidence descending, then UID ascending to resolve ties. Group folds use `question_id` (IDs are dataset-prefixed), `StratifiedGroupKFold`, five folds, seed 20261106.
- **[Verified]** Dev results are optimistic; only 27 dev questions are unseen (`dev_uq`). The frozen 0.64 threshold belongs to path (i) and is unchanged. It was not used to select w or applied to paths (ii)/(iii).

## OOF aggregation metrics

**[Tested]** The grid was w=1.0 to 2.0 by 0.1. Selection criterion was the highest five-fold OOF three-way Macro-F1. The selected global w is 1.7. Because the rule is row-wise and has no fitted model, path (i)/(ii) OOF scores equal their observed dev scores. Path (iii) uses the selected w on those same OOF rows; its reported score is selection-optimistic, not an independent estimate.

| Status | Path | w | Accuracy | Macro-F1 | Partial recall | QWK | Predicted I/P/C | Gold I/P/C | N |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Tested | (i) pooled collapse then argmax | — | 0.563690 | 0.527046 | 0.263359 | 0.401530 | 1,095 / 268 / 686 | 659 / 524 / 866 | 2,049 |
| Tested | (ii) five-way argmax then map | — | 0.580283 | 0.556598 | 0.385496 | 0.431834 | 759 / 436 / 854 | 659 / 524 / 866 | 2,049 |
| Tested | (iii) collapsed scores, Partial x w | 1.7 | 0.557833 | 0.552813 | 0.532443 | 0.396714 | 852 / 640 / 557 | 659 / 524 / 866 | 2,049 |

**[Tested]** Paired 95% bootstrap CIs use 2,000 resamples of whole questions (seed 20261106); each row is a difference from path (i). CIs are conditional on the selected w and do not account for grid-selection uncertainty.

| Status | Difference | Accuracy CI | Macro-F1 CI | Partial-recall CI | QWK CI |
|---|---|---:|---:|---:|---:|
| Tested | (ii) minus (i) | [-0.006133, 0.039390] | [0.007665, 0.053721] | [0.084935, 0.169239] | [-0.005292, 0.063255] |
| Tested | (iii), w=1.7, minus (i) | [-0.030266, 0.015589] | [-0.001641, 0.049665] | [0.216008, 0.325116] | [-0.026554, 0.015540] |

## Risk/coverage

**[Tested]** The following are observed dev and five-fold OOF values. For these row-wise rules they are numerically identical; w=1.7 was selected on the same dev OOF folds, so path (iii) is optimistic. Accuracy entries show `accuracy (n accepted)`.

| Status | Coverage target | (i) dev / OOF | (ii) dev / OOF | (iii), w=1.7, dev / OOF |
|---|---:|---:|---:|---:|
| Tested | 10% (n=205) | 0.868293 (205) / 0.868293 (205) | 0.951220 (205) / 0.951220 (205) | 0.882927 (205) / 0.882927 (205) |
| Tested | 15% (n=308) | 0.821429 (308) / 0.821429 (308) | 0.886364 (308) / 0.886364 (308) | 0.834416 (308) / 0.834416 (308) |
| Tested | 20% (n=410) | 0.775610 (410) / 0.775610 (410) | 0.851220 (410) / 0.851220 (410) | 0.790244 (410) / 0.790244 (410) |
| Tested | 25% (n=513) | 0.764133 (513) / 0.764133 (513) | 0.830409 (513) / 0.830409 (513) | 0.775828 (513) / 0.775828 (513) |
| Tested | 30% (n=615) | 0.754472 (615) / 0.754472 (615) | 0.806504 (615) / 0.806504 (615) | 0.744715 (615) / 0.744715 (615) |
| Tested | 40% (n=820) | 0.693902 (820) / 0.693902 (820) | 0.763415 (820) / 0.763415 (820) | 0.712195 (820) / 0.712195 (820) |
| Tested | 50% (n=1,025) | 0.668293 (1,025) / 0.668293 (1,025) | 0.738537 (1,025) / 0.738537 (1,025) | 0.658537 (1,025) / 0.658537 (1,025) |

**[Tested]** Maximum confidence-ranked prefix meeting each accuracy floor; n and coverage are shown. OOF equals observed for these deterministic rules, with the path (iii) selection caveat above.

| Status | Path | >=85% accuracy: n / coverage / accuracy | >=90% accuracy: n / coverage / accuracy |
|---|---|---:|---:|
| Tested | (i) pooled collapse | 254 / 12.396% / 0.850394 | 165 / 8.053% / 0.903030 |
| Tested | (ii) five-way argmax then map | 427 / 20.839% / 0.850117 | 274 / 13.372% / 0.901460 |
| Tested | (iii) Partial x 1.7 | 242 / 11.811% / 0.851240 | 184 / 8.980% / 0.902174 |

## High-confidence consensus review pool

- **[Tested]** The legacy cross-generation rule (all three legacy five-way argmax-then-map component predictions and current pooled path (i) choose the same wrong label, with pooled confidence >=0.64) yields 110 rows. Their gold counts are Partial 64, Correct 43, Irrelevant 2, Contradictory 1.
- **[Tested]** The requested sample uses the 107 Partial/Correct rows: 5 per each of the 2 gold labels x 2 datasets x 2 seen/unseen splits. The other 3 consensus rows are not in those requested gold strata and are excluded from the sample.
- **[Verified]** `E1_review_sample.csv` retains original gold, includes 40 unique UIDs, leaves all reviewer fields blank, and puts any suggested correction in a separate blank column. No gold label was changed.

## 0.588 and 0.579 dev figures

- **[Verified]** Working COPY cell 97 (Block 37) filters `stack_features_v1.parquet` to dev_ua/dev_uq, averages the five-way `ft_p`, `sb_p`, and `nl_p` probabilities per row, collapses to three classes, then computes accuracy. Its saved output is 0.588 for 2,049 rows. This is a mean across three legacy components per row, not a mean across seen/unseen cohorts. It is not current pooled p0-p4.
- **[Tested]** Applying current pooled path (i) gives three-way accuracy 0.563690; path (ii) gives 0.580283. Neither gives 0.588 because cell 97 uses legacy v1 component probabilities.
- **[Verified]** Working COPY cell 108 (Block 41) reports five-way Macro-F1 0.579 [0.523, 0.629] for the deployed v2 pooled probabilities. Recalculation from saved p0-p4 gives 0.578892. The requested three-way Macro-F1s are 0.527046 and 0.556598; they cannot reproduce a five-class Macro-F1. Five-way argmax before path (ii)'s mapping is the prediction basis for 0.579, but after mapping the requested three-way metric changes.

