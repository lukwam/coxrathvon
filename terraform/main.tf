terraform {
  backend "gcs" {
    bucket = "altissimo-coxrathvon-tf"
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.2.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "5.2.0"
    }
  }
}

provider "google" {
  project     = var.project_id
}

provider "google-beta" {
  project     = var.project_id
}

variable "app_region" {
  default = "us-central"
}

variable "project_id" {
  default = "altissimo-coxrathvon"
}

variable "project_name" {
  default = "Altissimo - CoxRathvon"
}
