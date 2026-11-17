# G1 — Multi-agent notebook selection review

**Verdict: BLOCKED BY MISSING EVIDENCE.** Best local reference candidate:
the D snapshot at `drive_backup_20261107/notebooks/`, SHA-256
`37170A8B10DD590C300198BB45A5543B829D4A723443D2268E49A2375A8876C5`.
This is a recommendation for the local source baseline only, not a selection
of an authoritative notebook and not proof of live Drive identity.

## Recomputed local identities

| Candidate | Bytes | SHA-256 | Cells* | Finding |
|---|---:|---|---:|---|
| Working COPY | 2,690,082 | `5EB5DC4FD1AD85DCE55C9B1222603FC11DE19D51BB682103FC7923BC78B5FAF0` | 167 | Local working copy; source differences recorded in earlier report |
| Updated local | 3,642,032 | `F2E2A4A5FDD7BEAA208A192F6101EC9CB40789400B0D823003554FB1F4AABD4D` | 169 | Prior static report says source matches D |
| D dated snapshot | 2,471,126 | `37170A8B10DD590C300198BB45A5543B829D4A723443D2268E49A2375A8876C5` | 169 | Strongest local source reference; not live Drive |
| Phase 2 executed copy | 3,389,226 | `EBB83C058F58CF724153BB897BBDB0854E5A390FBB9EB5BF0A29E885042CC787` | 169 | Prior report records unapproved source changes at cell 157 and extra cells 167–168 |

Hashes were recomputed on 2026-11-16. Cell counts and source-difference facts
are carried forward from `PHASE0_FINAL_CLOSURE_REPORT.md` and earlier static
reviews; this review did not reparse notebook JSON or inspect saved outputs.
Execution-count metadata does not prove which runtime artifacts were loaded
or that a run completed successfully.

## Independent reviews

| Reviewer | Finding |
|---|---|
| Notebook forensics specialist | D is the best local reference candidate; updated local source was previously reported identical to D. Executed copy differs at cell 157; its extra policy check is an unapproved source delta. No candidate is proven live or authoritative. |
| Systems architect | No operationally coherent live combination is verified. Notebook/scorer root is a source-coded candidate only; the expected root policy is absent. |
| Data/configuration auditor | Notebook choice cannot repair the root/policy ambiguity; current local hashes identify files but not authority. |
| ML reproducibility scientist | No authoritative notebook. Hub model revisions and environment versions are unpinned/unverified; execution counts do not establish reproducibility. |
| Adversarial evaluator | D and updated-local source comparison is historical, not freshly re-parsed here. Do not treat saved execution metadata as artifact provenance. |

## CDO assessment

D is preferred over the other local files only as the reference source for a
future decision: the previous audit identifies it as the D baseline, and its
source was reported identical to the updated local file. The working COPY is
167 cells and has documented source differences; the executed copy has an
unapproved cell-157 patch plus two extra cells. D still lacks live Drive
verification and an approved runtime-root decision. A local candidate must
not be called the Colab notebook.

**Required user decision:** approve or reject the exact notebook path/hash and
runtime root. Then perform G3 preflight in Colab. No notebook is selected by
this report.

*Cell counts above are prior-report evidence, not freshly recomputed here.
