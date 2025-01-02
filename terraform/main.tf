terraform {
  required_version = ">= 1.0.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "pl-krywion-tfstate"
    key    = "vpn/terraform.tfstate"
    region = "eu-central-1"
  }
}