# Nested question-grouped CV design

**Drafted.** Folds use only `Phase_3/dev_text_2049.parquet` (2,049 rows,
2,049 UIDs) and group key `dataset|question_id`. A filename-only search of
the working tree outside `.git`, `archive`, backups, test-named files, and the
unified split found no train-only text parquet; external/Drive files are
Unverified. Separate official training data is **BLOCKED**.
The fold file is a dev-only cross-validation design, not an independent
confirmation set. All results remain **dev-only, optimistic**.

## Assignment

`nested_cv_folds_v1.csv` has exactly `uid,dataset,question_id,label3,
outer_fold,inner_fold`. Outer assignment is five-fold stratified grouped CV
(seed 42); inner assignment is four-fold stratified grouped CV (seed 42).
The three-way mapping is Correct -> 2, Partial -> 1, all other five-way
labels -> 0. Stratification is approximate because each question group is
indivisible. Verified checks: 2,049 rows and unique UIDs; no group appears in
more than one outer or inner fold.

For an outer fold, hold that fold out completely. Use only the remaining outer
training rows for inner-fold model selection; the global `inner_fold` labels
are restricted to those rows. Select epoch by mean inner validation Macro-F1,
refit on all outer-training rows for that epoch count, then predict the held-
out outer fold once. The outer fold must not affect selection. Repeat for each
outer fold and seed. This plan uses dev rows for both training and outer
evaluation; it does not recreate the original train split.

## Outer fold sizes and class balance

Counts below are computed from the fold file. Class columns are Incorrect,
Partial, Correct. Scope: dev-only, optimistic.

| Fold | Rows | Incorrect | Partial | Correct | dev_ua rows / questions | dev_uq rows / questions | Beetle / SciEntsBank rows |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 409 | 132 | 104 | 173 | 146 / 29 | 263 / 6 | 149 / 260 |
| 1 | 410 | 132 | 105 | 173 | 131 / 27 | 279 / 6 | 184 / 226 |
| 2 | 412 | 132 | 106 | 174 | 120 / 27 | 292 / 6 | 173 / 239 |
| 3 | 410 | 132 | 105 | 173 | 186 / 32 | 224 / 4 | 200 / 210 |
| 4 | 408 | 131 | 104 | 173 | 170 / 35 | 238 / 5 | 214 / 194 |
| Total | 2,049 | 659 | 524 | 866 | 753 / 150 | 1,296 / 27 | 920 / 1,129 |

There are 177 dataset-question groups total. Each is assigned to one outer
fold. Inner-fold row counts (Incorrect / Partial / Correct) are: fold 0 =
166 / 131 / 217 (514 rows); fold 1 = 163 / 131 / 216 (510); fold 2 =
166 / 131 / 217 (514); fold 3 = 164 / 131 / 216 (511). These are global
assignments, and each outer iteration must first exclude its held-out outer
fold.

## Unseen-QWK margin proposal

**Tested, dev-only:** a 2,000-resample, seed-42 question-group bootstrap of
the frozen pooled path on `dev_uq` gives baseline QWK 95% interval
0.2097-0.3760 (width 0.1663). **Proposed:** retain E4's 0.01 absolute QWK
non-inferiority margin; it is well below half this interval width (0.0831)
and is therefore conservative relative to this sampling range. The gate must
still report the interval and cannot use this dev resampling as independent
confirmation.

## Pool, limits, and uncovered work

The pool is the 2,049 dev rows only: 753 `dev_ua` rows and 1,296 `dev_uq`
rows. No train-only text source was found, so production-like training on the
official train split is blocked until Jigar provides an approved derived
train-only text file. The 4,562-row official unseen-domain set was not opened;
its clean-access history is Unverified. The folds do not establish a locked
test result, validate CBSE answers, resolve near-duplicate label conflicts,
or replace human review. Stage 1 remains unapproved.
