"""
LOS Solutions Ltd - Flask Web Application
Run: python app.py (dev) or gunicorn -w 4 app:app (prod)
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'los-solutions-secret-2026')

# ─── Email Configuration ───────────────────────────────────────────
MAIL_SERVER   = os.environ.get('MAIL_SERVER',   'smtp.gmail.com')
MAIL_PORT     = int(os.environ.get('MAIL_PORT', 587))
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')   # your Gmail
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')   # Gmail App Password
MAIL_RECIPIENT = 'louisazuamairo84@gmail.com'


# ─── Routes ───────────────────────────────────────────────────────
@app.route('/')
def index():
    """Serve the main landing page."""
    return render_template('index.html')


@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submissions and send email."""
    try:
        name    = request.form.get('name', '').strip()
        email   = request.form.get('email', '').strip()
        phone   = request.form.get('phone', 'Not provided').strip()
        service = request.form.get('service', 'General Enquiry').strip()
        subject = request.form.get('subject', 'Website Enquiry').strip()
        message = request.form.get('message', '').strip()

        if not all([name, email, message]):
            return jsonify({
                'success': False,
                'message': 'Please fill in all required fields.'
            }), 400

        _send_email(name, email, phone, service, subject, message)

        return jsonify({
            'success': True,
            'message': 'Thank you! Your message has been received. We will respond within 24 hours.'
        })

    except smtplib.SMTPAuthenticationError:
        return jsonify({
            'success': False,
            'message': 'Email configuration error. Please contact us directly.'
        }), 500
    except Exception as e:
        app.logger.error(f'Contact form error: {e}')
        return jsonify({
            'success': False,
            'message': 'Something went wrong. Please try again or contact us directly.'
        }), 500


# ─── Email Helper ─────────────────────────────────────────────────
def _send_email(name, email, phone, service, subject, message):
    """Send enquiry email via SMTP."""
    msg = MIMEMultipart('alternative')
    msg['From']    = MAIL_USERNAME or 'noreply@lossolutions.com'
    msg['To']      = MAIL_RECIPIENT
    msg['Subject'] = f'[LOS Solutions] New Enquiry: {subject}'
    msg['Reply-To'] = email

    # Plain-text version
    plain = f"""
New contact form submission from LOS Solutions Ltd website
═══════════════════════════════════════════════════════════

Name:    {name}
Email:   {email}
Phone:   {phone}
Service: {service}
Subject: {subject}

Message:
{message}

───────────────────────────────────────────────────────────
This message was sent via the LOS Solutions Ltd website contact form.
To reply, simply respond to this email (Reply-To: {email})
"""

    # HTML version
    html = f"""
<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px;">
  <div style="background:#04101f;padding:20px 30px;border-radius:8px 8px 0 0;">
    <h2 style="color:#0ea5e9;margin:0;font-size:1.4rem;">LOS Solutions Ltd</h2>
    <p style="color:#7fa3c8;margin:4px 0 0;font-size:.85rem;">New Contact Form Submission</p>
  </div>
  <div style="border:1px solid #e2e8f0;border-top:none;padding:30px;border-radius:0 0 8px 8px;">
    <table style="width:100%;border-collapse:collapse;">
      <tr><td style="padding:8px 0;color:#64748b;font-size:.85rem;width:100px;">Name</td>
          <td style="padding:8px 0;font-weight:600;">{name}</td></tr>
      <tr><td style="padding:8px 0;color:#64748b;font-size:.85rem;">Email</td>
          <td style="padding:8px 0;"><a href="mailto:{email}" style="color:#0ea5e9;">{email}</a></td></tr>
      <tr><td style="padding:8px 0;color:#64748b;font-size:.85rem;">Phone</td>
          <td style="padding:8px 0;">{phone}</td></tr>
      <tr><td style="padding:8px 0;color:#64748b;font-size:.85rem;">Service</td>
          <td style="padding:8px 0;">{service}</td></tr>
      <tr><td style="padding:8px 0;color:#64748b;font-size:.85rem;">Subject</td>
          <td style="padding:8px 0;font-weight:600;">{subject}</td></tr>
    </table>
    <div style="margin-top:20px;padding:16px;background:#f8fafc;border-radius:6px;border-left:3px solid #0ea5e9;">
      <p style="color:#64748b;font-size:.8rem;margin:0 0 6px;text-transform:uppercase;letter-spacing:.06em;">Message</p>
      <p style="margin:0;line-height:1.7;">{message}</p>
    </div>
    <p style="margin-top:20px;font-size:.8rem;color:#94a3b8;">
      Sent via <strong>lossolutions.com.ng</strong> &nbsp;|&nbsp; Reply directly to this email to respond.
    </p>
  </div>
</body>
</html>
"""

    msg.attach(MIMEText(plain, 'plain'))
    msg.attach(MIMEText(html,  'html'))

    if MAIL_USERNAME and MAIL_PASSWORD:
        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.send_message(msg)
    else:
        # Fallback: log to console if SMTP not configured
        app.logger.info(f'[EMAIL NOT CONFIGURED] Would have sent:\n{plain}')


# ─── Run ──────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
