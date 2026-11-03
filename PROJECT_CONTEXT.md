# Project S: Q&A branch, full context (state as of 2 Nov 2026, Day 3 of 5)

## 1. Project
Project S builds an interpretable reading-skills profile for children (ages 8 to 12). Reading and comprehension are reported separately. There is no single total score. Each skill has its own uncertainty interval and a teacher-review flag.
- Reading branch (Askar and Safal): design stage. Reference text, transcripts and human ratings are missing, so most experiments are blocked. Askar's baseline: age classification 42.01% +/- 4.61%. This comes from Notion; re-check before using on a slide.
- Q&A branch (Jigar and Vishwajeet): built and measured on public English data (SciEntsBank, Beetle). Not measured on NNCES or CBSE.
- Jigar owns architecture, Q&A scoring, profile layer, evaluation. Vishwajeet's notebook is his own; Jigar cannot edit it. Published numbers from other papers are hypotheses until tested on our data.
- Notion master page: "Reading Skills Profile Generation of Children, Project Master Page". Child page: "Q&A Branch: Next 5 Days, Effective Work Plan (from 31 Oct 2026)". Deadline (Day 5 = 4 Nov) is ASSUMED; confirm it.

## 2. Deployed scorer (measured, dev data, optimistic)
- Average of three local models: fine-tuned DistilRoBERTa, SBERT + logistic regression, NLI + logistic regression. Model version v2-avg3-ft+sbert+nli.
- Outputs: incorrect / partial / correct (0/1/2), confidence, probabilities, NLI entail/contradict, concepts, needs_teacher_review (confidence below 0.64).
- Inference file: A_predict.py with predict(question, reference_answer, student_answer, dataset="both") and predict_batch(items, dataset="both", policy=None). The project path /content/drive/MyDrive/project_s_qa is hard-coded.
- Rule L8: no hosted LLM, no external API in the deployed scorer. Local open-weights models in Colab are allowed.
- Dev QWK: all 0.432 (0.358 to 0.509); seen 0.630; unseen 0.317 (0.199 to 0.412) over 27 questions. Plan was 0.55 to 0.60: NOT met.
- Dev macro-F1: all 0.579, seen 0.730, unseen 0.490.
- Review threshold 0.64, ECE 0.017. Accuracy on auto-scored answers: dev 0.751 at coverage 0.306; test 0.790 at coverage 0.288. Target 85% at 30% coverage: NOT met (grouped-CV estimate 0.748 at 0.313).
- Exploratory test QWK: all 0.454 (0.392 to 0.515); unseen domain 0.441. Test sets were seen in v1 (access log reads 3), so every test number is exploratory.
- Demo parity: PASS on 15 of 15 hand-written reference cases. It shows consistency, not independent replication.
- Negation control set (36 sentences): 3 of 12 negated answers scored exactly right; all 12 flagged for review.

## 3. Folder map (Project 4/, Windows: C:\Users\Jigar\OneDrive\Desktop\Project 4)
- Jigar_Q&A_Branch_Baseline.ipynb: ORIGINAL on disk. READ-ONLY, never edit. It has 151 cells, NOT the clean 162. Blocks 45 (heading and parity code) and 55 (heading and policy code) were deleted from it by mistake earlier. It is not clean v1 history.
- Jigar_Q&A_Branch_Baseline_COPY.ipynb: the working copy and the ONLY notebook you may edit. 161 cells.
- Jigar_Q&A_Branch_Baseline_COPY_before_block60.ipynb: backup of the copy, 159 cells. READ-ONLY.
- reference/: must hold the CLEAN 162-cell notebook (the reference for every comparison; 70 code cells, 3,798 code lines). Jigar recovered it from the Recycle Bin and must copy it here. If it is not in this folder, STOP and ask. Do not search the Recycle Bin or the rest of the disk. READ-ONLY.
- extracted_A_predict.py: local extract of the v2 scorer. READ-ONLY. It imports torch and transformers: read it as text, never import or run it.
- comparison_table.json: cell-by-cell map of the 162 vs 151 notebooks. READ-ONLY. Treat it as helpful but unverified; re-check against the notebooks.
- project_s_qa_phase1_v1.zip and project_s_qa_final_v1.zip: archived Phase 1 package and frozen v1 results. READ-ONLY. Do not unzip into this folder, do not overwrite, do not modify.
- New folder (2)/block_60_voice_demo_cell.py (68 lines, sha256 cb082b77f2536c234310b3f8e230415f4d07a8ef8be4a1ca3c2337f98409d6c5) and New folder (2)/cbse_demo_questions_v1.csv (12 draft questions, status draft_unreviewed, not labelled student answers). READ-ONLY.
- My Research Papers/, New folder/, Askar/: PDFs (papers on ASAG, literacy assessment, child speech, reading-side work by Askar and Safal). READ-ONLY. Do not open or summarise a PDF unless Jigar asks for that exact paper. Askar/ belongs to the reading branch, not this task.
- .cursor/rules/project-s.mdc: always-on rules. Do not edit it unless Jigar asks.
- The notebook is about 3 MB, mostly saved outputs. Never paste it into chat. Use an outline (cell index, type, first line, block) and edit with small Python scripts that read and write .ipynb JSON and change only the listed cells.

## 4. What was done on the COPY (verified by script: valid JSON, 161 cells, 149 untouched cells with identical source, outputs and execution counts, 12 differing cells)
Deleted from the 162 reference (9 cells): original 0, 1, 2 (basic checks, GPU check, memory cleanup); 120 and 122 (Block 45 timestamp checks); 153 (Block 55 file check); 154 (RoBERTa file listing); 155 and 156 (Block 56 "withdrawn").
Restored from the reference: Block 45 heading and parity code; Block 55 heading and policy code.
Copy cell map:
- 0: READ FIRST (never Run all; run only Summary, Block 59, Block 60; do-not-run list)
- 43: Block 17 note "dev-only side result, uses an API call, not part of the deployed scorer"
- 72: Block 28 heading, stray ")" removed
- 118: Block 45 provenance note (demo_outputs.json regenerated 31 Oct 06:46; earlier file kept as demo_outputs_PREVIOUS.json)
- 124: Block 45c Gradio cell, description clause "reliable for related answers" removed (only that string changed)
- 154 to 155: Block 59 latency (hardware print, 1 warm-up, median of 20 runs)
- 156 to 157: Block 60 question dropdown + local Whisper-small voice input, editable transcript, scored by A_predict.predict
- 158: Limitations cell (NLI evidence caveat 0.87 to 0.96 on 3 of 4 off-topic sentences; hard-coded path in A_predict.py)
- 159 to 160: Summary for the panel (read-only loader of 8 reports_v2 files plus fig*_*.png)
NOTHING has been run in Colab. Summary, Block 59 and Block 60 are untested.

## 5. Rules (always)
- Edit only. NEVER run any notebook cell. NEVER use Run all (it rewrote 18 frozen v1 files on 30 Oct and raised the test-access count to 3). Do not run Python that imports torch, transformers, A_predict or extracted_A_predict.
- Edit only the COPY. Everything else in section 3 is read-only.
- Never edit or delete Blocks 12 and 22 (manifest, freeze check), Block 17 (LLM_PRED is used by Blocks 18 and 24), Block 26 (only record of the RoBERTa-base run; weights were never saved), Block 42 (Block 49 reads its seed summary), or the old duplicate helper cells (to3, met, sha256, boot, make_qid, pick, nli_X, predict_probs, ens, md, rc). Editing them forces a re-run.
- New blocks start at Block 61 (59 and 60 are taken). Files written to reports_v2/ start with "A_". Never overwrite question_bank_v1.csv (Block 12 writes it, Block 22 hashes it). The question bank file is cbse_demo_questions_v1.csv, which lives in project_s_qa/processed/ on Drive.
- New helper code goes in one A_utils.py for NEW cells only. Library first: pretrained model, then library function, then documented recipe, then own code.
- Before any change: show the plan and wait for "go". After: integrity checks against the 162-cell reference (valid JSON, untouched cells identical in source, outputs and execution counts, list of differing cells).
- Test numbers are labelled "exploratory (test seen in v1)". Dev numbers are labelled "dev, optimistic". If a number is not in the notebook, write "not in notebook". Never invent or estimate a number. Never compute a plain overall accuracy for the panel if the notebook does not report one.
- Do not use the 36 negation control sentences for training.

## 6. Pending work, in order
1. Folder fix by Jigar: copy the clean 162-cell notebook into reference/.
2. Colab runs by Jigar (nothing has run yet): back up the Drive folder project_s_qa; upload cbse_demo_questions_v1.csv to project_s_qa/processed/; upload the COPY as a new notebook; run only Summary (last cell), then Block 59, then Block 60. Test the voice demo with about 10 adult recordings (slow, fast, noisy). Check no frozen file timestamp changed.
3. Read-only accuracy report from saved outputs, compared with the numbers in section 2. List every mismatch.
4. Question bank: 12 of the planned 20 to 30. Jigar and Vishwajeet review the science and wording and write the rest. Reference answers: 1 or 2 short sentences, one idea each.
5. Pilot: 5 to 8 volunteers type answers to 15 to 20 questions. Jigar and Vishwajeet label 0/1/2 separately, blind to the scorer; report agreement first (labellers also wrote the questions; say so). Then score and report QWK, review rate, silent failures as a pilot of 100 to 150 answers, not a validation.
6. One gated accuracy experiment (choose on Day 3). Recommended: Option C, negation augmentation (synthetic negated answers, flagged synthetic, training only). Option A (learned deferral): keep as a study, do not deploy (0.815 vs 0.751 accuracy at coverage 0.306, interval 0.002 to 0.128, tuned on the same dev data). Option B (DeBERTa-v3 cross-encoder): drop first if short on time. Before any training, write 30+ NEW negation test sentences kept out of training. Judge on out-of-fold results over all 177 dev questions, not only the 27 unseen. Adoption gates, ALL must hold: macro-F1 beats v2 by at least 0.01 with a paired interval above 0; unseen-question QWK does not fall; negation exact goes above 3 of 12. Stop at midday Day 4 if no clear result. Adopting a model means re-running calibration, policy, parity and Block 58. Measure latency before changing anything.
7. Day 4: backup screen video of the demo (the Gradio link works only while the Colab runtime is alive); run A_predict.py once on a fresh runtime.
8. Day 5 freeze: re-run Block 45 then Block 58, confirm DEMO PARITY: PASS and no warnings; screenshots (five text cases, voice demo, dropdown); update Notion; pipeline diagram slide; slides; rehearsal. No new features.
9. Vishwajeet's items (he does them; Jigar cannot): restore headings of his Blocks 34, 37, 40, 43; say 0.581 is mean macro-F1 over four dev splits; answer whether he fine-tuned his own RoBERTa; copy V_roberta_three_seed_metrics_v2.csv and rb_probs_v2.parquet into shared reports_v2/ (then Jigar re-runs Block 42 only after copying the Drive folder); delete his 23 empty cells.

## 7. Status against the 5-day plan (honest)
About 1.5 of 5 days done, about 1 day verified. Not started: pilot, accuracy experiment, freeze, slides. Biggest risk: nothing has been run in Colab.

## 8. Weak spots to state openly
- Vague answer "It works because of electricity." scored 0 (expected 1) at confidence 0.745, NOT flagged: the only silent failure in the 15 reference cases.
- Partly-right answers are scored wrong but flagged for a teacher.
- Negation: 3 of 12 exact, nine scored "correct".
- NLI evidence panel shows entailment 0.87 to 0.96 on off-topic sentences: do not present it as an explanation for off-topic answers.
- Unseen questions: QWK 0.317. Public data only. Voice demo: adult voices only, child speech untested, transcript errors flow into the score. CBSE questions untested. All demo examples are hand-written sanity checks, not an evaluation.

## 9. Not doing in this window
Adaptive question selection (BM25 plus Elo, Block 56 withdrawn); averaging in Vishwajeet's RoBERTa; CBSE or child-speech accuracy claims; retraining RoBERTa-base; deploying the learned deferral; v3 multi-task cross-encoder and conformal sets (future work).
