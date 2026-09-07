"""
Export Data CLI Script for Annapoorni Academy V2.0
Usage: python scripts/export_data.py [--output backup.json]
"""

import os
import sys
import json
from datetime import datetime

# Add backend directory to path
backend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
sys.path.insert(0, backend_dir)

from app import create_app
from services.backup_service import generate_academy_backup_data

def main():
    app = create_app()
    with app.app_context():
        print("[INFO] Generating Annapoorni Academy V2.0 data snapshot...")
        backup = generate_academy_backup_data()
        
        output_file = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else f"annapoorni_backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(backup, f, indent=2, ensure_ascii=False)
            
        print(f"[SUCCESS] Exported {len(backup.get('courses', []))} courses, {len(backup.get('subjects', []))} subjects, {len(backup.get('lessons', []))} lessons to: {output_file}")

if __name__ == '__main__':
    main()
