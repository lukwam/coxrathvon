#!/usr/bin/env bash

IMAGE="coxrathvon"
PROJECT_ID="altissimo-coxrathvon"

docker run -it --rm \
    --expose 8080 \
    --name coxrathvon \
    -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/service_account.json \
    -e GOOGLE_CLOUD_PROJECT="${PROJECT_ID}" \
    -e GOOGLE_PROJECT_ID="${PROJECT_ID}" \
    -e PORT=8080 \
    -p 8081:8080 \
    -v "$(pwd):/workspace" \
    -v "$(pwd)/tmp:/tmp" \
    -v "$(pwd)/etc:/secrets" \
    "${IMAGE}"
