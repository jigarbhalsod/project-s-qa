# Child page: "Q&A Branch: Baseline Build" (v1 write-up, last updated 20 Oct 2026)

Source: https://app.notion.com/p/3ff2419db624816eb6dbda8a6afaa5a6 (fetched 2 Nov 2026).
**Status: HISTORY (v1). The numbers here are v1 (abstain threshold 0.75, combiner macro-F1 0.596). The deployed system is v2 (threshold 0.64, equal-weight average, dev QWK 0.432). Do not mix them. See doc 01 section 7 for v2.**

## One line
The Q&A branch reads a child's short written answer and scores it incorrect / partial / correct, with a confidence value and a teacher-review flag. Built and tested on two public datasets because collecting child answers was not possible. Boundary: the branch ends at a structured, interpretable score; fusion into the profile and report writing are downstream.

Design principle: textbooks and syllabi decide what to ask; only expert-labelled student answers can teach a model how to score.

## Headline numbers on this page (v1)
16,003 labelled answers, about 253 questions, 2 datasets; final combiner dev macro-F1 0.596 and QWK 0.464 on 2,049 dev answers; about 70% of the public-data roadmap done (14 of 20 steps, Phase 2 complete).

## Team and scope
Q&A: Vishwajit Sonawane and Jigar Bhalsod. Reading: Ayush Askar and Safal Gawande. **Scope decision:** prove the pipeline on public datasets only (no access to schools or children, no time). The report must show the system works, not tie it to one exam board. CBSE syllabus and answers paused; added later as an extension in the same data format.

## Data
| Dataset | Questions | Answers | Splits (answers) | Licence |
| --- | --- | --- | --- | --- |
| SciEntsBank (school science, 15 domains) | 197 | 10,804 | train 4,969; test_ua 540; test_uq 733; test_ud 4,562 | CC-BY-4.0 |
| Beetle (basic electricity tutoring) | 56 | 5,199 | train 3,941; test_ua 439; test_uq 819 | CC-BY-4.0 |

Each row: question, reference answer, student answer, expert label. Source: SemEval-2013 Task 7 (Dzikovska et al. 2013), English. test_ua = new answers to seen questions; test_uq = new questions (hardest realistic case); test_ud = new domains (SciEntsBank only).

## Labels
correct -> correct (2); partially correct, incomplete -> partial (1); contradictory, irrelevant, non-domain -> incorrect (0). Rules: QWK only on the ordered 3-level labels; the 3-level scheme is custom and must never be compared with published 3-way results; accuracy and macro-F1 also on the original labels.

## How answers are scored (v1 pipeline)
Majority (floor); TF-IDF similarity + logistic regression; SBERT all-MiniLM-L6-v2 similarity and pair-feature LR; NLI (DeBERTa-v3 cross-encoder, each reference sentence checked for entailment/contradiction); fine-tuned DistilRoBERTa on both datasets' training data; combiner (logistic regression stacked on the above, trained on dev predictions); abstain rule (auto-score only when confidence >= 0.75); LLM check (Qwen2.5-3B with rubric prompt on 100 answers per test split; benchmark only, not in the combiner).

## How the test stayed clean
Official test splits locked and never used for tuning; training data divided into train, dev_ua, dev_uq with checks for no shared question or identical answer; all model choices and the abstain threshold on dev only; pipeline frozen and file hashes recorded before test scoring; test scored once and the access logged.

## v1 results
Baselines (macro-F1, original labels, mean over each dataset's test splits): Majority 0.116 (Beetle) / 0.118 (SciEntsBank); TF-IDF similarity only 0.332 / 0.250; SBERT similarity only 0.370 / 0.292; SBERT pair-feature model 0.545 / 0.396.
- Contradictions handled much better: answers that contradict the reference but were scored correct fell from 25.2% (SBERT) to 9.6% (final combiner); NLI drives this.
- Similarity alone is weak (barely beats majority).
- The combiner is not clearly better than a plain average: untrained average of the three models beats the stacked combiner on 4 of 5 test splits and on dev (macro-F1 0.604 vs 0.596); only SciEntsBank test_uq goes the other way (0.378 vs 0.359).
- **New questions remain the weak spot:** QWK on unseen questions 0.480 (Beetle test_uq), 0.494 (SciEntsBank test_uq), 0.480 (SciEntsBank test_ud). Target 0.55 to 0.60 not met. SciEntsBank test_uq macro-F1 on original labels only 0.378.
- Small open LLM is the weakest scorer (accuracy 0.38 to 0.59 on 100 answers per split).
- Teacher-review rule (confidence >= 0.75): dev auto-scored share 35.0%, accuracy 75.6% (85% target not met); test all splits 31.9% and 81.1%; Beetle test_ua 90.4%.
- Cross-check: independent teammate baseline (SBERT on SciEntsBank test_uq) accuracy 0.453, macro-F1 0.301 vs ours 0.450 and 0.312.

## Limitations (v1 page)
Public English data only; 3-level labels are our own mapping; dev splits small (especially unseen-question), so differences of a point or two are noise; NLI "concepts" are reference sentences (the `required_concepts` rubric field is still empty); LLM tested on 100 answers per split only; question type, difficulty and negation tags are auto-generated and unchecked.

## Roadmap on this page (23 steps, 4 phases)
1 Dataset preparation about 86% (open: rubric concepts for about 100 questions, spot-check tags). 2 Baselines 100%. 3 Advanced scoring about 88% (open: NLI with real concepts, retrained combiner, stronger LLM on dev). 4 Extend and validate about 8% (open: third dataset review, generalisation report, speech input, adaptive questions).
Suggested order: decide on ASAP-SAS; generalisation report by domain and question type (no new test look); retrain combiner on out-of-fold predictions and compare on dev only; write required concepts for about 100 public questions; re-run NLI with them; review FairytaleQA licence; speech input (simulate recognition errors); adaptive selection optional.

## CBSE extension (later)
Syllabus list for Classes 4 to 6 exists (123 chapters; 5 titles still to verify against the official textbooks). Needs: a loader into the same format; questions and rubrics in our own words (textbook text cannot be redistributed); real labelled student answers (at least 1,000, ideally 1,800, each rated by two people with kappa >= 0.70); parental consent and ethics approval before collecting any child data.

## Reproducibility (v1)
v1 notebook has 24 blocks; files in Google Drive folder `project_s_qa`; seed 42; manifest with SHA-256 hashes, freeze record and test-access log saved. Frozen reference: combiner dev macro-F1 0.596, QWK 0.464, 2,049 dev answers, threshold 0.75. Further work goes into a v2 notebook; v1 stays untouched; any new test number is "v2, exploratory" because the test splits have been looked at.

Glossary: macro-F1 (average over classes); QWK (agreement for ordered labels, punishes big misses); NLI; abstain (decline to auto-score, send to teacher); dev set (held-out training data for choosing settings).
