#!/usr/bin/env bash
set -euo pipefail
if [ -f .env ]; then source .env; fi

: "${NATS_URL:?NATS_URL required}"
: "${REDIS_URL:?REDIS_URL required}"
: "${AGENT_ID:?AGENT_ID required}"
: "${ED25519_PUBKEY:?ED25519_PUBKEY required}"
: "${REDIS_STREAM_GROUP:?REDIS_STREAM_GROUP required}"
: "${REDIS_CONSUMER_NAME:?REDIS_CONSUMER_NAME required}"

echo "$NATS_URL" | grep -Eq '^nats(s)?://' || { echo "Invalid NATS_URL"; exit 1; }
echo "$REDIS_URL" | grep -Eq '^redis(s)?://' || { echo "Invalid REDIS_URL"; exit 1; }

if [ ${#ED25519_PUBKEY} -lt 32 ]; then
  echo "ED25519_PUBKEY appears too short"; exit 1
fi

angelctl status || { echo "angelctl status failed"; exit 1; }
angelctl config validate || { echo "config validate failed"; exit 1; }

echo "Configuration checks passed."
