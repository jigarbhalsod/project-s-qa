# G2 — Multi-agent JSON and policy selection review

**Verdict: BLOCKED BY MISSING EVIDENCE.** Best local integrity candidate:
the packaged JSON/policy pair below. This does not make it the canonical or
live pair. Do not stage or combine files without Jigar's separate approval.

## Hash and configuration evidence

| Item | Local path | SHA-256 | Relevant declared/configured value |
|---|---|---|---|
| Root scorer | `project_s_qa/reports_v2/A_predict.py` | `CA7C2752A4863F2A24B20EC7CD9000B651D83A0CFC39709F0080EBCBDAD0A053` | Same scorer hash is declared by both JSON candidates |
| Root JSON | `project_s_qa/reports_v2/A_demo_reference_outputs_v2.json` | `C99B7D84D000046C9629708D5EE440D5A20AB28FD298F63708E2E8C13F89DC92` | pooled; declares policy hash `BABF76F460D2A6516D9EF11D317F69CEDDB0958DD67A2CE06D3B67496163AD25` |
| Scratch policy bytes | `Project_S_QA_Evidence/Phase_0/scratch/policy_compare_20261107_160707/staged_policy.json` | `BABF76F460D2A6516D9EF11D317F69CEDDB0958DD67A2CE06D3B67496163AD25` | Matches root JSON declaration; not at active policy filename/path |
| Packaged JSON | `project_s_qa/A_submission_v2/reports_v2/A_demo_reference_outputs_v2.json` | `EA5288E9F12B25D28A66F36EC38D48B08C65E19452BF3B5EFA17EED2BE20AEB9` | pooled; declares packaged policy hash |
| Packaged policy | `project_s_qa/A_submission_v2/reports_v2/A_abstain_policy_v2.json` | `B6548EDEB682EABD2BA6B74D9B9B67BFF293C1FEA9C3CB6345E0A7EBF7E9EF9B` | pooled; threshold 0.64; temperature 1.0000000000000004; contradiction flag false |

The packaged JSON/policy declared hashes match the files and scorer hash.
The root JSON's policy hash also matches a local scratch file. Hashes were
recomputed on 2026-11-16; live Drive was not accessed.

## Runtime compatibility and fallback

Static source review of `A_predict.py`:

- Lines 8–9 derive `ROOT`, `INTERIM`, and `V2`; default root is
  `/content/drive/MyDrive/project_s_qa` and `PROJECT_S_ROOT` can override it.
- Lines 11–12, 23–35, and 106 identify the local DistilRoBERTa/joblib paths
  and Hub-loaded NLI/SBERT components.
- Lines 139–141 load `V2/A_abstain_policy_v2.json` or use the provisional
  policy; lines 16–17 set its fallback threshold to 0.60.

The top-level local `project_s_qa/` has the required `interim/` files but no
`reports_v2/A_abstain_policy_v2.json`. The nested
`project_s_qa/A_submission_v2/` has JSON and policy but no `interim/` directory.
Therefore neither existing root is a complete operational runtime as-is.
The packaged pair is hash-compatible with the local scorer bytes, but using it
with the top-level model root requires an approved placement decision. No
runtime pair was staged, and no Colab execution was performed.

## Independent reviews and verdict

The configuration auditor, systems architect, ML reproducibility scientist,
and adversarial evaluator agree: the packaged pair is the strongest local
integrity candidate, but there is **no defensible canonical/live selection**.
The root pair is content-hash explainable via scratch but operationally
misplaced; the packaged root lacks model artifacts. Hub revisions/cache and
live paths remain unverified.

**Required user decision:** select the exact JSON/policy hashes and intended
runtime paths, and separately authorize any staging. Then run the G3
read-only preflight. This recommendation does not mark D0-4 approved.
