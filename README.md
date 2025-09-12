# ANGEL.AI v10.0 — Deployment Bundle

This bundle automates deployment of governance/reg adapters, swarm agents, ORB parameters,
risk/Kelly limits, execution mesh, compounding daemon, dashboard, stress tests, and validation.

## Prerequisites
- Linux host (Ubuntu 20.04+ or Amazon Linux 2 recommended)
- `angelctl` installed and authenticated to your environment
- Network access to NATS, Redis, and exchanges
- `jq`, `bc`, `curl`, and `git` installed (or run `scripts/install_deps.sh`)
- Populate `.env` from `.env.example`

## Quick Start
```bash
cp .env.example .env
# Edit .env with real values (NATS/Redis URLs, keys, NAV, MAX_DD)

source .env
scripts/install_deps.sh
scripts/configure.sh
scripts/deploy_governance.sh
scripts/setup_swarm.sh
scripts/set_orb.sh
scripts/set_risk_kelly.sh
scripts/setup_execution_mesh.sh
scripts/start_dashboard.sh &
scripts/run_compounder.sh &
scripts/run_stress.sh

# Validate & snapshot
scripts/verify.sh
angelctl snapshot create v10.0-pre
```

## Rollback
```bash
scripts/rollback.sh
```

## Contents
- `scripts/`: executable deployment scripts
- `config/controlplane.schema.json`: control-plane envelope schema
- `k8s/agent-deployment.yaml`: example Kubernetes deployment
- `.env.example`: environment template
- `README.md`: this file

## Strategy Evaluation
```bash
make bootstrap
make eval24
make decide
```
`make eval24` runs a 24-hour backtest with Monte Carlo for each config and `make decide` prints the best setup by profit and drawdown.

## Testing
```bash
make test
```
Run the FastAPI and trading unit tests.
