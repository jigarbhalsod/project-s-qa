# Phase 4 Archive Verification

## Historical findings (superseded)
Earlier checks reported the extracted folder missing at the locations checked at that time. Those results are superseded by this fresh comparison.

## Current corrected comparison
- Archive: `project_s_qa/A_submission_v2.zip`
- Extracted folder: `project_s_qa/A_submission_v2`
- Extracted folder exists: YES
- ZIP readability and CRC test: PASS
- ZIP SHA-256: `0abb38aaba65194cc4fbd495a441861afce7d2ab2ee3659e83cd51703d93f09f`
- File entries: 55; explicit directory entries: 0
- Uncompressed size: 950030 bytes
- Virtual folder structure: demo/, reports_v2/
- Extracted files: 55
- Missing: 0; extra: 0; size mismatches: 0; SHA-256 mismatches: 0
- Duplicate paths: none; zero-byte files: none
- Exact file path, size and SHA-256 match: YES

### Difference lists
- Missing files: none
- Extra files: none
- Size mismatches: none
- SHA-256 mismatches: none

### Submission manifest
- Manifest path: `reports_v2/A_submission_manifest_v2.json`
- Declared payload files: 54; manifest hash mismatches: none
- Archive files not declared, excluding the manifest itself: none
- Count discrepancy resolved: 55 ZIP entries = 54 payload files + the manifest itself.
- Manifest parity field: `pass`; it is an archived claim, not separate proof of execution provenance.

## Final status: PASS
