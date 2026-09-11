# Dockerfile authority and provenance (v365/v366 closure)

The retained application snapshot contains multiple historical Dockerfiles. They are not equally authoritative for the final Phase-7 Linux/container campaign, and a Dockerfile label is not by itself benchmark-time runtime proof.

## Final container-image evidence

Retained build logs show that the final image family was built from `Dockerfile.v2`, `Dockerfile.apache-wsgi` and `Dockerfile.nginx-uwsgi` against:

`python:3.12-slim@sha256:401f6e1a67dad31a1bd78e9ad22d0ee0a3b52154e6bd30e90be696bb6a3d7461`

The thesis records CPython 3.12.13 for the Linux/container paths and a nominal eight application-execution slots: 2 processes/workers × 4 threads for Apache/mod_wsgi, Nginx/uWSGI and Gunicorn.

`Dockerfile.v2` has the correct `FROM python:3.12-slim` and 2×4 Gunicorn command, but its header/metadata label historically says 3.13. That text is a metadata typo; it does not override the retained build log or base-image identity. `application/Dockerfile` is an earlier/non-controlling variant using Python 3.13 and a 4×2 Gunicorn layout and must not be used as final campaign authority.

## Gunicorn reproduction derivative

`Dockerfile.benchmark.PUBLIC` is a corrected, security-safe Gunicorn reproduction derivative. It pins the observed Python 3.12 base-image digest and records the 2×4 Gunicorn configuration without rewriting historical source files.

## Apache boundary

The Apache historical Dockerfile also uses the Python 3.12 base despite stale 3.13 metadata wording. Its nominal process/thread authority is documented by the retained configuration/build evidence and thesis configuration table, with the normal historical-evidence qualifications stated elsewhere.

## Nginx/uWSGI conflict and v366 reproduction derivative

The retained Nginx/uWSGI files are internally inconsistent if combined literally:

- `configuration/uwsgi.ini` listens on TCP `127.0.0.1:3031` and specifies **4 processes × 2 threads**;
- `configuration/nginx-uwsgi.conf` forwards to UNIX socket `/run/uwsgi/django.sock`;
- `application/supervisord.conf` loads `/app/uwsgi.ini` without an overriding socket argument;
- `application/Dockerfile.nginx-uwsgi` carries stale metadata claiming **2 processes × 4 threads**.

The thesis/current nominal target is 2×4 over a UNIX socket, but an exact benchmark-time 2×4 UNIX-socket uWSGI capture was **not recovered**. Therefore the conflicting historical/current files are preserved unchanged and are not presented as one proven executable benchmark-time chain.

For a clean public rerun, use the explicitly prospective derivative under:

`configuration/reproduction/nginx-uwsgi-v366/`

That recipe uses a single UNIX socket (`/run/uwsgi/django.sock`), 2 uWSGI processes × 4 threads and a repository-root build context. It is a **reproduction recipe**, not retroactive evidence of which historical Nginx/uWSGI variant executed during the campaign.

No numerical benchmark result is changed by this documentation/reproduction closure.
