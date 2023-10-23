resource "google_storage_bucket" "coxrathvon-data" {
  name          = "coxrathvon-data"
  project       = module.project.project_id
  location      = "US"
  force_destroy = false

  uniform_bucket_level_access = true
}

resource "google_storage_bucket_iam_member" "member" {
  bucket = google_storage_bucket.coxrathvon-data.name
  role   = "roles/storage.admin"
  member = data.google_app_engine_default_service_account.default.member
}
