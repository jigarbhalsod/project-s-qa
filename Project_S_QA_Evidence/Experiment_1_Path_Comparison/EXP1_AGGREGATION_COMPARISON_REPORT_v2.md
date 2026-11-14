# Experiment 1 — Path A vs Path B

**Scope:** dev-only, optimistic; saved predictions/probabilities only. No model inference, training, notebook execution, or test data access.

## Inputs and validation

- Path A and gold: `project_s_qa/A_submission_v2/reports_v2/A_deployed_dev_probs_v2.parquet` SHA-256 `2e29a708152b288019a9fa50b55b9d823781e4bbe0144cd5ee533fee9ddb5b0e`.
- Component probabilities: `Project_S_QA_Evidence/Phase_8_Accuracy_Max/A_component_probs_v7.parquet` SHA-256 `71dd07621bb838b38af1932f43d985059a6a69e61d39361e6a5063eb5bdc5f88`.
- Dev text metadata: `Project_S_QA_Evidence/Phase_3/dev_text_2049.parquet` SHA-256 `21e7305557825b392a297fc4558b73e1161fcefb07d82c9f802e33c877836ea2`.
- A_predict source checked without import: SHA-256 `ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053`; class order and collapse source verified.
- PASS: 2,049 unique UIDs per artifact; identical UID sets; dataset/split/question_id/label5 match by UID; only dev_ua/dev_uq splits; required columns, finite probabilities, row sums, mapped gold labels, and Path A export parity verified.
- Path A uses stored deployed d_p0–d_p4, collapse `[p1+p3+p4, p2, p0]`, argmax. Path B averages saved ft/sb/nl five-class probabilities, five-way argmax, then maps 1/3/4→Incorrect, 2→Partial, 0→Correct.
- Dedup sensitivity retains the lexicographically smallest UID per exact content group; all original rows remain unchanged. Raw-source provenance remains unverified.

## Overall metrics

  population   scope   path    n  accuracy  macro_f1  weighted_f1  partial_precision  partial_recall  partial_f1      qwk
primary_2049 overall Path A 2049  0.563690  0.527046     0.549617           0.514925        0.263359    0.348485 0.401530
primary_2049 overall Path B 2049  0.580283  0.556598     0.577211           0.463303        0.385496    0.420833 0.431834
  dedup_2030 overall Path A 2030  0.563547  0.527431     0.549544           0.514925        0.265385    0.350254 0.400945
  dedup_2030 overall Path B 2030  0.580788  0.557696     0.577867           0.463303        0.388462    0.422594 0.433827

## Dataset and seen/unseen metrics

  population         scope   path    n  accuracy  macro_f1  weighted_f1  partial_precision  partial_recall  partial_f1      qwk
primary_2049   SciEntsBank Path A 1129  0.542958  0.518796     0.533114           0.474747        0.316498    0.379798 0.369712
primary_2049   SciEntsBank Path B 1129  0.539415  0.526481     0.541288           0.417508        0.417508    0.417508 0.374549
primary_2049        Beetle Path A  920  0.589130  0.528979     0.563938           0.628571        0.193833    0.296296 0.435961
primary_2049        Beetle Path B  920  0.630435  0.591050     0.618778           0.561151        0.343612    0.426230 0.495757
primary_2049   seen_dev_ua Path A  753  0.691899  0.665502     0.685324           0.722222        0.414894    0.527027 0.587950
primary_2049   seen_dev_ua Path B  753  0.721116  0.706369     0.720822           0.641618        0.590426    0.614958 0.629784
primary_2049 unseen_dev_uq Path A 1296  0.489198  0.446166     0.470140           0.375000        0.178571    0.241935 0.294900
primary_2049 unseen_dev_uq Path B 1296  0.498457  0.468277     0.493049           0.346008        0.270833    0.303840 0.316863
  dedup_2030   SciEntsBank Path A 1110  0.542342  0.518778     0.532399           0.474747        0.320819    0.382892 0.367346
  dedup_2030   SciEntsBank Path B 1110  0.539640  0.527697     0.541710           0.417508        0.423208    0.420339 0.376661
  dedup_2030        Beetle Path A  920  0.589130  0.528979     0.563938           0.628571        0.193833    0.296296 0.435961
  dedup_2030        Beetle Path B  920  0.630435  0.591050     0.618778           0.561151        0.343612    0.426230 0.495757
  dedup_2030   seen_dev_ua Path A  746  0.690349  0.664621     0.683408           0.722222        0.414894    0.527027 0.585837
  dedup_2030   seen_dev_ua Path B  746  0.719839  0.705856     0.719443           0.641618        0.590426    0.614958 0.629048
  dedup_2030 unseen_dev_uq Path A 1284  0.489875  0.447154     0.471233           0.375000        0.180723    0.243902 0.295442
  dedup_2030 unseen_dev_uq Path B 1284  0.500000  0.470083     0.494951           0.346008        0.274096    0.305882 0.320533

## Paired bootstrap differences (Path B minus Path A)

10,000 resamples per population and scheme; seed 20261106. Row bootstrap samples rows; grouped bootstrap samples question IDs. Percentile 95% CIs:

| Population | Scheme | Metric | Difference | 95% CI | Includes zero |
|---|---|---|---:|---|---|
| primary_2049 | paired_row | accuracy | 0.016593 | [0.001464, 0.031723] | no |
| primary_2049 | paired_row | macro_f1 | 0.029553 | [0.013560, 0.045233] | no |
| primary_2049 | paired_row | weighted_f1 | 0.027594 | [0.012388, 0.042708] | no |
| primary_2049 | paired_row | partial_precision | -0.051623 | [-0.088981, -0.015529] | no |
| primary_2049 | paired_row | partial_recall | 0.122137 | [0.094876, 0.150094] | no |
| primary_2049 | paired_row | partial_f1 | 0.072348 | [0.043292, 0.101592] | no |
| primary_2049 | paired_row | qwk | 0.030304 | [0.002650, 0.057171] | no |
| primary_2049 | paired_question_group | accuracy | 0.016593 | [-0.006211, 0.040239] | yes |
| primary_2049 | paired_question_group | macro_f1 | 0.029553 | [0.007466, 0.054207] | no |
| primary_2049 | paired_question_group | weighted_f1 | 0.027594 | [0.005332, 0.050698] | no |
| primary_2049 | paired_question_group | partial_precision | -0.051623 | [-0.089422, -0.011555] | no |
| primary_2049 | paired_question_group | partial_recall | 0.122137 | [0.086629, 0.167117] | no |
| primary_2049 | paired_question_group | partial_f1 | 0.072348 | [0.041250, 0.112364] | no |
| primary_2049 | paired_question_group | qwk | 0.030304 | [-0.005175, 0.064918] | yes |
| dedup_2030 | paired_row | accuracy | 0.017241 | [0.001478, 0.033005] | no |
| dedup_2030 | paired_row | macro_f1 | 0.030264 | [0.014235, 0.046465] | no |
| dedup_2030 | paired_row | weighted_f1 | 0.028323 | [0.012886, 0.043916] | no |
| dedup_2030 | paired_row | partial_precision | -0.051623 | [-0.089294, -0.015407] | no |
| dedup_2030 | paired_row | partial_recall | 0.123077 | [0.095785, 0.151229] | no |
| dedup_2030 | paired_row | partial_f1 | 0.072340 | [0.043382, 0.100959] | no |
| dedup_2030 | paired_row | qwk | 0.032882 | [0.005615, 0.059867] | no |
| dedup_2030 | paired_question_group | accuracy | 0.017241 | [-0.005565, 0.040269] | yes |
| dedup_2030 | paired_question_group | macro_f1 | 0.030264 | [0.008065, 0.054067] | no |
| dedup_2030 | paired_question_group | weighted_f1 | 0.028323 | [0.005951, 0.050928] | no |
| dedup_2030 | paired_question_group | partial_precision | -0.051623 | [-0.089759, -0.012103] | no |
| dedup_2030 | paired_question_group | partial_recall | 0.123077 | [0.087523, 0.167703] | no |
| dedup_2030 | paired_question_group | partial_f1 | 0.072340 | [0.041255, 0.112029] | no |
| dedup_2030 | paired_question_group | qwk | 0.032882 | [-0.002191, 0.066449] | yes |

## Disagreements and decision gates

  population    n  different  A_correct_B_wrong  A_wrong_B_correct  both_correct  both_wrong  questions
primary_2049 2049        336                116                150          1039         744        177
  dedup_2030 2030        334                115                150          1029         736        177

McNemar was not used: repeated answers are clustered by question, so independent-pair assumptions are not established; question-grouped bootstrap is reported instead.

Primary accuracy difference: 0.016593; question-grouped CI [-0.006211, 0.040239]. Sensitivity differences: {'accuracy': 0.017241379310344862, 'macro_f1': 0.0302644167907824, 'partial_recall': np.float64(0.12307692307692308), 'partial_f1': np.float64(0.07234033515281524)}.
Deduplicated unseen/seen safety check: unseen accuracy non-regression=True.
**Classification: INCONCLUSIVE.** Path B is not promoted to production.

## Reproduction

From the Project 4 root: `python Project_S_QA_Evidence/Experiment_1_Path_Comparison/EXP1_REPRODUCE_v2.py`. Requires pandas, NumPy, scikit-learn and an installed parquet engine. Refuses test-named paths, source hash/schema/alignment failures, or existing v2 outputs.
