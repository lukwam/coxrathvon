#!/usr/bin/env bash
# Export Poetry dependencies to requirements.txt for Docker builds.
set -e

cd "$(dirname "$0")/.." || exit

poetry export --without-hashes --format=requirements.txt \
    | grep -E -v "Running command|Resolving dependencies" \
    | sed 's/ $//' > app/requirements.txt

echo "✓ Created app/requirements.txt ($(wc -l < app/requirements.txt) packages)"
