# Experiment 3 risk register

Scope: static source and dev-only saved-artifact review. No model or checkpoint
was loaded. Severity follows the Experiment 3 definitions.

| Severity | Risk | Evidence and status | Impact | Recommended resolution |
|---|---|---|---|---|
| HIGH | Training/dev UID exclusion cannot be proven | [Unverified] No exact train-only UID manifest is linked to the saved FT or pooled-LR artifacts. | A nonzero overlap cannot be ruled out; do not say overlap is zero. | Provide immutable train UID lists for each fitted artifact and compare against the 2,049 dev UIDs. |
| HIGH | Exact fitted estimator provenance is missing | [Unverified] pooled_lr_v2.joblib is present and hashed but was not deserialized; fit script/config/seed/data UID record is absent. | Cannot validate what data or preprocessing fitted the deployed SBERT-LR and NLI-LR. | Preserve fit source, UID list, hyperparameters, seed and artifact hash at generation. |
| HIGH | Checkpoint-to-prediction linkage is missing | [Unverified] Current FT weights have a hash, but the 30 Oct run manifest skipped hashing the large weights; dev predictions have no embedded model hashes. | Current checkpoint cannot be established as the model that generated saved dev probabilities. | Recover the original generation record or regenerate only after a separately approved protocol. |
| HIGH | Probability-generation version is not fully traceable | [Unverified] Saved probabilities have no row-level generator/config/environment identifiers; file dates differ. | Recomputed component metrics are traceable to files but not to an exact generating runtime. | Record source revision, model hashes, environment, seeds, ordered UID list and generation timestamp. |
| MEDIUM | Development data used for selection/calibration | [Verified] FT epoch, legacy LR C, temperature and review threshold are selected using dev. | Dev accuracy and selective performance are optimistic; selection uncertainty is not removed by a saved point estimate. | Keep labels “dev, optimistic”; use an independent question-grouped confirmation set. |
| MEDIUM | Legacy final stacker is in-sample on dev | [Verified source] Notebook cell 52 fits final combiner_v1 on all dev after grouped OOF evaluation. | Its final fitted dev predictions are not an independent estimate. This is not the deployed pooled component path. | Keep legacy stacker claims separate; never call it deployed pooled LR. |
| MEDIUM | Feature cache scope includes the in-memory dataset table | [Verified source; historical execution Unverified] Notebook cells 40 and 43 build frozen encoder features over the table, with no label fitting in feature extraction. | May represent transductive text exposure; does not by itself prove supervised leakage. | Record precisely which splits are encoded in any future run and keep feature-generation provenance. |
| MEDIUM | Duplicate training/dev contamination is unresolved | [Unverified] Dev duplicate policy is documented; no verified training UID/content manifest is available. | Exact row UIDs alone would not rule out repeated content across partitions. | Compare normalized records using a verified train-only snapshot; retain source IDs. |
| MEDIUM | Pretraining data overlap and revisions are unknown | [Unverified] NLI/SBERT IDs are static strings; hub revisions and pretraining corpora are not recorded. | Benchmark exposure during external pretraining cannot be assessed here. | Pin model revisions and document known training corpora/limitations. |
| LOW | Report/document and live artifacts may differ | [Verified] Local manifests describe staged artifacts; live Drive synchronization was not independently checked here. | Local hashes do not prove cloud/runtime identity. | Compare hashes at the execution location before any future run. |

## Decision

[Verified] No confirmed leakage was identified in the inspected evidence.
[Unverified] This audit cannot establish zero train/dev overlap or full
prediction provenance. The overall result is PARTIAL PASS — SOME PROVENANCE
UNVERIFIED; Experiment 4 should wait for the high-risk provenance gaps to be
resolved.

