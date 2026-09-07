# Annapoorni Academy V2.0 — Production Deployment Guide

This guide details how to deploy **Annapoorni Academy V2.0** on **Google Cloud Run** with **Cloud Firestore** and **Gmail SMTP Automation**.

> For the comprehensive production runbook, cost analysis, and DNS setup, see [DEPLOYMENT_V2.md](file:///c:/Shino/sindhu/ai/docs/DEPLOYMENT_V2.md).

---

## 1. Environment Variable Reference

### Production Environment Variables

| Variable Name | Required / Optional | Default (Local Dev) | Description |
| :--- | :--- | :--- | :--- |
| `FLASK_ENV` | Required | `development` | Set to `production` for live deployments. |
| `PORT` | Optional | `8080` | Port automatically assigned by Cloud Run (`8080`). |
| `SECRET_KEY` | Required | Default fallback | Flask session secret key. Generate a random secret string. |
| `JWT_SECRET_KEY` | Required | Default fallback | JWT signature key for Admin authentication tokens. |
| `JWT_ACCESS_TOKEN_EXPIRES_DAYS` | Optional | `7` | Number of days until JWT admin token expires. |
| `DATABASE_URL` | Optional | `sqlite:///annapoorni.db` | Local/fallback database URL (in production, Cloud Firestore / native mode is used). |
| `FRONTEND_URL` | Optional | `https://annapoorniacademy.com` | Production frontend domain for CORS origin permission. |
| `ADMIN_USERNAME` | Optional | `admin` | Username for initial admin account seeding. |
| `ADMIN_EMAIL` | Optional | `coach.sindhuram@gmail.com` | Email for initial admin account seeding. |
| `ADMIN_PASSWORD` | Optional | `$12345678` | Password for initial admin account seeding. |
| `MAIL_SERVER` | Optional | `smtp.gmail.com` | SMTP server host for Gmail dispatch. |
| `MAIL_PORT` | Optional | `587` | SMTP server port (587 for STARTTLS). |
| `MAIL_USE_TLS` | Optional | `true` | Enable STARTTLS security. |
| `MAIL_USERNAME` | Optional | `coach.sindhuram@gmail.com` | SMTP sender email username. |
| `MAIL_FROM` | Optional | `coach.sindhuram@gmail.com` | Default FROM address. |
| `MAIL_PASSWORD` | Optional | `""` | Google App Password (16 characters, 2FA enabled, stored securely via Secret Manager). |

---

## 2. Production Start & Entrypoint Commands

- **WSGI Production Server Command (Gunicorn)**:
  ```bash
  gunicorn --bind 0.0.0.0:$PORT app:app
  ```
- **Direct Flask Command (Development/Container Standalone)**:
  ```bash
  python app.py
  ```

---

## 3. Database Initialization & Seeding

The application automatically creates all required database tables (`db.create_all()`) and seeds default content & admin credentials (`seed_database()`) on initial backend startup.

If you prefer to initialize MySQL tables manually using SQL files:
```bash
mysql -u <db_user> -p <db_name> < database/schema.sql
mysql -u <db_user> -p <db_name> < database/seed.sql
```

---

## 4. Docker Compose Setup (Local or Self-Hosted Production)

```bash
# 1. Clone repository
git clone https://github.com/shinoansonanand-netizen/annapoorni-academy.git
cd annapoorni-academy

# 2. Copy environment template
cp .env.example .env

# 3. Build & start full container stack
docker-compose up -d --build
```
