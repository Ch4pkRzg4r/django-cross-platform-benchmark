# Repository Completeness v365 — Staging Plan

Base analytical release: `5cfb18adb04da928bd07517a4f76261fe74246a1`  
Working branch: `repo-completeness-v365`

This branch is for repository-completeness work only. It must not silently rewrite the frozen 280×39 canonical dataset, the byte-exact v330 analytical base, or historical evidence.

## Current verified strengths

- Frozen canonical dataset `data/canonical/master_runs.csv` (280 × 39) and data dictionary.
- Four campaign k6 scenario scripts, campaign orchestrator and parser.
- Current v360 release entry point and release layer over the validated v330 base.
- Principal analysis scripts, supplementary analytical carriers, Chapter-4 table/figure carriers, verification records and SHA-256 manifests.
- Safe/redacted platform/scenario configuration metadata for all seven deployment paths.
- Selected benchmark-relevant Django application source capture.
- Raw/run-log/Docker-telemetry integrity manifests, with heavy evidence intentionally kept outside ordinary Git history.

## Known completeness gaps to close only from verified source snapshots

### Application source

The current `application/` tree is not a complete runnable historical Django source tree. Candidate files that should be recovered from a verified source snapshot, where they actually existed, include:

- project support: `ecommerce/__init__.py`, `asgi.py`, `gunicorn_conf.py` and any other imported project modules;
- app support: `commerce/__init__.py`, `apps.py`, `admin.py`, `forms.py`, `signals.py`, `tests.py`;
- complete migration tree;
- complete template tree and custom template tags;
- verified fixture/loading tooling and only a safe publishable fixture derivative;
- required static source assets where needed to run the benchmark-facing routes.

Do not reconstruct these files from thesis prose. Recover exact bytes from the retained source snapshot, hash them, secret-scan them, and create clearly labelled `.PUBLIC` derivatives if redaction is needed.

### Deployment/platform captures

Create an auditable per-platform configuration structure for all seven paths, using exact or sanitised verified captures:

1. Apache + mod_wsgi — server config, Docker/build definition, compose/service/resource-limit excerpt.
2. Nginx + uWSGI — Nginx/uWSGI/Supervisord configs, Docker/build definition, compose/service/resource-limit excerpt.
3. Django + Gunicorn — Gunicorn startup/config (`gunicorn_conf.py` if used), Docker/build definition, compose/service/resource-limit excerpt.
4. Azure Container Apps — sanitised deployment/export or CLI/Bicep/YAML recipe recording region, image identity, CPU/RAM, ingress/port, min/max replicas and scaling settings.
5. Koyeb — sanitised service definition/export/CLI recipe recording region, image identity, resources, port, health/scaling settings.
6. Fly.io — verified `fly.toml`, image/deployment identity, machine/resource/region and auto-start/auto-stop/min-machine settings.
7. IIS + Waitress — verified `web.config`, Waitress launch/service settings, memory-limit script/config and Windows/IIS/Python runtime capture, preserving the documented REV5 boundary.

Data tier should additionally have a verified/sanitised PgBouncer configuration or runtime-equivalent extract and data-initialisation/fixture procedure where available.

### Data and heavy evidence

Do **not** place the ~73.5 GB original raw archive into ordinary Git history. Keep:

- canonical 280×39 dataset and small supplementary data in Git;
- full per-file SHA-256 manifests in Git;
- optional small representative raw examples in Git if approved;
- complete raw JSON/CSV, run logs and full Docker telemetry in controlled/archival storage, linked through `DATA_AVAILABILITY.md` only after completeness and access checks.

### Repository metadata / automation

After new verified files are staged:

- regenerate `FILE_INDEX.csv` from the actual tree (the current index predates several v360 files);
- regenerate `MANIFEST_SHA256.csv` using the repository convention (manifest does not hash itself);
- add/update source-snapshot and platform-configuration verification records;
- add a current-release CI workflow that exercises the current v360 entry point without changing the frozen analysis base;
- after thesis v365 is frozen, create `THESIS_V365_ALIGNMENT.md` and update final figure/table mirrors as required.

## Security gate

Never commit credentials, API keys, cloud secrets, connection strings, private keys, payment data, shell histories or unredacted sensitive configuration. Historical evidence files with sensitive data stay outside the publishable repository. Use `.PUBLIC` derivatives and record their source hash/provenance.

## Required workflow

1. Inventory exact retained source/config files on the user workstation without uploading their contents.
2. Compare the inventory against this plan and identify recoverable exact files.
3. Secret-scan candidate files before content transfer.
4. Stage safe exact files or clearly labelled `.PUBLIC` derivatives on this branch.
5. Validate imports/config syntax and benchmark-facing route completeness.
6. Regenerate repository index/hash/provenance records.
7. Run analytical and repository regression checks.
8. Review the branch diff; only then open a PR to `main`.

No merge to `main` is permitted merely because a file appears in an old thesis listing; source identity and security must be established first.
