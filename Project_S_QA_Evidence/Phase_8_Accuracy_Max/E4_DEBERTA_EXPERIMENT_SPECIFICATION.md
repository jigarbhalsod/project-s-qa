# E4 DeBERTa experiment specification

**Drafted; execution requires separate approval and successful Colab Blocks
59–62.** This is the single Phase 8 source for planned hyperparameters.

| Setting | Value | Source / status |
|---|---|---|
| Seed | 20261106 | Script line 3; plan file agrees. Notion 8.4 says 42 (Reported); Jigar to align Notion. |
| Learning rate | 2e-5 | Notion 8.4 (Reported); Proposed until approved. |
| Epochs | 3 | Notion 8.4 reports 3-4 (Reported); 3 is Proposed. |
| Warmup ratio | 0.10 | Notion 8.4 (Reported); Proposed until approved. |
| Weight decay | Not set in script | Script line 19; Unverified (library default applies). |
| Max length | 256 | Script lines 3 and 15. |
| Train batch | Per-device 4 x accumulation 4; effective 16 | Script line 19. |
| Eval batch | 8 per device | Script line 19. |
| Precision | fp16; bf16 not selected for T4 | Script line 19; T4/bf16 statement Reported by Jigar; memory safety Unverified. |
| Loss | Cross-entropy | Proposed for three-class classification. |
| Evaluation / saving | Each epoch / each epoch; keep one checkpoint | Script line 19. |
| Best checkpoint | Validation Macro-F1 (`eval_macro_f1`), higher is better | Proposed; implemented by script lines 2 and 19. |
| Checkpoint order | `MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli`; fallback `cross-encoder/nli-deberta-v3-base` | Script line 3; availability Unverified. |
| Input / labels | `[question][reference][answer]`; five labels collapsed to three | Script lines 4, 5, 15; Drafted. |
| Selection split | Existing `dev_uq`; not independent confirmation | Script line 4; Exploratory. |
| Test split | Never read or used for selection | Script line 4; Drafted. |

**Drafted:** Paths and run checklist remain in `PHASE_8_ACCURACY_MAX_PLAN.md`.
**Drafted:** Hyperparameters are resolved in this specification, pending your approval of these values.
