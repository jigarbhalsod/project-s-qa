# Project S Q&A branch: test results (v1)
Generated 2026-11-02T09:44:03. Frozen at 2026-10-19T20:38:17.

## 1. Test results (locked splits)
| dataset | split | model | n | macroF1_5 | macroF1_3_official | macroF1_3_ours | qwk_ours |
|---|---|---|---|---|---|---|---|
| beetle | test_ua | simple_average | 439 | 0.614 | 0.701 | 0.693 | 0.641 |
| beetle | test_ua | finetuned_distilroberta | 439 | 0.607 | 0.675 | 0.672 | 0.62 |
| beetle | test_ua | stacked_combiner | 439 | 0.595 | 0.671 | 0.666 | 0.609 |
| beetle | test_ua | sbert_pair_features_lr | 439 | 0.557 | 0.621 | 0.64 | 0.52 |
| beetle | test_ua | tfidf_text_plus_similarity | 439 | 0.545 | 0.603 | 0.619 | 0.478 |
| beetle | test_ua | sbert_similarity_only | 439 | 0.422 | 0.507 | 0.568 | 0.431 |
| beetle | test_ua | tfidf_similarity_only | 439 | 0.379 | 0.514 | 0.529 | 0.408 |
| beetle | test_ua | nli_lr | 439 | 0.266 | 0.514 | 0.41 | 0.374 |
| beetle | test_ua | nli_features_lr | 439 | 0.266 | 0.514 | 0.41 | 0.374 |
| beetle | test_ua | majority | 439 | 0.114 | 0.191 | 0.191 | 0.0 |
| beetle | test_uq | simple_average | 819 | 0.584 | 0.619 | 0.614 | 0.513 |
| beetle | test_uq | sbert_pair_features_lr | 819 | 0.533 | 0.543 | 0.545 | 0.379 |
| beetle | test_uq | finetuned_distilroberta | 819 | 0.526 | 0.585 | 0.58 | 0.444 |
| beetle | test_uq | stacked_combiner | 819 | 0.52 | 0.596 | 0.599 | 0.48 |
| beetle | test_uq | tfidf_text_plus_similarity | 819 | 0.49 | 0.506 | 0.535 | 0.32 |
| beetle | test_uq | sbert_similarity_only | 819 | 0.318 | 0.395 | 0.453 | 0.204 |
| beetle | test_uq | tfidf_similarity_only | 819 | 0.284 | 0.403 | 0.43 | 0.199 |
| beetle | test_uq | nli_lr | 819 | 0.231 | 0.41 | 0.402 | 0.244 |
| beetle | test_uq | nli_features_lr | 819 | 0.231 | 0.41 | 0.402 | 0.244 |
| beetle | test_uq | majority | 819 | 0.118 | 0.197 | 0.197 | 0.0 |
| scientsbank | test_ua | simple_average | 540 | 0.57 | 0.635 | 0.591 | 0.544 |
| scientsbank | test_ua | stacked_combiner | 540 | 0.538 | 0.631 | 0.566 | 0.532 |
| scientsbank | test_ua | finetuned_distilroberta | 540 | 0.477 | 0.574 | 0.555 | 0.49 |
| scientsbank | test_ua | sbert_pair_features_lr | 540 | 0.472 | 0.529 | 0.528 | 0.422 |
| scientsbank | test_ua | tfidf_text_plus_similarity | 540 | 0.408 | 0.575 | 0.552 | 0.409 |
| scientsbank | test_ua | nli_lr | 540 | 0.271 | 0.534 | 0.429 | 0.306 |
| scientsbank | test_ua | nli_features_lr | 540 | 0.271 | 0.534 | 0.429 | 0.306 |
| scientsbank | test_ua | sbert_similarity_only | 540 | 0.27 | 0.435 | 0.457 | 0.252 |
| scientsbank | test_ua | tfidf_similarity_only | 540 | 0.25 | 0.437 | 0.46 | 0.302 |
| scientsbank | test_ua | majority | 540 | 0.121 | 0.201 | 0.201 | 0.0 |
| scientsbank | test_ud | simple_average | 4562 | 0.571 | 0.619 | 0.546 | 0.479 |
| scientsbank | test_ud | stacked_combiner | 4562 | 0.526 | 0.62 | 0.538 | 0.48 |
| scientsbank | test_ud | finetuned_distilroberta | 4562 | 0.449 | 0.47 | 0.461 | 0.363 |
| scientsbank | test_ud | tfidf_text_plus_similarity | 4562 | 0.433 | 0.498 | 0.46 | 0.347 |
| scientsbank | test_ud | sbert_pair_features_lr | 4562 | 0.409 | 0.448 | 0.449 | 0.268 |
| scientsbank | test_ud | sbert_similarity_only | 4562 | 0.321 | 0.433 | 0.504 | 0.349 |
| scientsbank | test_ud | nli_lr | 4562 | 0.302 | 0.592 | 0.474 | 0.421 |
| scientsbank | test_ud | nli_features_lr | 4562 | 0.302 | 0.592 | 0.474 | 0.421 |
| scientsbank | test_ud | tfidf_similarity_only | 4562 | 0.252 | 0.434 | 0.47 | 0.354 |
| scientsbank | test_ud | majority | 4562 | 0.118 | 0.197 | 0.197 | 0.0 |
| scientsbank | test_uq | stacked_combiner | 733 | 0.378 | 0.574 | 0.541 | 0.497 |
| scientsbank | test_uq | simple_average | 733 | 0.359 | 0.547 | 0.53 | 0.454 |
| scientsbank | test_uq | finetuned_distilroberta | 733 | 0.334 | 0.509 | 0.489 | 0.332 |
| scientsbank | test_uq | sbert_pair_features_lr | 733 | 0.312 | 0.483 | 0.475 | 0.303 |
| scientsbank | test_uq | sbert_similarity_only | 733 | 0.283 | 0.44 | 0.494 | 0.374 |
| scientsbank | test_uq | tfidf_text_plus_similarity | 733 | 0.269 | 0.429 | 0.429 | 0.229 |
| scientsbank | test_uq | tfidf_similarity_only | 733 | 0.247 | 0.48 | 0.471 | 0.387 |
| scientsbank | test_uq | nli_lr | 733 | 0.23 | 0.53 | 0.436 | 0.449 |
| scientsbank | test_uq | nli_features_lr | 733 | 0.23 | 0.53 | 0.436 | 0.449 |
| scientsbank | test_uq | majority | 733 | 0.116 | 0.194 | 0.194 | 0.0 |

## 2. 95% bootstrap intervals (resampling questions)
| dataset | split | model | questions | macroF1_lo | macroF1_hi | qwk_lo | qwk_hi |
|---|---|---|---|---|---|---|---|
| beetle | test_ua | majority | 44 | 0.102 | 0.128 | 0.0 | 0.0 |
| beetle | test_uq | majority | 9 | 0.085 | 0.144 | 0.0 | 0.0 |
| scientsbank | test_ua | majority | 135 | 0.11 | 0.131 | 0.0 | 0.0 |
| scientsbank | test_uq | majority | 15 | 0.085 | 0.138 | 0.0 | 0.0 |
| scientsbank | test_ud | majority | 46 | 0.105 | 0.133 | 0.0 | 0.0 |
| beetle | test_ua | sbert_pair_features_lr | 44 | 0.515 | 0.605 | 0.436 | 0.597 |
| beetle | test_uq | sbert_pair_features_lr | 9 | 0.44 | 0.596 | 0.254 | 0.482 |
| scientsbank | test_ua | sbert_pair_features_lr | 135 | 0.366 | 0.545 | 0.335 | 0.503 |
| scientsbank | test_uq | sbert_pair_features_lr | 15 | 0.258 | 0.353 | 0.161 | 0.437 |
| scientsbank | test_ud | sbert_pair_features_lr | 46 | 0.357 | 0.458 | 0.2 | 0.339 |
| beetle | test_ua | finetuned_distilroberta | 44 | 0.549 | 0.667 | 0.536 | 0.694 |
| beetle | test_uq | finetuned_distilroberta | 9 | 0.464 | 0.594 | 0.308 | 0.53 |
| scientsbank | test_ua | finetuned_distilroberta | 135 | 0.378 | 0.579 | 0.395 | 0.566 |
| scientsbank | test_uq | finetuned_distilroberta | 15 | 0.254 | 0.404 | 0.19 | 0.487 |
| scientsbank | test_ud | finetuned_distilroberta | 46 | 0.401 | 0.489 | 0.28 | 0.435 |
| beetle | test_ua | stacked_combiner | 44 | 0.523 | 0.667 | 0.534 | 0.683 |
| beetle | test_uq | stacked_combiner | 9 | 0.448 | 0.593 | 0.335 | 0.624 |
| scientsbank | test_ua | stacked_combiner | 135 | 0.424 | 0.614 | 0.45 | 0.607 |
| scientsbank | test_uq | stacked_combiner | 15 | 0.308 | 0.438 | 0.362 | 0.619 |
| scientsbank | test_ud | stacked_combiner | 46 | 0.471 | 0.57 | 0.389 | 0.565 |

## 3. Abstain / teacher-review rule (frozen, threshold 0.75, policy 'A: confidence only')
| dataset | split | n | coverage | review_rate | acc_all | acc_auto | acc_reviewed |
|---|---|---|---|---|---|---|---|
| beetle | test_ua | 439 | 0.355 | 0.645 | 0.679 | 0.904 | 0.555 |
| beetle | test_uq | 819 | 0.315 | 0.685 | 0.614 | 0.829 | 0.515 |
| scientsbank | test_ua | 540 | 0.361 | 0.639 | 0.583 | 0.8 | 0.461 |
| scientsbank | test_ud | 4562 | 0.304 | 0.696 | 0.578 | 0.8 | 0.48 |
| scientsbank | test_uq | 733 | 0.364 | 0.636 | 0.591 | 0.798 | 0.472 |
| ALL | ALL test | 7093 | 0.319 | 0.681 | 0.59 | 0.81 | 0.487 |

## 4. Contradictory answers scored as correct
| model | contradictory_answers | scored_correct_rate |
|---|---|---|
| sbert_pair_features_lr | 894 | 0.252 |
| finetuned_distilroberta | 894 | 0.17 |
| nli_lr | 894 | 0.14 |
| stacked_combiner | 894 | 0.094 |

## 5. Per-question accuracy
See per_question_test_v1.csv.

## 6. Limitations
- Public English datasets only (SciEntsBank, Beetle). There is no CBSE student data yet, so nothing here shows performance on CBSE answers.
- Our correct / partial / incorrect scheme is a custom mapping of the SemEval 5-way labels. Compare with published work on the 5-way labels, and use QWK only on our ordered 3-level labels.
- All model choices were made on dev splits. The test splits were scored once with the frozen pipeline (see test_access_log_v1.json).
- The dev splits are small, especially dev_uq, and the bootstrap intervals only reflect question sampling.
- The LLM scorer was run on a sample of rows, not every answer.
- student_key is a best-effort parse of the answer id, so student-overlap checks are informational.
- Required concepts for NLI are sentences of the reference answer, not expert-written concepts.

## 7. LLM scorer on shared rows
| dataset | split | model | n | acc3_ours | macroF1_3_ours | qwk_ours |
|---|---|---|---|---|---|---|
| beetle | test_ua | llm_Qwen2.5-3B-Instruct | 100 | 0.45 | 0.37 | 0.254 |
| beetle | test_ua | sbert_pair_features_lr | 100 | 0.63 | 0.63 | 0.393 |
| beetle | test_ua | finetuned_distilroberta | 100 | 0.69 | 0.683 | 0.55 |
| beetle | test_ua | stacked_combiner | 100 | 0.68 | 0.663 | 0.596 |
| beetle | test_uq | llm_Qwen2.5-3B-Instruct | 100 | 0.38 | 0.332 | 0.245 |
| beetle | test_uq | sbert_pair_features_lr | 100 | 0.54 | 0.523 | 0.326 |
| beetle | test_uq | finetuned_distilroberta | 100 | 0.58 | 0.554 | 0.383 |
| beetle | test_uq | stacked_combiner | 100 | 0.61 | 0.589 | 0.433 |
| scientsbank | test_ua | llm_Qwen2.5-3B-Instruct | 100 | 0.59 | 0.489 | 0.499 |
| scientsbank | test_ua | sbert_pair_features_lr | 100 | 0.63 | 0.61 | 0.589 |
| scientsbank | test_ua | finetuned_distilroberta | 100 | 0.63 | 0.592 | 0.53 |
| scientsbank | test_ua | stacked_combiner | 100 | 0.61 | 0.587 | 0.532 |
| scientsbank | test_ud | llm_Qwen2.5-3B-Instruct | 100 | 0.43 | 0.3 | 0.279 |
| scientsbank | test_ud | sbert_pair_features_lr | 100 | 0.45 | 0.41 | 0.253 |
| scientsbank | test_ud | finetuned_distilroberta | 100 | 0.48 | 0.472 | 0.323 |
| scientsbank | test_ud | stacked_combiner | 100 | 0.48 | 0.451 | 0.316 |
| scientsbank | test_uq | llm_Qwen2.5-3B-Instruct | 100 | 0.41 | 0.281 | 0.307 |
| scientsbank | test_uq | sbert_pair_features_lr | 100 | 0.6 | 0.578 | 0.484 |
| scientsbank | test_uq | finetuned_distilroberta | 100 | 0.55 | 0.469 | 0.488 |
| scientsbank | test_uq | stacked_combiner | 100 | 0.63 | 0.58 | 0.611 |
