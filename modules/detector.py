import datetime
import re
from flask import Blueprint, request, render_template

detector_bp = Blueprint('detector', __name__)

# In-memory list to store recent detections for the dashboard
detections_log_memory = []

# Simple regex signatures for common attacks demonstrated in this lab
SIGNATURES = {
    "SQLi (Auth Bypass)": r"' OR '1'='1",
    "SQLi (UNION)": r"(?i)UNION\s+SELECT",
    "XSS (Script Tag)": r"(?i)<script>",
    "XSS (JavaScript URI)": r"(?i)javascript:",
    "XSS (Fetch Payload)": r"(?i)fetch\(",
    "Session Hijacking/XSS": r"(?i)document\.cookie",
}

def init_detector(app):
    """
    Registers the before_request hook directly on the main Flask app instance.
    This acts as a passive WAF that observes all incoming traffic.
    """
    @app.before_request
    def inspect_request():
        # Avoid inspecting binary file uploads for simplicity
        if request.path == '/upload' and request.method == 'POST':
            # But we can still inspect query params on the upload route
            pass
            
        ip = request.remote_addr
        
        # Check URL query parameters
        for key, value in request.args.items():
            _check_for_attacks(value, ip)
            
        # Check POST form data
        if request.form:
            for key, value in request.form.items():
                if isinstance(value, str):
                    _check_for_attacks(value, ip)

def _check_for_attacks(payload, ip):
    """
    Scans a payload against known signatures. 
    In this educational sandbox, we passively log the attack but intentionally DO NOT block it, 
    so that the vulnerable endpoints still fire and the user can see the successful exploit.
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
            
            # Cap at 100 to prevent memory leaks in the sandbox
            if len(detections_log_memory) > 100:
                detections_log_memory.pop()
                
            # Write to a persistent log file
            try:
                with open("detections.log", "a", encoding="utf-8") as f:
                    # Replace newlines in payload to keep log file format clean
                    clean_payload = payload.replace('\n', ' ').replace('\r', '')
                    f.write(f"[{timestamp}] IP: {ip} | Attack: {attack_name} | Payload: {clean_payload}\n")
            except Exception as e:
                print(f"Failed to write to detections.log: {e}")
                
            # We break after the first match to avoid double-logging the same parameter
            break

@detector_bp.route('/admin/detections')
def view_detections():
    return render_template('admin_detections.html', detections=detections_log_memory)
