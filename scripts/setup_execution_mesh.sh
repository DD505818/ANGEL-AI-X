#!/usr/bin/env bash
set -euo pipefail
if [ -f .env ]; then source .env; fi

: "${VENUE_CRYPTO:=binance,coinbase,kraken,bybit}"
: "${VENUE_EQUITY:=alpaca}"
: "${SLICE_DEFAULT:=THETA_BURST}"
: "${COLO:=NY4}"
: "${FEED:=pcap_mold_udp}"
: "${DRIVER:=ef_vi}"

angelctl inject \
  venue_crypto="$VENUE_CRYPTO" \
  venue_equity="$VENUE_EQUITY" \
  slice_default="$SLICE_DEFAULT" \
  colo="$COLO" \
  feed="$FEED" \
  driver="$DRIVER"
