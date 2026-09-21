from flask import Blueprint, request, session, redirect, url_for
from config import VULN_MODE

session_bp = Blueprint('session_hijack', __name__)

@session_bp.route('/set_session')
def set_session():
    """
    Simulates a Session Fixation attack vector.
    An attacker tricks a victim into clicking a link like:
    http://127.0.0.1:5000/set_session?sessionid=KNOWN_ATTACKER_ID
    
    If vulnerable, the server forces the victim's session ID to match 
    the attacker's known ID. When the victim subsequently logs in, 
    the server binds their authentication state to that known ID.
    """
    if VULN_MODE.get("session", True):
        sid = request.args.get('sessionid')
        if sid:
            # Force the victim's browser to adopt the attacker's known session ID
            session['session_id'] = sid
            
    # Redirect them to login so they authenticate using this fixed session ID
    return redirect(url_for('sqli.login'))
