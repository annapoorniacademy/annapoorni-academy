import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from parent or current directory .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'annapoorni-secret-key-v2-production-2026')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'annapoorni-jwt-secret-key-v2-production-2026')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES_DAYS', 7)))

    # Database Mode: 'sqlite', 'mysql', or 'firestore'
    DB_TYPE = os.environ.get('DB_TYPE', 'auto').lower()
    GOOGLE_CLOUD_PROJECT = os.environ.get('GOOGLE_CLOUD_PROJECT') or os.environ.get('FIRESTORE_PROJECT_ID', '')
    FIRESTORE_DATABASE = os.environ.get('FIRESTORE_DATABASE', '(default)')

    # Fallback to local SQLite database if DATABASE_URL is not set or empty
    # Automatically convert mysql:// to mysql+pymysql:// for PyMySQL driver compatibility
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith('mysql://'):
        db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)

    SQLALCHEMY_DATABASE_URI = db_url or f"sqlite:///{os.path.join(os.path.dirname(__file__), 'annapoorni.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload & Media configurations
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 10 * 1024 * 1024)) # 10MB limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
    STORAGE_BUCKET = os.environ.get('STORAGE_BUCKET', '')

    # Static folder for serving bundled React SPA build in unified Cloud Run container
    STATIC_FOLDER = os.environ.get('STATIC_FOLDER') or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig if os.environ.get('FLASK_ENV') == 'production' else DevelopmentConfig
}
