# Schema-only unit-test specification

**Status: Drafted cases; not implemented or executed.** Use small synthetic
schema fixtures only. Tests must not import the deployed scorer, load models,
score answers, or touch production data.

| Case | Expected result |
|---|---|
| Complete draft bundle | Structural pass; no approval implied |
| Missing required field | Fail with record ID and JSON field path |
| Duplicate question ID | Fail and identify both locations |
| Invalid subject | Fail and list allowed enum values |
| Missing question-to-rubric reference | Fail referential-integrity check |
| Rubric points to missing question | Fail reverse reference check |
| Approved rubric missing required concepts | Fail or review-required per approved schema rule; never auto-fill |
| Unknown review status | Fail enum validation |
| Approved status without reviewer evidence | Fail approval-integrity check |
| Unsupported schema version | Fail with migration guidance; no rewrite |
| Missing provenance | Fail or draft warning per owner-approved policy |
| Edit without new version | Fail immutable-history fixture rule |

Tests must be deterministic and must not mutate fixtures. Unit tests cannot
approve educational content. These specifications have not been run.
