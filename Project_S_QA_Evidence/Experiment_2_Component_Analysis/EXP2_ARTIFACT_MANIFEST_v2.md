# Experiment 2 artifact manifest

Dev-only inputs; no test artifacts opened. Manifest omits its own hash.

## Inputs

| Path | Bytes | SHA-256 | Rows | Unique UIDs |
| Project_S_QA_Evidence/Phase_3/dev_text_2049.parquet | 107715 | 21e7305557825b392a297fc4558b73e1161fcefb07d82c9f802e33c877836ea2 | 2049 | 2049 |
| Project_S_QA_Evidence/Phase_8_Accuracy_Max/A_component_probs_v7.parquet | 444822 | 71dd07621bb838b38af1932f43d985059a6a69e61d39361e6a5063eb5bdc5f88 | 2049 | 2049 |
| project_s_qa/A_submission_v2/reports_v2/A_deployed_dev_probs_v2.parquet | 131382 | 2e29a708152b288019a9fa50b55b9d823781e4bbe0144cd5ee533fee9ddb5b0e | 2049 | 2049 |
| Project_S_QA_Evidence/Phase_8_Accuracy_Max/x0_export_component_probs_v7.py | 8871 | 75b8ae23f41a9a5e92df4186c888c0dcdc23c2205b9882dc23b20cdadad0eb3b | n/a | n/a |
| project_s_qa/A_submission_v2/reports_v2/A_predict.py | 7626 | ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053 | n/a | n/a |

Class order: ['correct', 'contradictory', 'partially_correct_incomplete', 'irrelevant', 'non_domain']. Mapping: indices 1/3/4=Incorrect; 2=Partial; 0=Correct.
Seed=20261110; bootstrap=10000; populations=2,049 primary and 2,030 approved sensitivity.
Path A prediction agreement=2049/2,049; component-export Path A agreement=2049/2,049.

## Outputs

| File | Bytes | SHA-256 |
| EXP2_COMPONENT_ANALYSIS_REPORT_v2.md | 67311 | 57b3fc958c2ca7a23fb17ef45ac08f0a740c265e79a6f5528fcf2318d7f8aa7f |
| EXP2_COMPONENT_METRICS_v2.csv | 23145 | c522d13bec09610fa0a0033a0a0c4f50d5513f997df2e58284d495621a2b225b |
| EXP2_ABLATION_RESULTS_v2.csv | 3050 | 4b2871573d4032c14d0202490f37454cba4aa2d5f59a2e32d8fd39b632665808 |
| EXP2_ERROR_COMPLEMENTARITY_v2.csv | 1674 | 862a293ef28f170a9040dbdbcfcd4f4c230dd60c5e922da9ddd80411295c2f38 |
| EXP2_UID_LEVEL_ANALYSIS_v2.csv | 838390 | fa07e85fd120f16c4f89254a173aeb6df34fdf6a00663e094d45cc30c0d97077 |
| EXP2_BOOTSTRAP_RESULTS_v2.csv | 19436 | b68a6cbc164cd40d73f9de5447340404b9c9fa709e3def50d3924a9e24f72889 |
| EXP2_CONFUSION_MATRICES_v2.csv | 41255 | e5e251127edf8c13bf30343592649a8eeb136df35324af940079d0db75664d92 |
| EXP2_REPRODUCE_v1.py | 27525 | 48de7dc000cc4c41ac84d42025a242c0af61a0a52772c5672e4dae6cd68fa9a3 |
