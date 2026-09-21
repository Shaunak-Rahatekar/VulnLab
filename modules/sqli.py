# modules/sqli.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from sqlalchemy import text
from config import VULN_MODE
from models import db, User, server_sessions
from werkzeug.security import check_password_hash
import uuid

sqli_bp = Blueprint('sqli', __name__)

@sqli_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        if VULN_MODE["sqli"]:
            # VULNERABLE MODE
            # Direct string concatenation allowing SQL Injection.
            # Example payload: ' OR '1'='1
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            
            # Execute directly without sanitization or parameterization
            result = db.session.execute(text(query)).fetchone()
            
            if result:
                # Session Fixation / Hijacking Logic
                if VULN_MODE.get("session", True):
                    # VULNERABLE: Reuse existing session ID (Fixation)
                    if 'session_id' not in session:
                        session['session_id'] = str(uuid.uuid4())
                else:
                    # PATCHED: Clear session completely and generate a new session ID
                    session.clear()
                    session['session_id'] = str(uuid.uuid4())
                
                # Store auth state server-side tied to this session_id
                server_sessions[session['session_id']] = {'user_id': result[0], 'username': result[1]}
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password', 'error')
                
        else:
            # PATCHED MODE
            # Uses SQLAlchemy ORM which handles parameterized queries automatically
            user = User.query.filter_by(username=username).first()
            
            # Safely verify the password hash
            if user and check_password_hash(user.password_hash, password):
                if VULN_MODE.get("session", True):
                    if 'session_id' not in session:
                        session['session_id'] = str(uuid.uuid4())
                else:
                    session.clear()
                    session['session_id'] = str(uuid.uuid4())
                    
                server_sessions[session['session_id']] = {'user_id': user.id, 'username': user.username}
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password', 'error')
                
    # Render the template and pass the vuln_mode flag for the footer
    return render_template('login.html', vuln_mode=VULN_MODE["sqli"])
