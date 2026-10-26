# modules/admin_manager.py
import os
import glob
from flask import Blueprint, jsonify, request, current_app
from config import VULN_MODE
from models import db, User, Product, Comment, server_sessions, seed_db
from modules.detector import detections_log_memory

admin_mgr_bp = Blueprint('admin_manager', __name__)

@admin_mgr_bp.route('/admin/toggles', methods=['GET'])
def get_toggles():
    return jsonify(VULN_MODE)

@admin_mgr_bp.route('/admin/toggle/<feature>', methods=['POST'])
def toggle_feature(feature):
    if feature in VULN_MODE:
        if isinstance(VULN_MODE[feature], bool):
            VULN_MODE[feature] = not VULN_MODE[feature]
            new_val = VULN_MODE[feature]
            
            # Synchronize Flask runtime settings
            if feature == "session":
                current_app.config['SESSION_COOKIE_HTTPONLY'] = not new_val
                current_app.config['SESSION_COOKIE_SAMESITE'] = 'Strict' if not new_val else None
            elif feature == "csrf":
                current_app.config['WTF_CSRF_ENABLED'] = not new_val
                
            return jsonify({
                "status": "success",
                "feature": feature,
                "value": new_val,
                "message": f"Module '{feature}' is now {'VULNERABLE' if new_val else 'PATCHED'}."
            })
        elif feature == "waf_mode":
            VULN_MODE["waf_mode"] = "active" if VULN_MODE["waf_mode"] == "passive" else "passive"
            return jsonify({
                "status": "success",
                "feature": "waf_mode",
                "value": VULN_MODE["waf_mode"],
                "message": f"WAF Mode set to '{VULN_MODE['waf_mode'].upper()}'."
            })
            
    return jsonify({"status": "error", "message": f"Unknown feature toggle: {feature}"}), 400

@admin_mgr_bp.route('/admin/reset_lab', methods=['POST'])
def reset_lab():
    try:
        # 1. Reset database tables
        Comment.query.delete()
        Product.query.delete()
        User.query.delete()
        db.session.commit()
        seed_db()

        # 2. Flush uploaded files in static/uploads and safe_uploads
        for folder in [os.path.join('static', 'uploads'), 'safe_uploads']:
            if os.path.exists(folder):
                for f in glob.glob(os.path.join(folder, '*')):
                    if os.path.isfile(f):
                        try:
                            os.remove(f)
                        except Exception:
                            pass

        # 3. Clear sessions and progress
        server_sessions.clear()
        current_app.config['COMPLETED_LEVELS'].clear()

        # 4. Clear detections log
        detections_log_memory.clear()
        try:
            with open("detections.log", "w", encoding="utf-8") as f:
                f.write("")
        except Exception:
            pass

        return jsonify({
            "status": "success",
            "message": "VulnLab database, uploaded files, session cache, and logs have been reset to pristine initial state."
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
