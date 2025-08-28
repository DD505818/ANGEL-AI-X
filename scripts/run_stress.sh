#!/usr/bin/env bash
set -euo pipefail
if [ -f .env ]; then source .env; fi
: "${STRESS_PATHS:=1000000}"
angelctl stress --scenarios=flash_crash,fed_shock,exchange_halt --paths="$STRESS_PATHS"
