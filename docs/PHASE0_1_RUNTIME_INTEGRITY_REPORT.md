# Project S — Phase 0.1 Runtime Integrity & Configuration Lock

**Inspection date:** 15 Nov 2026  
**Scope:** local, read-only inspection plus this new report only. No Project S
script, notebook cell, model, training, or inference was run; local shell
metadata/hash queries and JSON metadata parsing were used. No notebook output,
test file/split, ZIP, PDF, or live service was inspected. Notebook cell sources
and metadata were examined; output values were not accessed or printed.

## 1. Executive verdict

**PHASE 0.1 NOT COMPLETE. PHASE 0 REMAINS OPEN.** A dated local snapshot has a
locally hash-consistent scorer/JSON/policy set and the required local model and
demo inputs. The current local `project_s_qa/` root has the scorer and interim
artifacts but lacks the expected policy and has a JSON that references an
unavailable policy hash. Live Google Drive is **NOT VERIFIED**. No notebook
candidate verifies the reference JSON file's own SHA-256, and there is no
approved notebook/runtime-root selection.

**Recommended notebook:** `NO AUTHORITATIVE NOTEBOOK ESTABLISHED`.  
**Recommended configuration option:** Option B is the best-supported local
candidate, not a deployed choice: use the packaged JSON/policy pair at the
top-level runtime paths only after Jigar approves and the live paths are
verified. No file was staged or changed.

## 2. Investigation scope and method

Read `AGENTS.md`, `PROJECT_CONTEXT.md`, and all six required Phase 0 documents:
`REPOSITORY_AUDIT.md`, `SOURCE_OF_TRUTH.md`,
`IMPLEMENTATION_GAP_ANALYSIS.md`, `FILE_CHANGE_PLAN.md`,
`PHASE0_EVIDENCE_REVIEW.md`, and `PHASE0_DECISION_RECORD.md` under `docs/`.
Inspected Git status before writing. It showed pre-existing untracked archives,
scratch files, and the six existing reports; they were left unchanged. Existing
ignored model/test artifacts were not opened.

Notebook metadata came from JSON cell counts, cell types, source text, and
`execution_count` only. `outputs` were not inspected. Scorer source was read as
text only. JSON configuration files were parsed for metadata fields only;
their `cases` arrays were not read. Hashes were computed from the listed local
files. No ZIP/PDF content or test data was accessed. No live Drive or external
service was queried. **Confidence:** high for local hashes/source; none for
live Drive state or runtime execution.

## 3. Notebook comparison

| Candidate | Local path | SHA-256 | Cells (code/markdown) | Exec-count metadata | Relevant cells |
|---|---|---|---:|---:|---|
| Working COPY | `notebooks/Jigar_Q&A_Branch_Baseline_COPY.ipynb` | `5EB5DC4FD1AD85DCE55C9B1222603FC11DE19D51BB682103FC7923BC78B5FAF0` | 167 (68/99) | 0 non-null | 157, 159, 161, 163 |
| Updated local | `notebooks/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb` | `F2E2A4A5FDD7BEAA208A192F6101EC9CB40789400B0D823003554FB1F4AABD4D` | 169 (70/99) | 5 non-null | 157, 159, 161, 163 |
| Dated Drive snapshot | `drive_backup_20261107/notebooks/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb` | `37170A8B10DD590C300198BB45A5543B829D4A723443D2268E49A2375A8876C5` | 169 (70/99) | 8 non-null | 157, 159, 161, 163 |
| Phase 2 executed-named copy | `Project_S_QA_Evidence/Phase_2/Jigar_QA_PHASE2_RUN_COPY_EXECUTED.ipynb` | `EBB83C058F58CF724153BB897BBDB0854E5A390FBB9EB5BF0A29E885042CC787` | 169 (70/99) | 4 non-null | 157, 159, 161, 163 |
| Same executed file with double suffix | `Project_S_QA_Evidence/Phase_2/Jigar_QA_PHASE2_RUN_COPY_EXECUTED.ipynb.ipynb` | `EBB83C058F58CF724153BB897BBDB0854E5A390FBB9EB5BF0A29E885042CC787` | 169 (70/99) | same bytes as above | duplicate |

All notebook files are nbformat 4. Non-null execution counts are metadata,
not proof that the intended files were loaded or that a run succeeded. No
outputs were checked.

### Cell 157 source comparison

Updated local and D have identical cell source. D versus the Phase 2
executed-named copy differs only at cell 157. The executed copy adds a
Drive-mount `try/except` and this exact policy preflight after the scorer-hash check:

```text
D, cell 157 line 5: drive.mount("/content/drive")
Executed, cell 157 lines 5–8:
try:
    drive.mount("/content/drive")
except Exception as e:
    print("Drive mount skipped or already active:", e)
Executed, cell 157 lines 28–33:
policy_path = f"{V2}/A_abstain_policy_v2.json"
if not os.path.isfile(policy_path):
    raise FileNotFoundError(f"Missing: {policy_path}")
policy_hash = hashlib.sha256(open(policy_path, "rb").read()).hexdigest()
if ref_data.get("policy_sha256") != policy_hash:
    raise ValueError("A_abstain_policy_v2.json hash mismatch")
```

The unchanged cell 157 source in D/updated points to
`/content/drive/MyDrive/project_s_qa/reports_v2/A_demo_reference_outputs_v2.json`,
imports `A_predict` after adding that `reports_v2` directory to `sys.path`,
requires JSON existence and `scorer_mode == "pooled"`, then checks the loaded
`A_predict.__file__` digest against `a_predict_sha256`. It does **not** hash the
reference JSON file itself or check `policy_sha256`.

The executed-named cell 157 also does **not** hash the JSON file itself; it
checks the scorer hash and checks the policy file digest against the JSON's
`policy_sha256`. The mount exception is printed and swallowed; later file
checks still fail if the configured files cannot be reached. It does not
verify that a mounted Drive is the intended account or that the module's
`PROJECT_S_ROOT` equals the notebook's hard-coded `ROOT`.

D and updated source match at every index. D versus the 167-cell working COPY
has source differences at cells 12, 26, 48, 84, 106, 114, and 164; D also has
two additional cells at indices 167 and 168. The working COPY is therefore
not source-identical to D. The cell roles are: Block 59 heading/code 156/157;
Block 60 heading/code 158/159; Block 61 heading/code 160/161; Block 62
heading/code 162/163. The double-suffix executed notebook is byte-identical
to the Phase 2 executed-named file.

### Candidate criteria

| Criterion | D and updated | Phase 2 executed-named copy | Evidence / limitation |
|---|---|---|---|
| Checks scorer hash | Yes | Yes | Cell 157 compares JSON `a_predict_sha256` with loaded scorer bytes. |
| Checks reference JSON file hash | No | No | Neither computes the JSON file's own SHA-256. |
| Checks policy file hash | No | Yes | Executed cell 157 only. |
| Missing JSON / non-pooled mode | Raises/asserts | Raises/asserts | Cell 157; no execution performed. |
| Missing/mismatched policy | Not checked in cell 157; scorer falls back if missing | Explicit missing-file/hash errors | `A_predict.py:139–141`; executed cell 157. |
| Paths compatible with proposed root | Conditional | Conditional | Notebook hard-codes `/content/drive/MyDrive/project_s_qa`; live contents unknown. |
| Imports intended scorer | Intended top-level `reports_v2` | Intended top-level `reports_v2` plus digest check | Fresh-runtime origin still unverified. |
| Preserves frozen baseline | Source-only cells read/check; no edits made | Same | Whole notebook remains unsafe to Run All under project rules. |

No candidate satisfies all requested verification criteria. The executed copy
is stronger on policy hash checking, but it has a source patch relative to D,
swallows the mount exception, and still does not hash the reference JSON.
Execution metadata cannot certify provenance. **Decision: NO AUTHORITATIVE
NOTEBOOK ESTABLISHED.**

## 4. Scorer comparison

The notebook's intended local import is the top-level
`project_s_qa/reports_v2/A_predict.py`. Thirteen `A_predict.py` files were
found; all have size 7,626 bytes and SHA-256
`CA7C2752A4863F2A24B20EC7CD9000B651D83A0CFC39709F0080EBCBDAD0A053`:

- `project_s_qa/reports_v2/A_predict.py`
- `project_s_qa/A_submission_v2/reports_v2/A_predict.py`
- `project_s_qa/A_submission_v2/demo/A_predict.py`
- `drive_backup_20261107/reports_v2/A_predict.py`
- `drive_backup_20261107/demo/A_predict.py`
- `drive_backup_20261107/project_s_qa_v2_package/reports_v2/A_predict.py`
- `drive_backup_20261107/project_s_qa_v2_package/demo/A_predict.py`
- `project_s_qa_backup_20261106_1957/reports_v2/A_predict.py`
- `project_s_qa_backup_20261106_1957/A_submission_v2/reports_v2/A_predict.py`
- `project_s_qa_backup_20261106_1957/A_submission_v2/demo/A_predict.py`
- `_backups/project_s_qa_20261106_001907/project_s_qa/reports_v2/A_predict.py`
- `_backups/project_s_qa_20261106_003323852/project_s_qa/reports_v2/A_predict.py`
- `PROJECT_S_QA_HANDOVER/src/A_predict.py`

`tools/extracted_A_predict.py` is a different, stale file: size 7,311 bytes,
SHA-256 `11E897C74EC415737423FE35A3E1F61FCDC9F1668702FBC98A83E08CFD5D216B`.
Its `predict_batch`/`predict` default is `scientsbank` and its allowed dataset
values omit `pooled` (`:134–139, 162`). It is not the notebook's import target.

The top-level local scorer is the best-supported **local** operational
candidate, not a verified live deployment. Source evidence:

- Root and model paths: `A_predict.py:8–10`; `PROJECT_S_ROOT` can override the
  default `/content/drive/MyDrive/project_s_qa`.
- Hub model IDs: NLI `cross-encoder/nli-deberta-v3-base` and SBERT
  `sentence-transformers/all-MiniLM-L6-v2` (`:11–12`). They load through
  `from_pretrained` / `SentenceTransformer` without pinned revisions
  (`:26,32,34`).
- Local model and legacy startup dependency: FT tokenizer/model under
  `INTERIM/ft_distilroberta_v1`, plus `combiner_v1.joblib` loaded at `:30–35`.
- Pooled joblib: `pooled_lr_v2.joblib` at `:104–107`; pooled SBERT-LR/NLI-LR
  inference at `:130–136`.
- Pooled decision: `predict_batch()` averages `ft`, `sb`, and `nl` five-class
  probabilities equally and applies `_to3` (`:152–153`; mapping at `:56–57`),
  optionally temperature-scales (`:154–157`), then argmaxes and takes the
  maximum probability as confidence (`:159–160`).
- Policy: `V2/A_abstain_policy_v2.json` at `:139–141`.
- Prediction behavior: pooled default and allowed values `:144–153`;
  temperature, confidence, and review logic `:154–170`; public single-answer
  `predict()` default `pooled` at `:176–178`.

No scorer was imported, no model artifact was loaded, and no scoring function
was run. **Conclusion:** the root scorer remains the best-supported local
candidate because the notebook imports it and its hash matches local JSON
metadata. Which bytes are live in Drive is **NOT VERIFIED**.

## 5. JSON/policy compatibility

| Local configuration root | JSON SHA-256 / validity | Mode and scorer hash | Policy path / SHA-256 | Compatibility |
|---|---|---|---|---|
| `project_s_qa/` expected root | `C99B7D84D000046C9629708D5EE440D5A20AB28FD298F63708E2E8C13F89DC92`, valid JSON | `pooled`; embedded scorer hash matches `A_predict.py` | Expected `reports_v2/A_abstain_policy_v2.json` is missing; stored hash `babf76f460d2a6516d9ef11d317f69ceddb0958dd67a2ce06d3b67496163ad25` | **Incompatible/incomplete locally.** Scorer silently falls back if called without the policy. |
| `project_s_qa/A_submission_v2/` nested package | `EA5288E9F12B25D28A66F36EC38D48B08C65E19452BF3B5EFA17EED2BE20AEB9`, valid JSON | `pooled`; scorer hash matches | `reports_v2/A_abstain_policy_v2.json`, `B6548EDEB682EABD2BA6B74D9B9B67BFF293C1FEA9C3CB6345E0A7EBF7E9EF9B`; hash matches | Pair consistent, but package has no `interim/`; not a complete scorer root. |
| `drive_backup_20261107/` snapshot root | Same `EA5288…20AEB9`, valid JSON | `pooled`; scorer hash matches | Top-level policy `B6548E…F7E9EF9B`; hash matches | **Locally complete candidate snapshot**: scorer, paired JSON/policy, interim, processed CSV and Block 61 CSV present and hashes match corresponding local project artifacts. This is a dated local backup, not live Drive. |
| `drive_backup_20261107/project_s_qa_v2_package/` | Same packaged JSON SHA, valid | `pooled`; scorer hash matches | Packaged policy SHA `B6548E…F7E9EF9B`; matches | Pair consistent; nested package lacks `interim/`. |
| `project_s_qa_backup_20261106_1957/` | Contains both root `C99B…F89DC92` and nested package `EA5288…20AEB9` JSON copies | Both name the same scorer hash | Nested policy copies have `B6548E…F7E9EF9B`; root policy absent | Historical local backup only; not live state. |
| `PROJECT_S_QA_HANDOVER/src/config/` | Packaged JSON copy, SHA `EA5288…20AEB9` | `pooled`; scorer hash matches | Packaged policy copy, SHA `B6548E…F7E9EF9B` | Inspection/config copy only, not notebook import path or runtime root. |

The remaining packaged JSON copies in the local tree have the same `EA5288…`
hash; root backup copies have the same `C99B…` hash. All discovered files named
`A_abstain_policy_v2.json` have the packaged `B6548E…` hash. No local file
with that expected filename matches the root JSON's `babf76…` policy hash.

The JSON `policy` metadata object reports temperature approximately 1,
confidence threshold 0.64, and `use_contradiction_flag=false`. The scorer does
not read that embedded object: it loads the separate policy file
(`A_predict.py:139–141`). Thus embedded settings do not repair the missing
root policy. Packaged policy metadata is `status=final`, temperature 1,
confidence threshold 0.64, contradiction threshold 0.5, and contradiction
review disabled.

These evidence levels are distinct:

1. **Internally hash-consistent:** packaged JSON + packaged policy; verified
   locally. Root JSON + root policy: not consistent because root policy is
   absent.
2. **At expected local paths:** scorer, root JSON and interim exist under
   `project_s_qa/`; root policy does not.
3. **Referenced by notebook:** cells 157/159/161/163 point at top-level
   `/content/drive/MyDrive/project_s_qa/reports_v2` and `processed/`.
   Executed-named cell 157 additionally checks the policy there.
4. **Verified in live runtime:** **No.**

## 6. Fallback behavior (static source)

| Condition | Static behavior | Evidence |
|---|---|---|
| Policy absent | `_load_policy()` returns `PROVISIONAL_POLICY` silently. It sets confidence threshold 0.60 and contradiction threshold 0.5; `use_contradiction_flag` is absent and line 164 defaults it to `True`. | `A_predict.py:16–17,139–141,162–165` |
| Policy exists but its hash differs from the JSON | `A_predict.py` does not hash or compare it; it loads the policy. D/current updated cell 157 does not compare policy hashes. The Phase 2 executed cell 157 raises `ValueError` on mismatch before timing. | `A_predict.py:139–141`; executed cell 157 lines 28–33 |
| Reference JSON absent | `A_predict.py` itself does not read the reference JSON. Cell 157 asserts it exists; cell 163 attempts `json.load` and fails. Cell 159 does not read it and can call the scorer. | D/updated cell 157 lines 18–20; cell 163 source; cell 159 source |
| Reference JSON has wrong scorer mode/hash | D/updated and executed cell 157 assert pooled mode and compare the stored scorer hash with `A_predict.__file__`; failure raises. Block 60 on its own does not repeat these checks. | cell 157 lines 21–24; cell 159 source |
| Policy hash mismatch in executed copy | Explicit `ValueError`; mount-only exception handling does not wrap this check. | executed cell 157 lines 28–33 |

The current local root has no policy, so static scorer fallback would use 0.60
and enable contradiction review by default if called. This is a source-based
behavioral conclusion, not a tested runtime result. D/current cell 157 would
not detect a policy mismatch; the Phase 2 executed copy would.

## 7. Runtime root completeness

Notebook cells hard-code `/content/drive/MyDrive/project_s_qa`; cell 157 and
cell 159 add its `reports_v2` to `sys.path`. `A_predict.py:8` independently
reads `PROJECT_S_ROOT` or uses the same default, then derives `interim/` and
`reports_v2/` (`:9–10`). If that environment variable points elsewhere, the
notebook import path and scorer artifact root can diverge. No cell sets or
checks the variable.

| Dependency | Expected under proposed root | Current local `project_s_qa/` | Dated snapshot `drive_backup_20261107/` | Required / status |
|---|---|---|---|---|
| Scorer | `reports_v2/A_predict.py` | Present; SHA `CA7C…D0A053` | Present; same SHA | Required; local verified, live unverified |
| Reference JSON | `reports_v2/A_demo_reference_outputs_v2.json` | Present; SHA `C99B…F89DC92` | Present; SHA `EA528…20AEB9` | Required by Blocks 59/62; current root's policy hash conflicts |
| Policy | `reports_v2/A_abstain_policy_v2.json` | Missing | Present; SHA `B654…F7E9EF9B` | Required by intended policy; missing at current local root |
| FT model files | `interim/ft_distilroberta_v1/{config.json,model.safetensors,tokenizer_config.json,tokenizer.json}` | Present; all four file hashes recorded below | Present; all four hashes match local root | Required by `_load()`; verified locally by names/hashes, not loaded |
| Legacy base container | `interim/combiner_v1.joblib` | Present; SHA `057E…966E875` | Present; same SHA | Required: loaded unconditionally at `:35`, including pooled mode |
| Pooled LR artifact | `interim/pooled_lr_v2.joblib` | Present; SHA `2164…AA96F` | Present; same SHA | Required for pooled inference at `:104–106` |
| CBSE demo bank | `processed/cbse_demo_questions_v1.csv` | Present; SHA `7885…987E3B` | Present; same SHA | Required by Block 60; CSV not opened here |
| Negation diagnostic CSV | `reports_v2/A_negation_paraphrase_v2.csv` | Present; SHA `A4B7…E5A5AB` | Present; same SHA | Required by Block 61; CSV not opened here |
| NLI model | Hub ID `cross-encoder/nli-deberta-v3-base` | No project-local weights expected | No project-local weights expected | Required; cache/hub availability **Unverified** |
| SBERT model | Hub ID `sentence-transformers/all-MiniLM-L6-v2` | No project-local weights expected | No project-local weights expected | Required; cache/hub availability **Unverified** |
| Whisper model | Hub ID `openai/whisper-small` in Block 60 | No project-local weights expected | No project-local weights expected | Required for voice; cache/hub availability **Unverified** |

SHA-256 values for the current local root's files above (and the corresponding
files at the dated snapshot root) are:

| File | SHA-256 |
|---|---|
| `reports_v2/A_predict.py` | `CA7C2752A4863F2A24B20EC7CD9000B651D83A0CFC39709F0080EBCBDAD0A053` |
| `reports_v2/A_demo_reference_outputs_v2.json` (current root) | `C99B7D84D000046C9629708D5EE440D5A20AB28FD298F63708E2E8C13F89DC92` |
| `reports_v2/A_demo_reference_outputs_v2.json` (dated snapshot) | `EA5288E9F12B25D28A66F36EC38D48B08C65E19452BF3B5EFA17EED2BE20AEB9` |
| `reports_v2/A_abstain_policy_v2.json` (dated snapshot only) | `B6548EDEB682EABD2BA6B74D9B9B67BFF293C1FEA9C3CB6345E0A7EBF7E9EF9B` |
| `reports_v2/A_negation_paraphrase_v2.csv` | `A4B7F45A12F1A4DE8C256EE2634DE2FC10F06C2B664FF74EB500B2D730E5A5AB` |
| `processed/cbse_demo_questions_v1.csv` | `78852EB405819DE017FA99A3839CC47912ED1BD40ACD0BD0A3966BE4B6987E3B` |
| `interim/combiner_v1.joblib` | `057E3DECD03ACA99C804D4408CAA6A5832B44F0DC18DE67CFD6061E5C966E875` |
| `interim/pooled_lr_v2.joblib` | `216493152A1B7AE2143F0FC60CE2EED6FFC735F40676E308455225B1B55AA96F` |
| `interim/ft_distilroberta_v1/config.json` | `8C906F8EB778D92EC953D68975285AF55C12092BED2C7151F6B42034E3919416` |
| `interim/ft_distilroberta_v1/model.safetensors` | `671E70ACF931C6DEDD28EBFF73BACCFA3ACF3B07DBA13CB3EB15FC39F04761FD` |
| `interim/ft_distilroberta_v1/tokenizer_config.json` | `AA6A8A3F069D2D98C09444EE3F9671D64C29CE647473DCCD78169B10C490D359` |
| `interim/ft_distilroberta_v1/tokenizer.json` | `EF73668535466D56FD3571306556BCBF3C3D16FD93CDF5E4D38970290C89165B` |

The nested `project_s_qa/A_submission_v2/` package has `reports_v2/` but no
`interim/`; it cannot serve alone as `PROJECT_S_ROOT`. The top-level dated
snapshot has all above local files at matching relative paths, with JSON and
policy hashes matching each other. It is still only a local snapshot.

Blocks 59–62 do not reference original datasets or an index. Block 59 reads
the JSON demo cases; Block 60 reads the CBSE CSV and loads Whisper; Block 61
reads the negation CSV; Block 62 reads the JSON demo cases. The scorer's local
and hub artifacts are listed above. No test split was opened.

### Package and cache requirements

Static imports identify `numpy`, `joblib`, `torch`, `transformers`,
`sentence_transformers`, `pandas`, and `gradio`; the notebook also uses
`google.colab`. Standard-library imports include `os`, `re`, `json`, `sys`,
`time`, `hashlib`, and `importlib`. The persisted LR joblib objects also
require compatible estimator libraries at load time; exact versions were not
verified. No root-level `requirements`, `environment`, `pyproject`, or
`Pipfile` was found. Package versions are **Unverified**. Hub revisions are
not pinned in `A_predict.py`; cache contents, cache freshness, network
availability, and actual Colab model revisions are **Unverified**. No model
cache was inspected or loaded.

## 8. Local versus live Drive verification

| Evidence level | Status |
|---|---|
| Workspace files under `project_s_qa/` | **Verified locally** at the recorded paths and hashes. |
| `drive_backup_20261107/` | **Verified as a local dated snapshot**, including the matching top-level packaged JSON/policy and runtime artifacts. |
| OneDrive sync indicator | Not used to infer Google Drive status. |
| Live Google Drive `My Drive/project_s_qa/` | **NOT VERIFIED**; no Drive mount, connector, browser session, or external service was accessed. |
| Actual Colab module/config/model-cache identity | **NOT VERIFIED**. |

## 9. Recommended notebook

**`NO AUTHORITATIVE NOTEBOOK ESTABLISHED`.** D and updated local are bytewise
source-equivalent, but cell 157 lacks a policy-hash guard. The Phase 2
executed-named copy adds a scorer/policy check, but differs from D at cell
157, catches mount exceptions, and never checks the reference JSON file's own
hash. Its execution counts do not prove which files were loaded. The 167-cell
working COPY also differs from D at seven cells and is two cells shorter.
Choose and approve a specific candidate and its hash before any runtime use;
no notebook was edited or executed here.

## 10. Recommended configuration option

**Proposed: Option B, conditionally.** The package JSON and policy are valid
JSON, their hashes match, their scorer hash matches the 13 local scorer copies,
and the dated top-level `drive_backup_20261107/` snapshot contains the
corresponding interim/demo files at one root. This is the strongest complete
local configuration evidence.

It is not yet runtime-compatible at the current local `project_s_qa/` root:
that root's JSON has a different policy hash and the expected policy file is
missing. Making Option B usable would require either a separately approved
new runtime root or an approved replacement procedure that first preserves
the existing JSON; a direct copy would overwrite an existing file and is not
permitted. Also confirm `PROJECT_S_ROOT` agrees with the notebook's path. Do
not copy, stage, or deploy this pair without Jigar's approval.

| Option | Evidence for | Evidence against / required action | Status |
|---|---|---|---|
| A — recover original policy | Root JSON records expected hash `babf76…`. | No file with that hash exists among discovered policy-named local files; archives were not opened. Must provide the exact original policy and verify its hash. | **Blocked locally** |
| B — packaged pair | JSON/policy hashes match; both name the matching scorer; dated top-level snapshot includes expected local artifacts. | Pair is not at the current local root's expected paths; live Drive is unknown. Requires explicit approval and verification at the actual mounted root. | **Recommended proposal; not applied** |
| C — create a new pair | Could document a deliberate configuration generation process. | No approved generation process or exact new settings/hash manifest exists. Must be separately specified and approved. | **Possible future option; not selected** |

## 11. Five-agent runtime-integrity review

All reviews were static and independent; no agent ran a script, model, or
notebook. Agreement is not treated as proof of runtime state.

| Role | Status | Verified finding | Unresolved / risk | Recommendation |
|---|---|---|---|---|
| Adversarial Evaluator | PARTIALLY VERIFIED | Missing policy silently changes fallback behavior: threshold 0.60 and contradiction review default true (`A_predict.py:16–17,139–141,164`). | Live policy and actual loaded root unknown; same scores can produce different review flags. | Block execution until exact live config is verified. |
| Assessment Architect | PARTIALLY VERIFIED | Frozen pooled decision path is preserved by the scorer if intended artifacts/policy are loaded (`:151–170`). | Root policy missing; packaged config not at expected top-level path. | Preserve baseline; require a complete hash-matched runtime root. |
| Systems Architect | PARTIALLY VERIFIED | Local notebook import path and scorer-derived paths are statically compatible only for the expected root (cell 157/159; `A_predict.py:8–10`). | Notebook/root/config selection, hub cache and live Drive remain unknown. | Select notebook/root and verify all files at those exact paths. |
| Evaluation Scientist | PARTIALLY VERIFIED | Reproducibility needs exact scorer, reference, policy, interim files and environment (`A_predict.py:8–12,21–35,139–170`). | Package versions, hub revisions/cache and runtime-loaded bytes are unknown. | Capture artifact and environment identities before evaluation. |
| Chief Decision Officer | PARTIALLY VERIFIED | Local evidence does not establish one authorized runtime configuration. | Notebook, root, JSON/policy, bank and confirmation protocol remain unresolved. | Keep Phase 0 open; do not begin Phase 1. |

## 12. Proposed final runtime manifest

This is a decision aid, not a runtime YAML file or deployment instruction.

```yaml
runtime_status: local candidate only; live runtime NOT VERIFIED
notebook: NO AUTHORITATIVE NOTEBOOK ESTABLISHED
notebook_sha256: NOT VERIFIED
runtime_root: /content/drive/MyDrive/project_s_qa (proposed; live contents unknown)
scorer: project_s_qa/reports_v2/A_predict.py
scorer_sha256: CA7C2752A4863F2A24B20EC7CD9000B651D83A0CFC39709F0080EBCBDAD0A053
reference_json: drive_backup_20261107/reports_v2/A_demo_reference_outputs_v2.json (candidate source)
reference_json_sha256: EA5288E9F12B25D28A66F36EC38D48B08C65E19452BF3B5EFA17EED2BE20AEB9
policy: drive_backup_20261107/reports_v2/A_abstain_policy_v2.json (candidate source)
policy_sha256: B6548EDEB682EABD2BA6B74D9B9B67BFF293C1FEA9C3CB6345E0A7EBF7E9EF9B
confidence_threshold: packaged candidate 0.64; current local missing-policy fallback 0.60
contradiction_review: packaged candidate false; current local fallback defaults true
required_directories: reports_v2, interim, processed
missing_dependencies: policy at current local root; live hub/cache and package identity unknown
live_drive_verified: NOT VERIFIED
configuration_status: NOT LOCKED
```

## 13. Remaining blockers

1. No authoritative notebook has been selected; candidate source hashes differ.
2. Current local runtime root has no policy and its JSON's stored policy hash
   is not explained by any discovered policy file.
3. Live Google Drive and actual Colab file identities are unverified.
4. Hub model revisions/cache and Python package versions are unverified; no
   root dependency lock was found.
5. The current root policy fallback can change review decisions silently.
6. Phase 0 decisions on canonical question bank/review and evaluation
   confirmation remain open in `docs/PHASE0_DECISION_RECORD.md`.

## 14. Exact user decisions required

### Decisions Jigar can make now

1. Select one notebook by the exact local path and SHA-256, or confirm that
   none is selected until a new approved run copy is prepared.
2. Confirm or reject Option B: packaged reference JSON and policy from the
   dated local snapshot, intended for the existing top-level runtime paths.
3. Confirm the intended Colab root is `/content/drive/MyDrive/project_s_qa`.

### Files or artifacts Jigar must provide

4. If choosing Option A, provide the original policy whose SHA-256 is the
   root JSON's stored `babf76…` value. If choosing B, the candidate files are
   present in the dated local snapshot; approval is still required before
   synchronization or any replacement of the existing root JSON.

### Live Drive checks requiring Jigar's access

5. In the authorized Colab account, verify the mounted root and record the
   hashes of scorer, reference JSON, policy, and required interim files.
6. Confirm availability of the three hub models and record installed package
   versions; this report did not access caches or install anything.

### Before Phase 1

7. Resolve the notebook and runtime root, place a hash-matched complete
   configuration at that exact root under an approved process, and have the
   fresh-runtime preflight pass. Resolve or explicitly defer the remaining
   bank/review and clean-confirmation decisions. Phase 1 does not start
   automatically.

## 15. Final Phase 0.1 readiness verdict

**PHASE 0.1 NOT COMPLETE.** The local dated snapshot is a promising
configuration candidate, but no selected notebook validates the reference
JSON's own hash, the current local root has a policy mismatch/absence, and
live Drive/runtime state is unknown.  
**PHASE 0 REMAINS OPEN.** Phase 1 must not start automatically.

## HOW THIS HELPS ACCURACY, AND BY HOW MUCH

This checkpoint can prevent stale scorer selection, silent threshold or
contradiction-review changes, notebook-path drift, and irreproducible
comparisons. Its direct demonstrated accuracy improvement is **0 percentage
points**. No projected gain is claimed.

## Final integrity record

- The report path was checked absent before creation.
- Only this new report was written.
- No tracked project source was modified; no pre-existing file was
  overwritten. Pre-existing untracked/ignored paths were left untouched.
- No Project S script, notebook cell, model, training, or inference was run;
  only local shell inspection, JSON metadata parsing, and hashing commands
  were used. No package was installed; no external service was accessed; no
  test data, notebook output, ZIP, or PDF content was inspected.
- Final Git status and report SHA-256 are recorded in the completion reply.
