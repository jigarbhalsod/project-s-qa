# Dev-only component export procedure

**Inputs:** `evidence/export_trial/inputs/dev_text_2049.parquet` and
`evidence/export_trial/inputs/A_deployed_dev_probs_v2.parquet`. The dev-text
copy's SHA-256 was verified as
`21e7305557825b392a297fc4558b73e1161fcefb07d82c9f802e33c877836ea2`.
The dev probability file is the packaged saved dev artifact. Do not substitute
any `A_test_*`, `A_table_test_*`, or unified mixed-split file.

The script `src/validation/x0_export_component_probs_v7.py` is a draft from
the existing Phase 8 work. Static inspection shows it accepts the dev-text,
dev-probs, scorer directory, project root, output path and limit arguments.
It imports the frozen scorer, validates UID/label/split alignment, scores in
chunks and writes only outside `reports_v2`. It was not executed by Codex.

The local 2,049-row component output and its validation report are copied to
`evidence/export_trial/outputs/` and `evidence/export_trial/`. The saved report
documents matching Path A/B counts and the full export. A separate 16-row
trial result was not found in the inspected Phase 8 directory; do not claim it
ran.

For any future user-run trial, choose a new temporary output outside the Drive
project and outside `reports_v2`. Use `--limit 16` first. On any hash, schema,
UID or parity failure, stop and preserve the full error; do not run the full
export. Only after manual approval and a clean trial should Jigar choose a new
full-run output path. Keep all outputs explicitly labelled
`dev-only, optimistic`; no test split is to be used.
