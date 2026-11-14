# E4 — DeBERTa experiment specification (v3)

**Drafted; Stage 1 remains unapproved.** No model was loaded or trained. Any
performance result from the available fold pool is **dev-only, optimistic**.

## Training-pool decision

| Finding | Status | Source |
|---|---|---|
| No train-only text file with question, reference, student answer, and labels was found in the scoped working-tree search. No non-test file named `sra_unified_splits_v1.parquet` was present in those scopes. | Verified, metadata/name search only; no split contents opened. | `project_s_qa/raw/`, `processed/`, `interim/`, notebook data exports, Phase 1, Phase 3. Search excluded archives, backups, test-named files, and cloud locations. |
| `dev_text_2049.parquet` is the available text table: 2,049 dev rows, with `dev_ua` and `dev_uq` splits. | Verified, dev-only. | Phase 3 file; its previously verified schema includes UID, dataset, split, question ID, five-way label, question, reference answer, and student answer. |
| Decision outcome **(b)**: any candidate trained only within these folds has a smaller training pool than v2, so label its result **“exploratory, smaller training pool, not comparable with v2.”** | Proposed consequence of the verified inventory; v2's full training pool is Reported from Jigar's task context. | This document and the dev-only fold design. |

No `nested_cv_folds_v2.csv` was created because there is no train-only pool to add. The existing `nested_cv_folds_v1.csv` is unchanged. A future approved train-only export should contain only train rows and the needed UID, dataset, question ID, label, question, reference answer, and student answer; Jigar should create it from an authorized source without opening or exporting test rows.

## Unseen-question QWK uncertainty

**Tested, dev-only, optimistic:** Path A (deployed pooled collapse then
argmax) on the 1,296 `dev_uq` rows and 27 dataset-question groups has QWK
0.294900. A seed-42 bootstrap resampling whole question groups 10,000 times
gives a 95% percentile interval 0.206416 to 0.377733 and bootstrap standard
error 0.043863. The supplied dev text and component-probability hashes matched
the approved values. No test data was read.

**Proposed approximate MDD:** use the conventional two-sided 5%, 80%-power
normal multiplier 1.96 + 0.84 = 2.80 and substitute the baseline bootstrap
SE for the unavailable paired-difference SE: 2.80 x 0.043863 = 0.122816
absolute QWK. This is only a rough proxy. Candidate predictions, paired
covariance, and candidate variance are unavailable, so the actual paired MDD
cannot be estimated yet. Averaging three seeds does not create more than 27
independent question groups.

| Candidate margin | Meaning | Interpretation |
|---:|---|---|
| 0.0100 | Allow at most a 0.010 QWK decrease from baseline. | About 0.23 baseline SE; very narrow relative to the observed uncertainty. |
| 0.0219 | Allow at most a 0.0219 decrease (half the baseline SE). | **Proposed default** for a descriptive comparison; not a pass/fail gate. |
| 0.0439 | Allow at most a 0.0439 decrease (one baseline SE). | A materially larger tolerated loss; not recommended as a hard gate. |
| 0.1228 | The rough proxy MDD. | A loss this large could be hard to distinguish under the stated approximation; far too permissive as an acceptable-loss margin. |

With only 27 unseen questions, unseen-QWK non-inferiority is an exploratory
guard, not a strong test. **Proposed decision:** report unseen QWK and the
margin comparison as a secondary result, not as a hard gate. Keep every other
E4 gate unchanged. The 0.64 threshold remains unchanged.

## E4 settings retained

**Proposed, unchanged from E4 v2:** seed supplied by `--seed` (exploratory
42; final 42, 123, 2026), LR 2e-5, 3 epochs, warmup 0.10, train batch 4 x
gradient accumulation 4, evaluation batch 8, max length 256, fp16, and
checkpoint selection by inner-validation Macro-F1. Checkpoint availability
and T4 fit remain Unverified. Macro-F1, accuracy, overall QWK, and Partial
recall/F1 gates are unchanged; negation controls remain diagnostic only;
latency is reported, not gated.
