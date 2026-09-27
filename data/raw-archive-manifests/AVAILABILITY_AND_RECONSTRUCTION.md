# Raw Archive Availability and Reconstruction

## Raw-data location and access

The complete retained raw k6 collection is stored in the author's [raw-data archive on Google Drive](https://drive.google.com/drive/folders/1jAqu_W0vK0bgscBe5DE6t67NCMf2Sfhd). It contains **280 canonical JSON/CSV run pairs (560 files)** for seven platforms × four scenarios × ten replications. The raw archives are stored outside GitHub; this repository provides the canonical analytical dataset, code and integrity manifests.

Google Drive permissions govern access. If the folder requires permission, request access from the author through Google Drive. The link identifies the storage location and does not imply unrestricted public download access.

## Multipart archive layout

Use these two complete RAR sets in the linked folder:

| Raw format | Archive parts | Contents |
|---|---|---|
| JSON | `taw data  json.part001.rar` through `taw data  json.part005.rar` | 280 retained per-run JSON files |
| CSV | `raw data excel.part001.rar` through `raw data excel.part003.rar` | 280 retained per-run CSV files; the archive name uses “excel” |

Preserve the supplied filenames, download all parts of each required set into the same local directory, and open the first part to test and extract that set. The integrity statement here applies to the eight listed RAR volumes and their verified contents; other archive formats in the folder are not substituted for these verified sets.

## Verified retained-data coverage

The integrity review read the actual archive bytes and verified:

- all eight archive-volume sizes and SHA-256 values against the retained volume manifest;
- all 560 per-run file sizes and SHA-256 values against `raw_files_sha256_manifest.csv`;
- all 280 canonical run IDs, without missing, extra or duplicate retained identities;
- the complete 7×4×10 retained design: 40 pairs per platform, 70 pairs per scenario and 10 pairs per platform–scenario cell.

The frozen canonical dataset (`data/canonical/master_runs.csv`, 280×39) has SHA-256:

`710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7`

## Raw-to-canonical reconciliation

Replaying the historical JSON parser over all 280 retained JSON streams reproduced all **32 JSON-derived fields per run** at the parser's stored precision: **8,960 comparisons with no discrepancy**. Seven identity/metadata fields (`run_id`, `platform`, `scenario`, `replication`, `start_time`, `end_time`, `target_rps`) were retained from the canonical dataset and are not counted as independently reconstructed JSON fields. CSV size/hash verification is distinct from semantic replay of downstream CSV-based calculations.

## Verification of a downloaded copy

1. Preserve the downloaded archive bytes and record their sizes and SHA-256 values.
2. Test each complete multipart RAR set before extraction.
3. Verify every raw file against `raw_files_sha256_manifest.csv`.
4. Check run-ID uniqueness, JSON/CSV pairing and the 7×4×10 retained design.
5. Replay the historical parser and compare the 32 derived fields at its stored precision.
6. Check metadata and downstream temporal/statistical outputs under their respective procedures.

## Interpretation boundary

Complete retained raw files support checking the reported 280-run dataset. They do not, by themselves, establish a complete immutable ledger of every attempt, replacement or exclusion, identify every effective per-run runtime setting, or recreate unrecorded historical provider state. Version-specific audit records retain their historical scope; this document states the current retained-data availability and access route.
