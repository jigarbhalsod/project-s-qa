# Agent rules for Project S (Q&A branch). Read PROJECT_CONTEXT.md before every task.

## Hard rules
1. Edit ONLY the working copy notebook (notebooks/Jigar_Q&A_Branch_Baseline_COPY.ipynb). Everything else is read-only: the 151-cell original, the 162-cell reference, the backup (before_block60), both zips, extracted_A_predict.py, comparison_table.json, the paper folders, and the Block 60 files unless I ask.
2. NEVER run a notebook cell. NEVER "Run all". It rewrote 18 frozen v1 files on 30 Oct and raised the test-access count to 3. Do not run Python that imports torch, transformers, sentence_transformers, A_predict or extracted_A_predict. Reading those files as text is fine.
3. Edit notebooks only with a small Python script using the json module: load, change only the listed cells, keep every other cell byte-identical, keep outputs and execution_count unchanged, keep the file's JSON indent and key order, write to a temp file, validate it, then replace. Never rewrite the whole notebook by hand. Never paste a notebook into chat (3 MB, mostly outputs).
4. Before any edit: show the plan (cell index, block, old text, new text) and WAIT for my "go". After any edit: integrity check against the reference (valid JSON, cell count, number of untouched cells with identical source/outputs/execution counts, list of every differing cell with index and first 60 characters).
5. Match cells by heading and first line of code, NEVER by index. Indices differ between the 162 reference, the 151 original, the 159 backup and the 161 copy.
6. Never edit or delete Blocks 12 and 22 (manifest, freeze check), Block 17 (its in-memory LLM_PRED is used by Blocks 18 and 24), Block 26 (only record of the RoBERTa-base run; weights were never saved), Block 42 (Block 49 reads its seed summary), or the old duplicate helper cells (to3, met, sha256, boot, make_qid, pick, nli_X, predict_probs, ens, md, rc). Editing them forces a re-run.
7. Never re-run or modify the blocks that write frozen v1 files: Blocks 19, 20, 21, 25, 28 (they write ft_probs_v1.parquet, combiner_v1.joblib, stack_features_v1.parquet, abstain_config_v1.json, scored_dev_v1.parquet). Any new experiment = NEW cells writing NEW files.
8. New blocks start at Block 61 (59 and 60 exist). New files written to reports_v2/ start with "A_". Never overwrite question_bank_v1.csv (Block 12 writes it, Block 22 hashes it). Never edit A_predict.py on Drive (its sha256 is stored in A_demo_reference_outputs_v2.json). Put speed variants in a NEW file (A_predict_fast.py).
9. Rule L8: no hosted LLM, no external API in the deployed scorer. Local open-weights models in Colab are allowed.
10. Numbers: never invent, estimate or round up. If a number is not in the notebook, write "not in notebook". Test numbers are "exploratory (test seen in v1)". Dev numbers are "dev, optimistic". Do not compute a plain overall accuracy for the panel if the notebook does not report one. Do not train on the 36 negation control sentences.
11. No network calls, no pip installs, no git push, no file deletion, no moving files unless I ask in that message. Use the most restrictive sandbox and approval setting. Ask before any command that writes.
12. If anything is unclear, ask one short question. Do not guess.

## How to talk to me
Direct, simple English (the audience is an academic panel). Short answers. No softened feedback. No unsolicited tangents. Say what you verified and what you did not. If you are unsure, say "unverified".

## Efficiency
- Reuse before writing: existing notebook cells, library functions, and documented recipes take priority; the Summary cell already loads saved files.
- Smallest change that works: one script per task, 20 lines maximum, no helper layers, and at most one comment line.
- Notebook work: use nbformat for read, validation, and write; use nbdime (`nbdiff`) for comparisons. Ask once before pip-installing either.
- Report only: cell index, first 60 characters, and pass/fail; explain only if asked.
Source of truth = AGENTS.md and PROJECT_CONTEXT.md. Files in .AI\AI context are background only; on any conflict, ours win. Do not re-read them unless I ask.
