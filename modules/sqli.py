# modules/sqli.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from sqlalchemy import text
from config import VULN_MODE
from models import db, User
from werkzeug.security import check_password_hash

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
                # Result is a Row object. Access by index: 0=id, 1=username
                session['user_id'] = result[0]
                session['username'] = result[1]
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password', 'error')
                
        else:
            # PATCHED MODE
            # Uses SQLAlchemy ORM which handles parameterized queries automatically
            user = User.query.filter_by(username=username).first()
            
            # Safely verify the password hash
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                session['username'] = user.username
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password', 'error')
                
    # Render the template and pass the vuln_mode flag for the footer
    return render_template('login.html', vuln_mode=VULN_MODE["sqli"])
