#!/usr/bin/env bash
# CoxRathvon - Container Development Script
# Runs the app in Docker using ADC (no service account key file).
# Use this to verify the container works before deploying.

set -e

cd "$(dirname "$0")" || exit

PROJECT_ID="altissimo-coxrathvon"
SERVICE_ACCOUNT_EMAIL="altissimo-coxrathvon@appspot.gserviceaccount.com"
IMAGE="coxrathvon"
PORT=8080

# Build the image
echo "🔨 Building ${IMAGE} image..."
docker build -t "${IMAGE}" .

echo ""
echo "🐳 Starting CoxRathvon in container..."
echo "   Image: ${IMAGE}"
echo "   URL: http://localhost:${PORT}"
echo ""

# Run container with ADC mounted (no service account key file)
docker run -it --rm \
    --name coxrathvon \
    -p "${PORT}:8080" \
    -v "$(pwd):/app" \
    -v "${HOME}/.config/gcloud:/root/.config/gcloud:ro" \
    \
    -e GOOGLE_CLOUD_PROJECT="${PROJECT_ID}" \
    -e GOOGLE_IMPERSONATE_SERVICE_ACCOUNT="${SERVICE_ACCOUNT_EMAIL}" \
    -e PORT=8080 \
    -e PYTHONDONTWRITEBYTECODE=1 \
    \
    "${IMAGE}"
