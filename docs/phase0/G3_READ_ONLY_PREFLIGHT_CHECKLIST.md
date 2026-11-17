# G3 read-only Colab preflight checklist

**Status: PENDING USER-RUN VERIFICATION.** This checklist performs no scoring,
inference, training, or file writes. Local evidence cannot establish live
Drive contents.

## Preconditions

- G1 candidate: local D snapshot, SHA-256
  `37170A8B10DD590C300198BB45A5543B829D4A723443D2268E49A2375A8876C5`.
- G2 candidate: root reference JSON and matching scratch policy, hashes
  recorded in `PHASE0_PENDING_USER_DECISIONS.md`.
- Intended root from scorer source: `/content/drive/MyDrive/project_s_qa`;
  current live root is unverified.
- Do not run notebook cells, import A_predict, load models, score, install,
  download, or alter files during this preflight.

## Read-only checks and evidence to record

| Check | Local evidence | Colab evidence to record | Pass condition |
|---|---|---|---|
| Notebook identity | D local hash matches approved candidate | Hash of notebook opened in Colab | Exact approved hash |
| Runtime root | A_predict defaults to `/content/drive/MyDrive/project_s_qa`; `PROJECT_S_ROOT` may override | Print selected root and override state | Notebook setup and scorer root are the same |
| Root JSON | Local root JSON hash matches candidate | File exists; SHA-256; `scorer_mode`; declared scorer and policy hashes | Hashes and pooled mode match approved values |
| Policy path | Expected path is `reports_v2/A_abstain_policy_v2.json`; local file is missing | File exists at exact path; SHA-256; threshold and contradiction flag | Approved hash; threshold 0.64; contradiction flag false |
| Scorer policy behavior | A_predict reads the expected path; missing policy silently falls back to 0.60 | Confirm source version/hash and policy file presence without importing scorer | No fallback condition; source hash is approved |
| Local model artifacts | Top-level local root contains FT files and joblibs | Confirm each expected path exists and record hashes | Required files all present under selected root |
| Hub components | NLI and SBERT use unpinned Hub identifiers | Record whether required models are already cached; do not download | Cache availability established without download |
| Dependencies | Versions are not established by a tested lock | Record installed versions without installing | Required packages present; versions recorded |
| Execution provenance | Local notebook metadata is not proof of current runtime | Record runtime type and notebook identity only | No claim of a completed run from metadata alone |

## Expected local dependency paths

Under the selected root, check `reports_v2/A_predict.py`,
`reports_v2/A_demo_reference_outputs_v2.json`,
`reports_v2/A_abstain_policy_v2.json`, `interim/combiner_v1.joblib`,
`interim/pooled_lr_v2.joblib`, and
`interim/ft_distilroberta_v1/{config.json,model.safetensors,tokenizer_config.json,tokenizer.json}`.
NLI `cross-encoder/nli-deberta-v3-base` and SBERT
`sentence-transformers/all-MiniLM-L6-v2` are Hub-loaded; revisions and cache
availability remain unverified.

## User Colab steps

1. Mount Drive and set the root to `/content/drive/MyDrive/project_s_qa`.
2. Read-only list the required paths; compute hashes for the scorer, JSON, and
   policy; inspect the JSON mode/hash fields and policy threshold/flag.
3. Record package versions and whether the two Hub model IDs are cached; do
   not install or download.
4. Compare the notebook hash with the approved D candidate and confirm its
   setup points to the same root.
5. Save the complete preflight output for review. Stop on any missing path,
   hash mismatch, unexpected threshold, fallback risk, or root mismatch.

## Prohibited actions

Do not run notebook cells, Run All, A_predict, inference, training, scoring,
model loading, package installation, downloads, or file changes. Do not treat
local verification as proof of live Drive synchronization. Passing this
checklist does not close G1-G3 or authorize Phase 1.