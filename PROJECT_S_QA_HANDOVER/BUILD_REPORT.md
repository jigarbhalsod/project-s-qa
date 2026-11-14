# Project S Q&A handover build report

**Prepared:** 10 November 2026  
**Project root:** `C:\Users\Jigar\OneDrive\Desktop\Project 4`  
**Package:** `PROJECT_S_QA_HANDOVER/`  
**Overall status:** **PARTIAL**. This is a static handover package, not a tested
release. No notebook, scorer, model, project script, or test suite was run.

## Audit scope and evidence labels

The working tree, AGENTS.md, PROJECT_CONTEXT.md, relevant AI-context notes,
available architecture/setup/Phase 3/Phase 4 documents, notebook JSON structure,
scorer/config files, question-bank source and generated records, ingestion and
validation source, drafted tests, Phase 2/3 evidence inventory, Phase 8 export
artifacts, and accessible Notion tracker were inspected read-only. No live Drive
state was checked. No test split or test output was opened; test-named artifacts
were listed only where required. Notion was read, not edited.

`Verified` means directly checked from local files or their hashes. `Reported`
means recorded in user-provided results or existing project reports.
`Drafted` means created here and not executed. `Not tested` means no runtime
validation was performed. `Blocked` means an unresolved input or decision
prevents a safe claim.

## Deliverable status

| Deliverable | File path | Status | Verification evidence | Remaining action |
|---|---|---|---|---|
| Handover guide | `HANDOVER.md` | Drafted | Documents source-of-truth, architecture, restrictions, gaps and handoff steps | Jigar selects notebook and resolves policy hash conflict |
| Frozen artifact registry | `docs/frozen_files_manifest.csv` | Drafted | Source and included-copy hashes/sizes; notebook copies verified byte-identical to their sources | Resolve the policy reference discrepancy; obtain current Drive verification |
| Notebook candidates | `notebooks/notebook_D.ipynb`, `notebooks/notebook_run_copy.ipynb` | Verified | D: 169 cells; run copy: 169 cells; source-only diff is cell 157 only | Jigar must choose one; run provenance and cloud sync remain unverified |
| Scorer source copy | `src/A_predict.py` | Verified | SHA-256 matches packaged source: `CA7C2752...D0A053` | Runtime must import authorized project copy, not this inspection copy |
| Runtime config copies | `src/config/` | Partial | JSON copies match packaged sources; policy source hash is `B6548EDE...E9EF9B` | Supplied policy reference is actually scorer hash; do not treat policy copy as verified for runtime |
| Question bank | `question_bank/questions.json`, `rubrics.json`, `schema.json` | Drafted | JSON parses; 12 question and 12 rubric records; every record `draft_unreviewed` | Human review and reliable curriculum sources; 228 more to reach 240 |
| CSV source snapshot | `question_bank/cbse_demo_questions_v1_source.csv` | Verified | Byte hash matches local source; 12 rows, all draft_unreviewed | Vishwajeet's corrections remain pending |
| Ingestion | `src/ingestion/` | Drafted | JSON/CSV and optional Excel paths in source; PDF explicitly deferred | User must run tests in isolated environment |
| Validation and lookup | `src/validation/`, `src/question_bank.py` | Drafted | Required fields, IDs, labels, linked rubrics and review status checked in source | User must run tests; no claim of runtime pass |
| Demo bank wrapper | `src/block64_demo_bank.py` | Drafted | Reads selected question/rubric and passes question/reference/answer to frozen scorer; rubric is display-only | Requires authorized runtime paths and manual integration check |
| Block 64 notebook cell | `notebooks/Block_64_cell.py` | Drafted | Separate source file; not inserted into either notebook | Jigar must approve and paste into a new run copy |
| Unit tests | `tests/` | Not tested | Four test source files drafted for validation, ingestion, retrieval and JSON import | Run only after approval in an isolated environment |
| Dependency list | `requirements.txt` | Drafted | Historical versions separated from unspecified versions | Confirm current runtime and approve installation choices |
| Checkpoint instructions | `models/CHECKPOINT_ACCESS.md` | Drafted | Access directions only; weights not included | Vishwajeet needs authorized Drive access and hash verification |
| Phase 3 evidence materials | `evidence/phase3/` | Drafted | Runbook, cases, checklist, checker and blank logs copied; no screenshots/video found | Jigar performs procedure and preserves actual evidence |
| Export trial materials | `evidence/export_trial/` | Reported | Full dev export and validation report copied; 16-row trial evidence not found | Jigar decides whether to run 16-row trial manually |
| Package hash list | `SHA256SUMS.txt` | Drafted | Lists package files, sizes and SHA-256; excludes itself by design | Rebuild after any package change |

## Frozen files and hash verification

The detailed registry is `docs/frozen_files_manifest.csv`. Rechecked source
hashes include:

| Artifact | SHA-256 | Status |
|---|---|---|
| Packaged `A_predict.py` | `CA7C2752A4863F2A24B20EC7CD9000B651D83A0CFC39709F0080EBCBDAD0A053` | Verified |
| Packaged reference outputs JSON | `EA5288E9F12B25D28A66F36EC38D48B08C65E19452BF3B5EFA17EED2BE20AEB9` | Verified |
| Packaged scorer contract JSON | `1A2B21A94EBA50F70F390995A038A8329C4D6D81AB58775E26083329A97D837C` | Verified |
| Packaged scorer metadata JSON | `5BDFE4BBA65EA6B81D1442DC71A1843FCF6367FE80AF1D5AE7EC49D8808F53BC` | Verified |
| Packaged abstain policy JSON | `B6548EDEB682EABD2BA6B74D9B9B67BFF293C1FEA9C3CB6345E0A7EBF7E9EF9B` | Verified as observed hash; blocked against supplied expected value |
| Dev text parquet | `21E7305557825B392A297FC4558B73E1161FCEFB07D82C9F802E33C877836EA2` | Verified |
| Dev probability parquet | `2E29A708152B288019A9FA50B55B9D823781E4BBE0144CD5EE533FEE9DDB5B0E` | Verified |
| Fine-tuned model weights | `671E70ACF931C6DEDD28EBFF73BACCFA3ACF3B07DBA13CB3EB15FC39F04761FD` | Verified source hash; weights not copied |

The 23 registry rows were rechecked against the current source paths and any
included package copies: zero size or hash mismatches. The package contains 55
files; `SHA256SUMS.txt` lists the other 54 and excludes itself to avoid a
self-referential hash.

The supplied abbreviated policy hash `ca7c2752…a053` does **not** identify the
policy; it matches `A_predict.py`. The policy's observed source hash is
`B6548EDE...E9EF9B`. The policy file was copied into `src/config/` before this
conflict was identified. That copy is explicitly marked not for runtime use
until Jigar resolves the reference. No original frozen file was changed.

Notebook D and the Phase 2 executed notebook copies have matching hashes to
their identified sources. Both contain 169 cells. Static source comparison
found a single difference at cell 157: the run copy adds a Drive-mount
try/except and a policy existence/hash check. This source comparison does not
authenticate a live Colab runtime. The clean 162-cell reference was not found.

## Completed by Codex

- Created an independent handover directory; existing project files were not
  edited, moved, renamed or overwritten.
- Copied notebook candidates and selected runtime/config evidence with hashes.
- Drafted the question schema, 12 linked question/rubric records, ingestion,
  validation, lookup, demo wrapper, Block 64 cell, instructions and tests.
- Copied Phase 3 instructions and the existing full dev export evidence.
- Prepared this report, a frozen-file registry and package SHA-256 list.

## Drafted but not tested

- Ingestion, validation, question-bank lookup, the Gradio wrapper, and Block 64.
- All four local test files. No test was run.
- Dependency installation instructions and Phase 3/export procedures.
- The draft question bank; it is not an accuracy improvement or validated
  curriculum resource.

## User execution required

- Choose D or the executed run copy; keep both copies unchanged until then.
- Resolve the policy hash mismatch and confirm the intended Drive folder.
- Transfer authorized Drive access to Vishwajeet without sharing credentials.
- Run the Phase 3 evidence checklist and preserve outputs, screenshots, video,
  voice log and runtime dates. The current local Phase 3 folder has no media.
- Decide whether to perform the 16-row dev export trial. The full dev export
  exists, but a separate 16-row trial artifact was not found.
- Run drafted tests in an isolated environment and report actual results.

## Vishwajeet execution required

- Independently verify file hashes and authorized model access.
- Review the 12 draft questions and rubrics; complete the 12 requested CBSE
  corrections and return them with provenance.
- Confirm label space, split, and UID alignment for any comparison artifacts.
- Perform no training until Jigar separately approves it.

## Blocked items

- Policy configuration cannot be certified against the supplied hash.
- Notebook submission choice remains undecided; clean 162-cell reference is
  absent locally.
- Live Google Drive synchronization and permission state are unverified.
- Question-bank target of 240 is incomplete: only 12 Science drafts are
  present; no Math, Social Science or EVS bank is included.
- Phase 3 evidence acceptance is not met; no screenshots or video were found.
- No current clean test holdout or CBSE/student-answer validation is claimed.

## Known limitations and recommended next steps

The model has not met the recorded target of 85% accuracy at 30% coverage.
Existing test results remain exploratory because the test sets were seen in
v1. No student pilot, CBSE validation, or clean-room reproducibility was
established here. Historical package versions are not a current environment
lock. The live Drive state is unknown.

Recommended sequence: resolve the policy hash and notebook choice; transfer
authorized access; have Vishwajeet independently verify the package; complete
the Phase 3 evidence workflow; review the question bank; then run the drafted
unit tests locally. Do not treat this handover as project completion.
