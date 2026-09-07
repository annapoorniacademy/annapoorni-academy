import os
from flask import Flask, send_from_directory, jsonify, Response
from config import config_by_name
from extensions import db, cors, jwt
from middleware.error_handler import register_error_handlers
from services.seed_service import seed_database

# Import Blueprints
from routes.auth import auth_bp
from routes.public import public_bp
from routes.admin_settings import admin_settings_bp
from routes.admin_theme import admin_theme_bp
from routes.admin_homepage import admin_homepage_bp
from routes.admin_navigation import admin_nav_bp
from routes.admin_social import admin_social_bp
from routes.admin_courses import admin_courses_bp
from routes.admin_subjects import admin_subjects_bp
from routes.admin_lessons import admin_lessons_bp
from routes.admin_quizzes import admin_quizzes_bp
from routes.admin_announcements import admin_announcements_bp
from routes.admin_media import admin_media_bp
from routes.admin_seo import admin_seo_bp
from routes.admin_contact import admin_contact_bp
from routes.admin_dashboard import admin_dashboard_bp
from routes.admin_enrollments import admin_enrollments_bp
from routes.admin_backup import admin_backup_bp

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'production')

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Configure CORS origins based on FRONTEND_URL or allow local dev origins
    frontend_env = os.environ.get('FRONTEND_URL', '')
    allowed_origins = [
        'https://annapoorniacademy.com',
        'https://www.annapoorniacademy.com',
        'https://annapoorniacademy.netlify.app',
        'http://localhost:5173',
        'http://127.0.0.1:5173',
        'http://localhost:5000',
        'http://localhost:8080',
        'http://localhost:80'
    ]
    if frontend_env and frontend_env.strip() != '*':
        for url in frontend_env.split(','):
            cleaned = url.strip()
            if cleaned and cleaned not in allowed_origins:
                allowed_origins.append(cleaned)
    elif frontend_env.strip() == '*':
        allowed_origins = '*'

    # Initialize extensions
    db.init_app(app)
    cors.init_app(app, resources={
        r"/api/*": {"origins": allowed_origins},
        r"/uploads/*": {"origins": allowed_origins}
    }, supports_credentials=True)
    jwt.init_app(app)

    # Register error handlers
    register_error_handlers(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_settings_bp)
    app.register_blueprint(admin_theme_bp)
    app.register_blueprint(admin_homepage_bp)
    app.register_blueprint(admin_nav_bp)
    app.register_blueprint(admin_social_bp)
    app.register_blueprint(admin_courses_bp)
    app.register_blueprint(admin_subjects_bp)
    app.register_blueprint(admin_lessons_bp)
    app.register_blueprint(admin_quizzes_bp)
    app.register_blueprint(admin_announcements_bp)
    app.register_blueprint(admin_media_bp)
    app.register_blueprint(admin_seo_bp)
    app.register_blueprint(admin_contact_bp)
    app.register_blueprint(admin_dashboard_bp)
    app.register_blueprint(admin_enrollments_bp)
    app.register_blueprint(admin_backup_bp)

    # Serve uploaded media files
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Production & Deployment Health Check
    @app.route('/health', methods=['GET'])
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'version': '2.0.0',
            'service': 'Annapoorni Academy Production Service'
        }), 200

    # Dynamic SEO: robots.txt
    @app.route('/robots.txt', methods=['GET'])
    def robots_txt():
        content = """User-agent: *
Allow: /
Disallow: /admin
Disallow: /api/admin

Sitemap: https://annapoorniacademy.com/sitemap.xml
"""
        return Response(content, mimetype='text/plain')

    # Dynamic SEO: sitemap.xml
    @app.route('/sitemap.xml', methods=['GET'])
    def sitemap_xml():
        base_url = "https://annapoorniacademy.com"
        urls = [
            f"<url><loc>{base_url}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>",
            f"<url><loc>{base_url}/about</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>",
            f"<url><loc>{base_url}/courses</loc><changefreq>daily</changefreq><priority>0.9</priority></url>",
            f"<url><loc>{base_url}/subjects</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>",
            f"<url><loc>{base_url}/announcements</loc><changefreq>daily</changefreq><priority>0.7</priority></url>",
            f"<url><loc>{base_url}/contact</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>",
        ]
        
        try:
            from models.course import Course
            courses = Course.query.filter_by(status='published').all()
            for c in courses:
                urls.append(f"<url><loc>{base_url}/courses/{c.id}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>")
        except Exception:
            pass

        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(urls)}
</urlset>"""
        return Response(xml, mimetype='application/xml')

    # Serve static frontend build (SPA Catch-All)
    static_folder = app.config.get('STATIC_FOLDER')
    if static_folder and os.path.exists(static_folder):
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def serve_frontend(path):
            if path and path.startswith('api/'):
                return jsonify({'error': 'Not found'}), 404
            
            full_path = os.path.join(static_folder, path)
            if path and os.path.exists(full_path) and os.path.isfile(full_path):
                return send_from_directory(static_folder, path)
            
            # Catch-all for SPA routes (e.g. /about, /courses, /admin, etc.)
            index_path = os.path.join(static_folder, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder, 'index.html')
            return jsonify({'message': 'Annapoorni Academy API is live. Frontend build pending.'}), 200

    # Auto-create tables and seed database
    with app.app_context():
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        try:
            db.create_all()
            seed_database()
        except Exception as e:
            app.logger.warning(f"Database initialization note: {e}")

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    is_debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=is_debug)
