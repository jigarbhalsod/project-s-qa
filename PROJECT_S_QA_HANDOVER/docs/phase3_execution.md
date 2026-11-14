# Phase 3 evidence procedure

**Source:** `evidence/phase3/PHASE3_RUNBOOK_v2.md` and
`evidence/phase3/phase3_check_evidence_v2.py`, copied from the project.

1. Jigar chooses the notebook and verifies Drive paths and frozen hashes.
2. Select a T4 runtime, mount Drive, and verify the project root.
3. Run only the authorized fresh-runtime check and selected demo blocks; never
   Run All, Block 49, or cell 166.
4. Complete the five typed cases and ten adult voice runs exactly as specified
   in the runbook. Treat them as interface/ASR checks, not accuracy evidence.
5. Record score, confidence, review flag, errors and Block 62 timings.
6. Save the executed notebook under a new name; capture screenshots and the
   short backup video without overwriting existing evidence.
7. Download the fresh-runtime log and all evidence into a new Phase 3 folder.
8. Run the local evidence checker only after the files are present. Preserve
   its actual report, including any missing-item results.

**Current local audit:** no PNG/JPG or video media was found in
`Project_S_QA_Evidence/Phase_3/`. A Phase 2 `voice_runs_reported.txt` exists;
it is included as user-reported notes, not independently measured evidence.
No aggregate voice-run rate is claimed. Phase 3 is not complete.
