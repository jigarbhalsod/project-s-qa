# Gate 2 — Policy comparison

**Status: BLOCKED.** The local packaged JSON and policy are internally
consistent, but no pair is approved as canonical or verified in live Drive.

| Pair | JSON hash | Declared policy hash | Policy file/hash | Result |
|---|---|---|---|---|
| Root reports_v2 | C99B7D84...F89DC92 | BABF76F4...63AD25 | Exact bytes at Phase_0/scratch/.../staged_policy.json; expected A_abstain_policy_v2.json absent from root reports_v2 | Content hash explained locally; runtime path unverified |
| Handover package | EA5288E9...20AEB9 | B6548EDE...F7E9EF9B | A_abstain_policy_v2.json, B6548EDE...F7E9EF9B | Local pair hash-consistent |

The root JSON's declared hash is explained by staged_policy.json in Phase_0
scratch, but those bytes are not at the scorer's expected path. The policy
files must not be treated as interchangeable: choosing the
packaged policy selects a different declared policy hash and threshold
behavior from the missing root policy. The scorer's missing-policy fallback
is documented in A_predict.py lines 139–141 and must not be mistaken for a
verified deployment policy.

**Decision required:** select root policy recovery, packaged pair, or another
approved configuration process; name exact hashes and destination paths.
This report does not authorize staging.
