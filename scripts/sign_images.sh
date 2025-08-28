#!/bin/bash
# Sign container images using cosign.
# Usage: ./scripts/sign_images.sh IMAGE[:TAG]

set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: $0 image[:tag]" >&2
  exit 1
fi

IMAGE="$1"
COSIGN_KEY="${COSIGN_KEY:-cosign.key}"

cosign sign --key "$COSIGN_KEY" "$IMAGE"
