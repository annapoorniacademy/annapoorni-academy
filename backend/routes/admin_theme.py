import re
from flask import Blueprint, request, jsonify
from extensions import db
from models.theme import ThemeSetting
from utils.auth import admin_required

admin_theme_bp = Blueprint('admin_theme', __name__, url_prefix='/api/admin/website/theme')

HEX_COLOR_PATTERN = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3}|[A-Fa-f0-9]{8})$')
SAFE_FONT_PATTERN = re.compile(r'^[a-zA-Z0-9\s\-_]+$')

def sanitize_color(val, default='#1E3A8A'):
    if isinstance(val, str) and HEX_COLOR_PATTERN.match(val.strip()):
        return val.strip()
    return default

def sanitize_font(val, default='Inter'):
    if isinstance(val, str) and SAFE_FONT_PATTERN.match(val.strip()) and len(val.strip()) <= 50:
        return val.strip()
    return default

@admin_theme_bp.route('', methods=['PUT'])
@admin_required()
def update_theme():
    data = request.get_json() or {}
    theme = ThemeSetting.query.first()
    if not theme:
        theme = ThemeSetting()
        db.session.add(theme)

    color_fields = [
        'primary_color', 'secondary_color', 'accent_color',
        'background_color', 'text_color', 'card_color', 'button_color',
        'header_color', 'footer_color'
    ]

    for f in color_fields:
        if f in data and data[f]:
            setattr(theme, f, sanitize_color(data[f], getattr(theme, f)))

    if 'font_heading' in data:
        theme.font_heading = sanitize_font(data['font_heading'], theme.font_heading)
    if 'font_body' in data:
        theme.font_body = sanitize_font(data['font_body'], theme.font_body)
    if 'active_preset' in data and isinstance(data['active_preset'], str):
        theme.active_preset = data['active_preset'][:50]
    if 'font_scale' in data and data['font_scale'] in {'small', 'medium', 'large'}:
        theme.font_scale = data['font_scale']
    if 'border_radius' in data and isinstance(data['border_radius'], str):
        theme.border_radius = data['border_radius'][:20]
    if 'shadow_style' in data and isinstance(data['shadow_style'], str):
        theme.shadow_style = data['shadow_style'][:20]
    if 'is_published' in data:
        theme.is_published = bool(data['is_published'])

    db.session.commit()
    return jsonify({'message': 'Theme updated successfully', 'theme': theme.to_dict()}), 200
