# Repository Gap Scan v365

This note records the **metadata-only** targeted gap scan supplied on 2026-09-10. It does not promote any candidate file into the repository and does not certify a file as safe merely because the filename scan did not flag it.

## Public release stage

The retained WSL directory `~/thesis/public_release_stage` exists and contains exactly three staged artefacts:

- `ecommerce_migrated_public_clean.tar.gz` — 15,799,951 bytes — SHA-256 `3b4d15c1f9e200e9cc93fe13cb344f18dffa2ffb1893fb1e0929d6e2dbe0393f`
- `environment_manifest.txt` — 2,852 bytes — SHA-256 `2e701c5a3b227192306ec13ab011551dee4f08916707e757da78b7f49ec3d0d9`
- `public_release_sha256.txt` — 238 bytes — SHA-256 `7a4ffbd11693d2d0ba818f7a44551dbacf66b02e00bd369ef92c9e4f055485f4`

The staged archive is the preferred next source for recovering a publishable application tree, but its contents still require extraction, content-level secret scanning and source-hash/provenance checks before repository promotion.

## Targeted configuration evidence discovered

The scan returned 529 path-name candidates. Useful high-confidence candidates include:

### Gunicorn

- Historical WSL source: `ecommerce_migrated/ecommerce/gunicorn_conf.py`
- Size 357 bytes; SHA-256 `5af98c90b48939ae9c4c0942f7b4040b144fadb788657a890ab920b49e28198b`
- This closes a concrete current repository gap because `application/Dockerfile` references `ecommerce.gunicorn_conf` but the file is absent from the current Git tree.

### IIS + Waitress

Multiple retained captures exist. The strongest publishable-looking candidates are the redacted/safe variants, including:

- `web.config.redacted.xml` — SHA-256 `8f9a66e32e39...` in the 2026-06-22 alignment capture;
- `apply-memory-limit.ps1` — SHA-256 `b0c954ce54c4...`;
- `appcmd_config_redacted.xml` — SHA-256 `a66ee4a56f1b...`;
- `sites_safe.txt`, runtime/process snapshots and Python/Waitress package/version captures.

These remain candidates until their contents are reviewed. Raw `settings.py`, `views.py` and one IIS `site.txt` were conservatively secret-flagged and must not be promoted directly.

### PgBouncer

The current repository already contains `environment/pgbouncer_runtime_extract.PUBLIC.txt` with SHA-256 `902c7ec7fcdda324169d481f25341712e4a181b874ec60f8cbda3f41f815c414`, matching one retained evidence copy. No replacement is required unless a stronger exact benchmark-time configuration is recovered.

### Azure Container Apps

A safe-named capture script exists (`04_capture_azure_containerapps.sh`), but the targeted scan did **not** identify a clear benchmark-time ACA deployment export/Bicep/YAML definition. Later Azure read-only evidence exists, but it must not be silently reclassified as benchmark-time deployment truth.

### Koyeb

Several capture/probe scripts and evidence-package hashes exist. A non-empty exact benchmark-time service export was not identified by this scan. Current and later captures must remain distinguished from benchmark-time evidence.

### Fly.io

The earlier local inventory found `C:\Users\Tech Line\fly-deploy\fly.toml` (820 bytes; SHA-256 `7760d48f66c207e73d9a2e41fe6df0dbe80968b736cd148119719517bd18f300`), but the conservative scan flagged it as potentially secret-bearing. It must not be uploaded raw. A reviewed `.PUBLIC.toml` derivative should be produced from this exact source while retaining its source hash and redaction provenance.

## Security findings

The targeted scan conservatively flagged 16 files. Repeated sensitive candidates include raw Django `settings.py`, some `views.py` captures, one IIS `site.txt`, and capture scripts. These flags may include false positives, but all flagged files require content review/redaction before any GitHub write.

The existing `configuration/docker-compose-phase65.PUBLIC.yml` was also pattern-flagged by the conservative scanner even though it is already a `.PUBLIC` derivative. That should be manually reviewed rather than automatically removed or rewritten.

## Next gate

1. Extract `ecommerce_migrated_public_clean.tar.gz` locally and content-scan it.
2. Package the safe application source tree plus exact manifests/provenance for review.
3. Produce a redacted Fly.io derivative from the exact `fly.toml` while preserving its source SHA-256.
4. Package only the selected redacted/safe IIS evidence files.
5. Do not claim exact ACA/Koyeb deployment definitions unless an actual benchmark-time export/config is found.
6. Only after content review, stage safe files on this branch and regenerate `FILE_INDEX.csv` and `MANIFEST_SHA256.csv`.

No change to the frozen 280×39 canonical dataset or historical analytical base is authorised by this gap scan.
