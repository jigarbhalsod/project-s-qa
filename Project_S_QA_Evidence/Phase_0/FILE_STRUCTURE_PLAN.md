# Project S File Structure Plan — Stage A Dry Run

[Verified] Dry run only. No Stage B moves were performed. The inventory covers 101
files and excludes backup folders and `Project_S_QA_Evidence/`. Test-named artifacts
are included with path, size, and mtime only; their SHA-256 fields are intentionally
not computed. See `FILE_STRUCTURE_PLAN.csv` for one classified row per file.

## Notebook decision and candidates

| Status | Copy | Cells | SHA-256 | Decision |
|---|---|---:|---|---|
| [Reported by Jigar] D: `drive_backup_20261107/project_s_qa/notebooks/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb` | 169 | `37170a8b10dd590c300198bb45a5543b829d4a723443d2268e49a2375a8876c5` | Proposed submission candidate; awaiting explicit confirmation |
| [Verified] L: `notebooks/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb` | 169 | `f2e2a4a5fdd7beaa208a192f6101ec9cb40789400b0d823003554fb1f4aabd4d` | Same Block 59-62 outputs as D; keep pending decision |
| [Verified] F: `some files to fix/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb` | 167 | `a35efc489c25806f2ad3db8684006dc2d627634dc1e6d2a61d3fbc75c615030e` | Oldest; no Block 59-62 outputs; archive-only candidate |

[Verified] The prior identification memo said “cannot decide”; therefore all notebook
moves remain BLOCKED until Jigar confirms D. F is not quarantined now.

## Inventory classes

| Class | Count |
|---|---:|
| [Verified] KEEP-CANONICAL | 3 |
| [Verified] KEEP-REFERENCED | 54 |
| [Verified] QUARANTINE-DUPLICATE | 0 |
| [Verified] QUARANTINE-STALE | 0 |
| [Verified] PROTECTED | 30 |
| [Verified] BLOCKED-NEEDS-DECISION | 14 |

[Verified] Five test-named files have metadata only: `A_handtests_v2.csv`,
`A_table_test_v2.csv`, `A_test_access_log_v2.json`, `A_test_results_v2.csv`, and
`A_test_scored_v2.parquet`, all under `project_s_qa/A_submission_v2/reports_v2/`.
No content or hashes were collected for them.

## Exact duplicate groups and keepers

| Status | Hash prefix | Files | Keeper/evidence |
|---|---|---|---|
| [Verified] | `78852eb40581` | `block60/cbse_demo_questions_v1.csv`; `project_s_qa/processed/cbse_demo_questions_v1.csv`; upload staging `processed/` copy | Keep the source file for README and runtime CSV for notebook path; staging copy remains protected. |
| [Verified] | `ca7c2752a486` | `project_s_qa/reports_v2/A_predict.py`; `project_s_qa/A_submission_v2/reports_v2/A_predict.py`; `project_s_qa/A_submission_v2/demo/A_predict.py` | Runtime-path candidate is root reports_v2; package copies remain. Canonical scorer copy is not designated. |
| [Verified] | `a4b7f45a12f1` | Root, package, and upload-staging copies of `A_negation_paraphrase_v2.csv` | Root reports_v2 is the notebook runtime path; package copy stays with package; staging copy is protected. |
| [Verified] | `057e3decd03a` | Root interim and upload staging `combiner_v1.joblib` | Keep root interim runtime artifact. |
| [Verified] | `216493152a1b` | Root interim and upload staging `pooled_lr_v2.joblib` | Keep root interim runtime artifact. |
| [Verified] | `8c906f8eb778` | Root interim and upload staging `config.json` | Keep root model directory. |
| [Verified] | `671e70acf931` | Root interim and upload staging `model.safetensors` | Keep root model directory; protected checkpoint. |
| [Verified] | `ef7366853546` | Root interim and upload staging `tokenizer.json` | Keep root model directory. |
| [Verified] | `aa6a8a3f069d` | Root interim and upload staging `tokenizer_config.json` | Keep root model directory. |

[Verified] All duplicate groups are referenced or protected; none is safe to quarantine.
Near-name copies: D/L/F share the COPY_UPDATED basename but have different hashes;
`some files to fix/` contains F and a manual upload staging directory. The file named
`PROJECT_S_PHASE2_RUNTIME_CHECK.txt` and the upload manifest remain
BLOCKED-NEEDS-DECISION. No other outside-Evidence scratch/temp/checkpoint-copy names
were found.

## Before / proposed after tree

[Verified] Before (subdirectories summarized; full paths are in the CSV):

```text
Project 4/
  .AI/  archive/  block60/  notebooks/  project_s_qa/
  some files to fix/  tools/  root docs
  [excluded from inventory: backups/ and Project_S_QA_Evidence/]
```

[Proposed] After, if separately approved; no moves now:

```text
Project 4/
  AGENTS.md  PROJECT_CONTEXT.md  README_FILES.txt  README.md  .gitignore
  docs/ [BLOCKED: protected docs and root references]
  notebooks/ [D candidate pending confirmation; preserve reference/ and backups/]
  project_s_qa/
    reports_v2/ [preserve existing notebook runtime path]
    processed/ [PROTECTED]
    interim/ [PROTECTED; do not move to models/]
    A_submission_v2/ [retain Pair A package]
    demo/ [BLOCKED: moving scorer breaks import/path]
  archive/ block60/ tools/ .AI/ [retain unless individually approved]
  data/ models/ [no safe move while paths and artifacts are protected]
```

## Paths a proposed move would break

[Verified] No path-breaking move is in the Stage B list. These candidate structure
changes are BLOCKED because they would break notebook/scorer/README references:

| Proposed move | Referenced path string and evidence |
|---|---|
| Move/rename project root folders | Notebook `/content/drive/MyDrive/project_s_qa`; code cells 22, 27, 29, 36, 58, 65, 68, 72, 74, 78, 80, 82, 86, 88, 90, 93, 95, 97, 100, 102, 104, 108, 110, 112, 116, 118, 120, 122, 125, 127, 131, 133, 135, 139, 141, 143, 145, 148, 150, 153, 155, 157, 159, 166, 167 |
| Move A_predict to demo/ | `reports_v2/A_predict.py`; notebook import/copy/check cells 118, 123, 125, 139, 157, 163, 167; A_predict uses sibling `reports_v2`, `interim`, and model directories |
| Move model files from interim/ to models/ | `interim/combiner_v1.joblib` cells 52, 62, 82, 86; `interim/pooled_lr_v2.joblib` cells 100, 112; A_predict lines 9, 10, 35, 106 |
| Move policy/JSON out of reports_v2/ | `reports_v2/A_abstain_policy_v2.json` cells 86, 90, 104, 112, 116, 131, 133, 135, 143, 145, 148, 150, 155, 166; reference JSON cells 118, 127, 139, 157, 163, 167 |
| Move control CSV out of reports_v2/ | `reports_v2/A_negation_paraphrase_v2.csv` cells 141, 161, 166 |
| Move CBSE CSV out of processed/ | `processed/cbse_demo_questions_v1.csv` cell 159; README line 54 |
| Move notebook/support files | README_FILES.txt lines 20, 25, 29, 34, 41, 46, 52, 57, 62, 67, 72; AGENTS.md specifies the working COPY path |

## Exact Stage B move list and restore format

[Proposed] Stage B move list: **none**. Every duplicate is protected or referenced;
notebook moves await D confirmation; other staging files have unresolved purpose.
No file will move until Jigar replies `go B` with approved rows.

[Proposed] Restore manifest columns:
`original_path,new_path,sha256,reason,move_time,status`.

[Verified] This is a dry-run plan. No file was moved, renamed, quarantined, merged,
modified, overwritten, or deleted.
