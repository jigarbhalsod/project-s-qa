Project S, Q&A branch. Day 4 = 3 Nov 2026.
Rule: edit ONLY the COPY notebook.
Never run a cell outside the planned order. Never "Run all".

AGENTS.md
What: rules for every coding agent (what to edit, what never to run)
Why needed: read first
Edit?: only on request

PROJECT_CONTEXT.md
What: full project state: results, changes, pending work
Why needed: gives an agent the context
Edit?: update after each session

README_FILES.txt
What: this guide
Why needed: quick map of the folder
Edit?: update when files move

notebooks/Jigar_Q&A_Branch_Baseline_COPY.ipynb
What: working notebook, 165 cells (Blocks 59 to 62 and Summary added)
Why needed: upload THIS to Colab
Edit?: the only editable file

notebooks/backups/Jigar_Q&A_Branch_Baseline_COPY_before_block60.ipynb
What: snapshot, 159 cells
Why needed: to undo edits
Edit?: read-only
notebooks/backups/Jigar_Q&A_Branch_Baseline_COPY_before_block61.ipynb
What: snapshot, 161 cells
Why needed: to undo edits
Edit?: read-only

notebooks/reference/Jigar_Q&A_Branch_Baseline_REFERENCE_162.ipynb:
NOT YET PRESENT (Jigar adds it)
What: clean 162-cell notebook
SHA256: f2991cf09f431a3110101d388610149728643c140e55e1e43d83fc5c53922cda
Why needed: to check that only planned cells changed
Edit?: read-only

notebooks/reference/Jigar_Q&A_Branch_Baseline.ipynb
What: 151-cell file; Blocks 45 and 55 were deleted by mistake
Why needed: history only, not the truth
Edit?: read-only

block60/block_60_voice_demo_cell.py
What: Block 60 source (question dropdown + local Whisper voice input)
Why needed: already inside the COPY; source reference
SHA256: cb082b77f2536c234310b3f8e230415f4d07a8ef8be4a1ca3c2337f98409d6c5
Edit?: read-only

block60/cbse_demo_questions_v1.csv
What: 12 draft CBSE-style questions, not reviewed
Why needed: upload to Drive project_s_qa/processed/ for Block 60
Edit?: edit after review

tools/extracted_A_predict.py
What: local scorer copy; older than Drive version (lacks pooled mode)
Why needed: to read function names
Edit?: read-only

tools/comparison_table.json
What: comparison table JSON; contents not inspected
Why needed: not specified in supplied facts
Edit?: read-only

archive/project_s_qa_phase1_v1.zip
What: ZIP archive; not opened
Why needed: not specified in supplied facts
Edit?: read-only

archive/project_s_qa_final_v1.zip
What: ZIP archive; not opened
Why needed: not specified in supplied facts
Edit?: read-only

README.md: # reading-skills-profile-generation
.gitignore: *.zip
