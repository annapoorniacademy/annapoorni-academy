from flask import Blueprint, jsonify, Response
import json
from services.backup_service import generate_academy_backup_data
from utils.auth import admin_required

admin_backup_bp = Blueprint('admin_backup', __name__, url_prefix='/api/admin/backup')

@admin_backup_bp.route('/export', methods=['GET'])
@admin_required()
def export_backup():
    """Download full structured JSON export of all academy data."""
    try:
        backup_data = generate_academy_backup_data()
        json_str = json.dumps(backup_data, indent=2, ensure_ascii=False)
        
        return Response(
            json_str,
            mimetype='application/json',
            headers={
                'Content-Disposition': 'attachment; filename=annapoorni_academy_v2_backup.json'
            }
        )
    except Exception as e:
        return jsonify({'error': f'Failed to export backup: {str(e)}'}), 500
