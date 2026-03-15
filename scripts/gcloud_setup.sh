#!/usr/bin/env bash
# Setup script for the CoxRathvon gcloud environment.
# Safe to run repeatedly — only opens browser when necessary.

CONFIGURATION="default"
PROJECT="altissimo-coxrathvon"
ACCOUNT="${COXRATHVON_ACCOUNT:-karlsson@altissimo.io}"

set -e

# ── 1. gcloud configuration ──────────────────────────────────────────────────
echo "Activating [$CONFIGURATION] gcloud configuration..."
gcloud config configurations activate "$CONFIGURATION"
gcloud config set project "$PROJECT" --quiet
gcloud config set account "$ACCOUNT" --quiet

# ── 2. gcloud auth (CLI) ─────────────────────────────────────────────────────
# Check if the active account has a valid token; if not, re-login.
if ! gcloud auth print-access-token &>/dev/null; then
    echo "gcloud credentials missing or expired. Logging in..."
    gcloud auth login --account="$ACCOUNT"
fi

# ── 3. Application Default Credentials ───────────────────────────────────────
echo "Setting Application Default Credentials..."
gcloud auth application-default login -q

echo "Setting the gcloud Application Default Credentials quota project to: ${PROJECT}"
gcloud auth application-default set-quota-project "${PROJECT}"

echo ""
echo "✓ CoxRathvon environment ready"
echo "  Account: $(gcloud config get account 2>/dev/null)"
echo "  Project: $(gcloud config get project 2>/dev/null)"
