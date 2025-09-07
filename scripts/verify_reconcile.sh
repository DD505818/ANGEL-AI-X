#!/usr/bin/env bash
set -euo pipefail
echo "[verify] reconnect → reconcile → diff"
python - <<'PY'
from backend.oms.reconcile import OMSReconciler
class V:
    def __init__(self,name): self.name=name
    def list_open_orders(self): return []
class L:
    def list_open_orders(self): return []
    def mark_cancelled(self,oid,reason): print("cancel",oid,reason)
    def mark_ack(self,oid,vid): print("ack",oid,vid)
class O:
    def replace(self,*a,**k): print("replace",a,k)
r=OMSReconciler([V("binance")], L(), O()).reconcile_all()
print(r)
PY
echo "[ok] reconcile dry run complete"
