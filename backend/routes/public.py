from flask import Blueprint, jsonify, request
from datetime import datetime
from extensions import db
from models.website_settings import WebsiteSetting
from models.theme import ThemeSetting
from models.homepage import HomepageSection
from models.navigation import NavigationItem
from models.social import SocialLink
from models.contact import ContactSetting
from models.seo import SeoSetting
from models.course import Course
from models.subject import Subject
from models.lesson import Lesson
from models.quiz import Quiz, QuizAttempt, QuizAnswer
from models.announcement import Announcement
from models.enrollment import Enrollment
from models.inquiry import ContactInquiry
from models.activity_log import ActivityLog
from services.email_service import (
    send_contact_inquiry_emails,
    send_enrollment_emails,
    send_admin_email_notification,
    send_student_confirmation_email
)
from services.firestore_service import is_firestore_enabled, enrollments_col, inquiries_col

public_bp = Blueprint('public', __name__, url_prefix='/api')

@public_bp.route('/website/settings', methods=['GET'])
def get_website_settings():
    setting = WebsiteSetting.query.first()
    return jsonify(setting.to_dict() if setting else {}), 200

@public_bp.route('/website/theme', methods=['GET'])
def get_website_theme():
    theme = ThemeSetting.query.first()
    return jsonify(theme.to_dict() if theme else {}), 200

@public_bp.route('/homepage', methods=['GET'])
@public_bp.route('/homepage/sections', methods=['GET'])
def get_homepage():
    sections = HomepageSection.query.filter_by(is_enabled=True).order_by(HomepageSection.display_order.asc()).all()
    return jsonify([sec.to_dict() for sec in sections]), 200

@public_bp.route('/navigation', methods=['GET'])
def get_navigation():
    items = NavigationItem.query.filter_by(is_enabled=True).order_by(NavigationItem.display_order.asc()).all()
    return jsonify([item.to_dict() for item in items]), 200

@public_bp.route('/social-links', methods=['GET'])
def get_social_links():
    links = SocialLink.query.filter_by(is_enabled=True).order_by(SocialLink.display_order.asc()).all()
    return jsonify([link.to_dict() for link in links]), 200

@public_bp.route('/contact', methods=['GET'])
def get_contact_settings():
    contact = ContactSetting.query.first()
    return jsonify(contact.to_dict() if contact else {}), 200

@public_bp.route('/seo', methods=['GET'])
def get_seo_settings():
    seo = SeoSetting.query.first()
    return jsonify(seo.to_dict() if seo else {}), 200

# Public Courses
@public_bp.route('/courses', methods=['GET'])
def get_courses():
    subject_id = request.args.get('subject_id')
    category = request.args.get('category')
    featured = request.args.get('featured')
    search = request.args.get('search')

    query = Course.query.filter_by(status='published')

    if subject_id:
        query = query.filter_by(subject_id=subject_id)
    if category:
        query = query.filter_by(category=category)
    if featured and featured.lower() in ['true', '1']:
        query = query.filter_by(is_featured=True)
    if search:
        query = query.filter(Course.title.ilike(f'%{search}%') | Course.description.ilike(f'%{search}%'))

    courses = query.order_by(Course.display_order.asc(), Course.created_at.desc()).all()
    return jsonify([c.to_dict() for c in courses]), 200

@public_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course_detail(course_id):
    course = Course.query.filter_by(id=course_id, status='published').first()
    if not course:
        # Check by slug
        course = Course.query.filter_by(slug=str(course_id), status='published').first()
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    return jsonify(course.to_dict(include_details=True)), 200

# Public Subjects
@public_bp.route('/subjects', methods=['GET'])
def get_subjects():
    subjects = Subject.query.filter_by(status='published').order_by(Subject.display_order.asc()).all()
    return jsonify([s.to_dict() for s in subjects]), 200

@public_bp.route('/subjects/<int:subject_id>', methods=['GET'])
def get_subject_detail(subject_id):
    subject = Subject.query.filter_by(id=subject_id, status='published').first()
    if not subject:
        subject = Subject.query.filter_by(slug=str(subject_id), status='published').first()
    if not subject:
        return jsonify({'error': 'Subject not found'}), 404

    data = subject.to_dict()
    data['courses'] = [c.to_dict() for c in subject.courses if c.status == 'published']
    data['lessons'] = [l.to_dict() for l in subject.lessons if l.is_published]
    return jsonify(data), 200

# Public Lessons
@public_bp.route('/lessons/<int:lesson_id>', methods=['GET'])
def get_lesson_detail(lesson_id):
    lesson = Lesson.query.filter_by(id=lesson_id, is_published=True).first()
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404

    data = lesson.to_dict(include_details=True)
    
    # Previous and Next lesson navigation in course
    all_lessons = Lesson.query.filter_by(course_id=lesson.course_id, is_published=True).order_by(Lesson.display_order.asc()).all()
    idx = next((i for i, l in enumerate(all_lessons) if l.id == lesson.id), -1)
    data['prev_lesson_id'] = all_lessons[idx - 1].id if idx > 0 else None
    data['next_lesson_id'] = all_lessons[idx + 1].id if (idx >= 0 and idx < len(all_lessons) - 1) else None

    return jsonify(data), 200

# Public Quizzes & Submission
@public_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz_detail(quiz_id):
    quiz = Quiz.query.filter_by(id=quiz_id, is_published=True).first()
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    # Do not include correct answer flag for public quiz taking
    return jsonify(quiz.to_dict(include_questions=True, include_correct=False)), 200

@public_bp.route('/quizzes/<int:quiz_id>/submit', methods=['POST'])
def submit_quiz(quiz_id):
    quiz = Quiz.query.filter_by(id=quiz_id, is_published=True).first()
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    data = request.get_json() or {}
    user_identifier = data.get('user_name', 'Guest Student')
    submitted_answers = data.get('answers', {}) # format: { question_id: [selected_option_ids] or selected_option_id }

    total_score = 0
    max_score = 0
    detailed_results = []

    for question in quiz.questions:
        q_id = str(question.id)
        max_score += question.points
        user_selection = submitted_answers.get(q_id) or submitted_answers.get(question.id)

        if not isinstance(user_selection, list):
            user_selection = [user_selection] if user_selection is not None else []

        # Find correct options for this question
        correct_option_ids = [opt.id for opt in question.options if opt.is_correct]
        
        is_q_correct = set(user_selection) == set(correct_option_ids) and len(correct_option_ids) > 0
        q_score = question.points if is_q_correct else 0
        total_score += q_score

        detailed_results.append({
            'question_id': question.id,
            'question_text': question.question_text,
            'points': question.points,
            'earned_points': q_score,
            'is_correct': is_q_correct,
            'explanation': question.explanation,
            'user_selection': user_selection,
            'correct_option_ids': correct_option_ids
        })

    percentage = round((total_score / max_score * 100), 1) if max_score > 0 else 0.0
    is_passed = percentage >= quiz.passing_score

    # Save Attempt
    attempt = QuizAttempt(
        quiz_id=quiz.id,
        user_identifier=user_identifier,
        score=total_score,
        max_score=max_score,
        percentage=percentage,
        is_passed=is_passed
    )
    db.session.add(attempt)
    db.session.commit()

    return jsonify({
        'attempt_id': attempt.id,
        'quiz_id': quiz.id,
        'quiz_title': quiz.title,
        'user_identifier': user_identifier,
        'score': total_score,
        'max_score': max_score,
        'percentage': percentage,
        'passing_score': quiz.passing_score,
        'is_passed': is_passed,
        'results': detailed_results
    }), 200

# Public Announcements
@public_bp.route('/announcements', methods=['GET'])
def get_announcements():
    category = request.args.get('category')
    featured = request.args.get('featured')
    
    query = Announcement.query.filter_by(status='published')
    if category:
        query = query.filter_by(category=category)
    if featured and featured.lower() in ['true', '1']:
        query = query.filter_by(is_featured=True)

    items = query.order_by(Announcement.created_at.desc()).all()
    return jsonify([i.to_dict() for i in items]), 200

@public_bp.route('/courses/<int:course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json() or {}

    student_name = data.get('student_name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    preferred_mode = data.get('preferred_mode', 'Live Online via Zoom').strip()
    message = data.get('message', '').strip()

    if not student_name or not email or not phone:
        return jsonify({'error': 'Name, email, and phone number are required.'}), 400

    # 1. Save to Database FIRST
    enrollment = Enrollment(
        course_id=course.id,
        course_title=course.title,
        student_name=student_name,
        email=email,
        phone=phone,
        preferred_mode=preferred_mode,
        message=message
    )
    db.session.add(enrollment)

    # Log activity for admin dashboard
    log = ActivityLog(
        action=f"New Enrollment: {student_name} for '{course.title}' ({preferred_mode})",
        details=f"Email: {email}, Phone: {phone}, Message: {message}"
    )
    db.session.add(log)
    db.session.commit()

    # Firestore synchronization if active
    if is_firestore_enabled():
        try:
            enrollments_col.create(enrollment.id, enrollment.to_dict())
        except Exception:
            pass

    # 2. Attempt dual email dispatch (Outlook SMTP)
    email_results = send_enrollment_emails(enrollment.to_dict())
    email_delivered = bool(email_results.get('applicant_confirmed') or email_results.get('admin_notified'))

    return jsonify({
        'message': f"Enrollment registration for '{course.title}' submitted successfully!",
        'enrollment': enrollment.to_dict(),
        'email_sent': email_delivered
    }), 201

@public_bp.route('/contact/inquiry', methods=['POST'])
@public_bp.route('/inquiries', methods=['POST'])
def submit_contact_inquiry():
    data = request.get_json() or {}

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    mode = data.get('mode', 'General Inquiry').strip()
    subject = data.get('subject', 'General Inquiry').strip()
    message = data.get('message', '').strip()

    if not name or not email or not message:
        return jsonify({'error': 'Name, email, and message are required.'}), 400

    # 1. Save to Database FIRST
    inquiry = ContactInquiry(
        name=name,
        email=email,
        phone=phone,
        mode=mode,
        subject=subject,
        message=message
    )
    db.session.add(inquiry)

    # Log activity for admin dashboard
    log = ActivityLog(
        action=f"New Contact Inquiry from {name}: '{subject}' ({mode})",
        details=f"Email: {email}, Phone: {phone}, Message: {message}"
    )
    db.session.add(log)
    db.session.commit()

    # Firestore synchronization if active
    if is_firestore_enabled():
        try:
            inquiries_col.create(inquiry.id, inquiry.to_dict())
        except Exception:
            pass

    # 2. Attempt dual email dispatch (Outlook SMTP)
    email_results = send_contact_inquiry_emails(inquiry.to_dict())
    email_delivered = bool(email_results.get('applicant_confirmed') or email_results.get('admin_notified'))

    return jsonify({
        'message': 'Your inquiry has been received. Our team will contact you shortly.',
        'inquiry': inquiry.to_dict(),
        'email_sent': email_delivered
    }), 201

