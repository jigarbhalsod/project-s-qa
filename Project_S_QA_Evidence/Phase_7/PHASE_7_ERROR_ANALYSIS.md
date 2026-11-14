# Phase 7 error analysis

Audit date: 6 Nov 2026. [Tested] Current pooled errors are calculated from
saved dev p0-p4 predictions. Dev is dev, optimistic; test is exploratory
(test seen in v1). No human labels were created or changed.

## H8: Partial class

[Tested] Three-way confusion matrix, rows gold and columns predicted in order
Incorrect, Partial, Correct:

| Gold / prediction | Incorrect | Partial | Correct |
|---|---:|---:|---:|
| Incorrect | 525 | 71 | 63 |
| Partial | 255 | 138 | 131 |
| Correct | 315 | 59 | 492 |

[Tested] Partial recall is 0.263359 (138/524); precision is 0.514925.
There are 894 total errors. 516 errors, 57.72%, involve Partial as either
gold or prediction. Of 524 gold Partial answers, 255 are predicted Incorrect,
131 Correct, and 138 Partial. Gold class counts are Incorrect 659, Partial
524, Correct 866. Predicted counts are Incorrect 1,095, Partial 268,
Correct 686.

[Tested] Hypothetical arithmetic only: if Partial recall rose to the target
and all newly recovered Partial answers became correct, with all else fixed,
three-way accuracy would be:

| Hypothetical Partial recall | Resulting accuracy |
|---:|---:|
| 40% | 0.598633 |
| 50% | 0.624207 |
| 60% | 0.649780 |

[Unverified] These scenarios do not predict model performance or establish
that the missed labels are correct.

## H5: split and question generalization

[Tested] Development metrics use deployed probability-collapse predictions.
All rows are dev, optimistic.

| Dataset / split | N / questions | Accuracy | Macro-F1 | Weighted-F1 | QWK |
|---|---:|---:|---:|---:|---:|
| Beetle dev_ua | 338 / 37 | 0.710059 | 0.638070 | 0.689518 | 0.627028 |
| Beetle dev_uq | 582 / 7 | 0.518900 | 0.467654 | 0.493176 | 0.319126 |
| SciEntsBank dev_ua | 415 / 113 | 0.677108 | 0.667692 | 0.674149 | 0.551145 |
| SciEntsBank dev_uq | 714 / 20 | 0.464986 | 0.426489 | 0.449005 | 0.271401 |

[Tested] Aggregate seen dev_ua is accuracy 0.691899, macro-F1 0.665502,
QWK 0.587950 (753 answers, 150 questions). Aggregate unseen dev_uq is
accuracy 0.489198, macro-F1 0.446166, QWK 0.294900 (1,296 answers,
27 questions). Seen-minus-unseen gaps are 20.27, 21.93 and 29.31 percentage
points, respectively.

[Tested] 36 of 177 dev questions have accuracy below 40%: 27/150 dev_ua and
9/27 dev_uq. By dataset/split: Beetle dev_ua 1/37, Beetle dev_uq 1/7,
SciEntsBank dev_ua 26/113, SciEntsBank dev_uq 8/20.

[Tested] Exploratory (test seen in v1) split metrics:

| Dataset / split | N / questions | Accuracy | Macro-F1 | Weighted-F1 | QWK |
|---|---:|---:|---:|---:|---:|
| Beetle test_ua | 439 / 44 | 0.676537 | 0.639081 | 0.661298 | 0.578333 |
| Beetle test_uq | 819 / 9 | 0.615385 | 0.541312 | 0.587960 | 0.449666 |
| SciEntsBank test_ua | 540 / 135 | 0.605556 | 0.560423 | 0.594765 | 0.513814 |
| SciEntsBank test_uq | 733 / 15 | 0.552524 | 0.482605 | 0.524142 | 0.421056 |
| SciEntsBank test_ud | 4,562 / 46 | 0.578036 | 0.524730 | 0.561604 | 0.441364 |

[Verified] Test_ua and test_uq share one question ID; 27 dev_uq question IDs
occur in test_ua. The archived source has 24 exact normalized
question/reference/answer keys shared between train and test_ua; seven keys
have differing label sets. No row UIDs overlap train with dev/test.
These overlaps limit clean seen/unseen and test interpretation.

## H1: data ceiling and label noise

[Verified] Block 6 documents norm_answer as lower-case, collapsed whitespace,
trimmed text. That stored normalization matches the rule on the archived
source split. Grouping by dataset, question ID, normalized reference and
normalized student answer finds 13 conflicting-label groups among all 16,003
rows, affecting 39 rows. Under that exact-normalization equivalence, the
minority labels imply at least 14/16,003 (0.0875%) errors if one deterministic
prediction is required for each group. This is a normalization-based bound,
not a universal bound for models that can distinguish original casing or
spacing.

[Verified] In dev, no exact normalized question/reference/answer group has
conflicting labels (0 groups, 0 affected rows, lower bound 0). In the
test-only subset there is 1 group with 6 rows and a one-row minority label;
test is exploratory. This exact-match check does not find semantic near
duplicates or decide whether any reference or gold label is wrong.

[Tested] Five-way per-original-label results from pooled five-way argmax:

| Original label | N | Accuracy | Error rate |
|---|---:|---:|---:|
| correct | 866 | 0.667436 | 0.332564 |
| contradictory | 307 | 0.433225 | 0.566775 |
| partially_correct_incomplete | 524 | 0.385496 | 0.614504 |
| irrelevant | 283 | 0.554770 | 0.445230 |
| non_domain | 69 | 0.971014 | 0.028986 |

[BLOCKED] The current v2 dev-probability file contains pooled p0-p4 only, not
current DistilRoBERTa, SBERT-LR and NLI-LR per-row probabilities. Exact current
four-way agreement against gold cannot be computed without running inference
or obtaining those saved outputs.

[Verified] Legacy-only: In archive/project_s_qa_phase1_v1.zip, interim/stack_features_v1.parquet has SHA-256 c51e1f04ca181a44bf6d952131c6dfb9d73255612253eb1a99f7f67acec0857a and aligned ft,
sb and nl component probabilities for the same 2,049 dev UIDs. Their separate
three-way accuracies are 0.558809, 0.573939 and 0.500244. These are not the
current pooled-v2 component scores. All three legacy components agree on the
same wrong class for 199/2,049 rows. All three legacy components plus the
current pooled prediction agree wrong on 197/894 current pooled errors; among
156 current pooled errors with confidence >=0.64, that cross-generation
agreement occurs for 110 (70.51%). Treat this only as a legacy diagnostic,
not current component complementarity evidence.

[Verified] The high-confidence error set is 156 dev rows with pooled
confidence >=0.64 and prediction different from gold. A_errors_sample_dev_v2.csv
has 25 sampled examples but no review/judgment fields. The 40-row
A_concepts_review_sheet_v2.csv has zero completed reviewer, reviewed_concepts
or ok fields. [BLOCKED] Documented human-reviewed answer errors: 0 of 156;
there is no linked completed manual error-review file. No gold labels were
changed and no correction file was created.

[Tested] Hypothetical sensitivity only: if 5%, 10% or 20% of the 156
high-confidence prediction/gold disagreements were actually label noise, and
all such cases were corrected to match the model, accuracy would be 0.567496,
0.571303 or 0.578917. This is arithmetic, not evidence that the labels are
wrong.

[Unverified] H1 verdict: neither a data ceiling nor a model ceiling is
established. Exact normalized conflicts are rare and absent in dev, but
semantic label quality and current component agreement are unresolved. Human
adjudication of partial and high-confidence errors plus current-v2 OOF
component outputs would decide more.

## H4, H13 and H14

[Tested] All 2,049 dev rows have a non-empty reference answer in the archived
source split; deployed-rule accuracy on that group is 0.563690. There is no
missing-reference comparison group. Non-empty does not establish reference
quality.

[Verified] A_predict.py input contract requires non-empty strings for question,
reference_answer and student_answer. DistilRoBERTa receives the pair
(question + " | " + reference_answer, student_answer). SBERT encodes reference
and student answers and builds embeddings, absolute/product differences,
cosine similarity and a log word-count ratio. NLI receives
(reference_answer, student_answer) and student-answer/reference-concept pairs.

[Tested] The local DistilRoBERTa tokenizer JSON applied to all 2,049 dev
input pairs yields zero sequences longer than A_predict.py's truncation
max_length=160; maximum encoded length is 160. This is tokenizer-only
analysis, not model inference.

[Verified] A_predict.py sets NLI truncation max_length=192. [BLOCKED] Actual
NLI truncation exposure and SBERT max-sequence exposure are unavailable from
the project files: corresponding tokenizer/model runtime outputs are absent,
and SBERT encode does not pass an explicit max length. Do not infer an
exposure rate.