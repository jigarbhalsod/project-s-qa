# G1/G2 CDO recommendation — 16 November 2026

## Decision status

G1 and G2 candidates are approved by Jigar for review, not operationally
resolved. Phase 0 remains open. G3 is pending a user-run read-only Colab
preflight; G4-G6 remain blocked. Phase 1 has not started.

## G1 — notebook

Approved local reference candidate:
`drive_backup_20261107/notebooks/Jigar_Q&A_Branch_Baseline_COPY_UPDATED.ipynb`,
169 cells, SHA-256
`37170A8B10DD590C300198BB45A5543B829D4A723443D2268E49A2375A8876C5`.
The hash was recomputed locally and matches the approved value. This is a
local dated snapshot, not proof of authoritative or live Colab identity.
The Phase 2 executed copy has stored outputs but differs from D in cell 157;
that source delta means it is not a clean replacement. No notebook is
verified as live.

**Verdict: BLOCKED BY MISSING EVIDENCE.** D is the best local reference
candidate; user selection of a runtime notebook and live identity check remain
necessary.

## G2 — configuration

Approved candidate root JSON:
`project_s_qa/reports_v2/A_demo_reference_outputs_v2.json`, SHA-256
`C99B7D84D000046C9629708D5EE440D5A20AB28FD298F63708E2E8C13F89DC92`.
It declares pooled mode, the matching local scorer hash, and policy hash
`BABF76F460D2A6516D9EF11D317F69CEDDB0958DD67A2CE06D3B67496163AD25`.
The matching policy candidate is
`Project_S_QA_Evidence/Phase_0/scratch/policy_compare_20261107_160707/staged_policy.json`,
with that SHA-256. The policy is not at the scorer's expected path
`project_s_qa/reports_v2/A_abstain_policy_v2.json`, which is absent. The
scorer silently falls back to threshold 0.60 when policy is absent. The
approved policy candidate specifies 0.64 and disables contradiction review.

The top-level local root has model artifacts but misses the policy at the
expected path. The nested packaged root has a hash-consistent JSON/policy pair
but lacks required interim model artifacts. Neither local layout is fully
operational as-is.

**Verdict: BLOCKED BY MISSING EVIDENCE.** The candidate pair is approved, but
policy staging and live runtime verification remain pending.

## Staging and G3

Policy staging is approved in principle only. The separate plan is
`G2_POLICY_STAGING_WRITE_PLAN.md`; staging has not occurred and requires
separate explicit authorization for the exact copy. The expected Colab root
is `/content/drive/MyDrive/project_s_qa`, based on local scorer source; live
Drive state is unverified. Use `G3_READ_ONLY_PREFLIGHT_CHECKLIST.md` after
policy staging is separately authorized and completed.

## Remaining decisions and blockers

1. Confirm the notebook path/hash to use in Colab and verify its identity.
2. Separately authorize the exact policy copy operation; then verify all
   paths and hashes in the user-run Colab preflight.
3. Select a canonical question/rubric source and qualified reviewers (G4-G5).
4. Approve the evaluation protocol and establish independent confirmation
   data (G6).

No staging, notebook/scorer change, inference, training, or Phase 1 work is
authorized by these candidate approvals.