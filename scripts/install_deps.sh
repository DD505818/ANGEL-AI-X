#!/usr/bin/env bash
set -euo pipefail

if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update -y
  sudo apt-get install -y jq bc curl ca-certificates
elif command -v yum >/dev/null 2>&1; then
  sudo yum install -y jq bc curl ca-certificates
else
  echo "Unsupported OS: install jq, bc, curl manually." >&2
fi

if ! command -v angelctl >/dev/null 2>&1; then
  echo "angelctl not found. Install per vendor instructions before proceeding." >&2
fi
