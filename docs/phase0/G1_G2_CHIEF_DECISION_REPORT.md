# Chief Decision Report — G1 notebook and G2 configuration

**Phase 0 status: OPEN. G1 and G2 verdicts: BLOCKED BY MISSING EVIDENCE.**
The five independent reviewers support a local-candidate recommendation but
do not support an authoritative or live selection. Weighted criteria do not
override missing runtime/path evidence. The accompanying scorecard therefore
has no aggregate passing score.

Scorecard ratings are CDO judgments on observed evidence, not measured
performance: 0 means contradicted/absent, 5 means partial evidence, 8 means
strong local evidence with a known limitation, and 10 means verified for the
local criterion. Other numeric values indicate intermediate evidence/risk.
Blank scores mean the critical criterion is blocked or unknown; no weighted
total is calculated with those gaps.

## Decision summary

| Gate | Best-supported local candidate | Verdict | Is it selected/operational? |
|---|---|---|---|
| G1 | D snapshot `drive_backup_20261107/notebooks/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb`, SHA `37170A8B10DD590C300198BB45A5543B829D4A723443D2268E49A2375A8876C5` | BLOCKED BY MISSING EVIDENCE | No. D is a dated local snapshot, not live Drive; Jigar's G1 decision remains deferred. |
| G2 | Packaged JSON `EA5288E9F12B25D28A66F36EC38D48B08C65E19452BF3B5EFA17EED2BE20AEB9` + policy `B6548EDEB682EABD2BA6B74D9B9B67BFF293C1FEA9C3CB6345E0A7EBF7E9EF9B` | BLOCKED BY MISSING EVIDENCE | No. Pair is locally hash-consistent, but its nested root lacks `interim/`, and it is not approved/live. |

## Five-agent reconciliation

1. **Notebook forensics:** D is the strongest local reference; updated local
   source was reported identical. Executed copy differs at cell 157; that
   delta is unapproved. Counts/source comparisons were not re-parsed here.
2. **Systems architecture:** no operationally coherent root is verified.
   Top-level root has interim artifacts but misses the expected policy path;
   nested package has JSON/policy but no interim artifacts.
3. **Data/configuration integrity:** packaged pair declarations match local
   hashes and scorer hash. Root JSON policy bytes are found in scratch, not at
   the active policy path.
4. **ML reproducibility:** model Hub revisions/cache and package versions are
   unverified; execution counts do not prove which files were loaded.
5. **Adversarial evaluation:** local snapshots are not live evidence; the
   scorer's missing-policy fallback can silently change the review threshold.

## Adversarial objections and unknowns

- No notebook is explicitly authorized; no live Drive notebook hash is
  available.
- Cell counts/source comparisons are carried forward from the closure report;
  notebook outputs were not inspected or used here.
- The executed copy's cell-157 source patch is unapproved. It must not be
  assumed safer without source-boundary review.
- No live runtime confirms the project root, model artifacts, policy path,
  Hub revisions, or installed package versions.
- A hash-consistent config pair does not make its directory an operational
  runtime. Conversely, a local root with models but no policy can invoke the
  scorer's 0.60 provisional fallback.

## What G3 requires

1. Jigar selects the exact notebook path/hash and runtime root.
2. Jigar selects the JSON/policy hashes and their runtime paths; separately
   authorize any staging. Ensure the policy is present where A_predict reads
   it and verify the declared hashes.
3. Run the existing read-only Colab preflight and preserve its complete
   output. No scoring/training is included in this step.
4. Resolve every failed path/hash/model-cache/environment check before any
   later runtime execution.

**User approval remains required.** D0-2, D0-3, and D0-4 remain deferred in
`PHASE0_PENDING_USER_DECISIONS.md`. This report recommends candidates but does
not change those statuses. G3 is still blocked. No files were staged and no
production artifact was modified.
