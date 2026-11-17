# Ingestion architecture

**Status: Drafted design only. No real data was ingested or modified.**

1. Register source/custodian, source ID/path, permission evidence where
   applicable, author, receipt date, and source version.
2. Preserve an immutable raw snapshot and hash, separate from normalized
   records; never overwrite a previous snapshot.
3. Map source identifiers to stable passage/question/rubric IDs using an
   explicit mapping file. Report unmatched and duplicate IDs.
4. Normalize representation only; preserve original text and source fields.
   Record transformation version and lineage.
5. Run structural validation; route failures to review, never serving.
6. Route content to qualified reviewers. Only approved versions enter an
   approved bundle.
7. Export an immutable bundle manifest with hashes, counts, statuses, schema
   version, and source mappings.

Student-answer ingestion is separate and permission-controlled, with
pseudonymous IDs, provenance, label history, and split custody. It is not
authorized or implemented here. Open decisions: storage/access controls,
retention, permissions review, custodians, and publication authority.
