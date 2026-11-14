# Project S — Phase 0 Verification Report v2

**Verified:** Read-only continuation. No notebook output fields or test-split contents were inspected. Local files only; live Drive status remains unverified.

## Task 3b — JSON conflict

| Status | Field / check | Staged `reports_v2` JSON | Packaged `A_submission_v2/reports_v2` JSON |
|---|---|---|---|
| Verified | Path | `project_s_qa/reports_v2/A_demo_reference_outputs_v2.json` | `project_s_qa/A_submission_v2/reports_v2/A_demo_reference_outputs_v2.json` |
| Verified | Size / filesystem mtime | 16,474 bytes; 2026-11-06 00:02:08.3959188 +05:30 | 16,474 bytes; 2026-11-06 03:33:57.6158509 +05:30 |
| Verified | SHA-256 | `c99b7d84d000046c9629708d5ee440d5a20ab28fd298f63708e2e8c13f89dc92` | `ea5288e9f12b25d28a66f36ec38d48b08c65e19452bf3b5efa17eed2be20aeb9` |
| Verified | `/created` | `2026-10-24T14:31:06` | `2026-10-30T09:20:06` |
| Verified | `/policy_sha256` | `babf76f460d2a6516d9ef11d317f69ceddb0958dd67a2ce06d3b67496163ad25` | `b6548edeb682eabd2ba6b74d9b9b67bff293c1fea9c3cb6345e0a7ebf7e9ef9b` |
| Verified | Identical fields checked | `scorer_mode=pooled`; `a_predict_sha256=ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053` | Same values |

**Verified:** Recursive JSON comparison found exactly two differing fields (`/created`, `/policy_sha256`). No test-split node was found; no case answers or saved outputs are included in this report.

| Status | Policy file check | Path / SHA-256 | Match |
|---|---|---|---|
| Verified | Staged policy | `project_s_qa/reports_v2/A_abstain_policy_v2.json` — missing | Staged JSON hash has no matching policy file in the staged path or its backup copy |
| Verified | Packaged policy | `project_s_qa/A_submission_v2/reports_v2/A_abstain_policy_v2.json` — `b6548edeb682eabd2ba6b74d9b9b67bff293c1fea9c3cb6345e0a7ebf7e9ef9b` | Matches packaged JSON |
| Verified | Backup packaged policy | `project_s_qa_backup_20261106_1957/A_submission_v2/reports_v2/A_abstain_policy_v2.json` — same SHA-256 | Matches packaged JSON |
| Verified | Policy reference | `reports_v2/A_predict.py`, lines 139–141 | `_load_policy()` reads `A_abstain_policy_v2.json` from V2; if absent, it uses `PROVISIONAL_POLICY` |

**Verified:** The scorer file is identical in both folders: SHA-256 `ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053`; staged mtime 2026-11-06 00:02:08.3777872 +05:30; packaged mtime 2026-11-06 03:33:57.3306372 +05:30.

**Verified:** The notebook source names the reference JSON in cells 118, 127, 139, 157, and 163. Block 59 is code cell 157; it reads `/content/drive/MyDrive/project_s_qa/reports_v2/A_demo_reference_outputs_v2.json`, checks `scorer_mode == "pooled"`, and checks `a_predict_sha256` against the loaded `A_predict.__file__` SHA-256. It does not check `policy_sha256`. Block 60 code cell 159 does not reference this JSON. **Verified:** `README_FILES.txt` has no line naming `A_demo_reference_outputs_v2.json`.

**Unverified / recommendation inconclusive:** The packaged JSON has the stronger local pairing evidence because its `policy_sha256` matches an available policy file. Block 59 instead reads the staged `reports_v2` path, where that policy file is absent. No local Google Drive mount was found, so live Drive state cannot establish which JSON is active. No file was replaced; Jigar's decision is needed.

## Task 4 — Notebook candidates

| Status | Candidate | Path | Size | Filesystem mtime | SHA-256 | Cells / code cells |
|---|---|---|---:|---|---|---:|
| Verified | Local COPY | `notebooks/Jigar_Q&A_Branch_Baseline_COPY.ipynb` | 2,690,082 bytes | 2026-11-06 04:20:13.2337466 +05:30 | `5eb5dc4fd1ad85dce55c9b1222603fc11de19d51bb682103fc7923bc78b5faf0` | 167 / 68 |
| Verified, provenance unverified | Likely Colab-executed candidate `COPY_UPDATED` | `notebooks/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb` | 3,642,032 bytes | 2026-11-06 02:56:12.6067136 +05:30 | `f2e2a4a5fdd7beaa208a192f6101ec9cb40789400b0d823003554fb1f4aabd4d` | 169 / 70 |
| Verified | Separate `notebooks/colab_download/*.ipynb` export | Folder not present | — | — | — | Not found |
| Verified | Clean 162-cell reference | `notebooks/reference/*REFERENCE_162*.ipynb` | — | — | — | Not found |

**Verified:** `COPY_UPDATED` has non-null execution-count metadata on code cells 157, 159, 161, and 163 (Blocks 59–62; counts 2–5), plus cell 167 (count 1). The local COPY has no non-null execution-count metadata. No saved outputs were inspected, so successful execution is unverified.

**Proposed:** Use `COPY_UPDATED` as the likely Colab-execution evidence candidate because its execution-count metadata covers Blocks 59–62. Keep the local COPY as the authoritative editable source. Do not merge; the candidates differ in count and no output-level comparison was performed.

## Task 5 — T3, backup chain, and README inventory

| Status | Check | Actual result |
|---|---|---|
| Verified | Local COPY cell count | 167 total, 68 code; README line 20 says 165 |
| BLOCKED | T3 against clean reference | Reference not found; expected 165 / 16 differing / 149 identical cannot be verified |
| Verified | Backup `before_block60` | Present; 159 cells; SHA-256 `ae0ccae2ca195cf3b955daa0f79d1577142f540cde01edda9a4d47daa92ff944` |
| Verified | Backup `before_block61` | Present; 161 cells; SHA-256 `953e5133fff3b87d5c938d1fda7186a446c80cdb855480734389193bcdce449d` |
| Verified | Additional `before_Block59_60_20261106_010007_389` | Present; 167 cells; SHA-256 `e241d40e8804de89e0b52bc486786987d0107e0dc2c5a05f03c8773cbb856a7b` |
| Verified | Additional `before_phase5` | Present; 165 cells; SHA-256 `b170db749806ebbe2798d56c6392fc1b0cee0acc8ef1b8f7d49c89f97c5134bf` |
| Verified | Additional `before_phase5_docs_20261106` | Present; 167 cells; SHA-256 `a35efc489c25806f2ad3db8684006dc2d627634dc1e6d2a61d3fbc75c615030e` |

**Verified:** README-listed paths exist except the 162-cell reference; its line 34 already says `NOT YET PRESENT`. The listed Block 60 files, tools, archives, original notebook, and two named backups are present. **Verified:** README line 20 has a stale COPY cell count (165 vs 167).

**Verified — unlisted extras:** `notebooks/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb`; the three additional backups above; top-level `.AI/`, `_backups/`, `project_s_qa/`, `project_s_qa_backup_20261106_1957/`, `Project_S_QA_Evidence/`, `PHASE0_REPORT.md`, and `PHASE1_VISHWAJEET.md`. The `notebooks/colab_download/` folder is absent.

## Task 6 — Static code-block safety classification

**Verified:** Classification uses notebook source only. `FROZEN` means protected, test-sensitive, or one-time frozen pipeline state; `RERUN-WITH-BACKUP` means source writes artifacts that may be overwritten; `SAFE-TO-RERUN` means no persistent project write, model training, or test-split access was found. This classification is not permission to run: cell 0 says run only Summary and Blocks 59–62; other cells are one-time producers.

| Cell | Block / section | Classification | Source evidence |
|---:|---|---|---|
| 5 | Block 1: install, config, folders | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 7 | Block 2: load both datasets and check counts | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 9 | Block 3: one shared table | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 13 | Block 4: label mappings | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 15 | Block 5: label distribution and per-question report | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 17 | Block 6: data-quality and leakage checks, then save | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 20 | Block 7: source register (Step 1) and CBSE syllabus hook | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 22 | Block 8: question bank | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 24 | Block 9: rubric stubs | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 27 | Block 9: rubric stubs | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 29 | Block 10: build the splits | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 31 | Block 11: leakage checks | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 33 | Block 12: save v1, rebuild rubrics, hash manifest | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 36 | Block 13: setup, metrics, majority baseline | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 38 | Block 14: TF-IDF baselines (similarity-only and TF-IDF + LR) | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 40 | Block 15: SBERT baselines, comparison table, saved results | Verified — RERUN-WITH-BACKUP | static source has to_csv, to_parquet, json.dump, file write, model save; outputs may be overwritten |
| 43 | Block 16: NLI concept-check features | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 45 | Block 17: rubric-prompted LLM scorer (dev splits only) | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 47 | Block 18: NLI classifier, fair comparison, save | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 50 | Block 19: fine-tune DistilRoBERTa | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 52 | Block 20: stack the models into a combiner | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 54 | Block 21: abstain / teacher-review rule and scored output | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 58 | Block 22: freeze check (run before touching EVAL_TEST) | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 60 | Block 23: test results, confidence intervals, frozen abstain rule | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 62 | Block 24: error analysis, LLM comparison, report summary, final package | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 65 | Block 25: dev-only ensemble weights and abstain rule | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 68 | Block 26: fine-tune a second, stronger model | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 70 | Block 26: fine-tune a second, stronger model | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 72 | Block 27: v2 needs_review flag for non_domain (score stays 0) | Verified — RERUN-WITH-BACKUP | static source has to_csv, to_parquet; outputs may be overwritten |
| 74 | Block 28: select the final scorer on dev only | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 78 | Block 29: housekeeping audit and artifact inventory (read-only) | Verified — RERUN-WITH-BACKUP | static source has file write; outputs may be overwritten |
| 80 | Block 30: resolve the freeze finding, run manifest (no GPU needed) | Verified — RERUN-WITH-BACKUP | static source has json.dump, file write; outputs may be overwritten |
| 82 | Block 31: component check | Verified — RERUN-WITH-BACKUP | static source has json.dump, file write; outputs may be overwritten |
| 86 | Block 32: write A_predict.py and test it on one example | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 88 | Block 33: parity check (20 dev rows, tolerance 0.02) | Verified — RERUN-WITH-BACKUP | static source has to_csv; outputs may be overwritten |
| 90 | Block 34: provisional review policy, contract, hand-written smoke test | Verified — RERUN-WITH-BACKUP | static source has to_csv, json.dump, file write; outputs may be overwritten |
| 93 | Block 35: dev comparison of all models under one protocol | Verified — RERUN-WITH-BACKUP | static source has to_csv; outputs may be overwritten |
| 95 | Block 36: choose the dataset default | Verified — RERUN-WITH-BACKUP | static source has to_csv, json.dump, file write; outputs may be overwritten |
| 97 | Block 37: error analysis on dev | Verified — RERUN-WITH-BACKUP | static source has to_csv; outputs may be overwritten |
| 100 | Block 38 : choose the deployable scorer | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 102 | Block 39: calibration diagnostics, temperature scaling, threshold choice | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 104 | Block 40: final review policy and a check that the demo function matches it | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 108 | Block 41: paired question-level bootstrap CIs | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 110 | Block 42: seed-variability summary | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 112 | Block 43: exploratory test run (frozen policy) | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 116 | Block 44: reference outputs for the demo (15 hand-written cases) | Verified — RERUN-WITH-BACKUP | static source has json.dump, file write; outputs may be overwritten |
| 118 | Block 45: parity with Vishwajeet’s demo | Verified — RERUN-WITH-BACKUP | static source has to_csv, json.dump, file write, copy/zip/savefig; outputs may be overwritten |
| 120 | Block 45: parity with Vishwajeet’s demo | Verified — RERUN-WITH-BACKUP | static source has json.dump, file write, copy/zip/savefig; outputs may be overwritten |
| 122 | Block 45b: five test cases | Verified — RERUN-WITH-BACKUP | static source has to_csv; outputs may be overwritten |
| 123 | Block 45b: five test cases | Verified — SAFE-TO-RERUN | static source has no persistent write, training, or test-split access |
| 125 | Block 45c: Gradio interface | Verified — SAFE-TO-RERUN | static source has no persistent write, training, or test-split access |
| 127 | Block 46: tested-answers summary and slide examples | Verified — RERUN-WITH-BACKUP | static source has to_csv, file write; outputs may be overwritten |
| 131 | Block 47: final tables | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 133 | Block 48: figures | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 135 | Block 49: results summary, v2 package and status | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 139 | Block 50: concepts and per-concept NLI | Verified — RERUN-WITH-BACKUP | static source has to_csv, json.dump, file write; outputs may be overwritten |
| 141 | Block 51: negation, paraphrase and spelling control set | Verified — RERUN-WITH-BACKUP | static source has to_csv, file write; outputs may be overwritten |
| 143 | Block 52: ML/DL-only audit | Verified — RERUN-WITH-BACKUP | static source has json.dump, file write; outputs may be overwritten |
| 145 | Block 53: generalization by question cluster (dev only) | Verified — RERUN-WITH-BACKUP | static source has to_csv, file write, training; outputs may be overwritten |
| 148 | Block 54: learned deferral vs the threshold (study only, grouped CV) | Verified — RERUN-WITH-BACKUP | static source has to_csv, json.dump, file write, training; outputs may be overwritten |
| 150 | Block 55, deployed policy has no hand rule | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 153 | Block 57, ML-derived question descriptors | Verified — RERUN-WITH-BACKUP | static source has to_csv; outputs may be overwritten |
| 155 | Block 58: closure and zip | Verified — FROZEN | READ FIRST / AGENTS protected or test-sensitive block |
| 157 | Block 59: latency benchmark (single-answer and batch, in ms) | Verified — RERUN-WITH-BACKUP | reads reference JSON and runs timing inference; writes no files |
| 159 | Block 60: question dropdown and voice input demo (adult voices only) | Verified — SAFE-TO-RERUN | source comment says writes no files; launches demo runtime |
| 161 | Block 61: component probabilities for the 12 negations (diagnostic, writes nothing) | Verified — SAFE-TO-RERUN | diagnostic/timing source states writes nothing |
| 163 | Block 62: stage timing (writes nothing) | Verified — RERUN-WITH-BACKUP | diagnostic/timing source states writes nothing |
| 166 | Summary for the panel | Verified — RERUN-WITH-BACKUP | Summary code loads saved files; no persistent write found |
**Verified — requested blocks:** Block 42 cell 110 is FROZEN (seed summary is consumed by Block 49); Block 45 cells 118 and 120 are RERUN-WITH-BACKUP (write/copy parity artifacts); Block 49 cell 135 is FROZEN (report/package producer); Block 58 cell 155 is FROZEN (closure/package producer); Block 59 cell 157, Block 60 cell 159, Block 61 cell 161, and Block 62 cell 163 are SAFE-TO-RERUN by source (write no files). Block 63 heading is absent.

**Verified — Block 59 checks:** `V2` is `/content/drive/MyDrive/project_s_qa/reports_v2`; JSON path is `${V2}/A_demo_reference_outputs_v2.json`. The cell checks only `scorer_mode == "pooled"` and `a_predict_sha256 == sha256(A_predict.__file__)`. It does not validate `policy_sha256`.

## Done-when status and remaining blockers

| Status | Done-when item | Result |
|---|---|---|
| Verified | Backup exists and hash/path verification passes | PASS; prior Phase 0 report has the full 67-file source/backup SHA-256 manifest |
| Verified | Notebook candidate identified | PASS; local COPY and likely executed COPY_UPDATED identified |
| Verified | Scorer/reference pair identified | PARTIAL; scorer hashes match; JSON policy hashes conflict |
| BLOCKED | T3 structural comparison | Reference missing; not compared |
| Verified | Block safety classification recorded | PASS; all 68 code cells listed above |
| Unverified | Google Drive live status/sync | UNVERIFIED; local mount not available |

- **BLOCKED:** Jigar must decide which JSON is authoritative for the live `reports_v2` runtime; no replacement was made.
- **BLOCKED:** T3 requires the clean 162-cell reference notebook.
- **Unverified:** COPY_UPDATED execution-count metadata suggests a Colab run, but outputs and run provenance were not verified.
- **Unverified:** Live Google Drive state and synchronization.

## Erratum — safety table and policy mtime

- **Verified:** Static source review found that a generic `open()` detector counted read-mode file access as a write. This affected cells 78, 157, 163, and 166. Their corrected classifications are **SAFE-TO-RERUN**; this erratum supersedes the table entries for those four cells. The other RERUN-WITH-BACKUP rows also contain explicit output operations such as `to_csv`, `to_parquet`, `json.dump`, `joblib.dump`, copy/archive, or model training.
- **Verified:** The packaged policy file and backup copy each have mtime `2026-11-06 03:33:57.2981041 +05:30`, size 784 bytes, and SHA-256 `b6548edeb682eabd2ba6b74d9b9b67bff293c1fea9c3cb6345e0a7ebf7e9ef9b`. The staged policy path and its backup counterpart are absent, so they have no local mtime/hash to report.
