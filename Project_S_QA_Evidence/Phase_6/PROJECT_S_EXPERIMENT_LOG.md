# Project S Q&A Experiment Log

## Evidence labels
- **Verified local artifact/output:** inspected in the project or verified submission archive; execution provenance may still be limited where execution counts are null.
- **User-reported:** supplied by Jigar in ChatGPT, not independently reproduced.
- **Exploratory:** test data had been seen in v1; do not present as an untouched final test.
- **Not verified:** no local output or source establishes the claim or its execution provenance.

## Data and evaluation protocol
Datasets: public English science answers from SciEntsBank and Beetle. Five-label target: correct, contradictory, partially correct/incomplete, irrelevant, non-domain. QWK uses the separate three-level ordinal mapping. `dev_ua` holds answer groups for seen questions; `dev_uq` holds out whole training questions. Model selection uses development data. Grouped-CV results estimate a policy and are not test results. Question-level bootstrap intervals appear in the archived evaluation files.

## Experiment chronology
| Stage | Experiment | Evidence and status |
| --- | --- | --- |
| Blocks 13-15 | Majority, TF-IDF and SBERT baselines | Historical notebook experiment; frozen results are inputs to later comparisons. Do not rerun producer cells as part of documentation. |
| Blocks 16-18 | NLI features/classifier and a dev-only LLM side experiment | NLI evidence enters the learned component. Block 17 is not part of deployed inference; no hosted LLM/API is used by the deployed scorer. |
| Blocks 19-21 | Fine-tuned DistilRoBERTa, stack/combiner experiment, review rule | Saved artifacts; training is not part of the deployed runtime task. |
| Blocks 25-28 | Further ensemble/model selection work | Dev selection led to the current pooled scorer. RoBERTa-base weights were not saved; its saved-probability comparison cannot be regenerated from weights. |
| Blocks 32-40 | Inference contract, comparisons, calibration and policy | Archived `A_predict.py`, deployed-scorer record and final policy document the selected pooled mode. Final confidence threshold is 0.64; separate NLI contradiction flag is disabled. |
| Blocks 41-43 | Paired question-level bootstrap and exploratory test | Archived outputs provide dev intervals and test tables. Test results are exploratory because the test sets were seen in v1. |
| Block 45 | Reference-output parity | Saved cell 118 and user report: 15/15, predictions/review flags match, confidence differences within 0.001. This is software parity, not accuracy. Local execution_count is null. |
| Block 51 | Negation/paraphrase/spelling controls | Notebook limitation records exact negation result 3/12 and all 12 flagged for review. This is a small control set, not held-out validation. |
| Block 54 | Learned deferral vs fixed threshold | Study-only grouped-CV estimate: 74.77% accuracy at 31.33% coverage. Not deployed. |
| Block 58 | Closure and submission package | Saved cell 155 displays archived metrics, reports Block 45 parity PASS, and says 54 files packaged. ZIP contains 55 entries because the 54-file payload manifest is itself included. CRC and extracted-file hashes pass. Cell execution_count is null. |
| Blocks 59-62 | Timing, demo and diagnostics | Jigar reported runs; local cells 157, 159, 161 and 163 have no saved outputs. Latencies and Block 61 component results remain user-reported, not independently verified in this local notebook. |

## Development metrics
Source: archived `A_deployed_metrics_ci_v2.csv`. These are dev, optimistic.

| Split/group | Metric | Value (95% CI) |
| --- | --- | --- |
| All dev | QWK, 3-level | 0.432 (0.358-0.509) |
| All dev | Macro-F1, 5-class | 0.579 (0.523-0.629) |
| Seen answers (`dev_ua`) | QWK | 0.630 (0.562-0.692) |
| Seen answers (`dev_ua`) | Macro-F1, 5-class | 0.730 (0.689-0.766) |
| Unseen questions (`dev_uq`, 27 questions) | QWK | 0.317 (0.199-0.412) |
| Unseen questions (`dev_uq`) | Macro-F1, 5-class | 0.490 (0.406-0.544) |

## Review threshold and grouped CV
The final policy uses confidence threshold 0.64. Archived policy records dev auto-scored accuracy 0.7512 at coverage 0.306. Grouped-CV policy estimate is 74.77% accuracy at 31.33% coverage. The required 85% accuracy at 30% coverage target was **not met**.

## Exploratory test results
Source: `A_test_results_v2.csv`; every row is labelled `EXPLORATORY (test seen in v1)`.

- All test: QWK 0.454 (95% CI 0.392-0.515).
- All test: five-class macro-F1 0.576 (95% CI 0.543-0.606).
- All test: three-way accuracy 0.588; coverage 0.288; auto-scored accuracy 0.790 (95% CI 0.747-0.834).

Do not describe these as a fresh untouched test estimate.

## Negation, contradiction and unrelated-answer evidence
- **Block 51 notebook record:** exact negation 3/12; all 12 sent for teacher review.
- **Block 61 user report:** fine-tuned component predicted correct on 12/12 and NLI predicted contradictory with probabilities around 0.507. No local Block 61 output is saved. Keep this as a separate user-reported diagnostic; do not combine it with Block 51 or treat it as validation.
- **Saved NLI evidence:** entailment 0.87-0.96 on three of four unrelated examples. This indicates NLI evidence can fail to distinguish unrelated responses; the evidence panel should not be presented as a reliable explanation.

## Demo, runtime and integrity
Block 45 parity is reported as PASS on 15 reference cases with matching labels/review flags and confidence tolerance 0.001. The Phase 4 ZIP and extracted folder match by path, size and SHA-256; its internal manifest lists 54 payloads and excludes itself. A_predict's SHA matches the reference JSON's stored hash and scorer mode is pooled. The notebook has saved output text for some cells, but null execution counts mean the exact execution session is not authenticated. Drive synchronization is not verified.

## Performance limitations and next research
The unseen-question QWK of 0.317 is weaker than seen-answer QWK of 0.630. Negation and contradiction behavior needs carefully separated, held-out diagnostics. Unrelated-answer evidence is weak. No pilot student-answer validation and no validated CBSE/Indian schoolchildren evaluation are available. Future work may improve generalization, calibration, control behavior, and teacher-reviewed evaluation, but no model change or gain is claimed here.
