provider "aws" {
  region = var.aws_region
}

data "aws_iam_policy_document" "trading_bot_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com", "eks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "trading_bot" {
  name               = var.trading_role_name
  assume_role_policy = data.aws_iam_policy_document.trading_bot_assume.json
}

data "aws_iam_policy_document" "trading_bot_policy" {
  statement {
    sid     = "AllowMarketDataS3"
    actions = ["s3:GetObject", "s3:ListBucket"]
    resources = [
      "arn:aws:s3:::market-data-bucket",
      "arn:aws:s3:::market-data-bucket/*"
    ]
  }
  statement {
    sid       = "AllowCloudWatchLogs"
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "trading_bot_policy" {
  name   = "${var.trading_role_name}-policy"
  role   = aws_iam_role.trading_bot.id
  policy = data.aws_iam_policy_document.trading_bot_policy.json
}
