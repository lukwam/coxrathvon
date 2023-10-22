resource "google_app_engine_application" "app" {
  project       = module.project.services["appengine.googleapis.com"].project
  location_id   = var.app_region
  database_type = "CLOUD_FIRESTORE"
}

data "google_app_engine_default_service_account" "default" {
  project = module.project.services["appengine.googleapis.com"].project
}

resource "google_app_engine_domain_mapping" "coxrathvon-com" {
  domain_name = "coxrathvon.com"
  project     = module.project.services["appengine.googleapis.com"].project

  ssl_settings {
    ssl_management_type = "AUTOMATIC"
  }
}

resource "google_app_engine_domain_mapping" "www-coxrathvon-com" {
  domain_name = "www.coxrathvon.com"
  project     = module.project.services["appengine.googleapis.com"].project

  ssl_settings {
    ssl_management_type = "AUTOMATIC"
  }
}
