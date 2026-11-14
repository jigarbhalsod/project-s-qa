# Project S Phase 0 Final Closure

All claims are labelled. Scope: local Project 4 only. Backup directories and
`Project_S_QA_Evidence/` were excluded from the working-tree inventory.

## Part 1 — Cell 122, D vs L

| Status | D: drive_backup copy | L: local notebooks copy |
|---|---|---|
| [Verified] First source line | `from google.colab import drive` | `from google.colab import drive` |
| [Verified] Output types | 2 stream, 3 display_data; 0 image, 0 error | 2 stream, 3 display_data; 0 image, 0 error |
| [Verified] Serialized output size | 1,843 bytes | 1,843 bytes |
| [Verified] Error/traceback | none | none |
| [Verified] Cell metadata | `executionInfo` present; outputId differs; Colab height and referenced_widgets differ | `executionInfo` absent; outputId differs; Colab height and referenced_widgets differ |

[Verified] Output payloads at cell 122 differ, but have the same serialized size.
No output content is reproduced.

[Verified] L is 1,170,906 bytes larger than D. Serialized source and output
payload totals are equal across the files. D's raw JSON is compact (2,471,126
bytes); L's compact serialization is 2,469,858 bytes, while its stored file is
3,642,032 bytes. The 1,172,174-byte excess in L is JSON formatting whitespace;
compact metadata/content differences offset 1,268 bytes of that gap.

## Part 2 — Notebook decision memo

| Copy | Evidence for | Evidence against |
|---|---|---|
| [Reported by Jigar] D | Jigar reports this is the manually checked Drive copy and supplied its matching hash; newest local mtime; Blocks 59-62 outputs/counts match L | Local path is under `drive_backup_20261107`; cell 122 output and metadata differ from L; local inspection does not independently verify cloud state |
| [Verified] L | Same 169-cell source and same Block 59-62 outputs/counts as D | Older mtime; no supplied evidence that L is the selected Drive/submission copy; cell 122 output differs from D |
| [Verified] F | 167 cells and same source for 167 matched cells; useful historical snapshot | Oldest mtime; Blocks 59-62 have no saved outputs; treat archive-only |

[Proposed] Candidate: **D**, based on Jigar's report that it is the manually
checked Drive copy and its latest local mtime. Before treating it as final, Jigar
must confirm: (1) D is the submission notebook; (2) the cell 122 output difference
from L is expected; and (3) L and F should remain retained as local/archive copies.
No notebook was changed or moved.

## Part 3 — Block 59 policy-hash guard

[Proposed] Exact diff only; not applied (Phase 2 item):

```diff
 assert ref_data.get("a_predict_sha256") == loaded_hash, "A_predict.py hash mismatch"
+assert ref_data.get("policy_sha256") == hashlib.sha256(open(f"{V2}/A_abstain_policy_v2.json", "rb").read()).hexdigest(), "A_abstain_policy_v2.json hash mismatch"
```

## Part 4 — File structure dry run

[Verified] Inventory: 101 files, excluding backup folders and Phase_0/Evidence.
96 files have SHA-256 values. Five test-named artifacts are metadata-only; no hash
or contents were read for them. See `FILE_STRUCTURE_PLAN.csv` for every path,
size, mtime, role, classification, reason, and Stage B status.

| Classification | Count |
|---|---:|
| [Verified] KEEP-CANONICAL | 3 |
| [Verified] KEEP-REFERENCED | 54 |
| [Verified] QUARANTINE-DUPLICATE | 0 |
| [Verified] QUARANTINE-STALE | 0 |
| [Verified] PROTECTED | 30 |
| [Verified] BLOCKED-NEEDS-DECISION | 14 |

[Verified] Metadata-only test artifacts (not opened or hashed):

| Path | Size | LastWriteTime |
|---|---:|---|
| `project_s_qa/A_submission_v2/reports_v2/A_handtests_v2.csv` | 548 | 2026-11-06 03:33:56 +05:30 |
| `project_s_qa/A_submission_v2/reports_v2/A_table_test_v2.csv` | 667 | 2026-11-06 03:33:57 +05:30 |
| `project_s_qa/A_submission_v2/reports_v2/A_test_access_log_v2.json` | 393 | 2026-11-06 03:33:57 +05:30 |
| `project_s_qa/A_submission_v2/reports_v2/A_test_results_v2.csv` | 2,287 | 2026-11-06 03:33:57 +05:30 |
| `project_s_qa/A_submission_v2/reports_v2/A_test_scored_v2.parquet` | 195,541 | 2026-11-06 03:33:57 +05:30 |

### Exact duplicates and keepers

| Status | SHA-256 | Duplicate paths | Keeper/evidence |
|---|---|---|---|
| [Verified] | `78852eb405819de017fa99a3839cc47912ed1bd40acd0bd0a3966be4b6987e3b` | `block60/cbse_demo_questions_v1.csv`; `project_s_qa/processed/cbse_demo_questions_v1.csv`; upload staging copy | Keep the first two for source and runtime paths; the staging copy remains protected data. |
| [Verified] | `ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053` | root reports_v2, package reports_v2, package demo A_predict.py | Runtime-path candidate is root reports_v2; retain package copies. No canonical A_predict copy is designated. |
| [Verified] | `a4b7f45a12f1a4de8c256ee2634de2fc10f06c2b664ff74eb500b2d730e5a5ab` | root reports_v2, package reports_v2, upload staging A_negation CSV | Keep runtime root and package copy; staging copy is protected control data. |
| [Verified] | `057e3decd03aca99c804d4408caa6a5832b44f0dc18de67cfd6061e5c966e875` | root interim and upload staging combiner | Keep root interim runtime copy; model files are protected. |
| [Verified] | `216493152a1b7ae2143f0fc60ce2eed6ffc735f40676e308455225b1b55aa96f` | root interim and upload staging pooled LR | Keep root interim runtime copy; model files are protected. |
| [Verified] | `8c906f8eb778d92ec953d68975285af55c12092bed2c7151f6b42034e3919416` | root interim and upload staging config.json | Keep root interim runtime copy; model files are protected. |
| [Verified] | `671e70acf931c6dedd28ebff73baccfa3acf3b07dba13cb3eb15fc39f04761fd` | root interim and upload staging model.safetensors | Keep root interim runtime copy; model files are protected. |
| [Verified] | `ef73668535466d56fd3571306556bcbf3c3d16fd93cdf5e4d38970290c89165b` | root interim and upload staging tokenizer.json | Keep root interim runtime copy; model files are protected. |
| [Verified] | `aa6a8a3f069d2d98c09444ee3f9671d64c29ce647473dccd78169b10c490d359` | root interim and upload staging tokenizer_config.json | Keep root interim runtime copy; model files are protected. |

[Verified] No exact-duplicate group is safe to quarantine under the protection and
reference rules. Near-duplicate names: D/L/F share the COPY_UPDATED basename but
have different hashes; the F notebook and upload staging directory are also
named by the `some files to fix` path. Notebook moves are blocked until D is
confirmed. No other outside-Evidence scratch/temp/checkpoint-of-checkpoint path
was identified by the inventory name scan.

### Before/after tree

[Verified] Before (101 in-scope files; subdirectories summarized):

```text
Project 4/
  .AI/                  archive/              block60/
  notebooks/            project_s_qa/          some files to fix/
  tools/                root project/docs
  drive_backup/         project backup/        Project_S_QA_Evidence/
```

[Proposed] Target (no moves performed; blocked changes marked):

```text
Project 4/
  AGENTS.md  PROJECT_CONTEXT.md  README_FILES.txt  README.md  .gitignore
  docs/ [BLOCKED: root references and protected docs]
  notebooks/ [D candidate pending confirmation; keep reference/ and backups/]
  project_s_qa/
    reports_v2/ [KEEP existing runtime path]
    processed/  [PROTECTED]
    interim/    [PROTECTED; do not rename to models/]
    A_submission_v2/ [KEEP packaged Pair A]
    demo/ [BLOCKED: moving scorer here breaks notebook import/path]
  archive/ block60/ tools/ .AI/ [retain until individually approved]
  data/ models/ [no move: no path-safe reorganization approved]
```

[Verified] Path references that a structural move would break (all such moves are
BLOCKED):
- Notebook root `/content/drive/MyDrive/project_s_qa`: code cells 22, 27, 29, 36,
  58, 65, 68, 72, 74, 78, 80, 82, 86, 88, 90, 93, 95, 97, 100, 102, 104, 108,
  110, 112, 116, 118, 120, 122, 125, 127, 131, 133, 135, 139, 141, 143, 145,
  148, 150, 153, 155, 157, 159, 166, 167.
- Notebook A_predict imports/copies/checks are in cells 118, 123, 125, 139, 157,
  163, and 167; reference JSON reads are in cells 118, 127, 139, 157, 163, 167.
  Policy reads/writes use
  `reports_v2/A_abstain_policy_v2.json` in cells 86, 90, 104, 112, 116, 131, 133,
  135, 143, 145, 148, 150, 155, 166.
- Notebook control CSV `reports_v2/A_negation_paraphrase_v2.csv`: cells 141, 161,
  166. CBSE input `processed/cbse_demo_questions_v1.csv`: cell 159.
- Notebook model paths include `interim/combiner_v1.joblib` (cells 52, 62, 82, 86)
  and `interim/pooled_lr_v2.joblib` (cells 100, 112); `ft_distilroberta_v1` is
  resolved under `interim` by A_predict.py.
- A_predict.py lines 9-10 derive `interim`, `reports_v2`, and
  `ft_distilroberta_v1` from the project root; lines 35, 106, and 140 load the
  combiner, pooled LR, and sibling policy. Moving A_predict.py to `demo/` breaks
  notebook imports and its sibling-path assumptions.
- README_FILES.txt paths at lines 20, 25, 29, 34, 41, 46, 52, 57, 62, 67, and 72
  are inventory references; moving those files breaks the guide.

[Proposed] Exact Stage B move list: **none**. No item is both unprotected,
unreferenced, and supported by a confirmed keeper. The CSV has blank move source
and destination fields. If approved later, every move requires a fresh hash check.

[Proposed] Restore manifest format for any future approved quarantine move:
`original_path,new_path,sha256,reason,move_time,status`.

## Part 5 — Phase 0 closure checklist

| Item | Status | Evidence |
|---|---|---|
| Drive backup | PARTIAL | [Reported by Jigar, hashes supplied] D is his manually checked Drive copy; complete Drive-folder hash comparison remains unverified here. |
| Staged pair inspected | DONE-evidenced | Local scorer and both JSON/policy copies inspected and hashed in earlier Phase 0 reports. |
| Staged vs current SHA comparison | DONE-evidenced | Scorer hashes match; JSON versions have distinct hashes; policy behavior differs only by creation timestamp. |
| No-overwrite rule | DONE-evidenced | No source files overwritten; this stage created only Phase 0 plan files. |
| Drive-not-accessible rule | PARTIAL | [Reported by Jigar, hashes supplied] manual Drive check; live state not independently accessed. |
| `scorer_mode=pooled` | DONE-evidenced | Both JSON copies contain pooled. |
| JSON scorer hash matches A_predict.py | DONE-evidenced | Both JSONs store the local scorer's matching hash. |
| Notebook candidate confirmed | PARTIAL | D recommended; Jigar's explicit submission-candidate confirmation is pending. |
| 162-cell reference (non-blocking) | BLOCKED | Not found at expected path; T3 remains non-blocking per roadmap. |
| T3, backup chain, README | PARTIAL | Reference absent; backups inventoried in earlier reports; README count is stale and its edit is deferred. |

[Verified] Checklist totals: 5 DONE-evidenced, 4 PARTIAL, 1 BLOCKED, 0 UNVERIFIED.
[Proposed] Phase 0 is not fully closed until Jigar confirms D as submission
candidate and confirms the complete Drive backup status. The absent reference is
non-blocking; no Phase 1 or Phase 2 work is started here.

[Verified] Inventory hashes are in `FILE_STRUCTURE_PLAN.csv`. This report contains
no self-hash.
