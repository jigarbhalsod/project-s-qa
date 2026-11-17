# Gate 4 — Question-bank and rubric evidence

**Status: BLOCKED.** Two local candidate sources were inspected structurally;
neither is selected as canonical, and structural presence is not content
approval.

| Source | Verified local facts | Gaps |
|---|---|---|
| project_s_qa/A_submission_v2/reports_v2/A_rubrics_v2.json | 251 keyed records; fields include question_id, dataset, reference_answer, accepted_variants, required_concepts, misconceptions, rubric_levels, worked_examples, status, verified_by, version, concepts_status. Status: 248 auto_draft, 3 demo; verified_by empty for all 251; concepts_status: 248 auto_draft_unreviewed, 3 hand_written_unreviewed. | No subject or grade fields; no reviewer sign-offs; not designated canonical. |
| PROJECT_S_QA_HANDOVER/question_bank/questions.json | 12 questions, all Science; grades 4/5/6 counts 4/6/2; all draft_unreviewed; required_concepts empty for all 12. | Draft prototype; no approved content or canonical designation. |
| PROJECT_S_QA_HANDOVER/question_bank/rubrics.json | 12 rubric entries keyed cbse_demo_01 through cbse_demo_12; all draft_unreviewed; required_concepts empty for all 12. | Draft rubric set; no reviewer approval or canonical designation. |

The files expose different IDs and schemas. No automatic merge is justified.
Ownership, authoritative source, version policy, provenance completeness,
subject/grade coverage, and approved status remain unresolved.

**Needed to pass:** Jigar selects a source/schema owner; provenance and
identifiers are reconciled; question/rubric records meet the review template;
only records with actual qualified sign-off may be marked approved.
