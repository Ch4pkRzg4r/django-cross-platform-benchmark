# Prospective Nginx + uWSGI reproduction recipe (v366)

**Status: prospective public reproduction derivative — not benchmark-time historical proof.**

The retained repository contains a real provenance conflict:

- `configuration/uwsgi.ini` listens on TCP `127.0.0.1:3031` and uses 4 processes × 2 threads;
- `configuration/nginx-uwsgi.conf` forwards to `/run/uwsgi/django.sock`;
- the thesis/current nominal target is 2 processes × 4 threads over a UNIX socket.

Those retained files are preserved unchanged. This directory supplies one internally consistent recipe for a future like-for-like rerun without pretending that it reconstructs the exact historical Nginx/uWSGI runtime.

## Reproduction choices

- Python base: `python:3.12-slim` (same major/minor line as the retained final Linux/container evidence).
- uWSGI: 2 processes × 4 threads = 8 application execution slots.
- Nginx ↔ uWSGI transport: UNIX socket `/run/uwsgi/django.sock`.
- Nginx worker connections: 4096.
- Application source: current reviewed public `application/` tree.
- Secrets/database connectivity: supplied at runtime through environment variables/public-safe configuration; no secret is embedded here.

## Build context

Run from the **repository root**:

```bash
docker build \
  -f configuration/reproduction/nginx-uwsgi-v366/Dockerfile \
  -t thesis-nginx-uwsgi-v366 .
```

The Dockerfile deliberately uses repository-root paths so there is no ambiguity about where `application/`, the prospective `uwsgi.ini`, `nginx.conf` and `application/supervisord.conf` come from.

## Runtime

Provide the same externally required database/environment variables used by the public-safe application configuration, then expose container port 80. For example, adapt the environment block from the public compose/configuration derivatives rather than copying historical credentials.

Before using the image in a new benchmark, verify:

```bash
# inside the running container
uwsgi --version
nginx -V
cat /app/uwsgi.ini
cat /etc/nginx/nginx.conf
```

and confirm that the socket exists and is owned/readable by the expected service user:

```bash
ls -l /run/uwsgi/django.sock
```

## Evidence rule

This recipe resolves **public reproducibility consistency** only. It does not establish which conflicting historical Nginx/uWSGI variant executed in the original campaign. The thesis and configuration evidence map therefore qualify the exact historical socket/worker variant as not established.
