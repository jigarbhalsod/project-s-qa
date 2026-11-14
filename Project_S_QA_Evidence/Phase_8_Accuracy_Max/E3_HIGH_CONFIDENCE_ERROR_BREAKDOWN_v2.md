# E3 — Current-v2 high-confidence errors, Partial diagnosis, and data quality

**Tested — all performance results here are dev-only, optimistic.** Inputs:
`A_component_probs_v7.parquet` (SHA-256
`71dd07621bb838b38af1932f43d985059a6a69e61d39361e6a5063eb5bdc5f88`) and
`dev_text_2049.parquet` (SHA-256
`21e7305557825b392a297fc4558b73e1161fcefb07d82c9f802e33c877836ea2`).
The 2,049 UIDs are unique and align exactly.
No test file or split was opened. Current-v2 component probabilities are used
below; this is not the earlier legacy-component analysis.

## 1. Current-v2 high-confidence errors

Definition: Path A pooled prediction is wrong and its confidence (maximum of
`p_incorrect`, `p_partial`, `p_correct`) is at least 0.64. **Tested:** 156
rows meet this definition.

| Breakdown | Counts |
|---|---|
| Gold five-way label | Partial 84; Correct 68; Irrelevant 2; Contradictory 2; Non-domain 0 |
| Dataset | SciEntsBank 91; Beetle 65 |
| Question split | Seen (`dev_ua`) 40; unseen (`dev_uq`) 116 |
| Dataset × split | SciEntsBank/dev_ua 25; SciEntsBank/dev_uq 66; Beetle/dev_ua 15; Beetle/dev_uq 50 |

**Tested — three current component predictions, collapsed to Incorrect /
Partial / Correct:**

| Row pattern among the 156 errors | Count |
|---|---:|
| All three components wrong and chose the same wrong class | 131 |
| All three wrong but disagreed on the wrong class | 14 |
| Mixed: at least one component right and at least one wrong | 11 |

Within the 131 same-wrong-class rows, the shared wrong prediction was
Incorrect on 115 and Correct on 16. In the 11 mixed rows, DistilRoBERTa alone
was right on 2; NLI-LR alone was right on 9; SBERT-LR was never the sole
correct component. These are current-v2 component predictions from the
export, not legacy probabilities.

## 2. Partial-class diagnosis

**Tested:** 386 of 524 gold-Partial rows are Path A errors: 255 predicted
Incorrect and 131 predicted Correct.

| Dataset / question split | Gold-Partial errors | Predicted Incorrect | Predicted Correct |
|---|---:|---:|---:|
| Beetle / seen | 53 | 45 | 8 |
| Beetle / unseen | 130 | 67 | 63 |
| SciEntsBank / seen | 57 | 46 | 11 |
| SciEntsBank / unseen | 146 | 97 | 49 |

| Three-way Partial metric | Path A: pooled collapse then argmax | Path B: five-way argmax then map |
|---|---:|---:|
| Precision | 0.514925 | 0.463303 |
| Recall | 0.263359 | 0.385496 |
| F1 | 0.348485 | 0.420833 |

**Tested:** Path B gains 0.122138 Partial recall and 0.072348 Partial F1,
while Partial precision falls by 0.051623. Path B remains an unvalidated
candidate; it is not deployed.

**Tested — `E1_review_sample.csv`:** 40 rows; all 40 have blank
`reviewer_name`, `reviewer_judgement`, `reviewer_note`, and
`suggested_gold_correction`. All are counted as unreviewed. No reviewer
judgement was inferred and no gold label was changed.

## 3. Dev-only data-quality audit

| Check | Result |
|---|---|
| Rows / unique UIDs | 2,049 / 2,049; no duplicate UID. |
| Gold five-way balance | Correct 866; Partially-correct/incomplete 524; Contradictory 307; Irrelevant 283; Non-domain 69. |
| Mapped three-way balance | Incorrect 659; Partial 524; Correct 866; no unmapped label. Mapping used: correct→2, partial→1, other three labels→0. |
| Exact duplicate answers | 22 pairs within the same dataset and question after case-folding and whitespace collapse; 0 pairs with conflicting five-way gold labels. |
| Near-duplicate answers | 169 pairs within the same dataset and question, using case-folded/whitespace-collapsed text, minimum length 12, and `SequenceMatcher` ratio ≥0.95; 41 pairs have different five-way labels. This is a heuristic screen, not human adjudication. |
| Cleanlab / out-of-fold audit | **BLOCKED:** no valid current-v2 out-of-fold component probabilities are available. |

The 41 near-pair label conflicts were: Correct/Irrelevant 22;
Contradictory/Correct 16; Correct/Partial 2; Contradictory/Partial 1. The
five dataset/question groups with at least one such conflict are:
`beetle|BEE-11e25a30`, `beetle|BEE-666c7672`,
`beetle|BEE-66c4dd68`, `beetle|BEE-b7f32586`, and
`beetle|BEE-f1d9b6c0`. Only IDs and aggregate labels are listed; answer text
is not reproduced. Near-pair results depend on the stated similarity rule.

**Scope:** These findings describe the supplied dev rows only. They do not
establish label errors, independent confirmation, or performance on new
questions or students.
