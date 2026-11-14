# Project S Phase 0 Completion Report

All findings below are labelled. No saved notebook outputs or test data were opened.

## 1. Policy file diff

| Status | Evidence |
|---|---|
| [Verified] Staged policy | Extracted in memory-safe manner from `archive/project_s_qa_phase1_v1.zip` to the Phase 0 scratch directory; 784 bytes; SHA-256 `babf76f460d2a6516d9ef11d317f69ceddb0958dd67a2ce06d3b67496163ad25`. |
| [Verified] Packaged policy | `project_s_qa/A_submission_v2/reports_v2/A_abstain_policy_v2.json`; 784 bytes; SHA-256 `b6548edeb682eabd2ba6b74d9b9b67bff293c1fea9c3cb6345e0a7ebf7e9ef9b`. |
| [Verified] Scratch copies | Both policy copies are under `Project_S_QA_Evidence/Phase_0/scratch/policy_compare_20261107_160707/`; original files were untouched. |

[Verified] Unified diff (staged to packaged):

```diff
--- staged_policy.json
+++ packaged_policy.json
@@ -3,7 +3,7 @@
   "status": "final",
   "version": "v2",
-  "created": "2026-10-24T13:22:20",
+  "created": "2026-10-30T09:18:42",
   "scorer_mode": "pooled",
```

[Verified] The only policy content difference is the `created` timestamp. Thresholds,
labels, ordering, coverage rules, and wording are unchanged. The files are
behaviorally identical by their policy fields: the difference cannot change a
score, confidence, 0.64 threshold behavior, or review flag.

## 2. Which policy the code uses

| Status | Evidence |
|---|---|
| [Verified] A_predict policy lookup | `A_predict.py` line 140 constructs `V2 + "/A_abstain_policy_v2.json"`; line 141 loads that sibling file when present, otherwise uses `PROVISIONAL_POLICY`. |
| [Verified] Local staged scorer path | `project_s_qa/reports_v2/A_predict.py` has the expected hash, but its sibling policy file is absent. Static code therefore selects provisional policy in that local folder. Runtime behavior was not tested. |
| [Verified] Packaged scorer path | `project_s_qa/A_submission_v2/reports_v2/` contains A_predict and the packaged policy together. |
| [Verified] Demo notebook paths | Block 60 imports from `/content/drive/MyDrive/project_s_qa/reports_v2` and reads the CSV from `project_s_qa/processed/`; Block 59 and Block 62 read `/content/drive/MyDrive/project_s_qa/reports_v2/A_demo_reference_outputs_v2.json`. They do not directly read a policy JSON. |
| [Verified] Block 59 policy hash | It checks JSON existence, `scorer_mode == "pooled"`, and `a_predict_sha256`; it does not check `policy_sha256`. |

| Artifact | Filesystem mtime | ZIP entry date |
|---|---|---|
| [Verified] Staged policy | No standalone file in root `project_s_qa/reports_v2`; archive entry date 2026-10-24 13:22:26 +05:30 | Phase 1 ZIP `reports_v2/A_abstain_policy_v2.json` |
| [Verified] Packaged policy | 2026-11-06 03:33:57 +05:30 | submission ZIP entry date 2026-10-30 09:18:48 +05:30 |
| [Verified] Staged JSON | 2026-11-06 00:02:08 +05:30 | Phase 1 ZIP entry date 2026-10-24 14:31:06 +05:30 |
| [Verified] Packaged JSON | 2026-11-06 03:33:57 +05:30 | submission ZIP entry date 2026-10-30 09:20:12 +05:30 |

[Verified] The packaged pair is newer by embedded creation time and ZIP entry dates.
Filesystem mtimes reflect later local staging and are not treated as cloud timestamps.

## 3. Canonical pair decision

| Option | Evidence for | Evidence against |
|---|---|---|
| [Verified] A: packaged JSON + packaged policy | Newer embedded dates; hashes match the extracted packaged policy and scorer; files are co-located in the package. Policy behavior matches staged policy. | Package pair is nested under `A_submission_v2/`, while the notebook uses root `project_s_qa/reports_v2/`. |
| [Verified] B: staged JSON + staged policy | Staged JSON is at the notebook's expected root path; scorer mode/hash match. Policy content is behaviorally identical to A. | Staged policy exists in the Phase 1 archive, not as a standalone root runtime file. |
| [Proposed] C: neither | Avoids selection if provenance is considered insufficient. | The policy diff shows only a timestamp; the packaged pair has the stronger recency and local-pair evidence. |

[Proposed] Recommendation: **A, the packaged JSON + packaged policy**, because it is the newer, hash-consistent pair and the policy behavior is identical. Before Phase 2, Jigar must approve using this pair and approve a non-overwriting placement plan for the notebook's root runtime path. If a destination already exists, compare hashes and obtain explicit replacement approval first. Also approve adding the one-line Block 59 policy-hash guard shown below before execution. No pair was moved or replaced here.

## 4. Block 59 weakness

[Proposed] Proposed one-line check only; not applied:

```python
assert ref_data.get("policy_sha256") == hashlib.sha256(open(f"{V2}/A_abstain_policy_v2.json", "rb").read()).hexdigest(), "A_abstain_policy_v2.json hash mismatch"
```

## 5. Cell count and README reconciliation

| Status | Finding |
|---|---|
| [Verified] `COPY_UPDATED` | 169 cells, not 167. The `before_phase5` backup has 165. |
| [Verified] Two cells explaining the stated 167-vs-165 difference | Cell 1: `### Run history note (30 Oct 2026)`; cell 151: `### Block 56: withdrawn`. Neither is a Block 59-62 addition. |
| [Verified] Two further cells in the actual 169-cell file | Cell 167: `import os, json, hashlib, importlib.util`; cell 168: blank code cell. These are after Summary; neither is a Block 59-62 block. |
| [Verified] Blocks 59-62 | Already present in the 165-cell `before_phase5` backup; not the source of its count increase. |
| [Verified] Reference/T3 | The 162-cell reference is absent at the expected path. T3 is not blocking per the roadmap. |

[Verified] Stale README_FILES.txt lines:
- Line 21: says the working COPY has 165 cells; the file has 167.
- Lines 68 and 74: say the ZIPs were not opened; archive entries were inspected for policy hashes.

[Unverified] Line 22's “upload THIS to Colab” is ambiguous because a separate
`COPY_UPDATED` exists and no final Colab/Drive source choice is confirmed.
README_FILES.txt was not edited; its correction belongs to Phase 6.

## 6. Hash registry

[Verified] `PHASE_0_HASH_REGISTRY.csv` contains the requested roles, paths, byte
sizes, mtimes, SHA-256 values, and evidence status. The four supplied report
hashes were recomputed and match. No hash was placed inside its own report.

## 7. Manual Drive checklist

[Unverified] Live Google Drive is not locally accessible; no cloud state is claimed.
Jigar's manual check:
1. Back up `My Drive/project_s_qa/` to a new dated folder; do not overwrite.
2. Compare SHA-256 for `reports_v2/A_predict.py`, staged and packaged
   `A_demo_reference_outputs_v2.json`, and the selected notebook.
3. Record each Drive path, size, SHA-256, timestamp/status, and whether it matches
   the local registry. Report the result before treating Drive as verified.

## 8. Phase 0 closure checklist

| Roadmap checkbox | Status | Evidence |
|---|---|---|
| Back up Drive `project_s_qa/` | PARTIAL | Local project backup is verified; live Drive backup/sync remains unverified. |
| Inspect staged pair | DONE-evidenced | Staged A_predict and JSON metadata/hash/config inspected. |
| Compare staged vs current; record SHA-256 | DONE-evidenced | Scorer hashes match; JSON hashes differ; policy diff is timestamp-only. |
| Do-not-overwrite rule | DONE-evidenced | No existing file was overwritten. |
| Drive-not-accessible rule | DONE-evidenced | Live Drive explicitly remains UNVERIFIED; no cloud claim was made. |
| Verify `scorer_mode=pooled` | DONE-evidenced | Both JSONs contain pooled. |
| Verify JSON scorer hash matches A_predict.py | DONE-evidenced | Both JSONs store the matching scorer hash. |
| Confirm notebook candidate | PARTIAL | Local COPY and COPY_UPDATED identified; final Colab/Drive candidate not confirmed. |
| 162-cell reference | BLOCKED | Not found at expected path; roadmap says this does not block T3 status reporting. |
| T3, backup chain, README | PARTIAL | Backups were counted; T3 comparison is blocked by missing reference; README has stale lines. |

[Verified] Checklist totals: 6 DONE-evidenced, 3 PARTIAL, 1 BLOCKED, 0 UNVERIFIED.
[Proposed] Phase 0 is not fully evidence-closed until Jigar confirms the Drive
backup/current cloud files and selects the notebook candidate. The missing 162-cell
reference is not a blocker under the roadmap. README changes are deferred to Phase 6.
