# Project S, Q&A branch: full context (state as of 3 Nov 2026, Day 4 of 5)

## 1. Date and deadline
Date: Day 4 = 3 Nov 2026
Plan days: Day 1 = 31 Oct, Day 2 = 1 Nov, Day 3 = 2 Nov, Day 4 = 3 Nov (today), Day 5 = 4 Nov (freeze, ASSUMED deadline; confirm with Jigar). Earlier chat messages wrongly treated 2 Nov as today. Honest progress: about 1.5 of 5 plan-days done, nothing verified by running in Colab. Roughly 2.5 days behind.

## 2. Project
Project S builds an interpretable reading-skills profile for children (ages 8 to 12). Reading and comprehension are reported separately. There is no single total score. Each skill has its own uncertainty interval and a teacher-review flag.
- Reading branch (Askar and Safal): design stage. Reference text, transcripts and human ratings are missing, so most experiments are blocked. Askar baseline: age classification 42.01% +/- 4.61% (from Notion, unverified here).
- Q&A branch (Jigar Bhalsod and Vishwajeet Sonawane): built and measured on public English data (SciEntsBank, Beetle). Not measured on NNCES or CBSE. Jigar owns architecture, Q&A scoring, profile layer and evaluation. Vishwajeet's notebook is his own; Jigar cannot edit it.
- Jigar: B.Tech CSE, IIIT Nagpur, 2027, ML/GenAI/RAG track. The panel is academic: explain simply.
- Notion master page: "Reading Skills Profile Generation of Children, Project Master Page" (last updated 31 Oct 2026, Q&A results in section 5A). Child page: "Q&A Branch: Next 5 Days, Effective Work Plan (from 31 Oct 2026)". Published numbers from other papers are hypotheses until tested on our data.

## 3. Tool history (what each assistant did)
- Claude chat (this thread): reviewed the notebook; wrote the Summary section code, the Block 60 cell and the 12-question CSV; wrote every prompt below; ran a read-only diagnosis on the 162-cell notebook (section 8).
- Antigravity (ran out of tokens): found the clean 162-cell notebook in the Windows Recycle Bin (file named like $RK1WTDE.ipynb); compared it with the 151-cell file; explained 162 vs 151; restored the four cells deleted by mistake; built the COPY; made all edits in section 6; added Blocks 59 and 60 and the Summary; ran integrity checks; created a backup; probably produced extracted_A_predict.py and comparison_table.json (unverified).
- Cursor (limit hit): created .cursor/rules/project-s.mdc (alwaysApply true; safety rules plus a short Project S snapshot, content not read by Claude) and an earlier PROJECT_CONTEXT.md (9 sections). It reported that reference/ did not exist. Its reference-hash check, copy-vs-reference comparison and read-only diagnosis were NOT done.
- Codex (now): you. This file and AGENTS.md replace the Cursor files as the source of truth.

## 4. Folder layout
Project 4/
  AGENTS.md
  PROJECT_CONTEXT.md
  README_FILES.txt
  .AI/ (leave exactly as it is)
  notebooks/
    Jigar_Q&A_Branch_Baseline_COPY.ipynb (165 cells; only editable file)
    backups/
      Jigar_Q&A_Branch_Baseline_COPY_before_block60.ipynb (159 cells; read-only)
      Jigar_Q&A_Branch_Baseline_COPY_before_block61.ipynb (161 cells; read-only)
    reference/
      Jigar_Q&A_Branch_Baseline_REFERENCE_162.ipynb (not yet present; Jigar adds it)
      Jigar_Q&A_Branch_Baseline.ipynb (151-cell original; read-only)
  block60/
    block_60_voice_demo_cell.py
    cbse_demo_questions_v1.csv
  tools/
    extracted_A_predict.py
    comparison_table.json
  archive/
    project_s_qa_phase1_v1.zip
    project_s_qa_final_v1.zip
  README.md
  .gitignore
Paper folders are not in Project 4.

## 5. Notebook versions
- REFERENCE (clean, 162 cells, 70 code cells, 3,798 code lines; 92 markdown). sha256 f2991cf09f431a3110101d388610149728643c140e55e1e43d83fc5c53922cda. Single source of truth for comparisons.
- ORIGINAL on disk: 151 cells. Blocks 45 (heading plus parity code) and 55 (heading plus policy code) were deleted by mistake in an earlier manual edit. Not clean v1 history.
- BACKUP before Block 60: 159 cells.
- COPY: 161 cells. Verified by script (Antigravity): valid JSON; 149 untouched cells identical in source, outputs and execution counts; 12 differing cells (8 new, 4 edited). Note: an earlier message said 150 untouched; 149 is correct.
- Block 60 file: block_60_voice_demo_cell.py, 68 lines, 3,680 bytes, sha256 cb082b77f2536c234310b3f8e230415f4d07a8ef8be4a1ca3c2337f98409d6c5 (matches the code cell byte for byte).
- Cell numbering in the reference: Block N heading, then its code cell right after. Block 41 code is cell 109, Block 47 cell 133, Block 49 cell 137.

## 6. What was changed in the COPY (from the 162 reference)
Voice input and the question bank are DRAFTED, not tested or done, until Jigar reports the Colab run.
Deleted (9 reference cells): 0, 1, 2 (basic-checks heading, memory cleanup, GPU check); 120 and 122 (Block 45 timestamp checks of demo_outputs.json and demo_outputs_PREVIOUS.json); 153 (Block 55 file check; no later cell uses it); 154 (RoBERTa folder file listing); 155 and 156 (Block 56 "withdrawn" heading and code; the cell wrote a small JSON note nobody reads).
Restored from the reference after the mistaken deletion: 118 and 119 (Block 45 heading and parity code), 151 and 152 (Block 55 heading and policy code).
Copy cell map (copy indices):
- 0 NEW markdown "READ FIRST: what to run and what not to run": never Run all; run only the Summary (last cell), then Block 59, then Block 60; do-not-run list (Blocks 1 to 11, 17, 18 to 21 and 26, 22 to 24, 41 and 42, demo cells, reporting blocks 47 to 49 and 58); how to re-run one block safely; what to do if the Summary prints MISSING; run history (30 Oct full run rewrote 18 frozen v1 files and raised the test-access count to 3).
- 43 EDIT Block 17 heading: note "Dev-only side result. It uses an API call and is not part of the deployed scorer." (Cell 46 of the reference installs the anthropic package and sets a Claude haiku model name; the Notion page says no hosted model. The note resolves this for panel readers.)
- 72 EDIT Block 28 heading: stray ")" removed.
- 118 NEW markdown, Block 45 provenance: "demo_outputs.json was regenerated on 31 Oct (06:46). Vishwajeet's earlier file is kept as demo_outputs_PREVIOUS.json."
- 124 EDIT Block 45c Gradio cell: only the description string changed. Removed the unsupported clause "it is reliable for related answers but". New text: "The evidence shown is the model's own NLI output and can be misleading for off-topic answers." Outputs and execution count unchanged.
- 154 and 155 NEW Block 59 latency: prints runtime hardware (GPU name or CPU), loads A_demo_reference_outputs_v2.json, 1 warm-up then 20 timed runs with time.perf_counter, median (ms) for a single answer (case 1) and a batch of 15, per-item median. It calls predict with dataset=scorer_mode read from the JSON (value "pooled"). It writes nothing, prints only.
- 156 and 157 NEW Block 60 voice demo (section 9).
- 158 EDIT Limitations cell: added "The NLI evidence panel shows entailment 0.87 to 0.96 for three of four unrelated sentences, so it cannot be presented as an explanation for off-topic answers." and "A_predict.py has the Google Drive project path (/content/drive/MyDrive/project_s_qa) hard-coded and must be overridden when executing from a differently named folder." Existing bullets kept (unseen QWK 0.317, 85% at 30% target unmet).
- 159