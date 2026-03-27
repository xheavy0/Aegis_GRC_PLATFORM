#!/bin/bash
# ═══════════════════════════════════════════════════════
# Aegis GRC Platform — EC2 First-Time Setup Script
# Run this as EC2 User Data (or manually after SSH)
# Ubuntu 22.04 LTS
# ═══════════════════════════════════════════════════════
set -e

echo "▶ Updating system..."
apt-get update -y && apt-get upgrade -y

echo "▶ Installing Docker..."
apt-get install -y ca-certificates curl gnupg git
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  > /etc/apt/sources.list.d/docker.list
apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

echo "▶ Enabling Docker..."
systemctl enable docker
systemctl start docker
usermod -aG docker ubuntu

echo "▶ Cloning repository..."
cd /home/ubuntu
git clone https://github.com/xheavy0/Aegis_GRC_PLATFORM.git aegis
cd aegis

echo "▶ Creating .env from example..."
cp backend/.env.example backend/.env

# Generate random secret key
SECRET=$(openssl rand -hex 32)
sed -i "s/change-this-to-a-random-secret-key-in-production/$SECRET/" backend/.env

echo "▶ Starting application..."
docker compose up -d --build

echo ""
echo "✅ Setup complete!"
echo "   App is running at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo "   Login: admin@aegis.local / Admin@1234"
echo "   Change the default password after first login!"
