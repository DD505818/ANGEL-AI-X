#!/usr/bin/env bash
set -euo pipefail
if [ -f .env ]; then source .env; fi

: "${NAV:?NAV required}"
: "${MAX_DD:?MAX_DD required}"

risk_max_dd_abs=$(echo "$NAV * $MAX_DD" | bc -l)
risk_max_notional=$(echo "$NAV * 0.10" | bc -l)

angelctl inject \
  risk.max_dd_abs="$risk_max_dd_abs" \
  risk.max_notional="$risk_max_notional" \
  risk.kelly_scalar=0.20
