# TODO: Remove after app code is deployed without SA key usage.
# Kept temporarily so the currently deployed app still works.
resource "google_service_account_key" "appengine" {
  service_account_id = data.google_app_engine_default_service_account.default.id
}
