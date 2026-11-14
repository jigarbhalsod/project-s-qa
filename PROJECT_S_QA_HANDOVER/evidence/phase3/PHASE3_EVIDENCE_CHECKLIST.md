# Phase 3 evidence checklist

Use a fresh Colab session. Keep the demo and evidence run separate from model
training. Never run All, Block 49, or Summary cell 166. Do not claim accuracy
or child-assessment validation from demonstration cases.

- [ ] **Drafted — Question dropdown:** save `01_question_dropdown.png`.
- [ ] **Drafted — Five reference cases:** save `02_five_reference_cases.png`.
- [ ] **Drafted — Score, confidence, review flag:** save
  `03_score_confidence_review.png`.
- [ ] **Drafted — One adult voice run:** separately note transcript and score;
  save `04_voice_run_transcript.png` and, only if permitted, `04_voice_run.wav`.
- [ ] **Drafted — Backup screen video:** save `05_demo_backup_video.mp4`.
- [ ] **Drafted — Block 62 latency:** save `06_block62_latency.png` and the
  executed notebook copy. **Verified from Phase 2 report:** 270.7 ms is the
  batch-15 `predict_batch total` median from the executed run, cell 163.
  **Unverified:** provenance of the 356 ms figure; it was not found in the
  Phase 2 Markdown reports. Do not combine these values.
- [ ] **Drafted — Frozen-file Drive Modified dates:** save
  `07_frozen_drive_modified_dates.txt` with Drive screenshots/evidence for
  `A_predict.py`, scorer/reference JSON, policy, model artifacts, and dev
  probability file. **Unverified:** current Drive dates until captured.

For each captured item, record date, runtime/GPU, exact input case ID, and any
error. Voice examples are demo-only; do not report an accuracy metric from them.
