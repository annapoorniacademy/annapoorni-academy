-- Initial Seed Data for Annapoorni Academy V1.0

-- Admin (password: admin123)
INSERT INTO admins (username, email, password_hash)
VALUES ('admin', 'shinoansonanand@gmail.com', 'pbkdf2:sha256:260000$sQj9u3tW$b6118d3b84ca2557e4e0b0439c0d3fa78d2b271d4b6ec340d04c4146db796f63');

-- Website Settings
INSERT INTO website_settings (site_name, tagline, site_description, dark_mode_default)
VALUES (
    'Annapoorni Academy',
    'Empowering Minds, Shaping Futures',
    'Annapoorni Academy is a premier educational platform providing world-class courses, subjects, lessons, and interactive learning assessments.',
    FALSE
);

-- Theme Settings
INSERT INTO theme_settings (
    active_preset, primary_color, secondary_color, accent_color, background_color, text_color, card_color, button_color, header_color, footer_color, font_heading, font_body, is_published
) VALUES (
    'Academic', '#1E3A8A', '#0D9488', '#F59E0B', '#F8FAFC', '#0F172A', '#FFFFFF', '#1E3A8A', '#FFFFFF', '#0F172A', 'Outfit', 'Inter', TRUE
);

-- Homepage Sections
INSERT INTO homepage_sections (section_key, section_name, is_enabled, display_order, title, subtitle, cta_text, cta_url, secondary_cta_text, secondary_cta_url, background_style)
VALUES 
('hero', 'Hero Section', TRUE, 1, 'Learn Better. Grow Smarter.', 'Discover world-class educational courses, interactive subjects, structured lessons, and real-time assessments.', 'Explore Courses', '/courses', 'Browse Subjects', '/subjects', 'gradient'),
('about', 'About Section', TRUE, 2, 'Welcome to Annapoorni Academy', 'Committed to educational innovation, accessible learning, and comprehensive knowledge mastery.', 'Learn More About Us', '/about', NULL, NULL, 'default'),
('featured_courses', 'Featured Courses', TRUE, 3, 'Featured Courses', 'Handpicked premium courses designed by leading educators.', NULL, NULL, NULL, NULL, 'default'),
('benefits', 'Learning Benefits', TRUE, 4, 'Why Learn With Annapoorni Academy?', 'We provide an unmatched educational experience built for modern learners.', NULL, NULL, NULL, NULL, 'default'),
('testimonials', 'Testimonials', TRUE, 5, 'What Our Learners Say', 'Real feedback from students thriving at Annapoorni Academy.', NULL, NULL, NULL, NULL, 'default'),
('announcements', 'Announcements', TRUE, 6, 'Academy News & Updates', 'Stay informed with the latest notifications, workshops, and exam alerts.', NULL, NULL, NULL, NULL, 'default'),
('cta', 'Call To Action', TRUE, 7, 'Ready to Begin Your Educational Journey?', 'Explore our extensive library of subjects and take your knowledge to the next level today.', 'Get Started Free', '/courses', NULL, NULL, 'dark');

-- Navigation Items
INSERT INTO navigation_items (label, destination, display_order, is_enabled, is_external, location)
VALUES 
('Home', '/', 1, TRUE, FALSE, 'both'),
('About', '/about', 2, TRUE, FALSE, 'both'),
('Courses', '/courses', 3, TRUE, FALSE, 'both'),
('Subjects', '/subjects', 4, TRUE, FALSE, 'both'),
('Announcements', '/announcements', 5, TRUE, FALSE, 'both'),
('Contact', '/contact', 6, TRUE, FALSE, 'both');

-- Social Links
INSERT INTO social_links (platform, url, icon, display_order, is_enabled, show_in_header, show_in_footer, show_in_contact, show_in_homepage)
VALUES 
('Instagram', 'https://www.instagram.com/coachsindhuram?igsh=MXR4cmdvaHZveHZleA%3D%3D', 'Instagram', 1, TRUE, TRUE, TRUE, TRUE, TRUE),
('YouTube', 'https://youtube.com/@annapoorniacademy', 'Youtube', 2, FALSE, FALSE, FALSE, FALSE, FALSE),
('LinkedIn', 'https://www.linkedin.com/in/coach-sindhuram/', 'Linkedin', 3, TRUE, TRUE, TRUE, TRUE, TRUE),
('Facebook', 'https://facebook.com/annapoorniacademy', 'Facebook', 4, TRUE, TRUE, TRUE, TRUE, TRUE),
('X', 'https://x.com/annapoorni_edu', 'Twitter', 5, FALSE, FALSE, TRUE, TRUE, FALSE);

-- Contact Settings
INSERT INTO contact_settings (email, phone, whatsapp, address, working_hours, contact_form_recipient)
VALUES ('coach.sindhuram@gmail.com', '+91 90803 85589', '+919080385589', 'Coach Sindhu Ram Academy, Tamil Nadu, India', 'Monday - Saturday: 8:30 AM - 6:30 PM', 'coach.sindhuram@gmail.com');

-- SEO Settings
INSERT INTO seo_settings (site_title, meta_description, keywords, og_title, og_description)
VALUES ('Annapoorni Academy — Premier Educational Platform', 'Empowering minds with structured courses, subjects, video lessons, and interactive quizzes.', 'education, academy, courses, subjects, lessons, quizzes, annapoorni', 'Annapoorni Academy — Excellence in Education', 'Explore premier educational content and test your skills with interactive quizzes.');
