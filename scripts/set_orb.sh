#!/usr/bin/env bash
set -euo pipefail
if [ -f .env ]; then source .env; fi

: "${ORB_WINDOW:=5m}"
: "${ORB_VOL_GATE:=75}"
: "${ORB_SENTIMENT_GATE:=0.35}"
: "${ATR_PERIOD:=14}"
: "${ATR_REFRESH:=30s}"

angelctl inject \
  orb_window="$ORB_WINDOW" \
  orb_vol_gate="$ORB_VOL_GATE" \
  orb_sentiment_gate="$ORB_SENTIMENT_GATE" \
  atr_period="$ATR_PERIOD" \
  atr_refresh="$ATR_REFRESH"
