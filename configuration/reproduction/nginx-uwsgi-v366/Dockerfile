# Prospective v366 public reproduction derivative.
# Build from repository root:
# docker build -f configuration/reproduction/nginx-uwsgi-v366/Dockerfile -t thesis-nginx-uwsgi-v366 .
# This file is NOT benchmark-time provenance.

FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
        nginx \
        supervisor \
        gcc \
        libpq-dev \
        curl \
        build-essential \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY application/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && pip install --no-cache-dir uwsgi==2.0.28

WORKDIR /app
COPY application/ /app/

# Explicit prospective reproduction configs. These two files use the same UNIX socket.
COPY configuration/reproduction/nginx-uwsgi-v366/uwsgi.ini /app/uwsgi.ini
COPY configuration/reproduction/nginx-uwsgi-v366/nginx.conf /etc/nginx/nginx.conf
COPY application/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN python manage.py collectstatic --noinput || true \
    && mkdir -p /run/uwsgi \
    && chown -R www-data:www-data /run/uwsgi /app

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -fsS http://localhost/health/ || exit 1

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

LABEL thesis-reproduction-status="prospective-not-historical-proof" \
      python-version="3.12" \
      wsgi-server="Nginx+uWSGI" \
      wsgi-transport="unix:/run/uwsgi/django.sock" \
      wsgi-config="processes=2 threads=4" \
      document-closure="v366"
