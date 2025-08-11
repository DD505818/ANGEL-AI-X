terraform {
  required_version = ">= 1.6.0"
  backend "s3" {
    bucket         = "angelai-terraform-state"
    key            = "global/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "angelai-terraform-locks"
    encrypt        = true
  }
}
