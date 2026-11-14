# Project S Q&A branch: final tables (v2)

Dev numbers were used to select the scorer and threshold, so they are optimistic. Test numbers are EXPLORATORY (the test sets were already scored in v1).

## Table 1: deployed scorer on dev, 95% question-bootstrap CI

| group | n_questions | n_answers | qwk_3level | macroF1_5 |
|---|---|---|---|---|
| seen answers (dev_ua) | 150 | 753 | 0.630 [0.562, 0.692] | 0.730 [0.689, 0.766] |
| unseen questions (dev_uq) | 27 | 1296 | 0.317 [0.199, 0.412] | 0.490 [0.406, 0.544] |
| ALL dev | 177 | 2049 | 0.432 [0.358, 0.509] | 0.579 [0.523, 0.629] |

## Table 2: paired differences on dev, deployed minus comparator ('*' = CI excludes 0)

| group | comparator | macroF1_5 | qwk_3level |
|---|---|---|---|
| ALL dev | avg3 native (reference only) | -0.027 [-0.044, -0.009]* | -0.041 [-0.072, -0.012]* |
| ALL dev | finetuned_distilroberta | +0.021 [+0.002, +0.043]* | +0.034 [-0.007, +0.073] |
| ALL dev | majority | +0.460 [+0.404, +0.511]* | +0.432 [+0.358, +0.509]* |
| ALL dev | roberta_base | -0.023 [-0.055, +0.012] | -0.028 [-0.098, +0.046] |
| ALL dev | sbert_pair_features_lr | +0.022 [-0.003, +0.051] | +0.031 [-0.014, +0.075] |
| ALL dev | stacker (out-of-fold) | n/a | -0.015 [-0.070, +0.045] |
| ALL dev | tfidf_text_plus_similarity | +0.034 [+0.001, +0.073]* | +0.044 [-0.016, +0.107] |
| seen answers (dev_ua) | avg3 native (reference only) | -0.007 [-0.027, +0.014] | -0.018 [-0.054, +0.018] |
| seen answers (dev_ua) | finetuned_distilroberta | +0.035 [+0.012, +0.061]* | +0.024 [-0.021, +0.072] |
| seen answers (dev_ua) | majority | +0.613 [+0.570, +0.651]* | +0.630 [+0.562, +0.692]* |
| seen answers (dev_ua) | roberta_base | -0.005 [-0.035, +0.026] | -0.054 [-0.109, -0.001]* |
| seen answers (dev_ua) | sbert_pair_features_lr | +0.063 [+0.028, +0.106]* | +0.052 [+0.002, +0.101]* |
| seen answers (dev_ua) | stacker (out-of-fold) | n/a | +0.071 [+0.003, +0.143]* |
| seen answers (dev_ua) | tfidf_text_plus_similarity | +0.088 [+0.060, +0.120]* | +0.091 [+0.029, +0.156]* |
| unseen questions (dev_uq) | avg3 native (reference only) | -0.040 [-0.070, -0.014]* | -0.055 [-0.102, -0.015]* |
| unseen questions (dev_uq) | finetuned_distilroberta | +0.014 [-0.013, +0.044] | +0.043 [-0.014, +0.100] |
| unseen questions (dev_uq) | majority | +0.370 [+0.283, +0.422]* | +0.317 [+0.199, +0.412]* |
| unseen questions (dev_uq) | roberta_base | -0.034 [-0.081, +0.016] | -0.014 [-0.115, +0.104] |
| unseen questions (dev_uq) | sbert_pair_features_lr | -0.001 [-0.035, +0.033] | +0.017 [-0.047, +0.075] |
| unseen questions (dev_uq) | stacker (out-of-fold) | n/a | -0.066 [-0.140, +0.009] |
| unseen questions (dev_uq) | tfidf_text_plus_similarity | -0.001 [-0.046, +0.051] | +0.018 [-0.067, +0.107] |

## Table 3: exploratory test results

| group | n | questions | macroF1_5 | qwk_3level | acc3 | coverage | acc_auto |
|---|---|---|---|---|---|---|---|
| ALL test | 7093 | 248 | 0.576 [0.543, 0.606] | 0.454 [0.392, 0.515] | 0.588 | 0.288 | 0.790 [0.747, 0.834] |
| beet/test_ua | 439 | 44 | 0.613 [0.555, 0.673] | 0.578 [0.510, 0.644] | 0.677 | 0.383 | 0.839 [0.776, 0.898] |
| beet/test_uq | 819 | 9 | 0.513 [0.449, 0.557] | 0.450 [0.325, 0.554] | 0.615 | 0.283 | 0.819 [0.694, 0.902] |
| scie/test_ua | 540 | 135 | 0.501 [0.405, 0.594] | 0.514 [0.441, 0.583] | 0.606 | 0.328 | 0.831 [0.769, 0.887] |
| scie/test_uq | 733 | 15 | 0.353 [0.283, 0.420] | 0.421 [0.253, 0.575] | 0.553 | 0.345 | 0.771 [0.599, 0.892] |
| scie/test_ud | 4562 | 46 | 0.541 [0.500, 0.574] | 0.441 [0.353, 0.523] | 0.578 | 0.267 | 0.776 [0.719, 0.836] |

## Table 4: deployed scorer vs frozen v1 on test

| dataset | split | deployed_F1 | v1_simple_F1 | v1_stacked_F1 | deployed_QWK | v1_simple_QWK | v1_stacked_QWK |
|---|---|---|---|---|---|---|---|
| beetle | test_ua | 0.613 | 0.614 | 0.595 | 0.578 | 0.641 | 0.609 |
| beetle | test_uq | 0.513 | 0.584 | 0.52 | 0.45 | 0.513 | 0.48 |
| scientsbank | test_ua | 0.501 | 0.57 | 0.538 | 0.514 | 0.544 | 0.532 |
| scientsbank | test_uq | 0.353 | 0.359 | 0.378 | 0.421 | 0.454 | 0.497 |
| scientsbank | test_ud | 0.541 | 0.571 | 0.526 | 0.441 | 0.479 | 0.48 |

## Table 5: risk-coverage

| threshold | dev_coverage | dev_acc_auto | test_coverage | test_acc_auto | frozen |
|---|---|---|---|---|---|
| 0.4 | 0.92 | 0.586 | 0.918 | 0.605 |  |
| 0.5 | 0.638 | 0.643 | 0.609 | 0.681 |  |
| 0.6 | 0.379 | 0.714 | 0.368 | 0.754 |  |
| 0.64 | 0.306 | 0.751 | 0.288 | 0.79 | <- frozen |
| 0.7 | 0.211 | 0.774 | 0.198 | 0.825 |  |
| 0.75 | 0.144 | 0.828 | 0.125 | 0.865 |  |
| 0.8 | 0.103 | 0.858 | 0.08 | 0.89 |  |
| 0.85 | 0.063 | 0.946 | 0.035 | 0.924 |  |

Dev expected calibration error (10 bins): 0.017
