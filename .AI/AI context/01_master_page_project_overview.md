# Project S master page: "Reading Skills Profile Generation of Children"

Source: https://app.notion.com/p/3f22419db624810a9157f08b897a088a (fetched 1 Nov 2026 17:25 UTC; banner "updated 31 Oct 2026"). This is a faithful condensation, not a replacement. Evidence labels: (E) found in a paper read; (P) our proposal; (I) inference; (doc) number from the earlier research document, not re-checked; (NV) not verified; (M) measured in Jigar's notebook on dev. **Everything is theory and plan except section 7 (Q&A, measured on public English data, not on NNCES or CBSE). Say "the paper suggests X, and we will test it" unless measured on our data.**

## 1. Overview
- ML-based multimodal oral-reading and comprehension assessment. Core objective: an interpretable child skill profile from oral reading plus Q&A.
- Two questions: Reading ("how well does the child read the text?") and Q&A ("how well does the child understand and respond?").
- Output is multidimensional: each skill separate, with an uncertainty interval, **no overall score**.
- Branches stay separate until the profile layer. NNCES is the primary dataset; everything added is an extra source.

## 2. What changed in evaluation round 1 (7 Oct design to 9 Oct refined design)
| Area | Before | Now | Evidence |
| --- | --- | --- | --- |
| Child ASR | Whisper or wav2vec2 baseline | ASR prompted with passage text + LLM fix-up. Bake-off: Whisper-large-v3(-turbo), Parakeet-tdt-0.6b-v3, Canary, Qwen3-ASR; TICL+ in-context learning as a no-fine-tuning option | Prompted Whisper + LLM: word error 9.4% to 5.1%, miscue F1 0.39 to 0.73 (Dutch kids, Gao 2025) (E). TICL+ up to 53.3% relative word-error cut (E) |
| Phoneme path | Frozen wav2vec2-base-960h last layer | SSL phone recognizer (wav2vec2-XLSR or WavLM Base+) fine-tuned with CTC on children | Phone error 9.67% vs 18.15% hybrid, Indian L2 children (Gothi 2024) (E) |
| Miscue detection | Word ASR + alignment | Two-pass: pass 1 labels words; pass 2 re-checks words called correct (min-phone GOP, confusion-weighted phone edit distance, entropy confidence) fused by logistic regression | Pass 1 missed 72%; fused miss rate 31.07% at 5% false alarms, AUC 0.935 (Gothi 2024) (E) |
| Alignment | Plain word match | Phonetically informed alignment (MFA or Qwen3-ForcedAligner-0.6B, hand-checked) | Gothi 2024 (E) |
| Prosody/rate | Pitch mean/SD, ZCR, pause count and duration | F0 in cents, speaker mean removed, 150 to 450 Hz; pause position; per-minute counts; distance to adult readings. **Mean pitch and ZCR dropped** | Prosody lifted expressivity 0.62 to 0.78, phrasing 0.77 to 0.83 (Bailly 2022) (E) |
| Speech representation | Last layer | Middle layers or mean over layers | Layer 17 of 24 CCC 0.808 vs output layer 0.772 (Vaidya 2024) (E) |
| Fluency scoring | Blocked | Bake-off: SSL embedding head vs rubric-guided SpeechLLM (Qwen2-Audio-7B-Instruct + LoRA). Both need human ratings | SSL head Pearson 0.827; SpeechLLM PCC about 0.81, QWK about 0.50 vs human-human 0.50 to 0.56 (E) |
| Uncertainty | One confidence number | Conformal intervals (90% target) + "needs review" | Parikh 2026 (E) |
| Profile scale | Example 86/100 | 1 to 4 bands per skill (pace, smoothness, phrasing, expressivity) | Bailly 2022 rubric; adults score 4.01 to 4.8 so top saturates (E) |
| Q&A scorer | TF-IDF/SBERT/cross-encoder/NLI in one weighted formula | **Proposed:** rubric-prompted open LLM + NLI per concept + small tuned model + calibrated combiner; TF-IDF as ablation baseline. (**Built version differs: see section 7.**) | Expect QWK about 0.55 to 0.60 on unseen questions (German study) (E) |
| Training data | NNCES only | Add speechocean762, MPS (needs permission), adult readings, at least 2 raters | (E) |

### Corrections already made (do not reintroduce)
- Medin paper authors are **Gelin, Medin, Cruel and Liu** (SLaTE 2025).
- GradeAid trains one model per question, so it does not prove unseen-question performance.
- Profile uses 1 to 4 bands, not percentages. Pitch range 150 to 450 Hz; the earlier means of about 47 to 52 Hz are implausible and need an audit (E0).
- XLSR: weak as frozen fluency features (Vaidya), strong as a fine-tuned phone recognizer (Gothi).
- Do not promise 0.70 QWK: human-human agreement is only about 0.50 to 0.56.

## 3. Architecture (refined)
```
Child
 |- Reading task: passage + audio
 |    QC (SNR, clipping, duration) + VAD
 |      |- Path A: word ASR prompted with passage (+ LLM fix-up)
 |      '- Path B: SSL phone recognizer (CTC) -> phonetically informed alignment
 |    Pass 1 word labels -> Pass 2 re-check of "correct" words (GOP + phone edit distance + confidence)
 |    Rate: WCPM, articulation rate, pause-position profile
 |    Prosody: speaker-normalised F0, duration residuals, distance to adult readings
 |    Fluency scorer: SSL mid-layer head vs rubric SpeechLLM -> score + conformal interval
 '- Q&A task: question + spoken or typed answer
      spoken -> same ASR; typed -> text; normalise (keep "not")
      [proposed] rubric LLM + NLI per concept + small fine-tuned model -> calibrated combiner
      -> Correct / Partial / Incorrect + flags (Contradictory, Irrelevant) + needs review
Profile layer: separate dimensions, intervals, no overall score -> dashboard/report
```

## 4. Dataset status (NNCES, reading branch)
- 50 children, ages 8 to 12, about 5,000 read-speech recordings, 44.1 kHz 16-bit WAV, metadata (speaker, age, gender, prompt ID, repetition). 4,990 checked, 1 zero-length removed, **4,989 usable**. 10 reading prompts.
- Limits: no human fluency ratings; **no reference text for the 10 prompts**; only 50 speakers (speaker-independent validation, bootstrap by speaker); speakers' first language unchecked (parked).
- Planned extra data: speechocean762 (5,000 utterances, 250 non-native speakers, half children, 5 expert raters; Mandarin L1), MPS (1,110 Indian L2 children, 19 h, licence needs permission from Dr. Preeti Rao), adult reference readings (to collect), own transcribed subset (300 to 500 clips, 2 annotators), own rated subset (at least 2 raters, 1 to 4 rubric, store every rater's score).

## 5. Work completed (status table)
| Area | Status | Note |
| --- | --- | --- |
| Dataset analysis, audio validation | DONE | manifest; 4,989 usable |
| Acoustic features | DONE | pitch mean/SD, ZCR, pauses (mean pitch and ZCR now dropped) |
| Pitch analysis | AUDIT REQUIRED | ages 11/12 means about 52 and 47 Hz are implausible; re-run 150 to 450 Hz |
| wav2vec2 | DONE | frozen base-960h embeddings (last layer) |
| Age experiment | DONE, SIDE EXPERIMENT | 5-way age classification **42.01% +/- 4.61%** (speaker-independent 5-fold; chance 20%). Not a fluency result |
| Literature round 1 | DONE | 15 papers read (7 original, 8 added) |
| Reading accuracy | BLOCKED | needs reference text and alignment |
| Subjective fluency | BLOCKED | needs human ratings |
| **Q&A scoring** | **BUILT (v2), see section 7** | public English data; not tested on NNCES/CBSE |
| Final profile | PROPOSED | |

## 6. Research direction established
Run a controlled ASR bake-off; WER is not reading-error detection (prompt-constrained ASR "corrects" misreadings); use prompted ASR + phone path + second-pass classifier; middle SSL layers for fluency; speaker-normalised prosody and adult references; keep dimensions separate; conformal intervals and judge against human-human agreement; for Q&A evaluate on unseen questions and expect lower scores there; treat published gains as hypotheses until tested on NNCES.

## 7. Q&A branch: results and status (section 5A, 31 Oct 2026)
All numbers are (M): Jigar's notebook, dev data, public English data (SciEntsBank + Beetle). Test splits were seen in v1; the test-access log reads 3 evaluations; test numbers are exploratory.

**What was built**
- Data: 5 official labels collapsed to 3-level (0/1/2). Questions kept apart between train, dev and test. Dev 2,049 answers over 177 questions. Test 7,093 answers over 248 questions.
- Scorer v2: average of three trained models (fine-tuned DistilRoBERTa; SBERT + logistic regression; NLI classifier + logistic regression). No LLM, no hosted model; audit found no API reference in the deployed code.
- Review rule: teacher reviews when calibrated confidence < 0.64 (fitted on dev). ECE 0.017, temperature 1.00.
- Demo: one function (`A_predict.py`) behind Gradio; five test cases and 15 reference cases; **parity PASS 15/15** (max confidence difference 0.0005; same function, so consistency not independent replication).
- Controls: 36 hand-written sentences (paraphrase, spelling, negation) and per-concept NLI evidence for demo questions.
- Studies (not deployed): embedding clusters of questions; learned deferral model (gradient boosting, question-grouped CV).
- **Not built:** voice input, CBSE-style question bank, pilot answers. The rubric-prompted LLM scorer was replaced by the trained ensemble; a prompted 3B model ran on 100 to 250 rows as an excluded side result.

**Results**
| Measure | Value | Note |
| --- | --- | --- |
| Dev QWK, all | 0.432 (0.358 to 0.509) | 177 questions |
| Dev QWK, seen answers | 0.630 (0.562 to 0.692) | 150 questions |
| **Dev QWK, unseen questions** | **0.317 (0.199 to 0.412)** | only 27 questions; plan expected about 0.55 to 0.60 |
| Dev macro-F1 (5 labels) all / seen / unseen | 0.579 / 0.730 / 0.490 | |
| Exploratory test QWK, all | 0.454 (0.392 to 0.515) | 248 questions |
| Exploratory test unseen questions | Beetle 0.450 (9 questions); SciEntsBank 0.421 (15 questions) | very wide intervals |
| Exploratory test unseen domain (SciEntsBank) | 0.441 (0.353 to 0.523) | 46 questions |
| Accuracy on auto-scored at 0.64 | dev 0.751 at coverage 0.306; test 0.790 at coverage 0.288 | |
| **85% accuracy at 30% coverage** | **Not met** | grouped-CV estimate 0.748 at 0.313; highest dev coverage reaching 85% is about 0.10 |

Against baselines (paired question-level bootstrap): clear gain over majority (+0.370 macro-F1 on unseen dev questions, 0.283 to 0.422) and over TF-IDF + LR on seen answers (+0.088, 0.060 to 0.120). On unseen questions the deployed scorer is level with the best single fine-tuned model and with SBERT (intervals include zero). On exploratory test splits it is equal to or lower than the earlier simple average on all five splits (0.001 to 0.071 macro-F1; e.g. 0.513 vs 0.584 on Beetle unseen questions). Pooled was chosen because it works without knowing the dataset (dataset-specific variant 0.583 mean dev macro-F1 vs 0.528 combined, but needs the dataset name at run time). Sign convention of the baseline table is inferred (I).

**Model comparison and seeds (dev macro-F1, mean of 4 splits)**
- DistilRoBERTa alone 0.532; clearly worse than the ensemble (-0.047, -0.068 to -0.028).
- Ensemble with dataset-specific heads 0.583 (reference; deployed pooled version needs no dataset name).
- RoBERTa-base, Jigar's single run 0.584: tie (-0.002, -0.036 to 0.032). Weights not saved.
- RoBERTa-base, Vishwajeet's three seeds 0.565 / 0.582 / 0.527 (average 0.558): his own fine-tune; SciEntsBank unseen-question dev F1 ranges 0.279 to 0.474 across seeds, so gaps near 0.02 are noise.
- Raw NLI features (his ablation): removing the 7 features changes macro-F1 by +0.003 (0.5975 vs 0.5943); "without NLI" still contains nl_p0 to nl_p4.

**Weak spots (hand-written sanity checks, not an evaluation)**
- Negation: exactly right in 3 of 12; nine scored "correct"; all 12 flagged. Wording flips scores: "Plants do not need sunlight." scored incorrect while "...to make food." scored correct (both flagged).
- Partly-right answers scored wrong but flagged.
- One silent failure in 15 reference cases (c15, vague bulb answer, scored 0 at 0.745, not flagged).
- NLI evidence panel showed entailment 0.87 to 0.96 for three of four unrelated sentences; final scores still right; do not present it as an explanation for off-topic answers.

**Reproducibility caveats**
- A full run on 30 Oct 2026 rewrote 18 files meant to be frozen and raised the test-access count to 3. Deployed scores reproduced exactly; older comparison tables moved by 0.006 or less. Never use Run all.
- RoBERTa-base weights are not on Drive; its row cannot be regenerated.
- `A_predict.py` has the project path built in; Vishwajeet had to override it.
- One hard-coded constant remains (DistilRoBERTa dev F1 in Block 26, used only in a printed comparison).

**Vishwajeet's work (his notebook, outputs saved):** three-seed RoBERTa-base run, error analysis, seen/unseen bootstrap intervals (7 Beetle + 20 SciEntsBank unseen dev questions = 27), NLI ablation, file audit, a run of the 15 demo cases from a folder copy producing a 15-row file. His review flag (confidence < 0.75, about 54% flagged) is provisional; final rule is 0.64. Open: his seed results are not yet in Jigar's shared folder (Jigar's seed summary reads "pending").

## 8. Jigar's part (sections 7.1 to 7.5)
- 7.1 Architecture: Child -> Reading task + Q&A task -> assessment -> fusion -> Child Skill Profile; branches separate until profile.
- 7.2 Reading pipeline (proposed, not implemented): QC+VAD; word ASR (candidates above; passage prompt; LLM fix-up; TICL+ or LoRA on own transcribed subset); phone recognizer (XLSR or WavLM Base+, CTC, two-stage fine-tuning: about 1,000 steps CTC layer only, then Transformer with CNN frozen); alignment (MFA, Qwen3-ForcedAligner: 27.8 ms vs 88.6 ms NFA shift, untested on children); pass-2 miscue classifier (min-phone GOP, confusion-weighted phone edit distance, temperature-scaled entropy, logistic regression with balanced bagging); word+phoneme fusion (Gelin 2025: WCPM error 8.4 vs 9.74 word-only vs 20.9 phoneme-only; F1 42.5); rate (WCPM, articulation rate); pausing/prosody (Praat via parselmouth, cents, pause position, adult distance); fluency scorer (mid-layer SSL mean + MLP with CCC loss, or Qwen2-Audio-7B-Instruct + LoRA rank 32, about 10M trainable parameters, conformal calibration); pronunciation flags (GOP, GOPT as design reference only).
- 7.3 Q&A (proposed): same ASR for spoken answers; text normalisation (keep negations); rubric-prompted open LLM; NLI per concept (DeBERTa-style); small fine-tuned model (LoRA small LM, ModernBERT/GTE); logistic-regression combiner + abstention; TF-IDF + cross-encoder + regression (GradeAid-style) as ablation baseline only. **Update 31 Oct: the built scorer is a trained ensemble with no LLM (rule L8), unseen-question QWK 0.317 vs 0.55 to 0.60 expected.**
- 7.4 Q&A output: Correct / Partial / Incorrect; flags Contradictory and Irrelevant/no-answer; needs teacher review when parts disagree or interval wide; missing ideas listed.
- 7.5 Profile: word accuracy (% + error types); rate (WCPM + articulation); pausing/phrasing (pause-position profile, 1 to 4 band); prosody and smoothness (1 to 4 band + conformal interval); pronunciation (flags + confidence); comprehension (per-skill grade + flags); question difficulty (context only); confidence (interval + review flag); **overall score: none by default.** Dimensions overlap (phrasing correlates 0.85 with pace, 0.79 with smoothness, 0.77 with expressivity), so report side by side.

## 9. Papers: what we take (key numbers)
- Vaidya 2024 (full PDF): 1,447 recordings, 165 speakers, ages 10 to 14, L2 English; rater agreement 0.76; layer 17 CCC 0.808; handcrafted baseline Pearson 0.794; mean-over-layers Pearson 0.827.
- Bailly 2022 (full PDF): 1,063 readings, 442 children, 42 adults, 29 raters; four 1 to 4 ratings; test correlations 0.69 to 0.86.
- Fan 2024 (doc): OGI zero-shot Whisper-large-v3 19.9, Canary 18.2, Parakeet 16.7; fine-tuned Whisper 1.4, WavLM 1.8, wav2vec2 2.5; MyST Whisper-small 9.3, WavLM 10.4.
- Molenaar 2023 (doc): MCC about 0.63 to 0.65; confidence r = 0.45 (Dutch).
- Gelin 2025 (full PDF): combined WCPM error 8.4; accuracy error 16.8; F1 42.5; false-alarm 9.5; word F1 56.4 (grade 1) to 35.9 (grade 5); trained on 84 h of US children aged 5 to 8.
- GOPT (abstract): about 0.6 phone / 0.55 word / 0.7+ utterance (secondary source).
- GradeAid (full text): RMSE up to 0.25 on 0 to 5; semantic features significant on 2 of 4 sets; one model per question.
- Gothi 2024 (full PDF): MPS 1,110 speakers, 1,600 utterances, 19 h; about 10% of words are miscues; XLSR phone error 9.67% vs 18.15%.
- Gao 2025, Gelin 2021 (48.7% relative phone-error gain; augmentation 13.1% relative), TICL/TICL+ (up to 53.3%): abstracts only.
- Parikh 2026 (full text, speechocean762, Mandarin L1): PCC about 0.81, RMSE about 0.83, QWK about 0.50; human-human 0.50 to 0.56; zero-shot models too generous.
- Qwen3-ASR (Jan 2026, Apache 2.0, Hindi supported): no English child results.
- Q&A studies: German short-answer: unseen answers QWK 0.74 (fine-tuned encoder) vs about 0.60 (GPT-4o); unseen questions about 0.60 vs 0.55 to 0.60. Henkel 2023: GPT-4 QWK 0.92 vs experts 0.915 on Ghanaian children's answers.

## 10. Tech stack (candidates, chosen by experiments)
torchaudio, librosa, Praat/parselmouth; Hugging Face Transformers, PEFT (LoRA), NeMo, Qwen3-ASR; Montreal Forced Aligner, Qwen3-ForcedAligner; PyTorch MLP with CCC loss; Gaussian NLL + split conformal prediction; open-weights LLM, DeBERTa-style NLI, embedding model, ModernBERT; jiwer, scikit-learn (F1, MCC, QWK); MLflow or Weights and Biases; FastAPI if deployed. WER is for ASR only, never for miscue detection.

## 11. Evaluation framework
- Reading: ASR WER/CER/PER (speaker-independent); miscue detection miss rate at 5% false alarms, DET, AUC, MCC, macro-F1 (accuracy meaningless: about 10% miscues); word accuracy and WCPM MAE, Pearson, Bland-Altman; fluency/prosody CCC, Pearson, QWK vs human ratings with human-human agreement as ceiling; conformal coverage (target 90%); fairness per age/gender MAE and bias, bootstrap by speaker.
- Q&A: macro-F1 and QWK; leave-one-question-out and unseen-answer splits; Cohen's kappa between graders first; spoken answers gold vs ASR transcript; paraphrase and negation control sets.

## 12. Research decisions
1. No arbitrary overall score (fixed weights such as 30/20/20/20/10 are not research-supported).
2. WER is not enough.
3. No raw mean pitch.
4. Modern Q&A stack, old methods as baseline.
5. Human ratings required for subjective scores (at least 2 raters per clip).
6. Bake-off before commitment.
7. Precision over recall for feedback to children (low false-alarm rate).
8. Report the realistic ceiling; do not promise 0.70 QWK.

## 13. Question bank, retrieval, adaptive selection (proposed, nothing built)
- Record fields: question_id, passage_id, subject, grade, topic, skills, question_type, answer_mode, bloom_level, reference_answers, accepted_variants, required_concepts (each a short sentence = one NLI hypothesis and rubric line), keywords, negation_sensitive, misconceptions, rubric, prerequisites, readability, calibration (observed % correct, Elo difficulty, text-predicted difficulty kept separate; IRT empty until enough responses), provenance.
- Retrieval: hard filters (grade within one level, subject, passage, not answered); BM25 + Sentence-BERT fused; re-rank by target difficulty and skill gap (P). Evaluate on 40 to 60 query contexts, two annotators relevance 0/1/2, nDCG@5/10, MRR, Recall@K, kappa.
- Adaptive: Elo-style update (Pelanek 2016): P = 1/(1+exp(-(theta-d))), theta += K(S-P), d -= K(S-P); choose items with expected success in a band (e.g. 0.6 to 0.8). BKT only for repeated skills. IRT deferred (needs hundreds of respondents per item). Offline test: temporal split, AUC and log-loss vs mean baseline.
- **Status:** adaptive selection (BM25 plus Elo) was withdrawn in the Q&A branch as hand-written rules (Block 56).

## 14. Fairness and robustness plan
- Fairness: per age band and gender MAE, mean signed error (bias), standardised difference; bootstrap by speaker; about 10 children per age band so exploratory; state which fairness definition is used (Loukina 2019).
- Robustness: noise at SNR 20/10/5/0 dB; reverberation; band-limit to 8 kHz and codec; speed 0.8 to 1.2; unseen speakers/passages/questions; stability (Spearman clean vs perturbed).

## 15. Experiments E0 to E17
E0 pitch audit 150 to 450 Hz; E1 hand-transcribe 300 to 500 clips (2 annotators); E2 ASR bake-off; E3 reference-text reconstruction; E4 SSL phone recognizer with CTC; E5 two-pass miscue detector; E6 layer sweep; E7 fluency bake-off with conformal intervals; E8 WCPM validity; E9 Q&A benchmark on unseen questions; E10 Q&A ablation by feature group; E11 spoken answers gold vs ASR; E12 paraphrase/negation controls; E13 retrieval; E14 difficulty; E15 adaptive vs fixed-length (simulation); E16 fairness by age/gender; E17 robustness sweep.

**Q&A status (31 Oct 2026):** E9 mostly done on public data (unseen QWK 0.317, M). E10 Vishwajeet's NLI ablation exists but keeps nl_p0 to nl_p4. E11 not done (voice demo planned). E12 done on 36 hand-written sentences (negation exact 3/12). E13 to E15 not done (adaptive selection withdrawn). E16 not applicable (public Q&A data has no age/gender fields). E17 not done.

## 16. Blockers and build order
Blockers: recover/reconstruct the 10 reference texts; fix pitch (150 to 450 Hz); hand-transcribe 300 to 500 clips; record adult readings; collect human ratings (at least 2 raters, 1 to 4 rubric); annotate miscues; build Q&A question bank, answer keys, rubrics; collect teacher-graded child answers; request MPS permission; check NNCES dataset card for first language.
Build order: (1) fix pitch, record adults, recover reference text; (2) transcribe subset, ASR bake-off; (3) two-pass miscue detector with phone recognizer; (4) ratings, fluency bake-off with conformal intervals; (5) build and test Q&A on unseen questions; (6) assemble profile with intervals and review flags.

## 17. Caveats to state openly
Fan, Molenaar and GOPT numbers not re-checked; Parikh's results are on Mandarin-L1 speakers, Gelin 2025 on US children, Gothi on Indian children aged 7 to 11 (none is exactly our population); Qwen3-ASR has no English child results; MPS needs permission; German short-answer comparison uses very different data; whether any published gain holds on NNCES can only be answered by our experiments.

## 18. Team (section 18)
- **Agreed 17 Oct (team WhatsApp): Q&A = Vishwajit Sonawane + Jigar Bhalsod; Reading = Ayush Askar + Safal Gawande.** The experiment-level split below is still a proposal.
- Jigar: architecture, Q&A branch, profile, evaluation, question bank, calibration, shared leakage-safe evaluation framework; E7, E13 to E15, E16, E17, integration. Status: Q&A built and measured on public data; question bank, voice demo and reading-side work pending.
- Askar: child-speech ASR, representations, miscue detection; E0, E2 to E6. DONE (per Jigar): manifest, audio validation, acoustic features, wav2vec2 embeddings, age classifier; pitch needs audit.
- Vishwajeet: oral-reading assessment and comprehension; E8 to E12. Q&A work recorded 31 Oct (RoBERTa-base comparison, error analysis, 3-seed run, NLI ablation, bootstrap, demo run on 15 cases); not comparable with Jigar's.
- Safal: child speech, fluency, prosody; E7 prosody features, E0 spot-check, adult readings. No completed work recorded.
- Shared: transcription (E1), human ratings, miscue annotation (Askar leads), Q&A bank and teacher-graded answers (Jigar + Vishwajeet), MPS permission (unassigned).

## 19. Decision rationale in five lines
Small unrated data favours LoRA, TICL+, rubric prompting, Elo and bake-offs; every published number is a hypothesis; safety beats raw score (pass 1 missing 72%, F1 falling with age drive the two-pass design and low false-alarm target); humans set the ceiling (human-human QWK 0.50 to 0.56; unseen-question Q&A about 0.55 to 0.60); tools are the least evidence-based layer. No number backs the NLI models, MFA, Praat, the combiner or the tracking tools.

## 20. Research gaps and dataset decisions (section 19, 15 Oct; dataset details NV)
- No more broad literature research; two targeted reads: WCPM norms for non-native English readers aged 8 to 12; a rater protocol (band descriptions, training, agreement target) for the 1 to 4 fluency rubric.
- Start now: recover 10 passages, hand-transcribe, ASR bake-off and WCPM, audit pitch, write the Q&A question bank, request MPS permission.
- Datasets: keep speechocean762; keep CMU Kids only if licence is free (paid LDC corpus); keep SciEntsBank (prefer official release); **drop ASAP-SAS** (grade-10 text only).

## 21. Glossary
ASR speech to text; WER/CER/PER error rates; miscue = reading mistake (substitution, omission, insertion, repetition); WCPM words correct per minute; prosody melody/rhythm/pausing; SSL self-supervised speech model (wav2vec2, WavLM); CTC training method without timing labels; GOP goodness of pronunciation; forced alignment; SpeechLLM; LoRA small add-on fine-tuning (about 1.2% of weights); TICL in-context learning; conformal prediction (interval covering the human score a chosen share of the time); NLI (does a sentence support, ignore or contradict another); rubric; CCC/PCC/QWK/MCC agreement measures; miss rate vs false-alarm rate; leave-one-question-out.
