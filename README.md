# 🎓 ANNAPOORNI ACADEMY V2.0
> **Production Website, Admin CMS & Ultra-Low-Cost Google Cloud Deployment**  
> **Production Domain:** `annapoorniacademy.com`

Annapoorni Academy V2.0 is a production-ready educational website and centralized Admin Content Management System (CMS) featuring coaching programs in **Vedic Mathematics**, **Memory Training**, and **Speed Reading** by **Coach Sindhu Ram**.

Designed for **ultra-low-cost hosting**, V2.0 runs as a **single-domain, scale-to-zero container on Google Cloud Run** backed by **Google Cloud Firestore (Free Tier)** and **Cloud Storage (Free Tier)** with expected recurring infrastructure operating costs approaching **₹0/month** within free quotas.

---

## 🌟 Key Features

### 1. Public Educational Website
- **Academy Homepage**: Clean branding, hero with dual CTAs ("Explore Courses", "Enquire Now"), dynamic flagship courses, dynamic subjects, concise learning benefits, latest announcements, clickable phone (`tel:`) and direct WhatsApp (`https://wa.me/`) links.
- **Floating WhatsApp Integration**: Persistent, responsive WhatsApp action button on all public pages, centrally driven from Admin Contact Settings.
- **Fault-Tolerant Contact Form**: Full validation for Name, Phone, Email, Preferred Learning Mode, Subject, and Message. Saves submissions directly to Firestore and attempts dual email notifications (admin notification + student confirmation copy). Always succeeds even if SMTP is unavailable.
- **Simple Course Enrollment**: Quick registration form for live Zoom / in-person batches with zero student-account friction.
- **Course & Subject Catalogs**: Dynamic course cards with skill levels, learning modes, durations, and syllabus timelines.
- **Interactive Quizzes & Assessments**: Immediate evaluation, score percentage calculations, answer reviews, and celebrations.

### 2. Centralized Admin Control CMS (`/admin`)
- **Dashboard Overview**: Real-time metric cards for Total Courses, Active Subjects, Lessons, Quizzes, Announcements, New Inquiries, Enrollment Requests, and Media Assets.
- **Course Management**: Create, edit, delete, and publish/unpublish courses with learning mode (Live Zoom, Offline, Hybrid), duration, category, and thumbnail selector.
- **Subject & Lesson Managers**: Manage coaching subjects and markdown lessons with video embed previews.
- **Quiz Builder**: Build assessments with multiple choice questions, points, options, and explanations.
- **Enrollments & Inquiries Tracker**: Filter, search, and update status (`New`, `Contacted`, `Interested`, `Enrolled`, `Closed`).
- **Live Theme & Appearance Editor**: Configure primary, secondary, and accent colors, Google Fonts (Outfit, Inter, Plus Jakarta Sans), logos, branding, and borders with live preview and CSS injection protection.
- **Homepage Section Editor**: Reorder and customize hero, about, benefits, and CTAs without developer intervention.
- **SEO & Social Media Controls**: Page title, meta descriptions, keywords, Open Graph cards, dynamic `/robots.txt`, and `/sitemap.xml`.
- **Media Library**: Image upload with automatic WebP compression to minimize bandwidth and storage.
- **One-Click Backup Export**: Download a full structured JSON backup of all academy data.

---

## 🛠️ Technology Stack

- **Frontend**: React 18, React Router v6, Axios, Lucide Icons, Recharts, Canvas Confetti, Vanilla CSS with custom design system.
- **Backend**: Python 3.11/3.12, Flask 3.0, Gunicorn WSGI, Flask-JWT-Extended, Werkzeug Security, Pillow (WebP optimization).
- **Database**: 
  - **Production**: Google Cloud Firestore (Native mode, 1 GiB free tier).
  - **Local Development / Offline**: SQLite zero-config fallback (`sqlite:///annapoorni.db`) or MySQL.
- **Cloud Infrastructure**: Google Cloud Run (Scale-to-zero, dynamic `$PORT`), Google Cloud Storage, Google-managed SSL/HTTPS.

---

## 🚀 Local Development Setup

### 1. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # macOS/Linux

pip install -r requirements.txt
python app.py
```
Backend API will be running at `http://localhost:5000`.

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend development server will be running at `http://localhost:5173`.

### 3. Running Test Suite
```bash
cd backend
python -m unittest test_suite.py
```

### 4. Building Production Bundle
```bash
cd frontend
npm run build
```

---

## ☁️ Google Cloud Production Deployment

See the complete step-by-step deployment runbook in [docs/DEPLOYMENT_V2.md](docs/DEPLOYMENT_V2.md).

### Quick Deploy Summary:
```bash
# 1. Build and push image to Google Cloud Build
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/annapoorni-web:v2.0

# 2. Deploy single-domain container to Cloud Run (Scale-to-zero)
gcloud run deploy annapoorni-web \
    --image gcr.io/YOUR_PROJECT_ID/annapoorni-web:v2.0 \
    --platform managed \
    --region asia-south1 \
    --allow-unauthenticated \
    --min-instances 0 \
    --max-instances 2 \
    --concurrency 80

# 3. Map custom domain
gcloud beta run domain-mappings create --service annapoorni-web --domain annapoorniacademy.com
```

---

## 📄 Documentation

- [Production Deployment Runbook](docs/DEPLOYMENT_V2.md)
- [REST API Specification](docs/API.md)
- [Architecture Guide](docs/ARCHITECTURE.md)
