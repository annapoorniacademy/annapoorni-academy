# Annapoorni Academy V1.0 — Production Deployment Guide

This guide details how to deploy the **React/Vite Frontend on Netlify** and the **Flask/PyMySQL Backend on a cloud provider (Render, Railway, AWS, Docker Compose, or VPS)**.

---

## 1. Environment Variable Reference

### Backend Production Environment Variables

| Variable Name | Required / Optional | Default (Local Dev) | Description |
| :--- | :--- | :--- | :--- |
| `FLASK_ENV` | Required | `development` | Set to `production` for live deployments. |
| `PORT` | Optional | `5000` | Port provided by hosting provider (e.g. Render/Railway). |
| `SECRET_KEY` | Required | Default fallback | Flask session secret key. Generate a random secret string. |
| `JWT_SECRET_KEY` | Required | Default fallback | JWT signature key for Admin authentication tokens. |
| `JWT_ACCESS_TOKEN_EXPIRES_DAYS` | Optional | `7` | Number of days until JWT admin token expires. |
| `DATABASE_URL` | Required for MySQL | `sqlite:///annapoorni.db` | Production MySQL connection string (PyMySQL driver format: `mysql+pymysql://user:pass@host:3306/dbname`). Automatically converts `mysql://` to `mysql+pymysql://`. |
| `FRONTEND_URL` | Required | `http://localhost:5173` | Deployed Netlify frontend URL (e.g. `https://your-site-name.netlify.app`). Used for strict CORS origin permission. |
| `UPLOAD_FOLDER` | Optional | `uploads` | Path to file uploads directory (e.g. `/tmp/uploads` or persistent storage mount). |
| `MAX_CONTENT_LENGTH` | Optional | `10485760` (10MB) | Maximum file upload size limit in bytes. |
| `ADMIN_USERNAME` | Optional | `admin` | Username for initial admin account seeding. |
| `ADMIN_EMAIL` | Optional | `annapoorniacademy@gmail.com` | Email for initial admin account seeding. |
| `ADMIN_PASSWORD` | Optional | `$12345678` | Password for initial admin account seeding. |
| `MAIL_SERVER` | Optional | `smtp.gmail.com` | SMTP server host for email dispatch. |
| `MAIL_PORT` | Optional | `587` | SMTP server port. |
| `MAIL_USERNAME` | Optional | `annapoorniacademy@gmail.com` | SMTP sender email username. |
| `MAIL_PASSWORD` | Optional | `""` | Google App Password (16 characters, 2FA enabled). |

---

### Netlify Frontend Environment Variables

| Variable Name | Required / Optional | Description |
| :--- | :--- | :--- |
| `VITE_API_BASE_URL` | Required on Netlify | The live URL of your deployed Flask backend API (e.g. `https://annapoorni-api.onrender.com`). |

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
