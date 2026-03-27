#!/bin/bash
# ═══════════════════════════════════════════════════════
# Aegis GRC — Deploy / Update script (run on EC2)
# Called by GitHub Actions on every push to main
# ═══════════════════════════════════════════════════════
set -e

APP_DIR="/home/ubuntu/aegis"

echo "▶ Pulling latest code..."
cd "$APP_DIR"
git pull origin main

echo "▶ Rebuilding containers..."
docker compose up -d --build --remove-orphans

echo "▶ Removing unused images..."
docker image prune -f

echo "✅ Deploy complete — $(date)"
