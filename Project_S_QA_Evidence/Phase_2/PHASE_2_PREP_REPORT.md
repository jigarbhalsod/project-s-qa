# Project S ? Phase 2 preparation report

**Scope ? Verified:** static source and filename/size inspection of local
`drive_backup_20261107/project_s_qa`; no notebook outputs or test artifacts
were opened. No Google Drive connection was used. No notebook, model, training
or Project S script was executed; no installation or download was performed.

## Notebook cells and safety review

| Section | Source cell(s) | Reads | Writes / overwrite risk | Imports / device | Missing-file behavior and test status |
|---|---:|---|---|---|---|
| Summary | 165 markdown, 166 code | **Verified:** optional files under `reports_v2`: `A_deployed_scorer_v2.json`, `A_ml_only_audit_v2.json`, `A_abstain_policy_v2.json`, `A_demo_parity_v2.json`, `A_model_comparison_dev_v2.csv`, `A_deployed_metrics_ci_v2.csv`, `A_negation_paraphrase_v2.csv`, and `fig*_*.png`. It also reads `A_test_results_v2.csv` at code-cell source line 46. | **Verified:** no project-file writes in source. | **Verified:** os, glob, json, pandas; no GPU requirement. | **BLOCKED-READS-TEST:** do not run as written; it reads and prints a saved test artifact. Other listed inputs are guarded with existence checks and silently skipped if absent. |
| Block 59 | 156 markdown, 157 code | **Verified:** `reports_v2/A_demo_reference_outputs_v2.json`; imports `A_predict`, which reads policy/model artifacts listed below. | **Verified:** no project-file writes. HF model cache may be populated if model assets are not cached. | **Verified:** os, sys, json, time, importlib, hashlib, numpy, torch, Colab Drive; GPU optional in source, T4 recommended for speed. | **Verified:** explicit missing-JSON, pooled-mode, and scorer-hash assertions. **Verified:** no policy-hash check. No test artifact reference in this block's source. |
| Block 60 | 158 markdown, 159 code | **Verified:** `processed/cbse_demo_questions_v1.csv`; `A_predict` policy/model artifacts; Whisper model ID `openai/whisper-small`. | **Verified:** no project-file writes in source; Gradio/runtime temp and model-cache writes are possible outside project artifacts. | **Verified:** os, sys, importlib, pandas, torch, gradio, transformers pipeline, Colab Drive; GPU optional for ASR/scorer. | **Verified:** raises `FileNotFoundError` for absent CSV and `ValueError` for missing required columns. Gradio/model-cache availability is unverified. No test artifact reference in source. |
| Block 61 | 160 markdown, 161 code | **Verified:** `reports_v2/A_negation_paraphrase_v2.csv`; `A_predict` policy/model artifacts. | **Verified:** no project-file writes in source. | **Verified:** sys, pandas, Colab Drive, A_predict; GPU optional in A_predict. | **Verified:** missing CSV fails at `read_csv`; row/triple mismatch fails its assertion. No test artifact reference in source. |
| Block 62 | 162 markdown, 163 code | **Verified:** `reports_v2/A_demo_reference_outputs_v2.json`; `A_predict` model artifacts. | **Verified:** no project-file writes in source. | **Verified:** sys, json, time, numpy, torch, Colab Drive, A_predict; GPU optional in source. | **Verified:** missing JSON fails at `open`; missing model/cache assets fail during load. No test artifact reference in source. |

**Verified:** Block 63 is absent from notebook source. The inspected canonical
D copy has 169 cells; target cell indices above are from that copy.

## Paths and runtime dependencies

**Verified:** notebook root is `/content/drive/MyDrive/project_s_qa`;
`reports_v2`, `processed`, and `interim` paths match that Drive layout. The
inspected cells do not use `demo/` or `models/` paths. `A_predict.py` uses
`PROJECT_S_ROOT` if set, otherwise the same root.

| Dependency | Local Drive-backup check (name and size only) |
|---|---|
| `reports_v2/A_predict.py` | **Verified found:** 7,626 bytes. SHA-256 `CA7C2752A4863F2A24B20EC7CD9000B651D83A0CFC39709F0080EBCBDAD0A053` (rechecked). |
| `reports_v2/A_demo_reference_outputs_v2.json` | **Verified found:** 16,474 bytes. Packaged copy SHA-256 begins `EA5288E9` (rechecked); no JSON contents inspected. |
| `reports_v2/A_abstain_policy_v2.json` | **Verified found:** 784 bytes in the packaged pair. Policy SHA-256 `B6548EDEB682EABD2BA6B74D9B9B67BFF293C1FEA9C3CB6345E0A7EBF7E9EF9B` (hash only). |
| `reports_v2/A_negation_paraphrase_v2.csv` | **Verified found:** 3,657 bytes. |
| `processed/cbse_demo_questions_v1.csv` | **Verified found:** 2,888 bytes. |
| `interim/combiner_v1.joblib` | **Verified found:** 129,270 bytes. |
| `interim/pooled_lr_v2.joblib` | **Verified found:** 63,625 bytes. |
| `interim/ft_distilroberta_v1/config.json` | **Verified found:** 919 bytes. |
| `interim/ft_distilroberta_v1/model.safetensors` | **Verified found:** 328,501,508 bytes. |
| `interim/ft_distilroberta_v1/tokenizer_config.json` | **Verified found:** 388 bytes. |
| `interim/ft_distilroberta_v1/tokenizer.json` | **Verified found:** 3,558,895 bytes. |
| NLI model | **Unverified in Drive:** source names `cross-encoder/nli-deberta-v3-base`; weights are not in the inspected project `interim` files. A Colab cache is required to avoid fetching it. |
| SBERT model | **Unverified in Drive:** source names `sentence-transformers/all-MiniLM-L6-v2`; weights are not in the inspected project `interim` files. A Colab cache is required to avoid fetching it. |
| Whisper model | **Unverified in Drive:** Block 60 names `openai/whisper-small`; weights are not in the inspected project files. A Colab cache is required to avoid fetching it. |
| Summary-only files | **Verified by name/size:** scorer, audit, policy, parity, dev comparison, dev CI, and negation files were present in local `reports_v2`; figures are optional. **BLOCKED:** no check was made for the test file. |

**Verified:** `A_predict.py` source loads DistilRoBERTa from
`interim/ft_distilroberta_v1`, the combiner and pooled LR joblibs from
`interim`, and NLI/SBERT models by the IDs above. It selects CUDA when
available, otherwise CPU. Its policy loader reads `reports_v2/A_abstain_policy_v2.json`
when present and otherwise returns an internal provisional policy.

**Drafted:** a successful `A_predict._load()` would return its populated model
state without an exception; a subsequent prediction would return the scorer's
prediction/probability/review fields. This has not been tested here.

## Block 59 policy-hash gap

**Verified:** current Block 59 checks `scorer_mode == "pooled"` and compares
`a_predict_sha256` with the loaded scorer hash; it does not inspect
`policy_sha256`.

**Proposed only ? not applied:** insert after the scorer-hash assertion:

```diff
 assert ref_data.get("a_predict_sha256") == loaded_hash, "A_predict.py hash mismatch"
+policy_path = f"{V2}/A_abstain_policy_v2.json"
+if not os.path.isfile(policy_path):
+    raise FileNotFoundError(f"Missing: {policy_path}")
+policy_hash = hashlib.sha256(open(policy_path, "rb").read()).hexdigest()
+if ref_data.get("policy_sha256") != policy_hash:
+    raise ValueError("A_abstain_policy_v2.json hash mismatch")
```

**Verified:** pooled-mode mismatch already stops at the existing assertion.
This proposed addition checks the paired policy file and fails clearly if it is
missing or its hash differs. It has not been applied or run.

## CBSE question bank

**Verified:** CSV columns include `question_id`, `question_text`,
`reference_answer`; it has 12 rows and every status value is
`draft_unreviewed`. **Reported:** Vishwajeet's correction list was not
received. **BLOCKED:** applying corrections cannot proceed without that list.
**Drafted:** Block 60 can technically read and display the uncorrected CSV,
but questions remain draft/unreviewed and are not validated; obtain Jigar's
approval before using it in the live demo.

## Fresh-runtime and readiness

**Drafted:** Block 59, 61, and 62 rely on A_predict's local artifacts plus cached
NLI/SBERT models. Block 60 additionally requires the CSV, Whisper cache, and
Gradio. Package versions and Colab cache availability are **Unverified**.
If caches are absent, these cells may attempt network fetches; do not proceed
under a no-download constraint until Jigar confirms assets are cached or
approves another process.

**Drafted:** Blocks 59?62 contain no direct project artifact writes and do not
reference test artifacts. They can be run individually in order only after
runtime dependencies are available, the proposed policy-hash correction is
approved/applied to a new run copy, and the CSV use is approved. The requested
Summary-first sequence is **BLOCKED** because Summary reads a test result; skip
it unless a separately approved safe version is prepared. This is not a claim
that any cell has run successfully.

## Phase 2 checkbox state

| Item | Status |
|---|---|
| Static cell/path review | **Verified** ? indices and source paths recorded above. |
| Runtime files | **Verified** ? project-staged files are present by name/size. |
| Model caches / packages | **Unverified** ? Colab runtime state not accessible. |
| Block 59 policy hash | **BLOCKED** ? current cell omits policy hash; patch is proposed only. |
| Summary-first execution | **BLOCKED** ? source reads `A_test_results_v2.csv`. |
| Blocks 59?62 execution | **Drafted** ? conditional on the prerequisites above and Jigar running them in Colab. |
| Phase 2 overall | **PARTIAL / BLOCKED** ? preparation is documented; Colab run remains with Jigar. |
