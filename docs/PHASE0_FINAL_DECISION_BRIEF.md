# Project S — Phase 0 Final Decision Brief

**Recommendation:** `APPROVE REVISED PHASE 0 CLOSURE DEFINITION` as a staged
readiness policy, subject to Jigar's approval. This is not approval to start
Phase 1. The current Phase 0 remains open until Jigar approves the scope and
the minimum foundation items below.

## Decision summary

| Decision | Options | Evidence | Preferred option | Approval required | Blocks Phase 1? |
|---|---|---|---|---|---|
| Phase 0 scope | Keep six all-before-Phase-1 gates; revise into foundation/runtime/experiment/pilot gates; defer all | Live runtime, complete four-subject content review, and a new confirmation set are not prerequisites for isolated schema design, but remain necessary before the work they protect. | Revised, staged gates | Jigar explicitly adopts scope | Yes, until scope approval; no implementation in this task |
| Baseline notebook | Working COPY (167); updated local (169); D snapshot (169); executed copy (169) | Source hashes/cells differ; no candidate validates the JSON file's own hash; live runtime unknown. | No notebook selected. Later prefer a separately approved minimal runtime entrypoint or exact source-reviewed run copy. | Exact path/hash and source-boundary approval | Blocks notebook execution and scorer integration, not schema design |
| Runtime root | Candidate `/content/drive/MyDrive/project_s_qa`; other root with verified contents | Notebook import path and scorer `PROJECT_S_ROOT` can diverge. No live Drive evidence. | One explicit root; same root for notebook, scorer, config and artifacts | Jigar selects; live preflight must pass | Blocks runtime execution |
| Config | A current root JSON + policy bytes matching its declared hash; B packaged JSON/policy; C new approved pair | A hash-matching policy bytes exist in audit scratch but not runtime path. B pair is internally hash-consistent, but only a local snapshot; nested package lacks interim. C is not defined. | No option is deployment-ready. B is simplest complete local snapshot candidate; A is the exact-content match to the current root JSON. | Select option, paths and hashes; separate approval for staging | Blocks scorer execution |
| Question bank | 251-record package; 12-question Science prototype; new bundle | Package lacks subject/grade and human review; prototype is Science-only draft; schemas differ. | Neither canonical; select only as a starting source after mapping/provenance review | Jigar chooses source/schema owner | Blocks content integration and subject-specific claims |
| Assessment reviewers | Names/qualifications unknown | No reviewer assignment or sign-off evidence | Nominate subject experts for all four subjects and an adjudicator | Jigar nominates and arranges actual review | Blocks approved content and pilot; not generic schema design |
| Evaluation | Existing data; new clean confirmation set | Dev used for selection; historical test exposure; train/probability provenance incomplete | New question-disjoint, independently reviewed, custodian-held confirmation set | Approve collection, custody, sample-size precision plan and acceptance rules | Blocks confirmatory accuracy claims/model promotion; not schema work |

## Notebook/runtime choice

**Verified:** local candidates are not interchangeable: 167-cell COPY and
three 169-cell variants have different hashes/source; the Phase 2 executed
copy has a cell-157 source change relative to D. No live Colab root is
verified. The current notebook import path is hard-coded; scorer root can be
overridden with `PROJECT_S_ROOT`.

**Proposed:** keep the large research notebook frozen. For future execution,
prefer a small, separately approved runtime entrypoint with exact frozen
scorer/config hashes and one root. If an existing notebook is retained, select
one exact path/hash and review its source changes. No new runner or notebook
was created here.

## Configuration choice

- **Option A:** root reference JSON `C99B7D84D000046C9629708D5EE440D5A20AB28FD298F63708E2E8C13F89DC92`
  declares scorer hash `CA7C2752A4863F2A24B20EC7CD9000B651D83A0CFC39709F0080EBCBDAD0A053`
  and policy hash `BABF76F460D2A6516D9EF11D317F69CEDDB0958DD67A2CE06D3B67496163AD25`.
  Bytes matching that policy hash exist at
  `Project_S_QA_Evidence/Phase_0/scratch/policy_compare_20261107_160707/staged_policy.json`;
  they specify pooled, temperature 1, threshold 0.64, contradiction flag
  false. **Against:** provenance and runtime placement are not established.
- **Option B:** packaged JSON hash `EA5288E9F12B25D28A66F36EC38D48B08C65E19452BF3B5EFA17EED2BE20AEB9`
  and policy hash `B6548EDEB682EABD2BA6B74D9B9B67BFF293C1FEA9C3CB6345E0A7EBF7E9EF9B`
  match each other and the local scorer. **Against:** local snapshot only; the
  nested submission package lacks `interim/`; live state and notebook choice
  are unknown.
- **Option C:** create a deliberate new config pair. **Against:** no approved
  generation process or manifest exists; this changes configuration and needs
  a separate decision.

**Choice:** no option is sufficiently verified for deployment. Jigar should
approve A/B/C and exact runtime paths/hashes. Do not copy, replace, or sync
anything until separately authorized. The scorer's missing-policy fallback
(`A_predict.py:139–141`) makes path/hash validation mandatory.

## Question-bank and assessment decision

**Evidence:** package has 251 public-data rubric records without subject/grade
metadata; 248 are `auto_draft`, 3 `demo`, and no `verified_by` values exist.
The 12-question prototype is all `draft_unreviewed`, Science only. Earlier
docs disagree on accepted-variant/misconception counts for the package.

**Choice:** do not call either source canonical or merge them. Jigar may select
one as a mapping/provenance starting point or approve a new bundle. The
minimum common schema should include stable ID, subject, grade, chapter/topic,
difficulty, prompt, reference answers, accepted variants, required/supporting
concepts, misconceptions, contradictory claims, partial-credit criteria,
source/provenance, author, reviewer, status, timestamp, version and change
rationale. Subject reviewers must approve content before it is presented as
educationally validated.

## Proposed Phase 0 scope and decision rationale

The old definition is too restrictive for *all* Phase 1 work because it makes
live runtime preflight, four-subject content review, and collection of a final
confirmation set prerequisites for non-scoring schema/interface design. Those
requirements remain hard before scorer execution, rubric-based claims, pilot,
and confirmatory accuracy claims.

**Safeguards if revised:** freeze/hash the baseline; isolate new work from
`A_predict.py`, notebooks and frozen artifacts; require Jigar's scope
approval; label all unreviewed content; keep experiments dev-only and
exploratory; do not call a candidate better or deploy it; require runtime
preflight before any scorer call; require independent data before confirmation.

**Phase 1 entry under this recommendation:** generic question-bank schema,
versioning, ingestion validation, and an isolated non-scoring interface may
begin only after Jigar approves the revised scope, protected baseline boundary,
schema goals and acceptance checks. No Phase 1 implementation began here.
Training, inference, scorer integration, CBSE/student assessment, or model
promotion remain blocked by the relevant gates.

## Immediate next action

Jigar should answer the decisions in
`docs/PHASE0_USER_DECISION_REGISTER.md`: approve/reject the revised scope;
select notebook/root; choose a JSON/policy option; choose a bank as a starting
point; nominate reviewers; approve the evaluation/custody plan. Then run the
Colab preflight only after the exact runtime manifest is approved.
