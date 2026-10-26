# config.py

# VULN_MODE toggles the vulnerability state for each module.
# True = Vulnerable (educational/demonstration mode)
# False = Patched (secure mode)
VULN_MODE = {
    "sqli": True,         # Level 1 & 2: SQL Injection (Auth Bypass & UNION)
    "xss": True,          # Level 3 & 4: Stored & Reflected XSS
    "session": True,      # Level 7: Session Fixation & Hijacking
    "csrf": True,         # Level 5: Cross-Site Request Forgery
    "upload": True,       # Level 6: Insecure File Upload
    "traversal": True,    # Level 8: Directory Traversal & Local File Inclusion (LFI)
    "headers": True,      # Level 9: Missing Security Headers & Clickjacking
    "bruteforce": True,   # Level 10: Password Attacks & Lack of Rate Limiting
    "recon": True,        # Level 11: Information Disclosure & Banner Grabbing
    "waf_mode": "passive" # WAF Mode: "passive" (detection only) or "active" (blocking 403)
}
