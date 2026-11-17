# Project S — Assessment Review Template

**Status: Drafted.** No reviewer is nominated and no record is approved by
this template. `approved` is reserved for actual, documented human approval.

## Subject reviewer assignments

Complete one row per reviewer and subject before review begins. Jigar assigns
reviewers; no names or qualifications are assumed here.

| Subject | Required expertise | Reviewer name / ID | Qualifications and evidence | Independence/conflict check | Assignment date |
|---|---|---|---|---|---|
| Science | Relevant science teaching or subject-matter expertise; age/grade-appropriate explanations and misconceptions | __________ | __________ | __________ | __________ |
| Social Science | Relevant history/geography/civics/economics expertise; sources, chronology, context and causal claims | __________ | __________ | __________ | __________ |
| Mathematics | Relevant mathematics teaching or subject expertise; symbolic equivalence, units, tolerances and valid methods | __________ | __________ | __________ | __________ |
| English | English/language teaching or subject expertise; meaning, paraphrase, context and objective-relevant grammar | __________ | __________ | __________ | __________ |

For disputed or high-impact records, use a second independent reviewer and a
named adjudicator. The adjudicator records the resolution and rationale.

## Required workflow and status transitions

| Current state | Who may transition it | Next state | Required evidence |
|---|---|---|---|
| `draft_unreviewed` | Content author/owner | `in_review` | Stable ID, source/provenance, version, complete required fields, no self-approval. |
| `in_review` | Assigned qualified subject reviewer | `revision_required` | Field-level comments and reason for each requested change. |
| `revision_required` | Content author/owner | `in_review` | New version; preserve prior version and response to comments. |
| `in_review` | Assigned qualified reviewer(s) | `rejected` | Reason, evidence, and unresolved issue; rejected records cannot be served as approved assessment content. |
| `in_review` | Qualified reviewer plus adjudicator when needed; project owner records outcome | `approved` | Signed question/rubric review checklist, source verification, version, reviewer identities and dates. |

The project owner may not mark an item approved without the required subject
review sign-off. Any substantive edit to an approved question or rubric creates
a new version and returns it to `draft_unreviewed` or `in_review`.

## Question-level review checklist

Record `PASS`, `REVISION`, `FAIL`, or `NOT APPLICABLE` with evidence for each:

- [ ] Stable unique question ID; subject, grade, chapter/topic and difficulty
  are present and consistent.
- [ ] Question text is clear, age-appropriate, answerable, and supported by
  the recorded source/provenance.
- [ ] Reference answer is correct for the stated question and grade.
- [ ] Accepted variants preserve the required meaning and do not admit a
  wrong or off-question answer.
- [ ] Required concepts are necessary and sufficient for the expected answer;
  supporting concepts are distinguished from required ones.
- [ ] Misconceptions and contradictory claims describe realistic errors and
  are not confused with valid alternative explanations.
- [ ] Partial-credit rules specify observable evidence, missing concepts,
  contradictions, and valid partial reasoning.
- [ ] Ambiguous or under-specified questions have an explicit disposition;
  do not invent a unique gold answer where several are valid.
- [ ] Provenance, source version/page, author, reviewer, timestamp, and record
  version are stored.

## Rubric-level review checklist

- [ ] Rubric is linked to exactly the intended question ID and version.
- [ ] Correct / Partial / Incorrect criteria are mutually understandable and
  cover plausible answer variations.
- [ ] Subject-specific criteria are used:
  - **Science:** concept accuracy, causal reasoning, and misconception handling.
  - **Social Science:** factual accuracy, chronology, context, and causal
    relationships.
  - **Mathematics:** numerical/symbolic equivalence, units, tolerances, and
    alternate valid methods or partial work.
  - **English:** meaning-preserving paraphrase, contextual interpretation, and
    grammar only where it is part of the learning objective.
- [ ] Accepted alternatives, required/supporting concepts, misconceptions,
  contradictory claims, examples, and partial-credit definitions are reviewed
  separately.
- [ ] Reviewer records a rationale and at least one edge case or ambiguity.
- [ ] A second review/adjudication is recorded for disagreements.

## Per-record sign-off

```text
question_id:
question_version:
rubric_version:
subject / grade:
source provenance and version:
review status before review:
reviewer name / ID:
qualification evidence:
review date:
question correctness: PASS / REVISION / FAIL
accepted variants: PASS / REVISION / FAIL
concepts and misconceptions: PASS / REVISION / FAIL
contradictions: PASS / REVISION / FAIL
partial-credit criteria: PASS / REVISION / FAIL
ambiguity disposition:
review notes / evidence:
adjudicator (if needed):
final decision: approved / revision_required / rejected
approved version and timestamp (only when approved):
reviewer sign-off:
project owner recorded by / date:
```

## Current evidence reminder

The inspected package contains 251 rubric records (248 `auto_draft`, 3
`demo`); `verified_by` is empty for all. The 12-question Science prototype
records are all `draft_unreviewed`; the CSV's draft status is not review
evidence. These source-level facts do not establish educational quality or
approval. Social Science, Mathematics, and English reviewer/content coverage
remain unverified.
