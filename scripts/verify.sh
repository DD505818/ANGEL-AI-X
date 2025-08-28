#!/usr/bin/env bash
set -euo pipefail
angelctl status
angelctl config validate
angelctl health --all
angelctl dryrun trade --symbol BTC-USD --size 1000 || true
