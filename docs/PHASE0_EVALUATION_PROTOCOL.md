# Project S — Independent Evaluation Protocol

**Status: Proposed protocol; no independent confirmation set is currently
verified.** Existing scores must be described as saved development results,
`dev, optimistic`. This document does not authorize experiments or a scorer
change.

## Existing evidence and limits

The saved development analysis reports 2,049 aligned rows in 177
`dataset|question_id` groups, with 27 questions in the development
unseen-question subset. The saved nested grouped-CV design uses development
data for model and checkpoint selection; it is not independent confirmation.
The current 0.64 threshold and temperature were selected/evaluated on dev.
Earlier test exposure is documented in project instructions/reports. No test
file or test output was opened for this protocol. A provenance audit did not
verify a training UID manifest or pooled-LR fit record, so it cannot prove
all development rows were excluded from all fitting.

**Decision:** `NEW CONFIRMATION SET REQUIRED`.

## Evaluation population and provenance

Collect new student-answer data for all four approved subject domains:
Science, Social Science, Mathematics, and English. Record source, grade,
question author, answer collection process, consent/permissions as applicable,
collection date, and schema/version. Use only questions for which qualified
reviewers have approved the question, reference answers, variants, concepts,
misconceptions, contradictions, and partial-credit criteria. Preserve stable
UIDs and immutable original labels with label-version history.

Do not synthesize examples and call them independent real-world confirmation.
The confirmation data must not be used for training, checkpoint selection,
hyperparameter selection, rubric edits, calibration, threshold selection, or
error-driven rule changes.

## Splits and question grouping

1. Assign whole question IDs to train, development, or confirmation before
   answer-level expansion; no question may cross partitions.
2. Keep the confirmation partition under a custodian, with labels and answers
   inaccessible to model authors until the final frozen evaluation.
3. Define **cold-question** results on confirmation question IDs absent from
   all model fitting and selection. Define **warm-question** results only if
   such questions are explicitly held out at answer level while question text
   exposure is documented; report separately.
4. Report dataset and subject strata, label counts, unique question counts,
   and exclusions. Pre-register the split manifest/hash without exposing
   confirmation labels.
5. Use grouped/nested cross-validation on train+dev only for development
   decisions. Existing dev nested CV is exploratory/development evidence, not
   the final confirmation result.

The confirmation sample size and group counts must be determined in advance
by a documented precision/power analysis using a predeclared effect and
confidence-width target; do not choose them after inspecting confirmation
outcomes.

## Model-selection and lock procedure

- Train and choose checkpoints using train and grouped development folds
  only; record UID/group manifests, seed, code revision, scorer/config hashes,
  data hashes, package versions, model IDs and immutable revisions.
- Select calibration and selective-prediction thresholds only on development
  folds. Freeze scorer, threshold, rubric, data pipeline, and analysis code
  before opening confirmation labels.
- Record an experiment ID, parent baseline hash, all decisions, exclusions,
  and artifact manifest. Never overwrite a prior run.
- The independent evaluator verifies the lock manifest, then runs the
  predeclared analysis once. Any post-unlock change makes that confirmation
  exploratory and requires a new independent set for confirmation.

## Metrics and uncertainty

Report N, number of question groups, label distribution, and missingness with
each result. Primary metric: **Macro-F1 on the approved three-class
Correct/Partial/Incorrect mapping**, with accuracy reported alongside it.
Secondary metrics: per-class precision/recall/F1, weighted F1, QWK for the
ordered three-class labels, confusion matrix, and per-subject/per-dataset
results. Report five-class metrics separately if used; do not mix label spaces.

Report calibration with ECE and Brier score using a calibration procedure
frozen on development only. Report selective accuracy versus coverage,
including the approved 0.64 baseline threshold and any development-selected
alternatives as separate frozen policies. Report cold-question and warm-
question results separately. Include paired question-group bootstrap
confidence intervals for model differences; predeclare resample count and
seed and preserve the resampling unit as question, not answer row.

## Acceptance criteria (must be approved before collection/unlock)

The existing policy states a target of 85% accuracy at 30% coverage and that
it was not met. Treat that as a reported project target, not a demonstrated
capability. Before collection, Jigar and reviewers must approve whether it
remains the primary operational gate and specify the interval rule, minimum
per-subject sample/group counts, acceptable class-wise floors, and calibration
limits. Do not invent those thresholds after seeing confirmation data.

For an improvement claim, require the predeclared primary metric to improve
against the frozen baseline on the same confirmation UIDs, with a paired
question-group interval and no material predeclared harm in cold-question or
per-subject results. Any rule or model selected using current dev remains a
candidate until this test. No accuracy gain is assumed.

## Required report

Publish the locked manifest identifier, hashes, provenance, split/group
counts, reviewer approval status, model/config hashes, seeds, package/model
revisions, all metrics and intervals, coverage and calibration results,
per-subject and cold/warm results, failures/exclusions, and any deviation from
the preregistered protocol. Preserve results even if they fail acceptance.
