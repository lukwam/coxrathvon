---
description: Steps to run before committing changes to ensure everything is in order
---

# Pre-Commit Checklist

Before committing changes, always follow these steps:

## 1. If `pyproject.toml` dependencies changed

If any dependencies were added, removed, or updated in `pyproject.toml`:

```bash
# turbo
poetry lock
```

```bash
# turbo
poetry install
```

## 2. If `app/` files changed

If any files under `app/` were modified (code, templates, styles, etc.):

- Bump the version in `pyproject.toml` using semantic versioning:
  - **Patch** (1.0.x): bug fixes, minor styling tweaks
  - **Minor** (1.x.0): new features, new routes, significant UI changes
  - **Major** (x.0.0): breaking changes, major rewrites

```bash
# turbo
poetry version patch  # or minor/major as appropriate
```

## 3. Regenerate requirements.txt

// turbo

```bash
./scripts/create_requirements.sh
```

## 4. Run tests

// turbo

```bash
poetry run pytest tests/ -v
```

## 5. Run pre-commit checks

// turbo

```bash
pre-commit run -a
```

## 6. Stage and review

```bash
git add -u
git status .
```

Review the staged changes before committing.
