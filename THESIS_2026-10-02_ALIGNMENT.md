# Thesis and repository alignment — 2 October 2026

This document supersedes the 1 October record for the identity of the distributed Word files. The computational release, canonical dataset, scientific tables, figure payloads, primary inference and archived-summary sensitivity values are unchanged. Historical alignment records and their hashes continue to identify their original versions.

## Document clarification

Four prose paragraphs were revised in Sections 3.11.1, 3.17.2, 4.3 and 6.4. They distinguish the researcher's stated operational reason for managed-service retests from the limits of independent run-by-run attribution. They explicitly preserve the final 280-run dataset as the primary analysis and retain the archived Fly.io comparison as exploratory sensitivity evidence. Neither an outcome-based motive nor the invalidity of every earlier measurement is asserted as established.

The 257-row backup comparison still yields 228 unchanged rows, 29 replaced run IDs and 23 final IDs absent from that backup. No observation or numerical result was changed during this clarification. The dataset remains 280 × 39 with 10,349,833 recorded requests. This revision did not repeat the full raw-data replay or collect a new benchmark campaign.

## Verification

The controlling Full, Part 1 and Part 2 SHA-256 values are in `documentation/thesis_alignment_2026-10-02.json`. Their local render counts remain 191, 102 and 89. Full body text equals the concatenated parts. All 73 Full tables, 28 media payloads, references and citation hyperlinks are preserved. Only four Full paragraphs change, with two corresponding changes in each part. All 222 static navigation entries still agree with the final local render.

Only `word/document.xml` changes inside each Word package. The previously cleaned package structure and empty core/app metadata remain intact. No macros, comments, tracked changes, custom XML, embedded objects or live body fields were introduced. Restored author, supervisor and university details are intentionally preserved. These are identified thesis copies, not anonymous checking-service copies.

Rendering uses LibreOffice. No new native Microsoft Word or Turnitin processing result is claimed.

## Computation and historical records

The commands in `REPRODUCIBILITY.md` remain the current computational entry points. All numerical reference carriers and figure maps retain their 1 October identities. `verification/verify_current_thesis.py` now reads the 2 October document alignment and integrity manifest; its numerical checks remain unchanged.

`MANIFEST_2026-10-02_SHA256.csv` covers the current alignment, documentation, verifier and the previously reviewed computational files. Check historical manifests at their corresponding historical commits. The prior `THESIS_2026-10-01_ALIGNMENT.md` and JSON are preserved without rewriting their past document hashes.
