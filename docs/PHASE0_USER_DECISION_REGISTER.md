# Project S — Phase 0 User Decision Register

No choice below is approved by this report. Recommendations are not
deployment permission.

| Decision | Available options | Evidence | Recommendation | Approval needed | Status |
|---|---|---|---|---|---|
| Notebook | Working 167-cell COPY; updated 169-cell local file; D 169-cell dated snapshot; 169-cell Phase 2 executed copy | Four local SHA-256 values and source differences are in `PHASE0_FINAL_CLOSURE_REPORT.md`; no candidate checks JSON's own hash | Select one exact file/hash, or authorize a new run copy in a separate task after source review | Jigar must state path and SHA-256 | OPEN / BLOCKED |
| Runtime root | `/content/drive/MyDrive/project_s_qa` candidate; other root only if selected files and paths are verified | Notebook source uses this Drive root; scorer reads `PROJECT_S_ROOT` or its default; no live runtime inspected | Use one root for notebook imports and scorer artifacts, and bind `PROJECT_S_ROOT` explicitly or verify default behavior | Jigar approves root and live preflight confirms it | OPEN / BLOCKED |
| Configuration | A: top JSON + policy hash `BABF76F4...63AD25`; B: packaged JSON+policy hashes `EA5288E9...20AEB9` + `B6548EDE...F7E9EF9B`; C: new approved pair | A policy bytes matching declared hash exist in Phase 0 scratch, not adjacent to scorer; B pair matches internally, but nested package lacks interim; outer dated snapshot is not live | No option sufficiently verified for deployment. A is exact-content match for current top JSON; B is a complete local snapshot pair. Approve exact pair and a separate staging plan | Jigar chooses A/B/C and exact paths/hashes; no copy/replace authorized here | OPEN / BLOCKED |
| Question-bank source | 251-record package; 12-question Science prototype; create a new canonical bundle | Package has 251 records but no subject/grade and no `verified_by`; prototype has 12 Science drafts, grades 4–6; no four-subject approvals | No source ready for approval; select a starting point only after provenance review | Jigar selects source/schema owner; do not merge automatically | OPEN / BLOCKED |
| Subject review | Nominate reviewers for Science, Social Science, Mathematics, English | No names, qualification evidence, or sign-offs found | Two independent reviews for disputed/high-impact content plus adjudication | Jigar nominates qualified reviewers and arranges reviews | OPEN / BLOCKED |
| Evaluation confirmation | Existing data; new independent question-disjoint set | Existing dev is optimistic and used for selection; prior test exposure is documented; no clean locked set established | New confirmation set required; pre-register protocol and hold labels with a custodian | Jigar approves collection, custody, sample-size plan, metric gates | OPEN / BLOCKED |
| Live Colab check | User-run read-only preflight | No authorized live inspection available; dated local snapshot is not cloud confirmation | Run `PHASE0_COLAB_READ_ONLY_PREFLIGHT.md` after notebook/config selection | Jigar mounts Drive and returns complete output | OPEN / BLOCKED |

## Decisions Jigar can make now

1. Name the exact notebook path and SHA-256 to use, or say no candidate is
   approved yet.
2. Select runtime root and explicitly set/confirm how `PROJECT_S_ROOT` will
   agree with the notebook import root.
3. Select Option A, B, or C for JSON/policy and approve the exact hashes. This
   is a decision only; it does not authorize copying or deployment.
4. Choose which bank is a starting point for review, or direct creation of a
   new canonical bundle, without calling it approved.
5. Approve the proposed review and independent-evaluation workflows.

## External actions

- Run the read-only Colab preflight from the authorized account and return
  its output.
- Nominate qualified reviewers for all four subjects; collect sign-offs and
  resolve disagreements.
- Collect a new provenance-documented, human-reviewed, question-disjoint
  confirmation set and keep it locked until the model/config/analysis are
  frozen.

## Decisions that cannot yet be made

- **Notebook/runtime deployment:** live Drive state and authoritative source
  are unknown; local hashes alone do not prove which copy Colab opens.
- **Final policy in use:** the file matching the top JSON hash exists only in
  audit scratch, while the active root is missing its adjacent policy; no live
  import path has been checked.
- **Canonical assessment content:** no four-subject expert review or approved
  provenance is evidenced.
- **Final accuracy claim:** no clean independent confirmation set exists;
  development and previously exposed data cannot substitute.
