# Phase 7 baseline reproduction report

Audit date: 6 Nov 2026. Evidence tags apply to every finding:
Verified = directly inspected local/archive artifact; Tested = calculated now
from saved rows; Reported = supplied by Jigar; Unverified = not established;
Pending = future approved work; BLOCKED = required evidence is absent.

## Scope and sources

[Verified] The audit used saved reports in project_s_qa/A_submission_v2/reports_v2,
the 167-cell COPY notebook as JSON, text of A_predict.py, the two project ZIPs,
and local review CSVs. Analysis read ZIP entries into memory; it did not extract
files. No model inference, training, notebook execution, network access, or
package installation occurred.

[Verified] The source split parquet is absent at the loose path
project_s_qa/processed/sra_unified_splits_v1.parquet, but is present in both
archive/project_s_qa_phase1_v1.zip and archive/project_s_qa_final_v1.zip.
The two archived entries are byte-identical, SHA-256
bdb67bf80f1cfa2a58a8193f3ca503bb1e462b393bb72c0635e1cc684b22676a6.
It has 16,003 rows and 19 columns. No copy was extracted.

[Verified] Submission-manifest hashes match the packaged scorer and evaluation
inputs: A_predict.py ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053;
A_demo_reference_outputs_v2.json ea5288e9f12b25d28a66f36ec38d48b08c65e19452bf3b5efa17eed2be20aeb9;
A_deployed_dev_probs_v2.parquet
2e29a708152b288019a9fa50b55b9d823781e4bbe0144cd5ee533fee9ddb5b0e;
A_test_scored_v2.parquet
8ec79019686135868b2ae739bac6b9fd7b8cc9fd636477936a39fc9969956faa.

## Deployed rule and alignment

[Verified] A_predict.py sets LABEL5_ORDER to correct, contradictory,
partially_correct_incomplete, irrelevant, non_domain. Its three-way map is
incorrect = p1+p3+p4, partial = p2, correct = p0; it averages the three
component five-way probabilities before applying that collapse and argmax.

[Tested] The saved dev p0-p4 values reproduce that rule. Joining the 2,049
dev prediction rows to the archived source split by UID gives 2,049 matches,
zero missing UIDs, zero duplicate UIDs, and zero score_ours/label5 mapping
mismatches. The full source split has 16,003 unique UIDs. Dev/test UIDs do not
overlap; no row UID overlaps train with dev or test. Dev five-way rows are
finite and their sums differ from one by at most 5.75e-8.

[Verified] Question-group counts in the archived source are 150 dev_ua and
27 dev_uq. Train shares 150 question IDs with dev_ua and none with dev_uq.
Train shares 152 with test_ua, none with test_uq or test_ud. Test_ua and
test_uq share one question ID; 27 dev_uq question IDs also occur in test_ua.
Test is exploratory (test seen in v1).

[Tested] Exact normalized input keys (dataset, question, normalized reference,
normalized student answer) have no train/dev overlap. There are 24 keys shared
between train and test_ua; seven shared keys have different label sets. This
is additional reason to keep test results exploratory, even though row UIDs
are disjoint.

## Reproduced development metrics

[Tested] All figures in this section are dev, optimistic. Predictions were
calculated from the saved pooled probabilities, not from model inference.

| Population | N answers / questions | Accuracy | Macro-F1 | Weighted-F1 | QWK |
|---|---:|---:|---:|---:|---:|
| All dev, pooled collapse | 2,049 / 177 | 0.563690 | 0.527046 | 0.549617 | 0.401530 |
| Beetle dev | 920 / 44 | 0.589130 | 0.528979 | 0.563938 | 0.435961 |
| SciEntsBank dev | 1,129 / 133 | 0.542958 | 0.518796 | 0.533114 | 0.369711 |
| Seen answers dev_ua | 753 / 150 | 0.691899 | 0.665502 | 0.685324 | 0.587950 |
| Unseen questions dev_uq | 1,296 / 27 | 0.489198 | 0.446166 | 0.470140 | 0.294900 |

[Tested] Dataset by dev split, with three-way deployed predictions:

| Dataset / split | N / questions | Accuracy | Macro-F1 | Weighted-F1 | QWK |
|---|---:|---:|---:|---:|---:|
| Beetle dev_ua | 338 / 37 | 0.710059 | 0.638070 | 0.689518 | 0.627028 |
| Beetle dev_uq | 582 / 7 | 0.518900 | 0.467654 | 0.493176 | 0.319126 |
| SciEntsBank dev_ua | 415 / 113 | 0.677108 | 0.667692 | 0.674149 | 0.551145 |
| SciEntsBank dev_uq | 714 / 20 | 0.464986 | 0.426489 | 0.449005 | 0.271401 |

[Tested] Overall three-way confusion matrix, rows gold and columns prediction
in order Incorrect, Partial, Correct:

| Gold / prediction | Incorrect | Partial | Correct |
|---|---:|---:|---:|
| Incorrect | 525 | 71 | 63 |
| Partial | 255 | 138 | 131 |
| Correct | 315 | 59 | 492 |

[Tested] Three-way per-class precision, recall, F1, and support:

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| Incorrect | 0.479452 | 0.796662 | 0.598632 | 659 |
| Partial | 0.514925 | 0.263359 | 0.348485 | 524 |
| Correct | 0.717201 | 0.568129 | 0.634021 | 866 |

[Tested] Saved five-way p0-p4 argmax results give accuracy 0.554905 and
macro-F1 0.578892. Five-way per-class scores:

| LABEL5_ORDER class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| correct | 0.676815 | 0.667436 | 0.672093 | 866 |
| contradictory | 0.431818 | 0.433225 | 0.432520 | 307 |
| partially_correct_incomplete | 0.463303 | 0.385496 | 0.420833 | 524 |
| irrelevant | 0.425474 | 0.554770 | 0.481595 | 283 |
| non_domain | 0.817073 | 0.971014 | 0.887417 | 69 |

[Tested] Five-way confusion matrix uses the LABEL5_ORDER above, rows gold and
columns predicted:
[[578,94,89,102,3],[78,133,61,27,8],[171,66,202,82,3],
 [27,14,84,157,1],[0,1,0,1,67]].

## Test results and provenance

[Tested] The saved test predictions reproduce 0.587904 three-way accuracy,
0.453888 QWK, and 0.533193 three-way macro-F1 on 7,093 answers / 248
questions. Label this exploratory (test seen in v1); the test set was seen in
v1 and is not a confirmatory evaluation. Test five-way predictions are absent,
so five-way test accuracy is unavailable.

[Tested] Exploratory test split metrics from saved predictions:

| Dataset / split | N / questions | Accuracy | Macro-F1 | Weighted-F1 | QWK |
|---|---:|---:|---:|---:|---:|
| Beetle test_ua | 439 / 44 | 0.676537 | 0.639081 | 0.661298 | 0.578333 |
| Beetle test_uq | 819 / 9 | 0.615385 | 0.541312 | 0.587960 | 0.449666 |
| SciEntsBank test_ua | 540 / 135 | 0.605556 | 0.560423 | 0.594765 | 0.513814 |
| SciEntsBank test_uq | 733 / 15 | 0.552524 | 0.482605 | 0.524142 | 0.421056 |
| SciEntsBank test_ud | 4,562 / 46 | 0.578036 | 0.524730 | 0.561604 | 0.441364 |

## Remaining baseline blockers

[BLOCKED] The Vishwajeet seed predictions, all-seed aggregation, UID-aligned
comparison, metrics, split metrics, error overlap, evaluation config and
manual review files listed in the metric-discrepancy report are absent.
A_seed_summary_v2.json says status missing. The user-supplied comparison is
not reproduced here.

[Verified] The local working COPY has 167 cells, 68 code cells, valid JSON,
and no non-null execution counts. A separate 169-cell COPY_UPDATED file has
saved outputs, but its Colab origin is unverified and it is not the designated
working COPY. Saved notebook outputs do not prove execution provenance.

[BLOCKED] Local CBSE/demo files do not establish CBSE or Indian schoolchildren
validation. No student pilot is evidenced. No pinned requirements file or
clean-runtime reproduction is available. No scientific literature comparison
was checked offline.