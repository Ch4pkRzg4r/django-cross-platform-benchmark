# Local Inventory v365 — Findings

Inventory run: 2026-09-10  
Purpose: compare retained local source/configuration evidence with the current thesis repository without uploading source contents.

## Inventory result

- Django source tree: 538 files inventoried.
- Phase-7 tree: 996 files inventoried.
- Fly.io deployment directory: 2 files inventoried.
- IIS deployment root `C:\inetpub\thesis-app`: not found at the scanned location; this is not proof that IIS evidence is absent elsewhere.
- Total files inventoried: 1,536.
- Potential-secret flags: 8.
- Scan errors: 0.

No source/configuration file from the local workstation has been committed by this inventory step.

## Strongly supported application-source gaps in current Git

The retained local `ecommerce_migrated` tree contains exact candidate files not present in the current Git application tree, including:

- `commerce/__init__.py`
- `commerce/admin.py`
- `commerce/apps.py`
- `commerce/forms.py`
- `commerce/signals.py`
- `commerce/tests.py`
- migrations `0001` through `0015` plus migrations `__init__.py`
- complete retained `commerce/templates/` candidate tree
- retained `commerce/templatetags/` candidate tree
- `ecommerce/__init__.py`
- `ecommerce/asgi.py`
- `ecommerce/celery.py`
- `ecommerce/gunicorn_conf.py`
- `load_data.py`
- `datadump.json`
- `.dockerignore`
- `.env.example`
- retained source `static/` tree

Many already-published benchmark/application files have local SHA-256 values matching the repository provenance records, including the principal Dockerfiles, `manage.py`, `requirements.txt`, `commerce/models.py`, `commerce/urls.py`, `ecommerce/urls.py`, `ecommerce/wsgi.py`, PostgreSQL configuration, k6 scenarios, orchestrator and parser. This supports the retained tree as a high-value candidate source snapshot, but every newly published file must still pass the source-identity/security gate.

## Files requiring quarantine/sanitisation review before publication

The metadata-only scan flagged eight candidate files. Their contents were not uploaded by the inventory step:

- `.env`
- `ecommerce/settings.py`
- `docker-compose-phase65.yml`
- `commerce/views.py`
- `MIGRATION_GUIDE.md`
- local `README.md`
- `benchmark-k6/scripts/ecommerce_journey.js`
- Fly.io `fly.toml`

A potential-secret flag is conservative and may be a false positive, but none of these files should be copied to Git verbatim until inspected/sanitised. The existing repository already contains safe `.PUBLIC` derivatives for several configuration items.

`commerce/views.py` needs special treatment: the local retained source differs from the repository's redaction-processed copy. The repository provenance record already documents that its public capture suffered a syntax artefact during redaction. A corrected publishable derivative should therefore be made from the verified retained source without exposing credentials and should preserve the original source hash/provenance.

## Deployment-configuration status

- Apache + mod_wsgi: multiple exact/local configuration candidates found; repository already contains core safe config.
- Nginx + uWSGI: multiple exact/local configuration candidates found; repository already contains core safe config.
- Django + Gunicorn: local `ecommerce/gunicorn_conf.py` found; this is a concrete current Git gap because `application/Dockerfile` references it.
- Fly.io: local `fly.toml` found, but it is secret-flagged and must be sanitised before publication.
- Azure Container Apps: no standalone local deployment-definition candidate was identified by filename in the completed inventory.
- Koyeb: no standalone local deployment-definition candidate was identified by filename in the completed inventory.
- IIS + Waitress: the scanned live IIS root was not found; an older `archive/old_configs/web.config` candidate exists inside the Django source snapshot, but it must be treated as historical unless independently tied to the benchmark-time IIS deployment.
- PostgreSQL: retained PostgreSQL configs are present and already represented in Git.
- PgBouncer: no standalone local `pgbouncer.ini` candidate was identified in the completed inventory; the repository currently carries a sanitised runtime extract.

## Data boundary

The phase-7 inventory confirms substantial retained benchmark evidence, including full run-log/Docker-telemetry material outside ordinary Git. The ~73.5 GB original raw JSON/CSV archive remains intentionally outside normal Git history. The current policy remains appropriate: canonical data, compact supplementary carriers and SHA-256 manifests in Git; heavy raw evidence in controlled/archival storage.

## Next gate

Before copying source contents to this branch:

1. inventory the sibling `public_release_stage`, because it may already contain sanitised publishable derivatives;
2. search targeted retained locations for benchmark-time/current configuration evidence for ACA, Koyeb, IIS/Waitress and PgBouncer;
3. package only non-secret candidate contents for inspection;
4. create clearly labelled `.PUBLIC` derivatives for any required secret-bearing file;
5. validate the complete application import/template/migration tree;
6. stage approved files to this branch;
7. regenerate the repository file index and SHA-256 manifest only after the tree is stable.
