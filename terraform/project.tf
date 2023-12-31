module "project" {
  source          = "altissimo-hq/project/google"
  version         = "1.0.6"
  billing_account = "01CA85-FC3FC5-42D114"
  folder_id       = "175461412505"
  gcloud_command  = "gcloud"
  project_id      = var.project_id
  project_name    = var.project_name

  iam_policy = {
    "roles/appengine.serviceAgent" = [
      "serviceAccount:service-PROJECT_NUMBER@gcp-gae-service.iam.gserviceaccount.com",
    ]
    "roles/cloudbuild.builds.builder" = [
      "serviceAccount:PROJECT_NUMBER@cloudbuild.gserviceaccount.com",
    ]
    "roles/cloudbuild.serviceAgent" = [
      "serviceAccount:service-PROJECT_NUMBER@gcp-sa-cloudbuild.iam.gserviceaccount.com",
    ]
    "roles/containerregistry.ServiceAgent" = [
      "serviceAccount:service-PROJECT_NUMBER@containerregistry.iam.gserviceaccount.com",
    ]
    "roles/editor" = [
      "serviceAccount:altissimo-coxrathvon@appspot.gserviceaccount.com",
    ]
    "roles/firebaserules.system" = [
      "serviceAccount:service-PROJECT_NUMBER@firebase-rules.iam.gserviceaccount.com",
    ]
    "roles/firestore.serviceAgent" = [
      "serviceAccount:service-PROJECT_NUMBER@gcp-sa-firestore.iam.gserviceaccount.com",
    ]
    "roles/pubsub.serviceAgent" = [
      "serviceAccount:service-PROJECT_NUMBER@gcp-sa-pubsub.iam.gserviceaccount.com",
    ]
    "roles/run.serviceAgent" = [
      "serviceAccount:service-PROJECT_NUMBER@serverless-robot-prod.iam.gserviceaccount.com",
    ]
    "roles/secretmanager.secretAccessor" = [
      "serviceAccount:altissimo-coxrathvon@appspot.gserviceaccount.com",
    ]
  }

  services = [
    "appengine.googleapis.com",
    "cloudbuild.googleapis.com",
    # "compute.googleapis.com",
    # "containerregistry.googleapis.com",
    "drive.googleapis.com",
    "firestore.googleapis.com",
    "iam.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    # "oslogin.googleapis.com",
    # "pubsub.googleapis.com",
    "run.googleapis.com",
    "secretmanager.googleapis.com",
    # "storage-api.googleapis.com",
    # "storage-component.googleapis.com",
    "vision.googleapis.com",
  ]
}

output "project_number" {
  value = module.project.project_number
}

output "project_id" {
  value = module.project.project_id
}

output "unmanaged_project_services" {
  value = module.project.unmanaged_project_services
}

output "unmanaged_service_accounts" {
  value = module.project.unmanaged_service_accounts
}