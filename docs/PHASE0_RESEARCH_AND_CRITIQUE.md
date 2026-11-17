# Project S — Phase 0 Research and Critical Review

**Status:** static internal review; no implementation or external literature
review was performed. **Phase 0 is not closed.** This document does not
authorize Phase 1 or any scorer/runtime change.

## Evidence labels and limits

- **Verified:** current local source, schema, file metadata, hash, or saved
  report was inspected in the stated scope.
- **Reported:** an earlier project report describes the finding; it was not
  newly measured here.
- **Inference:** consequence reasoned from verified source or reported data.
- **Proposed:** recommendation, not a project decision.
- **Unverified/Blocked:** evidence or access is missing.

Read `AGENTS.md`, `PROJECT_CONTEXT.md`, the prior audit and Phase 0 documents,
current scorer source, handover validator/schema, and non-test evaluation and
provenance reports. Notebook sources/metadata were previously fingerprinted;
no notebook output was inspected in this review. No test file, split, output,
ZIP, or PDF was opened. No code, notebook, model, or inference was executed.
`PROJECT_CONTEXT.md` describes a Nov 3, 165-cell state; later static reports
record 167- and 169-cell candidates. The context is stale and cannot select a
current notebook.

### External research status

`AGENTS.md` prohibits network calls. **External research is BLOCKED.** No
academic standard, professional guidance, paper, DOI, publication date, or
URL is cited here. The standards and literature findings requested in the
prompt remain outstanding; the recommendations below are internal technical
analysis, not claims of legal or standards compliance. Do not treat a
standards recommendation as law. An authorized follow-up research task should
verify the relevant educational-testing standards, constructed-response
rubric research, automated short-answer grading evaluations, calibration and
selective prediction methods, and grouped validation guidance using primary
sources with title, issuer/author, date, URL, applicability, and limitations.

## Executive findings

1. **Scorer behavior is reproducible only when source, root, policy, model
   files, and dependencies are bound together.** The scorer reads
   `PROJECT_S_ROOT` or a hard-coded default (`project_s_qa/reports_v2/A_predict.py:8–10`).
   The notebook inserts a hard-coded Drive `reports_v2` path. Those roots can
   diverge. The policy loader silently substitutes a provisional policy when
   the expected policy file is absent (`A_predict.py:139–141`); that fallback
   changes review behavior (`:16–17,162–165`). This is a critical runtime
   safety gap, but it does not prevent isolated schema design.
2. **The baseline is a frozen candidate, not a fully provenance-verified
   baseline.** The source hash is locally identifiable, but the notebook
   authority and exact artifact/run linkage are unresolved. The provenance
   report says no verified train UID manifest, pooled-LR fit record, or
   prediction-generation manifest was found
   (`Project_S_QA_Evidence/Experiment_3_Provenance_Audit/EXP3_PROVENANCE_AUDIT_REPORT_v1.md:7–11,61–75`).
   This is not proof of leakage; it prevents ruling it out.
3. **The scorer does not implement rubric-based correctness, explicit
   relevance, or concept-count partial credit.** The deployed decision is an
   equal average of component probabilities, a fixed class collapse, and an
   argmax (`A_predict.py:56–57,152–170`). The model can therefore accept
   semantically plausible but off-question text if its components do not
   detect the mismatch.
4. **Current bank assets are not educationally approved.** The 251-entry
   package is not four-subject ready; the 12-entry prototype is Science-only
   and draft status. Structural validation checks shape and relationships,
   not educational meaning (`PROJECT_S_QA_HANDOVER/src/validation/question_bank.py:1,14–55`).
5. **Saved performance evidence is development evidence.** The latest
   Experiment 1 report is dev-only and optimistic. On its 2,049-row primary
   population, Path B's grouped-bootstrap accuracy interval includes zero;
   the grouped Macro-F1 interval is above zero, but it is still a development
   comparison after prior selection. Do not turn it into an independent
   improvement claim (`Project_S_QA_Evidence/Experiment_1_Path_Comparison/EXP1_AGGREGATION_COMPARISON_REPORT_v2.md:43–60`).
   Earlier reports contain different estimates/configurations; cite the
   specific saved artifact and metric definition rather than combining them.
6. **A new question-disjoint, human-reviewed confirmation set is required
   before confirmatory accuracy claims.** The historical test exposure and
   unresolved fit provenance prevent calling an existing split clean
   confirmation. This does not prevent a non-scoring schema prototype.

## Evidence ledger

| Topic | Verified/reported evidence | Interpretation and limitation |
|---|---|---|
| Scorer inputs | FT receives question plus reference and student separately (`A_predict.py:61–75`); SBERT uses reference/student (`:92–101`); NLI uses student/reference-derived sentence pairs and a whole reference/student pair (`:43–45,78–89,110–129`). | Question context differs by component; no separate relevance function is visible. Source inspection cannot predict every error. |
| Aggregation | Three component probabilities are averaged equally and collapsed to three classes, with optional temperature scaling (`A_predict.py:13–15,56–57,152–170`). | Equal weights are a design choice, not evidence that component probabilities are comparable or calibrated. |
| Confidence/review | Confidence is maximum three-class probability; review reasons are threshold/contradiction rules (`A_predict.py:160–170`). | Confidence is not independently proven calibrated. The threshold is dev-derived per the provenance audit. Review flag does not change the predicted label. |
| Policy fallback | Missing policy silently returns `PROVISIONAL_POLICY` (`A_predict.py:16–17,139–141`); default contradiction flag is true (`:164`). | A root mismatch can change review decisions without changing model identity. Must block execution until exact policy path/hash is checked. |
| Rubric | No rubric or question-ID lookup in `A_predict.py`; separate Block 64 retrieves/displays a rubric but calls scorer without it (`PROJECT_S_QA_HANDOVER/src/block64_demo_bank.py:14–30`). | Stored rubric fields do not govern deployed scoring or Partial assignment. |
| Package bank | `project_s_qa/A_submission_v2/reports_v2/A_rubrics_v2.json`: 251 entries; 196 SciEntsBank, 52 Beetle, 3 demo; no subject/grade fields; current content counts: 248 `auto_draft`, 3 `demo`, 152 nonempty accepted variants, 113 nonempty misconceptions, 248 worked examples, zero `verified_by`. | Earlier report counts differ for variants/misconceptions (155/116); resolve file/version/hash drift before relying on those fields. Dataset name is not subject coverage. |
| Science prototype | Handover `question_bank/questions.json` has 12 Science items, grades 4/5/6 (4/6/2), all `draft_unreviewed`; reference answers/partial-credit criteria/provenance fields exist; accepted variants, concepts, misconceptions, and contradictions are empty in the question records. | Draft data; does not establish reviewed assessment content. Other subject coverage absent in inspected banks. |
| Structural validator | `PROJECT_S_QA_HANDOVER/src/validation/question_bank.py:1,14–55` checks fields, labels, IDs, status, rubric links, and provenance. | Structural pass is not semantic or educational validation. |
| Data leakage/provenance | EXP3 report: dev artifacts align; no verified training UID manifest or pooled-LR fit record; FT recipe selects epochs on dev; actual pooled artifact origin is unlinked (`EXP3_PROVENANCE_AUDIT_REPORT_v1.md:7–11,39–47,61–75`). | No confirmed leakage was found in reviewed source, but absence of leakage is not established. |
| Generalization/evaluation | `NESTED_CV_DESIGN.md` uses grouped development folds; it explicitly does not create independent confirmation. EXP1 reports question-grouped uncertainty on dev. | Cold-question dev is still selection data, not confirmation. No result here is recomputed. |
| Configuration | Current root JSON and packaged JSON/policy options are described in `PHASE0_1_RUNTIME_INTEGRITY_REPORT.md` and `PHASE0_FINAL_CLOSURE_REPORT.md`; live Drive is not inspected. | Hash consistency in a local snapshot does not prove which config Colab loads. |

## Agent 1 — Adversarial Evaluator

### Main question: what can mislead accuracy or assessment claims?

- **Verified source:** The deployed scorer uses equal probability averaging
  despite component input differences. The FT model alone sees the question;
  SBERT and NLI compare answer/reference text without the question
  (`A_predict.py:61–68,92–101,115–125`). A wrong or off-question answer may
  still look similar to the reference. No separate relevance gate is
  present.
- **Verified source:** `Partial` is a learned class after probability
  collapse; the scorer does not count satisfied rubric concepts or apply
  subject-specific partial-credit rules (`A_predict.py:56–57,110–136,153`).
- **Verified source:** `A_predict.py:139–141` silently falls back to a
  provisional policy. Missing policy means confidence threshold 0.60 and
  contradiction review default true, versus packaged policy metadata at 0.64
  and contradiction review disabled. Review changes teacher flag, not label.
- **Reported:** The 0.64 threshold and temperature were derived/evaluated on
  dev; `EXP3_PROVENANCE_AUDIT_REPORT_v1.md:67,84` labels selective estimates
  optimistic. Historical test exposure is recorded in `AGENTS.md` and Phase 8
  closure documents; any historical test result is exploratory.
- **Reported:** EXP1's Path B accuracy difference has a question-grouped
  interval that includes zero; grouped Macro-F1 interval excludes zero in
  that saved dev report. Neither is confirmatory because the rows were used
  for development selection. No new metric was computed here.
- **Inference:** A single accuracy value hides the important Partial and
  per-subject failure modes. Require per-class and grouped reporting, and
  do not present calibration/coverage as independent when tuned on the same
  dev population.

**Critical before Phase 1 scoring/runtime:** exact baseline, path/config
guard, experiment isolation, and no-overwrite manifest. **Can wait for later
scoring experiments:** improved relevance checks, rubric integration,
component reweighting, calibration changes, and new architecture. Those must
be tested only under a predeclared evaluation plan; do not modify the frozen
baseline as part of this closure.

## Agent 2 — Assessment Architect

### Bank comparison

The 251-record package reflects public-data rubric metadata and has no
subject/grade fields; 248 statuses are `auto_draft`, 3 are `demo`, and no
`verified_by` values exist. Earlier documentation's 155 accepted variants
and 116 misconceptions conflict with the present-file counts of 152 and 113.
The 12-question handover prototype is a different schema and only Science;
all 12 are `draft_unreviewed`. The prototype has reference answers and
partial-credit text but lacks populated concept/variant/misconception fields.
Do not merge or declare either canonical by count alone.

### Proposed reusable schema and review process

The handover schema is a useful structural starting point because it separates
question and rubric records and has IDs/links, but it should be versioned and
expanded or mapped to include: stable question ID, subject, grade, chapter,
topic, difficulty, question text, reference answer(s), accepted variants,
required/supporting concepts, misconceptions, contradictory claims,
partial-credit rules, source/provenance, reviewer identity/qualification,
review status, timestamp, version, and change rationale. Keep source records
immutable; define migration mapping instead of merging by text.

Subject-specific checks (all **Proposed**, not external-standard claims):

| Subject | Review evidence to capture |
|---|---|
| Science | Correct concepts, explanation/cause chain, known misconceptions, contradictory claims, concept completeness. |
| Social Science | Fact/source accuracy, chronology where relevant, location/time context, causal claims, supporting evidence. |
| Mathematics | Equivalent numeric/symbolic forms, units, rounding/tolerances, valid alternate methods, method credit when final answer is wrong. |
| English | Meaning-preserving paraphrase, contextual interpretation, valid vocabulary/grammar alternatives; grammar scored only if it is the objective. |

Partial credit should correspond to observable rubric evidence, not keyword
count alone. Distinguish a correct but incomplete response from a response
whose central claim is wrong or contradictory. Mark ambiguous questions/answers
for human adjudication. One schema can represent all subjects; subject-specific
rules must be explicit data/rubric fields and reviewed by subject specialists.

**Proposed workflow:** content author submits provenance/version; assigned
subject reviewer independently checks question and rubric; disagreements go
to a second reviewer/adjudicator; only documented human sign-off can mark
`approved`. Use `draft_unreviewed`, `in_review`, `revision_required`, `approved`,
`rejected`, with reviewer/date/version/rationale for every transition. No real
reviewer is nominated and no current item is approved.

**Phase classification:** schema and review process can be designed now;
expert review is mandatory before content is used as reviewed assessment or
rubric-based validity evidence; all four subjects must have reviewed content
before claiming four-subject readiness or running a four-subject assessment
evaluation.

## Agent 3 — Systems Architect

- **Verified source:** `A_predict.py:8–10` reads `PROJECT_S_ROOT` or uses
  `/content/drive/MyDrive/project_s_qa`; the notebook separately inserts a
  hard-coded Drive import path. Those can point to different roots.
- **Verified source:** `A_predict.py:11–12,21–35,104–107` loads hub NLI/SBERT,
  local FT assets, `combiner_v1.joblib` (even in pooled mode), and
  `pooled_lr_v2.joblib`. Hub revisions/package versions are not pinned in the
  local project lock; runtime availability is unverified.
- **Verified local evidence:** current root JSON, package JSON/policy, and
  exact-hash policy copy are documented in `PHASE0_FINAL_CLOSURE_REPORT.md`.
  Local hash matching is not live deployment verification.
- **Verified reports:** candidate notebook source/counts differ; executed
  cell 157 differs from D. No candidate is selected, and no notebook checks
  the JSON file's own SHA-256. Run metadata does not prove which runtime files
  were loaded.
- **Proposed architecture:** freeze the research notebook and scorer; after
  Jigar selects the baseline, provide a small separately approved runtime
  entrypoint with strict scorer/JSON/policy hashes, a single explicit root,
  dependency/revision reporting, and hard failure on missing/mismatched
  config. Keep a versioned question-bank service separate from frozen scoring
  until reviewed content and integration are approved. Do not implement here.

**Safest notebook strategy:** not an existing candidate until selected. A
separate runtime entrypoint minimizes research-notebook drift but requires a
Jigar-approved source/hash and explicit path. A clean notebook copy can be a
short-term option only after source review; it must not silently alter
Block 59/60 behavior.

## Agent 4 — Evaluation Scientist

- **Reported in EXP3:** dev probability artifacts are UID-aligned, but no
  verified training UID manifest or pooled-LR fit record establishes complete
  exclusion of dev rows from every exact fitted artifact. FT recipe uses train
  rows and selects epoch by dev Macro-F1; pooled artifact provenance is not
  linked (`EXP3_PROVENANCE_AUDIT_REPORT_v1.md:7–11,39–47,61–75`).
- **Reported in EXP1/NESTED CV:** question groups are used for bootstrap and
  grouped folds; current dev unseen subset is not independent because it is
  part of development/selection. Existing test exposure means old test cannot
  be renamed a clean holdout.
- **Proposed protocol:** reserve new whole question IDs before answer
  collection/expansion; use train for fit, grouped dev/nested CV for all
  selection/calibration/threshold choices, and a custodian-held confirmation
  partition for one final frozen run. Record provenance, label review,
  UID/group manifests, hashes, versions, seeds, model revisions, exclusions,
  confidence intervals and analysis version.
- **Proposed metrics:** accuracy alongside Macro-F1 as a primary candidate;
  per-class precision/recall/F1, weighted F1, QWK for ordered labels, ECE and
  Brier score, coverage-accuracy curves, per-subject and cold/warm results,
  with paired question-group intervals. Jigar must approve the primary metric,
  acceptance thresholds and sample-size/precision target before collection or
  unblinding. No threshold is invented here.

## Agent 5 — Chief Decision Officer: cross-examination

| Challenge | Evidence and resolution | Remaining unknown / next actor |
|---|---|---|
| Does a runtime recommendation prevent drift? | Not by itself. A single root plus hash-checked scorer/JSON/policy and a manual live preflight would reduce drift. The scorer currently has silent fallback. | Jigar approves exact hashes/root; must run preflight in Colab before inference. |
| Are the existing banks defensible? | No. Structural schema and rich fields do not demonstrate correctness; 251 records lack subject/grade, and 12 records are Science drafts only. | Jigar selects a starting source; qualified reviewers establish quality. |
| Does the evaluation design prevent question leakage? | Grouping by `dataset|question_id` and holding whole questions helps. Existing saved work still uses dev for selection and provenance is incomplete. | Need verified train manifests and new custodian-held questions/labels. |
| Can Phase 1 begin without live Colab? | Yes for isolated, non-scoring schema/ingestion/interface design, after Jigar approves scope and immutable baseline boundary. No scorer calls, production, accuracy claim, or model experiment. | Jigar must explicitly authorize the revised scope. |
| Can new confirmation data wait? | It can wait for schema/design; it cannot wait past candidate model/threshold selection if a confirmatory accuracy claim is required. | Data steward/reviewers create and lock a new set before confirmatory evaluation. |
| Does four-subject review need to block all Phase 1 work? | No for generic infrastructure. It must block use of those subjects' content as approved scoring material, four-subject evaluation claims, or pilot assessment. | Jigar nominates reviewers and sequences content review. |

**CDO recommendation:** revise the six-gate definition into staged readiness.
The original rule over-blocks design-only infrastructure by requiring live
runtime, finished four-subject review, and collected confirmation data before
any Phase 1 work. Keep those gates hard before the activities they protect.
This is a recommendation, not Jigar's approval. No Phase 1 work was started.

## Critical risks and recommendations

| Risk | Consequence | Minimum safeguard | Classification |
|---|---|---|---|
| Root/policy mismatch or fallback | Teacher-review behavior silently differs | Hash-check exact JSON/policy/scorer at one root; fail closed | Critical before scorer execution |
| Notebook source drift | Wrong block/config run | Select exact notebook hash; diff against frozen source | Critical before notebook execution |
| No question context in two components | Relevance misses, especially cold questions | Treat as candidate weakness; evaluate relevance slices | Later scorer experiment |
| No rubric in deployed path | Partial/correct decisions may not match educational criteria | Do not claim rubric-based scoring; require approved criteria before integration | Critical before rubric scoring/pilot |
| Unreviewed banks | Invalid answer keys/rubrics | Explicit draft status, subject review, versioned sign-off | Critical before content use/pilot |
| Dev selection/test exposure | Inflated or non-independent claims | Grouped dev for selection; new locked confirmation for claims | Critical before confirmatory claim |
| Unpinned model/package identity | Reproduction drift/runtime failure | Capture exact hashes, package versions, hub snapshot IDs | Critical before runtime reproduction |
| Historical artifact-writing cells | Overwrite frozen outputs | Keep explicit cell allowlist; never Run All | Critical before notebook action |

## Research-topic review and sources

| Area | Internal finding | Practical recommendation | External research |
|---|---|---|---|
| Leakage and grouped evaluation | Prior test exposure and unverified fit provenance are documented; question grouping exists in saved dev analyses. | Group by question before all split/bootstrapping; lock new confirmation. | BLOCKED: no-network rule; no external source cited. |
| Constructed-response grading | Current scorer has no rubric input; Partial is learned output. | Validate rubric criteria with subject experts before scoring claims. | BLOCKED. |
| Assessment validity/reliability | Schema validation checks structure, not educational meaning. | Independent reviews, adjudication, provenance, versioning. | BLOCKED. |
| Math equivalence and method credit | Current corpus does not demonstrate mathematics coverage. | Include symbolic/numeric equivalence, units/tolerances, alternate methods. | BLOCKED. |
| Calibration/selective prediction | Confidence threshold is dev-derived; missing policy can change review behavior. | Calibrate on development only; evaluate frozen review policy on independent data. | BLOCKED. |
| Dataset/confirmation design | Existing clean independent set not established. | Collect new provenance-documented question-disjoint data; lock labels. | BLOCKED. |
| Reproducibility/config | Hash/path issues and unpinned revisions/versions. | Lock file hashes, root, package versions, model revisions, run manifests. | BLOCKED. |
| Question-bank versioning | Handover bundle has schema and IDs; no authority decision. | Use immutable IDs, versioned records and explicit status transitions. | BLOCKED. |
| Human review | No reviewers/signoffs found. | Four-subject assignments and review record required. | BLOCKED. |

## Final critique

The current v2 scorer can serve as a **frozen comparison baseline** for
development work only when the exact scorer/config/artifacts are bound and
its results are labeled appropriately. It is not yet a provenance-complete,
educationally reviewed, live-reproducible production foundation. The minimum
safe near-term work is to approve scope and a baseline boundary, design the
canonical schema/review workflow and predeclare evaluation. Runtime
verification, content sign-off, and independent confirmation remain hard
gates before scorer execution, assessment claims, or pilot use as described
in the phase criteria.
