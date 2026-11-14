# Project S — Phase 2 completion review

## Scope and file identity

**Verified:** No notebook cell, model, training, or Project S script was run by
Codex. No package was installed; no file was moved, overwritten, or deleted.
No separate `A_test_*` or `A_table_test_*` artifact was opened. Stored outputs
were reviewed only for the requested cells and screened for test content.

**Verified:** The specified executed file
`Project_S_QA_Evidence/Phase_2/Jigar_QA_PHASE2_RUN_COPY_EXECUTED.ipynb` is
missing. The run-copy path exists, has 169 cells, size 3,389,226 bytes, and
local mtime 2026-11-07 19:54:49. Its current SHA-256 is
`EBB83C058F58CF724153BB897BBDB0854E5A390FBB9EB5BF0A29E885042CC787`, which
differs from the supplied pre-run hash
`953af96b1f620ec4cdea06e23b0b4198fcbc4a8d6c2cc45b96cdf31aed0714dc`.
It contains execution counts and outputs for Blocks 59–62, but it is not the
separately named executed notebook requested.

**Verified:** Against the available local D notebook, the current run-copy
source differs only at cell 157 (Block 59), where the policy-hash check was
added. Both files have 169 cells. The named executed notebook was unavailable,
so its source could not be compared directly with the run copy.

## 1. Block 59 — cell 157

**Verified source:** the policy-hash check is present. The pooled-mode check,
scorer-file SHA-256 check, policy-file existence check, and policy SHA-256
check are all on the successful path. **Tested from saved run evidence:**
execution count 6; no error/traceback output; the cell reached its final
latency prints, so those checks did not raise during that saved execution.

**Verified:** It does not print nothing on success. Stored output includes the
Drive mount notice, runtime hardware, model-loading progress, and latency
lines. The latency lines are not the only output.

**Block 59 source (cell 157):**

```python
import os, sys, json, time, importlib, hashlib
import numpy as np
import torch
from google.colab import drive
try:
    drive.mount("/content/drive")
except Exception as e:
    print("Drive mount skipped or already active:", e)

ROOT = "/content/drive/MyDrive/project_s_qa"
V2 = f"{ROOT}/reports_v2"
sys.path.insert(0, V2)
import A_predict
importlib.reload(A_predict)

# Print runtime hardware
dev_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
print(f"Colab Runtime Hardware: {dev_name} (CUDA available: {torch.cuda.is_available()})")

# Load reference outputs for test inputs
ref_path = f"{V2}/A_demo_reference_outputs_v2.json"
assert os.path.isfile(ref_path), f"Missing: {ref_path}"
ref_data = json.load(open(ref_path))
scorer_mode = ref_data.get("scorer_mode")
assert scorer_mode == "pooled", f"Expected pooled scorer, got {scorer_mode!r}"
loaded_hash = hashlib.sha256(open(A_predict.__file__, "rb").read()).hexdigest()
assert ref_data.get("a_predict_sha256") == loaded_hash, "A_predict.py hash mismatch"
policy_path = f"{V2}/A_abstain_policy_v2.json"
if not os.path.isfile(policy_path):
    raise FileNotFoundError(f"Missing: {policy_path}")
policy_hash = hashlib.sha256(open(policy_path, "rb").read()).hexdigest()
if ref_data.get("policy_sha256") != policy_hash:
    raise ValueError("A_abstain_policy_v2.json hash mismatch")

# --- Single Answer Latency ---
q = ref_data["cases"][0]["question"]
ref = ref_data["cases"][0]["reference_answer"]
ans = ref_data["cases"][0]["student_answer"]

# Warm-up (1 run)
_ = A_predict.predict(q, ref, ans, dataset=scorer_mode)

# 20 timed runs
single_times = []
for _ in range(20):
    t0 = time.perf_counter()
    _ = A_predict.predict(q, ref, ans, dataset=scorer_mode)
    single_times.append((time.perf_counter() - t0) * 1000.0)

median_single_ms = float(np.median(single_times))

# --- Batch Latency (15 reference items) ---
batch_items = [{"question": c["question"], "reference_answer": c["reference_answer"], "student_answer": c["student_answer"]}
               for c in ref_data["cases"]]

# Warm-up (1 run)
_ = A_predict.predict_batch(batch_items, dataset=scorer_mode)

# 20 timed runs
batch_times = []
for _ in range(20):
    t0 = time.perf_counter()
    _ = A_predict.predict_batch(batch_items, dataset=scorer_mode)
    batch_times.append((time.perf_counter() - t0) * 1000.0)

median_batch_ms = float(np.median(batch_times))
median_per_item_ms = median_batch_ms / len(batch_items)

print(f"Single-answer latency (median of 20 runs): {median_single_ms:.1f} ms")
print(f"Batch latency for {len(batch_items)} items (median of 20 runs): {median_batch_ms:.1f} ms ({median_per_item_ms:.1f} ms / item)")
```

## 2. Blocks 60–62 saved outputs

| Block / cell | Saved execution evidence | Output summary | Error / traceback |
|---|---|---|---|
| **Tested — Block 60 / cell 159** | Execution count 2; 18 outputs. | Gradio interface launched and printed a temporary public URL. Whisper model loading completed. No saved Score-button result is present in this cell output. | None stored. A Transformers warning says `chunk_length_s` is experimental; Gradio enabled sharing automatically in the hosted notebook. These are warnings, not recorded failures. |
| **Tested — Block 61 / cell 161** | Execution count 3; 5 outputs. | Printed 12 negation rows with ft, sb, and nl component predictions/probabilities. NLI-LR predicts `contradictory` at about 0.507 on all 12. | None stored. |
| **Tested — Block 62 / cell 163** | Execution count 4; 1 output. | Printed component timing medians for one answer and the 15-case batch. | None stored. |
| **Verified — Summary / cell 166** | Execution count is empty; zero outputs in the current run-copy. | Not executed in this file. | Not applicable. Source line 46 reads `A_test_results_v2.csv`; keep this cell blocked under the test-data rule. |

**Verified:** The current run-copy's cell 166 has no stored test output. In other
cells, test-related stored output was detected and not printed: **test content
present in cell 60; cell 72; cell 78; cell 112; cell 131; cell 150; cell 155**.

## 3. Latency values in saved outputs

**Tested (saved notebook output): Block 59, cell 157** — single-answer median
of 20 runs: **95.2 ms**; batch-15 median of 20 runs: **138.9 ms**;
**9.3 ms/item**.

**Tested (saved notebook output; Block 62 official component figures), cell 163:**

| Scope | Component / stage | Stored median |
|---|---|---:|
| single | DistilRoBERTa | 14.2 ms |
| single | NLI (whole-reference pairs only) | 43.9 ms |
| single | SBERT features | 49.8 ms |
| single | component_probs total | 247.7 ms |
| single | predict_batch total | 151.9 ms |
| batch15 | DistilRoBERTa | 20.2 ms |
| batch15 | NLI (whole-reference pairs only) | 53.7 ms |
| batch15 | SBERT features | 75.4 ms |
| batch15 | component_probs total | 267.4 ms |
| batch15 | predict_batch total | 270.7 ms |

**Verified source limitation:** Block 62 reports medians over 20 runs for one
answer and 15 answers. It does not print batch-32 timings or p95. No values
were averaged across cells or runs here.

## 4. Negation diagnostic interpretation

**Tested (saved output):** all 12 `nl` values are near 0.507; the printed
values range from 0.5069 to 0.5071. This is the NLI-LR component's five-class
probability for `contradictory`, not the raw NLI model's contradiction
probability.

**Verified source:** Block 61 calls `component_probs(items, dataset="pooled")`.
The NLI features combine cross-encoder probabilities for student-answer vs
reference-concept pairs and whole-reference vs student-answer pairs; the pooled
NLI logistic-regression model maps those features to five-class probabilities.
The stored output and source establish the inputs and near-constant prediction,
but do not explain why the fitted classifier produces that near-constant value.
**Diagnostic only; not a gate and not validation evidence.**

## 5. Voice notes and dates

| Requested evidence | Finding |
|---|---|
| Voice notes file | **BLOCKED / Unverified:** `evidence/voice_runs_reported.txt` is absent. No individual run records can be tabulated. |
| Predicted matches, review-flag rate, wrong-but-unflagged | **Unverified:** not computed because run records are absent. |
| Contradiction >= 0.95 but prediction “correct” | **Unverified:** cannot check without run-level voice notes. |
| Drive Modified dates before/after | **Unverified:** the prompt contains `[FILL]` placeholders and no before-run baseline. Current local timestamps cannot substitute for Drive dates. |

**Reported:** The prompt describes the intended voice tests as adult voice,
CBSE-style and `draft_unreviewed`. The missing notes file means those runs and
labels are not independently reviewable here; they remain demo-only and are
not accuracy evidence.

## 6. Failure classification

| Category | Finding |
|---|---|
| Data | **BLOCKED, non-blocking for basic demo launch:** corrected CBSE CSV was not received; existing CSV is `draft_unreviewed`. No data-file error appears in the saved Block 60 output. |
| Path/configuration | **Verified:** Blocks 59–62 show no stored traceback. **BLOCKED:** Summary reads a test artifact and was not run. The separately named executed notebook is missing. |
| Model loading | **Tested (saved output):** Block 60 shows Whisper loading and interface launch; no loading traceback is stored. This does not independently verify every runtime asset. |
| Inference | **Tested (saved output):** Blocks 59, 61 and 62 reached their printed outputs. **Unverified:** no saved Block 60 Score-button result. |
| ASR | **Unverified:** the UI's microphone path exists, but voice-run notes/transcription outcomes are absent. |
| Interface | **Tested (saved output):** Gradio launched and emitted a temporary share URL. **Unverified:** whether it is still live now. |

## 7. Phase 2 checklist mapping

**Unverified source note:** the Notion roadmap itself was not accessed. The map
below uses the Phase 2 run-sheet and task requirements already in this project.

| Checklist item | Status and evidence |
|---|---|
| Notebook uploaded/opened in intended Colab session | PARTIAL — saved Colab outputs exist in the current run-copy, but the named executed file and exact upload identity are unverified. |
| T4 runtime and Drive mount | DONE-evidenced — saved Block 59 output identifies Tesla T4; Blocks 59–62 report Drive already mounted. |
| Preflight diagnostic | UNVERIFIED — no diagnostic-cell output is present in the reviewed evidence. |
| Blocks 59–62 run individually | DONE-evidenced — execution counts 6, 2, 3, 4; outputs stored; no errors in these cells. |
| Demo typed scoring cases | PARTIAL — interface launched; no saved button-result evidence for the requested test cases. |
| Adult voice runs and transcription notes | UNVERIFIED — referenced notes file missing. |
| Latency and Block 61 evidence captured | DONE-evidenced — Block 59 and 62 timings and Block 61 diagnostics are stored. |
| Frozen-file mtime check | UNVERIFIED — before-run dates were not recorded. |
| Separate executed notebook saved at requested path | BLOCKED — named `..._EXECUTED.ipynb` is absent; the run-copy file itself has outputs and a changed hash. |
| Corrected CBSE CSV received | BLOCKED, non-blocking for basic demo — corrections not received; source CSV remains draft_unreviewed. |

**Verified count:** 3 DONE-evidenced, 2 PARTIAL, 2 UNVERIFIED, 3 BLOCKED.
**Conclusion:** Phase 2 cannot yet be called complete: the requested executed
copy, frozen-file timestamp comparison, and voice-run evidence are missing;
typed scoring-case results are also not evidenced. Blocks 59–62 have saved
execution evidence in the current run-copy, but that does not fill those gaps.
