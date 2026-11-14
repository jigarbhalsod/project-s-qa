# Child page: "before eval 1" (archived master page, 7 Oct 2026)

Source: https://app.notion.com/p/3f42419db62481aba5d1cc1a0a69e30b (fetched 2 Nov 2026; page last edited 9 Oct 2026).
**Status: ARCHIVE. Superseded by the refined master page (doc 01). Use only to understand what changed and why. Nothing here is current design.**

## What this page was
The project master page exactly as it stood on 7 Oct 2026, before the first literature evaluation round ("eval 1"). Status labels were used so proposed work was not presented as completed results.

## Overview (unchanged in the refined design)
ML-based multimodal oral-reading and comprehension assessment. Reading ("how well does the child read the text?") and Q&A ("how well does the child understand?") are scored separately and combined into an interpretable multidimensional child skill profile, not one unexplained score.

## Old architecture (7 Oct)
- Reading: passage + audio -> speech preprocessing -> speech representation -> acoustic/phonetic/linguistic analysis -> oral reading assessment.
- Q&A: question -> spoken/typed answer -> ASR if spoken -> text/semantic analysis -> Q&A scoring.
- Both -> fusion/profile layer -> child reading skill profile -> dashboard/report.
- Proposed reading pipeline: QC + VAD; word-level ASR (Whisper/Canary/Parakeet) and phoneme/CTC path (WavLM/wav2vec2/HuBERT); reference-aware alignment + error analysis; accuracy / WCPM / pronunciation / prosody.
- Proposed Q&A scorer: lexical evidence (TF-IDF, BM25-style), SBERT similarity, cross-encoder, NLI/entailment, contradiction detection, required-concept coverage, question relevance, ASR confidence for spoken answers, all feeding a **learned classifier** (no arbitrary fixed weights). Output Correct / Partial / Incorrect + flags Contradictory and Irrelevant/no-answer.

## Dataset status on 7 Oct (NNCES)
50 children, ages 8 to 12, about 5,000 recordings, 44.1 kHz 16-bit WAV; 4,990 checked, 1 broken removed, 4,989 usable. No human fluency ratings; reference text for the 10 prompts missing; only 50 speakers.

## Work completed on 7 Oct
Dataset analysis, audio validation, acoustic features (pitch mean/SD, ZCR, pauses), wav2vec2-base-960h frozen embeddings: DONE. Pitch: done but audit required (low values). Age experiment: 5-way age classification about 42.01% +/- 4.61% (speaker-independent 5-fold CV), a side experiment and not a fluency result. Reading accuracy and subjective fluency: BLOCKED. Q&A scoring: proposed. Final profile: proposed.

## Top 7 papers (7 Oct)
Vaidya 2024; Bailly 2022; Fan 2024; Molenaar 2023; "Medin et al. 2025" (**later corrected to Gelin, Medin, Cruel and Liu**); GOPT (Gong 2022); GradeAid (del Gobbo 2023).

## Decisions on 7 Oct
No arbitrary overall score; WER is not enough; mean pitch is not a reading skill (use speaker-normalised contours); Q&A must not use only cosine similarity (negation breaks it); human ratings required for subjective assessment.

## Old blockers and next steps
Blockers: recover the 10 reference texts; fix pitch extraction; manually transcribed subset; reference-based alignment; miscue annotation; human ratings; Q&A question bank, answer keys, rubrics; labelled child Q&A responses; controlled model comparisons.
Next steps in priority order: reference text; ASR bake-off; reading-error detection (word + phoneme); human annotation; Q&A prototype benchmarking lexical, SBERT, cross-encoder, NLI and learned approaches; final profile with confidence.

## What the 7 Oct design had that is now gone
Fixed weights 30/20/20/20/10 into one reading score; example profile scores like 86/100; Q&A as TF-IDF + SBERT cosine in one weighted formula; last-layer frozen wav2vec2 as the speech representation; no uncertainty intervals.

Positioning line (7 Oct): "An ML-based multimodal system that evaluates children's oral-reading performance and comprehension separately, then combines the evidence into an interpretable multidimensional reading-skill profile."
