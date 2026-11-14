# Phase 8 closure package

All measured values below are **dev-only, optimistic**. This is static
preparation; no model, notebook, or Project S script was run.

## Status

| Stage / item | State | Evidence / remaining condition |
|---|---|---|
| Stage 0 E1 aggregation and risk/coverage | DONE, dev-only | `E1_AGGREGATION_AND_RISK_COVERAGE.md`; two decision paths and review rule are documented. |
| Stage 0 E2 component inventory | DONE for current dev export | `A_component_probs_v7.parquet`; export validation and component analysis in `EXPORT_VALIDATION_AND_NLI_RESULTS_v2.md`. No OOF component probabilities yet. |
| Stage 0 E3 high-confidence errors and data quality | DONE, dev-only | `E3_HIGH_CONFIDENCE_ERROR_BREAKDOWN_v2.md`; near-duplicate label conflicts are heuristic findings, not adjudicated errors. |
| Stage 0 E4 experiment specification | DONE as draft | `E4_DEBERTA_EXPERIMENT_SPECIFICATION_v2.md`; see nested design and gate drafts here. |
| Phase 3 demo evidence prerequisite | PARTIAL | Phase 2 status records launch-only Block 60 evidence; screenshots/video and aggregate voice evidence remain absent. Stage 1 stays blocked until Phase 3 is complete. |
| Stage 1 DeBERTa nested CV | PREPARED / BLOCKED | `x1_deberta_train_v2.py`; no train-only derived text file found. Dev-only fold CV is designed, but execution requires Phase 3 completion and explicit `approved Stage 1`. |
| Stage 2 OOF stacking | FUTURE WORK / UNAPPROVED | No stacking run or fitted combiner is authorized here; needs separate approval and valid OOF component predictions. |
| Stage 3 calibration / selective prediction | FUTURE WORK / UNAPPROVED | No calibration run; keep deployed 0.64 threshold unchanged. Needs separate approval. |
| Locked evaluation and freeze | BLOCKED | Existing test exposure means there is no clean locked-test claim. The official unseen-domain set was not opened; clean access history is Unverified. |
| Human review of the 40-row sample | PENDING JIGAR | `E1_review_sample.csv`; reviewer fields were blank in the existing report. Jigar's 30-45 minute estimate is Reported, not measured. |

## Stage 0 findings (six lines)

- **Tested, dev-only:** Path A accuracy = 1,155 / 2,049.
- **Tested, dev-only:** Path B accuracy = 1,189 / 2,049 (+1.66 points); paired 95% CI for the difference is [-0.0061, 0.0394], includes zero; candidate only.
- **Tested, dev-only:** the two paths predict different classes on 336 rows.
- **Tested, dev-only:** Macro-F1 gain CI is +0.8 to +5.4 points; Partial recall changes from 26.3% to 38.5% (gain CI +8.5 to +16.9 points).
- **Tested, dev-only:** 156 Path A high-confidence errors include 131 same-wrong-class component consensus rows.
- **Tested, dev-only:** the >=0.95 contradiction-review rule was rejected; it adds 118 reviews for one additional high-confidence wrong prediction caught, and is not independent confirmation.

## Limitations

- No clean locked test is available; existing test results are exploratory only.
- All current performance claims above use dev rows and are optimistic.
- E3's heuristic found 41 conflicting-label near-duplicate pairs; this is not
  human adjudication and does not establish which label is correct.
- No current Stage 1, Stage 2, or Stage 3 model result exists in this package.
- No train-only text file was found, so the official train split is unavailable
  to the proposed scripts without a separately approved derived file.
- The 4,562-row official unseen-domain set was not opened; access history is
  Unverified and it cannot be called a clean holdout yet.

## Four short panel answers

1. **Why is unseen-question performance weaker?** The dev-only QWK and
   accuracy are lower on `dev_uq`; new questions change the wording and
   examples the scorer sees. The current scores do not establish the cause.
2. **Why no CBSE accuracy claim?** The demo question bank is draft material;
   there is no reviewed CBSE/student validation set with independent labels.
3. **Why trust the review flag?** It is a conservative aid, not a guarantee:
   dev evidence shows errors can remain above 0.64, so a teacher must verify
   flagged and unflagged answers in real use.
4. **What is the improvement claim?** Path B improves some dev metrics but
   its accuracy interval includes zero; it is unvalidated and not deployed.
   DeBERTa gain is unknown until an approved three-seed run passes every gate.

## Paste-ready Notion update for roadmap section 8.4

> **Status:** Stage 1 remains future work and requires Phase 3 completion plus
> Jigar's explicit `approved Stage 1`. Nested question-grouped CV is the
> adopted protocol. Use exploratory seed 42 and final seeds 42, 123, 2026;
> scripts accept `--seed`. The proposed DeBERTa uses LR 2e-5, 3 epochs,
> warmup 0.10, max length 256, per-device batch 4 x accumulation 4, fp16,
> and validation Macro-F1 selection. Require three-seed mean Macro-F1 gain
> >=0.01 with paired question-group bootstrap 95% CI lower bound >0; overall
> accuracy and QWK above frozen baseline; unseen-question QWK no more than
> 0.01 below baseline (Proposed); Partial recall and F1 both higher. The
> 12-case negation set is diagnostic only, not a gate. Report batch-1 and
> batch-32 median/p95 latency. Any failed gate falls back to frozen v2. These
> estimates remain dev-only, optimistic; no locked-test claim is available.

## Static script deltas

| Draft | Delta from original | Validation |
|---|---|---|
| `x1_deberta_train_v2.py` | Replaces the hard-coded unified-split/Drive paths with `--dev-text`, `--folds`, `--output-dir`, `--seed`, and `--fold`; selects epoch on inner grouped folds and predicts only the outer held-out dev fold; writes UID-keyed fold output and run metadata; records truncation and batch-1/32 latency. | Drafted only; AST parse passed. Checkpoint availability, T4 fit, and runtime behavior Unverified. |
| `x1_gate_check_v2.py` | Replaces one-seed/2,000-resample evaluation with three seeds, five OOF folds, identical-UID checks, 10,000 question-group bootstrap resamples, accuracy/Macro-F1/QWK/Partial precision-recall-F1, unseen QWK, diagnostic-only negation, and batch latency summaries. | Drafted only; AST parse passed. No result was computed by this script. |

The operational unseen-QWK gate uses the E4 v2 proposed 0.01 margin. The
dev-only baseline QWK bootstrap interval is 0.2097-0.3760 (2,000 question-
group resamples, seed 42; interval width 0.1663); 0.01 is less than half that
width and is the existing E4 proposal. It is still not independent
confirmation. No gate was loosened from the E4 v2 proposal.
