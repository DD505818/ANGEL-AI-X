# ANGEL.AI xx – Phase A Baseline

This repository is the **runnable baseline (Phase A)** for ANGEL.AI xx.  
Run `./install.sh` on Ubuntu 22.04 to spin up the full stack (FastAPI backend, Next.js dashboard, PostgreSQL, Redis, Prometheus, Grafana) in Docker.

Sub‑projects:
* **backend/** – FastAPI async trade API
* **frontend/** – Next.js 14 + Tailwind dark‑mode dashboard
* **infra/** – Terraform (GCP) + Kubernetes manifests
* **scripts/** – utility scripts (latency bench, health checks)

All code is type‑hinted, async‑ready, and metrics exposed on `/metrics`.  
Secrets go into `.env.production` (see template provided).

> Phase A delivers the skeleton. Future phases will drop advanced latency core, DeepAgent logic, nightly back‑tests, FPGA feed drivers, etc., without breaking this baseline.  

