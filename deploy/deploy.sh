#!/usr/bin/env bash
# Aegis GRC deploy/update script for EC2.
set -Eeuo pipefail

APP_DIR="${APP_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
BRANCH="${BRANCH:-main}"
ENV_FILE="$APP_DIR/backend/.env"
ENV_TEMPLATE="$APP_DIR/backend/.env.production"

echo "==> Aegis deploy started at $(date)"
echo "==> App directory: $APP_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker is not installed or not in PATH."
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "ERROR: docker compose is not available."
  exit 1
fi

cd "$APP_DIR"

if [ ! -f "$ENV_FILE" ]; then
  echo "ERROR: $ENV_FILE not found."
  echo "Create it first. You can start from:"
  echo "  cp $ENV_TEMPLATE $ENV_FILE"
  exit 1
fi

echo "==> Pulling latest code from branch '$BRANCH'..."
git pull origin "$BRANCH"

echo "==> Rebuilding and starting containers..."
docker compose up -d --build --remove-orphans

echo "==> Cleaning unused images..."
docker image prune -f

echo "==> Current container status:"
docker compose ps

echo "==> Deploy complete at $(date)"
