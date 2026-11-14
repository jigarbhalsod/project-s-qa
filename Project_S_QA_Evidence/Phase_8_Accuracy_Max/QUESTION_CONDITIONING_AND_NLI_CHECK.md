# Question conditioning and NLI input check

Scope: static inspection only. No inference, model, notebook cell, test file,
or split was run or opened. Source references are to `project_s_qa/reports_v2/A_predict.py` and Block 61 code cell 161.

## Component inputs

| Component | Exact text/features received | Is question text used? |
|---|---|---|
| **Verified ? DistilRoBERTa** | `A_predict.py` lines 61?68 builds first sequence as `question + " | " + reference_answer`; second sequence is `student_answer`. The tokenizer receives these as paired sequences, with truncation and max length 160. | **Verified ? Yes.** Question is part of the first sequence. |
| **Verified ? SBERT-LR** | Lines 92?101 encodes `reference_answer` and `student_answer` separately; LR features are the two embeddings, absolute difference, elementwise product, cosine similarity, and log answer/reference word-count ratio. | **Verified ? No.** Neither question nor a question-derived feature is used. |
| **Verified ? NLI-LR** | Lines 115?125 builds NLI pairs and a 7-value feature vector; lines 130?136 pass that vector to the pooled NLI logistic-regression model's `predict_proba`. Pair details follow. | **Verified ? No.** Question is not included in either NLI pair or the 7 features. |

## NLI-LR feature construction and pair order

**Verified:** `_nli` (lines 79?89) passes tuple element 0 as the first tokenizer
sequence and tuple element 1 as the paired second sequence. The source does not
name these arguments ?premise? and ?hypothesis?; interpreting the first as
premise and second as hypothesis follows the pair convention, not an explicit
variable label in this file.

**Verified:** For each row, `_concepts(reference_answer)` splits the reference
into concepts (lines 43?45). Concept pairs are `(student_answer, reference
concept)` (lines 115?120): student answer is first, reference concept second.
The whole-reference pair is `(reference_answer, student_answer)` (line 121):
reference is first, student answer second. Thus the two feature paths use
opposite tuple order.

**Verified:** The seven NLI-LR features (lines 122?125) are the mean and minimum
entailment probabilities across concept pairs, maximum contradiction, mean
neutral, and the three probabilities from the whole-reference pair, in
entailment/contradiction/neutral order. The pooled NLI-LR then maps these
features to five-class probabilities (lines 130?136; class order at line 13).

## Block 61 comparison

**Verified:** Block 61 cell 161 builds 12 `(question, reference, negation)`
triples (lines 5?11), loads the CSV's `kind == "negation"` rows (line 12), and
asserts each CSV answer equals the corresponding triple's negation (line 13).
It creates items with all three fields (line 15) and calls
`component_probs(items, dataset="pooled")` (line 16).

**Verified:** The block's question/reference/answer strings vary across its 12
triples. The source does not feed identical pair strings to NLI across all
rows: each whole-reference pair uses that row's reference and negation, and
concept pairs use that row's negation and its reference concepts.

## Interpreting the near-constant output

**Reported:** The saved Block 61 output showed the NLI-LR component predicting
`contradictory` at approximately 0.507 across the 12 diagnostic inputs.

**Verified:** This value is the pooled NLI-LR five-class probability, not the
raw cross-encoder's contradiction probability. The code path receives varying
pairs and derives seven numeric features for each row; the question is omitted.

**Unverified:** Source alone cannot establish why the fitted LR probabilities
are so similar. The code does not show that the feature vector is identical,
that the classifier is saturated, or that a feature is missing. The opposite
pair ordering between concept and whole-reference features is observable, but
whether it is unintended or explains the output is unverified without examining
per-row features/model behavior.

**Verified:** This is a diagnostic observation only, not a gate or an accuracy
claim. The diagnosis itself changes accuracy by no points; any effect of a
future change is unknown until tested.
