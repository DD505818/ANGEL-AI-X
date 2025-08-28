#!/usr/bin/env bash
set -euo pipefail
if [ -f .env ]; then source .env; fi
: "${DASHBOARD_PORT:=7777}"
angelctl dashboard --port "$DASHBOARD_PORT" --theme dark
