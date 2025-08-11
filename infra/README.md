# Infrastructure

## Terraform Remote State and IAM Roles

Remote state resides in an encrypted S3 bucket with DynamoDB locking to prevent concurrent state writes.

```bash
cd infra/terraform
aws s3api create-bucket --bucket angelai-terraform-state --region us-east-1
aws dynamodb create-table \
  --table-name angelai-terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
terraform init -backend-config="bucket=angelai-terraform-state" \
  -backend-config="region=us-east-1"
terraform plan
```

Environment variables required:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION` (defaults to `us-east-1`)

## Kubernetes Policies

- `k8s/network-policy.yaml` restricts ingress to the monitoring namespace and egress to DNS plus a market data provider subnet.
- `k8s/resource-quota.yaml` caps pods, CPU, and memory in the trading namespace.

Apply with:

```bash
kubectl apply -f k8s/network-policy.yaml
kubectl apply -f k8s/resource-quota.yaml
```

## Autopilot Settings for Low-Latency Trading

Use a GKE Autopilot cluster tuned for deterministic performance:

```bash
gcloud container clusters create-auto trading-autopilot \
  --region=us-east1 \
  --release-channel=rapid \
  --enable-private-nodes \
  --workload-pool=<PROJECT_ID>.svc.id.goog \
  --max-pods-per-node=16
```

Recommendations:
- Prefer regions with direct exchange connectivity.
- Pin minimum CPU platform `Intel Ice Lake` for consistent frequency.
- Export Prometheus metrics and forward to Cloud Monitoring.
