from flask import Blueprint, request, jsonify
from extensions import db
from models.navigation import NavigationItem
from utils.auth import admin_required

admin_nav_bp = Blueprint('admin_navigation', __name__, url_prefix='/api/admin/navigation')

def is_safe_destination(dest):
    if not isinstance(dest, str):
        return False
    d = dest.strip()
    # Allow safe relative paths starting with /
    if d.startswith('/') and not d.startswith('//'):
        return True
    # Allow safe external http / https urls
    if d.startswith('http://') or d.startswith('https://'):
        return True
    return False

@admin_nav_bp.route('', methods=['GET'])
@admin_required()
def get_all_navigation_items():
    items = NavigationItem.query.order_by(NavigationItem.display_order.asc()).all()
    return jsonify([i.to_dict() for i in items]), 200

@admin_nav_bp.route('', methods=['POST'])
@admin_required()
def create_navigation_item():
    data = request.get_json() or {}
    label = data.get('label', '').strip()
    destination = data.get('destination', '').strip()

    if not label or not destination:
        return jsonify({'error': 'Label and destination are required'}), 400

    if not is_safe_destination(destination):
        return jsonify({'error': 'Destination must be a relative path (starting with /) or valid http(s) URL.'}), 400

    item = NavigationItem(
        label=label[:100],
        destination=destination[:255],
        display_order=int(data.get('display_order', 0)),
        is_enabled=bool(data.get('is_enabled', True)),
        is_external=bool(data.get('is_external', False)),
        location=data.get('location', 'both')
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@admin_nav_bp.route('/<int:item_id>', methods=['PUT'])
@admin_required()
def update_navigation_item(item_id):
    item = NavigationItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Navigation item not found'}), 404

    data = request.get_json() or {}
    if 'destination' in data and not is_safe_destination(data['destination']):
        return jsonify({'error': 'Destination must be a relative path (starting with /) or valid http(s) URL.'}), 400

    for f in ['label', 'destination', 'display_order', 'is_enabled', 'is_external', 'location']:
        if f in data:
            setattr(item, f, data[f])

    db.session.commit()
    return jsonify(item.to_dict()), 200

@admin_nav_bp.route('/<int:item_id>', methods=['DELETE'])
@admin_required()
def delete_navigation_item(item_id):
    item = NavigationItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Navigation item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Navigation item deleted successfully'}), 200
