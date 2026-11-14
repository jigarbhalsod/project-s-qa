# Checkpoint and model access

No checkpoint weights or credentials are included in this handover.

## Local artifacts observed

These local project files were present and SHA-256 recorded in
`docs/frozen_files_manifest.csv`:

- `project_s_qa/interim/ft_distilroberta_v1/config.json`
- `project_s_qa/interim/ft_distilroberta_v1/model.safetensors`
- `project_s_qa/interim/ft_distilroberta_v1/tokenizer_config.json`
- `project_s_qa/interim/ft_distilroberta_v1/tokenizer.json`
- `project_s_qa/interim/pooled_lr_v2.joblib`
- `project_s_qa/interim/combiner_v1.joblib`

The deployed scorer source also refers to the model identifiers
`cross-encoder/nli-deberta-v3-base` and
`sentence-transformers/all-MiniLM-L6-v2`. Cache availability and live Drive
synchronization were not verified. The `combiner_v1.joblib` is loaded by the
scorer's initialization path; `pooled_lr_v2.joblib` supplies the pooled
SBERT-LR and NLI-LR models.

## Access steps for Jigar

1. Confirm the shared Drive folder and grant Vishwajeet the minimum required
   access using the organization's normal account controls.
2. Do not put tokens, passwords, or private service credentials in this file,
   the notebook, Git, or the handover archive.
3. Confirm the mounted project root contains `interim/` and `reports_v2/`.
4. Compare each downloaded artifact hash with
   `docs/frozen_files_manifest.csv` before use.
5. If a file differs or is absent, stop and report the path; do not replace it
   from an unverified source.

The local hashes do not prove that Google Drive is currently synchronized.
