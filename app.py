# app.py
from flask import Flask, redirect, url_for, session, render_template
from config import VULN_MODE
from models import db, seed_db, server_sessions
from modules.sqli import sqli_bp
from modules.search import search_bp
from modules.xss import xss_bp
from modules.session_hijack import session_bp
from modules.csrf_module import csrf_bp
from modules.upload_module import upload_bp
from modules.file_inclusion import traversal_bp
from modules.security_headers import headers_bp
from modules.bruteforce import bruteforce_bp
from modules.recon import recon_bp
from modules.report import report_bp
from modules.admin_manager import admin_mgr_bp
from modules.detector import detector_bp, init_detector
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_vulnlab_sandbox'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vulnlab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Progress tracker for the sidebar (stores the level numbers that have been successfully exploited)
app.config['COMPLETED_LEVELS'] = set()

@app.context_processor
def inject_sidebar_data():
    return dict(
        completed_levels=app.config.get('COMPLETED_LEVELS', set()),
        vuln_mode_dict=VULN_MODE
    )

# Session Cookie Configuration based on VULN_MODE
if VULN_MODE.get("session", True):
    app.config['SESSION_COOKIE_HTTPONLY'] = False
else:
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
    
# Initialize CSRF Protection
csrf = CSRFProtect(app)

if VULN_MODE.get("csrf", True):
    app.config['WTF_CSRF_ENABLED'] = False
else:
    app.config['WTF_CSRF_ENABLED'] = True

# Exempt non-CSRF blueprints so they function across modes
csrf.exempt(sqli_bp)
csrf.exempt(search_bp)
csrf.exempt(xss_bp)
csrf.exempt(session_bp)
csrf.exempt(upload_bp)
csrf.exempt(traversal_bp)
csrf.exempt(headers_bp)
csrf.exempt(bruteforce_bp)
csrf.exempt(recon_bp)
csrf.exempt(report_bp)
csrf.exempt(admin_mgr_bp)

# Initialize the database
db.init_app(app)

# Register module blueprints
app.register_blueprint(sqli_bp)
app.register_blueprint(search_bp)
app.register_blueprint(xss_bp)
app.register_blueprint(session_bp)
app.register_blueprint(csrf_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(traversal_bp)
app.register_blueprint(headers_bp)
app.register_blueprint(bruteforce_bp)
app.register_blueprint(recon_bp)
app.register_blueprint(report_bp)
app.register_blueprint(admin_mgr_bp)
app.register_blueprint(detector_bp)

# Apply global security headers middleware (Unit IV: Security Headers)
@app.after_request
def apply_security_headers(response):
    if not VULN_MODE.get("headers", True):
        # PATCHED: Inject defense-in-depth headers
        response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' https://fonts.googleapis.com; img-src 'self' data:; frame-src 'self';"
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    else:
        # VULNERABLE: Omit hardening headers and leak server banner (Unit II: Reconnaissance)
        response.headers['Server'] = 'Werkzeug/3.0.1 Python/3.11'
        response.headers['X-Powered-By'] = 'VulnLab-Educational-Platform'
    return response

# Initialize the WAF detection middleware
init_detector(app)

# Create tables and seed data upon startup
with app.app_context():
    db.create_all()
    seed_db()

@app.route('/')
def index():
    return redirect(url_for('sqli.login'))

@app.route('/dashboard')
def dashboard():
    sid = session.get('session_id')
    user_data = server_sessions.get(sid)
    
    if not user_data:
        return redirect(url_for('sqli.login'))
    
    return render_template('dashboard.html', 
                           username=user_data['username'],
                           vuln_mode=VULN_MODE.get("session", True))

@app.route('/logout')
def logout():
    sid = session.get('session_id')
    if sid in server_sessions:
        del server_sessions[sid]
    session.clear()
    return redirect(url_for('sqli.login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
