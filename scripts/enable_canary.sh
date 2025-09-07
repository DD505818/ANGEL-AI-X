#!/usr/bin/env bash
set -euo pipefail
NS=${1:-angel}
echo "[canary] applying netpol/pdb/hpa and helm values"
kubectl -n "$NS" apply -f deploy/k8s/networkpolicy-backend.yaml
kubectl -n "$NS" apply -f deploy/k8s/pdb-backend.yaml
kubectl -n "$NS" apply -f deploy/k8s/hpa-backend.yaml
helm upgrade --install angel charts/angel -n "$NS" -f deploy/helm/values-canary.yaml
echo "[canary] done"
