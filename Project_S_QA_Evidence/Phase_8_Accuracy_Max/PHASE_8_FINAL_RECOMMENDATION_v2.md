# Phase 8 status and recommendation (v2)

**Status:** Stage 0 analysis is complete on current-v2 dev artifacts, with
Cleanlab/OOF analysis blocked. Stage 1 is prepared but not approved or run.
All reported scores are **dev-only, optimistic**. No 85% or 90% target is
promised.

## Protocol decision memo

Two paths were considered:

- **Existing official dev splits (`dev_ua` / `dev_uq`):** fewer new artifacts
  and simpler. But the current training script selects the checkpoint on
  `dev_uq`, and the gate also evaluates there, so it cannot independently
  confirm that selected checkpoint.
- **Nested question-grouped CV on dev:** more fold assignments, checkpoints,
  predictions, code, and compute. It separates inner checkpoint selection
  from outer dev evaluation and is the recommended protocol for Stage 1 gate
  estimates. It still uses dev and is not external confirmation.

**Proposed:** choose nested question-grouped CV if Stage 1 advances. A separate
clean confirmation set is required before claiming independent confirmation.
No protocol was applied.

## Stage status

| Stage | Status | Evidence / remaining condition |
|---|---|---|
| Stage 0 — high-confidence, Partial, data quality | DONE with limitation | Current-v2 report `E3_HIGH_CONFIDENCE_ERROR_BREAKDOWN_v2.md`; OOF/Cleanlab blocked because valid OOF probabilities are unavailable. |
| Stage 0 — E4 settings and protocol | DONE as draft | `E4_DEBERTA_EXPERIMENT_SPECIFICATION_v2.md`; Jigar must approve hyperparameters, seed discrepancy, margin, and protocol. |
| Stage 1 — DeBERTa | BLOCKED / needs approval | No training. Phase 3 report says PARTIAL; training waits for Phase 3 completion and explicit Stage 1 approval. Current scripts write to Drive Phase 8, not `/content/phase8_tmp`; approved temporary-output configuration is needed before a safe run. Existing gate is one-seed and does not implement all proposed gates. |
| Stage 2 — OOF stacking | UNAPPROVED | Requires a separately approved design and valid out-of-fold component probabilities. |
| Stage 3 — calibration/selective prediction | UNAPPROVED | Requires separate approval; keep 0.64 unchanged. |
| Locked evaluation / freeze | BLOCKED | Existing test exposure means no clean locked-test claim is available today. A new untouched confirmation set is future work. |

## Decisions needed before Stage 1

1. Complete Phase 3 demo evidence; its current report is PARTIAL.
2. Approve the E4 values and resolve the script seed 20261106 vs Notion 42.
3. Approve nested question-grouped CV or select the existing split for
   exploratory use only.
4. Approve the proposed 0.01 unseen-QWK non-inferiority margin and complete
   gate changes for three seeds, accuracy, overall QWK, Partial F1, and
   batch-1/32 latency median/p95.
5. Approve a temporary-copy output-path change to `/content/phase8_tmp`.
6. Give explicit Stage 1 approval. Stages 2 and 3 remain separately
   unapproved.

Fallback remains frozen v2 if prerequisites or gates fail. No scorer,
threshold, notebook, checkpoint, or frozen artifact was changed.
