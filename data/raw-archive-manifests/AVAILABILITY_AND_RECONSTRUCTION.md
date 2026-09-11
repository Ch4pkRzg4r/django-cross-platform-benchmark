# Raw Archive Availability and Reconstruction

## Current submission-access state

The repository contains integrity manifests describing the expected historical raw campaign files and archive parts. **Those manifests are identity records; they are not evidence that every corresponding raw byte stream is currently accessible.**

The independent v365 full-evidence audit examined the raw archives supplied with the submission evidence. Four files (`raw_k6_280.zip`, `raw_k6_B_mixed.zip`, `raw_k6_C_checkout.zip`, and `raw_k6_D_burst.zip`) begin with ZIP local-file headers but are **truncated**: they lack a complete central directory/end-of-central-directory record and their terminal member streams are incomplete.

Complete-prefix recovery and canonical SHA-256 matching established:

- **73 complete canonical run pairs** (73 JSON + 73 CSV) recoverable and identity-verified;
- **207 of the 280 canonical run pairs unavailable** in the supplied submission evidence;
- every recovered complete member was checked for completed DEFLATE stream, size/CRC where available and canonical raw-file hash identity;
- malformed terminal partial members were not counted as complete runs.

Recoverable complete run coverage in the supplied damaged archives was:

- Apache + mod_wsgi: A=10, B=10, C=10, D=10;
- Nginx + uWSGI: B=9, C=1, D=10;
- Django + Gunicorn: D=10;
- Azure Container Apps: D=3.

Other recovered same-name/pilot candidates did not add canonical matches for the missing run identities. Multipart-RAR manifests were found, but the actual historical RAR volumes were **not present in the inspected submission/recovery evidence**. Therefore the repository no longer claims that complete locally verified multipart RAR sets are presently available to a reader of this public release.

## What remains reproducible

- The frozen canonical analytical dataset (`data/canonical/master_runs.csv`, 280 × 39) remains byte-identified and supports complete rerunning of the retained computational analysis.
- The recovered 73 complete raw run pairs independently reconcile with their corresponding canonical rows and support, rather than contradict, the frozen parser-derived values.
- Full raw-to-canonical reconstruction of all 280 retained runs **cannot be certified from the currently supplied raw bytes**.
- The missing raw streams are an evidence-availability boundary; they are not imputed, regenerated or treated as zero.

## Integrity manifests

The adjacent manifests retain the expected identities for historical raw files, run logs, Docker telemetry and historical archive parts. They are useful for checking a recovered file/volume **if the actual bytes are later supplied**. They must not be described as proof that the bytes are currently available.

## If additional historical volumes are recovered

Do not overwrite the damaged submission archives. Stage recovered volumes separately and:

1. test the complete archive/container before extraction (`7z t ...` or the format-appropriate test command);
2. extract to a disposable directory;
3. verify every recovered raw file against `raw_files_sha256_manifest.csv`;
4. verify naming/run-ID uniqueness and the 7 × 4 × 10 expected retained design;
5. rerun representative and full raw-to-canonical reconciliation through the historical parser logic;
6. record the recovered-volume hashes and custody/source in a new dated evidence register.

No public raw-data URL or complete-raw release is claimed until those steps have succeeded for the actual bytes.
