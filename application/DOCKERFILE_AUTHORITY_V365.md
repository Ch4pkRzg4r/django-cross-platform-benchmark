# Dockerfile authority and provenance (v365)

The retained application snapshot contains multiple historical Dockerfiles. They are not equally authoritative for the final Phase-7 Linux/container campaign.

## Final container-image evidence

Retained build logs show that the final image family was built from `Dockerfile.v2`, `Dockerfile.apache-wsgi` and `Dockerfile.nginx-uwsgi` against:

`python:3.12-slim@sha256:401f6e1a67dad31a1bd78e9ad22d0ee0a3b52154e6bd30e90be696bb6a3d7461`

The final thesis records CPython 3.12.13 for the Linux/container paths and a nominal eight application-execution slots: 2 processes/workers × 4 threads for Apache/mod_wsgi, Nginx/uWSGI and Gunicorn.

`Dockerfile.v2` has the correct `FROM python:3.12-slim` and 2×4 Gunicorn command, but its header and `python-version` label incorrectly say 3.13. That text is a historical metadata typo; it does not override the build log or base-image identity. `application/Dockerfile` is an earlier/non-controlling variant using Python 3.13 and a 4×2 Gunicorn layout and must not be used as the final campaign authority.

## Reproduction derivative

`Dockerfile.benchmark.PUBLIC` is a corrected, security-safe reproduction derivative. It pins the observed Python 3.12 base-image digest and records the 2×4 Gunicorn configuration without rewriting the historical source files.

The Apache and Nginx historical Dockerfiles likewise use the Python 3.12 base despite stale 3.13 metadata labels. Their final process/thread authority comes from the retained configurations/build evidence and thesis configuration table, not those stale labels.

No numerical benchmark result is changed by this documentation/correction layer.
