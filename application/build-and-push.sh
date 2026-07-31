#!/bin/bash
set -e
cd ~/thesis/ecommerce_migrated

echo "================================================================"
echo "PHASE 6.5: BUILDING APPLE-TO-APPLE WSGI IMAGES"
echo "================================================================"

echo ""
echo "=== Pre-flight checks ==="
echo "Docker version: $(docker --version)"
echo "Docker Hub login: $(docker login --get-login 2>/dev/null || echo 'NOT LOGGED IN')"

if false; then
    echo "ERROR: Please run 'docker login' first (use chapkrzgar account)"
    exit 1
fi

echo ""
echo "============================================"
echo "Building chapkrzgar/ecom-apache:2.0"
echo "============================================"

docker build \
    -f Dockerfile.apache-wsgi \
    -t chapkrzgar/ecom-apache:2.0 \
    --progress=plain \
    .

docker images chapkrzgar/ecom-apache:2.0 --format 'Image: {{.Repository}}:{{.Tag}} | Size: {{.Size}}'

echo ""
echo "============================================"
echo "Building chapkrzgar/ecom-nginx:2.0"
echo "============================================"

docker build \
    -f Dockerfile.nginx-uwsgi \
    -t chapkrzgar/ecom-nginx:2.0 \
    --progress=plain \
    .

docker images chapkrzgar/ecom-nginx:2.0 --format 'Image: {{.Repository}}:{{.Tag}} | Size: {{.Size}}'

echo ""
echo "============================================"
echo "Pushing images to Docker Hub"
echo "============================================"

docker push chapkrzgar/ecom-apache:2.0
docker push chapkrzgar/ecom-nginx:2.0

echo ""
echo "============================================"
echo "Final image digests (for thesis documentation)"
echo "============================================"

echo ""
echo "=== chapkrzgar/ecom:2.0 (Django direct) ==="
docker inspect chapkrzgar/ecom:2.0 --format '{{range .RepoDigests}}{{.}}{{end}}'

echo ""
echo "=== chapkrzgar/ecom-apache:2.0 ==="
docker inspect chapkrzgar/ecom-apache:2.0 --format '{{range .RepoDigests}}{{.}}{{end}}'

echo ""
echo "=== chapkrzgar/ecom-nginx:2.0 ==="
docker inspect chapkrzgar/ecom-nginx:2.0 --format '{{range .RepoDigests}}{{.}}{{end}}'

echo ""
echo "================================================================"
echo "PHASE 6.5 BUILD COMPLETE"
echo "================================================================"
