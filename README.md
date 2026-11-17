# Reading Skills Profile Generation of Children

An ML-based framework for analyzing children's reading and comprehension skills through speech-based reading assessment and automated evaluation of question-answer responses.

**Repository:** [jigarbhalsod/project-s-qa](https://github.com/jigarbhalsod/project-s-qa)

---

## 1. Overview

Reading Skills Profile Generation of Children explores how machine learning and natural language processing can support the assessment of children's reading and comprehension abilities.

The framework is organized around two complementary assessment directions:

1. **Oral Reading and Speech Assessment** — analyzing children's spoken reading to investigate reading-related characteristics through acoustic, phonetic, and linguistic information.
2. **Reading Comprehension and Answer Assessment** — evaluating student responses to questions using reference answers, semantic representations, and natural language inference.

The broader objective is to move beyond a single correctness score and investigate how multiple signals can contribute to a more informative reading skills profile.

The repository contains research materials, notebooks, model artifacts, evaluation outputs, prototype implementations, documentation, and experiment records.

> **Project status:** Research and development. The repository contains working components and experimental evidence, but the complete assessment framework has not yet been independently validated as a production-ready system.

---

## 2. Project Objectives

The main objectives are:

- Investigate machine learning approaches for assessing children's oral reading.
- Explore acoustic, phonetic, and linguistic representations of speech.
- Develop automated methods for evaluating student answers.
- Investigate semantic similarity and natural language inference for answer assessment.
- Explore confidence estimation and selective prediction.
- Study model performance on previously encountered and unseen questions.
- Establish reproducible evaluation procedures.
- Investigate how reading and comprehension signals could contribute to a structured reading skills profile.

---

## 3. System Components

### 3.1 Oral Reading and Speech Assessment

This component focuses on analyzing children's spoken reading.

The research direction includes:

- Speech preprocessing and transcription.
- Acoustic feature extraction.
- Phonetic and linguistic feature analysis.
- Speech representation learning.
- Investigation of reading-related characteristics from recorded utterances.

Models and technologies explored include:

- wav2vec 2.0
- HuBERT
- WavLM
- Whisper
- Parakeet
- Python-based audio processing and machine learning tools

The NNCES corpus is an important dataset considered in this research direction. The project materials describe a collection involving 50 children aged 8–12, native Telugu speakers learning English, with approximately 20 hours of recordings and 5,000 read and 5,000 spontaneous utterances.

**Current limitations:**

- The ten passage texts and their audio mappings require recovery and verification.
- Human-verified fluency ratings are not established as a complete training target.
- Speaker-independent evaluation is important because the dataset contains a relatively small number of speakers.
- The age-group classification experiment must not be interpreted as validated reading-assessment performance.

### 3.2 Reading Comprehension and Answer Assessment

This component investigates automated evaluation of student answers against reference answers.

The current scoring research uses a combination of:

- Fine-tuned DistilRoBERTa representations.
- Sentence-BERT semantic features.
- Natural Language Inference (NLI) features.
- Probability aggregation.
- Confidence estimation and review flags.

The five-class internal label space distinguishes:

- Correct
- Partially correct
- Contradictory
- Irrelevant
- Non-domain

These are mapped into three user-facing categories:

| Internal categories | User-facing category |
|---|---|
| Correct | Correct |
| Partially correct | Partially Correct |
| Contradictory, irrelevant, non-domain | Incorrect |

The three-class mapping is used for the reported answer-assessment metrics. Five-class and three-class metrics must be kept distinct when interpreting experimental results.

**Important limitation:** The current scorer does not establish rubric-aware scoring. It does not load an approved question-specific rubric or use a question ID during inference. Planned rubric retrieval, concept coverage, and separate relevance checks should not be considered completed functionality.

### 3.3 Confidence and Selective Prediction

The answer-assessment research also investigates whether the system can identify uncertain predictions for human review.

This includes:

- Prediction confidence.
- Review flags.
- Contradiction-related evidence.
- Risk-coverage analysis.
- Threshold-based selective prediction.
- Calibration and uncertainty analysis.

Selective accuracy must always be reported alongside coverage. A high accuracy value at very low coverage does not mean the system accurately evaluates most student answers.

---

## 4. High-Level Architecture

The conceptual assessment workflow is:

```text
                  Student Input
                       |
          +------------+------------+
          |                         |
     Spoken Reading             Question Answer
          |                         |
    Audio Processing           Text Processing
          |                         |
    Speech Features           Text Representations
          |                         |
    Speech Models          +--------+--------+
          |                |        |        |
   Reading Analysis     DistilRoBERTa SBERT   NLI
          |                |        |        |
          |                +--------+--------+
          |                         |
          |                Probability Aggregation
          |                         |
          |                Prediction & Confidence
          |                         |
          |                Review / Uncertainty
          |                         |
          +------------+------------+
                       |
             Reading Skills Research
                       |
             Profile Generation
              (Research Direction)
```

This diagram represents the broader research direction. It should not be interpreted as proof that every component is integrated into one operational application.

---

## 5. Technology Stack

The repository explores technologies across machine learning, NLP, speech processing, and experimentation.

| Area | Technologies |
|---|---|
| Programming | Python |
| Data processing | NumPy, Pandas |
| Machine learning | Scikit-learn |
| Deep learning | PyTorch |
| NLP | Hugging Face Transformers |
| Text representations | Sentence-BERT |
| Language inference | DeBERTa-based NLI models |
| Speech processing | wav2vec 2.0, HuBERT, WavLM, Whisper |
| Model artifacts | Joblib, Hugging Face model artifacts |
| Experimentation | Jupyter Notebook, Google Colab |
| Data formats | CSV, JSON, Parquet, XLSX |
| Version control | Git, GitHub |

The repository contains multiple experimental environments and historical dependency records. A fully pinned, clean-install environment has not yet been verified.

---

## 6. Repository Structure

The repository contains active working materials, research evidence, historical snapshots, and prototype implementations.

```text
.
├── AGENTS.md
├── PROJECT_CONTEXT.md
├── README.md
├── README_FILES.txt
│
├── notebooks/
│   ├── Working notebooks
│   ├── Updated notebook candidates
│   ├── Reference notebooks
│   └── Backups
│
├── project_s_qa/
│   ├── reports_v2/
│   │   └── A_predict.py
│   ├── interim/
│   │   ├── Model artifacts
│   │   └── Serialized components
│   ├── processed/
│   │   └── Demo question data
│   └── A_submission_v2/
│       ├── demo/
│       └── reports_v2/
│
├── block60/
│   ├── Standalone demo source
│   └── Demo question data
│
├── PROJECT_S_QA_HANDOVER/
│   ├── src/
│   ├── question_bank/
│   ├── tests/
│   └── Documentation
│
├── Project_S_QA_Evidence/
│   ├── Phase reports
│   ├── Evaluation evidence
│   └── Experiment records
│
├── drive_backup_20261107/
│   └── Historical local snapshot
│
├── project_s_qa_backup_20261106_1957/
│
├── _backups/
│
├── archive/
│
├── tools/
│   ├── extracted_A_predict.py
│   └── comparison_table.json
│
├── docs/
│   ├── REPOSITORY_AUDIT.md
│   ├── SOURCE_OF_TRUTH.md
│   ├── IMPLEMENTATION_GAP_ANALYSIS.md
│   ├── FILE_CHANGE_PLAN.md
│   ├── PHASE0_FINAL_CLOSURE_REPORT.md
│   ├── phase0/
│   └── phase1/
│
└── research/
    └── manuscript/
        └── manuscript_draft.txt
```

*Note: This is a functional overview, not an exhaustive listing of every file. Some directories contain historical snapshots, duplicate artifacts, or experimental materials.*

### Important directory descriptions

| Directory | Purpose |
|---|---|
| `notebooks/` | Development notebooks, working copies, reference versions, and backups. |
| `project_s_qa/` | Local runtime-shaped implementation, model artifacts, scoring code, and submission materials. |
| `block60/` | Standalone demonstration source and associated demo data. |
| `PROJECT_S_QA_HANDOVER/` | Question-bank utilities, ingestion and validation prototypes, draft tests, and handover documentation. |
| `Project_S_QA_Evidence/` | Experiment reports, saved evaluation evidence, and historical analyses. |
| `docs/` | Repository audits, source-of-truth documentation, implementation gaps, and phase reports. |
| `research/` | Research manuscript materials. |
| `tools/` | Supporting scripts and historical extracted utilities. |
| `archive/`, `_backups/` | Historical files and snapshots. |

---

## 7. Answer Assessment: Implementation Details

The local operational scorer is:

```text
project_s_qa/reports_v2/A_predict.py
```

The scorer combines three sources of model evidence.

### Component 1: Fine-tuned DistilRoBERTa

- Receives the question and reference answer alongside the student answer.
- Produces five-class prediction probabilities.
- Provides contextual representations for answer evaluation.

### Component 2: Sentence-BERT

- Generates semantic representations of reference and student answers.
- Supplies features to the pooled classification component.
- Helps capture semantic similarity beyond exact lexical matching.

### Component 3: Natural Language Inference

- Evaluates relationships between reference-answer and student-answer text.
- Generates NLI-related evidence and probabilities.
- Provides contradiction-related signals.

### Prediction flow

The local scorer's documented prediction path:

1. Computes the component-level five-class probabilities.
2. Equally averages the three component probability vectors.
3. Collapses the resulting probabilities into three user-facing classes.
4. Applies optional temperature scaling.
5. Selects the predicted class.
6. Derives confidence and review-related information.

The exact policy and runtime configuration must be verified before treating this behavior as the deployed configuration.

### Implementation limitations

The current local scorer:

- Does not load a question-specific rubric during inference.
- Does not use a question ID as an inference input.
- Does not implement a distinct relevance or on-topic gate.
- Does not implement an explicit rubric-based concept-count rule for partial correctness.
- Can fall back to a provisional abstention policy when the expected policy file is missing.

The presence of separate question-bank and rubric prototypes does not mean that they are integrated into the operational scoring path.

---

## 8. Experimental Results

The following are previously reported development-set results for the answer-assessment component. They are included to document the current experimental baseline, not to claim independent validation.

### 8.1 Main Development Results

| Metric | Reported result |
|---|---:|
| Development answers | 2,049 |
| Accuracy | 56.37% |
| Macro-F1 (three-class) | 52.70% |
| Quadratic Weighted Kappa (QWK) | 0.4015 |
| Partial-class recall | 26.34% |

### 8.2 Seen vs. Unseen Questions

| Evaluation subset | Samples | Accuracy |
|---|---:|---:|
| Seen questions | 753 | 69.19% |
| Unseen questions | 1,296 | 48.92% |

The performance difference indicates that generalization to unseen questions remains a major challenge.

### 8.3 Selective Prediction

One previously reported operating point:

| Metric | Result |
|---|---:|
| Selective accuracy | 75.12% |
| Coverage | 30.60% |
| Accepted predictions | 627 |

This result corresponds to a particular threshold-based development evaluation. It does not mean that the system achieves 75.12% accuracy on all student answers.

### 8.4 Evaluation Caveats

- These results are development-set results and are optimistic.
- Historical test-set access has been documented in earlier project work.
- A clean, independent confirmation evaluation has not been established.
- The aggregation path and label mapping must be stated alongside each metric.
- Three-class and five-class Macro-F1 values are not interchangeable.
- Selective accuracy must always be accompanied by its coverage.
- Historical experiment reports have not all been independently reconstructed from raw inputs.

**No claim of 85–90% overall accuracy is supported by the current evidence.**

---

## 9. Research and Documentation

The `docs/` and `research/` directories contain material intended to make the development process auditable.

Important documents include:

| File | Description |
|---|---|
| `docs/REPOSITORY_AUDIT.md` | Inventory and technical audit of the repository. |
| `docs/SOURCE_OF_TRUTH.md` | Documents source-of-truth decisions and unresolved ambiguities. |
| `docs/IMPLEMENTATION_GAP_ANALYSIS.md` | Identifies differences between intended functionality and verified implementation. |
| `docs/FILE_CHANGE_PLAN.md` | Records the planned documentation and repository changes. |
| `docs/PHASE0_FINAL_CLOSURE_REPORT.md` | Phase 0 audit and closure assessment. |
| `docs/phase0/` | Phase 0 evidence and design materials. |
| `docs/phase1/PHASE1_ENTRY_BLOCKERS.md` | Documents outstanding blockers for the next phase. |
| `research/manuscript/manuscript_draft.txt` | Working research manuscript draft. |

The manuscript and research claims should be treated as working material until the evidence, references, and numerical results have been independently verified.

---

## 10. Current Development Status

The repository is in a research and audit stage.

| Area | Current status |
|---|---|
| Repository inventory | Documented |
| Source and notebook audit | Conducted locally; live runtime remains unverified |
| Speech-assessment research | Under development |
| Answer-assessment scorer | Local implementation available |
| Model artifacts | Present locally; complete provenance not established |
| Question-bank utilities | Prototype implementation |
| Rubric-aware scoring | Not integrated into the operational scorer |
| Demo implementation | Prototype materials available |
| Evaluation | Historical development evidence available |
| Independent validation | Not established |
| Research manuscript | Draft; not submission-ready |
| Phase 0 | Open / blocked |
| Phase 1 | Not ready to start |

### Outstanding priorities

1. Establish the authoritative notebook and runtime environment.
2. Resolve the scorer's expected policy-file path and configuration.
3. Identify one canonical question-bank and rubric source.
4. Verify question and rubric content with appropriate reviewers.
5. Establish a defensible evaluation protocol and independent confirmation set.
6. Verify model artifact provenance and dependency versions.
7. Integrate and test rubric-aware scoring before claiming that functionality.
8. Validate the speech-assessment pipeline using appropriate human-verified targets.
9. Reproduce the reported evaluation results from traceable artifacts.

---

## 11. Reproducibility and Usage Notes

This repository contains multiple notebook copies, historical snapshots, and prototype implementations. Not every file is an active entry point.

Before running or modifying anything:

1. Read `AGENTS.md` for repository-specific working rules.
2. Consult the source-of-truth and repository audit documents.
3. Identify the intended notebook and its corresponding runtime files.
4. Verify that required model artifacts and policy files are available.
5. Confirm dependency compatibility.
6. Preserve existing experimental evidence and frozen artifacts.

The repository does not currently establish a verified, clean, one-command installation and execution workflow. The local notebook and scorer paths should not be assumed to match a live Google Colab or Google Drive environment.

### Important

Do not assume that:

- Every notebook is an authoritative version.
- Every model artifact is part of the current inference pipeline.
- A displayed rubric is necessarily used for scoring.
- A saved development metric proves independent generalization.
- A prototype is equivalent to a completed integration.

---

## 12. Research Limitations

The following limitations are important when interpreting the work:

- The available speech corpus has a limited number of speakers.
- Human-verified reading-fluency targets require further verification.
- Unseen-question answer evaluation remains substantially weaker than seen-question evaluation.
- The operational answer scorer does not yet use approved question-specific rubrics.
- Question-bank content requires review before educational use.
- Model revisions and portions of the runtime configuration are not pinned.
- Historical evaluation evidence requires stronger independent reproducibility.
- The complete reading skills profile workflow has not been validated as an integrated system.

These limitations are part of the current research state and should be addressed before making claims about real-world educational effectiveness.

---

## 13. Future Research Directions

Potential future development areas include:

- More robust acoustic and phonetic representations for oral reading.
- Better speech transcription and alignment.
- Human-verified reading-fluency assessment targets.
- Question-specific rubric retrieval and concept-level evidence.
- Stronger semantic and NLI-based answer evaluation.
- Improved handling of partially correct answers.
- Question-grouped and speaker-independent evaluation.
- Better confidence calibration and selective prediction.
- Integration of validated reading and comprehension indicators into a structured student profile.

These are research directions, not claims of completed implementation.

---

## 14. Contribution Guidelines

Contributions should prioritize reproducibility, traceability, and correctness.

Potential areas for contribution:

- Speech preprocessing and feature extraction.
- Question-bank and rubric validation.
- Scoring architecture review.
- Evaluation and statistical analysis.
- Error categorization and qualitative analysis.
- Documentation and reproducibility improvements.

Before submitting changes:

1. Explain the problem being addressed.
2. Identify the affected files and components.
3. Preserve frozen artifacts and historical evidence.
4. Document any changes to evaluation procedures.
5. Include reproducible tests or evidence where applicable.
6. Avoid reporting unsupported performance improvements.

---

## 15. Academic and Research Integrity

This repository is intended for research and development.

All reported results should be traceable to their corresponding datasets, model versions, evaluation procedures, and experiment artifacts.

In particular:

- Do not present development results as independent test results.
- Do not claim validated performance on children without appropriate evaluation evidence.
- Do not describe draft rubrics as teacher-approved.
- Do not report planned features as implemented.
- Do not claim educational effectiveness without suitable validation.

The objective is not simply to maximize a reported metric, but to develop an assessment framework whose outputs are explainable, reproducible, and supported by evidence.

---

## 16. Repository

**GitHub:** [https://github.com/jigarbhalsod/project-s-qa](https://github.com/jigarbhalsod/project-s-qa)

**Project:** Reading Skills Profile Generation of Children

**Focus Areas:** Machine Learning · Natural Language Processing · Speech Processing · Reading Assessment · Semantic Evaluation · Educational AI

---

*Reading Skills Profile Generation of Children — Research and Development Repository.*
