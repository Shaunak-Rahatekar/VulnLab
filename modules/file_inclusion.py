# modules/file_inclusion.py
import os
from flask import Blueprint, render_template, request, flash, current_app
from werkzeug.utils import safe_join
from config import VULN_MODE

traversal_bp = Blueprint('file_inclusion', __name__)

DOCS_DIR = os.path.abspath('docs')

ALLOWED_DOCS = {
    'privacy_policy.txt': 'Privacy Policy',
    'terms_of_service.txt': 'Terms of Service',
    'confidential_memo.txt': 'Internal Memorandum'
}

@traversal_bp.route('/view_doc', methods=['GET'])
def view_doc():
    filename = request.args.get('file', 'privacy_policy.txt')
    vuln_mode = VULN_MODE.get("traversal", True)
    file_content = ""
    error_msg = ""
    resolved_path = ""

    if vuln_mode:
        # VULNERABLE MODE (Directory Traversal / LFI)
        # Directly concatenates user input to the directory path without sanitization.
        # An attacker can traverse directories using '../' (e.g., ?file=../../app.py)
        try:
            target_path = os.path.join(DOCS_DIR, filename)
            resolved_path = os.path.abspath(target_path)
            
            with open(target_path, 'r', encoding='utf-8', errors='replace') as f:
                file_content = f.read()
                
            # If path climbing was used, unlock Level 8
            if '..' in filename:
                current_app.config['COMPLETED_LEVELS'].add(8)
                
        except Exception as e:
            error_msg = f"Failed to load file: {str(e)}"
    else:
        # PATCHED MODE (Strict Path Validation & safe_join)
        # 1. safe_join guarantees the resolved path stays strictly within DOCS_DIR
        # 2. Whitelist validation prevents accessing unauthorized files inside the directory
        safe_path = safe_join(DOCS_DIR, filename)
        
        if not safe_path or not safe_path.startswith(DOCS_DIR) or '..' in filename:
            error_msg = "Access Denied: Directory Traversal sequence ('..') detected by security filter."
        elif filename not in ALLOWED_DOCS:
            error_msg = f"Access Denied: '{filename}' is not in the authorized document whitelist."
        else:
            try:
                resolved_path = safe_path
                with open(safe_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
            except Exception as e:
                error_msg = f"Error opening file: {str(e)}"

    return render_template('view_doc.html',
                           current_file=filename,
                           file_content=file_content,
                           error_msg=error_msg,
                           resolved_path=resolved_path,
                           allowed_docs=ALLOWED_DOCS,
                           vuln_mode=vuln_mode)
