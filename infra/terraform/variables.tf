variable "aws_region" {
  description = "AWS region for infrastructure resources."
  type        = string
  default     = "us-east-1"
}

variable "trading_role_name" {
  description = "IAM role assumed by trading workloads."
  type        = string
  default     = "trading-bot-role"
}
