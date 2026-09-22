from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import VULN_MODE
from models import db, User, server_sessions

csrf_bp = Blueprint('csrf_module', __name__)

@csrf_bp.route('/profile', methods=['GET'])
def profile():
    sid = session.get('session_id')
    user_data = server_sessions.get(sid)
    
    if not user_data:
        return redirect(url_for('sqli.login'))
        
    user = User.query.get(user_data['user_id'])
    
    return render_template('profile.html',
                           username=user.username,
                           current_email=user.email,
                           vuln_mode=VULN_MODE.get("csrf", True))

@csrf_bp.route('/change-email', methods=['POST'])
def change_email():
    sid = session.get('session_id')
    user_data = server_sessions.get(sid)
    
    if not user_data:
        return redirect(url_for('sqli.login'))
        
    new_email = request.form.get('new_email')
    
    user = User.query.get(user_data['user_id'])
    if user and new_email:
        user.email = new_email
        db.session.commit()
        # In a real app we'd flash a message here, but we redirect immediately
        
    return redirect(url_for('csrf_module.profile'))
