# Child page: "Q&A Branch: Execution Plan v2 and Member-wise Work Distribution"

Source: https://app.notion.com/p/4032419db62481a6b1eceb7eb6a25bab (fetched 2 Nov 2026; created 24 Oct, updated 25 Oct). Written for Jigar and Vishwajeet, who work in **two separate notebooks** and integrate through shared files on Google Drive, not each other's code.
**Sections 1 to 12 are the 24 Oct v2 plan, left as written (stale in places). Section 13 (25 Oct) is the current status and the v3 strategy. Locked decisions L1 to L8 are current.**
Labels: (M) measured in Jigar's notebook on dev (optimistic: best epochs picked on dev, single seed); (NV) not verified (Vishwajeet's notebook had no saved outputs on 24 Oct); (P) estimate. Day numbers are relative.

## 1. Where the branch stood on 24 Oct (stale snapshot)
- DONE (Jigar): data, labels, splits, source register, question bank (248 public questions), rubric stubs (Blocks 1 to 12); baselines Majority/TF-IDF/SBERT (13 to 15); NLI features, NLI classifier, small-sample LLM scorer on 100 to 250 rows per split (16 to 18); fine-tuned DistilRoBERTa, stacked combiner, abstain rule (19 to 21); locked test evaluation, error analysis, final package (22 to 24; test already inspected); stronger ensemble weights and RoBERTa-base (25, 26; RoBERTa-base beat DistilRoBERTa on dev in all 4 splits); non_domain needs-review flag (A27); final scorer selection on dev (A28; current ensemble kept, RoBERTa swap not established).
- Vishwajeet: V27 to V44 code written, outputs unverified then.
- NOT DONE then: calibration/validated abstain policy, `required_concepts`, inference function and Gradio demo, panel material.

Dev macro-F1 (5 labels), (M):
| Model | Beetle dev_ua | Beetle dev_uq | SciEntsBank dev_ua | SciEntsBank dev_uq | Mean |
| --- | --- | --- | --- | --- | --- |
| DistilRoBERTa (ft) | 0.653 | 0.447 | 0.692 | 0.335 | 0.532 |
| RoBERTa-base (rb) | 0.688 | 0.495 | 0.747 | 0.408 | 0.584 |
| Ensemble ft + SBERT + NLI (current) | 0.700 | 0.490 | 0.729 | 0.412 | 0.583 |
| Swap rb + SBERT + NLI | 0.688 | 0.521 | 0.753 | 0.444 | 0.602 |
| Four-model average | 0.683 | 0.487 | 0.751 | 0.416 | 0.584 |

Paired question-level bootstrap vs current ensemble (177 dev questions, 1,000 resamples): DistilRoBERTa -0.047 (-0.068 to -0.028, clearly worse); RoBERTa-base -0.002 (-0.036 to 0.032, tie); swap +0.018 (-0.001 to 0.039, not established, loses 0.012 on Beetle dev_ua); four-model average +0.003 (-0.018 to 0.023, no gain). QWK (3-level) for the ensemble was 0.670 / 0.627 on seen questions (Beetle / SciEntsBank) but 0.404 / 0.339 on unseen questions: below the 0.55 to 0.60 expectation.

Problems found then: notebooks disagree on the final scorer; block numbers collide (both have Block 27 and 28); same filename different content (`scored_dev_v2.parquet` in `reports/` vs `reports_v2/`); different review rules (Jigar's calibrated 3-level confidence vs Vishwajeet's uncalibrated 5-way max probability at 0.75); freeze warning on `abstain_config`; test-access log may read "0 evaluations"; 85% at 30% target unmet (v1: 75.6% dev, 81.1% test at about 32% coverage).

## 2. Decisions
### Locked (do not reopen)
- **L1** non_domain keeps score 0 and gets a separate `needs_review` flag.
- **L2** v1 files frozen; every new result goes to a `_v2` file.
- **L3** Select models on dev only; test splits already inspected in v1, so further test results are "exploratory, test already seen in v1".
- **L4** English only. Synthetic answers, if ever used, flagged "synthetic", train-only, never in dev/test.
- **L5** QWK only on the ordered 3-level labels; accuracy and macro-F1 on official labels.
- **L6** CBSE is an extension; only clearly labelled untested demo items.
- **L7** The rubric-prompted LLM is a small-sample side result, not the final scorer (100 to 250 rows per split).
- **L8** (25 Oct) **Q&A scorer is completely ML/DL.** No external API or hosted LLM. No hand-written rule decides a score, flag, tag or review. Pretrained open-weight models fine-tuned and run locally are allowed. Rules allowed only as data plumbing (e.g. splitting text into sentences). L7 is met by the local 3B model of Block 17; the API block (Block 52) is dropped.

### To settle (Day 1 call)
- **D1 final scorer:** keep the current ensemble unless Vishwajeet's 3-seed RoBERTa mean beats it by at least 0.01 macro-F1 on average, is positive on at least 3 of 4 dev sets, and the paired bootstrap interval is above 0. If it ties, keep the ensemble. Demo may use RoBERTa alone only if the artifact inventory (J2) shows the ensemble cannot be reloaded reproducibly, and then says "single-model mode". (Rule set before the 3-seed results; switching afterwards is rule-shopping.)
- **D2 review policy:** Jigar's calibrated 3-level rule from J3. Vishwajeet's "predicted non_domain" flag is added as an extra reason only if his precision/recall check (V4) supports it.
- **D3 predict() format:** see 3.3.
(Outcome per later notes: D1 = ensemble kept; D2 = 0.64 confidence rule.)

### Panel wording
Say the built system is a fine-tuned + NLI + SBERT ensemble (not the proposed rubric LLM); report unseen-question QWK (about 0.34 to 0.40 on 24 Oct) as the main limitation; public English science datasets do not show CBSE/NCERT or Indian-schoolchildren performance.

## 3. How two notebooks work together
1. Jigar's `Q&A_Branch_Baseline.ipynb` is the v1 history; nobody edits Blocks 1 to 26.
2. Vishwajeet's notebook is his own copy; do not merge his copy of Blocks 1 to 26 over Jigar's (it lacks saved outputs).
3. Each person writes only their own files in `reports_v2/`: prefix `A_` (Jigar) or `V_` (Vishwajeet).
4. Block names: Jigar's new blocks A27, A28, A29...; Vishwajeet's V27, V28...; rename his headings so no two blocks share a number.
5. Hand over through **contract files**: inference function + artifacts (`A_predict.py` + model files, Jigar); policy (`A_abstain_policy_v2.json`, Jigar); demo rubrics with concepts (`V_rubrics_demo_v2.json`, Vishwajeet); seen/unseen evidence (`V_seen_unseen_bootstrap_v2.csv`, Vishwajeet).
6. Save notebook outputs before downloading.

### predict() contract (section 3.3; unchanged in v3 except `model_version`)
```py
predict(question: str, reference_answer: str, student_answer: str) -> dict
{
  "pred_label": "correct" | "partial" | "incorrect",
  "pred_score": 0 | 1 | 2,
  "confidence": float,                      # 3-level confidence
  "p_incorrect": float, "p_partial": float, "p_correct": float,
  "needs_teacher_review": bool,
  "review_reasons": ["low_confidence", "possible_contradiction", "likely_off_topic"],
  "nli": {"entail": float, "contradict": float},   # real model outputs, not an LLM story
  "model_version": "v2-<name>"
}
```
No LLM-written explanations of predictions; the demo shows real scores and NLI evidence. (Implemented review reasons: `low_confidence` only; the other two are not implemented.)

### Drive layout (`project_s_qa/`)
`reports/` frozen v1 outputs (read-only); `interim/` features, checkpoints, probability files; `reports_v2/` all new results prefixed `A_`/`V_`; `demo/` `A_predict.py`, Gradio app, example inputs.

## 4. Jigar's tasks (J1 to J8)
| ID | Task | Output | Time (P) |
| --- | --- | --- | --- |
| J1 | Housekeeping: check whether Block 25 overwrote `abstain_config` (Block 12 hash manifest); fix test-access log; add "Run order and required artifacts" cell; fix stray `)` in A28 heading; remove empty last cell; rename colliding `scored_dev_v2` | clean notebook | 0.5 d |
| J2 | Inference function: first list model files on Drive (DistilRoBERTa checkpoint, SBERT features/classifier, NLI classifier, `combiner_v1.joblib`); write `predict()`; parity on 20 dev rows (tolerance e.g. 0.001) | `A_predict.py`, parity table | 1.5 d |
| J3 | Calibration and abstain policy (reliability diagram, ECE/Brier, temperature scaling, re-pick threshold; report coverage, accuracy on auto-scored, share to review, accuracy on reviewed subset) **using question-grouped CV** | `A_abstain_policy_v2.json`, `A_risk_coverage_v2.csv`, figures | 1.5 d |
| J4 | One exploratory test run with J3 policy, labelled "exploratory, test already seen in v1" | `A_scored_test_v2.parquet`, `A_test_results_v2.csv` | 0.5 d |
| J5 | Final comparison table (Majority, TF-IDF, SBERT, NLI, DistilRoBERTa, RoBERTa-base, simple average, stacker), by dataset and by seen / unseen-question / unseen-domain, paired bootstrap intervals with number of questions | `A_model_comparison_v2.csv` + chart | 1 d |
| J6 | Integration notebook that only loads saved files and prints final tables | `Q&A_Integrated_v2.ipynb` | 1 d |
| J7 | Review Vishwajeet's rubrics (authors never verify their own items) | review notes | 0.5 d |
| J8 | Architecture diagram, slides, update master page sections 7.3, 13, 18 | slides, page edits | 0.5 d |

## 5. Vishwajeet's tasks (V1 to V7)
V1 verify and publish results (run V44 audit; share `roberta_three_seed_metrics_v2.csv`, NLI ablation, bootstrap table; save outputs in notebook). V2 rename and renumber (V27 to V44; RoBERTa-only file becomes `V_scored_dev_roberta_v2.parquet`). V3 rubric layer: `required_concepts` (1 to 4 atomic ideas) for 10 to 15 demo questions covering correct/partial/contradictory/irrelevant/ambiguous; LLM draft edited by a person; 3 to 5 CBSE-style questions in own words labelled untested; never copy textbook sentences; per-concept NLI as present/missing/contradicted (`V_rubrics_demo_v2.json`). V4 off-topic signal: test his "predicted non_domain" rule and a second signal (low NLI entailment + low similarity) for precision/recall on dev (only 69 true cases) (`V_offtopic_signal_v2.csv`). V5 negation and paraphrase control set (E12): 30 to 40 hand-made triples (answer, paraphrase, negation) plus spelling variants. V6 Gradio demo: build against a fake `predict()` first, then the real one; test 10 to 15 answers; outputs must match the notebook. V7 write-up: error patterns, NLI ablation (E10), 3-seed result, 3 good + 3 bad examples.

## 6. Shared tasks
S1 Day-1 call (D1 to D3); S2 slides (pipeline diagram, comparison table, seen vs unseen chart, good/bad examples, limitations); S3 limitations slide and rehearsal; S4 final freeze (numbers copied from saved files only).

## 7. Day-by-day (relative)
Day 1: S1 call; J1; start J2 inventory | V1; start V6 with fake predict (G1: D1 to D3 decided). Day 2: J2 + parity; start J3 | V2; start V3. Day 3: finish J3 | finish V3; V4 (G2: three contract files exist). Day 4: J7; J4 | V5; switch V6 to real predict. Day 5: J5; J6 | V6 tests and parity; V7 (G3: demo reproduces notebook). Day 6: J8; S2 | S2 (G4: freeze). Day 7: buffer, rehearsal.

## 8. Mapping to master-page experiments
E9 mostly done (Jigar); E10 NLI ablation with question-grouped CV (Vishwajeet, V41 to V43); E11 deferred (reading branch ASR); E12 V5; E13 to E15 deferred; E16 not applicable (no age/gender fields); E17 text version only (negation, paraphrase, spelling).

## 9. Priorities if time runs short
Must: J2 predict() with parity; J3 calibration + plain statement on the 85% target; J5 comparison table with seen vs unseen; V6 demo with 10 to 15 tested examples; limitations slide. Should: V3 rubric concepts; V5 negation/paraphrase; J4 exploratory test run. Cut first: V4 off-topic signal; 3 CBSE-style demo questions; extra seeds; pooled training; per-concept NLI beyond demo set.

## 10. Risks
Model files not saved loadably (medium; fallback single-model demo labelled as such); Vishwajeet's outputs not on Drive (medium; V1 Day 1); 85% target unmet (high; state plainly); unseen-question results weak (high; show honestly; do not tune on test); wide intervals (only 9 Beetle and 15 SciEntsBank unseen test questions; report number of questions); file overwrites (low with prefixes); wrong LLM-drafted rubric concepts (medium; second-person review J7).

## 11. Definition of done (checkboxes, original)
D1 to D3 decided; freeze warning explained and test-access log corrected; `predict()` reproduces stored probabilities on 20 dev rows; calibration + policy saved with plain statement on 85%; final comparison table by dataset and seen/unseen; rubric concepts written and reviewed; Gradio demo works on 10 to 15 answers and matches notebook; negation/paraphrase pass rate reported; one exploratory test run labelled as such; integration notebook runs from saved files on a fresh runtime; master page updated (7.3, 13, 18); slides, limitations slide, one rehearsal.

## 12. Caveats
Every dev number optimistic; v1 test numbers are not a fresh evaluation; Vishwajeet's numbers unverified until V1; public English data does not show CBSE/NCERT or Indian-schoolchildren performance; NCERT textbooks stay private (demo questions in own words); time estimates are guesses.

---
# 13. Pure ML/DL strategy (v3), added 25 Oct 2026

## 13.1 Status on 25 Oct (from Jigar's notebook) [stale in parts: see doc 00 section 6]
| Item | Status | Evidence |
| --- | --- | --- |
| J1 housekeeping | DONE | freeze check: only `created` timestamp differs for abstain config; test-access log reads 2 evaluations |
| J2 predict() + parity | DONE | PASS: same predicted score on 20/20 dev rows, max probability difference 0.0006 |
| Deployed scorer | DONE | pooled average of fine-tuned DistilRoBERTa, SBERT-LR, NLI-LR; dev QWK 0.432 (0.358 to 0.509); seen 0.630 (0.562 to 0.692); unseen 0.317 (0.199 to 0.412) over 27 questions |
| J3 calibration + policy | DONE, target not met | ECE 0.017, temperature 1.00, confidence-only policy threshold 0.64; **85% at 30% not met**: grouped-CV about 0.748 at 0.313 |
| J4 exploratory test | DONE, exploratory | all test QWK 0.454; accuracy 0.790 on auto-scored at 0.288 coverage |
| J5/J6 tables, figures, package | DRAFT | package stays draft until demo parity passes |
| V1 3-seed summary | NOT DONE | no seed file on Drive (Block 42) |
| V3 rubric concepts | PARTIAL | auto-drafted from reference sentences for all 248 questions; hand-written for 3 demo questions, not reviewed (J7) |
| V5 negation/paraphrase | DONE (36 cases) | paraphrase 12/12, spelling 12/12; negation exact 3/12, all 12 flagged; NLI contradiction >= 0.5 on all 12 negated answers (sanity check) |
| V6 demo parity | PENDING then | waiting for Vishwajeet's `demo_outputs.json` (later: parity PASS 15/15) |
| Blocks 53 to 58 | "WRITTEN, NOT RUN" (stale) | Block 52 (external LLM) dropped |

## 13.2 Why a new scorer
The model has evidence it does not use (contradiction signal fired on all 12 negated answers, yet the scorer called 9 correct; only low confidence stopped silent passing). Unseen questions are the weak spot (0.317, 27 questions). Calibration is already good, so remaining gain is in the scorer and unseen-question evaluation. Whether a stronger encoder helps on unseen questions is a hypothesis (P), not measured.

## 13.3 Workflow (all learned, all local)
```
question + reference answer + student answer
 [1] Cross-encoder: DeBERTa-v3 initialised from an NLI checkpoint, read in both directions
     heads: 5-way label | ordinal 3-level | contradiction
 [2] Evidence layer: learned attention over reference sentences
 [3] Deep ensemble: two backbones, three seeds, averaged logits
 [4] Calibration + conformal prediction sets + learned deferral
 -> score 0/1/2, calibrated confidence, review flag, per-sentence evidence
```

## 13.4 Training and evaluation protocol
Question-grouped 5-fold CV over all non-test questions (about 177), so unseen-question performance is measured on all of them instead of 27; one fold sealed until the final adoption decision; baselines retrained on the same folds (v2-style ensemble per fold); training additions: contrastive loss using labelled contradictory answers, group-DRO; test sets run once at the end, labelled exploratory; store only out-of-fold probabilities plus one final model; full 5-fold run about 1 to 2 GPU hours on a T4 (P, not measured).

## 13.5 What v3 replaces
Equal-weight average of three models -> one multi-task cross-encoder then deep ensemble; contradiction flag with 0.5 cut-off (Blocks 40, 50; switched off by a dev rule) -> trained contradiction head used inside the scorer; confidence grid threshold -> conformal sets + learned deferral checked by grouped CV; LLM-drafted rubric concepts -> reference sentences weighted by a trained attention layer, then reviewed; regex tags and percentage difficulty cut-offs (Blocks 53, 57) -> embedding clusters / item-response difficulty (optional); simulated ASR noise by random edits (Block 54) -> TTS then local ASR round trip (optional).

## 13.6 Teacher-in-the-loop adaptation (simulation only)
About 69% of answers go to a teacher under the current policy, so graded answers are produced anyway. Treat reviewed answers as per-question examples: fit a small head on frozen features + base logits for that question. In simulation, reveal 5 or 10 labelled answers per held-out question and measure QWK on the rest. Stays a simulation until real teacher labels exist.

## 13.7 Decision rules, fixed before any v3 result (do not change after seeing results)
1. **Adopt v3 as final scorer only if** pooled out-of-fold macro-F1 beats the same-fold v2-style baseline by at least 0.01, the paired question-bootstrap interval is above 0, unseen-question QWK does not fall, and the negation control improves from 3 of 12.
2. **Adopt the learned review policy only if** its grouped-CV risk-coverage is at least as accurate at equal or higher coverage than v2 (about 0.748 at 0.313).
3. Otherwise **v2 stays final** and v3 is reported as a study.

## 13.8 Block plan (Phase 11) [NUMBERING CONFLICT: the COPY notebook now uses Blocks 59 and 60 for latency and voice; renumber this plan from 61 if built]
New files use new names (`A_predict_v3.py`, `A_abstain_policy_v3.json`) so v2 stays as fallback.
Group 20 Protocol and baselines: 59 fold assignment + sealed fold; 60 training tables and contrast pairs; 61 v2-style baselines on same folds. Group 21 Scorers: 62 NLI-initialised DeBERTa multi-task model, fold loop; 63 ablations (ordinal head, contrastive loss, group-DRO); 64 second backbone and deep ensemble (reuse Vishwajeet's 3-seed RoBERTa-base once V1 verifies). Group 22 Reliability: 65 calibration + conformal sets; 66 learned deferral vs v2 policy; 67 teacher-in-the-loop simulation. Group 23 Integration: 68 v3 `predict()`, parity, rerun the 36-case set; 69 gate decision against 13.7 + one exploratory test run; 70 closure table and package. The predict() contract does not change except `model_version` becomes `v3-...` and `nli.contradict` comes from the contradiction head.

## 13.9 Priorities if time runs short
Must: Blocks 59 to 62, Block 65, Block 68, V6 demo parity, V1 verified seeds. Should: 63, 64, 66, J7. Cut first: item-response difficulty, TTS round trip, Block 67, extra seeds, second backbone.

## 13.10 Risks
Stronger encoder does not help on unseen questions (medium; report; v2 stays); 85% target unmet (high); Colab limits during fold loop (medium; resumable loop, save out-of-fold probabilities after each fold); less training data because one fold sealed (certain); seed variation (report spread); nothing tests CBSE or Indian schoolchildren (certain; keep limitations slide).

## 13.11 Added to definition of done
L8 accepted by both; fold assignment and sealed fold saved with questions per fold; v3 and baseline on same folds with paired intervals; gate decision recorded; v3 `predict()` reproduces stored probabilities and demo matches; negation control rerun vs 3/12; Section 1 refreshed from the 13.1 table once V1, V3, V6 are done.
