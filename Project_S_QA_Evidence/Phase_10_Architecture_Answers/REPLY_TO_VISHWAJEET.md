Vishwajeet,

The deployed scorer does not look up a rubric or use a final Logistic Regression combiner. It gives each of three models the answer information it needs, averages their five-way probabilities, then maps the result to Incorrect, Partial, or Correct.

DistilRoBERTa sees the question, reference, and student answer. SBERT and NLI compare the student answer with the reference; neither sees the question. There is no separate check that an answer is on-topic or covers required concepts, so a relevant-sounding but wrong answer can still be labelled Correct. NLI contradiction can request teacher review only when the loaded policy enables that rule; it does not veto the label.

The packaged policy disables that contradiction review rule. The demo imports the scorer from the project-root reports folder, whose local policy file is absent, so the exact Colab policy setting is unverified. Earlier reports of highly contradictory answers still scoring Correct and off-topic answers not being flagged are reported observations, not new tests.

The rubric file contains 251 entries, but the scorer does not read it. Most entries are drafts; the three hand-written entries are also marked unreviewed.
