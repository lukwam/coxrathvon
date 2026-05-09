# Allow the App Engine default SA to sign blobs (for GCS signed URLs)
# without requiring a stored service account key.
resource "google_project_iam_member" "appengine-token-creator" {
  project = var.project_id
  role    = "roles/iam.serviceAccountTokenCreator"
  member  = data.google_app_engine_default_service_account.default.member
}

# TODO: Remove after app code is deployed without SA key usage.
# Kept temporarily so the currently deployed app still works.
resource "google_service_account_key" "appengine" {
  service_account_id = data.google_app_engine_default_service_account.default.id
}
