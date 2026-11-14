# Phase 3 reference/demo cases

**Verified source:** Phase 2 run-copy cells 157 and 163 read
`A_demo_reference_outputs_v2.json`; cell 163 iterates its `cases`. Cases
c06-c10 below are from that JSON. `expected` is the stored output label,
not gold truth and not an expected Block 60 result.

| Case | Question | Reference answer | Student answer to enter | Expected (JSON only) |
|---|---|---|---|---|
| c06 | What do plants need to make their food? | Plants need sunlight, water and carbon dioxide to make food. | To make food a plant uses light from the sun, water, and carbon dioxide from the air. | correct |
| c07 | What do plants need to make their food? | Plants need sunlight, water and carbon dioxide to make food. | Plants need sunlight. | correct |
| c08 | What do plants need to make their food? | Plants need sunlight, water and carbon dioxide to make food. | Plants do not need sunlight to make food. | correct |
| c09 | What do plants need to make their food? | Plants need sunlight, water and carbon dioxide to make food. | I like to eat vegetables at lunch. | incorrect |
| c10 | What do plants need to make their food? | Plants need sunlight, water and carbon dioxide to make food. | Plants need sunlite, watter and carbon dioxide to make food. | correct |

**Verified compatibility note:** Block 60's dropdown fills its reference from
`cbse_demo_questions_v1.csv`. For this question the CSV reference is
"Plants need sunlight to make food. They also need water and carbon dioxide."
It differs from the JSON reference above. Do not edit the reference box or
use these JSON expected labels to judge Block 60. These exact cases are for
the fresh-runtime check; the five interactive CSV outputs have no stated
expected labels.

**Drafted voice schedule:** Use the student-answer sentences above in this
order, with an adult voice: slow c06-c09; fast c10, c06, c07; noisy c08-c10.
Use the plants dropdown item for each recording and leave its reference
unchanged. Voice scores are demo observations only.
