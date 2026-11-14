# Project S Q&A Architecture

## Scope
This diagram covers the implemented Q&A scorer and its Colab demo. It does not imply that the broader reading-assessment branch, child-profile fusion, or a production service is implemented.

## End-to-end data flow

```mermaid
flowchart LR
  D[Public SciEntsBank / Beetle records] --> P[Normalize and create train/dev/test splits]
  P --> T[Train and select components]
  T --> A[Saved inference artifacts]
  U[Question + reference + student answer] --> F[A_predict.predict, dataset pooled]
  A --> F
  F --> C1[DistilRoBERTa 5-way probabilities]
  F --> C2[SBERT features + pooled LR probabilities]
  F --> C3[NLI evidence/features + pooled LR probabilities]
  C1 --> E[Average 5-way probability vectors]
  C2 --> E
  C3 --> E
  E --> O[Map to incorrect / partial / correct]
  O --> Q[Temperature and final policy]
  Q --> R{Confidence below 0.64?}
  R -->|Yes| H[Teacher-review flag and reason]
  R -->|No| S[Automatic score result]
```

## Component interactions

1. **Fine-tuned DistilRoBERTa** reads question/reference context with the student answer and returns probabilities in the five-label order documented in the notebook.
2. **SBERT + Logistic Regression** uses embedding-derived reference/answer features. In deployed pooled mode, the logistic-regression artifact comes from `pooled_lr_v2.joblib`.
3. **NLI + Logistic Regression** uses DeBERTa NLI outputs for concept-level and answer-pair evidence. Aggregated NLI features feed the pooled logistic-regression component.
4. `A_predict.component_probs` produces component probabilities. `predict_batch` averages the three component vectors, maps them into the three-level score space, applies the saved temperature, then computes review reasons.

The older `combiner_v1.joblib` is associated with the earlier stacking experiment; it is not an additional deployed probability component. Block 17's LLM experiment is not called by deployed inference.

## Inference and review flow

```mermaid
sequenceDiagram
  participant Client as Caller or Gradio
  participant API as A_predict.predict
  participant FT as DistilRoBERTa
  participant SB as SBERT + pooled LR
  participant NLI as NLI + pooled LR
  participant Policy as Saved review policy
  Client->>API: question, reference_answer, student_answer
  API->>FT: score answer pair
  API->>SB: embedding features
  API->>NLI: concept and answer-pair evidence
  FT-->>API: 5-way probability vector
  SB-->>API: 5-way probability vector
  NLI-->>API: 5-way probability vector + evidence
  API->>API: average vectors, map to ordinal 3-way
  API->>Policy: temperature and review threshold
  Policy-->>API: score, confidence, review flag/reasons
  API-->>Client: result dictionary
```

The `confidence` field is the maximum post-temperature probability across the three ordinal classes. It is not a correctness guarantee. The archived final policy has threshold 0.64 and disables the separate contradiction flag; missing policy can cause A_predict to use its provisional fallback.

## Demo architecture

```mermaid
flowchart TD
  Q[CSV question bank] --> UI[Gradio dropdown]
  T[Typed response] --> UI
  V[Adult voice demo input] --> W[Whisper-small ASR]
  W --> UI
  UI --> API[A_predict pooled scorer]
  API --> OUT[Predicted score, confidence, review flag]
```

Block 60 reads `processed/cbse_demo_questions_v1.csv` and requires `question_id`, `question_text`, and `reference_answer`. Voice transcription is a demo path, not evidence of child-voice performance. Gradio share URLs are temporary; no permanent deployment is verified.

## Artifact boundaries
- Scorer/reference pair: `reports_v2/A_predict.py`, `reports_v2/A_demo_reference_outputs_v2.json`.
- Fine-tuned weights/tokenizer: `interim/ft_distilroberta_v1/`.
- Logistic regressors: `interim/pooled_lr_v2.joblib`, plus the legacy `interim/combiner_v1.joblib` for its earlier experiment.
- Final deployed mode and review behavior: `reports_v2/A_deployed_scorer_v2.json`, `reports_v2/A_abstain_policy_v2.json`.
- CBSE demo input: `processed/cbse_demo_questions_v1.csv`.

Local Phase 4 evidence confirms the scorer hash matches the reference JSON and staged artifact hashes match the local staging manifest. Local filesystem evidence does not establish cloud synchronization.
