# Phase 0 Notebook Identification

All claims are labelled. Notebook JSON was read for structure, source, and requested
output-status comparisons. No test output content is reproduced.

## 1. Fingerprints

| File | Size (bytes) | LastWriteTime | SHA-256 | Cells / code / markdown | nbformat |
|---|---:|---|---|---|---|
| [Verified] D: `drive_backup_20261107/project_s_qa/notebooks/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb` | 2,471,126 | 2026-11-07 16:19:41 +05:30 | `37170a8b10dd590c300198bb45a5543b829d4a723443d2268e49a2375a8876c5` | 169 / 70 / 99 | 4.0 |
| [Verified] L: `notebooks/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb` | 3,642,032 | 2026-11-06 02:56:12 +05:30 | `f2e2a4a5fdd7beaa208a192f6101ec9cb40789400b0d823003554fb1f4aabd4d` | 169 / 70 / 99 | 4.0 |
| [Verified] F: `some files to fix/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb` | 2,687,055 | 2026-11-06 01:01:51 +05:30 | `a35efc489c25806f2ad3db8684006dc2d627634dc1e6d2a61d3fbc75c615030e` | 167 / 68 / 99 | 4.0 |

[Verified] Each recomputed SHA-256 matches the hash supplied in the request.
[Verified] No same-named notebook exists anywhere inside
`project_s_qa_backup_20261106_1957`.

## 2. Cell-level comparison

Cells were aligned by heading and first source line, not by assumed index.
“Identical” means identical source text for matched cells.

| Pair | Identical source | Changed source | Added | Removed |
|---|---:|---:|---|---|
| [Verified] D vs L | 169 | 0 | none | none |
| [Verified] L vs F | 167 | 0 | L-only: cell 167 `import os, json, hashlib, importlib.util`; cell 168 blank code cell | none |
| [Verified] D vs F | 167 | 0 | D-only: cell 167 `import os, json, hashlib, importlib.util`; cell 168 blank code cell | none |

| Pair | Output differences | execution_count differences | Other metadata |
|---|---|---|---|
| [Verified] D vs L | cell 122 | cells 118, 122, 155 | notebook metadata differs |
| [Verified] L vs F | cells 157, 159, 161, 163 | cells 157, 159, 161, 163 | notebook metadata differs |
| [Verified] D vs F | cells 122, 157, 159, 161, 163 | cells 118, 122, 155, 157, 159, 161, 163 | notebook metadata differs |

[Verified] All reported pairwise differences are outputs and/or execution or notebook
metadata; no matched cell has a source change. D and L have the same source and cell
structure. F has two fewer trailing cells.

## 3. Blocks 59-62 stored state

| Copy | Block | Source present | Cell | execution_count | Outputs stored | Error output |
|---|---:|---|---:|---:|---|---|
| [Verified] D | 59 | yes | 157 | 2 | yes | no |
| [Verified] D | 60 | yes | 159 | 3 | yes | no |
| [Verified] D | 61 | yes | 161 | 4 | yes | no |
| [Verified] D | 62 | yes | 163 | 5 | yes | no |
| [Verified] L | 59 | yes | 157 | 2 | yes | no |
| [Verified] L | 60 | yes | 159 | 3 | yes | no |
| [Verified] L | 61 | yes | 161 | 4 | yes | no |
| [Verified] L | 62 | yes | 163 | 5 | yes | no |
| [Verified] F | 59 | yes | 157 | none | no | no |
| [Verified] F | 60 | yes | 159 | none | no | no |
| [Verified] F | 61 | yes | 161 | none | no | no |
| [Verified] F | 62 | yes | 163 | none | no | no |

[Verified] D and L have identical output payloads and execution counts for Blocks 59-62.
F has no saved outputs for these blocks. No output text is reproduced.
[Verified] D, L, and F: test content present in cell 36; test content present in
cell 58; test content present in cell 60; test content present in cell 62; test
content present in cell 78; test content present in cell 82; test content present
in cell 112; test content present in cell 131; test content present in cell 150;
test content present in cell 155. All such content was suppressed.

## 4. Block 63

| Copy | Result |
|---|---|
| [Verified] D | Block 63 absent |
| [Verified] L | Block 63 absent |
| [Verified] F | Block 63 absent |

## 5. Frozen-cell source check

[Verified] `PHASE_0_VERIFICATION_REPORT_v2.md` classifies blocks as FROZEN,
SAFE-TO-RERUN, or RERUN-WITH-BACKUP. Source comparison found no changes in any
matched cell, including cells belonging to blocks classified FROZEN. The only
unmatched cells relative to F are D/L's two trailing cells listed above; they are
not frozen-block cells. No notebook was changed during this check.

## 6. Cell-count reconciliation

| Copy/state | Cells | Explanation |
|---|---:|---|
| [Verified] Earlier `before_phase5` backup | 165 | Baseline backup; not one of D, L, or F |
| [Verified] F | 167 | The two cells relative to that baseline are cell 1 `### Run history note (30 Oct 2026)` and cell 151 `### Block 56: withdrawn` |
| [Verified] D and L | 169 | F's two cells plus cell 167 `import os, json, hashlib, importlib.util` and cell 168, a blank code cell |

[Verified] The earlier expectation that COPY_UPDATED had 167 cells is incorrect for D
and L; both contain 169. The two Block 59-62 cells are not the count difference:
Blocks 59-62 already exist in F and in the 165-cell backup.

## 7. Recommendation

| Copy | Evidence for | Evidence against |
|---|---|---|
| [Verified] D | Newest filesystem mtime; 169 cells; same Block 59-62 outputs as L | D vs L has an output difference at cell 122 and execution/metadata differences; later file mtime does not prove later Colab execution |
| [Verified] L | 169 cells; same source and Block 59-62 outputs as D | Older filesystem mtime; same unresolved output/metadata provenance difference at cell 122 |
| [Verified] F | 167 cells; earlier snapshot | Oldest mtime; no saved outputs for Blocks 59-62; lacks two trailing cells |

[Verified] D and L are tied as structural supersets of F: they have the same 169-cell
source layout, while F has the same 167 matched source cells. D has the newest file
mtime and F the oldest. The latest saved Block 59-62 output content is tied between
D and L; their output payloads and execution counts match. F has no saved outputs.
[Unverified] A file mtime does not establish when its cell outputs were produced.
[Proposed] Recommendation: cannot decide between D and L as submission candidate
without Jigar confirming which provenance/output at cell 122 is authoritative.
F is the older, no-Block-59-62-output copy.

## 8. Approval needed next

[Proposed] Jigar should approve which of D or L is the submission candidate, then
explicitly approve whether the other copies should be retained, renamed, or archived.
No file should be moved, renamed, merged, or deleted before that approval.

[Verified] No notebook, model, training, or Project S script was executed; no package
was installed; no file was moved, overwritten, or deleted. No test split was opened.
