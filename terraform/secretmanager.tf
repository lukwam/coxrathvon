# TODO: Remove after app code is deployed without SA key usage.
# Kept temporarily so the currently deployed app still works.
resource "google_secret_manager_secret" "appengine-sa-key" {
  secret_id = "appengine-sa-key"
  project   = module.project.services["secretmanager.googleapis.com"].project

  labels = {
    service = "appengine"
    type    = "service-account-key"
  }

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "appengine-sa-key" {
  secret      = google_secret_manager_secret.appengine-sa-key.id
  secret_data = base64decode(google_service_account_key.appengine.private_key)
}
