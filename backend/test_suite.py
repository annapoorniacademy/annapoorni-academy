import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app import app
from extensions import db
from models.admin import Admin
from models.course import Course
from models.subject import Subject
from models.inquiry import ContactInquiry
from models.enrollment import Enrollment
from services.email_service import _get_email_config, send_email, send_contact_inquiry_emails, send_enrollment_emails

class AnnapoorniAcademyTestSuite(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def _get_admin_token(self):
        login_res = self.client.post('/api/admin/login', json={'username': 'admin', 'password': '$12345678'}, content_type='application/json')
        return login_res.get_json()['token']

    # =========================================================================
    # 1. Official Email & Submission Flow Tests
    # =========================================================================

    def test_01_contact_submission_saves_successfully(self):
        """Test 1: Contact form submission saves inquiry successfully in database"""
        unique_name = "Jane Doe Inquiry Test"
        unique_email = "jane.doe.test@example.com"
        res = self.client.post('/api/contact/inquiry', json={
            'name': unique_name,
            'email': unique_email,
            'phone': '+91 90803 85589',
            'mode': 'Live Online via Zoom',
            'subject': 'Vedic Maths Query',
            'message': 'I would like more information on upcoming batches.'
        }, content_type='application/json')
        self.assertEqual(res.status_code, 201, "Contact submission should return 201 Created")
        data = res.get_json()
        self.assertIn('inquiry', data)
        self.assertEqual(data['inquiry']['email'], unique_email)
        
        # Verify persistence in DB
        inquiry_in_db = ContactInquiry.query.filter_by(email=unique_email).first()
        self.assertIsNotNone(inquiry_in_db, "Inquiry must be saved in database")
        self.assertEqual(inquiry_in_db.name, unique_name)

    @patch('services.email_service.send_email')
    def test_02_contact_submission_attempts_academy_notification(self, mock_send_email):
        """Test 2: Contact submission attempts academy notification to official email with Reply-To"""
        mock_send_email.return_value = (True, "Sent")
        inquiry_data = {
            'id': 991,
            'name': 'Ramesh Kumar',
            'email': 'ramesh.kumar@example.com',
            'phone': '+91 90803 85589',
            'mode': 'In-Person Offline',
            'subject': 'Memory Coaching',
            'message': 'Looking for weekend batch.'
        }
        results = send_contact_inquiry_emails(inquiry_data)
        self.assertTrue(results['admin_notified'])
        
        # Verify academy notification call
        calls = mock_send_email.call_args_list
        admin_call = next((c for c in calls if 'New Contact Inquiry' in c.kwargs.get('subject', '')), None)
        self.assertIsNotNone(admin_call, "Academy notification email must be triggered")
        self.assertIn('annapoorniacademy@gmail.com', admin_call.kwargs.get('to_email'))
        self.assertEqual(admin_call.kwargs.get('reply_to'), 'ramesh.kumar@example.com')

    @patch('services.email_service.send_email')
    def test_03_contact_submission_attempts_applicant_confirmation(self, mock_send_email):
        """Test 3: Contact submission attempts applicant confirmation copy"""
        mock_send_email.return_value = (True, "Sent")
        inquiry_data = {
            'id': 992,
            'name': 'Pooja Sharma',
            'email': 'pooja.sharma@example.com',
            'phone': '+91 9123456789',
            'mode': 'Live Online via Zoom',
            'subject': 'Speed Reading Enquiry',
            'message': 'Interested in 1-on-1 session.'
        }
        results = send_contact_inquiry_emails(inquiry_data)
        self.assertTrue(results['applicant_confirmed'])
        
        calls = mock_send_email.call_args_list
        student_call = next((c for c in calls if 'We received your enquiry' in c.kwargs.get('subject', '')), None)
        self.assertIsNotNone(student_call, "Applicant confirmation email must be triggered")
        self.assertEqual(student_call.kwargs.get('to_email'), 'pooja.sharma@example.com')

    def test_04_enrollment_submission_saves_successfully(self):
        """Test 4: Enrollment submission saves enrollment record successfully in database"""
        unique_student = "Deepak Verma Student"
        unique_email = "deepak.verma@example.com"
        res = self.client.post('/api/courses/1/enroll', json={
            'student_name': unique_student,
            'email': unique_email,
            'phone': '+91 90803 85589',
            'preferred_mode': 'Live Online via Zoom',
            'message': 'Ready to start immediately.'
        }, content_type='application/json')
        self.assertEqual(res.status_code, 201, "Enrollment submission should return 201 Created")
        data = res.get_json()
        self.assertIn('enrollment', data)
        self.assertEqual(data['enrollment']['email'], unique_email)

        # Verify DB persistence
        enr_in_db = Enrollment.query.filter_by(email=unique_email).first()
        self.assertIsNotNone(enr_in_db, "Enrollment record must be saved in database")
        self.assertEqual(enr_in_db.student_name, unique_student)

    @patch('services.email_service.send_email')
    def test_05_enrollment_submission_attempts_academy_notification(self, mock_send_email):
        """Test 5: Enrollment submission attempts internal notification to official academy email"""
        mock_send_email.return_value = (True, "Sent")
        enrollment_data = {
            'id': 881,
            'student_name': 'Kavita Sundar',
            'email': 'kavita.sundar@example.com',
            'phone': '+91 90803 85589',
            'course_title': 'Speed Reading Mastery',
            'preferred_mode': 'Live Online via Zoom',
            'message': 'Evening batch preferred.'
        }
        results = send_enrollment_emails(enrollment_data)
        self.assertTrue(results['admin_notified'])

        calls = mock_send_email.call_args_list
        admin_call = next((c for c in calls if 'New Enrollment Application' in c.kwargs.get('subject', '')), None)
        self.assertIsNotNone(admin_call)
        self.assertIn('annapoorniacademy@gmail.com', admin_call.kwargs.get('to_email'))
        self.assertEqual(admin_call.kwargs.get('reply_to'), 'kavita.sundar@example.com')

    @patch('services.email_service.send_email')
    def test_06_enrollment_submission_attempts_applicant_confirmation(self, mock_send_email):
        """Test 6: Enrollment submission attempts confirmation email to applicant"""
        mock_send_email.return_value = (True, "Sent")
        enrollment_data = {
            'id': 882,
            'student_name': 'Aarav Patel',
            'email': 'aarav.patel@example.com',
            'phone': '+91 9776655443',
            'course_title': 'Memory Coaching for Champions',
            'preferred_mode': 'Live Online via Zoom',
            'message': 'Registration confirmation check.'
        }
        results = send_enrollment_emails(enrollment_data)
        self.assertTrue(results['applicant_confirmed'])

        calls = mock_send_email.call_args_list
        student_call = next((c for c in calls if 'Application Received' in c.kwargs.get('subject', '')), None)
        self.assertIsNotNone(student_call)
        self.assertEqual(student_call.kwargs.get('to_email'), 'aarav.patel@example.com')

    @patch('smtplib.SMTP')
    def test_07_email_failure_preserves_database_record(self, mock_smtp):
        """Test 7: If email sending fails (SMTP error), database record is safely preserved and API returns 201"""
        # Configure SMTP mock to raise an exception
        mock_smtp.side_effect = Exception("Connection to smtp.gmail.com timed out")
        
        with patch.dict(os.environ, {
            'MAIL_USERNAME': 'annapoorniacademy@gmail.com',
            'MAIL_PASSWORD': 'test_mock_password'
        }):
            res = self.client.post('/api/contact/inquiry', json={
                'name': 'Fault Tolerance Tester',
                'email': 'fault.tester@example.com',
                'phone': '+91 90803 85589',
                'mode': 'Live Online via Zoom',
                'subject': 'Testing SMTP Failure Tolerance',
                'message': 'This submission must stay saved even if SMTP fails.'
            }, content_type='application/json')
            
            self.assertEqual(res.status_code, 201, "API must return 201 even if SMTP fails")
            data = res.get_json()
            self.assertIn('inquiry', data)
            
            # Verify record is still safely in DB
            db_record = ContactInquiry.query.filter_by(email='fault.tester@example.com').first()
            self.assertIsNotNone(db_record, "Database record must remain saved when SMTP fails")

    def test_08_no_email_credentials_exposed_in_api_responses(self):
        """Test 8: Ensure no email credentials or SMTP secrets are exposed in public or admin API responses"""
        # 1. Public contact response
        res = self.client.post('/api/contact/inquiry', json={
            'name': 'Security Check',
            'email': 'security.check@example.com',
            'phone': '+91 90803 85589',
            'message': 'Checking response body.'
        }, content_type='application/json')
        resp_str = json.dumps(res.get_json())
        self.assertNotIn('MAIL_PASSWORD', resp_str)
        self.assertNotIn('smtp_pass', resp_str)
        self.assertNotIn('password', resp_str)

        # 2. Public settings response
        settings_res = self.client.get('/api/contact')
        settings_str = json.dumps(settings_res.get_json())
        self.assertNotIn('MAIL_PASSWORD', settings_str)
        self.assertNotIn('password', settings_str)

    def test_09_email_sender_is_always_official_gmail(self):
        """Test 9: Official sender identity is always annapoorniacademy@gmail.com"""
        config = _get_email_config()
        self.assertEqual(config['official_email'], 'annapoorniacademy@gmail.com')
        
        with patch('smtplib.SMTP') as mock_smtp_class:
            mock_server = MagicMock()
            mock_smtp_class.return_value = mock_server
            with patch.dict(os.environ, {'MAIL_PASSWORD': 'dummy'}):
                send_email(
                    to_email='student@example.com',
                    subject='Test Subject',
                    body_html='<p>Test</p>'
                )
                # Verify sendmail envelope sender
                args, _ = mock_server.sendmail.call_args
                self.assertEqual(args[0], 'annapoorniacademy@gmail.com')

    def test_10_applicant_email_used_as_reply_to(self):
        """Test 10: Applicant email is set as Reply-To on academy notifications"""
        with patch('smtplib.SMTP') as mock_smtp_class:
            mock_server = MagicMock()
            mock_smtp_class.return_value = mock_server
            with patch.dict(os.environ, {'MAIL_PASSWORD': 'dummy'}):
                send_email(
                    to_email='annapoorniacademy@gmail.com',
                    subject='Inquiry from Student',
                    body_html='<p>Body</p>',
                    reply_to='student.applicant@example.com'
                )
                # Verify that message headers contain Reply-To
                args, _ = mock_server.sendmail.call_args
                raw_msg = args[2]
                self.assertIn('Reply-To: student.applicant@example.com', raw_msg)

    # =========================================================================
    # 2. Core Platform & Admin System Tests
    # =========================================================================

    def test_11_admin_login(self):
        """Test 11: Admin authentication with updated credentials"""
        res = self.client.post('/api/admin/login', json={
            'username': 'admin',
            'password': '$12345678'
        }, content_type='application/json')
        self.assertEqual(res.status_code, 200, "Admin login should return 200 OK")
        data = res.get_json()
        self.assertIn('token', data, "Login response must contain JWT token")

    def test_12_public_courses_and_subjects_api(self):
        """Test 12: Public courses and subjects endpoints"""
        c_res = self.client.get('/api/courses')
        self.assertEqual(c_res.status_code, 200)
        self.assertIsInstance(c_res.get_json(), list)

        s_res = self.client.get('/api/subjects')
        self.assertEqual(s_res.status_code, 200)
        self.assertIsInstance(s_res.get_json(), list)

    def test_13_production_health_and_seo(self):
        """Test 13: Production health check /health and dynamic SEO endpoints"""
        h_res = self.client.get('/health')
        self.assertEqual(h_res.status_code, 200)
        self.assertEqual(h_res.get_json()['status'], 'healthy')

        r_res = self.client.get('/robots.txt')
        self.assertEqual(r_res.status_code, 200)
        self.assertIn('User-agent:', r_res.get_data(as_text=True))

        sm_res = self.client.get('/sitemap.xml')
        self.assertEqual(sm_res.status_code, 200)
        self.assertIn('urlset', sm_res.get_data(as_text=True))

    def test_14_admin_dashboard_and_backup(self):
        """Test 14: Admin dashboard metrics and JSON backup export"""
        token = self._get_admin_token()
        dash_res = self.client.get('/api/admin/dashboard', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(dash_res.status_code, 200)
        self.assertIn('metrics', dash_res.get_json())

        bk_res = self.client.get('/api/admin/backup/export', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(bk_res.status_code, 200)
        self.assertEqual(bk_res.get_json()['version'], '2.0.0')

if __name__ == '__main__':
    unittest.main()
