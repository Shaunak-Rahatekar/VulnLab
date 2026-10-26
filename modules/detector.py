# modules/detector.py
import datetime
import re
from flask import Blueprint, request, render_template, current_app, abort, Response
from config import VULN_MODE

detector_bp = Blueprint('detector', __name__)

# In-memory list to store recent detections for the dashboard
detections_log_memory = []

# Regex signatures for attacks demonstrated in this lab
SIGNATURES = {
    "SQLi (Auth Bypass)": r"' OR '1'='1",
    "SQLi (UNION)": r"(?i)UNION\s+SELECT",
    "XSS (Script Tag)": r"(?i)<script>",
    "XSS (JavaScript URI)": r"(?i)javascript:",
    "XSS (Fetch Payload)": r"(?i)fetch\(",
    "Session Hijacking/XSS": r"(?i)document\.cookie",
    "Directory Traversal / LFI": r"\.\./|\.\.\\",
}

ENDPOINT_TO_LEVEL = {
    'sqli.login': 1,
    'search.search': 2,
    'xss.comments': 3,
    'xss.search_reflected': 4,
    'file_inclusion.view_doc': 8,
    'bruteforce.login_bruteforce': 10,
}

def init_detector(app):
    """
    Registers the before_request hook directly on the main Flask app instance.
    Acts as an IDS (Passive Logging) or IPS (Active Blocking) based on waf_mode.
    """
    @app.before_request
    def inspect_request():
        # Exclude static assets and admin reset
        if request.path.startswith('/static') or request.path.startswith('/admin/reset_lab'):
            return

        ip = request.remote_addr or '127.0.0.1'
        matched_attack = None
        offending_payload = None

        # Check URL query parameters
        for key, value in request.args.items():
            attack = _check_for_attacks(value, ip)
            if attack:
                matched_attack = attack
                offending_payload = value
                break

        # Check POST form data
        if not matched_attack and request.form:
            for key, value in request.form.items():
                if isinstance(value, str):
                    attack = _check_for_attacks(value, ip)
                    if attack:
                        matched_attack = attack
                        offending_payload = value
                        break

        # Active IPS/Firewall Mode: Block matching requests with HTTP 403
        if matched_attack and VULN_MODE.get("waf_mode") == "active":
            blocked_html = f"""
            <!DOCTYPE html>
            <html>
            <head><title>403 Forbidden - WAF Block</title></head>
            <body style="font-family: Arial, sans-serif; background: #f8f9fa; padding: 50px; text-align: center;">
                <div style="max-width: 650px; margin: auto; background: white; padding: 30px; border-radius: 8px; border-top: 5px solid #c0392b; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h1 style="color: #c0392b; margin-top: 0;">🛡️ 403 Forbidden: Blocked by VulnLab WAF</h1>
                    <p style="color: #555; font-size: 1.1em;">
                        Your request was intercepted by the active Web Application Firewall rule set (IPS Mode).
                    </p>
                    <div style="background: #fdfefe; border: 1px solid #ddd; padding: 15px; border-radius: 4px; text-align: left; font-family: monospace; font-size: 0.9em; margin: 20px 0;">
                        <strong>Triggered Signature:</strong> <span style="color: #c0392b;">{matched_attack}</span><br>
                        <strong>Offending Parameter:</strong> <code>{offending_payload}</code><br>
                        <strong>Client IP:</strong> {ip}<br>
                        <strong>Action Taken:</strong> Request Dropped (HTTP 403)
                    </div>
                    <p style="font-size: 0.85em; color: #888;">Network Security Controls, Firewalls & IPS Basics</p>
                    <a href="/admin/detections" style="color: #2980b9; text-decoration: none; font-weight: bold;">← View WAF Dashboard</a>
                </div>
            </body>
            </html>
            """
            return Response(blocked_html, status=403, mimetype='text/html')

def _check_for_attacks(payload, ip):
    """
    Scans a payload against known signatures.
    """
    for attack_name, pattern in SIGNATURES.items():
        if re.search(pattern, payload):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = {
                "timestamp": timestamp,
                "source_ip": ip,
                "attack_pattern": attack_name,
                "parameter": payload
            }

            # Add to in-memory list (insert at the beginning for reverse-chronological order)
            detections_log_memory.insert(0, log_entry)

            # Cap at 100 entries
            if len(detections_log_memory) > 100:
                detections_log_memory.pop()

            # Write to persistent log file
            try:
                with open("detections.log", "a", encoding="utf-8") as f:
                    clean_payload = payload.replace('\n', ' ').replace('\r', '')
                    f.write(f"[{timestamp}] IP: {ip} | Attack: {attack_name} | Payload: {clean_payload}\n")
            except Exception as e:
                print(f"Failed to write to detections.log: {e}")

            # Automatically unlock the level if the payload matches on the expected endpoint
            if request.endpoint in ENDPOINT_TO_LEVEL:
                current_app.config['COMPLETED_LEVELS'].add(ENDPOINT_TO_LEVEL[request.endpoint])

            if attack_name == "Session Hijacking/XSS":
                current_app.config['COMPLETED_LEVELS'].add(7)

            return attack_name
    return None

@detector_bp.route('/admin/detections')
def view_detections():
    waf_mode = VULN_MODE.get("waf_mode", "passive")
    return render_template('admin_detections.html', 
                           detections=detections_log_memory,
                           waf_mode=waf_mode)
