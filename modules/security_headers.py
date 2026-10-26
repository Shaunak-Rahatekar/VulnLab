# modules/security_headers.py
from flask import Blueprint, render_template, request, current_app
from config import VULN_MODE

headers_bp = Blueprint('security_headers', __name__)

SECURITY_HEADERS_LIST = [
    {
        "name": "Content-Security-Policy",
        "description": "Restricts sources from which scripts, images, and other resources can be loaded (Primary XSS defense).",
        "recommended": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;"
    },
    {
        "name": "X-Frame-Options",
        "description": "Instructs modern browsers whether the page may be embedded inside <frame>, <iframe>, or <object> tags (Clickjacking defense).",
        "recommended": "DENY or SAMEORIGIN"
    },
    {
        "name": "X-Content-Type-Options",
        "description": "Prevents MIME-sniffing by the browser, forcing it to honor the declared Content-Type header.",
        "recommended": "nosniff"
    },
    {
        "name": "Strict-Transport-Security (HSTS)",
        "description": "Enforces secure HTTPS connections, preventing SSL-stripping and man-in-the-middle attacks.",
        "recommended": "max-age=31536000; includeSubDomains"
    },
    {
        "name": "Referrer-Policy",
        "description": "Controls what information is sent in the HTTP Referer header when navigating away from the page.",
        "recommended": "strict-origin-when-cross-origin"
    }
]

@headers_bp.route('/security_headers', methods=['GET'])
def security_headers_view():
    vuln_mode = VULN_MODE.get("headers", True)
    
    # Analyze the simulated response headers
    header_status = []
    
    for h in SECURITY_HEADERS_LIST:
        is_present = not vuln_mode
        header_status.append({
            "name": h["name"],
            "description": h["description"],
            "recommended": h["recommended"],
            "present": is_present,
            "status": "MISSING (Vulnerable)" if not is_present else "CONFIGURED (Patched)"
        })
        
    current_app.config['COMPLETED_LEVELS'].add(9)

    return render_template('security_headers.html',
                           header_status=header_status,
                           vuln_mode=vuln_mode)
