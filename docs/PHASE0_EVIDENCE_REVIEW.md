# Project S — Phase 0 Evidence Review

## 1. Executive assessment

**Verdict: PARTIALLY DECISION-READY; NOT READY FOR PHASE 1.** The prior audit's central findings about scorer inputs, pooling, rubric non-use, local policy drift, and evaluation optimism are supported by the source and local metadata checked here. They are sufficient to prevent unsafe execution and to frame decisions. They do not establish which configuration is live in Drive, which notebook Jigar will submit, which question/rubric bank is authoritative, or that any clean confirmation set exists.

This was a static review. No notebook, model, script, inference, training job, or test suite was run. No test dataset/split file was opened. No notebook output was inspected. Local files do not prove current Drive synchronization.

## 2. Audit-document accuracy review

| Prior document | Review result | Qualification or correction |
|---|---|---|
| `docs/REPOSITORY_AUDIT.md` | Main scorer, notebook, bank, and evaluation statements are supported. | Add that the nested `A_submission_v2/` package is not a self-contained runtime root: it has `demo/` and `reports_v2/`, but no `interim/`; `A_predict.py` builds `INTERIM` from `PROJECT_S_ROOT`. Its reported metric summaries are from saved reports, not recomputed here. |
| `docs/SOURCE_OF_TRUTH.md` | Correctly identifies the operational import path and leaves configuration, bank and notebook authority unresolved. | Clarify that a hash-consistent packaged JSON/policy pair does not by itself establish a usable runtime: the scorer expects policy under the selected root's `reports_v2/` and model artifacts under that same root's `interim/`. |
| `docs/IMPLEMENTATION_GAP_ANALYSIS.md` | Risks and acceptance criteria are generally evidence-backed or clearly future recommendations. | The subject-specific criteria are proposals, not existing functionality. The two bank schemas must not be merged by concatenation; they require schema/ID/provenance mapping and human sign-off. |
| `docs/FILE_CHANGE_PLAN.md` | Protected/backup/runtime roles match the inspected rules and paths. | Any planned file changes remain subject to the AGENTS.md notebook-only rule and specific user approval. This review does not authorize implementation. |

The prior four documents remain unchanged. They do not themselves contain the five-agent status matrix requested by this review; the matrix is provided below and in this response.

## 3. Evidence verification matrix

| Finding | Evidence / exact location | Method | Confidence |
|---|---|---|---|
| Operational scorer bytes | `project_s_qa/reports_v2/A_predict.py`, SHA-256 `CA7C2752A4863F2A24B20EC7CD9000B651D83A0CFC39709F0080EBCBDAD0A053`; root and 12 other local copies match. | File hashes and text inspection. | VERIFIED locally; live Drive UNVERIFIED |
| Scorer inputs/pooling | `A_predict.py:61–75, 92–101, 110–136, 153–170`. | Read source as text. | VERIFIED |
| Policy fallback | `A_predict.py:16–17, 139–141, 162–165`. | Read source and policy metadata. | VERIFIED locally |
| Root reference/config | `project_s_qa/reports_v2/A_demo_reference_outputs_v2.json`, hash `C99B7D84D000046C9629708D5EE440D5A20AB28FD298F63708E2E8C13F89DC92`; mode pooled and scorer hash matches, stored policy hash `babf76f460d2a6516d9ef11d317f69ceddb0958dd67a2ce06d3b67496163ad25`. Root policy is absent. | JSON keys and hashes; policy filename/hash search in project/backups/handover. | VERIFIED locally; live Drive UNVERIFIED |
| Packaged pair | `project_s_qa/A_submission_v2/reports_v2/A_demo_reference_outputs_v2.json`, SHA `EA5288E9F12B25D28A66F36EC38D48B08C65E19452BF3B5EFA17EED2BE20AEB9`; policy SHA `B6548EDEB682EABD2BA6B74D9B9B67BFF293C1FEA9C3CB6345E0A7EBF7E9EF9B`. Embedded policy hash matches the packaged policy. | JSON field and SHA-256 comparison. | VERIFIED as an internally consistent pair, not as live runtime |
| Packaged runtime completeness | `project_s_qa/A_submission_v2/` contains `demo/` and `reports_v2/`; no `interim/` directory was present. `A_predict.py:8–10` derives `interim/` from root. | Directory names and source. | VERIFIED locally |
| Notebook candidates | Current updated: 169 cells, SHA `F2E2A4A5FDD7BEAA208A192F6101EC9CB40789400B0D823003554FB1F4AABD4D`; dated D: 169 cells, SHA `37170A8B10DD590C300198BB45A5543B829D4A723443D2268E49A2375A8876C5`; Phase 2 executed copy: 169 cells, SHA `EBB83C058F58CF724153BB897BBDB0854E5A390FBB9EB5BF0A29E885042CC787`. | JSON cell counts; source-only comparisons; file hashes. No outputs read. | VERIFIED locally |
| Notebook source difference | Current updated and D have identical source; executed copy differs only in cell 157. Cell 157 in executed copy adds policy existence/hash checks and wraps only Drive mount in try/except. | JSON source fields only. | VERIFIED |
| Execution metadata | Non-null execution counts: current updated 5 code cells, D 8, executed copy 4. Counts at cells 157/159/161/163 are current 2/3/4/5; D 2/3/4/5; executed 6/2/3/4. | JSON `execution_count` metadata only; outputs were not read. | VERIFIED metadata; successful provenance UNVERIFIED |
| Demo import path | Updated notebook cell 159 lines 5–8 inserts `/content/drive/MyDrive/project_s_qa/reports_v2`; lines 14–21 read the processed CSV and require `question_id`, `question_text`, `reference_answer`. | Read source only. | VERIFIED source; live path UNVERIFIED |
| Question-bank records | Handover `questions.json`: 12 Science questions, grades 4/5/6 counts 4/6/2, all `draft_unreviewed`, no chapters or populated required concepts. Handover `rubrics.json`: 12 linked records, all draft; required concepts and contradictory claims are not populated; variants, misconception and partial-criteria fields are present but unreviewed/placeholders. | Parse JSON metadata and count fields; no model/data run. | VERIFIED structural facts; educational quality UNVERIFIED |
| Packaged rubric records | `A_rubrics_v2.json`: 251 question-keyed records; all have required concepts; statuses 248 `auto_draft`, 3 `demo`; concept statuses 248 auto-draft-unreviewed and 3 hand-written-unreviewed. It also has accepted-variant fields in 155 records, misconception fields in 116, and worked-example/contradiction fields in 251. | Parse JSON metadata only. | VERIFIED field presence/status; correctness UNVERIFIED |
| Rubric use | `PROJECT_S_QA_HANDOVER/src/block64_demo_bank.py:23–30`; `project_s_qa/reports_v2/A_predict.py` has no bank/rubric load. | Read source. | VERIFIED |
| Evaluation state | `EXP1_REPRODUCE_v2.py` validates aligned dev UIDs and writes saved analyses; reports call results dev-only/optimistic. EXP3 report marks provenance unresolved. Phase 7 discrepancy report says Block 37's 0.588 is a legacy v1 component-average, not current pooled A_predict. | Read source and non-test reports; no analysis rerun. | VERIFIED that records say this; underlying results not recomputed |
| Confirmation set | Phase 7/8 reports state no clean locked-test claim and prior test exposure. No independent confirmation source was established by this audit. | Review non-test documentation and filenames; no test files opened. | BLOCKED / not established |

## 4. Five-agent findings

### Adversarial Evaluator — PARTIALLY VERIFIED

The current scorer's code path supports the documented three-component equal 5-class probability average, 5-to-3 collapse, max-probability confidence and policy-based review flag (`A_predict.py:110–170`). Only DistilRoBERTa receives question text; SBERT-LR and NLI-LR do not (`:61–68, 92–101, 115–125`). Partial is a classifier output, not concept-counted. The local saved reports label development metrics optimistic. Model-training UID provenance and live policy use remain unverified. No accuracy gain from a future relevance or rubric change is established.

### Assessment Architect — PARTIALLY VERIFIED

Two structurally different banks exist. The 12-record handover bank is Science-only, grades 4–6, and entirely draft/unreviewed; its rubric fields do not establish substantive reviewed criteria. The separate 251-record package rubric uses another schema/status system and is also unapproved. The validation module checks structure and linkage, not educational truth. No evidence establishes readiness for Social Science, Mathematics or English.

### Systems Architect — PARTIALLY VERIFIED

The notebook's local import target is the root scorer path, but no live Drive version was verified. Thirteen local scorer copies have the same hash; the extracted tool copy differs. The root JSON/policy configuration is incomplete; the packaged pair is internally hash-consistent but lacks an adjacent `interim/` directory if treated as a root. Notebook D/current-updated source matches; the executed copy differs at cell 157. No single notebook is proven to be the current submission.

### Evaluation Scientist — PARTIALLY VERIFIED

Experiment 1 is saved-artifact, development-only comparison of 2,049 and 2,030 rows; its report classifies the result INCONCLUSIVE, with question-grouped accuracy and QWK intervals including zero. Experiment 2 uses saved dev artifacts. Experiment 3 is a provenance audit; training UID overlap and pooled-LR fit provenance are not resolved. Phase 8 training/gating scripts are candidate drafts, not run evidence. A new clean confirmation set is not established.

### Chief Decision Officer — PARTIALLY VERIFIED

Retain the current scorer as a frozen baseline; do not rebuild or promote candidates now. Resolve configuration/root paths and notebook selection first; choose a bank only with human provenance/review; establish a locked evaluation protocol before candidate selection. These are recommendations; Jigar retains the decisions.

## 5. Cross-examination

| Conflict | Evidence on each side | Resolution |
|---|---|---|
| “Packaged pair is consistent” vs “runtime is unsafe” | Packaged reference JSON points to the available packaged policy hash. But Block 60 and A_predict default to the top-level project root, and the package has no `interim/` directory. | Both are true. The pair is internally consistent but not proven operational at the notebook's root. Stage or configure it only after Jigar selects the root and approves the file set. |
| D/current updated vs Phase 2 executed notebook | D and current updated source match. Executed copy adds policy validation at cell 157. Phase 2 report calls it the executed copy; Phase 4 checklist separately says execution provenance is partial and cloud sync is unverified. | Likely different evidence claims/time scopes. The local executed-named file exists and has execution metadata, but this does not prove which live files it loaded or successful reproducibility. Jigar must select the run source. |
| 12-item bank vs 251-entry rubric | Distinct IDs, schemas, fields and status vocabulary. Neither is called authoritative by the repo. | Unresolved. Do not merge automatically; first map IDs/schema/provenance and review content. |
| “Rubric fields exist” vs “rubric scoring exists” | Handover UI retrieves and displays rubric; wrapper explicitly passes only question/reference/answer and emits `rubric_used_for_score=False`. Frozen scorer has no rubric argument. | Resolved: fields are stored/displayed, not used for scoring. |
| Saved development metrics vs independent generalization | Reports show aligned dev analysis and explicitly label it optimistic; docs report prior test exposure. | Resolved: use dev metrics only as exploratory/selection evidence. No independent confirmation result is established. |
| Block 37's 0.588 vs current pooled baseline | `PHASE_7_METRIC_DISCREPANCY_REPORT.md` attributes the dev 0.588 to averaging legacy v1 component probabilities; current deployed Path A has separate saved v2 probabilities. | Resolved in the report; retain the label-space and scorer-version distinction in future summaries. |

## 6. Contradictions, unsupported claims and missing evidence

1. **No substantive scorer-code contradiction** was found in the four audit documents. The root/policy discrepancy is correctly stated.
2. **Runtime-root qualification was missing:** the nested package does not contain the `interim/` path that its scorer would derive if treated as `PROJECT_S_ROOT`.
3. **The bank summary was incomplete, not false:** the 12 handover rubric records include variant/misconception/partial-criteria fields, but those are drafts/placeholders; the rubric records themselves have no populated required concepts. This does not make them reviewed or score-effective.
4. **No review approval exists:** neither `auto_draft`, `demo`, `hand_written_unreviewed`, nor `draft_unreviewed` is evidence of expert approval.
5. **Notebook metadata is not execution provenance:** execution counters exist, but the runtime files, environment, cloud sync and cell output success cannot be proven by counters alone.
6. **Evaluation records have differing scope:** Phase 2's report describes a saved run copy; Phase 3 remains PARTIAL; Phase 4's checklist says local archive/parity PASS WITH LIMITATIONS but separate execution provenance and cloud sync are not verified.
7. **No clean confirmation set is evidenced.** Prior project documents state test exposure; do not relabel existing test data as locked confirmation.
8. **No four-subject bank is evidenced.** Only Science drafts appear in the handover bank; package rubric metadata is not a reviewed subject-wise answer key.

## 7. Risk register

| Risk | Severity | Evidence | Required gate |
|---|---|---|---|
| Wrong threshold/review policy loaded | Critical | Root policy missing; fallback is silent and differs from packaged policy. | Exact root, policy and reference hashes verified before Colab. |
| Candidate or notebook drift | High | Cell 157 differs; multiple copies and local-only history. | Select a notebook, create a new run copy, source-diff and hash it. |
| Educationally invalid rubric/question | High | Draft/unreviewed status, incomplete provenance and no expert sign-off. | Human content approval by subject before scoring claims. |
| Unseen/off-topic and Partial weaknesses | High | Question absent from SBERT/NLI; no on-topic or concept-count rule. | Human-adjudicated relevance/Partial evaluation; candidate remains separate. |
| Optimistic evaluation / leakage | Critical | Dev selection and prior test exposure recorded; provenance unresolved. | New untouched question-grouped confirmation set and locked analysis plan. |
| Runtime reproducibility | High | Hub/cache and live Drive state unverified; package lacks interim root. | Runtime manifest, exact dependency lock and file hashes. |

## 8. Corrections required to the original audit

No edits to the original four reports were made. For future use, add the package-root/interim qualification, describe the 12-rubric fields as draft/placeholders, and retain the five-agent status and cross-examination tables in this review. Keep the existing scorer, policy and notebook conclusions as written, with the explicit local-vs-live scope.

## 9. Overall Phase 0 evidence-review verdict

**PARTIALLY DECISION-READY.** Evidence is strong enough to retain the deployed scorer as a frozen baseline, prohibit automatic promotion, identify the local import path and state the configuration conflict. It is not strong enough to declare a live runtime, submission notebook, canonical bank, approved rubric or independent confirmation set. Phase 1 remains **NOT READY** until the decisions and entry criteria in `PHASE0_DECISION_RECORD.md` are satisfied.

## HOW THIS HELPS ACCURACY, AND BY HOW MUCH

Direct measured accuracy improvement: **0 percentage points**. Resolving runtime configuration, reviewing content, and separating model selection from confirmation can make future accuracy comparisons trustworthy. A rubric or relevance feature could help or hurt; its effect is unverified and must be measured on a clean, question-grouped confirmation set.
