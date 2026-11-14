# Child page: "Q&A Branch: Next 5 Days: Effective Work Plan (from 31 Oct 2026)"

Source: https://app.notion.com/p/40a2419db62481a0a7c1e50fab76c8f8 (fetched 2 Nov 2026 10:06 UTC; created 31 Oct, later edited with red-team findings). Day 1 = 31 Oct, **Day 5 = 4 Nov (deadline assumed; confirm)**. Labels: (M) measured on dev (optimistic); (P) proposal; (I) inference; (NV) not verified.
**Verdict on the page:** the scorer, demo and parity check are finished. Remaining time goes to a question bank, a voice demo, a small pilot, one gated accuracy experiment, and the freeze. Measured results are in doc 01 section 7.

## 1. Done recently (as of 31 Oct)
- Final scorer v2 built: average of fine-tuned DistilRoBERTa, SBERT+LR and NLI+LR; review when confidence < 0.64 (M).
- Blocks 56, 57, 58 restored in the notebook after an accidental deletion.
- Demo parity PASS 15/15 (max confidence difference 0.0005); same function as the notebook, so consistency, not independent replication.
- Five-case table saved (Block 45b); Gradio demo running (Block 45c); six more hand-written samples tried.
- Block 58 zip fixed (no duplicate manifest entry; 54 files).
- Vishwajeet: four clarifying notes and the 15-row demo file added to his notebook.

## 2. Rules that stay
- Never use Run all. Block 26 has no saved weights, and a full run rewrites frozen v1 files (the 30 Oct run did).
- Select models on dev only; test seen in v1, access log reads 3 evaluations, so every test number is exploratory.
- No hosted model or API (L8). Open-weights models running in Colab are allowed.
- Block numbers never change; keep the FULL backup copy.
- Adopt a model change only if all three gates in doc 04 section 13.7 hold: macro-F1 beats v2 by at least 0.01 with paired interval above 0; unseen-question QWK does not fall; negation exact goes above 3 of 12.

## 3. Day-by-day plan
| Day | Work | Owner | Done when |
| --- | --- | --- | --- |
| 1 (31 Oct) | Close-out items (section 4); latency cell; start question bank | Jigar, Vishwajeet | Checklist ticked; latency numbers recorded |
| 2 (1 Nov) | Finish question bank; add dropdown to Gradio demo; add voice input | Jigar, Vishwajeet | Bank saved as `cbse_demo_questions_v1.csv`; a spoken answer is transcribed and scored |
| 2 to 4 | Collect and label pilot answers (background) | Jigar, Vishwajeet, 5 to 8 volunteers | 100 to 150 labelled answers |
| 3 to 4 (2 to 3 Nov) | One gated accuracy experiment (section 7), only if bank, voice and pilot are on track; learned deferral stays a study (recommended after the 1 Nov red-team check) | Jigar | Gates pass or experiment dropped at midday Day 4; backup demo video recorded |
| 5 (4 Nov) | Freeze: re-run Block 45 then Block 58, final screenshots, update Notion, slides, rehearsal | Both | Parity PASS, status table all DONE, slides done |

## 4. Close-out checklist (Day 1)
### Jigar's notebook
- [ ] Run-history note under the title (30 Oct full run rewrote 18 frozen v1 files and raised test-access count to 3; both confirmed by Block 30 output; note still missing from the 31 Oct notebook).
- [x] Block 26 note ("never run it again"; weights not on Drive).
- [x] Limitations text cell at the end of the notebook (covers the missing RoBERTa-base weights).
- [ ] Add to limitations: the NLI evidence panel shows entailment 0.87 to 0.96 for three of four off-topic sentences, so it is not an explanation for off-topic answers.
- [ ] Run the latency cell; record single-answer and batch milliseconds (cell not in the notebook then; now Block 59 in the COPY, unrun).
- [ ] Add to limitations: the project path is built into `A_predict.py` and must be overridden on a differently named folder.
### Vishwajeet's notebook (only he can do these)
- [ ] Restore original headings of Blocks 34, 37, 40, 43; keep his notes as a second line.
- [ ] In the Block 40 note, say 0.581 is the mean macro-F1 over four dev splits.
- [ ] Answer: did he fine-tune his own RoBERTa or load Jigar's?
- [ ] Copy seed metrics CSV files and `rb_probs_v2.parquet` into shared `reports_v2/` with a `V_` prefix, then re-run Block 42. Block 42 reads any CSV with "seed" in its name that has a `seed` column, so `V_roberta_three_seed_metrics_v2.csv` suffices; until then Block 49 shows "seed summary: pending".
- [ ] Delete the 23 empty cells and the failed first attempt (FileNotFoundError output); cosmetic.
- [ ] Jigar: check Vishwajeet's access level on the shared folder. Viewer is enough; he writes his own files to his Drive and sends them.

## 5. Question bank (Days 1 to 2) (P)
- [ ] Write 20 to 30 questions in own words for Class 4 to 6 science (not copied from NCERT); 10 each.
- [ ] Columns: start from the header of `cbse_question_bank_template.csv` (written by Block 8) so the CBSE adapter plugs in; at least `question_id, class, subject, topic_id, question_text, reference_answer`.
- [ ] Each reference answer 1 or 2 short sentences, one idea per sentence (NLI splits the reference into sentences).
- [ ] Save as `cbse_demo_questions_v1.csv` in `project_s_qa/processed/`. **Do not use `question_bank_v1.csv`:** Block 12 writes it (the 248 public questions) and Block 22's freeze check hashes it.
- [ ] Add a question dropdown to the Gradio demo that fills the question and reference boxes.
- [ ] Label in the demo: untested on CBSE; scorer trained on SciEntsBank and Beetle.
(Status per Jigar 2 Nov: 12 draft questions exist, "draft_unreviewed".)

## 6. Voice input (Day 2) (P)
- [ ] Microphone input in the Gradio demo.
- [ ] Transcribe with a small open-weights speech model in Colab (no API). The reading branch's ASR can be used if Ayush and Safal have it ready.
- [ ] Editable transcript box, then score with `A_predict.predict`.
- [ ] Test about 10 adult recordings (slow, fast, noisy).
- [ ] Tell the panel: adult voices only, child speech not tested, transcript errors flow into the score.
(Status per Jigar 2 Nov: Block 60 written with Whisper-small, unrun.)

## 7. One gated accuracy experiment (Days 3 to 4) (P)
There are no labelled CBSE answers, so "maximum accuracy" cannot be measured on the question bank. Honest ceiling: public-data unseen-question QWK 0.317 (M). Stop at midday Day 4 if no clear result.

| Option | What to do | Cost and risk |
| --- | --- | --- |
| A. Learned deferral (no retraining) | Train gradient-boosting deferral model on all dev rows (Block 54 features), save, let `A_predict.py` use it for the review flag with 0.64 as fallback | 0.815 vs 0.751 accuracy on auto-scored at same 0.306 coverage; interval 0.002 to 0.128; still below 0.85 (M). Needs re-run of policy record, parity, Block 58. **Recommended (1 Nov red-team): do not deploy.** Interval barely clears zero and the threshold was tuned on the same dev data; keep as study |
| B. Stronger model | Fine-tune DeBERTa-v3 cross-encoder from the NLI checkpoint; best epoch on dev; compare with v2 | Higher latency; needs recalibration, policy, parity if adopted. RoBERTa-base tied the ensemble (M). **Drop first if short on time** |
| C. Negation augmentation | Add synthetic negated answers (flagged synthetic) to training only; evaluate on the 36 control sentences | Do not train on the control sentences. (Recommended option) |

- [ ] Before any training: write 30+ new negation sentences kept out of training (12 sentences cannot separate 3/12 from 4/12).
- [ ] Judge the other gates on out-of-fold results over all 177 dev questions, not only the 27 unseen ones (interval 0.199 to 0.412).
- [ ] Choose A, B or C on Day 3 and write it here.
- [ ] Measure latency before changing anything; undo any speed change that moves outputs by more than 0.001.

## 8. Pilot answers (Days 2 to 4) (P)
- [ ] 5 to 8 people type answers to 15 to 20 bank questions.
- [ ] Jigar and Vishwajeet label each answer 0/1/2 separately, **before** running the scorer (blind to its output); report their agreement first; say the labellers also wrote the questions.
- [ ] Day 4: run the scorer; report QWK, review rate and silent failures as a pilot of 100 to 150 answers (not a validation).

## 9. Day 5 freeze
- [ ] Day 4: record a backup screen video of the demo (the Gradio link only works while the Colab runtime is alive).
- [ ] Day 4: run `A_predict.py` once on a fresh runtime (project path is built in).
- [ ] Re-run Block 45 cell, then Block 58; confirm `DEMO PARITY: PASS` and no warnings.
- [ ] Screenshots: five text cases, voice demo, question bank dropdown.
- [ ] Update this page and the master page with final numbers.
- [ ] Slides and rehearsal (no new features on this day).

## 10. Weak spots to state openly (M; hand-written sanity checks, not an evaluation)
| Case | Behaviour |
| --- | --- |
| "It works because of electricity." (bulb question) | Scored 0 (expected 1) at 0.745, **not flagged**; the only silent failure in the 15 reference cases |
| Partly-right answers ("Plants need sunlight.", "The switch is closed.", "Light is quicker.") | Scored wrong, all flagged |
| Negated answers (36-sentence control set) | Exactly right 3 of 12; all 12 flagged; nine scored "correct" |
| NLI evidence panel on off-topic answers | Entailment 0.87 to 0.96 for three unrelated sentences; do not show as an explanation |
| Unseen questions | QWK 0.317 over 27 questions, interval 0.199 to 0.412 |
| 85% accuracy at 30% coverage | Not met (grouped-CV 0.748 at 0.313) |

## 11. Not doing in this window
Adaptive question selection (withdrawn, Block 56); averaging in Vishwajeet's RoBERTa (tie at best; checkpoint not on shared Drive; future work); child-speech or CBSE accuracy claims; retraining RoBERTa-base; v3 (future work); deploying the learned deferral.

## 12. Check against the 5-phase completion roadmap (31 Oct; read-only check of both notebooks, nothing re-run)
| Phase | Item | Status | Evidence / what is left |
| --- | --- | --- | --- |
| 1 Cleanup | Duplicate and empty cells | Mostly done | Jigar: none left. Vishwajeet: 23 empty cells |
| 1 | Missing blocks incl. Block 27 | Done | Blocks 27 and 28 have outputs |
| 1 | Data, labels, splits verified | Done | Blocks 4, 6, 11, 12 |
| 1 | Hard-coded metrics removed | One left | DistilRoBERTa dev F1 constant in Block 26 |
| 1 | Run notebook start to finish | **Do not** | A full run rewrote 18 frozen files; Block 26 needs weights never saved. Reproduce from saved files |
| 2 Models | Majority, TF-IDF, SBERT, NLI, fine-tuned, ensemble; macro-F1, QWK, accuracy; seen/unseen | Done | Blocks 13 to 15, 18, 19, 35, 41, 47 |
| 3 Reliability | Reference answers used | Done | All components read the reference; Block 50 adds per-concept NLI; raw NLI features showed no gain in Vishwajeet's ablation |
| 3 | Multiple seeds | Partly | RoBERTa-base only, in Vishwajeet's notebook; Jigar's seed summary "pending" until CSV copied |
| 3 | Intervals, calibration, abstention | Done | ECE 0.017, threshold 0.64; 85% not met |
| 3 | Cross-dataset | Done on dev | Block 36: Beetle-only scorer on SciEntsBank dev_ua 0.465 macro-F1 vs 0.729 for its own; reverse 0.530 vs 0.700 |
| 4 Demo | Gradio, five answer types, evidence, review flag | Done | Blocks 45b, 45c; link temporary (about a week); parity PASS 15/15 |
| 4 | Tested by Vishwajeet via the link | Not recorded | Ask for screenshots and a short table |
| 5 Panel | Tables, charts with intervals, seen vs unseen, examples | Done | Blocks 46 to 48 (four figures) |
| 5 | Pipeline diagram | Not done | One slide |
| 5 | Limitations and reproducibility notes | Mostly | Add the NLI-evidence caveat |
| 5 | Public data vs future CBSE | Stated | In limitations cell; needs a slide |

Completion criteria: validated metrics, unseen-question evaluation, working demo and honest limitations are in place. Still open: pipeline diagram, slides, careful wording of "improvement over the baseline" (clear over majority and TF-IDF; level with the best single fine-tuned model on unseen questions; see doc 01 section 7).
