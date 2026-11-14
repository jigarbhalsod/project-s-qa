# Accuracy audit: data alignment and provenance

Audit date: 6 Nov 2026. Read-only inputs; no notebook cells, model inference,
training or artifact changes were performed.

## Prediction files and identity

| Artifact | Rows | SHA-256 | Alignment result |
|---|---:|---|---|
| `A_deployed_dev_probs_v2.parquet` | 2,049 | `2e29a708152b288019a9fa50b55b9d823781e4bbe0144cd5ee533fee9ddb5b0e` | unique UIDs; labels and 5-way probabilities present |
| `A_test_scored_v2.parquet` | 7,093 | `8ec79019686135868b2ae739bac6b9fd7b8cc9fd636477936a39fc9969956faa` | unique UIDs; labels and deployed 3-way outputs present |
| `A_deployed_metrics_ci_v2.csv` | 6 metric rows | `31e49c3c02136543294972302db3fc453ba39f35ac346bb8a987223ad8a45126` | saved dev bootstrap metrics |
| `A_test_results_v2.csv` | 6 groups | `458839b4f42fbeb26116ff6810035b45936e71adbc911d3b3543afcc1e68f43f` | saved exploratory test metrics and CIs |

Both parquet files have zero null or duplicate UIDs, zero missing predictions,
and zero `label5` to `score_ours` mapping mismatches. The dev and test UID sets
are disjoint. The dev five-way probability rows are finite and sum to one
within a maximum absolute error of 0.000000058. Dataset labels match UID
prefixes. Dev has 753 `dev_ua` rows and 1,296 `dev_uq` rows across 177 questions.
Test has 979 `test_ua`, 1,552 `test_uq`, and 4,562 `test_ud` rows across 248
questions.

## Label and prediction alignment

The notebook defines `LABEL5_ORDER` as `correct`, `contradictory`,
`partially_correct_incomplete`, `irrelevant`, `non_domain`. The three-class
truth mapping is: `correct -> 2`, `partially_correct_incomplete -> 1`, and
`contradictory`, `irrelevant`, `non_domain -> 0`. This is the project mapping,
not a generic checkpoint mapping.

Development predictions were reconstructed only from saved five-class
probabilities using the inspected deployed `_to3` collapse:
incorrect = probability columns 1+3+4, partial = column 2, correct = column 0.
No scorer was imported and no new model predictions were generated. Test
predictions were read directly from saved `pred_score` and compared with
`score_ours` by row UID.

## Split and leakage checks

- Dev `dev_ua` and `dev_uq` have no shared question IDs.
- Test `test_ua` and `test_uq` share `BEE-66c4dd68`, so their question-level
  populations are not fully disjoint.
- 27 question IDs labelled `dev_uq` also appear in test `test_ua` (7 Beetle,
  20 SciEntsBank). The source split parquet is unavailable locally, so the
  meaning of this assignment cannot be resolved here.
- No row UID overlaps between dev and test. The raw split table
  `processed/sra_unified_splits_v1.parquet` is absent, so train-vs-dev/test UID
  overlap and a fresh source-label join are **not checked**.
- The test-access log records three evaluations, and the project freeze
  manifest marks test results exploratory because the test sets were seen in
  v1. Test numbers are labelled **exploratory (test seen in v1)**.

Overall row-aligned dev/test metrics can be recalculated from these files.
Use caution with test `test_ua` versus `test_uq` comparisons because of their
question-ID overlap. Do not treat test subgroup categories as a clean partition
until split metadata is reconciled.

## Scorer and manifest provenance

The packaged scorer `A_predict.py` has SHA-256
`ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053`.
The packaged reference JSON stores `scorer_mode=pooled` and that same scorer
hash. Both match the local submission manifest. Key evaluation files listed
above also match their submission-manifest hashes.

The root-level `project_s_qa/reports_v2/A_demo_reference_outputs_v2.json`
has SHA-256 `c99b7d84d000046c9629708d5ee440d5a20ab28fd298f63708e2e8c13f89dc92`,
while the packaged reference JSON has SHA-256
`ea5288e9f12b25d28a66f36ec38d48b08c65e19452bf3b5efa17eed2be20aeb9`. They are
different JSON builds; both record the same `A_predict.py` hash. The evaluation
artifacts were taken from the packaged build, whose manifest is present and
hash-verified.

The working notebook is valid JSON with 167 cells and SHA-256 `5eb5dc4fd1ad85dce55c9b1222603fc11de19d51bb682103fc7923bc78b5faf0`. This differs from the Phase 4 manifest hash `a35efc489c25806f2ad3db8684006dc2d627634dc1e6d2a61d3fbc75c615030e`; the reason is unverified. Its saved evaluation cells have null `execution_count`; Phase 4 also records no separate executed notebook. Artifact integrity is verified locally; Colab execution chronology and cloud synchronization remain unverified.
