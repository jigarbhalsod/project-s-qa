# Phase 3 Colab runbook (v2)

**Drafted — never use Run All. Never run cell 166 (Summary) or Block 49.**

1. **Colab setup.** Select a T4 GPU runtime. Mount Drive with
   `from google.colab import drive; drive.mount('/content/drive')`, then run
   `!ls /content/drive/MyDrive/project_s_qa/reports_v2`.
   Cells 157/159 use the hard-coded root
   `/content/drive/MyDrive/project_s_qa`; if absent, STOP rather than editing
   the notebook. Upload `dev_text_2049.parquet` to `/content/`.
2. **Fresh check.** Upload `phase3_fresh_runtime_check_v3.py` to `/content/`.
   Ensure `/content/drive/MyDrive/Project_S_QA_Evidence/Phase_3` exists
   (create it with `!mkdir -p` if needed), then run:
   `!python /content/phase3_fresh_runtime_check_v3.py --project-root /content/drive/MyDrive/project_s_qa --phase3-dir /content/drive/MyDrive/Project_S_QA_Evidence/Phase_3`.
   Download its `phase3_fresh_runtime_check_*.log` from Colab into the local
   `Project_S_QA_Evidence/Phase_3/` folder before running the local checker.
   SHA-256, scorer-mode, or policy-hash mismatch: STOP and report the full
   error; do not run notebook blocks.
3. **Run cells in order.** Open
   `Jigar_QA_PHASE2_RUN_COPY_EXECUTED.ipynb` in Phase_2. Run cell 157 (Block
   59; first 60 source characters:
   `import os, sys, json, time, importlib, hashlib\nimport numpy `), then
   cell 159 (Block 60; first 60:
   `# Block 60: question dropdown + voice input demo (adult voic`).
   After demo tests, run cell 163 (Block 62; first 60:
   `import sys, json, time, numpy as np, torch\nfrom google.colab`).
   Cell 161 (Block 61; first 60:
   `import sys, pandas as pd\nfrom google.colab import drive; dri`) is already
   done; do not rerun unless its diagnostic is needed. If any cell raises an
   error, save the full error text and STOP; do not run later cells.
4. **Typed demo.** In Block 60, select a CSV dropdown question, keep its
   reference box unchanged, enter one answer, score it, and log actual output.
   Repeat five times. Expected labels are not established for these CSV
   references; do not use reference-JSON labels as UI gold labels.
5. **Voice demo.** Use an adult voice and the CBSE plants dropdown item. Record
   exactly ten utterances: slow runs 1-4, fast runs 5-7, noisy runs 8-10.
   Use c06, c07, c08, c09, c10, c06, c07, c08, c09, c10 from
   `PHASE3_DEMO_CASES.md`. Those sentences use a different reference text
   than the dropdown plants question. Log scores as interface/ASR test results
   only, never as accuracy or child-validation evidence.
6. **Latency.** Cell 163 (Block 62) times one item and the 15-case batch.
   Record `predict_batch total` as `batch-1` and `batch-15` in
   `latency_log_v2.csv`. **Verified:** saved cell-163 output (execution count
   4) shows 151.9 ms for one item and 270.7 ms for batch of 15. The 356 ms
   figure is absent from that output (**Unverified**); do not use it.
7. **Capture evidence.** Save screenshots as `p3_dropdown_01.png`,
   `p3_five_cases_01.png`, `p3_voice_run_01.png`, and
   `p3_review_output_01.png`. Use `_02`, `_03` for extra shots. Save the video
   as `p3_backup_demo.mp4` (under two minutes), showing dropdown, one case,
   one voice run, and review output.
8. **Close safely.** Save the executed notebook as the new file
   `Jigar_QA_PHASE3_RUN_COPY_EXECUTED.ipynb`; never overwrite the Phase 2
   executed copy. Download it, stop the Gradio link, then disconnect runtime.
   Keep logs and captures in the local Phase_3 folder.
