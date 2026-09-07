import json
from extensions import db
from models.admin import Admin
from models.website_settings import WebsiteSetting
from models.theme import ThemeSetting
from models.homepage import HomepageSection
from models.navigation import NavigationItem
from models.social import SocialLink
from models.contact import ContactSetting
from models.seo import SeoSetting
from models.subject import Subject
from models.course import Course
from models.lesson import CourseModule, Lesson, Resource
from models.quiz import Quiz, Question, QuizOption
from models.announcement import Announcement

def seed_database():
    """Seed initial default configurations and sample content if database is empty."""
    
    # 1. Admin Account
    if not Admin.query.first():
        import os
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_email = os.environ.get('ADMIN_EMAIL', 'coach.sindhuram@gmail.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', '$12345678')

        admin = Admin(
            username=admin_username,
            email=admin_email
        )
        admin.set_password(admin_password)
        db.session.add(admin)

    # 2. Website Settings
    if not WebsiteSetting.query.first():
        site = WebsiteSetting(
            site_name='Annapoorni Academy',
            tagline='Empowering Minds, Shaping Futures',
            site_description='Annapoorni Academy is a premier educational platform providing world-class courses, subjects, lessons, and interactive learning assessments.',
            logo_url='https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=200&auto=format&fit=crop&q=80',
            favicon_url='https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=64&auto=format&fit=crop&q=80',
            dark_mode_default=False
        )
        db.session.add(site)

    # 3. Theme Settings
    if not ThemeSetting.query.first():
        theme = ThemeSetting(
            active_preset='Academic',
            primary_color='#1E3A8A',    # Navy Blue
            secondary_color='#0D9488',  # Teal
            accent_color='#F59E0B',     # Gold
            background_color='#F8FAFC', # Slate Light
            text_color='#0F172A',       # Dark Slate
            card_color='#FFFFFF',
            button_color='#1E3A8A',
            header_color='#FFFFFF',
            footer_color='#0F172A',
            font_heading='Outfit',
            font_body='Inter',
            font_scale='medium',
            heading_weight='700',
            body_weight='400',
            border_radius='12px',
            shadow_style='modern',
            is_published=True
        )
        db.session.add(theme)

    # 4. Homepage Sections
    if not HomepageSection.query.first():
        sections = [
            HomepageSection(
                section_key='hero',
                section_name='Hero Section',
                is_enabled=True,
                display_order=1,
                title='Master Vedic Maths, Memory & Speed Reading',
                subtitle='Unlock faster mental calculations, advanced memory recall, national competition practice, and rapid reading efficiency with Coach Sindhu Ram.',
                image_url='https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1000&auto=format&fit=crop&q=80',
                cta_text='Explore Courses',
                cta_url='/courses',
                secondary_cta_text='Browse Subjects',
                secondary_cta_url='/subjects',
                background_style='gradient'
            ),
            HomepageSection(
                section_key='about',
                section_name='About Section',
                is_enabled=True,
                display_order=2,
                title='Empowering Minds with Coach Sindhu Ram',
                subtitle='Specialized Coaching in Vedic Mathematics, Memory Training, and Speed Reading.',
                content='Annapoorni Academy offers world-class training in Vedic Maths (16 Sutras for rapid mental arithmetic), Memory Coaching (association & recall techniques), and Speed Reading (rapid information processing). Our students excel in national-level speed competitions and academic challenges.',
                image_url='https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=800&auto=format&fit=crop&q=80',
                cta_text='Learn More About Us',
                cta_url='/about',
                meta_json=json.dumps([
                    {'label': 'Active Students', 'value': '15,000+'},
                    {'label': 'Expert Courses', 'value': '120+'},
                    {'label': 'Interactive Lessons', 'value': '850+'},
                    {'label': 'Success Rate', 'value': '98%'}
                ])
            ),
            HomepageSection(
                section_key='featured_courses',
                section_name='Featured Courses',
                is_enabled=True,
                display_order=3,
                title='Featured Courses',
                subtitle='Handpicked premium courses designed by leading educators.',
                background_style='default'
            ),
            HomepageSection(
                section_key='benefits',
                section_name='Learning Benefits',
                is_enabled=True,
                display_order=4,
                title='Why Learn With Annapoorni Academy?',
                subtitle='We provide an unmatched educational experience built for modern learners.',
                meta_json=json.dumps([
                    {'title': 'Expert Learning', 'desc': 'Curated curriculum by seasoned academic leaders and subject experts.', 'icon': 'Award'},
                    {'title': 'Structured Courses', 'desc': 'Step-by-step modules that build deep mastery from basics to advanced levels.', 'icon': 'Layers'},
                    {'title': 'Interactive Assessments', 'desc': 'Immediate feedback on quizzes and progress tracking to reinforce knowledge.', 'icon': 'CheckCircle'},
                    {'title': 'Quality Resources', 'desc': 'Comprehensive study notes, downloadable guides, and video lectures.', 'icon': 'FileText'},
                    {'title': 'Flexible Pace', 'desc': 'Learn anytime, anywhere on mobile or desktop at your own comfort.', 'icon': 'Clock'},
                    {'title': 'Continuous Growth', 'desc': 'Regular announcements, updated modules, and expanding course libraries.', 'icon': 'TrendingUp'}
                ])
            ),
            HomepageSection(
                section_key='testimonials',
                section_name='Student & Parent Testimonials',
                is_enabled=True,
                display_order=5,
                title='What Our Learners Say',
                subtitle='Real feedback from students thriving at Annapoorni Academy.',
                meta_json=json.dumps([
                    {
                        'name': 'Priya Sharma',
                        'role': 'Science Student',
                        'quote': 'The structured lessons and quizzes at Annapoorni Academy transformed my understanding of Physics and Mathematics!',
                        'avatar': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80'
                    },
                    {
                        'name': 'Rohan Verma',
                        'role': 'Computer Science Learner',
                        'quote': 'Clear video tutorials, concise notes, and instant quiz scoring helped me clear my competitive examinations with ease.',
                        'avatar': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80'
                    },
                    {
                        'name': 'Ananya Iyer',
                        'role': 'High School Scholar',
                        'quote': 'The mobile-friendly layout and interactive assessments make revision fun and super efficient!',
                        'avatar': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80'
                    }
                ])
            ),
            HomepageSection(
                section_key='announcements',
                section_name='Latest Announcements',
                is_enabled=True,
                display_order=6,
                title='Academy News & Updates',
                subtitle='Stay informed with the latest notifications, workshops, and exam alerts.',
                background_style='default'
            ),
            HomepageSection(
                section_key='cta',
                section_name='Call To Action',
                is_enabled=True,
                display_order=7,
                title='Ready to Begin Your Educational Journey?',
                subtitle='Explore our extensive library of subjects and take your knowledge to the next level today.',
                cta_text='Get Started Free',
                cta_url='/courses',
                background_style='dark'
            )
        ]
        for sec in sections:
            db.session.add(sec)

    # 5. Navigation Items
    if not NavigationItem.query.first():
        nav_items = [
            NavigationItem(label='Home', destination='/', display_order=1, location='both'),
            NavigationItem(label='About', destination='/about', display_order=2, location='both'),
            NavigationItem(label='Courses', destination='/courses', display_order=3, location='both'),
            NavigationItem(label='Subjects', destination='/subjects', display_order=4, location='both'),
            NavigationItem(label='Announcements', destination='/announcements', display_order=5, location='both'),
            NavigationItem(label='Contact', destination='/contact', display_order=6, location='both')
        ]
        for item in nav_items:
            db.session.add(item)

    # 6. Social Links
    if not SocialLink.query.first():
        socials = [
            SocialLink(platform='Instagram', url='https://www.instagram.com/coachsindhuram?igsh=MXR4cmdvaHZveHZleA%3D%3D', icon='Instagram', display_order=1, is_enabled=True),
            SocialLink(platform='YouTube', url='https://youtube.com/@annapoorniacademy', icon='Youtube', display_order=2, is_enabled=False),
            SocialLink(platform='LinkedIn', url='https://www.linkedin.com/in/coach-sindhuram/', icon='Linkedin', display_order=3, is_enabled=True),
            SocialLink(platform='Facebook', url='https://facebook.com/annapoorniacademy', icon='Facebook', display_order=4, is_enabled=True),
            SocialLink(platform='X', url='https://x.com/annapoorni_edu', icon='Twitter', display_order=5, is_enabled=False)
        ]
        for soc in socials:
            db.session.add(soc)

    # 7. Contact Settings
    if not ContactSetting.query.first():
        contact = ContactSetting(
            email='coach.sindhuram@gmail.com',
            phone='+91 90803 85589',
            address='Coach Sindhu Ram Academy, Tamil Nadu, India',
            maps_embed_url='https://maps.google.com/maps?q=Annapoorni%20Academy%20Coach%20Sindhu%20Ram&t=&z=15&ie=UTF8&iwloc=&output=embed',
            working_hours='Monday - Saturday: 8:30 AM - 6:30 PM',
            contact_form_recipient='coach.sindhuram@gmail.com'
        )
        db.session.add(contact)

    # 8. SEO Settings
    if not SeoSetting.query.first():
        seo = SeoSetting(
            site_title='Annapoorni Academy — Premier Educational Platform',
            meta_description='Empowering minds with structured courses, subjects, video lessons, and interactive quizzes.',
            keywords='education, academy, courses, subjects, lessons, quizzes, annapoorni, learning',
            og_title='Annapoorni Academy — Excellence in Education',
            og_description='Explore premier educational content and test your skills with interactive quizzes.'
        )
        db.session.add(seo)

    # 9. Flagship Subjects (Coach Sindhu Ram)
    if not Subject.query.first():
        vm_sub = Subject(
            name='Vedic Mathematics',
            slug='vedic-mathematics',
            description='Master ancient Vedic maths techniques, mental arithmetic, faster calculations, and competition-oriented practice.',
            image_url='https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=600&auto=format&fit=crop&q=80',
            icon='Calculator',
            display_order=1
        )
        mem_sub = Subject(
            name='Memory Coaching',
            slug='memory-coaching',
            description='Transform recall, retention, and cognitive learning strategies with proven memory training techniques.',
            image_url='https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=600&auto=format&fit=crop&q=80',
            icon='Award',
            display_order=2
        )
        sr_sub = Subject(
            name='Speed Reading',
            slug='speed-reading',
            description='Develop speed-reading techniques to improve reading efficiency and rapidly process written information.',
            image_url='https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=600&auto=format&fit=crop&q=80',
            icon='BookOpen',
            display_order=3
        )
        db.session.add_all([vm_sub, mem_sub, sr_sub])
        db.session.flush()

        # 10. Flagship Courses
        c1 = Course(
            title='Vedic Maths & Speed Calculation Mastery',
            slug='vedic-maths-speed-calculation-mastery',
            description='Learn 16 Vedic Sutras for lightning-fast mental arithmetic, rapid multiplication, square roots, and national-level competition preparation.',
            thumbnail_url='https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=600&auto=format&fit=crop&q=80',
            category='Vedic Maths',
            subject_id=vm_sub.id,
            difficulty='All Levels',
            duration='4 Weeks',
            status='published',
            is_featured=True,
            display_order=1
        )
        c2 = Course(
            title='Memory Coaching & Retention Masterclass',
            slug='memory-coaching-retention-masterclass',
            description='Master cognitive recall techniques, mnemonic systems, mind mapping, and long-term memory retention strategies.',
            thumbnail_url='https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=600&auto=format&fit=crop&q=80',
            category='Memory Coaching',
            subject_id=mem_sub.id,
            difficulty='All Levels',
            duration='3 Weeks',
            status='published',
            is_featured=True,
            display_order=2
        )
        c3 = Course(
            title='Speed Reading & Rapid Information Processing',
            slug='speed-reading-rapid-information-processing',
            description='Double your reading speed, eliminate sub-vocalization, expand peripheral vision, and maximize comprehension efficiency.',
            thumbnail_url='https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=600&auto=format&fit=crop&q=80',
            category='Speed Reading',
            subject_id=sr_sub.id,
            difficulty='All Levels',
            duration='2 Weeks',
            status='published',
            is_featured=True,
            display_order=3
        )
        db.session.add_all([c1, c2, c3])
        db.session.flush()

        # Modules & Lessons for Vedic Maths
        m1 = CourseModule(course_id=c1.id, title='Module 1: Mental Arithmetic & Sutras', display_order=1)
        db.session.add(m1)
        db.session.flush()

        l1 = Lesson(
            course_id=c1.id,
            module_id=m1.id,
            subject_id=vm_sub.id,
            title='Fast Mental Multiplication Techniques',
            slug='fast-mental-multiplication-techniques',
            description='Learn Ekadhikena Purvena and Vertically & Crosswise techniques for instant mental calculations.',
            content='''# Vedic Maths: Fast Mental Calculations

Vedic Mathematics is an ancient Indian system of calculation based on 16 main Sutras (word-formulas).

## Key Benefits
- **Lightning Speed**: Solve complex arithmetic 10x faster than traditional methods.
- **Mental Agility**: Eliminates reliance on calculators.
- **Competition Readiness**: Prepares students for national-level speed challenges.

### Technique 1: Multiplication by 11
To multiply a 2-digit number by 11:
1. Separate the two digits.
2. Add the two digits together.
3. Place the sum in the middle!

Example: `45 x 11`
- 4 and 5 separated -> `4 _ 5`
- 4 + 5 = 9
- Result: **495**
''',
            video_url='https://www.youtube.com/embed/rfscVS0vtbw',
            duration='15 mins',
            display_order=1,
            is_published=True
        )
        l2 = Lesson(
            course_id=c2.id,
            module_id=None,
            subject_id=mem_sub.id,
            title='Mnemonic & Association Techniques',
            slug='mnemonic-association-techniques',
            description='Learn how to connect new concepts with vivid mental imagery for instant recall.',
            content='''# Memory Coaching: Mental Association & Mnemonics

Memory is built on association. By anchoring abstract information to vivid mental images, retention increases dramatically.

## Core Strategies
- **Visualization**: Make mental pictures bright, exaggerated, and active.
- **Peg System**: Associate numbers with predefined peg words.
- **Spaced Retrieval**: Re-visit key memories at strategic intervals.
''',
            video_url='https://www.youtube.com/embed/k9TUPpGqYTo',
            duration='20 mins',
            display_order=1,
            is_published=True
        )
        db.session.add_all([l1, l2])
        db.session.flush()

        # Quiz for Vedic Maths
        q1 = Quiz(
            course_id=c1.id,
            lesson_id=l1.id,
            title='Vedic Maths Speed Challenge',
            description='Test your mental calculation speed and sutra techniques.',
            time_limit_minutes=10,
            passing_score=70,
            is_published=True
        )
        db.session.add(q1)
        db.session.flush()

        qn1 = Question(
            quiz_id=q1.id,
            question_text='Using the Vedic Maths technique, what is 36 x 11?',
            question_type='single_choice',
            points=10,
            display_order=1,
            explanation='Separate 3 and 6, middle digit is 3 + 6 = 9. Answer is 396.'
        )
        db.session.add(qn1)
        db.session.flush()

        db.session.add_all([
            QuizOption(question_id=qn1.id, option_text='386', is_correct=False, display_order=1),
            QuizOption(question_id=qn1.id, option_text='396', is_correct=True, display_order=2),
            QuizOption(question_id=qn1.id, option_text='406', is_correct=False, display_order=3),
            QuizOption(question_id=qn1.id, option_text='366', is_correct=False, display_order=4)
        ])

        qn2 = Question(
            quiz_id=q1.id,
            question_text='Python is an interpreted programming language. True or False?',
            question_type='true_false',
            points=10,
            display_order=2,
            explanation='Yes, Python code is interpreted line-by-line by the Python interpreter.'
        )
        db.session.add(qn2)
        db.session.flush()

        db.session.add_all([
            QuizOption(question_id=qn2.id, option_text='True', is_correct=True, display_order=1),
            QuizOption(question_id=qn2.id, option_text='False', is_correct=False, display_order=2)
        ])

    # 11. Sample Announcements
    if not Announcement.query.first():
        a1 = Announcement(
            title='Admissions Open for Academic Year 2026-2027',
            slug='admissions-open-2026-2027',
            description='Annapoorni Academy invites applications for new structured learning programs across Science, Math, and Technology.',
            content='We are thrilled to announce that registration is now open for our upcoming batch of foundation and advanced courses. Early bird benefits available.',
            image_url='https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800&auto=format&fit=crop&q=80',
            category='Admission',
            status='published',
            is_featured=True
        )
        a2 = Announcement(
            title='National Science & Mathematics Olympiad Workshop',
            slug='national-science-math-olympiad-workshop',
            description='Join our intensive 2-day virtual workshop featuring guest lectures and problem-solving masterclasses.',
            content='Get ready for competitive academic challenges with live mentor guidance and interactive problem sets.',
            image_url='https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=800&auto=format&fit=crop&q=80',
            category='Workshop',
            status='published',
            is_featured=True
        )
        db.session.add_all([a1, a2])

    db.session.commit()
