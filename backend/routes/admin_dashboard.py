from flask import Blueprint, jsonify
from models.course import Course
from models.subject import Subject
from models.lesson import Lesson
from models.quiz import Quiz, QuizAttempt
from models.announcement import Announcement
from models.media import Media
from models.inquiry import ContactInquiry
from models.enrollment import Enrollment
from utils.auth import admin_required

admin_dashboard_bp = Blueprint('admin_dashboard', __name__, url_prefix='/api/admin/dashboard')

@admin_dashboard_bp.route('', methods=['GET'])
@admin_required()
def get_dashboard_summary():
    total_courses = Course.query.count()
    published_courses = Course.query.filter_by(status='published').count()
    total_subjects = Subject.query.count()
    active_subjects = Subject.query.filter_by(status='published').count()
    total_lessons = Lesson.query.count()
    published_lessons = Lesson.query.filter_by(is_published=True).count()
    total_quizzes = Quiz.query.count()
    total_quiz_attempts = QuizAttempt.query.count()
    total_announcements = Announcement.query.count()
    total_media = Media.query.count()
    
    total_inquiries = ContactInquiry.query.count()
    new_inquiries = ContactInquiry.query.filter_by(status='new').count()
    total_enrollments = Enrollment.query.count()
    new_enrollments = Enrollment.query.filter_by(status='new').count()

    recent_courses = [c.to_dict() for c in Course.query.order_by(Course.created_at.desc()).limit(5).all()]
    recent_announcements = [a.to_dict() for a in Announcement.query.order_by(Announcement.created_at.desc()).limit(5).all()]
    recent_attempts = [at.to_dict() for at in QuizAttempt.query.order_by(QuizAttempt.completed_at.desc()).limit(5).all()]
    recent_inquiries = [i.to_dict() for i in ContactInquiry.query.order_by(ContactInquiry.created_at.desc()).limit(5).all()]
    recent_enrollments = [e.to_dict() for e in Enrollment.query.order_by(Enrollment.created_at.desc()).limit(5).all()]

    return jsonify({
        'metrics': {
            'total_courses': total_courses,
            'published_courses': published_courses,
            'total_subjects': total_subjects,
            'active_subjects': active_subjects,
            'total_lessons': total_lessons,
            'published_lessons': published_lessons,
            'total_quizzes': total_quizzes,
            'total_quiz_attempts': total_quiz_attempts,
            'total_announcements': total_announcements,
            'total_media': total_media,
            'total_inquiries': total_inquiries,
            'new_inquiries': new_inquiries,
            'total_enrollments': total_enrollments,
            'new_enrollments': new_enrollments
        },
        'recent_courses': recent_courses,
        'recent_announcements': recent_announcements,
        'recent_attempts': recent_attempts,
        'recent_inquiries': recent_inquiries,
        'recent_enrollments': recent_enrollments
    }), 200
