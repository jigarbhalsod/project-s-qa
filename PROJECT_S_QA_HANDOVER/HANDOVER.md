# Project S Q&A Branch — Handover

**Prepared 10 November 2026.** This is a static handover package. It does not
claim clean-room reproducibility, a new accuracy result, or CBSE validation.

## 1. Purpose and current state

The Q&A branch predicts one of three labels for a student answer: Incorrect
(0), Partial (1), or Correct (2). It uses public SciEntsBank and Beetle data.
It has not been validated on CBSE answers or children. The minimum target of
85% accuracy at 30% coverage was not met in the project record.

## 2. Source of truth and notebook choice

The current local Drive-backup notebook D is
`drive_backup_20261107/notebooks/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb`
(169 cells; SHA-256 recorded in `docs/frozen_files_manifest.csv`). The
executed Phase 2 run copy is
`Project_S_QA_Evidence/Phase_2/Jigar_QA_PHASE2_RUN_COPY_EXECUTED.ipynb`
(169 cells). Static source comparison found only cell 157 differs: the run
copy wraps Drive mounting in a try/except and adds a policy-file/hash check.
It has stored outputs; the copied D is the code baseline. The Phase 2 tracker
reports Blocks 59–62 ran, but that is not an independent runtime reproduction.

Jigar must decide which notebook is the submission candidate. This package
contains byte-for-byte copies named `notebooks/notebook_D.ipynb` and
`notebooks/notebook_run_copy.ipynb`. Neither was edited. Block 64 is a
standalone draft in `notebooks/Block_64_cell.py`; it has not been inserted or
run. Block 63 is absent in both compared notebooks. Never use Run All, never
run Block 49, and never run cell 166 (Summary); those restrictions remain.

## 3. Architecture

See `docs/architecture.md`. The frozen scorer is `src/A_predict.py`, copied
from the local submission package. It is included for inspection only. At
runtime, import the Drive copy from `project_s_qa/reports_v2`, set
`PROJECT_S_ROOT` to the actual Drive project root, and verify the source hash
before use. The scorer needs `interim/ft_distilroberta_v1/`,
`interim/pooled_lr_v2.joblib`, and its configured NLI/SBERT model assets.

The scorer does not load the question-bank rubrics. Block 64 retrieves and
displays the linked rubric for traceability, but calls the frozen scorer with
question text, reference answer, student answer, and `dataset="pooled"` only.
No score or threshold has been changed in this package.

## 4. Question bank

`question_bank/` contains 12 existing Science demo questions copied from
`project_s_qa/processed/cbse_demo_questions_v1.csv`. All remain
`draft_unreviewed`. The source gives grade, topic ID, difficulty and a source
page, but not a chapter or reviewed concept rubric. Those omissions are marked
for human review; no CBSE approval is claimed. Math, Social Science and EVS
records are not present. The 240-question target is not met and must not be
represented as complete. The public-data `question_bank.csv` candidates were
not imported because they may mix splits and are outside this handover's
allowed data scope.

## 5. Ingestion and validation

`src/ingestion/ingest.py` supports JSON and CSV with the Python standard
library, and Excel when pandas plus an Excel reader are available. It preserves
IDs and review status, creates deterministic IDs only when absent, skips
normalized duplicates, refuses output overwrite, and creates missing rubric
records in `draft_unreviewed` status. PDF extraction and semantic duplicate
detection are deferred. Sentence-Transformers is not required for ingestion.

Validation is implemented in `src/validation/question_bank.py`. It checks
required fields, duplicate/missing IDs, grade/difficulty/review status, the
three-class label contract, rubric references, missing rubrics, and approval
requirements. No tests were run; see `tests/` for drafted tests and
`docs/setup.md` for user-run instructions.

## 6. Setup and model access

Read `docs/setup.md` and `models/CHECKPOINT_ACCESS.md`. The archived
`A_run_manifest_v2.json` records Python 3.13.16 and package versions, but those
values describe a historical runtime snapshot, not the current Colab image.
There is no verified lockfile or current dependency probe. Do not install
unlisted versions by inference. Model weights are not copied into this
handover; retrieve them only from the authorized project Drive location and
verify hashes against `docs/frozen_files_manifest.csv`.

## 7. Controlled demo and evaluation procedures

`docs/phase3_execution.md` links the copied Phase 3 runbook and evidence
checker. Phase 3 remains incomplete: no screenshot or video files were found
in the local Phase 3 directory. Phase 2 voice notes are included as
user-reported notes only; they provide no aggregate voice rate. Do not claim
child-voice or CBSE scoring accuracy.

`docs/export_trial.md` describes the 16-row dry run and full dev-only export.
The local full component-probability export and its validation report exist
in `evidence/export_trial/outputs/`; this does not establish that a new 16-row
trial was run during handover. Never open test files, test splits, cell 166,
or Block 49. User execution only, with saved logs and artifacts.

## 8. Known limitations and handover blockers

- The provided abbreviated “policy” hash (`ca7c2752…a053`) matches the
  scorer hash, not the packaged policy. The policy's observed full hash is in
  the build report; no policy file was changed. The copied policy config is
  marked unverified against the supplied expected value. Jigar must resolve
  the hash-reference error before packaging that config as verified.
- Local `project_s_qa/reports_v2/` does not contain the policy file; the
  package copy stores it under `A_submission_v2/reports_v2/`. The live Drive
  state is not independently confirmed.
- The question bank has 12 Science drafts, incomplete chapter/rubric metadata,
  and no human review; 228 more questions toward the stated target are absent.
- No child-answer pilot or CBSE validation exists. The existing test sets were
  exposed in earlier project work; any test result remains exploratory.
- No current notebook selection, runtime installation, or external access
  transfer was confirmed by this package.

## 9. Vishwajeet's independent handover steps

1. Read `AGENTS.md`, this file, `docs/architecture.md` and
   `docs/known_limitations.md`.
2. Verify the notebook and frozen-file hashes in `docs/frozen_files_manifest.csv`.
3. Ask Jigar to resolve the scorer-versus-policy hash discrepancy and choose
   D or the run copy before any notebook handoff.
4. Obtain authorized access to the Drive project root and model assets; do not
   use credentials embedded in messages or notebooks.
5. Review all 12 question and rubric records; fill missing chapters,
   concepts, misconceptions, accepted variants and partial-credit criteria.
6. Run the drafted tests in an isolated environment only after Jigar approves.
7. Perform the Phase 3 evidence workflow and the dev-only 16-row export trial
   manually. Save actual outputs; never claim success before the files exist.
8. Return the required 12 CBSE question corrections and any missing RoBERTa
   artifacts through the agreed project handoff.

## 10. Status

The package is **PARTIAL**. Source copies, documentation, draft ingestion,
validation, a 12-question draft bank, Block 64 draft, test drafts and run
instructions are prepared. No project script, notebook, test, model or
training procedure was executed. See `BUILD_REPORT.md` for deliverable status.
