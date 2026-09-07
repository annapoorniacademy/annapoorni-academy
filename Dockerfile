# ==============================================================================
# Annapoorni Academy V2.0 — Production Single-Domain Dockerfile
# Serves both React SPA and Flask REST API from a single Google Cloud Run service
# ==============================================================================

# Stage 1: Build React Frontend Production Bundle
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci || npm install

COPY frontend/ ./
RUN npm run build

# Stage 2: Production Python Flask & Gunicorn WSGI Server
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_ENV=production \
    PORT=8080 \
    STATIC_FOLDER=/app/frontend/dist \
    UPLOAD_FOLDER=/app/uploads

WORKDIR /app

# Install minimal system dependencies for cryptography & image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy built React frontend assets from Stage 1
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Create uploads directory for local media storage fallback
RUN mkdir -p /app/uploads

EXPOSE 8080

# Production scale-to-zero entrypoint with dynamic PORT binding
CMD exec gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 2 --threads 4 --timeout 0 app:app
