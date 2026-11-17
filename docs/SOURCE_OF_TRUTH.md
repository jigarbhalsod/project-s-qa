# Project S Q&A Branch — Source of Truth

## Decisions

| Area | Decision | Evidence and remaining ambiguity |
|---|---|---|
| Runtime scorer path | **Operational target identified:** `project_s_qa/reports_v2/A_predict.py`. | Block 60 cell 159 adds that directory to `sys.path`; scorer lines 8–10 derive `ROOT`, `interim`, and `reports_v2`. Thirteen local scorer copies share SHA-256 `ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053`. Which copy is currently deployed in live Drive is **UNRESOLVED**. |
| Inspection scorer | `PROJECT_S_QA_HANDOVER/src/A_predict.py` is byte-identical to the operational source in this checkout, but is not the notebook import target. | Handover docs instruct use of the authorized project copy. |
| Stale scorer | `tools/extracted_A_predict.py` is historical and differs (SHA `11e897c7…d5d216b`); no pooled mode and different default. | Do not use for runtime or pooled analysis. |
| Reference/policy pair | Packaged pair is internally consistent; root runtime pair is not. | Packaged JSON `EA5288E9…20AEB9` stores policy hash `B6548EDE…F7E9EF9B`, matching packaged policy. Root JSON `C99B7D84…F89DC92` stores policy hash `babf76…63ad25`; no matching policy was found and root policy is absent. The correct pair to install at the root runtime paths requires Jigar's confirmation and a separate approved action. |
| Runtime behavior when policy missing | Fallback behavior is established from source, but live Drive state is not. | `A_predict.py:139–141` silently selects provisional policy; `:16–17` sets 0.60; `:164` defaults contradiction flag to true. Packaged policy uses 0.64 and disables contradiction flag. |
| Notebook | No unique submission authority established by this audit. | Current updated local notebook has 169 cells; Phase 2 executed copy has source changes in cell 157; existing handover docs say Jigar must choose a candidate. Current updated cell 157 lacks policy-hash validation; executed Phase 2 cell 157 has it. |
| Question bank | **UNRESOLVED as canonical source.** | There is a 251-entry `A_rubrics_v2.json` package and a separate 12-question/12-rubric `PROJECT_S_QA_HANDOVER/question_bank/` draft bank. Neither is consumed by `A_predict.py`; Block 64 is a separate display-only prototype. |
| Rubric module | `PROJECT_S_QA_HANDOVER/src/question_bank.py` is the lookup module for the handover JSON bundle only. | It loads questions/rubrics and retrieves by ID; no evidence makes it the production bank. |
| Ingestion/validation | Handover `src/ingestion/ingest.py` and `src/validation/question_bank.py` are draft tools. | Code exists; no runtime tests were run. Structural checks do not verify educational correctness. |
| Evaluation | Experiment folders are reproducibility/evidence records, not production code. | EXP1 and EXP2 scripts consume saved dev artifacts; EXP3 is a static provenance audit. Reports exist, but this audit did not rerun them. Live clean test evaluation is not available. |

## Scorer implementation map

- `project_s_qa/reports_v2/A_predict.py`: frozen scorer; three components; equal averaging; 5-to-3 collapse; confidence/review. Key lines: `_load` 21–36, component inputs 61–101, `component_probs` 110–136, policy 139–141, prediction 144–178.
- `project_s_qa/interim/ft_distilroberta_v1/`: local model and tokenizer files.
- `project_s_qa/interim/pooled_lr_v2.joblib`: pooled SBERT-LR/NLI-LR heads.
- `project_s_qa/interim/combiner_v1.joblib`: legacy base-model structure loaded at initialization even for pooled path.
- `project_s_qa/reports_v2/A_demo_reference_outputs_v2.json`: root reference metadata and cases; scorer hash matches, policy hash does not match available policy.
- `project_s_qa/A_submission_v2/reports_v2/`: packaged scorer/config/policy/rubric snapshots. Not the import path used by current Block 60 unless root configuration is changed.
- `block60/block_60_voice_demo_cell.py` and notebook cell 159: demo source; imports top-level root scorer, reads the root processed CSV, and calls default pooled prediction.

## Question-bank and rubric ownership

The handover bundle has `question_bank/questions.json`, `rubrics.json`, and `schema.json`, plus `src/question_bank.py`, `src/ingestion/`, `src/validation/`, and `src/block64_demo_bank.py`. The handover bank has 12 Science question records and 12 linked rubric records, all `draft_unreviewed`; question records have empty `required_concepts`. The package's `A_rubrics_v2.json` has 251 records with concept fields; statuses are 248 `auto_draft` and 3 `demo`. These represent separate data assets, and the repo does not declare a single canonical question/rubric bundle.

`block64_demo_bank.py:23–30` retrieves a rubric but calls the scorer only with question, reference, student answer and pooled dataset, then states `rubric_used_for_score=False`. Block 64 is not integrated into current Block 60.

## Frozen, historical and stale artifacts

- **KEEP FROZEN:** deployed scorer, model weights/joblibs, gold labels, probability files, reference/policy files pending source-of-truth decision, backups, and protected notebook blocks described by AGENTS.md.
- **HISTORICAL/BACKUP:** `drive_backup_20261107/`, `project_s_qa_backup_20261106_1957/`, `_backups/`, archive ZIPs, prior notebook copies. Never infer cloud synchronization from local snapshots.
- **STALE:** `tools/extracted_A_predict.py`; older `PROJECT_CONTEXT.md`/`README_FILES.txt` notebook counts and layout; root `README.md` is template text.
- **DRAFT:** handover ingestion/validation/question-bank/Block 64 materials and Phase 8 x1 scripts. Do not treat as tested or deployed.

## Source-of-truth actions needed

1. Jigar selects one notebook candidate and one exact runtime root.
2. Jigar resolves the JSON/policy pair and confirms expected hashes before any synchronization or Colab use.
3. Jigar chooses whether the 251-entry package rubric or 12-entry handover draft is the starting source, or approves a new source-of-truth bundle.
4. Evaluation protocol and any candidate training require a clean confirmation set and separate approval. No test result is cleanly locked in the current repository record.
