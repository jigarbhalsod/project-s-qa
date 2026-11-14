# Project S Phase 4: Parity Verification and Freeze

## Status: PASS WITH LIMITATIONS
The local technical integrity checks pass. The Colab run is supported by user-provided results and saved output text, but no separate executed notebook or cloud sync is independently authenticated.

## Notebook and execution evidence
- Working notebook: `notebooks/Jigar_Q&A_Branch_Baseline_COPY.ipynb`; valid JSON, 167 cells; SHA-256 `a35efc489c25806f2ad3db8684006dc2d627634dc1e6d2a61d3fbc75c615030e`.
- Block 45 parity: code cell 118; saved output says `DEMO PARITY: PASS (15/15 cases, tolerance 0.001)`. Predictions and review flags match; confidence differences are within 0.001. User also supplied these Colab results.
- Block 58: code cell 155; saved output shows metrics and intervals, parity PASS, and `Zipped 54 files`. User reports 15 demo outputs saved, five-case CSV generated, and NLI diagnostics executed. Archive contents confirm 15 demo output rows and five diagnostic data rows.
- Saved outputs exist in the working notebook, but execution_count is null for cells 118/155. No separate executed notebook was found. Run provenance remains NOT VERIFIED.

## Metrics and limitations (from saved outputs / user report)
- Dev overall: QWK 0.432 (95% CI 0.358-0.509); macro-F1 0.579 (0.523-0.629).
- Dev seen: QWK 0.630 (0.562-0.692); macro-F1 0.730 (0.689-0.766).
- Dev unseen: QWK 0.317 (0.199-0.412); macro-F1 0.490 (0.406-0.544), 27 questions.
- Exploratory test: QWK 0.454 (0.392-0.515); macro-F1 0.576 (0.543-0.606); 3-way accuracy 0.588; coverage 0.288; auto-scored accuracy 0.790 (0.747-0.834).
- The 85% accuracy at 30% coverage target was NOT met. Grouped-CV estimate: 74.77% accuracy at 31.33% coverage.
- Test results are exploratory because test sets were seen in v1. No claim of CBSE or Indian schoolchildren validation. Negation and unrelated-answer weaknesses remain documented.

## Artifact and hash checks
- `A_predict.py`: `ca7c2752a4863f2a24b20ec7cd9000b651d83a0cfc39709f0080ebcbdad0a053`. Reference JSON: `c99b7d84d000046c9629708d5ee440d5a20ab28fd298f63708e2e8c13f89dc92`; scorer mode `pooled`; stored scorer hash matches.
- Static scorer check: default dataset is pooled and the pooled model loads from `interim/pooled_lr_v2.joblib`.
- All eight staged runtime artifacts match `A_runtime_stage_manifest_v2.json` in local size and SHA-256; see the freeze manifest for per-file hashes. This does not verify cloud presence.
- ZIP integrity, extracted comparison, and embedded submission manifest all PASS; see `PHASE_4_ARCHIVE_VERIFICATION.md`.
- Existing notebook backups are preserved; paths, cell counts and hashes are listed in the freeze manifest.

## Remaining unverified items
- No separate Colab-executed notebook was found; current saved outputs have null execution counts.
- Google Drive/OneDrive synchronization status is not verified.
- Execution provenance and cloud copy of the archive are not verified.

## Colab cells
Block 45 parity: cell 118. Block 58 freeze/package: cell 155. Do not use Run All.
