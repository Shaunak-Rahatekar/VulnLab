import os
import uuid
import magic
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from config import VULN_MODE
from models import db, User, server_sessions

upload_bp = Blueprint('upload_module', __name__)

VULN_UPLOAD_DIR = os.path.join('static', 'uploads')
PATCHED_UPLOAD_DIR = os.path.join('safe_uploads')

# Ensure directories exist upon startup
os.makedirs(VULN_UPLOAD_DIR, exist_ok=True)
os.makedirs(PATCHED_UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/gif'}

def get_current_user():
    sid = session.get('session_id')
    user_data = server_sessions.get(sid)
    if user_data:
        return User.query.get(user_data['user_id'])
    return None

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    user = get_current_user()
    if not user:
        return redirect(url_for('sqli.login'))

    vuln_mode = VULN_MODE.get("upload", True)

    if request.method == 'GET':
        return render_template('upload.html', 
                               current_pic=user.profile_pic,
                               vuln_mode=vuln_mode)

    # Handle POST
    if 'profile_pic' not in request.files:
        flash('No file part provided.', 'error')
        return redirect(request.url)
        
    file = request.files['profile_pic']
    if file.filename == '':
        flash('No file was selected for upload.', 'error')
        return redirect(request.url)

    if vuln_mode:
        # VULNERABLE MODE:
        # 1. Saves using the exact original filename (allows directory traversal if not careful)
        # 2. No robust extension checking (naive blacklist that can be bypassed)
        # 3. Saves directly to a publicly accessible static directory
        filename = file.filename
        
        # Naive blacklist approach (blocking exact exact .php or .exe, but allowing .py or .PHP)
        if filename.endswith('.php') or filename.endswith('.exe'):
            flash('Disallowed file type!', 'error')
            return redirect(request.url)
            
        filepath = os.path.join(VULN_UPLOAD_DIR, filename)
        file.save(filepath)
        
        user.profile_pic = filename
        db.session.commit()
        flash(f'File uploaded successfully to /static/uploads/{filename}', 'success')
        
    else:
        # PATCHED MODE:
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        # 1. Strict Extension Whitelist check
        if ext not in ALLOWED_EXTENSIONS:
            flash('Upload rejected: Only JPG, PNG, and GIF files are allowed.', 'error')
            return redirect(request.url)
            
        # 2. Magic bytes / MIME type content validation
        # We read the first 2048 bytes of the file to verify it is actually an image
        file_content = file.read(2048)
        file.seek(0) # Reset the file cursor so it can be saved properly later
        
        mime_type = magic.from_buffer(file_content, mime=True)
        if mime_type not in ALLOWED_MIME_TYPES:
            flash('Upload rejected: Invalid file content detected (magic bytes mismatch).', 'error')
            return redirect(request.url)
            
        # 3. Rename file to a random UUID to prevent overwriting and predictable paths
        new_filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(PATCHED_UPLOAD_DIR, new_filename)
        
        # 4. Save in a non-public "safe" location
        file.save(filepath)
        
        user.profile_pic = new_filename
        db.session.commit()
        flash('File validated and uploaded securely.', 'success')

    return redirect(url_for('upload_module.upload'))

@upload_bp.route('/serve_file/<path:filename>')
def serve_file(filename):
    """
    In vulnerable mode, this route serves the file but it's redundant because the 
    files are already publicly accessible under /static/uploads/.
    In patched mode, this route strictly controls access to files in /safe_uploads/.
    """
    vuln_mode = VULN_MODE.get("upload", True)
    
    if vuln_mode:
        return send_from_directory(VULN_UPLOAD_DIR, filename)
    else:
        # Require authentication to view the image
        user = get_current_user()
        if not user:
            return "Unauthorized", 401
            
        secure_name = secure_filename(filename)
        return send_from_directory(PATCHED_UPLOAD_DIR, secure_name)
