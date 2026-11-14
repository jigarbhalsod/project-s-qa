# Phase 0 Closure Report

## 1. Policy hash search

| Item | Result |
|---|---|
| [Verified] Staged JSON policy_sha256 | `babf76f460d2a6516d9ef11d317f69ceddb0958dd67a2ce06d3b67496163ad25` |
| [Verified] Staged hash file hit | `archive/project_s_qa_phase1_v1.zip!reports_v2/A_abstain_policy_v2.json`; 784 bytes; SHA-256 matches |
| [Verified] Second staged hash hit | Same archive: `project_s_qa_v2_package/reports_v2/A_abstain_policy_v2.json`; SHA-256 matches |
| [Verified] Packaged JSON policy_sha256 | `b6548edeb682eabd2ba6b74d9b9b67bff293c1fea9c3cb6345e0a7ebf7e9ef9b` |
| [Verified] Packaged hash file hits | `project_s_qa/A_submission_v2/reports_v2/A_abstain_policy_v2.json` and the matching backup copy; both 784 bytes and match |
| [Verified] ZIP hits for packaged hash | `project_s_qa/A_submission_v2.zip` and backup `A_submission_v2.zip`, each policy entry matches |
| [Verified] JSON timestamps | staged: 2026-11-06 00:02:08 +05:30; packaged: 2026-11-06 03:33:57 +05:30 |

[Verified] The staged hash is explained by archive entries; the packaged hash is explained by extracted files and archive entries. Both JSONs say `scorer_mode=pooled` and store the same A_predict SHA-256, `ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053`.

## 2. Block 59 static check

| Check | Result |
|---|---|
| [Verified] Heading/code | markdown cell 156; code cell 157 |
| [Verified] JSON path | `f"{ROOT}/reports_v2/A_demo_reference_outputs_v2.json"` |
| [Verified] Required checks | file exists; `scorer_mode == "pooled"`; JSON `a_predict_sha256` equals loaded `A_predict.__file__` SHA-256 |
| [Verified] policy_sha256 check | None; Block 59 does not read or validate this field |
| [Drafted] Staged JSON outcome | PASS for the three checks above, assuming its paired loaded scorer has the stored hash |
| [Drafted] Packaged JSON outcome | PASS for the three checks above, assuming its paired loaded scorer has the stored hash |
| [Verified] Strict fallback | Present for JSON/scorer validation: direct file assertion and assertions; no silent `both` fallback. This is a static conclusion, not a runtime test. |

## 3. Stored Block 59-62 outputs in COPY_UPDATED

[Verified] Notebook inspected: `notebooks/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb`, 169 cells. Only output fields of the four identified block code cells were inspected. No test-split rows or test metrics surfaced.

| Block | Code cell | execution_count | Stored outputs | Error/traceback | [Verified] Summary |
|---|---:|---:|---|---|---|
| 59 | 157 | 2 | yes (27 outputs) | no | Tesla T4; benchmark latency printed |
| 60 | 159 | 3 | yes (18 outputs) | no | model initialization logs and a temporary Gradio share URL were stored |
| 61 | 161 | 4 | yes (1 output) | no | negation component diagnostics printed |
| 62 | 163 | 5 | yes (1 output) | no | stage timing values printed |

[Verified] Block 59 saved output lines:

```text
Single-answer latency (median of 20 runs): 146.2 ms
Batch latency for 15 items (median of 20 runs): 214.6 ms (14.3 ms / item)
```

[Verified] Block 62 saved output lines:

```text
single DistilRoBERTa 10.1 ms
single NLI (whole-reference pairs only) 34.9 ms
single SBERT features 19.4 ms
single component_probs total 102.2 ms
single predict_batch total 106.3 ms
batch15 DistilRoBERTa 13.9 ms
batch15 NLI (whole-reference pairs only) 60.2 ms
batch15 SBERT features 31.6 ms
batch15 component_probs total 165.9 ms
batch15 predict_batch total 153.7 ms
```

[Verified] Stored execution counts and non-error outputs evidence that Blocks 59-62 ran without a saved exception. This confirms saved notebook execution evidence only; it does not verify that the temporary link remains active now.

## 4. Cell-count reconciliation

| Finding | Result |
|---|---|
| [Verified] Current COPY | 167 cells |
| [Verified] `before_phase5` backup | 165 cells |
| [Verified] Added cell | COPY cell 1: `### Run history note (30 Oct 2026)` |
| [Verified] Added cell | COPY cell 151: `### Block 56: withdrawn` |
| [Verified] README discrepancy | README says 165; the two added markdown cells explain 167 |
| [Verified] 162-cell reference | absent at the expected reference path |
| [Reported] T3 status | not blocking, per roadmap instruction |

## 5. Decision memo

| Option | Evidence for | Evidence against |
|---|---|---|
| [Verified] Use packaged JSON | its policy hash matches the extracted packaged policy and backup; scorer mode and scorer hash match the staged pair | Block 59 reads the root `reports_v2/` path, while packaged JSON is nested under `A_submission_v2/` |
| [Verified] Use staged JSON | it is at Block 59's expected `reports_v2/` path; scorer mode and scorer hash match; its policy hash matches entries in the Phase 1 archive | no standalone staged policy file was found at `project_s_qa/reports_v2/`; archive presence does not prove runtime policy availability |
| [Proposed] Regenerate JSON in Phase 2 via an approved process | would explicitly bind the selected active policy/scorer pair to the runtime path | requires Jigar to approve canonical policy selection and a non-overwriting generation/review process |

[Proposed] Recommendation: approve a controlled Phase 2 regeneration/review of the reference JSON after deciding which policy file is canonical. Do not replace either current JSON before that approval.

## Done-when status and remaining blockers

| Item | Status |
|---|---|
| [Verified] Policy hashes searched in project files, backup, and ZIP archives | done; both hashes have matching on-disk content |
| [Verified] Block 59 path, fields, and static outcomes for both JSONs | done; outcomes are Drafted, not runtime-tested here |
| [Verified] Stored outputs for Blocks 59-62 | done; no stored error/traceback; saved counts show execution |
| [Verified] Cell-count reconciliation and reference status | done; 167 vs 165 explained by two inserted markdown cells; reference absent |
| [Unverified] Canonical policy/JSON choice for future runtime | Jigar decision required |
| [Unverified] Live Drive contents and whether temporary Gradio link still works | not checked; no live Drive access used |
| [Reported] T3 reference comparison | not blocking |

[Verified] No notebook cell, model, training, or Project S script was executed; no installation, download, overwrite, or deletion occurred. No test split or saved test output was opened. Only the requested Blocks 59-62 stored outputs were inspected.
