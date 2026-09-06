# Repository Completeness Audit — Thesis v344 Alignment

This audit records what the private thesis/examination GitHub repository actually contains and, equally importantly, what it does **not** contain. Its purpose is to prevent the thesis or repository documentation from overstating reproducibility or release completeness.

## Audit verdict

### 1. Canonical analytical reproducibility: PASS, scope-qualified

Present in Git:

- canonical `data/canonical/master_runs.csv` (280 run-level rows × 39 fields) and data dictionary;
- controlling v330 analysis materialiser/runner and dependency record;
- principal analysis scripts and historical provenance;
- small supplementary post-idle, warm-up and burst-recovery carriers;
- current Chapter-4 numerical carriers and verification records;
- SHA-256/integrity manifests and provenance documentation.

A normal retained-data analytical rerun is supported. Exact reproduction of every frozen exhibit still depends on the controlled external evidence stated in `REPRODUCIBILITY.md`.

### 2. Benchmark execution logic: PASS

Present in Git:

- `benchmark/orchestrator/orchestrator.ps1`;
- all four k6 scenario scripts;
- `benchmark/parse_k6_output.py`;
- scenario/platform configuration evidence, with safe `.PUBLIC` derivatives where credentials or sensitive endpoints require redaction.

### 3. Canonical dataset: PASS

`data/canonical/master_runs.csv` is present and is the frozen 280 × 39 analytical dataset used by the controlling analysis.

### 4. Complete historical raw campaign inside ordinary Git: NOT CLAIMED / NOT PRESENT

The complete original per-run k6 JSON/CSV archive, the full retained run-log collection and the complete Docker telemetry archive are intentionally held outside ordinary Git history. Their manifests and availability boundaries are retained in this repository. This is therefore **not** a public all-raw-bytes archive.

### 5. Complete runnable historical Django application source tree inside this repository: NOT COMPLETE

The repository contains a selected sanitised benchmark-relevant application source capture, including `manage.py`, requirements/runtime files, Dockerfiles, project URLs/settings/WSGI files, and the principal `commerce` models/views/URLs.

However, the Git-tracked `application/commerce/` directory does not contain every supporting file historically associated with the full application tree. For example, the retained `views.py` imports `.forms`, while `commerce/forms.py` is not present in the current Git tree; the full templates and migration tree are also not present in ordinary Git. Consequently, this repository must **not** be described as containing every line of the complete historical Django application or as a self-contained byte-for-byte rebuild of that application.

The complete source tree was historically retained under the controlled research evidence environment; adding further source files to Git should occur only from a verified benchmark-time/current controlled source snapshot, after secret scanning and identity/hash checks. Older prose listings or reconstructed copies must not be substituted silently.

### 6. Configuration completeness: PASS for auditable safe captures; not unredacted-secret completeness

Configuration evidence needed to understand the benchmark is present in safe/redacted form where necessary. Credentials, private endpoints and other sensitive originals are deliberately excluded. This is a security boundary, not a missing-evidence claim.

## Thesis wording approved by this audit

A safe statement is:

> The private thesis/examination GitHub repository contains the canonical dataset, benchmark scripts, selected sanitised application/configuration captures, analysis scripts and integrity/provenance manifests. The complete raw archive, full Docker telemetry and restricted/sensitive originals remain outside ordinary Git history under controlled access.

Do **not** state that the GitHub repository contains “all code, all raw data and every historical artefact” unless a later audit first verifies those additional materials.

## Public-release gate

Before changing repository visibility or making a stronger completeness claim:

1. add the verified complete publishable application source snapshot if public full-source reproduction is intended;
2. secret-scan every added source/configuration file;
3. verify source identity against the controlled evidence state;
4. decide whether the heavy raw archive and full Docker telemetry will be published separately or remain controlled;
5. update the data-availability statement accordingly;
6. record a release tag/commit and, if used, archival DOI only after verification.
