# Phase 8 decisions

Decision record supplied by Jigar on 9 Nov 2026. Status: **Adopted** (user-
reported decision; not an independently verified project fact).

| Decision | Reason | Owner | What would change it |
|---|---|---|---|
| Stage 1 DeBERTa is future work, outside the submission. Start only after Phase 3 is complete and Jigar says `approved Stage 1`. | The demo, parity and documentation have priority. | Jigar | Phase 3 completion plus explicit Stage 1 approval. |
| Use nested question-grouped CV. The 4,562-row official unseen-domain set is only a possible future holdout if its access history proves it untouched. Status of that history: Unverified; it was not opened. | Keep question groups apart during selection and evaluation; do not make an unsupported locked-test claim. | Jigar | Provenance evidence for an untouched holdout or a newly approved protocol. |
| Jigar manually reviews the 40 rows in `E1_review_sample.csv`; estimate 30-45 minutes. | Preserve human review of uncertain gold labels; do not relabel automatically. | Jigar | Jigar changes the review plan or a reviewer is assigned. |
| Exploratory seed is 42; final candidate seeds are 42, 123, and 2026. Scripts take `--seed`; replace the older 20261106 default. | Make exploratory and final seeds explicit and repeatable. | Jigar | A preregistered seed protocol is approved. |

These decisions authorize documentation and draft preparation only. They do not
authorize training, model loading, checkpoint downloads, notebook runs, Stages
1-3, or a scorer/threshold change.
