# Project S — Revised Phase 0 Closure and Phase 1 Entry Criteria

**Status: Proposed for Jigar's decision.** This narrows the original gate so
non-scoring foundation work is not blocked by external execution tasks, while
retaining strict barriers before scoring, claims, and pilot use. It does not
authorize implementation.

## Why revise the six-gate rule?

The original rule requires an authoritative notebook, approved JSON/policy,
live Colab verification, canonical reviewed bank, qualified four-subject
review, and independent confirmation set before Phase 1. These are all
important, but not all are prerequisites for a non-scoring schema, ingestion,
or interface design task.

The risk is that a broad deferral could be used to run the scorer, tune on
development data, or present draft content as valid before safeguards exist.
Replace the single gate with explicit activity-specific gates. The baseline
must remain frozen and identified; any runtime use must pass live preflight;
any rubric scoring/pilot requires reviewed content; any confirmatory accuracy
claim requires new independent data. No test split can be relabeled clean.

## Revised staged closure definition

### Phase 0 — Foundation and Design Readiness

Close only when all items below are approved/documented:

1. **Frozen baseline boundary:** record local scorer hash and protected files;
   identify known provenance/config risks; no scorer/notebook/data/model edit
   is allowed by this gate.
2. **Scope approval:** Jigar approves a non-scoring Phase 1 scope, isolated
   output location, no-overwrite approach, and explicit prohibited activities.
3. **Design choices:** approve schema goals, status lifecycle, provenance
   fields, and review roles. Do not declare a question source canonical solely
   because it passes JSON/schema validation.
4. **Evaluation protocol:** approve split/grouping, selection/confirmation
   separation, metrics, uncertainty, and the acceptance decision process
   before any accuracy experiment.
5. **Phase 1 entry criteria:** state which tasks are infrastructure-only and
   which are scorer/assessment tasks; identify their separate gates.

Current status: **NOT CLOSED** because Jigar has not approved this revised
scope, the baseline notebook has not been selected, and the design/acceptance
decisions remain open.

### Phase 0.2 — External Runtime Verification

Required before any Colab notebook execution, model loading, inference, demo
scoring, or runtime integration:

- Select a notebook file and exact SHA-256; review any source delta.
- Select one runtime root and ensure notebook import root and
  `PROJECT_S_ROOT` agree.
- Approve exact scorer, reference JSON, and policy hashes and paths.
- Verify JSON scorer/policy hash fields against actual bytes; require the
  policy file at the path A_predict reads so no fallback occurs.
- Verify local model/joblib/data filenames and hashes; record installed
  package versions and Hub cache snapshot IDs/revisions without assuming a
  model ID pins a revision.
- Run the manual read-only Colab preflight and archive its output.

Until this passes, block all scorer/model/runtime execution. A local dated
snapshot is not a live Drive verification.

### Phase 1 — Safe foundation implementation (only after approval)

Allowed under revised scope only if Jigar approves:

- Versioned question-bank/rubric schema, structural validators, ingestion
  metadata and audit trail in a separate experimental area.
- Non-scoring interface prototypes using clearly marked draft content.
- Isolated unit/schema tests on synthetic schema fixtures or reviewed
  non-test fixtures; never overwrite frozen artifacts.
- No change to deployed `A_predict.py`, notebook scoring path, policy,
  threshold, model weights, labels, or saved baseline outputs.

This track cannot emit student scores or claim educational validity. If work
requires importing the frozen scorer or loading runtime artifacts, Phase 0.2
must pass first.

## Readiness gates by activity

| Gate/activity | Required before | Minimum acceptance |
|---|---|---|
| Notebook/source identity | Any notebook run or edit | Jigar approves path/hash; source changes are reviewed; never Run All. |
| Runtime root/config | Scorer import, model load, inference, demo scoring | Live preflight passes file/hash/root checks; missing or mismatched config fails closed operationally. |
| Question-bank schema | Generic schema/ingestion design | Jigar approves stable ID, versioning, provenance, status and field contract. |
| Canonical bank | Rubric scoring or approved assessment content | One source is selected; mapping/provenance reconciled; no automatic merge. |
| Expert review | Content-specific scoring claims or pilot | Qualified subject reviewers sign off; disputes adjudicated; versions recorded. |
| Data/model provenance | Candidate training or accuracy experiment | Data lineage, UID splits, artifact hashes, fit provenance, seeds and environment recorded. |
| Dev-only exploratory analysis | Any such analysis | Separate approval; question-grouped development only; all results labeled exploratory/dev optimistic; no promotion claim. |
| Independent confirmation | Confirmatory accuracy claim or promotion | New question-disjoint set, reviewed labels, provenance, custodian lock, preregistered analysis; test rows previously exposed are excluded. |
| Pilot | Any use to assess children/students | Approved content, reviewed scoring criteria, runtime integrity, human escalation, permissions/consent review as applicable, pilot-specific safeguards. No legal conclusion is made here. |

## Experimental readiness criteria

Before an accuracy experiment, require:

1. Jigar approves the experiment and immutable baseline; preserve the frozen
   v2 result as the comparator.
2. Verify UID-level train/dev membership and source provenance. If artifact
   fit provenance cannot be proven, report that limitation and restrict the
   claim; do not assert leakage is absent.
3. Group by question before all split, resampling, or cross-validation. Keep
   all answers for a question in the same fold.
4. Use development folds for all architecture, checkpoint, calibration, and
   threshold selection. Do not open the final confirmation set during these
   choices.
5. Freeze code, data manifest, model/config hashes, package versions, model
   revisions, threshold, metrics and analysis before confirmation unlock.
6. Predeclare primary/secondary metrics and acceptance thresholds, including
   the treatment of Partial class, per-subject harm, calibration and
   coverage. The reported 85% at 30% coverage target is not met and must not
   be promised.
7. Report group-aware uncertainty, per-class metrics, per-subject and
   cold-question performance, calibration and selective behavior. Candidate
   improvements on dev remain hypotheses.

## Pilot readiness criteria

Before a pilot that may influence a student's evaluation:

- Subject/grade-relevant questions and rubrics have documented qualified
  review and source provenance.
- Accepted variants, partial-credit criteria, contradictions, ambiguity
  handling, and teacher-review behavior are adjudicated and versioned.
- The runtime and scorer/config are pinned and live-verified; errors have a
  clear human fallback.
- A separate pilot plan defines consent/permission, data protection, who sees
  results, and how teacher decisions override the tool. These items require
  context-specific review; no legal advice is asserted.
- Pilot outcomes are described as feasibility/usability evidence unless the
  evaluation protocol supports a valid performance claim.

## Explicit no-go conditions

Do not execute or claim a result if any of these apply:

- Notebook or runtime root is unselected, or imports may reach a different
  scorer than the approved hash.
- JSON/policy mismatch, policy missing, or fallback is possible at the active
  runtime path.
- Model/revision/runtime identity cannot be recorded for a reproducibility
  claim.
- Draft or structurally validated content is presented as expert-approved.
- Dev-seen or historically exposed test data is described as independent
  confirmation.
- An experiment changes the frozen scorer, threshold, model, labels, or
  artifacts without separate approval and a new versioned baseline.
- A candidate is promoted because of an accuracy point estimate without the
  predeclared grouped uncertainty and subject/class safety checks.

## Decision and status

**Recommended policy:** adopt this staged definition. Jigar must approve it
before Phase 1. Under it, isolated non-scoring infrastructure can start after
scope/baseline safeguards are approved; scorer/runtime work remains blocked
until Phase 0.2; rubric-based or student assessment remains blocked until
content review; confirmatory accuracy claims remain blocked until independent
confirmation data and protocol are ready. At the time of this review, no such
approval or work has been started.
