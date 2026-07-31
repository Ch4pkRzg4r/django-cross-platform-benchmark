# ================================================================
# Django E-commerce Dockerfile - APT-Free Version
# (بێ بەکارهێنانی apt-get لەبەر کێشەی DNS لە WSL2)
# ================================================================

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SETTINGS_MODULE=ecommerce.settings

WORKDIR /app

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install Python packages - uses wheels, no compilation needed
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/media /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true

EXPOSE 8000

CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--threads", "2", \
     "--worker-class", "gthread", \
     "--worker-connections", "1000", \
     "--max-requests", "10000", \
     "--max-requests-jitter", "500", \
     "--timeout", "60", \
     "--graceful-timeout", "30", \
     "--keep-alive", "5", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "--config", "python:ecommerce.gunicorn_conf", \
     "ecommerce.wsgi:application"]
