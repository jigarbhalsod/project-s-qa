# Phase 3 Colab runbook

**Drafted — never use Run All. Do not run cell 166 (Summary), Block 49, or
cell 161 (Block 61, already completed) unless a rerun is needed.**

1. **Colab setup.** Select a T4 GPU runtime. Mount Drive with
   `from google.colab import drive; drive.mount('/content/drive')`, then run
   `!ls /content/drive/MyDrive/project_s_qa/reports_v2`.
   Cells 157/159 use the hard-coded root
   `/content/drive/MyDrive/project_s_qa`; if that path is absent, STOP rather
   than editing the notebook. Upload `dev_text_2049.parquet` to `/content/`.
2. **Fresh check.** Upload `phase3_fresh_runtime_check_v3.py` to `/content/`.
   Ensure `/content/drive/MyDrive/Project_S_QA_Evidence/Phase_3` exists
   (create it with `!mkdir -p` if needed), then
   run `!python /content/phase3_fresh_runtime_check_v3.py --project-root
   /content/drive/MyDrive/project_s_qa --phase3-dir
   /content/drive/MyDrive/Project_S_QA_Evidence/Phase_3`.
   SHA-256, scorer-mode, or policy-hash mismatch: STOP and report the full
   error; do not run the notebook blocks.
3. **Run cells in order.** Open
   `Jigar_QA_PHASE2_RUN_COPY_EXECUTED.ipynb` in Phase_2. Run cell 157 (Block
   59; first 60 source characters: `import os, sys, json, time, importlib, hashlib`),
   then cell 159 (Block 60; first 60: `# Block 60: question dropdown + voice input demo (adult voic`).
   After demo tests, run cell 163 (Block 62; `import sys, json, time, numpy as np, torch`).
   Stop on any error, save its full text, and do not continue. Cell 161 (Block
   61) is already done; rerun only if its diagnostic is specifically needed.
4. **Typed demo.** In Block 60, choose a CSV dropdown question, keep its
   reference box unchanged, enter one answer, score it, and log actual output.
   Repeat five times. Expected labels are not established for these CSV
   references; do not treat the reference-JSON labels as UI gold labels.
5. **Voice demo.** Use an adult voice and the CBSE plants dropdown item for
   each run. Record exactly ten utterances: slow runs 1-4, fast runs 5-7,
   noisy runs 8-10. Use sentences c06, c07, c08, c09, c10, c06, c07, c08,
   c09, c10 respectively, copied verbatim from PHASE3_DEMO_CASES.md. Log
   transcript and meaning changes separately from score results. These are
   demonstrations, not accuracy or child-validation evidence.
6. **Latency.** Cell 163 (Block 62) times one item and the 15-case batch.
   Record its `predict_batch total` values as `batch-1` and `batch-15` in
   latency_log.csv. **Verified:** saved cell-163 output has 151.9 ms for the
   single `predict_batch total` and 270.7 ms for `batch15` (saved execution
   count 4); the 356 ms figure is not in that output, so its provenance is
   Unverified.
7. **Capture evidence.** Save screenshots named `p3_<item>_<nn>.png` for the
   dropdown, five cases, voice run, and review output. Record a screen video
   named `p3_backup_demo.mp4` under two minutes, showing those interactions.
8. **Close safely.** Save a separate executed notebook copy (never overwrite
   the run copy), download it, stop the Gradio link, then disconnect runtime.
   Keep logs and captures in `Project_S_QA_Evidence/Phase_3/`.

**Verified compatibility note:** JSON cases c06-c10 use the same plants
question as dropdown item `cbse_demo_01`, but their reference text differs.
Do not replace the dropdown reference. The fresh-runtime checker scores its
own JSON cases; Block 60 results must be logged against the CSV reference.
