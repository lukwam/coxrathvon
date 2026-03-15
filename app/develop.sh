#!/usr/bin/env bash
# CoxRathvon - Local Development Script (venv, no Docker)
# Uses Poetry venv for quick iteration with hot reloading.

set -e

cd "$(dirname "$0")/.." || exit

PROJECT_ID="altissimo-coxrathvon"
SERVICE_ACCOUNT_EMAIL="altissimo-coxrathvon@appspot.gserviceaccount.com"

# Service account impersonation (no local key files)
export GOOGLE_CLOUD_PROJECT="${PROJECT_ID}"
export GOOGLE_IMPERSONATE_SERVICE_ACCOUNT="${SERVICE_ACCOUNT_EMAIL}"

# Unset any key file path (we use impersonation instead)
unset GOOGLE_APPLICATION_CREDENTIALS

# Local development flags
export PORT=8080
export FLASK_DEBUG=1

# Activate Poetry venv
if [ -d ".venv" ]; then
    # shellcheck source=/dev/null
    source .venv/bin/activate
else
    echo "No .venv found. Run 'poetry install' first."
    exit 1
fi

echo "🚀 Starting CoxRathvon locally..."
echo "   User: $(gcloud config get account 2>/dev/null)"
echo "   Impersonating: ${SERVICE_ACCOUNT_EMAIL}"
echo "   URL: http://localhost:${PORT}"
echo ""

# Start Flask with hot reload
cd app
python main.py
