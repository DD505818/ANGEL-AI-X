#!/usr/bin/env bash
set -euo pipefail
curl -s http://localhost:8000/healthz | grep '"ok": true'
# Risk halt authority
curl -s -X POST http://localhost:8000/v1/risk/kill -H 'Content-Type: application/json' -d '{"enabled":true}' | grep '"enabled": true'
# Order blocked under halt
code=$(curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:8000/v1/order \
  -H 'Content-Type: application/json' -H "X-Idempotency-Key: test-1" \
  -d '{"client_order_id":"abc12345","symbol":"BTC-USD","side":"BUY","qty":0.01}')
test "$code" = "403"
# Idempotency duplicate
curl -s -X POST http://localhost:8000/v1/risk/kill -H 'Content-Type: application/json' -d '{"enabled":false}'
curl -s -X POST http://localhost:8000/v1/order -H 'Content-Type: application/json' -H "X-Idempotency-Key: dup-1" \
  -d '{"client_order_id":"abc12346","symbol":"BTC-USD","side":"BUY","qty":0.01}' | grep '"accepted": true'
code=$(curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:8000/v1/order \
  -H 'Content-Type: application/json' -H "X-Idempotency-Key: dup-1" \
  -d '{"client_order_id":"abc12346","symbol":"BTC-USD","side":"BUY","qty":0.01}')
test "$code" = "409"
echo "ACCEPTANCE OK"
