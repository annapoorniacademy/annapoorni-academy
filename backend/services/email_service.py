import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

logger = logging.getLogger(__name__)

def _get_email_config():
    """
    Extract and validate SMTP settings from environment variables.
    Defaults to Google Gmail (smtp.gmail.com:587 STARTTLS) with official academy identity.
    """
    official_email = os.environ.get('MAIL_FROM') or os.environ.get('MAIL_USERNAME') or 'annapoorniacademy@gmail.com'
    from_name = os.environ.get('MAIL_FROM_NAME', 'Annapoorni Academy')
    admin_recipient = os.environ.get('ADMIN_EMAIL') or official_email
    
    mail_server = os.environ.get('MAIL_SERVER', 'smtp.gmail.com').strip()
    if '@' in mail_server:
        mail_server = 'smtp.gmail.com'
    elif ':' in mail_server:
        mail_server = mail_server.split(':')[0]
    elif not mail_server:
        mail_server = 'smtp.gmail.com'

    try:
        mail_port = int(os.environ.get('MAIL_PORT', 587))
    except (ValueError, TypeError):
        mail_port = 587

    use_tls = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', '1', 'yes']
    mail_username = os.environ.get('MAIL_USERNAME', official_email).strip()
    mail_password = os.environ.get('MAIL_PASSWORD', '').strip()

    return {
        'official_email': official_email,
        'from_name': from_name,
        'admin_recipient': admin_recipient,
        'server': mail_server,
        'port': mail_port,
        'use_tls': use_tls,
        'username': mail_username,
        'password': mail_password,
        'has_credentials': bool(mail_username and mail_password)
    }

def send_email(to_email, subject, body_html, reply_to=None, from_name=None, plain_text=None):
    """
    Core email delivery utility.
    - Official sender identity: ALWAYS annapoorniacademy@gmail.com (or configured MAIL_FROM).
    - Supports custom Reply-To (e.g. applicant email) for easy 1-click replies.
    - Connects over SMTP with STARTTLS on port 587 (smtp.gmail.com).
    - Never logs passwords, App Passwords, or sensitive credentials.
    - Returns (success_boolean, status_message).
    """
    config = _get_email_config()
    sender_email = config['official_email']
    display_name = from_name or config['from_name']

    # Build MIME message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"{display_name} <{sender_email}>"
    msg['To'] = to_email
    if reply_to:
        msg['Reply-To'] = reply_to

    # Plain text fallback
    text_content = plain_text or "Please enable HTML in your email client to view this message from Annapoorni Academy."
    msg.attach(MIMEText(text_content, 'plain', 'utf-8'))
    msg.attach(MIMEText(body_html, 'html', 'utf-8'))

    # If credentials are configured, attempt real SMTP delivery
    if config['has_credentials']:
        try:
            server = smtplib.SMTP(config['server'], config['port'], timeout=12)
            if config['use_tls']:
                server.starttls()
            server.login(config['username'], config['password'])
            server.sendmail(sender_email, [to_email], msg.as_string())
            server.quit()
            logger.info(f"Email sent successfully to {to_email} (Subject: {subject})")
            return True, "Email sent successfully over Gmail SMTP."
        except Exception as e:
            # Safe sanitized logging - do NOT log credentials or trace auth details
            error_type = type(e).__name__
            logger.warning(f"SMTP delivery note ({error_type}): Email to {to_email} could not be dispatched via SMTP.")
            return False, f"SMTP delivery failed ({error_type}). Submission remains safely stored in database."
    else:
        # Development / Offline mode: credentials not set, log safely
        logger.info(f"Email logged (SMTP credentials not set). To: {to_email} | Subject: {subject}")
        return True, "Email recorded locally (SMTP credentials not configured)."

def send_contact_inquiry_emails(inquiry_data):
    """
    Handles dual email flow for contact form inquiries:
    1. Academy notification to annapoorniacademy@gmail.com (with Reply-To set to applicant)
    2. Confirmation copy to applicant
    """
    config = _get_email_config()
    applicant_name = inquiry_data.get('name', 'Visitor')
    applicant_email = inquiry_data.get('email', '')
    applicant_phone = inquiry_data.get('phone', 'N/A')
    learning_mode = inquiry_data.get('mode', 'General Inquiry')
    subject = inquiry_data.get('subject', 'General Inquiry')
    message = inquiry_data.get('message', '')
    inquiry_id = inquiry_data.get('id', 'N/A')
    sub_date = datetime.now().strftime('%d %b %Y, %I:%M %p')

    results = {
        'admin_notified': False,
        'applicant_confirmed': False
    }

    # 1. Academy Notification Email
    admin_subject = f"New Contact Inquiry from {applicant_name}: {subject}"
    admin_html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px;">
      <h2 style="color: #1e3a8a; margin-top: 0; border-bottom: 2px solid #1e3a8a; padding-bottom: 8px;">📬 New Website Contact Inquiry</h2>
      <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
        <tr><td style="padding: 6px 0; color: #64748b; width: 140px;"><strong>Inquiry ID:</strong></td><td>#{inquiry_id}</td></tr>
        <tr><td style="padding: 6px 0; color: #64748b;"><strong>Applicant Name:</strong></td><td>{applicant_name}</td></tr>
        <tr><td style="padding: 6px 0; color: #64748b;"><strong>Applicant Email:</strong></td><td><a href="mailto:{applicant_email}">{applicant_email}</a></td></tr>
        <tr><td style="padding: 6px 0; color: #64748b;"><strong>Phone / WhatsApp:</strong></td><td>{applicant_phone}</td></tr>
        <tr><td style="padding: 6px 0; color: #64748b;"><strong>Preferred Mode:</strong></td><td>{learning_mode}</td></tr>
        <tr><td style="padding: 6px 0; color: #64748b;"><strong>Subject:</strong></td><td>{subject}</td></tr>
        <tr><td style="padding: 6px 0; color: #64748b;"><strong>Received On:</strong></td><td>{sub_date}</td></tr>
      </table>
      <div style="background-color: #f8fafc; padding: 15px; border-radius: 6px; border-left: 4px solid #1e3a8a; margin: 15px 0;">
        <strong style="color: #0f172a;">Message:</strong>
        <p style="margin: 8px 0 0 0; color: #334155; white-space: pre-line;">{message}</p>
      </div>
      <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 20px;">
        💡 You can reply directly to this email to contact the applicant ({applicant_email}).
      </p>
    </div>
    """
    admin_ok, _ = send_email(
        to_email=config['admin_recipient'],
        subject=admin_subject,
        body_html=admin_html,
        reply_to=applicant_email,
        from_name="Annapoorni Academy Inquiries"
    )
    results['admin_notified'] = admin_ok

    # 2. Applicant Confirmation Email
    if applicant_email:
        student_subject = "We received your enquiry – Annapoorni Academy"
        student_html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px; color: #1e293b;">
          <h2 style="color: #1e3a8a; margin-top: 0;">We received your enquiry – Annapoorni Academy</h2>
          <p>Dear <strong>{applicant_name}</strong>,</p>
          <p>Thank you for contacting Annapoorni Academy. We have received your enquiry successfully. Our team will review your request and get back to you shortly.</p>
          
          <div style="background-color: #f8fafc; padding: 16px; border-radius: 8px; margin: 20px 0; border: 1px solid #e2e8f0;">
            <h4 style="margin-top: 0; color: #0f172a; margin-bottom: 10px;">Summary of Your Enquiry:</h4>
            <p style="margin: 4px 0;"><strong>Subject:</strong> {subject}</p>
            <p style="margin: 4px 0;"><strong>Preferred Learning Mode:</strong> {learning_mode}</p>
            <p style="margin: 4px 0;"><strong>Message:</strong> {message}</p>
          </div>

          <p style="margin-top: 20px;">
            For immediate queries, you can also reach us directly on WhatsApp:
          </p>
          <p>
            <a href="https://wa.me/919080385589" style="background-color: #25D366; color: #ffffff; padding: 10px 18px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
              💬 Chat on WhatsApp (+91 90803 85589)
            </a>
          </p>

          <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0;" />
          <p style="margin-bottom: 4px;">Regards,</p>
          <p style="margin: 0; font-weight: bold; color: #1e3a8a;">Annapoorni Academy</p>
          <p style="margin: 2px 0 0 0; color: #64748b; font-size: 0.9rem;">
            <a href="mailto:{config['official_email']}" style="color: #1e3a8a;">{config['official_email']}</a> | <a href="https://annapoorniacademy.com" style="color: #1e3a8a;">annapoorniacademy.com</a>
          </p>
        </div>
        """
        student_ok, _ = send_email(
            to_email=applicant_email,
            subject=student_subject,
            body_html=student_html,
            from_name="Annapoorni Academy"
        )
        results['applicant_confirmed'] = student_ok

    return results

def send_enrollment_emails(enrollment_data):
    """
    Handles dual email flow for course enrollment applications:
    1. Academy notification to annapoorniacademy@gmail.com (with Reply-To set to applicant)
    2. Confirmation email to applicant
    """
    config = _get_email_config()
    student_name = enrollment_data.get('student_name', 'Applicant')
    email = enrollment_data.get('email', '')
    phone = enrollment_data.get('phone', 'N/A')
    course_title = enrollment_data.get('course_title', 'Course')
    preferred_mode = enrollment_data.get('preferred_mode', 'Live Online via Zoom')
    message = enrollment_data.get('message', '')
    enrollment_id = enrollment_data.get('id', 'N/A')
    sub_date = datetime.now().strftime('%d %b %Y, %I:%M %p')

    results = {
        'admin_notified': False,
        'applicant_confirmed': False
    }

    # 1. Academy Notification Email
    admin_subject = f"New Enrollment Application: {student_name} - {course_title}"
    admin_html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px;">
      <h2 style="color: #1e3a8a; margin-top: 0; border-bottom: 2px solid #1e3a8a; padding-bottom: 8px;">🎓 New Course Enrollment Application</h2>
      <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
        <tr><td style="padding: 6px 0; color: #64748b; width: 150px;"><strong>Enrollment ID:</strong></td><td>#{enrollment_id}</td></tr>
        <tr><td style="padding: 6px 0; color: #64748b;"><strong>Course:</strong></td><td><strong>{course_title}</strong></td></tr>
        <tr><td style="padding: 6px 0; color: #64748b;"><strong>Applicant Name:</strong></td><td>{student_name}</td></tr>
        <tr><td style="padding: 6px 0; color: #64748b;"><strong>Email:</strong></td><td><a href="mailto:{email}">{email}</a></td></tr>
        <tr><td style="padding: 6px 0; color: #64748b;"><strong>Phone / WhatsApp:</strong></td><td>{phone}</td></tr>
        <tr><td style="padding: 6px 0; color: #64748b;"><strong>Learning Mode:</strong></td><td>{preferred_mode}</td></tr>
        <tr><td style="padding: 6px 0; color: #64748b;"><strong>Submission Date:</strong></td><td>{sub_date}</td></tr>
      </table>
      <div style="background-color: #f8fafc; padding: 15px; border-radius: 6px; border-left: 4px solid #1e3a8a; margin: 15px 0;">
        <strong style="color: #0f172a;">Applicant Notes / Details:</strong>
        <p style="margin: 8px 0 0 0; color: #334155; white-space: pre-line;">{message or 'None'}</p>
      </div>
      <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 20px;">
        💡 You can reply directly to this email to contact the applicant ({email}).
      </p>
    </div>
    """
    admin_ok, _ = send_email(
        to_email=config['admin_recipient'],
        subject=admin_subject,
        body_html=admin_html,
        reply_to=email,
        from_name="Annapoorni Academy Enrollments"
    )
    results['admin_notified'] = admin_ok

    # 2. Applicant Confirmation Email
    if email:
        student_subject = "Application Received – Annapoorni Academy"
        student_html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px; color: #1e293b;">
          <h2 style="color: #1e3a8a; margin-top: 0;">Application Received – Annapoorni Academy</h2>
          <p>Dear <strong>{student_name}</strong>,</p>
          <p>Thank you for submitting your course enrollment application for <strong>{course_title}</strong> with Coach Sindhu Ram at Annapoorni Academy.</p>
          
          <p>We have successfully received your application. Our team will review the details and contact you shortly with the upcoming batch schedules, syllabus, and onboarding instructions.</p>

          <div style="background-color: #f8fafc; padding: 16px; border-radius: 8px; margin: 20px 0; border: 1px solid #e2e8f0;">
            <h4 style="margin-top: 0; color: #0f172a; margin-bottom: 10px;">Your Application Details:</h4>
            <p style="margin: 4px 0;"><strong>Course:</strong> {course_title}</p>
            <p style="margin: 4px 0;"><strong>Selected Mode:</strong> {preferred_mode}</p>
            <p style="margin: 4px 0;"><strong>Contact Phone:</strong> {phone}</p>
          </div>

          <p style="margin-top: 20px;">
            If you have any questions or want to confirm batch timings immediately, feel free to chat with us directly:
          </p>
          <p>
            <a href="https://wa.me/919080385589" style="background-color: #25D366; color: #ffffff; padding: 10px 18px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
              💬 Connect on WhatsApp (+91 90803 85589)
            </a>
          </p>

          <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0;" />
          <p style="margin-bottom: 4px;">Regards,</p>
          <p style="margin: 0; font-weight: bold; color: #1e3a8a;">Annapoorni Academy</p>
          <p style="margin: 2px 0 0 0; color: #64748b; font-size: 0.9rem;">
            <a href="mailto:{config['official_email']}" style="color: #1e3a8a;">{config['official_email']}</a> | <a href="https://annapoorniacademy.com" style="color: #1e3a8a;">annapoorniacademy.com</a>
          </p>
        </div>
        """
        student_ok, _ = send_email(
            to_email=email,
            subject=student_subject,
            body_html=student_html,
            from_name="Annapoorni Academy"
        )
        results['applicant_confirmed'] = student_ok

    return results

# Backward compatibility wrappers
def send_admin_email_notification(subject, body_html, recipient=None):
    config = _get_email_config()
    target = recipient or config['admin_recipient']
    return send_email(to_email=target, subject=subject, body_html=body_html, from_name="Annapoorni Academy Notifications")

def send_student_confirmation_email(recipient_email, student_name, subject, body_html):
    return send_email(to_email=recipient_email, subject=subject, body_html=body_html, from_name="Annapoorni Academy")
