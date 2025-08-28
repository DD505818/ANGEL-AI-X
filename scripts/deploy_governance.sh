#!/usr/bin/env bash
set -euo pipefail
angelctl deploy \
  --reg_adapter=SEC_CAT,FINRA_OATS,ESMA_MIFID \
  --ethics_engine=true \
  --audit_stream=worm://reg-feed

angelctl audit ping --stream worm://reg-feed
angelctl policy ls || true
