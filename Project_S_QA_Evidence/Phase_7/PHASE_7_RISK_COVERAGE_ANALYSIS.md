# Phase 7 risk-coverage analysis

Audit date: 6 Nov 2026. Evidence tags distinguish saved file values from
calculations. Dev values are dev, optimistic, because the threshold/ranking is
evaluated on the development population. Test values are exploratory (test
seen in v1).

## Saved file and frozen threshold

[Verified] A_risk_coverage_v2.csv is in the packaged snapshot. Its schema is
threshold, coverage, acc_auto; it has 12 rows for dev. It is a threshold grid,
not a test or CV file.

[Verified] The saved temperature is 1.0000000000000004; applying it changes no dev predictions, confidence rankings, or 0.64 accepted count. A_abstain_policy_v2.json says threshold 0.64 was calibrated on dev
only, and that the dev estimate was computed on all dev rows. Therefore the
0.64 result is reported on the same development data used to choose/calibrate
the threshold; it has an in-sample advantage.

[Tested] At threshold 0.64: 627 of 2,049 dev answers are auto-scored,
coverage 0.306003, accuracy 0.751196. A 2,000-replicate question-group
bootstrap with seed 20261106 gives accuracy CI 0.678317-0.821831 and
coverage CI 0.267766-0.349425. These intervals condition on the fixed
threshold and do not remove development selection bias.

## Fixed top-k coverage points

[Tested] For each requested coverage, answers were ranked by deployed
confidence from saved pooled probabilities. k is round(target*N); ties at the
cutoff are resolved by UID ascending for a deterministic exact k. The 25% and
50% cutoffs each split a two-answer confidence tie, selecting one; other
requested cutoffs had one answer at the boundary. These are dev, optimistic.

[Tested] CIs are percentile 95% intervals from 2,000 question-group bootstrap
resamples with fixed seed 20261106. A group is dataset plus question_id; 177
groups are sampled with replacement. Within each resample, confidence ranking
and target-k selection are repeated. These intervals do not account for model
or threshold selection.

| Target | Accepted N | Actual coverage | Accuracy | Question-bootstrap 95% CI |
|---:|---:|---:|---:|---:|
| 10% | 205 | 0.100049 | 0.868293 | 0.763871-0.945459 |
| 15% | 307 | 0.149829 | 0.824104 | 0.744728-0.892606 |
| 20% | 410 | 0.200098 | 0.775610 | 0.709181-0.847651 |
| 25% | 512 | 0.249878 | 0.763672 | 0.696181-0.829155 |
| 30% | 615 | 0.300146 | 0.754472 | 0.684742-0.818339 |
| 40% | 820 | 0.400195 | 0.693902 | 0.638096-0.766581 |
| 50% | 1,024 | 0.499756 | 0.668945 | 0.606419-0.731742 |

## Maximum observed confidence-threshold coverage

[Tested] This scan uses every distinct deployed confidence cutoff and includes
all answers tied at a cutoff. The threshold is selected on dev; these are
dev, optimistic. CIs use 2,000 question-group resamples at the selected fixed
threshold and seed 20261106. They are conditional, not post-selection
independent intervals.

| Accuracy floor | Selected threshold | N accepted / questions | Coverage | Accuracy | 95% bootstrap CI |
|---:|---:|---:|---:|---:|---:|
| 85% | 0.776020 | 253 / 89 | 0.123475 | 0.853755 | 0.765619-0.930131 |
| 90% | 0.824067 | 165 / 63 | 0.080527 | 0.903030 | 0.800000-0.979299 |
| 95% | 0.851329 | 128 / 52 | 0.062469 | 0.953125 | 0.887493-1.000000 |

[Tested] The highest accuracy in the full raw threshold scan is 1.000000 at
threshold 0.95, N=3, two questions, coverage 0.001464. The fixed-threshold
bootstrap interval is 1.000000-1.000000, but N=3 is too small for a useful
performance claim; the degenerate interval does not establish reliability.

[Verified] On the coarser 12-row A_risk_coverage_v2.csv grid, the maximum
observed coverage is 0.103465 (N=212) at >=85%, 0.063446 (N=130) at >=90%,
and 0.014153 (N=29) at >=95%. The difference from the full raw scan reflects
the coarse threshold grid.

[Tested] Linear interpolation between adjacent rows of the coarse saved grid
estimates coverage 0.114771 (about 235 answers) at 85%, 0.084515 (about 173)
at 90%, and 0.053655 (about 110) at 95%. These are interpolated estimates,
not observed operating points or confidence intervals.

## Grouped-CV result and test context

[Verified] A_abstain_policy_v2.json and A_calibration_params_v2.json record a
grouped-CV estimate of accuracy 0.747664 at coverage 0.313324. It is a saved
summary; per-row OOF predictions and a grouped-CV risk curve are absent, so it
was not independently recalculated and has no CI here.

[Tested] At the frozen 0.64 threshold, the same-dev result is 0.751196 at
0.306003 coverage, versus the saved grouped-CV estimate 0.747664 at 0.313324.
They are close point estimates but have different evaluation procedures.
The separate A_learned_deferral_cv_v2.csv confidence result 0.754 at nominal
30% ranks all dev rows and is not a held-out-fold baseline. Optional learned
policies are not deployed; the verdict says deployed_policy_changed=false.

[Verified] Test at threshold 0.64 is 0.790323 accuracy at 0.288453 coverage
(95% CI 0.746722-0.834494); label it exploratory (test seen in v1).

## Decision

[Tested] The original target of 85% accuracy at about 30% coverage is NOT
achieved. At 30% top-k coverage accuracy is 0.754472 (95% CI
0.684742-0.818339); the 0.64 policy gives 0.751196 at 0.306003 coverage.

[Tested] 90% is observed only up to 0.080527 coverage (N=165) in the full
confidence-threshold scan. Its bootstrap interval falls below 90%, and the
threshold was selected on the same dev data. No practical minimum coverage
was specified; evidence does not establish a reliable 90% operating point.
Do not present low-coverage accuracy as overall model accuracy.