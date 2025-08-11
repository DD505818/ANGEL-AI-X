output "trading_role_arn" {
  description = "ARN of the trading IAM role."
  value       = aws_iam_role.trading_bot.arn
}
