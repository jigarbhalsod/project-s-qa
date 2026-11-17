# Question-bank and rubric versioning design

**Status: Drafted proposal; no version was assigned to existing content.**

- Give each bundle a stable `bank_id` and immutable `bank_version`.
- Give each question and rubric a stable ID plus immutable record version.
- A substantive edit creates a new version; preserve prior bytes and record
  the superseded version and change reason.
- Each release manifest records schema version, source manifest, included
  IDs/versions, status counts, date, and SHA-256 for each file.
- Scoring/evaluation records identify exact bank and rubric versions; missing
  version identity limits reproducibility.
- Migrations are explicit, deterministic, versioned, and preserve source
  values. Never silently promote a draft status.
- Rejected/superseded items remain addressable but are excluded from an
  approved serving bundle.
- Rollback selects a prior immutable bundle by ID/hash; it does not rewrite
  current content.

Semantic-version format and compatibility policy remain owner decisions.
Hashes prove byte identity, not content authority or human approval.
