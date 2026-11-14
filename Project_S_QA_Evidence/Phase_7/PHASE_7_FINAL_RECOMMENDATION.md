# Phase 7 final recommendation

Audit date: 6 Nov 2026.

## Recommendation

[Verified] Best reproducible model: Jigar's pooled v2 scorer, reproduced from
saved probabilities. It is the only current deployed model independently
reproduced in this audit; it is not proven better than Vishwajeet's model.

[Tested] Reproduced overall accuracy is 56.37% (three-class, dev, optimistic),
using pooled five-way probability collapse before argmax, N=2,049.
The alternate five-class argmax then map path is 58.03% on the same rows and
disagrees on 336 predictions; it is not the deployed policy.

[Tested] Best point estimate at at least 95% accuracy with N>=100 in the raw
dev confidence-threshold scan is 95.31% accuracy at 6.25% coverage (N=128,
52 questions), with a question-bootstrap 95% CI of 88.75%-100.00%. The
threshold was selected on dev, so this is dev, optimistic and the interval is
conditional. The highest observed point is 100% at 0.146% coverage (N=3);
that small sample is not a useful performance claim.

[Tested] The largest observed dev coverage with point accuracy >=90% is
8.05% (N=165), at 90.30% accuracy; its conditional question-bootstrap CI is
80.00%-97.93%. This does not establish a reliable 90% operating point.
No minimum practical coverage was supplied.

[Verified] The saved grouped-CV policy summary is 74.77% accuracy at 31.33%
coverage. It lacks row-level OOF outputs for independent reproduction or a
confidence interval. A careful headline is:
"74.77% accuracy at 31.33% coverage with teacher-review fallback"
(saved grouped-CV estimate; not independently reproduced).

[Tested] The 85% accuracy at 30% coverage target is NOT achieved. The
dev 30%-top-k point is 75.45% at 30.01% coverage (95% question-bootstrap CI
68.47%-81.83%); the fixed 0.64 threshold is 75.12% at 30.60% coverage.

## H1 / H5 / H8 findings

[Tested] H1: neither a data ceiling nor a model ceiling is established.
Exact normalized duplicate-label conflicts affect 0 of 2,049 dev rows; manual
error adjudication is absent, and current v2 component agreement is blocked.

[Tested] H5: unseen dev accuracy is 48.92%, macro-F1 44.62%, QWK 0.2949
(N=1,296; 27 questions), versus seen dev accuracy 69.19%; 36/177 questions
have under 40% accuracy.

[Tested] H8: Partial recall is 26.34%, precision 51.49%; 516/894 (57.72%)
of deployed-rule dev errors involve Partial.

## First improvement and blocked items

[Pending] First, obtain the missing Vishwajeet seed predictions and UID-aligned
comparison exports, then reproduce both systems on identical rows. Next,
blindly adjudicate high-confidence and Partial errors before testing a
Partial-targeted loss or ordinal objective.

[BLOCKED] Vishwajeet seed comparisons, the 2,049-UID comparison and overlap
counts are unverified because their listed files are absent. Current v2
per-component OOF predictions, completed human error reviews, and a grouped
OOF risk curve are also absent.

## Dynamic question bank

[Verified] The current working COPY has 167 cells; older 165-cell notes are stale. The 162 figure is a historical reference count, not the COPY count. Block 60 uses the fixed
CBSE CSV and a dropdown populated from its existing LOOKUP; no manual/CSV
question-add path, live dropdown refresh or runtime-bank write was found.
No Block 63 dynamic-bank code is integrated in the notebook.

[BLOCKED] block63_dynamic_bank.py and
reports_v2/A_question_bank_runtime_v1.csv were not found by name in the
project tree, notebook backups, flat-layout folders or ZIP member lists.
No notebook cell contains dynamic_bank or question_bank_runtime code.
draft_unreviewed appears in the Block 50 concept-draft code and static question
data; it does not establish a dynamic question bank.

[Unverified] Likely external locations to check, not searched in this audit:
Google Drive, a Colab runtime/session, Downloads, Recycle Bin, or the relevant
chat transcript.

Dynamic bank: not integrated / not verified in real Colab-Gradio. Not validated on CBSE data.

## Remaining risks

[Unverified] Execution provenance and cloud synchronization are not proven.
Vishwajeet comparison files, current v2 component OOF outputs and completed
human reviews are absent. The test split is exploratory and has question and
exact-input overlap. Semantic label/reference quality remains unadjudicated.
NLI/SBERT truncation exposure is not available. No CBSE/Indian schoolchildren
or student-pilot validation is established.

[Verified] No model, model artifact, notebook, threshold, training script or
gold label was changed or executed for this audit.