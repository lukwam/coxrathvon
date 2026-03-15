---
description: How to deploy the CoxRathvon app to App Engine
---

# Deploying to App Engine

## Prerequisites

- Ensure all pre-commit checks pass (`/pre-commit`)
- Ensure all tests pass
- Ensure `app/requirements.txt` is up to date

## Deploy

```bash
cd app && gcloud app deploy --project=altissimo-coxrathvon
```

## Verify

After deploying, verify the app is running at:
<https://altissimo-coxrathvon.appspot.com>
