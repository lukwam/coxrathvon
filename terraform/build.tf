module "cloudbuildv2-connection" {
  source  = "altissimo-hq/cloudbuildv2-connection/google"
  version = "1.0.3"

  github_app_installation_id = 267250
  github_login               = "lukwam"
  project                    = var.project_id
  region                     = "us-central1"

  oauth_token_secret = "github-terraform-token"
  secret_project     = "lukwam-dev"

  repositories = [
    "coxrathvon",
  ]
}

resource "google_cloudbuild_trigger" "deploy-app" {
  provider    = google-beta
  name        = "deploy-app"
  description = "Deploy CoxRathvon App to App Engine"
  location    = "us-central1"
  project     = var.project_id

  include_build_logs = "INCLUDE_BUILD_LOGS_WITH_STATUS"

  included_files = [
    "app/**",
  ]

  repository_event_config {
    repository = module.cloudbuildv2-connection.repository_ids["coxrathvon"]
    push {
      branch = "main"
    }
  }

  build {
    step {
      name       = "gcr.io/google.com/cloudsdktool/cloud-sdk:slim"
      dir        = "app"
      entrypoint = "gcloud"
      args = [
        "app",
        "deploy",
        "--project=$PROJECT_ID",
        "--quiet",
      ]
    }
  }
}
