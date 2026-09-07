"""
Backup & Export Service for Annapoorni Academy V2.0
Generates a consolidated JSON export of all core database collections.
"""

from datetime import datetime
from models.course import Course
from models.subject import Subject
from models.lesson import Lesson, CourseModule, Resource
from models.quiz import Quiz, Question, QuizOption
from models.announcement import Announcement
from models.inquiry import ContactInquiry
from models.enrollment import Enrollment
from models.website_settings import WebsiteSetting
from models.theme import ThemeSetting
from models.contact import ContactSetting
from models.seo import SeoSetting
from models.homepage import HomepageSection
from models.navigation import NavigationItem
from models.social import SocialLink
from models.media import Media

def generate_academy_backup_data():
    """
    Exports all structured academy data into a portable JSON-serializable dictionary.
    """
    site = WebsiteSetting.query.first()
    theme = ThemeSetting.query.first()
    contact = ContactSetting.query.first()
    seo = SeoSetting.query.first()

    backup = {
        'version': '2.0.0',
        'export_timestamp': datetime.utcnow().isoformat() + 'Z',
        'academy': 'Annapoorni Academy',
        'settings': {
            'website': site.to_dict() if site else {},
            'theme': theme.to_dict() if theme else {},
            'contact': contact.to_dict() if contact else {},
            'seo': seo.to_dict() if seo else {},
            'homepage_sections': [s.to_dict() for s in HomepageSection.query.order_by(HomepageSection.display_order.asc()).all()],
            'navigation_items': [n.to_dict() for n in NavigationItem.query.order_by(NavigationItem.display_order.asc()).all()],
            'social_links': [s.to_dict() for s in SocialLink.query.order_by(SocialLink.display_order.asc()).all()]
        },
        'subjects': [s.to_dict() for s in Subject.query.order_by(Subject.display_order.asc()).all()],
        'courses': [c.to_dict(include_details=True) for c in Course.query.order_by(Course.display_order.asc()).all()],
        'lessons': [l.to_dict() for l in Lesson.query.order_by(Lesson.display_order.asc()).all()],
        'quizzes': [q.to_dict(include_questions=True, include_correct=True) for q in Quiz.query.all()],
        'announcements': [a.to_dict() for a in Announcement.query.order_by(Announcement.created_at.desc()).all()],
        'inquiries': [i.to_dict() for i in ContactInquiry.query.order_by(ContactInquiry.created_at.desc()).all()],
        'enrollments': [e.to_dict() for e in Enrollment.query.order_by(Enrollment.created_at.desc()).all()],
        'media': [m.to_dict() for m in Media.query.order_by(Media.created_at.desc()).all()]
    }

    return backup
