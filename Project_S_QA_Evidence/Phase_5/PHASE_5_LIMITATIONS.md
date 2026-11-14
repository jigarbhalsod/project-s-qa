# Phase 5 Limitations

Evidence labels: **verified locally** means present in inspected project/archive files; **user-reported** means supplied by Jigar; **not verified** means the available files do not establish the claim or its execution provenance.

## Data and population
- **Verified locally:** the evaluation pipeline uses public English science-answer datasets SciEntsBank and Beetle. The CBSE-style CSV contains draft demo questions and is not a validated evaluation set.
- There is no validated CBSE, NCERT, or Indian schoolchildren evaluation. Demo questions do not establish curriculum validity.
- No pilot student-answer validation has been conducted; there is no evidence here for real classroom performance.

## Generalization and evaluation
- **Verified in archived evaluation files:** dev overall QWK is 0.432 (95% CI 0.358-0.509), and five-class macro-F1 is 0.579. Dev is optimistic because model selection and policy decisions use dev data.
- Seen-answer QWK is 0.630; unseen-question QWK is 0.317 (95% CI 0.199-0.412) over 27 questions. The gap indicates weaker generalization to unseen questions.
- **Verified in archived policy/output:** grouped-CV estimate is 74.77% accuracy at 31.33% coverage. It is an estimate, not test performance.
- **Verified in archived test report:** test QWK is 0.454 (95% CI 0.392-0.515), macro-F1 is 0.576 (0.543-0.606), 3-way accuracy is 0.588, coverage is 0.288, and auto-scored accuracy is 0.790 (0.747-0.834). The test sets were seen in v1, so every test result is exploratory, not an unbiased final estimate.
- The required 85% accuracy at 30% coverage target was NOT achieved. Improving performance is future model-development work, outside documentation.

## Negation, contradiction and unrelated answers
- **Recorded by Block 51 in the notebook:** exact negation performance is 3/12 and all 12 controls were flagged for teacher review.
- **User-reported, not locally verified:** Block 61's separate diagnostic said the fine-tuned component predicted `correct` on 12/12, while NLI predicted `contradictory` with probabilities around 0.507. The local Block 61 output is absent. These results describe different diagnostics and must not be combined or presented as held-out validation.
- **Verified in saved diagnostic output:** the NLI evidence panel assigned entailment from 0.87 to 0.96 on three of four unrelated examples. That evidence is weak for explaining off-topic answers; unrelated-answer failure modes remain.
- The final saved review policy uses a confidence threshold of 0.64 and disables its separate NLI contradiction flag. A missing policy may trigger a provisional fallback, changing review behavior.

## Demo and parity
- Block 45's saved output and Jigar's report state 15/15 reference-case parity, predictions/review flags matching and confidence differences within 0.001. This checks consistency between the demo and scorer on those fixed cases; it does not measure accuracy or generalization.
- The adult voice demo uses Whisper-small. Voice transcription/scoring behavior and microphone availability were not independently validated here. No child recordings or child-assessment claims are supported.

## Reproducibility and provenance
- A_predict and the reference JSON hashes match locally; the reference scorer mode is pooled. Local staged artifacts match their staging manifest. This does not prove cloud synchronization.
- The current working notebook is valid and contains saved outputs for some cells, but relevant execution counts are null. No separate executed notebook was located; Blocks 59-62 have no saved local outputs. Colab execution details for these cells remain user-reported or unverified.
- The archived run manifest records package versions, but no pinned requirements file exists. These recorded versions are not a guarantee of the current runtime.
- The 30 Oct full-run/reproduction statement is retained as reported; current local evidence does not authenticate that execution.
