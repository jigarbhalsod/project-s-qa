# Project S — Phase 3 Test Report

Date: 6 Nov 2026
Status: PARTIAL — live demo tests and evidence collection are blocked.

## 1. Environment and hardware

- Jigar reports a Tesla T4 runtime. Not independently verified in this review.
- Jigar reports Block 59 latency of 146.2 ms for one answer and 214.6 ms for batch 15. These values are user-reported; this local notebook has no saved output or execution count for cell 157.
- Block 62 is reported complete, but its per-stage values were not provided. Cell 163 has no saved output or execution count locally.

## 2. Test cases and actual outputs

| Case | Status | Result/evidence |
|---|---|---|
| Correct answer | User-reported; not independently verified | Typed test returned correct (2/2), confidence 0.756. Exact input and screenshot not supplied. |
| Partially correct | Not tested in this review | No app access or saved result. |
| Incorrect | Not tested in this review | No app access or saved result. |
| Contradictory | Not tested in this review | No app access or saved result. |
| Off-topic | Not tested in this review | No app access or saved result. |

No demonstration case is an accuracy or validation estimate.

## 3. Voice testing

- Not tested. No active Gradio tab or share URL was available; no adult recording was supplied.
- Microphone permission, transcription quality, and voice scoring remain unverified.
- No child voices were used; no child-assessment claim is made.

## 4. Demo availability

- Jigar reports that Block 60 launched Gradio and produced a temporary URL.
- The URL was not available in the local notebook or current browser tab. Link activity and scoring-button behavior could not be rechecked.

## 5. Known failure: negation

- Jigar reports 12 Block 61 negation diagnostics: the fine-tuned component predicted correct on all 12, while NLI predicted contradictory at probabilities around 0.507.
- This is user-reported and not independently verified here; local cell 161 has no saved output or execution count.
- This indicates a component-level negation weakness in these examples. It does not establish overall scorer accuracy.

## 6. Evidence filenames

- `PHASE_3_TEST_REPORT.md` — this report.
- No screenshots, Block 59–62 output exports, voice recordings, transcripts, or failure captures were available to preserve. None were fabricated.

## 7. Limitations and unresolved issues

- The local 167-cell notebook and Desktop copy have no saved outputs for cells 157, 159, 161, or 163.
- Block 60 demo results and all voice behavior need to be captured from a live session.
- The 12 negation controls are diagnostic examples, not a held-out evaluation. Do not claim CBSE validation or child assessment accuracy.

## Next actions

1. Open the current Gradio share URL in Colab; if expired, run only Block 60 after confirming prerequisites.
2. Test the five typed answer types and save one screenshot per visible result, including exact inputs.
3. With consenting adults only, record up to 10 varied-speed/condition samples. Compare each transcript with the intended words before scoring; save transcript and score evidence separately.
4. Export Block 59, 61, and 62 outputs and save a separate executed notebook copy. Keep the original notebook and backups unchanged.