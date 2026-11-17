# Gate 1 — Notebook and runtime evidence

**Status: BLOCKED.** Hashes and sizes below were recomputed locally on 15 Nov
2026. They identify local files only; they do not establish live Drive state.

| Candidate | Cells* | Size (bytes) | SHA-256 | Finding |
|---|---:|---:|---|---|
| notebooks/Jigar_Q&A_Branch_Baseline_COPY.ipynb | 167 | 2,690,082 | 5EB5DC4FD1AD85DCE55C9B1222603FC11DE19D51BB682103FC7923BC78B5FAF0 | Working copy; not selected |
| notebooks/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb | 169 | 3,642,032 | F2E2A4A5FDD7BEAA208A192F6101EC9CB40789400B0D823003554FB1F4AABD4D | Local updated candidate; not selected |
| drive_backup_20261107/notebooks/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb | 169 | 2,471,126 | 37170A8B10DD590C300198BB45A5543B829D4A723443D2268E49A2375A8876C5 | Dated snapshot, not live Drive |
| Project_S_QA_Evidence/Phase_2/Jigar_QA_PHASE2_RUN_COPY_EXECUTED.ipynb | 169 | 3,389,226 | EBB83C058F58CF724153BB897BBDB0854E5A390FBB9EB5BF0A29E885042CC787 | Local executed copy; not selected |

The cell counts and source comparison are carried forward from
PHASE0_FINAL_CLOSURE_REPORT.md; this check recomputed file hashes but did not
inspect notebook outputs. That report records source differences among
candidates, including an extra cell-157 change in the executed copy. No
notebook is authorized as the submission/runtime authority.

**Runtime root:** /content/drive/MyDrive/project_s_qa is a candidate path in
the notebook/scorer records. Current mounted Drive contents were not available
for this local audit. Required packages, model cache revisions, and live
artifact paths remain unverified.

**Needed to pass:** Jigar selects one exact notebook path/hash and runtime
root; source deltas are accepted explicitly; a live preflight confirms the
notebook import root, PROJECT_S_ROOT, and required artifacts agree.

*Cell counts are recorded in the preceding static audit, not recalculated here.
