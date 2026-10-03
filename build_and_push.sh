#!/usr/bin/env bash
# Build the Docker image and push it to Google Artifact Registry.
set -euo pipefail

IMAGE="europe-west4-docker.pkg.dev/steady-scope-344316/thegcwedding-artifactory/app"
TAG="${1:-latest}"

cd "$(dirname "$0")"

docker build -t "${IMAGE}:${TAG}" .
docker push "${IMAGE}:${TAG}"
