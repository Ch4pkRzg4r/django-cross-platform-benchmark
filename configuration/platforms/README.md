# Seven-platform configuration evidence map

This directory maps the configuration evidence for all seven evaluated deployment paths. It distinguishes **exact/sanitised retained configuration**, **current-state evidence**, and **bounded metadata** so that later readers do not mistake a reconstructed recipe for benchmark-time proof.

| ID | Platform | Repository configuration/evidence | Evidence status |
|---|---|---|---|
| 01 | Apache + mod_wsgi | `application/Dockerfile.apache-wsgi`, `configuration/apache-mod_wsgi.conf`, `configuration/docker/apache.conf`, `configuration/docker-compose-phase65.PUBLIC.yml` | Strong retained Linux/REV6 configuration; final 2 processes × 4 threads and 2 vCPU/2 GiB scope documented. Historical Dockerfile metadata label saying Python 3.13 is stale; actual base/build evidence is Python 3.12. |
| 02 | Nginx + uWSGI | `application/Dockerfile.nginx-uwsgi`, `configuration/nginx-uwsgi.conf`, `configuration/uwsgi.ini`, `application/supervisord.conf`, `configuration/docker/nginx.conf`, compose derivative | Strong retained Linux/REV6 configuration; 2 processes × 4 threads, 2 vCPU/2 GiB. Historical metadata label issue is bounded as above. |
| 03 | Django + Gunicorn | `application/Dockerfile.v2`, `application/Dockerfile.benchmark.PUBLIC`, `application/ecommerce/gunicorn_conf.py`, compose derivative | Strong retained Linux/REV6 configuration; 2 workers × 4 threads. `Dockerfile.benchmark.PUBLIC` is the corrected reproduction derivative; see `application/DOCKERFILE_AUTHORITY_V365.md`. |
| 04 | Azure Container Apps | `configuration/platforms.PUBLIC.json` plus thesis/repository evidence notes | **Bounded**. Current REV6 allocation is recorded as 2 vCPU / 4 GiB in Germany West Central with scale-to-zero. No exact benchmark-time ACA YAML/Bicep/provider export was recovered; none is fabricated here. |
| 05 | Koyeb | `configuration/platforms.PUBLIC.json` plus thesis/repository evidence notes | **Bounded**. Current service state is recorded as 2 vCPU / 2 GB, Frankfurt, scale-to-zero. No exact benchmark-time Koyeb service export was recovered; none is fabricated here. |
| 06 | Fly.io | `06_flyio/fly.PUBLIC.toml` + `FLY_PUBLIC_PROVENANCE.md` | Sanitised derivative of the retained local `fly.toml`; source SHA-256 and redaction boundary are recorded. Current/recovered config is shared-cpu-2x, 2048 MiB, `fra`, min machines 0. |
| 07 | IIS + Waitress | `07_iis_waitress/web.config.PUBLIC.xml`, `apply-memory-limit.ps1`, `environment/iis_waitress/` | Safe retained Windows evidence. REV5 boundary is explicit; Waitress 3.0.1 / CPython 3.12.7 and 8-thread configuration are documented, with the IIS memory-limit verification limitation retained. |

## Shared data tier

The final study uses PostgreSQL 17 with PgBouncer transaction pooling. Relevant publishable evidence is in `application/postgres/`, `environment/pgbouncer_runtime_extract.PUBLIC.txt`, and `configuration/docker-compose-phase65.PUBLIC.yml`.

## Evidence rule

A file is not promoted to “benchmark-time exact” merely because it is plausible or because a later provider state looks similar. ACA and Koyeb therefore remain explicitly evidence-bounded. This is a reproducibility-strengthening choice, not a missing-data fabrication opportunity.
