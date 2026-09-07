# Annapoorni Academy V2.0 — Production Deployment & Google Cloud Run Runbook

> **Target Production Domain:** `annapoorniacademy.com`  
> **Infrastructure Model:** Ultra-Low-Cost Single-Domain Container on **Google Cloud Run** + **Firestore (Free Tier)** + **Cloud Storage (Free Tier)**  
> **Target Cloud Cost:** Approaching **₹0/month** within Google Cloud Free Quotas for low-to-medium traffic.

---

## 1. Architecture Overview

```
                      [ annapoorniacademy.com ]
                                  │
                                  ▼
           [ Google Cloud Managed DNS / SSL Certificate ]
                                  │
                                  ▼
 ┌─────────────────────────────────────────────────────────────────┐
 │               Google Cloud Run (Scale-To-Zero)                  │
 │                                                                 │
 │   ┌───────────────────────────┐   ┌─────────────────────────┐   │
 │   │   React 18 SPA Frontend   │   │     Flask REST API      │   │
 │   │   Vite Minified Assets    │   │    Python 3.11/Gunicorn │   │
 │   │   Dynamic Theme / Styles  │   │  Auth, Routes, Health   │   │
 │   └───────────────────────────┘   └─────────────────────────┘   │
 └────────────────────────────────┬─────────────────┬──────────────┘
                                  │                 │
                                  ▼                 ▼
                     [ Google Cloud Firestore ]  [ Cloud Storage ]
                       1 GiB Free Tier Storage     5 GiB Free Tier
                       50,000 Reads/Day Free      Optimized WebP
```

- **Single Domain Experience:** The React SPA and Flask REST API are bundled and served from the same Cloud Run service. All frontend requests use relative paths (`/api/...`), completely eliminating CORS complexity and hardcoded hostnames.
- **Scale-to-Zero (`min-instances=0`):** When there is no active traffic, Cloud Run scales to 0 instances, incurring 0 compute charges.

---

## 2. Google Cloud Free Tier Allowances & Cost Breakdown

| Resource | Monthly Free Allowance | Academy Estimated Usage | Expected Cost |
| :--- | :--- | :--- | :--- |
| **Cloud Run** | 2 Million requests/month, 360,000 GB-seconds memory, 180,000 vCPU-seconds | ~5,000 – 50,000 requests/month | **₹0.00** |
| **Cloud Firestore** | 1 GiB storage, 50,000 document reads/day, 20,000 writes/day, 20,000 deletes/day | < 50 MB data, ~500 reads/day | **₹0.00** |
| **Cloud Storage** | 5 GB-months standard storage, 5,000 Class A operations, 50,000 Class B operations | < 1 GB media assets | **₹0.00** |
| **Network Egress** | 100 GiB/month outbound data transfer to North America/global standard | < 5 GiB/month | **₹0.00** |
| **SSL / HTTPS** | Google-managed automatic SSL certificates for custom domains | Included free with Cloud Run | **₹0.00** |
| **Custom Domain** | Annual domain registration at registrar (GoDaddy, Namecheap, Google, etc.) | 1 domain | **~₹800 – ₹1,200 / year** (Paid to registrar) |

---

## 3. Step-by-Step Google Cloud Deployment Guide

### Prerequisites
1. A Google Cloud account ([console.cloud.google.com](https://console.cloud.google.com/)).
2. Google Cloud SDK (`gcloud` CLI) installed on your local machine:
   ```bash
   gcloud version
   ```
3. Authenticate with your Google account:
   ```bash
   gcloud auth login
   ```

---

### Step 3.1: Create Google Cloud Project & Set Defaults

```bash
# 1. Create a new project (or use existing)
gcloud projects create annapoorni-academy-prod --name="Annapoorni Academy"

# 2. Set default project
gcloud config set project annapoorni-academy-prod

# 3. Link your billing account to the project (required by GCP to enable APIs, even in free tier)
# List billing accounts:
gcloud billing accounts list
# Link billing account:
gcloud billing projects link annapoorni-academy-prod --billing-account=YOUR_BILLING_ACCOUNT_ID

# 4. Enable required Google Cloud APIs
gcloud services enable \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    firestore.googleapis.com \
    storage.googleapis.com
```

---

### Step 3.2: Initialize Google Cloud Firestore (Free Tier)

```bash
# Initialize Firestore in Native mode in your preferred region (e.g. asia-south1 for India or us-central1)
gcloud firestore databases create --location=asia-south1 --type=firestore-native
```

---

### Step 3.3: Create Cloud Storage Bucket for Media (Optional)

```bash
# Create standard storage bucket
gcloud storage buckets create gs://annapoorni-academy-media --location=asia-south1 --default-storage-class=STANDARD

# Make bucket publicly readable for website images
gcloud storage buckets add-iam-policy-binding gs://annapoorni-academy-media \
    --member=allUsers \
    --role=roles/storage.objectViewer
```

---

### Step 3.4: Build and Deploy Container to Cloud Run

```bash
# 1. Build and push image using Google Cloud Build
gcloud builds submit --tag gcr.io/annapoorni-academy-prod/annapoorni-web:v2.0

# 2. Deploy single-domain container to Cloud Run with scale-to-zero settings
gcloud run deploy annapoorni-web \
    --image gcr.io/annapoorni-academy-prod/annapoorni-web:v2.0 \
    --platform managed \
    --region asia-south1 \
    --allow-unauthenticated \
    --min-instances 0 \
    --max-instances 2 \
    --concurrency 80 \
    --memory 512Mi \
    --cpu 1 \
    --timeout 60 \
    --set-env-vars "\
FLASK_ENV=production,\
PORT=8080,\
SECRET_KEY=$(openssl rand -hex 24),\
JWT_SECRET_KEY=$(openssl rand -hex 24),\
GOOGLE_CLOUD_PROJECT=annapoorni-academy-prod,\
FIRESTORE_PROJECT_ID=annapoorni-academy-prod,\
DB_TYPE=firestore,\
STORAGE_BUCKET=annapoorni-academy-media,\
ADMIN_USERNAME=admin,\
ADMIN_EMAIL=annapoorniacademy@gmail.com,\
ADMIN_PASSWORD=YOUR_STRONG_ADMIN_PASSWORD,\
FRONTEND_URL=https://annapoorniacademy.com"
```

---

### Step 3.5: Migrate Existing Data to Firestore

Run the automated migration tool to populate all courses, subjects, lessons, quizzes, settings, and announcements into Firestore:

```bash
python scripts/migrate_to_firestore.py --project annapoorni-academy-prod
```

---

### Step 3.6: Map Custom Domain (`annapoorniacademy.com`)

```bash
# 1. Map custom domain to your Cloud Run service
gcloud beta run domain-mappings create \
    --service annapoorni-web \
    --domain annapoorniacademy.com \
    --region asia-south1

# Optional: Map www subdomain
gcloud beta run domain-mappings create \
    --service annapoorni-web \
    --domain www.annapoorniacademy.com \
    --region asia-south1
```

---

## 4. DNS Configuration at Domain Registrar

Log into your domain registrar (GoDaddy, Namecheap, Google Domains, Hostinger, etc.) and configure the following DNS records:

| Record Type | Name / Host | Value / Target | TTL |
| :--- | :--- | :--- | :--- |
| **A** | `@` | `216.239.32.21` | 3600 |
| **A** | `@` | `216.239.34.21` | 3600 |
| **A** | `@` | `216.239.36.21` | 3600 |
| **A** | `@` | `216.239.38.21` | 3600 |
| **AAAA** | `@` | `2001:4860:4802:32::15` | 3600 |
| **AAAA** | `@` | `2001:4860:4802:34::15` | 3600 |
| **AAAA** | `@` | `2001:4860:4802:36::15` | 3600 |
| **AAAA** | `@` | `2001:4860:4802:38::15` | 3600 |
| **CNAME** | `www` | `ghs.googlehosted.com.` | 3600 |

> [!NOTE]
> Google Cloud automatically provisions a **managed SSL / HTTPS certificate** for `annapoorniacademy.com` once the DNS records propagate (typically within 15–60 minutes).

---

## 5. Billing Safety & Budget Alerts (Prevent Unexpected Costs)

To guarantee that costs remain near ₹0 and protect against unintended spikes:

1. **Set up a Budget Alert ($0 to $5)**:
   - In Google Cloud Console, navigate to **Billing** → **Budgets & Alerts**.
   - Click **Create Budget**.
   - Name: `Academy-Zero-Cost-Guard`.
   - Target Amount: **₹100 INR** (or $2.00 USD).
   - Trigger Thresholds: 50%, 90%, and 100%.
   - Notification: Email alerts to `annapoorniacademy@gmail.com`.
2. **Cloud Run Limits**:
   - `--max-instances 2` ensures traffic spikes cannot spawn dozens of containers.
   - `--min-instances 0` ensures idle periods cost ₹0.

---

## 6. Local Development Instructions

### Running Backend Locally
```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # macOS/Linux
pip install -r requirements.txt
python app.py
```
Backend runs at `http://localhost:5000`.

### Running Frontend Locally
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`.

### Running Automated Test Suite
```bash
cd backend
python -m unittest test_suite.py
```

### Exporting Local Backup
```bash
python scripts/export_data.py backup_snapshot.json
```

---

## 7. Verification & Health Check Endpoints

| URL Path | Method | Expected Status | Purpose |
| :--- | :--- | :--- | :--- |
| `https://annapoorniacademy.com/health` | GET | `200 OK` (`{"status": "healthy"}`) | Load balancer / uptime health probe |
| `https://annapoorniacademy.com/robots.txt` | GET | `200 OK` | Dynamic search engine indexing rules |
| `https://annapoorniacademy.com/sitemap.xml` | GET | `200 OK` | Dynamic XML sitemap with all published courses |
| `https://annapoorniacademy.com/api/courses` | GET | `200 OK` | Dynamic course catalog |
| `https://annapoorniacademy.com/admin/login` | GET | `200 OK` | Admin control portal |
