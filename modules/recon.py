# modules/recon.py
from flask import Blueprint, render_template, Response, request, current_app
from config import VULN_MODE

recon_bp = Blueprint('recon', __name__)

@recon_bp.route('/recon', methods=['GET'])
def recon_workbench():
    vuln_mode = VULN_MODE.get("recon", True)
    current_app.config['COMPLETED_LEVELS'].add(11)
    return render_template('recon.html', vuln_mode=vuln_mode)

@recon_bp.route('/robots.txt')
def robots_txt():
    vuln_mode = VULN_MODE.get("recon", True)
    if vuln_mode:
        # VULNERABLE: Overly informative robots.txt disclosing sensitive paths to crawlers and OSINT tools
        content = """# robots.txt - Informational Disclosure
User-agent: *
Disallow: /admin/
Disallow: /admin/secret_backup
Disallow: /admin/detections
Disallow: /config.py.bak
Disallow: /database.db
"""
    else:
        # PATCHED: Generic robots.txt that does not advertise sensitive endpoints
        content = """User-agent: *
Disallow: /private/
"""
    return Response(content, mimetype='text/plain')

@recon_bp.route('/admin/secret_backup')
def secret_backup():
    return render_template('secret_backup.html')

@recon_bp.route('/config.py.bak')
def config_backup():
    vuln_mode = VULN_MODE.get("recon", True)
    if vuln_mode:
        content = """# BACKUP CONFIGURATION FILE (EXPOSED LEAK)
# Date: 2026-10-15
DB_INTERNAL_PASSWORD = "SuperSecretDbPassword2026!"
ADMIN_TOKEN = "token_c8a7b9e02394fd89"
"""
        return Response(content, mimetype='text/plain')
    else:
        return "404 Not Found - Access Denied to Backup Files", 404
