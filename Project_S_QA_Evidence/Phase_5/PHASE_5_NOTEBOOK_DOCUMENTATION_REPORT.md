# Phase 5 Notebook Documentation Report

## Status
Notebook Markdown documentation is updated and structurally validated. No notebook cells were run. This report distinguishes inspected local artifacts from user-reported evidence.

## Sources inspected
- Project rules and context: `AGENTS.md`, `PROJECT_CONTEXT.md`.
- Working notebook: `notebooks/Jigar_Q&A_Branch_Baseline_COPY.ipynb`.
- Runtime scorer/reference: `project_s_qa/reports_v2/A_predict.py`, `A_demo_reference_outputs_v2.json`.
- Runtime staging manifest and model files under `project_s_qa/interim/`.
- Archived evaluation and deployment files in `project_s_qa/A_submission_v2/reports_v2/`.
- Phase 3 test report and Phase 4 freeze evidence.
- No pinned `requirements.txt` was found. The path in the request `project_s_qa/notebooks/...` is absent; the authorized working copy is the root `notebooks/` path above.

## Notebook map
- Cells 2-33, Phases 1-3: source data, labels, question/rubric setup, train/dev/test splits and leakage checks.
- Cells 34-55: baselines, NLI features, the dev-only LLM side experiment, DistilRoBERTa, stacking and review policy.
- Cells 56-82: frozen test evaluation, later experiments and artifact audits. These are historical producers; do not rerun indiscriminately.
- Cells 83-112: final inference, pooled scorer selection, calibration/review policy, bootstrap intervals, seed summaries and exploratory test.
- Cells 113-135: reference outputs, Block 45 parity, demo cases, Gradio interface, result tables and figures.
- Cells 136-163: concept/control diagnostics, grouped-CV deferral study, closure package and Blocks 59-62 diagnostics.
- Cells 164-166: limitations and saved-file panel summary.

## Markdown documentation added
- Cell 12 / Block 4: assessment objective, datasets, five labels, official and ordinal 3-class mappings, and separation of draft CBSE demo inputs from evaluation data.
- Cell 26 / Group 4: normalization, seed, question-level `dev_uq`, answer-group `dev_ua`, preserved official test splits, leakage controls and their limits.
- Cell 48 / Group 7: roles of DistilRoBERTa, SBERT-LR and NLI-LR; feature types; five-class probability averaging; distinction between deployed pooled LR assets and the earlier combiner experiment.
- Cell 84 / Group 11: inference inputs/outputs, ordinal score, confidence interpretation, final 0.64 review threshold, and provisional-policy caveat.
- Cell 106 / Group 14: dev, grouped-CV and exploratory-test contexts, question-level bootstrap and the seen/unseen gap.
- Cell 114 / Group 15: 15-case reference comparison and why parity is implementation consistency, not accuracy or generalization.
- Cell 164 / Limitations: exact project metrics, the unmet target, test status, domain/pilot limits, separate Block 51/61 negation evidence, unrelated-answer issue and execution provenance.

## Pipeline and inference summary
The pipeline maps answer text into five labels, trains three component scorers, and selects a pooled deployment. In `A_predict.py`, the pooled mode obtains five-class probabilities from the fine-tuned DistilRoBERTa, SBERT-LR and NLI-LR components, averages them, maps to incorrect/partial/correct, applies the saved temperature and then the saved review policy. The final output includes label, score, confidence, NLI evidence and teacher-review reasons. No hosted LLM or external inference API is part of this deployed path.

The reference JSON records `scorer_mode=pooled`; its stored A_predict hash matches the locally inspected scorer. The archived final policy sets confidence threshold 0.64 and disables the separate NLI contradiction flag. If the policy is missing, A_predict can use a provisional fallback; that is not equivalent to the saved final configuration.

## Evaluation sources and context
- Development values come from the archived `A_deployed_metrics_ci_v2.csv` and are labelled dev, optimistic.
- Grouped-CV policy estimates are not a held-out test result.
- Test values come from `A_test_results_v2.csv`; the archive labels these `EXPLORATORY (test seen in v1)`.
- Block 45 parity output reports 15/15 within 0.001. It supports implementation consistency only.
- Block 61's 12/12 component statement is user-reported; the local cell has no saved output. It is not merged with Block 51's 3/12 exact-control result.

## Reproducibility and change validation
- The Phase 4 archived run manifest records an environment snapshot; it is not a lockfile and does not establish current package versions.
- Notebook SHA-256 before edit / verified backup: `a35efc489c25806f2ad3db8684006dc2d627634dc1e6d2a61d3fbc75c615030e`.
- Notebook SHA-256 after edit: `5eb5dc4fd1ad85dce55c9b1222603fc11de19d51bb682103fc7923bc78b5faf0`.
- Cell count remains 167. Only Markdown source changed in cells 12, 26, 48, 84, 106, 114 and 164.
- All code cells, other cell sources, outputs, execution counts, cell metadata, notebook metadata and cell order matched the backup structurally. JSON parses successfully.
- No code, outputs, counts, model artifacts or evaluation files were changed. No cell was run.

## Remaining gaps
A separate executed notebook and trustworthy execution counts are unavailable. Blocks 59-62 lack saved local outputs; their reported completion is not independently verified. The local files do not establish Drive synchronization. Package versions outside the archived run manifest remain unspecified.
