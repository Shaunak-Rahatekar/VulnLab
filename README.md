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

*Note: For detailed, step-by-step exploitation walkthroughs, root-cause code analysis, and patching details, please refer to the [DEVELOPER_DOCS.md](DEVELOPER_DOCS.md) file included in this repository.*
