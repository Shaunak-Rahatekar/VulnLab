# VulnLab - Comprehensive Testing Guide

Welcome to **VulnLab**, an educational security sandbox designed to demonstrate common web application vulnerabilities, their root causes, and how to patch them according to the university Ethical Hacking curriculum (Units I – V).

This guide walks you through installing the lab, running the server, toggling defenses, and testing every vulnerability.

---

## 🚀 Installation & Running Guide

### 1. Prerequisites
- Python 3.8+ installed on your system.

### 2. Setup Instructions
1. Open your terminal and navigate to the project folder (`d:\VulnLab`).
2. (Optional but recommended) Activate the virtual environment:
   ```bash
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the application:
   ```bash
   python app.py
   ```
5. Open your web browser and navigate to: **`http://127.0.0.1:5000`**

### 3. Toggling Vulnerabilities
You can toggle vulnerabilities in two ways:
1. **Live in Browser (Instant):** Use the control bar across the top of any page to switch between **VULNERABLE** and **PATCHED** mode without restarting the server!
2. **Configuration File:** Edit the `VULN_MODE` dictionary inside `config.py`.

---

## 🎯 Vulnerability Menu & Syllabus Navigation

| Level | Page Name | Route | Syllabus Unit | Vulnerability Category | Exploitation Script/Method |
|:---:|---|---|:---:|---|---|
| **1** | Login Page | `/login` | Unit IV | SQLi (Authentication Bypass) | Manual Payload (`' OR '1'='1`) |
| **2** | Product Search | `/search` | Unit IV | SQLi (UNION Data Extraction) | Manual Payload (`' UNION SELECT ...`) |
| **3** | Guestbook Comments | `/comments` | Unit IV | Stored Cross-Site Scripting (XSS) | `<script>fetch(...)</script>` |
| **4** | Quick Search | `/search_reflected` | Unit IV | Reflected Cross-Site Scripting (XSS) | URL Query String Reflection |
| **5** | Account Profile | `/profile` | Unit IV | Cross-Site Request Forgery (CSRF) | `attacks/csrf_attack.html` |
| **6** | Profile Picture | `/upload` | Unit IV | Insecure File Upload | `attacks/upload_attack.py` |
| **7** | Dashboard | `/dashboard` | Unit III | Session Hijacking & Fixation | `attacks/session_fixation.py` |
| **8** | Document Viewer | `/view_doc` | Unit IV | Directory Traversal & LFI | `attacks/traversal_attack.py` |
| **9** | Security Headers | `/security_headers` | Unit IV | Missing Security Headers & Clickjacking | Interactive Frame Simulation |
| **10** | Brute Force Login | `/login_bruteforce` | Unit III | Password Attacks & Lack of Rate Limiting | `attacks/bruteforce_attack.py` |
| **11** | Recon Workbench | `/recon` | Unit II | Reconnaissance & Information Disclosure | `/robots.txt`, `/config.py.bak` |
| **🛡️** | WAF & IPS Dashboard | `/admin/detections` | Unit III | Passive IDS Logging vs Active IPS 403 | Real-time event log & toggle |
| **📊** | Pentest Report | `/report` | Unit V | Pentest Reporting & Risk Rating | Printable Executive Summary & CVSS |

---

*Note: For detailed, step-by-step exploitation walkthroughs, root-cause code analysis, and patching details, please refer to [DEVELOPER_DOCS.md](DEVELOPER_DOCS.md).*
