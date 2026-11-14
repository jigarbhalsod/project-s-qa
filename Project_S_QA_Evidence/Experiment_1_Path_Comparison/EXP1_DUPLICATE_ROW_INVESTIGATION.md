# Experiment 1 — dev duplicate-row investigation

**Status:** Read-only investigation. No rows were changed, removed, or
overwritten. No model, notebook, or project script was run. No test data was
opened.

## Scope and duplicate definition

**Verified.** The inspected file was
`Project_S_QA_Evidence/Phase_3/dev_text_2049.parquet` (2,049 rows, 2,049 unique
UIDs). A strict duplicate means identical values for `dataset`,
`question_id`, `question`, `reference_answer`, `student_answer`, and `label5`;
UID and split are reported separately. Grouping by these fields found 17
duplicate groups containing 36 rows: 19 rows beyond one representative per
group. No student-identifying fields were requested or reported.

`dev_ua` is treated as seen and `dev_uq` as unseen, consistent with the saved
dev evaluation artifacts. All rows below are dev-only.

## Duplicate groups

Each group lists every UID and the exact shared content. Every listed group is
SciEntsBank, all its UIDs share the same question ID and split, and every
answer in that group has the stated gold label.

### Group 1 — unseen (`dev_uq`), Correct

- UIDs: `scientsbank-train-2939`, `scientsbank-train-2960`
- Dataset / question ID: `scientsbank` / `SCI-0a35647e`
- Question: Grace set up a science experiment. Here's what she wrote in her notebook. First I put eggshells into a cup and covered them with vinegar. After a while, small bubbles appeared on the surface of the eggshells. The next day there were more bubbles. In a couple of days, the eggshells were gone and the liquid was clear. I think I made a solution and a reaction. Explain why Grace thinks she made a reaction.
- Reference answer: A reaction was indicated by the bubbles of gas (a new material) being produced.
- Student answer: Because it bubbled.
- Gold label: `correct`

### Group 2 — unseen (`dev_uq`), Correct

- UIDs: `scientsbank-train-2944`, `scientsbank-train-2948`
- Dataset / question ID: `scientsbank` / `SCI-0a35647e`
- Question: Grace set up a science experiment. Here's what she wrote in her notebook. First I put eggshells into a cup and covered them with vinegar. After a while, small bubbles appeared on the surface of the eggshells. The next day there were more bubbles. In a couple of days, the eggshells were gone and the liquid was clear. I think I made a solution and a reaction. Explain why Grace thinks she made a reaction.
- Reference answer: A reaction was indicated by the bubbles of gas (a new material) being produced.
- Student answer: Because there were gas bubbles.
- Gold label: `correct`

### Group 3 — unseen (`dev_uq`), Irrelevant

- UIDs: `scientsbank-train-3834`, `scientsbank-train-3851`
- Dataset / question ID: `scientsbank` / `SCI-1302429c`
- Question: Why does the tree shown in the picture have a shadow?
- Reference answer: The tree blocks the light from the Sun.
- Student answer: Because the sun is up.
- Gold label: `irrelevant`

### Group 4 — seen (`dev_ua`), Correct

- UIDs: `scientsbank-train-4328`, `scientsbank-train-4329`, `scientsbank-train-4331`, `scientsbank-train-4350`
- Dataset / question ID: `scientsbank` / `SCI-59e99eb9`
- Question: The inside of a pea seed is shown below. Describe the function of each of the parts: embryo.
- Reference answer: The embryo contains the tiny leaves and root of the plant.
- Student answer: Baby plant.
- Gold label: `correct`

### Group 5 — unseen (`dev_uq`), Correct

- UIDs: `scientsbank-train-1429`, `scientsbank-train-1445`
- Dataset / question ID: `scientsbank` / `SCI-6f6d0ad6`
- Question: How can you use a magnet to find out if the key is iron or aluminum?
- Reference answer: If the key sticks, the key is iron; if the key does not stick the key is aluminum.
- Student answer: If it is iron it will stick if it is aluminum it will not stick.
- Gold label: `correct`

### Group 6 — unseen (`dev_uq`), Partially Correct

- UIDs: `scientsbank-train-1442`, `scientsbank-train-1447`
- Dataset / question ID: `scientsbank` / `SCI-6f6d0ad6`
- Question: How can you use a magnet to find out if the key is iron or aluminum?
- Reference answer: If the key sticks, the key is iron; if the key does not stick the key is aluminum.
- Student answer: The magnet will stick.
- Gold label: `partially_correct_incomplete`

### Group 7 — seen (`dev_ua`), Correct

- UIDs: `scientsbank-train-2111`, `scientsbank-train-2118`
- Dataset / question ID: `scientsbank` / `SCI-81b69aea`
- Question: Look at the schematic diagram. What will happen to the other 2 bulbs if the middle bulb burns out?
- Reference answer: If the middle bulb burns out the other 2 bulbs will stay lit.
- Student answer: They will stay light.
- Gold label: `correct`

### Group 8 — seen (`dev_ua`), Correct

- UIDs: `scientsbank-train-1708`, `scientsbank-train-1709`
- Dataset / question ID: `scientsbank` / `SCI-914b7539`
- Question: Only one circuit below will light the bulb. Which one will work? Why is that the only circuit that will work?
- Reference answer: That circuit is the only circuit that uses all of the correct contact points.
- Student answer: Because the negative is connected to the black part and the positive side is attached to the shiny part.
- Gold label: `correct`

### Group 9 — unseen (`dev_uq`), Correct

- UIDs: `scientsbank-train-176`, `scientsbank-train-178`
- Dataset / question ID: `scientsbank` / `SCI-96335095`
- Question: Georgia found one brown mineral and one black mineral. How will she know which one is harder?
- Reference answer: The harder mineral will leave a scratch on the less hard mineral. If the black mineral is harder, the brown mineral will have a scratch.
- Student answer: The harder mineral will leave a scratch on the less hard mineral.
- Gold label: `correct`

### Group 10 — seen (`dev_ua`), Correct

- UIDs: `scientsbank-train-4584`, `scientsbank-train-4608`
- Dataset / question ID: `scientsbank` / `SCI-9fba0c20`
- Question: How do you define a controlled experiment?
- Reference answer: An experiment is controlled if only one variable is changed at a time.
- Student answer: A controlled experiment is when you only change one variable at a time.
- Gold label: `correct`

### Group 11 — unseen (`dev_uq`), Partially Correct

- UIDs: `scientsbank-train-2046`, `scientsbank-train-2070`
- Dataset / question ID: `scientsbank` / `SCI-d684620d`
- Question: Look at the picture of the circuit to the right. What will happen to the motor if the light bulb burns out?
- Reference answer: The motor will continue to run because the motor still has a pathway to the D-cell.
- Student answer: It will still run.
- Gold label: `partially_correct_incomplete`

### Group 12 — unseen (`dev_uq`), Partially Correct

- UIDs: `scientsbank-train-2061`, `scientsbank-train-2068`
- Dataset / question ID: `scientsbank` / `SCI-d684620d`
- Question: Look at the picture of the circuit to the right. What will happen to the motor if the light bulb burns out?
- Reference answer: The motor will continue to run because the motor still has a pathway to the D-cell.
- Student answer: The motor will run.
- Gold label: `partially_correct_incomplete`

### Group 13 — unseen (`dev_uq`), Partially Correct

- UIDs: `scientsbank-train-2036`, `scientsbank-train-2039`
- Dataset / question ID: `scientsbank` / `SCI-d684620d`
- Question: Look at the picture of the circuit to the right. What will happen to the motor if the light bulb burns out?
- Reference answer: The motor will continue to run because the motor still has a pathway to the D-cell.
- Student answer: The motor will still run.
- Gold label: `partially_correct_incomplete`

### Group 14 — unseen (`dev_uq`), Contradictory

- UIDs: `scientsbank-train-2054`, `scientsbank-train-2067`
- Dataset / question ID: `scientsbank` / `SCI-d684620d`
- Question: Look at the picture of the circuit to the right. What will happen to the motor if the light bulb burns out?
- Reference answer: The motor will continue to run because the motor still has a pathway to the D-cell.
- Student answer: The motor will stop.
- Gold label: `contradictory`

### Group 15 — unseen (`dev_uq`), Correct

- UIDs: `scientsbank-train-2479`, `scientsbank-train-2482`
- Dataset / question ID: `scientsbank` / `SCI-da03e154`
- Question: Mary told her friend Sharice that she had a rug to sell. Sharice asked if the rug would fit perfectly, wall to wall, in her bedroom. Mary went home and measured the rug. She put her feet heel-to-toe and counted the number of shoe lengths it took to measure the rug. She found the rug was 18 shoes long and 12 shoes wide. Sharice did the same thing in her room to measure the space for the rug. Her floor was 18 shoes long and 12 shoes wide. A perfect fit! Sharice bought the rug and took it home. To her dismay, she found it was too short and too narrow for her bedroom! What could Mary and Sharice do to better measure the size of the rug?
- Reference answer: Use a standard unit of measurement such as centimeters or meters.
- Student answer: They could use a meter tape.
- Gold label: `correct`

### Group 16 — unseen (`dev_uq`), Correct

- UIDs: `scientsbank-train-2475`, `scientsbank-train-2476`
- Dataset / question ID: `scientsbank` / `SCI-da03e154`
- Question: Mary told her friend Sharice that she had a rug to sell. Sharice asked if the rug would fit perfectly, wall to wall, in her bedroom. Mary went home and measured the rug. She put her feet heel-to-toe and counted the number of shoe lengths it took to measure the rug. She found the rug was 18 shoes long and 12 shoes wide. Sharice did the same thing in her room to measure the space for the rug. Her floor was 18 shoes long and 12 shoes wide. A perfect fit! Sharice bought the rug and took it home. To her dismay, she found it was too short and too narrow for her bedroom! What could Mary and Sharice do to better measure the size of the rug?
- Reference answer: Use a standard unit of measurement such as centimeters or meters.
- Student answer: Use a meter tape.
- Gold label: `correct`

### Group 17 — seen (`dev_ua`), Correct

- UIDs: `scientsbank-train-2421`, `scientsbank-train-2429`
- Dataset / question ID: `scientsbank` / `SCI-f4b09ef4`
- Question: Jen was talking on the phone with her Uncle Bill who lives in Canada. When she asked him how the weather was, he said it was nice and warm, about 28 degrees. What unit is Uncle Bill using to report the temperature?
- Reference answer: Bill must have been using degrees Celsius if 28 is a warm temperature.
- Student answer: Degree Celsius.
- Gold label: `correct`

## Where the duplicates occur

| Check | Result |
|---|---|
| Within the same question ID | Yes; all 17 groups. |
| Across different question IDs | No; zero groups with repeated core text across question IDs. |
| Across datasets | No; every group is SciEntsBank and no exact-content group spans datasets. |
| Across seen/unseen splits | No; every group stays within one split. Five groups are seen (`dev_ua`); 12 are unseen (`dev_uq`). |
| Beetle rows | None in these groups. |

The groups contain 24 Correct rows, 8 Partially Correct rows, 2 Irrelevant
rows, and 2 Contradictory rows. They comprise 12 seen rows and 24 unseen
rows. The 19 excess repeated rows comprise 7 seen and 12 unseen rows.

## Source and preprocessing investigation

**Verified:** All 36 UIDs in the groups occur as separate unique UID rows in
each of:

- `project_s_qa/A_submission_v2/reports_v2/A_deployed_dev_probs_v2.parquet`
- `drive_backup_20261107/reports/scored_dev_v1.parquet`
- `drive_backup_20261107/reports/scored_dev_v2.parquet`

For each file, those 36 rows are SciEntsBank, span 11 question IDs, and have
the same 12 `dev_ua` and 24 `dev_uq` split counts. The scored probability
artifacts do not contain question, reference-answer, or student-answer text,
so they cannot independently confirm textual identity.

**Verified from source code:**
`Project_S_QA_Evidence/Phase_3/x0_make_dev_text_v3.py` filters source rows to
the dev-probability UID set, rejects duplicate UIDs, checks exact UID-set
coverage, and merges with `validate="one_to_one"`. It does not deduplicate
identical answer text. Therefore this export step cannot multiply rows through
a many-to-many UID join; it preserves distinct UIDs even when their text is
identical.

**Unverified:** Whether the repeated text was already present in the original
raw dataset or was introduced earlier in preprocessing cannot be established
from the inspected artifacts. The upstream `sra_unified_splits_v1.parquet`
contains mixed splits and was not opened. No separate test-free raw source
copy with the required text fields was identified in the searched local
project tree. The 36 UIDs already appearing in earlier scored-dev artifacts
show that these rows predate the Phase 3 text-export step, but do not prove the
exact text was identical at that earlier stage.

## Counts under possible policies

| Policy | Rows retained | Exact unique examples represented | Explanation |
|---|---:|---:|---|
| Retain all rows | 2,049 | 2,030 | Preserve every UID; the 17 groups contribute 19 repeated extra rows. |
| Retain one row per exact duplicate group | 2,030 | 2,030 | Remove 19 excess rows, keeping one representative from each group. |
| Exclude every duplicate group entirely | 2,013 | 2,013 | Remove all 36 rows in the 17 affected groups. |

These are counts only; no policy was applied and no source artifact was
changed.

## Evaluation risks and recommendation

Repeated exact examples can give those question-answer patterns extra weight
in row-level accuracy, F1, and confusion counts. All repeats are within a
single question group, so a question-grouped bootstrap keeps each duplicate
group together, but it does not undo their extra weight in the point estimates
or within-group row metrics. Removing all 36 rows would also discard valid
records and shift the label and seen/unseen composition.

**Recommendation:** retain all 2,049 UIDs for the primary reproduction unless
the dataset owner confirms these are accidental copies. The distinct source
UIDs and their presence in earlier scored-dev artifacts are consistent with
separate source responses that happen to share text, but raw-source identity
is unverified. If approved, report a secondary sensitivity analysis retaining
one row per exact duplicate group (2,030 rows); do not replace the original
baseline. Do not exclude entire groups without evidence that those records
are invalid. Experiment 1 remains blocked until Jigar explicitly chooses and
documents the duplicate policy.
