#!/usr/bin/env bash

export BUILDKIT_PROGRESS="plain"

IMAGE="coxrathvon"

# docker build -t "${IMAGE}" .
pack build "${IMAGE}" --builder gcr.io/buildpacks/builder
