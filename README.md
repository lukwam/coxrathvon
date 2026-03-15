# Cox Rathvon (Hex)

The official website of Emily Cox and Henry Rathvon, aka "Hex" — the legendary puzzle constructors behind the Atlantic's cryptic crossword and other beloved word puzzles.

🌐 **[coxrathvon.com](https://coxrathvon.com)**

## Overview

A Flask web application that serves the Cox & Rathvon puzzle archive. Puzzles are stored in Google Cloud Firestore with grid images hosted in Cloud Storage. The site provides browsable, searchable access to puzzles by year, publication, and type.

## Tech Stack

- **Backend:** Python / Flask
- **Database:** Google Cloud Firestore
- **Storage:** Google Cloud Storage (puzzle images, signed URLs)
- **Hosting:** Google App Engine
- **Infrastructure:** Terraform
- **CI/CD:** Google Cloud Build

## Project Structure

```text
├── app/                    # Flask application
│   ├── main.py             # Routes and application logic
│   ├── templates/          # Jinja2 HTML templates
│   ├── style.css           # Styles
│   ├── script.js           # Client-side JavaScript
│   ├── Dockerfile          # Container image definition
│   ├── develop.sh          # Local dev (venv, no Docker)
│   └── develop-container.sh # Local dev (Docker)
├── terraform/              # Infrastructure as code
├── scripts/                # Setup and utility scripts
├── pyproject.toml          # Poetry dependencies & tool config
└── .pre-commit-config.yaml # Code quality hooks
```

## Getting Started

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/)
- [Google Cloud SDK](https://cloud.google.com/sdk)
- Docker (optional, for container development)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/lukwam/coxrathvon.git
   cd coxrathvon
   ```

2. **Configure Google Cloud credentials:**

   ```bash
   ./scripts/gcloud_setup.sh
   ```

3. **Install dependencies:**

   ```bash
   poetry install
   ```

4. **Install pre-commit hooks:**

   ```bash
   pre-commit install
   ```

### Running Locally

**Venv (fast iteration with hot reload):**

```bash
cd app
./develop.sh
```

**Docker (mirrors production):**

```bash
cd app
./develop-container.sh
```

The app will be available at [http://localhost:8080](http://localhost:8080).

## Development Tools

| Tool                                             | Purpose                              |
| ------------------------------------------------ | ------------------------------------ |
| [Ruff](https://docs.astral.sh/ruff/)             | Python linting & formatting          |
| [mypy](https://mypy-lang.org/)                   | Python type checking                 |
| [djlint](https://djlint.com/)                    | Jinja2 template linting              |
| [Prettier](https://prettier.io/)                 | JSON, YAML, CSS, Markdown formatting |
| [ShellCheck](https://www.shellcheck.net/)        | Shell script linting                 |
| [hadolint](https://github.com/hadolint/hadolint) | Dockerfile linting                   |

Run all checks:

```bash
pre-commit run --all-files
```

## Managing Dependencies

```bash
# Add a runtime dependency
poetry add some-package

# Add a dev dependency
poetry add --group dev some-tool

# Regenerate requirements.txt for Docker
poetry export -f requirements.txt --without-hashes -o app/requirements.txt
```

## Deployment

```bash
cd app
./build.sh   # Build and push container image
./deploy.sh  # Deploy to App Engine
```
