# Known limitations and unresolved risks

- **Data scope:** the trained/evaluated scorer is based on SciEntsBank and
  Beetle. CBSE demo questions are drafts only. No Indian schoolchildren or
  CBSE answer accuracy validation is established.
- **Question context:** only DistilRoBERTa receives the question text.
  SBERT-LR and NLI-LR use reference/student answer features. A semantically
  similar but wrong or off-question answer can still be predicted Correct.
- **Rubrics:** deployed `A_predict.py` does not read rubrics or concept lists.
  The handover bank is a separate draft asset; Block 64 displays the rubric but
  does not alter scoring.
- **Partial score:** Partial comes from the model's class probabilities; no
  concept-count or completeness rule is applied in the deployed path.
- **Review:** confidence uses the highest 3-class probability. The packaged
  policy threshold is 0.64 and its contradiction flag is false. A missing
  policy triggers an A_predict fallback with a different threshold and the
  contradiction flag defaults on. The root-level local policy is absent; live
  Drive behavior is unverified.
- **Generalization:** prior project reports describe weaker unseen-question
  performance. These are development estimates and are optimistic. Do not
  describe them as independent confirmation.
- **Accuracy target:** 85% accuracy at 30% coverage was not met in the saved
  project record. This handover adds no accuracy improvement.
- **Question bank:** 12 existing Science records are copied as drafts. Their
  source has no chapter mapping or reviewed required concepts. No new
  Math/Social Science/EVS bank was generated; the 240-question target is open.
- **Pilot:** no labelled student-answer pilot was established in the files
  reviewed for this handover. Do not claim child-assessment accuracy.
- **Execution history:** earlier user reports describe Colab runs. This task
  did not independently run or reproduce them. The saved notebook copy's
  outputs are not a fresh-run guarantee.
- **Notebook ambiguity:** D and the executed run copy are both 169 cells.
  Source-only comparison found cell 157 differs by the Drive-mount wrapper and
  policy-hash check. Jigar must select the submission base.
- **Checkpoint access:** weights are not included in this handover; current
  Drive synchronization and model-cache availability are unverified.
- **Environment:** recorded package versions are historical snapshot values,
  not a clean reproducible lockfile. PDF ingestion and semantic deduplication
  are deferred.
