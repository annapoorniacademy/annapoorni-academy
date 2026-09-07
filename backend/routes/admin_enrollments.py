from flask import Blueprint, jsonify, request
from extensions import db
from models.enrollment import Enrollment
from utils.auth import admin_required

admin_enrollments_bp = Blueprint('admin_enrollments', __name__, url_prefix='/api/admin/enrollments')

@admin_enrollments_bp.route('', methods=['GET'])
@admin_required()
def get_enrollments():
    status = request.args.get('status')
    search = request.args.get('search')

    query = Enrollment.query
    if status:
        query = query.filter_by(status=status)
    if search:
        query = query.filter(
            (Enrollment.student_name.ilike(f'%{search}%')) |
            (Enrollment.email.ilike(f'%{search}%')) |
            (Enrollment.phone.ilike(f'%{search}%')) |
            (Enrollment.course_title.ilike(f'%{search}%'))
        )

    enrollments = query.order_by(Enrollment.created_at.desc()).all()
    return jsonify([e.to_dict() for e in enrollments]), 200

@admin_enrollments_bp.route('/<int:id>', methods=['PUT'])
@admin_required()
def update_enrollment_status(id):
    enrollment = Enrollment.query.get_or_404(id)
    data = request.get_json() or {}

    if 'status' in data:
        valid_statuses = ['New', 'Contacted', 'Interested', 'Enrolled', 'Closed']
        if data['status'] not in valid_statuses:
            return jsonify({'error': f"Invalid status '{data['status']}'. Must be one of {valid_statuses}"}), 400
        enrollment.status = data['status']
    if 'notes' in data:
        enrollment.message = data['notes']

    db.session.commit()
    return jsonify(enrollment.to_dict()), 200

@admin_enrollments_bp.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete_enrollment(id):
    enrollment = Enrollment.query.get_or_404(id)
    db.session.delete(enrollment)
    db.session.commit()
    return jsonify({'message': 'Enrollment record deleted successfully.'}), 200
