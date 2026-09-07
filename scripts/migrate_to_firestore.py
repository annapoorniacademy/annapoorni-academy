"""
Firestore Migration CLI Script for Annapoorni Academy V2.0
Migrates all SQL database records (SQLite / MySQL) to Google Cloud Firestore collections.

Usage:
  python scripts/migrate_to_firestore.py --project YOUR_GCP_PROJECT_ID
"""

import os
import sys
import argparse
import json
from datetime import datetime

# Add backend directory to path
backend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
sys.path.insert(0, backend_dir)

from app import create_app
from services.backup_service import generate_academy_backup_data

def migrate_to_firestore(project_id=None):
    try:
        from google.cloud import firestore
    except ImportError:
        print("[ERROR] google-cloud-firestore package is required. Install it using: pip install google-cloud-firestore")
        sys.exit(1)

    app = create_app()
    with app.app_context():
        print(f"[INFO] Initializing Firestore migration to project: {project_id or 'default'}")
        db = firestore.Client(project=project_id) if project_id else firestore.Client()
        
        data = generate_academy_backup_data()
        
        # 1. Settings Collection
        print(" -> Migrating website, theme, contact, and SEO settings...")
        settings_dict = data.get('settings', {})
        for key in ['website', 'theme', 'contact', 'seo']:
            if key in settings_dict and settings_dict[key]:
                db.collection('settings').document(key).set(settings_dict[key])
        
        # Homepage sections
        for section in settings_dict.get('homepage_sections', []):
            sec_id = section.get('section_key') or str(section.get('id'))
            db.collection('homepage_sections').document(sec_id).set(section)
            
        # Navigation
        for nav in settings_dict.get('navigation_items', []):
            db.collection('navigation_items').document(str(nav.get('id'))).set(nav)
            
        # Social links
        for soc in settings_dict.get('social_links', []):
            db.collection('social_links').document(str(soc.get('id'))).set(soc)

        # 2. Subjects
        print(" -> Migrating subjects...")
        for sub in data.get('subjects', []):
            db.collection('subjects').document(str(sub.get('id'))).set(sub)

        # 3. Courses & Modules
        print(" -> Migrating courses...")
        for course in data.get('courses', []):
            db.collection('courses').document(str(course.get('id'))).set(course)

        # 4. Lessons
        print(" -> Migrating lessons...")
        for les in data.get('lessons', []):
            db.collection('lessons').document(str(les.get('id'))).set(les)

        # 5. Quizzes
        print(" -> Migrating quizzes...")
        for quiz in data.get('quizzes', []):
            db.collection('quizzes').document(str(quiz.get('id'))).set(quiz)

        # 6. Announcements
        print(" -> Migrating announcements...")
        for ann in data.get('announcements', []):
            db.collection('announcements').document(str(ann.get('id'))).set(ann)

        # 7. Inquiries & Enrollments
        print(" -> Migrating inquiries and enrollments...")
        for inq in data.get('inquiries', []):
            db.collection('inquiries').document(str(inq.get('id'))).set(inq)
            
        for enr in data.get('enrollments', []):
            db.collection('enrollments').document(str(enr.get('id'))).set(enr)

        # 8. Media
        print(" -> Migrating media records...")
        for med in data.get('media', []):
            db.collection('media').document(str(med.get('id'))).set(med)

        print("\n[SUCCESS] Migration to Google Cloud Firestore completed successfully!")
        print("Your academy data is now fully synchronized in Firestore.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Migrate SQL database to Google Cloud Firestore")
    parser.add_argument('--project', default=os.environ.get('GOOGLE_CLOUD_PROJECT') or os.environ.get('FIRESTORE_PROJECT_ID'), help="Google Cloud Project ID")
    args = parser.parse_args()
    migrate_to_firestore(project_id=args.project)
