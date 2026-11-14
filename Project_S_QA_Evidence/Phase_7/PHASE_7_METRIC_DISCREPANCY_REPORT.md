# Phase 7 metric discrepancy report

Audit date: 6 Nov 2026. Evidence tags distinguish the deployed pooled policy,
an alternate five-way argmax rule, and blocked reported comparisons. Dev
numbers are dev, optimistic; test numbers are exploratory (test seen in v1).

## QWK reconciliation (exactly three requested rows)

| QWK value | What produces it | Population / N | Matches deployed policy? |
|---:|---|---|---|
| 0.4015 | [Tested] Collapse pooled five-way probabilities to three-way probabilities, then argmax | Dev, 2,049 | Yes |
| 0.4318 | [Tested] Five-class argmax, then map the predicted class to three-way | Dev, 2,049 | No |
| 0.4479 | [BLOCKED] Reported matched comparison; required V prediction/comparison files absent | N=2,049 is Reported, not verified | Unverified |

## Accuracy reconciliation (exactly three requested rows)

| Accuracy | What produces it | Population / N | Matches deployed policy? |
|---:|---|---|---|
| 56.37% | [Tested] Pooled five-way probability collapse, then three-way argmax | Dev, 2,049 | Yes |
| 58.03% | [Tested] Five-way argmax, then map to three-way on the same 2,049 rows | Dev, 2,049 | No |
| 57.83% | [BLOCKED] Reported matched comparison; comparison files absent | N=2,049 is Reported, not verified | Unverified |

[Tested] The two evaluated paths on the same 2,049 dev UIDs predict different
classes on 336 rows. Pooled collapse accuracy is 0.563690 and QWK 0.401530;
five-way argmax then mapping accuracy is 0.580283 and QWK 0.431834. The saved
bootstrap file's QWK 0.431834 is therefore not the deployed policy's QWK.

## Why both outputs say about 0.588

[Verified] The 0.588 dev output is saved in the working COPY notebook at the
Block 37 error-analysis code/output cell. Its source reads stack_features_v1,
averages the v1 ft_p, sb_p and nl_p probabilities, then collapses to three
classes. [Tested] Replaying that saved-probability calculation from the
archive gives 0.588092 on 2,049 dev rows. This is a legacy v1 component-average
path, not the current pooled A_predict policy.

[Verified] The 0.588 test output is in the Block 43 exploratory-test
code/output cell. It reports ALL test, N=7,093, with acc3 rounded to 0.588.
The exact saved A_test_results_v2.csv value is 0.5879036 and recalculation
from A_test_scored_v2.parquet gives 0.587904. Block 43 uses the pooled v2
inference path. This is exploratory (test seen in v1).

[Verified] These are different split populations and different evaluation
paths, not a duplicated value copied between dev and test. The saved outputs
have null execution counts in the current COPY; their original runtime
provenance is Unverified.

## Mapping, row alignment and source

[Verified] A_predict.py LABEL5_ORDER is correct, contradictory,
partially_correct_incomplete, irrelevant, non_domain. Truth mapping is
correct -> 2, partial -> 1, and contradictory/irrelevant/non_domain -> 0.
A_predict.py applies _to3 to the mean of the ft, sb and nl five-way component
probabilities. Its pooled mode loads pooled_lr_v2.joblib for SBERT-LR and
NLI-LR.

[Tested] The packaged dev probability file aligns one-to-one with the archived
source split on all 2,049 UIDs. There are zero duplicate/missing prediction
UIDs and zero label-map mismatches. The source split entry in the phase1 and
final-v1 ZIPs is byte-identical (SHA-256
bdb67bf80f1cfa2a58a8193f3ca503bb1e462b393bb72c0635e1cc684b22676a6).

## Vishwajeet comparison: BLOCKED

[BLOCKED] No local file was found for any of these requested items:
V_roberta_seed_42_dev_predictions.csv;
V_roberta_seed_123_dev_predictions.csv;
V_roberta_seed_2026_dev_predictions.csv;
V_roberta_all_seeds_dev_predictions.csv;
V_ensemble_vs_roberta_uid_comparison.parquet;
V_ensemble_vs_roberta_metrics.csv;
V_ensemble_vs_roberta_split_metrics.csv;
V_ensemble_vs_roberta_error_overlap.csv;
V_roberta_evaluation_config.json;
V_both_wrong_sample20_audit_v3.csv;
V_ensemble_only_correct_sample20_audit.csv;
V_roberta_30_manual_error_review_COMPLETED_v2.csv.

[BLOCKED] The reported overlap counts 933/557/307/252 and the reported
Vishwajeet/Jigar metrics 60.52%/0.4997 and 57.83%/0.4479 remain Reported,
not verified. The counts are not used to create predictions or QWK/F1.
A_seed_summary_v2.json records status missing.

[Verified] A_model_comparison_dev_v2.csv contains older per-dataset
stack_features_v1 summaries, including avg3_FINAL. Those are not the current
pooled A_predict output and do not resolve the matched-comparison discrepancy.
The roberta_base summary is Jigar's Block 26 row; the weights are absent.