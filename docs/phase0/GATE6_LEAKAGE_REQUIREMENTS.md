# Gate 6 — Leakage requirements

Status: required controls, not a completed audit of all source records.

- Assign complete question groups before answer-level expansion; no question
  crosses train, development, and confirmation partitions.
- Define child-level and passage-level separation explicitly; do not infer
  either from question grouping.
- Preserve UID provenance, label version, source, and split assignment.
- Verify model-fit inputs and artifact lineage; unresolved fit provenance
  prevents a claim that leakage is absent.
- Use development only for architecture, checkpoint, calibration, and
  threshold selection. Keep the 0.64 deployed threshold unchanged here.
- Keep prior exposed test data exploratory; do not relabel it as a clean
  confirmation set.
- Freeze code, policy, model, data manifest, and analysis before opening any
  independent confirmation labels.

No new split, data, model, or evaluation was created in this audit.
