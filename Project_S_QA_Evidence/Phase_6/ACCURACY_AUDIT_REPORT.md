# Project S accuracy audit (post-Phase 4)

Audit date: 6 Nov 2026. This audit reads saved predictions and probabilities only.
No notebook cell or model inference was run. It imports no scorer or model runtime.

## Answers

- **3-class accuracy:** dev, optimistic: 0.563690 (n=2,049). Exploratory test:
  0.587904 (n=7,093).
- **5-class accuracy:** dev, optimistic: 0.554905 (n=2,049). Test: not
  calculable from the saved test parquet; it has only three-class predictions.
- **QWK:** using the deployed `A_predict._to3` probability-collapse rule, dev QWK
  is 0.401530. Exploratory test QWK is 0.453888.
- **Unseen questions (dev_uq):** 3-class accuracy 0.489198; 5-class accuracy
  0.469136; deployed-rule 3-class QWK 0.294900 (n=1,296; 27 questions).
- **At the frozen 0.64 review threshold:** dev coverage 0.306003 and accuracy
  among auto-scored answers 0.751196 (627 accepted); exploratory test coverage
  0.288453 and auto-scored accuracy 0.790323 (2,046 accepted).
- **85% at about 30% coverage:** NOT achieved. The dev gap is 9.88 percentage
  points. The saved question-grouped CV estimate is 0.747664 accuracy at
  0.313324 coverage (10.23 points below target). Test is exploratory and is
  5.97 points below target at its 0.288453 coverage.

## Method and results

The deployed scorer is the pooled mean of the five-class probabilities from
fine-tuned DistilRoBERTa, SBERT-LR and NLI-LR. The inspected `A_predict.py`
then sums classes 1, 3 and 4 into `incorrect`, keeps class 2 as `partial`, and
class 0 as `correct`; the final prediction is the argmax of those three sums.
Temperature is 1.0000000000000004 and the frozen confidence threshold is 0.64.

For dev, the saved `d_p0` to `d_p4` probabilities were mapped using that exact
three-class rule. The five-class prediction is the argmax in `LABEL5_ORDER`:
`correct`, `contradictory`, `partially_correct_incomplete`, `irrelevant`,
`non_domain`. The project three-class truth mapping is `incorrect=0`,
`partial=1`, `correct=2`, from the notebook's `OURS_3`/`SCORE` mapping.

The dev 5-class accuracy is 0.554905 and macro-F1 is 0.578892. Dev 3-class
macro-F1 is 0.527046, weighted-F1 0.549617, macro-precision 0.570526, and
macro-recall 0.542716. All dev values are **dev, optimistic** because the
scorer and policy were selected using dev data. Per-class metrics and confusion
matrices are in `ACCURACY_METRICS.csv`.

There is a material dev QWK definition mismatch. The saved evaluation file
reports QWK 0.431834 (95% question-bootstrap CI 0.357853 to 0.508722). The
notebook's metrics cell obtains that value by taking the five-class argmax and
then mapping that label to three classes. The deployed `A_predict.py` instead
sums five-class probabilities into three classes before choosing a label. On
the same saved dev probabilities, that deployed rule gives QWK 0.401530 and
accuracy 0.563690. The saved unseen-question QWK 0.317 likewise uses the
five-class-argmax mapping; the deployed-rule value is 0.294900. The saved
macro-F1-5 values do reproduce from the saved probabilities. Keep both QWK
figures distinguished; do not describe 0.431834 as recalculated deployed-API
QWK.

The saved test parquet stores the scorer's three-class `pred_score`, truth
labels and confidence. Recalculation gives 3-class accuracy 0.587904, QWK
0.453888 and macro-F1-3 0.533193. These agree with the saved test-results
points (accuracy CI 0.548677 to 0.627816; QWK CI 0.392403 to 0.515201).
The saved test macro-F1-5 is 0.575732 (95% CI 0.542755 to 0.605536), but the
five-class test predictions are absent, so five-class accuracy and a fresh
five-class macro-F1 calculation are unavailable. Every test result is
**exploratory (test seen in v1)**.

At threshold 0.64, dev review accuracy is 0.481013 (n=1,422); test review
accuracy is 0.505845 (n=5,047). The threshold was fixed from dev calibration.
The saved grouped-CV estimate uses question-grouped folds and is an estimate,
not a new prediction run or test result.


A separate saved optional grouped-CV sweep reports the confidence baseline at
0.754 accuracy for nominal 0.30 coverage. That row ranks confidence on all dev
rows and is not a held-out fold estimate; it is not used as the honest CV
result. The optional learned-review rules report 0.805 and 0.815 at 0.30
coverage, but they are separate policies and `deployed_policy_changed=false`;
they are not the deployed scorer's performance.
## Evidence and limitations

Evaluation source: `project_s_qa/A_submission_v2/reports_v2/`.
The submission manifest hashes match the inspected scorer, reference JSON,
dev probabilities, test predictions, metrics, calibration and policy files.
The packaged `A_predict.py` SHA-256 is
`ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053`; the
packaged reference JSON stores the same scorer hash and `scorer_mode=pooled`.
The separate root reference JSON has a different file hash, but also stores that
same scorer hash. The packaged JSON is used here because it is listed by the
submission manifest with these evaluation artifacts.

UID alignment checks: dev 2,049 rows and test 7,093 rows; no missing or
duplicate UIDs; no dev/test UID overlap; no prediction or label-map mismatch.
The raw `processed/sra_unified_splits_v1.parquet` is absent locally, so a fresh
join to the source split file and train-vs-evaluation UID leakage check are
unverified. Dev `dev_ua` and `dev_uq` question IDs are disjoint. Test
`test_ua` and `test_uq` share one question ID (`BEE-66c4dd68`); additionally,
27 `dev_uq` question IDs occur in test `test_ua` (7 Beetle, 20 SciEntsBank).
Therefore those test subgroup labels are not mutually clean for seen/unseen
question comparisons. The overall test metric remains row-aligned, but subgroup
comparisons should be treated cautiously.

The working notebook is valid JSON with 167 cells and SHA-256 `5eb5dc4fd1ad85dce55c9b1222603fc11de19d51bb682103fc7923bc78b5faf0`. This differs from the Phase 4 manifest hash `a35efc489c25806f2ad3db8684006dc2d627634dc1e6d2a61d3fbc75c615030e`; the reason is unverified. Its inspected evaluation cells have null execution counts, so local outputs and package hashes do not prove when or where the evaluation ran. Cloud synchronization is unverified. No
CBSE/Indian schoolchildren or pilot validation is established by these results.
CBSE/Indian schoolchildren or pilot validation is established by these results.
Test sets were previously scored in v1; no test result should be presented as
confirmatory.

## Exact source artifacts

- `notebooks/Jigar_Q&A_Branch_Baseline_COPY.ipynb`
- `project_s_qa/A_submission_v2/reports_v2/A_predict.py`
- `project_s_qa/A_submission_v2/reports_v2/A_demo_reference_outputs_v2.json`
- `project_s_qa/A_submission_v2/reports_v2/A_deployed_dev_probs_v2.parquet`
- `project_s_qa/A_submission_v2/reports_v2/A_test_scored_v2.parquet`
- `project_s_qa/A_submission_v2/reports_v2/A_deployed_metrics_ci_v2.csv`
- `project_s_qa/A_submission_v2/reports_v2/A_test_results_v2.csv`
- `project_s_qa/A_submission_v2/reports_v2/A_calibration_params_v2.json`
- `project_s_qa/A_submission_v2/reports_v2/A_abstain_policy_v2.json`
- `project_s_qa/A_submission_v2/reports_v2/A_submission_manifest_v2.json`
- `Project_S_QA_Evidence/Phase_4/PHASE_4_FREEZE_MANIFEST.json`
- `project_s_qa/A_submission_v2/reports_v2/A_submission_manifest_v2.json` (created 2026-11-05T21:39:32)
- `project_s_qa/A_submission_v2/reports_v2/A_test_access_log_v2.json`
- `project_s_qa/A_submission_v2/reports_v2/A_learned_deferral_cv_v2.csv` and `A_learned_deferral_verdict_v2.json`
