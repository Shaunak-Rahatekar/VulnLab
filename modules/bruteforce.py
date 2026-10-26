# modules/bruteforce.py
import time
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from werkzeug.security import check_password_hash
from models import db, User, server_sessions
from config import VULN_MODE
import uuid

bruteforce_bp = Blueprint('bruteforce', __name__)

# In-memory dictionary tracking failed attempts per IP: {ip: [timestamp1, timestamp2, ...]}
FAILED_ATTEMPTS = {}
LOCKOUT_THRESHOLD = 5
LOCKOUT_WINDOW_SECONDS = 60

@bruteforce_bp.route('/login_bruteforce', methods=['GET', 'POST'])
def login_bruteforce():
    vuln_mode = VULN_MODE.get("bruteforce", True)
    client_ip = request.remote_addr or '127.0.0.1'
    now = time.time()
    
    # Clean up expired attempt records
    if client_ip in FAILED_ATTEMPTS:
        FAILED_ATTEMPTS[client_ip] = [t for t in FAILED_ATTEMPTS[client_ip] if now - t < LOCKOUT_WINDOW_SECONDS]

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Check rate-limiting in Patched Mode
        if not vuln_mode:
            attempts = FAILED_ATTEMPTS.get(client_ip, [])
            if len(attempts) >= LOCKOUT_THRESHOLD:
                remaining = int(LOCKOUT_WINDOW_SECONDS - (now - attempts[0]))
                flash(f"⛔ Rate Limit Exceeded: Account temporarily locked due to {LOCKOUT_THRESHOLD} failed attempts. Try again in {remaining} seconds.", "error")
                return render_template('login_bruteforce.html', 
                                       vuln_mode=vuln_mode, 
                                       attempts_count=len(attempts), 
                                       locked=True), 429

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            # Reset failed count on successful authentication
            if client_ip in FAILED_ATTEMPTS:
                del FAILED_ATTEMPTS[client_ip]
                
            session.clear()
            session['session_id'] = str(uuid.uuid4())
            server_sessions[session['session_id']] = {'user_id': user.id, 'username': user.username}
            
            # Unlock Level 10
            current_app.config['COMPLETED_LEVELS'].add(10)
            flash(f"Success! Authenticated as {username}.", "success")
            return redirect(url_for('dashboard'))
        else:
            # Record failed attempt
            if client_ip not in FAILED_ATTEMPTS:
                FAILED_ATTEMPTS[client_ip] = []
            FAILED_ATTEMPTS[client_ip].append(now)
            
            attempts_remaining = max(0, LOCKOUT_THRESHOLD - len(FAILED_ATTEMPTS[client_ip]))
            if vuln_mode:
                flash(f"Invalid credentials. (Unrestricted: {len(FAILED_ATTEMPTS[client_ip])} attempts made without rate limit)", "error")
            else:
                flash(f"Invalid credentials. Attempts remaining before lockout: {attempts_remaining}", "error")

    current_attempts = len(FAILED_ATTEMPTS.get(client_ip, []))
    return render_template('login_bruteforce.html', 
                           vuln_mode=vuln_mode, 
                           attempts_count=current_attempts,
                           locked=(not vuln_mode and current_attempts >= LOCKOUT_THRESHOLD))
