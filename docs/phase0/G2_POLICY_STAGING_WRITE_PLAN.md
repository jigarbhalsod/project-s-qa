# G2 policy staging write plan

**Status: WAITING FOR EXPLICIT USER AUTHORIZATION.** Candidate approval and
approval in principle do not authorize this copy operation.

## Objective

Copy the approved scratch policy to the scorer's expected path:

- Source: `Project_S_QA_Evidence/Phase_0/scratch/policy_compare_20261107_160707/staged_policy.json`
- Destination: `project_s_qa/reports_v2/A_abstain_policy_v2.json`
- Operation: **COPY SOURCE TO DESTINATION**
- Expected SHA-256: `BABF76F460D2A6516D9EF11D317F69CEDDB0958DD67A2CE06D3B67496163AD25`

Purpose: make the approved policy candidate available where the scorer looks
for it. Do not replace the root JSON or combine it with the packaged JSON.

## Source verification

Local audit on 16 November 2026 found a JSON file, 784 bytes, modified
2026-11-07 16:07:08. Its SHA-256 is
`BABF76F460D2A6516D9EF11D317F69CEDDB0958DD67A2CE06D3B67496163AD25`,
matching the approved value. The file declares pooled mode, temperature
1.0000000000000004, confidence threshold 0.64, and contradiction review off.

## Destination verification

The destination file is absent. Its parent directory exists. The parent has
ReadOnly and ReparsePoint attributes in the local listing; write ability and
cloud synchronization were not tested. Source and destination are on volume
`C:\`. Since the destination does not exist, symlink status is not applicable.
The absent destination has no tracked-file or uncommitted-change entry in the
local Git checks. No existing destination hash or size applies.

## Preconditions and operation

Proceed only if the source still exists and its hash matches exactly, the
parent still exists, the destination remains absent, and no relevant worktree
state has changed. Abort on any mismatch. Do not create directories. Do not
overwrite. A separate user approval must name this exact source, destination,
copy operation, and expected hash. The present approval is only in principle.

## Backup and rollback

No destination backup is needed while the destination is absent. If an
authorized copy later succeeds, rollback may remove only that newly created
file, only after confirming its hash still equals the approved hash and no
later process changed it. Removal requires separate authorization. Never
remove or replace a pre-existing user file.

## Post-write verification

After separate authorization, verify the destination is a regular file with
the expected SHA-256, verify the source hash is unchanged, and check that no
unrelated files changed. Record the actual Git status and hash results. Do not
claim cloud synchronization from local copy verification.

## Authorization

**WAITING FOR EXPLICIT USER AUTHORIZATION**

This document is not permission to execute the operation. Staging has not
been performed.