# Project S: START HERE (index and working rules for coding agents)

Snapshot: 3 Nov 2026. Built from the Notion master page and its four child pages (fetched 1 to 2 Nov 2026) plus Jigar's message of 2 Nov. Where a fact comes from neither, it is marked **[assistant note]**.

## 1. What the project is (30 seconds)
"Reading Skills Profile Generation of Children": a 7th-semester, 8-credit UG project at IIIT Nagpur. An ML system that assesses (a) oral reading and (b) comprehension (Q&A) separately, then fuses them into an interpretable multidimensional child skill profile. **No overall score; each skill has an uncertainty interval.**

- **Reading branch:** Ayush Askar and Safal Gawande. Dataset NNCES (50 children, ages 8 to 12). Mostly design only; blocked on reference text and human ratings.
- **Q&A branch:** Jigar Bhalsod and Vishwajeet Sonawane (spelled Vishwajit in some places). **This is the branch with built code and results.** It reads a typed answer to a science question and returns score 0/1/2, a confidence, and a teacher-review flag.
- Q&A is built and measured on **public English datasets only** (SciEntsBank + Beetle). CBSE/NCERT is an extension; nothing is validated on CBSE or Indian schoolchildren.

## 2. Read order and which doc is authoritative

| File | What it is | Trust for |
| --- | --- | --- |
| 05_child_next_5_days_plan.md | Current work plan (created 31 Oct, updated 2 Nov) | What to do now |
| 04_child_qa_execution_plan_v2_and_v3.md | 24 Oct plan plus 25 Oct v3 strategy | Rules L1 to L8, contracts, v3 gates. **Sections 1 to 12 are a stale 24 Oct snapshot** |
| 01_master_page_project_overview.md | Whole-project design and status | Reading design, papers, Q&A results (section 5A) |
| 03_child_qa_baseline_build_v1.md | v1 write-up (20 Oct) | History only. **Its numbers are v1 (threshold 0.75, macro-F1 0.596). The deployed system is v2 (threshold 0.64)** |
| 02_child_before_eval_1_archive.md | 7 Oct archive | History only. Superseded |

## 3. Rules (never break these)
From Notion (locked decisions) and from Jigar's 2 Nov message:
1. **Edit only. Never run any cell. Never use Run all.** The 30 Oct Run all rewrote 18 frozen v1 files and raised the test-access count to 3.
2. Work on the **COPY** notebook only. Never touch the original or the backup.
3. Do not edit or delete Blocks 12, 17, 22, 26, 42 or any old duplicate helper cell (editing forces re-runs). Block 26 (RoBERTa-base) has no saved weights; never re-run it. Block 49 reads Block 42's output; Blocks 18 and 24 read Block 17's results.
4. **L8: no hosted LLM or external API for the deployed scorer.** Local open-weights models are fine. No hand-written rule decides a score, flag or review.
5. Select models on **dev data only.** The test splits were already seen in v1; every test number is "exploratory". Dev numbers are optimistic.
6. **Never invent a number.** If it is not in the notebook or a saved file, write "not in notebook".
7. Block numbers never change. New blocks start from **Block 61**. Output files in `reports_v2/` must start with `A_` (Jigar) or `V_` (Vishwajeet). Never overwrite `question_bank_v1.csv` (the 248 public questions; Block 12 writes it and Block 22 hashes it).
8. Before any change: show the plan and wait for "go". After: run integrity checks against the 162-cell reference notebook (match cells by heading and first line, not index).
9. Adopt a model change only if all gates in doc 04 (section 13.7) pass.
10. Say plainly what is not met: unseen-question QWK 0.317 (27 questions) and the 85%-at-30% accuracy target is **not met**.

## 4. Local files (from Jigar, 2 Nov; Notion does not know these)
Folder: `C:\Users\Jigar\OneDrive\Desktop\Project 4` (do not search outside it).
- `Jigar_Q&A_Branch_Baseline.ipynb`: ORIGINAL on disk, untouched. 151 cells (Blocks 45 and 55 were deleted by mistake earlier).
- Original 162-cell notebook (from the Recycle Bin): the REFERENCE for all comparisons.
- `Jigar_Q&A_Branch_Baseline_COPY.ipynb`: the working file, 161 cells.
- `Jigar_Q&A_Branch_Baseline_COPY_before_block60.ipynb`: backup of the copy (159 cells).
- `block_60_voice_demo_cell.py` (68 lines) and `cbse_demo_questions_v1.csv` (12 draft questions, status "draft_unreviewed"): already inserted or verified.

What was done on the COPY (verified by Jigar's earlier session: valid JSON, 161 cells, 149 untouched cells identical, 12 differing): deleted 9 cells from the 162; restored Block 45 and Block 55 heading + code; added a "READ FIRST" cell 0; added provenance notes (Block 45, Block 17, Block 28 heading fix, limitations additions); added **Block 59 (latency, median of 20 runs)**, **Block 60 (question dropdown + local Whisper-small voice input, editable transcript, scored by `A_predict.predict`)** and a read-only "Summary for the panel". **Nothing has been run in Colab yet.**

Pending (from Jigar): (1) read-only accuracy report from saved outputs vs the Notion numbers; (2) Colab runs by Jigar in this order: Summary (last cell), Block 59, Block 60, after backing up Drive folder `project_s_qa` and uploading `cbse_demo_questions_v1.csv` to `project_s_qa/processed/`; (3) review the 12 draft questions (Jigar and Vishwajeet); (4) one gated accuracy experiment (recommended: Option C, negation augmentation, with 30+ new negation sentences kept out of training); (5) Day 5: re-run Block 45 then Block 58, confirm DEMO PARITY: PASS, screenshots, slides, pipeline diagram.

## 5. Current Q&A status in ten lines (all (M) = measured in Jigar's notebook on dev; optimistic)
- Deployed scorer v2: equal-weight average of fine-tuned DistilRoBERTa, SBERT+logistic regression and NLI+logistic regression ("pooled"). Files: `A_predict.py`, `A_abstain_policy_v2.json`, `pooled_lr_v2.joblib`.
- Review rule: teacher review when calibrated confidence < 0.64. Temperature 1.00, ECE 0.017.
- Dev QWK 0.432 (0.358 to 0.509); seen answers 0.630 (0.562 to 0.692); **unseen questions 0.317 (0.199 to 0.412) over only 27 questions**.
- Dev accuracy on auto-scored answers 0.751 at coverage 0.306. Grouped-CV estimate 0.748 at 0.313. **85% at 30% target not met.**
- Exploratory test (test already seen): QWK 0.454; accuracy 0.790 on auto-scored at coverage 0.288.
- Controls (36 hand-written): paraphrase 12/12, spelling 12/12, **negation exact only 3/12 (all flagged)**.
- 15 reference cases: 11 exact, 14 safe, 1 silent failure (c15: "It works because of electricity." scored 0, expected 1, confidence 0.745, not flagged).
- Demo parity PASS 15/15 (max confidence difference 0.0005). Same function as the notebook, so this shows consistency, not independent replication.
- Learned deferral study (gradient boosting): 0.815 vs 0.751 at equal coverage, interval 0.002 to 0.128. Study only; not deployed.
- Latency: not measured yet (Block 59 is written but not run).

## 6. Known stale items and conflicts [assistant notes]
- Doc 04 section 13.1 says Blocks 53 to 58 are "written, not run". Jigar's notebook (read 30 Oct) shows Blocks 50 to 55, 57 and 58 had run; Block 56 was withdrawn. Section 1 of doc 04 is the 24 Oct snapshot.
- **Block-number collision:** doc 04 section 13.8 reserves Blocks 59 to 70 for the v3 plan, but the COPY notebook now uses 59 (latency) and 60 (voice), and says new blocks start at 61. If v3 is built, renumber its plan.
- Doc 03 (v1) says abstain threshold 0.75 and macro-F1 0.596; v2 deployed values are 0.64 and QWK 0.432. Do not mix them.
- Block 17 (prompted Qwen2.5-3B) is a dev-only side result excluded from the deployed scorer. Earlier notes say it installs the `anthropic` package but its backend was local with an unused API branch. Check the cell's backend line before writing any note that says it "uses an API call".
- A_predict.py has the project path `/content/drive/MyDrive/project_s_qa` built in; it must be overridden on a differently named folder.
- The per-idea NLI evidence can be confidently wrong on off-topic answers (entailment 0.87 to 0.96 on three unrelated sentences). Do not present it as an explanation for off-topic answers.
- Vishwajeet's RoBERTa is a separate fine-tune (mean dev macro-F1 0.610 vs 0.584 for Jigar's); his three-seed average is about 0.558. Not comparable and not part of the final scorer.

## 7. Vocabulary
- `A_` / `V_`: file prefixes for Jigar / Vishwajeet. Blocks named A27, A28 / V27 to V44.
- Splits: `dev_ua` unseen answers (seen questions), `dev_uq` unseen questions, `test_ua`, `test_uq`, `test_ud` (unseen domain; SciEntsBank only). Dev = 2,049 answers over 177 questions. Test = 7,093 answers over 248 questions.
- Labels: 5 official (correct, partially_correct_incomplete, contradictory, irrelevant, non_domain). Ordered 3-level score: incorrect 0 (contradictory, irrelevant, non_domain) < partial 1 < correct 2. QWK only on the 3-level score.
- Evidence labels: (E) established in a paper read; (P) proposal; (I) inference; (M) measured in Jigar's notebook on dev; (doc) number from the earlier research document, not re-checked; (NV) not verified.
- Notion URLs: master https://app.notion.com/p/3f22419db624810a9157f08b897a088a ; execution plan https://app.notion.com/p/4032419db62481a6b1eceb7eb6a25bab ; baseline https://app.notion.com/p/3ff2419db624816eb6dbda8a6afaa5a6 ; next 5 days https://app.notion.com/p/40a2419db62481a0a7c1e50fab76c8f8 ; archive https://app.notion.com/p/3f42419db62481aba5d1cc1a0a69e30b
