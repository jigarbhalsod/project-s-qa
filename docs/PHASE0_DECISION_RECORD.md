# Project S — Phase 0 Decision Record

**Purpose:** prepare decisions; this document does not implement any of them. The deployed scorer remains frozen.

## Five decisions

| Decision | Current state | Options | Evidence | Risks | Recommendation | Approval required | Next action | Blocking status |
|---|---|---|---|---|---|---|---|---|
| 1. Runtime notebook and root | Three 169-cell candidates are local. Current updated notebook SHA `F2E2A4A5FDD7BEAA208A192F6101EC9CB40789400B0D823003554FB1F4AABD4D`; D SHA `37170A8B10DD590C300198BB45A5543B829D4A723443D2268E49A2375A8876C5`; Phase 2 executed file SHA `EBB83C058F58CF724153BB897BBDB0854E5A390FBB9EB5BF0A29E885042CC787`. D and current updated source are identical; executed source differs only in cell 157. | A. D/current source as baseline; make a fresh run copy. B. Executed copy as baseline. C. Another user-supplied Colab export. | D/current cell157 lacks policy hash check. Executed cell157 adds policy existence/hash validation and mount try/except. All local Block 60 paths point at `/content/drive/MyDrive/project_s_qa`. Source and execution-count metadata are local; live Drive unavailable. | Choosing executed copy carries its extra source patch; choosing D requires explicit strict policy preflight before run. Counts do not prove a successful or reproducible run. | **Recommendation only:** use D as the comparison baseline and create a new, separately named run copy after Jigar confirms; port no code without approval. Keep runtime root `/content/drive/MyDrive/project_s_qa` unless Colab proves another root. | Yes: select notebook and confirm runtime root. | Reply with exact source file and intended run-copy name/root. | Blocks Phase 1 runtime work. |
| 2. JSON/policy pair | Root JSON says pooled and has matching scorer SHA, but references unmatched policy hash `babf76…`; root policy absent. Packaged JSON/policy hashes match, but nested package lacks `interim/`. | A. Locate original policy for root JSON hash. B. Approve package JSON+policy copied to root `reports_v2/`, preserving originals. C. Recreate reference JSON from an approved scorer/policy pair. | Root JSON SHA `C99B7D84…F89DC92`; packaged JSON SHA `EA5288E9…20AEB9`; packaged policy SHA `B6548EDE…F7E9EF9B`; A_predict SHA `CA7C2752…D0A053`. Both JSONs name the A_predict hash; only packaged JSON names an available matching policy. Scorer defaults to root and silently falls back if its policy is missing (`A_predict.py:139–141`). | Option A cannot proceed without artifact. B changes runtime policy selection/threshold to the packaged 0.64 policy and must preserve the root model-artifact paths. C needs an approved reproducible generation procedure. Live Drive state is unknown. | **Recommendation only:** prefer B if Jigar confirms that the packaged policy is intended; place the verified pair at the root paths while keeping `PROJECT_S_ROOT` at the root that contains `interim/`. Otherwise block runtime and retrieve the original policy. Do not copy now. | Yes: select exact JSON/policy pair and approve any staging. | Choose A, B or C; if B, confirm policy values and destination. | Critical blocker for any scorer run. |
| 3. Authoritative question/rubric source | Two separate local sources exist; neither is designated canonical. | A. Use the 251-record package rubric as source after review/migration. B. Use the 12-record handover bank as a small prototype. C. Author a new canonical bundle and migrate approved records. | Package `A_rubrics_v2.json`: 251 entries, 248 `auto_draft`, 3 `demo`; all concept statuses remain unreviewed. Handover `questions.json`/`rubrics.json`: 12 Science, grades 4–6, all draft; no populated required concepts; criteria are placeholders/unreviewed. Schemas and identifiers differ. `A_predict.py` does not load either source. | Direct merge risks ID collision, lost provenance, schema/status confusion and treating draft criteria as approved. A large auto-draft bank can create false confidence. | **Recommendation only:** do not merge. Select one schema as a starting point only after writing an ID/provenance migration map; treat both content sets as unapproved until reviewed. The 12-item bundle is a smaller prototype, not production truth. | Yes: choose source and data owner. | Name the source bundle and approve review process. | Blocks rubric-aware experiment and subject claims. |
| 4. Assessment review and approval | No expert approval evidence found. Science draft bank only; no verified Social Science, Mathematics or English bank. | A. One qualified reviewer per item. B. Two independent reviewers plus adjudication for disagreements. | Handover records use `draft_unreviewed`; package uses `auto_draft`/`demo` plus unreviewed concepts. Validation is structural, not semantic. | Unreviewed reference answers or rubrics can encode wrong facts or partial-credit judgments. | **Recommendation:** require source provenance and two-person review for rubric content; an independent adjudicator resolves disagreements. For Math review equivalence, units, tolerance and reasoning; Science concepts/misconceptions; Social Science facts, chronology and causality; English meaning-preserving paraphrase and context. No item becomes `approved` without reviewer identity/date and source. | Yes: nominate qualified reviewers and approve statuses. | Confirm reviewers, subject coverage and approval fields. | Blocks educational validity claims and rubric use. |
| 5. Evaluation and confirmation protocol | Saved results are development-only/optimistic. Prior test exposure is documented. No untouched confirmation set is established. | A. Obtain a new question-disjoint confirmation set. B. Collect new domain data with frozen labels. C. Continue only dev diagnostics and make no independent-improvement claim. | EXP1/2 are saved-dev analyses; Phase 8 uses dev for selection; EXP3 flags provenance gaps; Phase 7/8 records say no clean locked-test claim. Existing test data must remain exploratory. | Reusing exposed rows or choosing thresholds/checkpoints on confirmation data inflates results. Row-level resampling ignores question clusters. | **Recommendation only:** A or B before any claim of real improvement; C is the safe fallback until then. Keep test set sealed; do question-grouped split before training; perform all model/threshold selection inside train/dev or nested grouped CV; lock confirmation data and labels before one final evaluation. | Yes: approve data collection and protocol. | Specify population, source, grouping, label review and who controls the lock. | Critical blocker for validation or promotion. |

## Recommended evaluation protocol

This protocol is proposed, not an existing verified procedure.

1. **Population and provenance:** identify dataset, subject, grade, question source, answer collection procedure, UID, reference version, labeler(s), and label mapping. Freeze a manifest before scoring.
2. **Question grouping:** assign entire question IDs to splits; no answer to a held-out question may appear in training or model selection. Report warm/seen and cold/unseen questions separately.
3. **Separation:** keep train for fitting; development for architecture, checkpoint, calibration and threshold selection; use nested question-grouped CV within development if comparing candidates. Obtain a new, untouched confirmation set; do not use previously exposed test rows as confirmation.
4. **Locked evaluation:** freeze code, policy, threshold, model, dataset UIDs, labels and analysis plan before opening confirmation predictions. Evaluate once; changes require a new confirmation set.
5. **Metrics:** report accuracy, Macro-F1, weighted-F1, class-wise precision/recall/F1, Partial precision/recall, QWK for the three ordered labels, ECE and/or Brier score, and coverage versus selective accuracy. Give N for every slice and confusion matrices. Report each subject/dataset, warm/cold questions, and relevant grade groups separately.
6. **Uncertainty:** use paired question-group bootstrap intervals for candidate-minus-baseline metrics; state seed, resample count and interval method. Do not treat answer rows as independent when question IDs repeat.
7. **Selection and success:** choose primary metric and minimum meaningful improvement before training. Require the paired interval for the primary improvement to exclude zero, no predeclared safety-slice regression, and calibration/review behavior to be reported. A candidate never replaces frozen v2 automatically.
8. **Data controls:** keep negation controls diagnostic and outside training unless a separately designed training study is approved. Never access or relabel the existing exposed test set as an untouched holdout.

## Decisions ready for approval

- Confirm the notebook source (D, current updated, or another named file) and exact runtime root.
- Choose the configuration option (A/B/C) and whether a root-level staging change is approved.
- Choose a question-bank starting source, or direct a new bundle; do not merge by file concatenation.
- Nominate subject reviewers and approve review/status workflow.
- Approve creation and governance of an untouched question-grouped confirmation set.

## Decisions still unresolved

- Which notebook is the submission/run authority; no live Drive synchronization evidence exists.
- Whether packaged policy values are the intended deployed policy; the root JSON's referenced policy is missing locally.
- Which question/rubric bank is canonical and who owns content approval.
- Whether an independent confirmation set can be collected and when.
- Current hub cache/package availability and exact cloud runtime environment.

## External dependencies and missing local artifacts

- Missing local runtime file: `project_s_qa/reports_v2/A_abstain_policy_v2.json`.
- No local policy matched the root reference JSON's `policy_sha256` (`babf76…`).
- Live Google Drive listing and synchronization state are unverified.
- No untouched confirmation dataset is established in the local project evidence.
- Qualified reviewers and approvals are not recorded for either rubric source.

## FINAL READINESS

**NOT READY FOR PHASE 1.** The baseline can remain frozen, and static planning can continue, but runtime execution, rubric-aware scoring and accuracy claims are blocked until the root/policy pair, notebook, bank and confirmation protocol are explicitly selected and verified.

## HOW THIS HELPS ACCURACY, AND BY HOW MUCH

Direct measured improvement: **0 percentage points**. A hash-verified runtime prevents evaluating the wrong policy. Reviewed rubrics and subject-specific criteria can reduce assessment errors, while question conditioning and relevance checks are hypotheses only. The split protocol prevents optimistic leakage from being mistaken for model gain. Every possible accuracy effect remains unverified until tested on the locked, question-disjoint confirmation set.

## YOUR PART

1. Select one notebook by exact path and confirm `/content/drive/MyDrive/project_s_qa` or provide the verified Colab root.
2. Choose the JSON/policy option and approve or reject staging the packaged pair at the root paths; do not run Block 59 until its hash checks pass.
3. Choose the question-bank source and nominate subject reviewers; decide whether to migrate or start a new bundle.
4. Approve the review workflow and who may mark records approved.
5. Provide or authorize a new, untouched question-grouped confirmation dataset; do not reuse exposed test rows.
