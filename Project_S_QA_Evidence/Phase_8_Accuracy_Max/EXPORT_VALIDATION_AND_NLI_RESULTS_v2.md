# Export validation and NLI contradiction analysis (v2)

**Tested — dev-only, optimistic; thresholds were evaluated on these same dev
rows.** No test file or split was opened. The analysis script was run once;
the original script and report were left unchanged.

## Export validation

| Check | Result |
|---|---|
| Export hash | `A_component_probs_v7.parquet`: `71dd07621bb838b38af1932f43d985059a6a69e61d39361e6a5063eb5bdc5f88` (matches supplied hash). |
| Rows and UID alignment | Export and dev gold each have 2,049 rows and unique UIDs; 2,049 matched, 0 missing, 0 extra. |
| Split and labels | Both are dev-only (`dev_ua`, `dev_uq`); UID, dataset, split, question_id and label5 agree after merge. |
| Nulls and probability sums | 0 export nulls. Maximum absolute row-sum error: ft 2.384185791015625e-07; sb 4.440892098500626e-16; nl 3.3306690738754696e-16; pooled 3-class 2.220446049250313e-16. All within 1e-5 of 1. |
| Label order | `correct`, `contradictory`, `partially_correct_incomplete`, `irrelevant`, `non_domain`; matches `A_predict.py` LABEL5_ORDER. |

## Prediction path reproduction

| Path | Correct | Expected (Reported) | Result |
|---|---:|---:|---|
| Path A: pooled collapse then argmax | 1,155 / 2,049 | 1,155 / 2,049 | MATCH |
| Path B: five-way argmax then map | 1,189 / 2,049 | 1,189 / 2,049 | MATCH |
| Different Path A/B predictions | 336 | 336 | MATCH |

## Contradiction threshold results

Baseline is recomputed from confidence >= 0.64: coverage 0.306003 and selective
accuracy 0.751196. `caught` and `missed` count wrong rows among cases the pooled
scorer predicted Correct with contradiction >= threshold. Added review rows
are previously auto-scored rows sent to review by the extra rule. Routing does
not change the pooled prediction; overall accuracy remains 1,155/2,049.

| Threshold | Rows >= t | Gold-label mix (contradictory, correct, partial, irrelevant, non-domain) | Pooled Correct | Wrong among those | Wrong caught / missed by 0.64 | Added reviews | New coverage | New selective accuracy |
|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 0.90 | 360 | 129, 91, 82, 55, 3 | 73 | 37 | 36 / 1 | 124 | 0.245486 | 0.755467 |
| 0.95 | 342 | 125, 87, 74, 53, 3 | 70 | 35 | 34 / 1 | 118 | 0.248414 | 0.756385 |
| 0.99 | 252 | 102, 63, 52, 35, 0 | 55 | 32 | 31 / 1 | 91 | 0.261591 | 0.757463 |

Paired 95% question-group bootstrap intervals (2,000 resamples, seed 42) for
new-minus-baseline coverage and selective accuracy:

| Threshold | Coverage difference CI | Selective-accuracy difference CI |
|---:|---|---|
| 0.90 | [-0.086657, -0.040020] | [-0.022387, 0.037198] |
| 0.95 | [-0.083097, -0.037919] | [-0.022123, 0.039222] |
| 0.99 | [-0.066135, -0.027670] | [-0.017363, 0.034154] |

## Components and question groups

| Component/path | Correct / N |
|---|---:|
| DistilRoBERTa | 1,135 / 2,049 |
| SBERT-LR | 1,099 / 2,049 |
| NLI-LR | 1,012 / 2,049 |
| NLI-LR correct where pooled is wrong | 208 / 2,049 |

| Dev group | N | Pooled accuracy | DistilRoBERTa | SBERT-LR | NLI-LR |
|---|---:|---:|---:|---:|---:|
| Seen (`dev_ua`) | 753 | 0.691899 | 0.681275 | 0.682603 | 0.515272 |
| Unseen (`dev_uq`) | 1,296 | 0.489198 | 0.479938 | 0.451389 | 0.481481 |

All results are dev-only and optimistic. The contradiction thresholds were
assessed on the same rows; they are not independent confirmation and do not
justify a scorer change. `A_predict.py` and the 0.64 threshold were not changed.
