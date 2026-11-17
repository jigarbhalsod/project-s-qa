# Gate 2 — JSON and policy integrity

**Status: BLOCKED.** Static local hashes and JSON fields were checked on
15 Nov 2026. No file was changed and no scorer was imported or executed.

| Candidate | SHA-256 | Key evidence | Runtime status |
|---|---|---|---|
| Root A_demo_reference_outputs_v2.json | C99B7D84D000046C9629708D5EE440D5A20AB28FD298F63708E2E8C13F89DC92 | pooled; scorer hash matches local A_predict; declares policy hash BABF76F460D2A6516D9EF11D317F69CEDDB0958DD67A2CE06D3B67496163AD25 | Matching bytes found in Phase_0 scratch, not expected root path |
| Packaged A_demo_reference_outputs_v2.json | EA5288E9F12B25D28A66F36EC38D48B08C65E19452BF3B5EFA17EED2BE20AEB9 | pooled; scorer hash matches local A_predict; declares B6548E... | Local package copy only |
| Packaged A_abstain_policy_v2.json | B6548EDEB682EABD2BA6B74D9B9B67BFF293C1FEA9C3CB6345E0A7EBF7E9EF9B | paired hash matches packaged JSON; threshold 0.64; temperature about 1; contradiction flag false | Local package copy only |

The root JSON's policy hash is explained by
Project_S_QA_Evidence/Phase_0/scratch/policy_compare_20261107_160707/staged_policy.json;
the file is not at the scorer's expected root path. This resolves local
content lookup, not operational placement or deployment choice. The scorer
source at project_s_qa/reports_v2/A_predict.py reads
A_abstain_policy_v2.json under its configured reports_v2 directory. Static
source lines 139–141 record a provisional fallback if the policy is absent;
line 16 gives its confidence threshold as 0.60. Therefore a missing policy can
change review behavior. The expected root policy path is absent locally.

**Needed to pass:** Jigar selects one exact JSON/policy pair, approves both
hashes and their runtime paths, and the selected policy is present at the path
the scorer reads. Do not copy or replace files until separately approved.
