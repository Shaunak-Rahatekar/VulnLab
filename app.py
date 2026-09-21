# app.py
from flask import Flask, redirect, url_for, session
from config import VULN_MODE
from models import db, seed_db
from modules.sqli import sqli_bp
from modules.search import search_bp
from modules.xss import xss_bp

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_vulnlab_sandbox'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vulnlab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Register module blueprints
app.register_blueprint(sqli_bp)
app.register_blueprint(search_bp)
app.register_blueprint(xss_bp)

# Create tables and seed data upon startup
with app.app_context():
    db.create_all()
    seed_db()

@app.route('/')
def index():
    return redirect(url_for('sqli.login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('sqli.login'))
    
    # A simple inline dashboard to demonstrate successful login
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head><title>Dashboard - VulnLab</title></head>
    <body style="font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f4f7f6; margin: 0;">
        <div style="background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
            <h1 style="color: #333; margin-top: 0;">Dashboard</h1>
            <p>Welcome, <strong>{session.get('username')}</strong>! You are logged in.</p>
            <p style="margin-top: 1.5rem;"><a href='/logout' style="color: white; background-color: #d9534f; padding: 0.5rem 1rem; text-decoration: none; border-radius: 4px;">Logout</a></p>
        </div>
    </body>
    </html>
    """

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('sqli.login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
