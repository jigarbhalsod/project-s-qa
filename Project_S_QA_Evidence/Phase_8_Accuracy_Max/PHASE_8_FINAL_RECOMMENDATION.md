# Phase 8 final recommendation

- **Tested:** Path B (five-class argmax then 5-to-3 mapping) is a candidate
  only. Its dev accuracy difference 95% CI versus path A includes zero.
- **Tested:** No evaluated path meets 85% accuracy at 30% coverage on dev.
- **Verified:** Path B is not deployed; the deployed scorer remains frozen v2.
- **BLOCKED:** Colab Blocks 59–62 are not yet verified as passed; Stage 1 has
  not received separate approval. Training waits for both conditions.
- **Drafted:** LR/epoch values are resolved in E4, pending approval.
- **Proposed:** If prerequisites or gates fail, fall back to frozen v2.
- **Verified:** Dev results are optimistic; existing test results are
  exploratory. No locked-test result is claimed.
