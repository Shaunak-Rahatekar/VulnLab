# app.py
from flask import Flask, redirect, url_for, session
from config import VULN_MODE
from models import db, seed_db, server_sessions
from modules.sqli import sqli_bp
from modules.search import search_bp
from modules.xss import xss_bp
from modules.session_hijack import session_bp

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_vulnlab_sandbox'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vulnlab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session Cookie Configuration based on VULN_MODE
if VULN_MODE.get("session", True):
    # VULNERABLE: Cookies accessible via JS and sent over HTTP
    app.config['SESSION_COOKIE_HTTPONLY'] = False
else:
    # PATCHED: Cookies hidden from JS (blocks XSS hijacking)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize the database
db.init_app(app)

# Register module blueprints
app.register_blueprint(sqli_bp)
app.register_blueprint(search_bp)
app.register_blueprint(xss_bp)
app.register_blueprint(session_bp)

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
