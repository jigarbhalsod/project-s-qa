# Project S Q&A v2 — architecture answers from source

**Scope:** static source review only. No notebook, model, or script was run.
No test file or split was opened. Code references below use
`project_s_qa/A_submission_v2/demo/A_predict.py`; the root `reports_v2`
copy has the same SHA-256, `ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053`.
Notebook citations are source-line numbers within the stated cell, not
notebook file line numbers.

## Earlier claims checked

| Claim | Result | Source evidence |
|---|---|---|
| Three five-class component probabilities are equally averaged, collapsed, then argmaxed. | **CONFIRMED, with optional temperature step.** | `A_predict.py:152-160`; collapse map `:56-57`. A temperature other than 1 would transform the collapsed probabilities at `:154-157`; inspected final policy has temperature 1. |
| Confidence is the largest three-class probability; review threshold is 0.64. | **CONFIRMED only when the final packaged policy is loaded.** | `A_predict.py:139-142, 160-169`; packaged `A_abstain_policy_v2.json` has threshold 0.64. The code fallback threshold is 0.60. Block 60 imports from the project-root `reports_v2` (`COPY.ipynb`, cell 159, source lines 10-13); the matching local root policy file is absent, so the live Colab threshold is **Unverified**. |
| Only DistilRoBERTa receives question text. | **CONFIRMED.** | Distil input `A_predict.py:63-68`; SBERT input `:92-101`; NLI pairs `:116-125`. |
| No rubric is read at inference; NLI concepts are reference-answer sentences. | **CONFIRMED.** | Policy-only file load `A_predict.py:139-142`; sentence split `:43-45`; NLI pairs from reference text `:116-129`. |
| Partial is a learned probability, with no concept-count rule. | **CONFIRMED.** | Classifier probabilities and three-way mapping `A_predict.py:48-57, 130-136, 152-160`; no required-concept field or count is read. |
| `avg3` means averaging, not a trained final combiner. | **CONFIRMED.** | Version label `A_predict.py:15`; equal average `:152-153`; final decision `:160`. |

## Q1 — Rubric matching

**Verified:** `A_predict.py` does not load a rubric file. The only JSON it
loads by path is `A_abstain_policy_v2.json` in `_load_policy()`; it uses a
provisional policy if that file is absent (`:139-142`). The public prediction
inputs are `question`, `reference_answer`, and `student_answer`; there is no
`question_id` argument or rubric lookup in `predict()` / `predict_batch()`
(`:144-150, 176-178`). Therefore rubric selection is neither keyed by ID nor
by text inside the scorer. Without a rubric, the scorer follows the same
model path.

**Verified:** no `required_concepts`, `accepted_variants`, `misconceptions`,
or `worked_examples` field is referenced anywhere in `A_predict.py`. The
code's `concepts` are generated directly by splitting the supplied reference
answer on sentence punctuation (`:43-45`), then passed to NLI as
student-answer/reference-sentence pairs and returned as evidence (`:116-129,
166-172`). That is not rubric matching.

**Verified:** Block 60's question dropdown reads
`processed/cbse_demo_questions_v1.csv`, checks `question_id`, `question_text`,
and `reference_answer`, and builds a lookup whose visible key combines the
question ID and text (`COPY.ipynb`, cell 159, source lines 14-22). Its score
function sends the selected question, reference, and answer to
`A_predict.predict()` (cell 159, source lines 38-42). It does not load a
rubric.

**Verified — rubric inventory counts only; no answer text displayed:**

| File / version | Entries | Non-empty `required_concepts` | Auto-draft | Hand-written, unreviewed | Reviewed |
|---|---:|---:|---:|---:|---:|
| `project_s_qa/A_submission_v2/reports_v2/A_rubrics_v2.json` | 251 | 251 | 248 | 3 | 0 |
| `drive_backup_20261107/processed/rubrics.json` | 248 | 0 | 248 | 0 | 0 |
| `drive_backup_20261107/processed/rubrics_v1.json` | 248 | 0 | 248 | 0 | 0 |

The v2 rubric's three hand-written entries are still marked as needing a
second person; the file's `status` values are 248 `auto_draft` and 3 `demo`.
The duplicate v2 copies inspected have the same aggregate counts. None is
read by `A_predict.py`.

## Q2 — Question context and tokenizer inputs

**Verified — deployed DistilRoBERTa inference:** `A_predict.py:63-68` builds
the first input as `question + " | " + reference_answer` and the second as
`student_answer`. It calls the tokenizer with those two sequences,
`truncation=True`, `max_length=160`, `padding=True`, and tensor output. The
literal pipe is ordinary text between question and reference; the tokenizer
also applies its normal pair formatting.

**Verified — DistilRoBERTa training:** the training cell is `COPY.ipynb`, cell
50. `pairs_of()` forms the same first sequence and second sequence (source
lines 21-22); `MAXLEN=160` is set at source line 14; the tokenizer call uses
the same two inputs, truncation, max length, padding, and tensor output at
source lines 27-31. The question is included in both training and inference,
and those text fields, order, separator, truncation, and maximum length match.
Training uses variable `MAXLEN`; its configured value is 160.

**Verified distinction:** cell 68 is a separate historical `roberta-base`
run, not the deployed DistilRoBERTa component (`COPY.ipynb`, cell 68, source
lines 13-14). It uses the same question/reference first sequence and student
answer second sequence at source lines 25-35. It is not the source for the
deployed v2 Distil component.

**Verified:** SBERT encodes only reference and student answer and builds
cosine, length-ratio, and embedding interaction features (`A_predict.py:92-
101`). NLI receives student-answer/reference-sentence pairs and a
reference/student pair (`:116-125`). Neither receives the question text.

## Q3 — Relevance and off-topic answers

**Verified:** there is no separate relevance, subject-match, or
question-answer on-topic classifier or feature in `A_predict.py`. The
DistilRoBERTa input contains the question, so it can learn question context
implicitly (`:63-75`). SBERT measures answer-to-reference similarity
(`:92-101`); NLI compares answer/reference text (`:116-125`). Their results
are pooled with DistilRoBERTa (`:152-153`). There is no explicit relevance
veto.

**Verified:** review is triggered by low confidence, or—if enabled by policy—
a Correct prediction with high NLI contradiction (`A_predict.py:160-169`).
That rule routes an answer to review; it does not replace the predicted label.
There is no dedicated off-topic rule.

**Reported, not tested in this audit:** earlier demo observations said some
answers with NLI contradiction at least 0.95 still received Correct, and
off-topic answers were not flagged. These reports are consistent with the
source: the contradiction component has no veto, and the review flag is
policy-controlled.

## Q4 — Partial credit and contradiction review

**Verified:** Partial comes from model probabilities. Each component maps to
the five-label order and the pooled five-way probabilities are averaged;
`_to3()` maps five-way Partial probability (index 2) to three-way Partial
(`A_predict.py:13, 48-57, 130-136, 152-160`). There is no code that counts
present/missing concepts or applies a concept-count rule. NLI sentence-level
evidence is a feature for the NLI-LR classifier, not a rule that assigns
Partial (`:116-136`).

**Verified, policy-dependent:** the final packaged policy
`project_s_qa/A_submission_v2/reports_v2/A_abstain_policy_v2.json` sets
`use_contradiction_flag=false`, threshold 0.5, and confidence threshold 0.64.
With that file loaded, contradiction review is disabled. In source,
`A_predict.py:164` defaults the flag to true if the key is absent. The
provisional fallback at `:16-17, 139-142` omits that key, so it uses the true
default and confidence threshold 0.60. Block 60 imports from
`project_s_qa/reports_v2` (`COPY.ipynb`, cell 159, lines 10-13), while the
local `project_s_qa/reports_v2/A_abstain_policy_v2.json` is absent. The
policy file present under `A_submission_v2/reports_v2` will not be selected
by that default root unless `PROJECT_S_ROOT` is pointed there. The live Drive
root contents are **Unverified**; therefore the actual Colab flag state is
not established by this local audit.

## Q5 — Probability and decision trace

| Operation | Code location | What it does |
|---|---|---|
| DistilRoBERTa probabilities | `A_predict.py:61-75` | Runs the fine-tuned classifier and softmaxes its logits. Training label indexing uses `LABEL5_ORDER` (`COPY.ipynb`, cell 50, source lines 14-17). |
| SBERT-LR / NLI-LR five-way probabilities | `A_predict.py:48-53, 104-107, 130-136` | Converts each LR model's `predict_proba` columns into `LABEL5_ORDER`. `component_probs()` exposes `ft`, `sb`, `nl`, NLI `feats`, and concepts (`:110-136`). |
| Equal average | `A_predict.py:152-153` | Computes `(ft + sb + nl) / 3`, then collapses to three classes. |
| Five-to-three collapse | `A_predict.py:13-14, 56-57` | Five-way order is `correct, contradictory, partially_correct_incomplete, irrelevant, non_domain`. Three-way order is `incorrect, partial, correct`. Map: index 0 -> Correct; index 2 -> Partial; indices 1, 3, 4 -> Incorrect. |
| Optional temperature | `A_predict.py:154-157` | Applies a normalized power transform only if policy temperature differs from 1. The inspected final policy and fallback use 1, so they do not change the probabilities. |
| Prediction and confidence | `A_predict.py:159-160, 166-172` | Argmax of the three-way values chooses the label; confidence is their maximum. |
| Review flag | `A_predict.py:161-169` | Adds low-confidence and conditional contradiction reasons; `needs_teacher_review` is true when any reason is present. |
| Single-answer and component APIs | `A_predict.py:110-136, 176-178` | `component_probs()` returns the component probabilities; `predict()` wraps `predict_batch()` for one item. |

**Verified:** no final Logistic Regression combiner is applied to the three
components. The artifact named `combiner_v1.joblib` is opened for its
`base_models` (`A_predict.py:35`), and those models supply dataset-specific
SBERT-LR/NLI-LR probabilities (`:134-135`). In pooled mode,
`pooled_lr_v2.joblib` supplies those two component classifiers (`:104-107,
130-133`). The final ensemble is the explicit average at `:152-153`, not an
LR meta-model.

## Main concern, stated plainly

**Verified from code:** yes, a semantically similar but wrong or off-question
answer can receive Correct. There is no rubric, explicit question-answer
relevance check, or rule that rejects an off-topic answer. DistilRoBERTa is
the only component given the question; SBERT and NLI compare answer text with
the reference. NLI can contribute contradiction evidence, but it does not
veto Correct. The only potential safeguard is teacher-review routing, and even that is
conditional on the loaded policy. **Reported, not tested here:** earlier
demo observations found cases with NLI contradiction >=0.95 still scored
Correct and off-topic answers not flagged. The packaged policy disables the
contradiction review flag; the policy loaded by the current Block 60 root is
Unverified.

## One low-cost improvement per question (not implemented)

| Question | Proposed change using existing assets | Expected risk | Approval |
|---|---|---|---|
| Q1 Rubric | After human review, use reviewed `required_concepts` to route missing coverage to teacher review; do not let auto-draft entries decide labels. | Incomplete concept lists can create false review flags. | Yes; rubric review and scorer/demo change approval. |
| Q2 Context | Keep the question-ID lookup bound to its stored reference and make that reference read-only in the demo. | Stale IDs or incorrect bank entries still pair the wrong reference. | Yes; Block 60 UI change. |
| Q3 Relevance | Reuse the existing SBERT encoder to add a question-to-answer similarity signal for review routing. | Similarity cutoffs can flag valid short or paraphrased answers; requires dev calibration. | Yes; new inference feature and evaluation. |
| Q4 Partial | Use only reviewed rubric concepts to provide a transparent concept-coverage review signal for likely Partial cases. | Draft rubric quality may hurt Partial decisions; do not convert coverage counts directly into grades without validation. | Yes; rubric approval and evaluation. |
| Q5 Traceability | Record per-component probabilities and the exact policy path/review reasons alongside each demo result. | Extra logs may expose student answers; restrict and review retention. | Yes; logging/privacy approval. |

**Unverified:** accuracy gain from any proposed change is unknown. No change
was applied.
