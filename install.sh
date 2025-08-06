#!/usr/bin/env bash
set -euo pipefail
echo "[ANGEL.AI] Installing Docker if absent..."
if ! command -v docker &>/dev/null; then
  curl -fsSL https://get.docker.com | sh
fi
if ! command -v docker-compose &>/dev/null; then
  apt-get update && apt-get install -y docker-compose
fi
echo "[ANGEL.AI] Launching stack..."
docker-compose pull
docker-compose up -d --build
echo "[ANGEL.AI] Stack is starting – check http://localhost:3000 for UI, http://localhost:9090 for Prometheus, http://localhost:3001/docs for API."
