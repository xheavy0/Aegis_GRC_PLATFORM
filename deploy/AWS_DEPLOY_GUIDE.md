# Aegis GRC — AWS EC2 Deployment Guide

## ნაბიჯი 1: EC2 Instance შექმნა

1. გადადი AWS Console → EC2 → **Launch Instance**
2. **Name:** `aegis-grc`
3. **AMI:** Ubuntu Server 22.04 LTS (Free tier eligible)
4. **Instance type:** `t2.micro` (Free Tier) ან `t3.small` (სწრაფი)
5. **Key pair:** შექმენი ახალი → ჩამოტვირთე `.pem` ფაილი
6. **Security Group — დაამატე ეს rules:**

| Type  | Port | Source    |
|-------|------|-----------|
| SSH   | 22   | My IP     |
| HTTP  | 80   | 0.0.0.0/0 |
| HTTPS | 443  | 0.0.0.0/0 |

7. **Storage:** 20 GB (default 8 GB-ის ნაცვლად)
8. **Advanced Details → User data** → ჩასვი `ec2-setup.sh`-ის შინაარსი
9. **Launch Instance**

---

## ნაბიჯი 2: Elastic IP (სტაბილური IP მისამართი)

1. EC2 → **Elastic IPs** → **Allocate Elastic IP**
2. **Associate** → აირჩიე შენი instance
3. ეს IP არ შეიცვლება instance გათიშვის შემდეგ

---

## ნაბიჯი 3: GitHub Actions Secrets

GitHub-ზე: **Settings → Secrets → Actions → New repository secret**

| Secret Name  | Value                           |
|--------------|---------------------------------|
| `EC2_HOST`   | Elastic IP მისამართი            |
| `EC2_SSH_KEY`| `.pem` ფაილის სრული შინაარსი   |

---

## ნაბიჯი 4: SSH-ით დაკავშირება (პირველად)

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_ELASTIC_IP
```

Setup script ავტომატურად გაეშვება User Data-ს სახით.
თუ ხელით გინდა გაშვება:

```bash
curl -O https://raw.githubusercontent.com/xheavy0/Aegis_GRC_PLATFORM/main/deploy/ec2-setup.sh
chmod +x ec2-setup.sh
sudo ./ec2-setup.sh
```

---

## ნაბიჯი 5: .env კონფიგურაცია

```bash
cd /home/ubuntu/aegis
nano backend/.env
```

შეცვალე:
- `SECRET_KEY` — გამოყენება: `openssl rand -hex 32`
- `FIRST_ADMIN_PASSWORD` — ძლიერი პაროლი
- `DATABASE_URL` — პაროლი შეცვალე

```bash
docker compose up -d --build
```

---

## შედეგი

```
http://YOUR_ELASTIC_IP      → Aegis GRC Platform
http://YOUR_ELASTIC_IP/api/docs  → API Documentation
```

---

## Auto-Deploy (GitHub Actions)

ახლიდან ყოველი `git push origin main` ავტომატურად განაახლებს EC2-ზე!

```
push → GitHub Actions → SSH → docker compose up --build
```

---

## ფასი (AWS)

| სერვისი | ფასი |
|---------|------|
| t2.micro (Free Tier, 1 წელი) | $0 |
| t2.micro (ამის შემდეგ) | ~$9/თვე |
| t3.small | ~$15/თვე |
| Elastic IP (instance-თან) | $0 |
| Storage 20GB | ~$2/თვე |
