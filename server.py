#!/usr/bin/env python3
"""
Simple contact form backend for Frame & Light portfolio
Saves submissions and sends email notifications
"""

import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
SUBMISSIONS_FILE = 'submissions.json'
EMAIL_CONFIG = {
    'sender': os.getenv('EMAIL_USER', 'your-email@gmail.com'),
    'password': os.getenv('EMAIL_PASS', ''),
    'owner_email': os.getenv('OWNER_EMAIL', 'adnanshora180899@gmail.com'),
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}

class ContactFormHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """Handle form submissions"""
        if self.path == '/api/contact':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(body)
                
                # Validate required fields
                required_fields = ['name', 'email', 'projectType', 'message']
                if not all(field in data for field in required_fields):
                    self.send_error(400, 'Missing required fields')
                    return
                
                # Save submission
                submissions = load_submissions()
                submissions.append({
                    'id': int(datetime.now().timestamp() * 1000),
                    'name': data.get('name'),
                    'email': data.get('email'),
                    'phone': data.get('phone', ''),
                    'projectType': data.get('projectType'),
                    'message': data.get('message'),
                    'timestamp': data.get('timestamp'),
                    'receivedAt': datetime.now().isoformat()
                })
                save_submissions(submissions)
                
                # Try to send email
                if EMAIL_CONFIG['password']:
                    send_email(data)
                else:
                    print('[INFO] Email not configured - submission saved to submissions.json')
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
                
                print(f"[NEW SUBMISSION] From {data.get('name')} ({data.get('email')})")
                
            except json.JSONDecodeError:
                self.send_error(400, 'Invalid JSON')
        
        elif self.path == '/api/submissions':
            submissions = load_submissions()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(submissions).encode())
        
        else:
            self.send_error(404)

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/api/submissions':
            submissions = load_submissions()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(submissions).encode())
        
        elif self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'Server is running'}).encode())
        
        else:
            # Serve static files
            file_path = self.path.lstrip('/')
            if not file_path:
                file_path = 'site/index.html'
            else:
                file_path = f'site/{file_path}'
            
            if os.path.exists(file_path):
                self.send_response(200)
                
                # Determine content type
                if file_path.endswith('.html'):
                    content_type = 'text/html'
                elif file_path.endswith('.css'):
                    content_type = 'text/css'
                elif file_path.endswith('.js'):
                    content_type = 'application/javascript'
                elif file_path.endswith(('.jpg', '.jpeg')):
                    content_type = 'image/jpeg'
                elif file_path.endswith('.png'):
                    content_type = 'image/png'
                else:
                    content_type = 'application/octet-stream'
                
                self.send_header('Content-Type', content_type)
                self.end_headers()
                
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404)

    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def load_submissions():
    """Load submissions from JSON file"""
    if os.path.exists(SUBMISSIONS_FILE):
        try:
            with open(SUBMISSIONS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_submissions(submissions):
    """Save submissions to JSON file"""
    with open(SUBMISSIONS_FILE, 'w') as f:
        json.dump(submissions, f, indent=2)

def send_email(data):
    """Send email notifications"""
    try:
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone', 'Not provided')
        project_type = data.get('projectType')
        message = data.get('message')
        
        # Email to owner
        owner_subject = f"New Inquiry: {project_type} - From {name}"
        owner_html = f"""
        <h2>New Portfolio Inquiry</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
        <p><strong>Phone:</strong> {phone}</p>
        <p><strong>Project Type:</strong> {project_type}</p>
        <h3>Message:</h3>
        <p>{message.replace(chr(10), '<br>')}</p>
        <hr>
        <p><em>Received: {datetime.now().isoformat()}</em></p>
        """
        
        send_email_message(
            EMAIL_CONFIG['owner_email'],
            owner_subject,
            owner_html
        )
        
        # Confirmation email to visitor
        visitor_subject = "Thank you for your inquiry - Frame & Light"
        visitor_html = f"""
        <p>Thank you for reaching out, <strong>{name}</strong>!</p>
        <p>I've received your inquiry about <strong>{project_type}</strong>. I'll review your message and get back to you as soon as possible.</p>
        <p>Looking forward to working with you!</p>
        <p>Best regards,<br><strong>Frame & Light</strong></p>
        """
        
        send_email_message(email, visitor_subject, visitor_html)
        
        print("[EMAIL] Notifications sent successfully")
        
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")

def send_email_message(recipient, subject, html_body):
    """Send a single email"""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = EMAIL_CONFIG['sender']
    msg['To'] = recipient
    
    part = MIMEText(html_body, 'html')
    msg.attach(part)
    
    with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
        server.starttls()
        server.login(EMAIL_CONFIG['sender'], EMAIL_CONFIG['password'])
        server.send_message(msg)

if __name__ == '__main__':
    PORT = int(os.getenv('PORT', 3000))
    server = HTTPServer(('localhost', PORT), ContactFormHandler)
    
    print(f"""
╔════════════════════════════════════════╗
║   Frame & Light Portfolio Server       ║
║   Running on http://localhost:{PORT}   ║
╚════════════════════════════════════════╝

📸 Site: http://localhost:{PORT}
📧 Contact form submissions saved to: submissions.json

✅ Form is ready to use!

To test:
1. Go to http://localhost:{PORT}/#contact
2. Fill out the form and submit
3. Check submissions.json for saved data

📧 Email notifications:
   - Currently DISABLED (no EMAIL_PASS set)
   - To enable, set EMAIL_USER and EMAIL_PASS environment variables
    """)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[STOP] Server stopped")
