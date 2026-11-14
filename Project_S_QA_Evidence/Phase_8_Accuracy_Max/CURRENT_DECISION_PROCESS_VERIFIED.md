# Current deployed v2 decision process - static verification

Scope: source and metadata inspection only. No model, inference, notebook cell,
script, test file, or split was executed or opened. Line references identify
`project_s_qa/reports_v2/A_predict.py` and Block 60, cell 159 source lines.

## 1. Component inputs

| Question | Answer and evidence |
|---|---|
| Does DistilRoBERTa receive the question? | **Verified - Yes.** `_ft` builds sequence A as `question + " | " + reference_answer` and sequence B as `student_answer`; paired tokenizer call is at A_predict.py L61-L68. |
| Does SBERT-LR receive the question? | **Verified - No.** `_sb_X` encodes the reference answer and student answer separately (L92-L101); the LR receives embeddings and derived features, not question text. |
| Does NLI-LR receive the question? | **Verified - No.** `component_probs` constructs NLI pairs from the student answer, reference concepts, and whole reference (L115-L125); no question text enters those pairs. |
| Does every component receive the reference answer? | **Verified - Yes.** It is concatenated into DistilRoBERTa's first sequence; encoded by SBERT; and split/passed to NLI as concepts and as the whole reference (L43-L45, L61-L68, L92-L101, L115-L125). |

**Verified:** NLI tuple order is positional in `_nli` (L79-L89): tuple item 0
is tokenizer sequence 1; tuple item 1 is sequence 2. For concept pairs, these
are student answer then reference concept (L115-L120). For whole-reference
pairs, they are reference answer then student answer (L121). Calling these
premise/hypothesis follows the model-pair convention; the code itself does not
name the tuple fields that way.

## 2. Demo question/reference pairing

| Question | Answer and evidence |
|---|---|
| How is a reference selected? | **Verified:** Block 60 reads `processed/cbse_demo_questions_v1.csv`, requiring `question_id`, `question_text`, `reference_answer` (cell 159, L14-L21). `LOOKUP` maps the displayed `question_id: question_text` label to `(question_text, reference_answer)` (L22); `pick` returns that pair to the question/reference textboxes (L29-L30; dropdown wiring L65). |
| Can a wrong reference be paired with a question? | **Verified - Yes.** The dropdown initially fills the paired values, but both textboxes are editable and `score` has no lookup/ID/pair validation (L38-L42, L58, L65-L67). |
| Is the student answer tied to the selected question? | **Verified - No.** The answer textbox is independent/editable; the score handler checks only that question, reference, and answer are nonempty, then passes those strings to `A_predict.predict` (cell 159, L38-L42, L62-L67). There is no check that an answer belongs to the selected question. |

## 3. Rubrics and concept evidence

| Field/file | Read/use found in source | Deployed scoring-time status |
|---|---|---|
| `A_rubrics_v2.json` | **Verified:** Block 50 / cell 139 writes it (L38, L79). Static search found no read of this file by `A_predict.py` or Block 60 scoring. | **Verified - Not read by deployed scoring.** |
| `required_concepts` | **Verified:** Legacy Block 16 reads `processed/rubrics_v1.json` (cell 43, L16); `concepts_for` returns `rb["required_concepts"]` when nonempty (L19-L22), and Block 16 uses concepts to build NLI features. Block 50 / cell 139 drafts and exports v2 values (L20, L36-L49). | **Verified - Not read from `A_rubrics_v2.json` by A_predict.** At deployed scoring, A_predict instead splits the supplied reference answer with `_concepts` (L43-L45, L115-L125). |
| `misconceptions` | **Verified:** Created in rubric-stub construction (cells 24 and 33); no read/use found in A_predict or Block 60 scoring. | **Verified - Not used by deployed scoring.** |
| `accepted_alternatives` | **Verified:** This field name is absent from the inspected rubric schema and notebook source; the notebook uses `accepted_variants` in cells 24 and 33. No deployed scoring read found. | **Verified - Not used by deployed scoring.** |
| `A_concept_evidence_demo_v2.csv` | **Verified:** Written by Block 50 / cell 139 (L78); Block 58 / cell 155 checks its presence (L17). No evidence that its rows feed prediction. | **Verified - Export/status artifact, not a scoring input.** |
| `A_concepts_review_sheet_v2.csv` | **Verified:** Written by Block 50 / cell 139 (L49). No deployed scoring read found. | **Verified - Review/export artifact, not a scoring input.** |

**Verified:** `A_predict.py` contains no references to rubric filenames or rubric
fields (static source search). Block 60 displays `A_predict`'s returned
`concepts` in its JSON output (cell 159, L43-L50); those are generated from
the supplied reference text by A_predict, not loaded from the rubric/evidence
CSV files.

## 4. Required-concept and review-status counts

| Dataset/file | Count only |
|---|---|
| **Verified -** packaged `A_rubrics_v2.json` | 251 entries have nonempty `required_concepts`; status: 248 `auto_draft`, 3 `demo`; concepts status: 248 `auto_draft_unreviewed`, 3 `hand_written_unreviewed`. |
| **Verified -** `processed/cbse_demo_questions_v1.csv` | 12 rows; `required_concepts` column absent; status: 12 `draft_unreviewed`. |

## 5. NLI-LR and the reported ~0.5070 values

**Verified:** `_concepts` splits a reference answer into sentence/clause-like
pieces (A_predict.py L43-L45). `component_probs` creates pairs
`(student_answer, reference_concept)` and `(reference_answer, student_answer)`
(L115-L121). `_nli` returns entailment/contradiction/neutral probabilities
for each pair (L79-L89). The seven LR features are concept-level mean
entailment, minimum entailment, maximum contradiction, mean neutral, plus the
three whole-reference pair probabilities (L122-L125). The pooled NLI-LR maps
those features to five-class probabilities (L130-L136).

**Verified:** These input pairs vary with the reference and student-answer
text; the code does not reuse one fixed pair or hard-code 0.5070. **Reported:**
Block 61's earlier diagnostic showed NLI-LR `contradictory` probabilities near
0.507 on 12 negation rows. **Verified:** Similar logistic-regression output
probabilities are possible when different feature vectors produce similar
scores. **Unverified:** Source alone cannot establish why they are nearly
constant; per-row feature values and model behavior were not inspected or run.
The missing question in NLI input does not make the text pairs identical.

## 6. Pooling, class collapse, and review threshold

| Question | Answer and evidence |
|---|---|
| What is the 5-way order? | **Verified:** `LABEL5_ORDER = [correct, contradictory, partially_correct_incomplete, irrelevant, non_domain]` (A_predict.py L13). |
| How are the components pooled? | **Verified:** Equal arithmetic mean, one-third each: `(ft + sb + nl) / 3` (L153). Components are DistilRoBERTa, SBERT-LR, and NLI-LR; `component_probs` returns those keys (L110-L136). |
| How do 5 classes collapse to 3? | **Verified:** `_to3` sums indices 1, 3, 4 as incorrect, keeps index 2 as partial, and index 0 as correct (L14, L56-L57; names at L14). |
| Where is 0.64 applied? | **Verified:** `predict_batch` loads a policy, computes max class probability as confidence, and adds `low_confidence` when `conf < pol["confidence_threshold"]` (L151, L159-L163). The packaged policy file has `confidence_threshold=0.64`; the deployed Colab file's live value is **Unverified** here. The local `project_s_qa/reports_v2/A_abstain_policy_v2.json` is absent; if that local root is used, `_load_policy` falls back to provisional 0.60 (L16-L17, L139-L142). |

## 7. Source of Partial

**Verified - Yes:** Partial is a model probability/argmax result. The five-way
`partially_correct_incomplete` probability (index 2) becomes the three-way
`partial` probability through `_to3`; the final `pred_label` comes from the
three-way argmax and `NAMES` (L13-L14, L56-L57, L153-L160, L166-L172).

**Verified - No:** Deployed A_predict has no rule that counts concepts or
assigns Partial from a concept-count threshold. Reference concepts contribute
to NLI-LR features, but the Partial label is still selected from pooled model
probabilities (L115-L135, L153-L160).

## 8. Four concerns vs code behavior

| Concern | What the code does | Status |
|---|---|---|
| Rubric use | **Verified:** Deployed A_predict/Block 60 do not read A_rubrics_v2 or its fields. Legacy Block 16 reads `required_concepts` from `rubrics_v1.json` for NLI features. | Verified |
| Question context | **Verified:** Question enters DistilRoBERTa only; SBERT-LR and NLI-LR use reference/student text without the question. | Verified |
| Relevance vs correctness | **Verified:** The five-way component classes include irrelevant and non-domain; final three-way collapse groups both with contradictory under incorrect. | Verified |
| Partial-credit mechanism | **Verified:** Partial comes from the model's `partially_correct_incomplete` probability; no explicit concept-count rule exists in deployed scoring. | Verified |

**Unverified:** Whether these implementation choices caused any observed error
rates, and the size of any gain from changing them, require separate measured
evaluation; no gains are claimed here.
