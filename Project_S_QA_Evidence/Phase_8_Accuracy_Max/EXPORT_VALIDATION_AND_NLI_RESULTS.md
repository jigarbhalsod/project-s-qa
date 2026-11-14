# Export validation and NLI contradiction analysis

**Status: validation PASS; analysis BLOCKED. All validated scores below are
dev-only, optimistic.** No test content was opened.

## Export validation

| Check | Result |
|---|---|
| SHA-256 | **Verified:** `A_component_probs_v7.parquet` = `71dd07621bb838b38af1932f43d985059a6a69e61d39361e6a5063eb5bdc5f88`; matches supplied hash. |
| Rows and UIDs | **Verified:** export and dev-gold each have 2,049 rows and unique UIDs; 2,049 match, 0 missing, 0 extra. |
| Split | **Verified:** both contain `dev_ua` and `dev_uq`; no test split detected. Metadata agrees by UID. |
| Nulls | **Verified:** 0 null cells in the export. |
| Probability sums | **Verified:** max absolute row-sum error: ft `2.384185791015625e-07`, sb `4.440892098500626e-16`, nl `3.3306690738754696e-16`, pooled 3-class `2.220446049250313e-16`. All within 1e-5 of 1. |
| Class order | **Verified:** `['correct','contradictory','partially_correct_incomplete','irrelevant','non_domain']`; matches `A_predict.py` LABEL5_ORDER and the export's p0-p4 order. |

## Path reproduction

| Path | Recomputed correct | Expected (Reported) | Result |
|---|---:|---:|---|
| Path A: pooled collapse then argmax | 1,155 / 2,049 | 1,155 / 2,049 | **Verified MATCH** |
| Path B: five-way argmax then map | 1,189 / 2,049 | 1,189 / 2,049 | **Verified MATCH** |
| Rows with different Path A/B predictions | 336 | 336 | **Verified MATCH** |

## Contradiction routing analysis

**BLOCKED:** The approved `nli_contradiction_analysis.py` was run once after
validation. It stopped at line 12 before computing results or writing either
analysis output. After merging the two input tables, `question_id` is named
`question_id_x` and `question_id_g`; the script accesses `m.question_id` and
raises `AttributeError`. The two expected script outputs are absent:
`nli_contradiction_threshold_results.csv` and
`nli_contradiction_threshold_report.md`.

| Threshold | Contradiction rows | Pooled Correct among them | Wrong among those | Wrong caught / missed by 0.64 | Added review / new coverage / selective accuracy |
|---|---:|---:|---:|---:|---|
| 0.90 | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED |
| 0.95 | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED |
| 0.99 | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED |

Per-component accuracy, seen/unseen accuracy, and question-grouped bootstrap
intervals were not computed. No contradiction-rule effect is claimed. The
analysis script needs a separately approved correction and rerun before these
results can be reported. No change was made to the scorer or 0.64 threshold.
