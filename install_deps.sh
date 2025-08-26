#!/usr/bin/env bash
set -euo pipefail

PKGS=(jq bc curl ca-certificates)

if ! command -v apt-get >/dev/null 2>&1; then
  echo "[install_deps] apt-get not available" >&2
  exit 1
fi

echo "[install_deps] updating package index"
apt-get update -y

for pkg in "${PKGS[@]}"; do
  if ! dpkg -s "$pkg" >/dev/null 2>&1; then
    echo "[install_deps] installing $pkg"
    apt-get install -y "$pkg"
  else
    echo "[install_deps] $pkg already present"
  fi
done

echo "[install_deps] dependencies installed"
