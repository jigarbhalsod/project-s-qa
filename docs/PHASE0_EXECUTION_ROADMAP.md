# Project S — Phase 0 Closure and Phase 1 Roadmap

**Status:** proposed, dependency-aware plan. No task below is authorization to
execute code or change files. Time labels are relative planning categories;
actual duration is **Unverified**.

## Dependency-aware tasks

| ID | Task | Owner | Prerequisite | Deliverable | Acceptance criteria | Phase | Blocking | Approval |
|---|---|---|---|---|---|---|---|---|
| R0-1 | Decide whether to adopt staged Phase 0 closure; approve protected baseline boundary and non-scoring Phase 1 scope | Jigar | Review this brief and decision register | Approved scope note | Scope says what may proceed; explicitly bars scorer/runtime/assessment claims until gates pass | Phase 0 | Blocks all Phase 1 work until decided | Yes |
| R0-2 | Select baseline notebook path/hash or designate none; identify the scorer hash and exact source delta | Jigar + Systems Architect | R0-1 | Notebook/baseline decision record | One exact notebook SHA and scorer SHA are named; source differences reviewed; no content merge | Phase 0 | Blocks notebook execution and integration | Yes |
| R0-3 | Choose runtime root and configuration option A/B/C; authorize staging only in a separate action | Jigar | R0-2 | Approved runtime manifest | One root; matching scorer, reference JSON, policy hashes; no missing-policy fallback; no unapproved overwrite | Phase 0 | Blocks scorer execution | Yes |
| R0-4 | Run read-only preflight in authorized live Colab after manifest approval | Jigar | R0-3 | Preflight output and environment record | Actual root, notebook/scorer/config/artifact hashes, package versions and model cache metadata recorded; every critical check passes | Phase 0.2 | Blocks any runtime scoring | Yes, user runs |
| R0-5 | Approve canonical schema and choose a question-bank starting point | Jigar + Assessment Architect | R0-1 | Schema/source decision | Stable IDs, subject/grade, provenance, version/status lifecycle agreed; package and prototype not merged by text alone | Phase 0 design | Blocks canonical content migration, not schema prototype | Yes |
| R1-1 | Build isolated schema/ingestion/validation design (non-scoring only) | Codex/engineer | R0-1, R0-5 | Versioned schema and structural validation plan | Separate output area; no frozen artifact writes; fixtures test schema shape only; no educational approval implied | Phase 1 | Does not block unrelated runtime identity work | Yes, scope approval |
| R0-6 | Nominate qualified reviewers for Science, Social Science, Mathematics, English and adjudication | Jigar | R0-5 | Reviewer assignment register | Names, relevant qualifications/evidence, independence/conflict check, availability and assigned domains recorded | Phase 0/Phase 1 | Blocks approval of content | Yes, external people |
| R1-2 | Review/migrate candidate content with provenance and independent review | Subject reviewers + content owner | R0-5, R0-6, R1-1 | Versioned reviewed bank/rubric bundle | Each item has source, status, author/reviewer/date/version; disputed items adjudicated; no silent merge | Phase 1 | Blocks rubric-based scoring and four-subject claims | Reviewers approve; Jigar accepts source |
| R0-7 | Approve evaluation protocol and predeclare decision rules | Jigar + Evaluation Scientist | R0-1 | Frozen protocol | Question grouping, primary/secondary metrics, CI, calibration/selective procedure, per-subject floors and target decision rule defined before experiments | Phase 0 design | Blocks accuracy experiments from being confirmatory | Yes |
| R1-3 | Verify data/artifact provenance and train/dev group separation | Evaluation Scientist + data owner | R0-2, R0-7 | UID/group and artifact provenance manifest | Exact fit inputs/checkpoints and code/config versions linked; unresolved provenance explicitly limits claims | Phase 1 / before experiments | Blocks training/promotion claims | Yes |
| R1-4 | Run separately approved exploratory dev experiments, if useful | Jigar/Evaluation Scientist | R0-7, R1-3, applicable runtime gate | Versioned dev-only report | Dev-only label; question-grouped analysis; no test access; no candidate promotion or accuracy claim | Phase 1 experimental | Does not establish confirmation | Yes, separate task approval |
| R0-8 | Design and collect a new independent question-disjoint confirmation set | Jigar + data custodian + subject reviewers | R0-5, R0-6, R0-7 | Locked confirmation manifest, provenance and reviewed labels | Whole questions separated; labels held by custodian; sample size/purpose predeclared; not used for fitting/selection/calibration | Before confirmatory accuracy stage | Blocks confirmatory claims | Yes, data/custody approval |
| R1-5 | Freeze candidate and conduct final one-time confirmation evaluation | Independent evaluator | R0-3, R0-4, R0-7, R1-2 where relevant, R1-3, R0-8 | Final evaluation report | Frozen model/code/config/threshold/analysis; independent set unsealed only after lock; complete metrics/CI/per-subject/cold-warm record | Later accuracy phase | Blocks model promotion | Yes, release/unlock approval |
| P-1 | Prepare any student-facing pilot and safeguards | Jigar + school/ethics/data owner + subject reviewers | R0-4, R1-2, R1-5 as applicable | Pilot protocol and reviewed materials | Human oversight, reviewed content, data permissions and context-specific safeguards documented; no unsupported accuracy/validation claim | Pilot phase | Blocks student use | Yes, external approval as applicable |

## Priority rationale

1. **Highest risk, shortest decision path:** R0-1 through R0-3 settle who/what
   may be run and prevent config drift. These are decisions, not coding.
2. **Runtime-dependent:** R0-4 is user-run and must precede any Colab inference.
   It can happen independently once choices are approved, not before.
3. **Parallel design path:** R0-5/R0-6/R0-7 can proceed while live runtime is
   being arranged. Schema/protocol design does not require model execution.
4. **Implementation only after scope:** R1-1 is isolated non-scoring work.
   R1-2 requires actual experts and should not be simulated by structural
   validation.
5. **Longest dependency:** R0-8 needs new data collection, provenance, and
   review. It can be planned early but must be complete before confirmation.
6. **Deferred model claims:** R1-3/R1-4/R1-5 require their data/config gates;
   exploratory dev work remains labeled exploratory and cannot substitute for
   the locked set.

**Time:** effort/duration is Unverified; no dates or person availability were
provided. R0-8 is expected to be the most external-dependency-heavy item, but
that is a planning inference rather than a measured estimate.

## Proposed Phase 1 entry checklist

Phase 1 may begin only as isolated, non-scoring infrastructure after Jigar
approves R0-1, R0-5 and the baseline/no-overwrite boundary in R0-2. Any task
that imports `A_predict`, loads models, runs a notebook, scores answers, edits
runtime configuration, or compares model performance is out of that entry
permission and needs the corresponding R0-3/R0-4/R0-7/R1-3 approvals first.

No roadmap task was executed as part of this review.
