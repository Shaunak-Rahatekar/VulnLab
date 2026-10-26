# VulnLab: Slide-by-Slide Presentation Content

---

## Slide 1: Title Slide

### **Slide Content**
- **Title:** VulnLab: A Docker-Based Vulnerable Web Application for Exploitation and Security Hardening
- **Subtitle:** An Interactive Full-Stack Security Engineering Sandbox & Pentest Simulation Platform
- **Academic Context:** Department of Computer Engineering — Ethical Hacking & Application Security
- **Team Members:**
  - Shaunak Rahatekar (Lead Security Architect & Developer)
  - [Teammate 2 Name / Roll No]
  - [Teammate 3 Name / Roll No]
- **Project Mentor / Guide:** [Prof. Guide Name]
- **Institution:** Vishwakarma Institute of Technology, Pune

### **Speaker Notes**
> "Good morning, respected professors and peers. Today, we are presenting our capstone security project: **VulnLab**. VulnLab is an interactive, Docker-containerized educational sandbox designed to demonstrate real-world web vulnerabilities, live exploit workflows, and production-grade defense and remediation mechanisms across the entire OWASP Top 10 spectrum."

---

## Slide 2: Introduction

### **Slide Content**
- **What is VulnLab?**
  - A purpose-built, dual-state educational security sandbox.
  - Bridges the gap between abstract cybersecurity theory and hands-on offensive/defensive engineering.
- **Key Characteristics:**
  - **11 Interactive Vulnerability Modules:** Spanning injection, authentication, broken access control, and reconnaissance.
  - **Dynamic Toggle Architecture:** Instant runtime switching between **Vulnerable** (Exploitable) and **Patched** (Hardened) modes without restarting the server.
  - **Active Hybrid WAF:** Custom Web Application Firewall featuring real-time attack pattern inspection and IPS blocking.
  - **Automated Pentest Engine:** Built-in CVSS scoring and executive risk audit reporting.

### **Speaker Notes**
> "In modern cybersecurity education, reading about exploits is not enough. VulnLab gives students and engineers a zero-risk, sandbox environment where they can safely launch exploits, observe underlying system behavior, and immediately switch to patched mode to understand defense-in-depth secure coding."

---

## Slide 3: Problem Statement

### **Slide Content**
- **The Core Problem:**
  - **High Attack Prevalence:** Web applications remain the #1 vector for data breaches (OWASP Top 10, CWE/SANS Top 25).
  - **Theoretical Knowledge Gap:** Traditional university courses teach security concepts theoretically without live interactive environments.
  - **Setup Complexity of Legacy Labs:** Tools like DVWA or WebGoat often require extensive legacy configurations (PHP, old MySQL versions) and lack real-time code-level visual comparison.
  - **Absence of Dual-State Inspection:** Most training environments only show the broken state, leaving students confused on *how* to write the remediated code.
- **The Solution:**
  - A modern, unified Python/Flask sandbox with instant side-by-side vulnerable vs. patched execution, built-in code diff inspection, and one-click containerization.

### **Speaker Notes**
> "The fundamental problem we observed is that students often know what SQL Injection or XSS is by definition, but cannot spot it in source code or write parameterized remediations. VulnLab directly addresses this by pairing every single vulnerable route with an isolated, secure implementation."

---

## Slide 4: Project Objectives

### **Slide Content**
- **Demonstrate Real-World Vulnerability Mechanics:**
  - Show precisely *why* common programming practices (string concatenation, unescaped reflection, missing security headers) lead to critical exploits.
- **Provide Safe & Controlled Exploitation:**
  - Deliver automated Python attack scripts and live interactive UI forms for safe penetration testing.
- **Teach Defensive Engineering & Remediation:**
  - Implement industry-standard secure programming practices: ORM parameterization, cryptographic password hashing, CSP nonce controls, and secure session management.
- **Simulate Enterprise Security Infrastructure:**
  - Integrate a Web Application Firewall (WAF/IPS) and an automated Executive Penetration Test Reporting engine.
- **Ensure Portability & Reproducibility:**
  - Enable instant, one-command deployment via Docker containers or virtual environments.

### **Speaker Notes**
> "Our objectives were threefold: first, illustrate offensive mechanics with zero guesswork; second, provide defensible secure coding patterns; and third, give students realistic exposure to enterprise tools like Web Application Firewalls and formal CVSS audit reports."

---

## Slide 5: Project Scope & Vulnerability Modules

### **Slide Content**
| Module # | Vulnerability Class | Attack Technique Demonstrated | Defense / Hardening Deployed |
| :--- | :--- | :--- | :--- |
| **01** | SQL Injection (Auth Bypass) | String delimiter escape (`' OR '1'='1`) | Parameterized SQLAlchemy queries |
| **02** | SQL Injection (UNION Data Leak) | `UNION SELECT username, password_hash` | Whitelisted parameterized search |
| **03** | Stored XSS | Script persistence in guestbook DB | Contextual HTML escaping & Jinja2 sanitization |
| **04** | Reflected XSS | Immediate URL query reflection | Explicit HTML entity encoding |
| **05** | Cross-Site Request Forgery (CSRF) | Zero-interaction auto-submitting POST | Cryptographic Anti-CSRF Synchronizer Tokens |
| **06** | Insecure File Upload | Web shell / executable upload (`.py`, `.php`) | Magic byte validation, MIME check & safe dir |
| **07** | Session Fixation & Hijacking | Pre-session fixation & document.cookie theft | Session ID regeneration & `HttpOnly` flags |
| **08** | Directory Traversal & LFI | Relative path dot-dot-slash (`../../config.py`) | Path normalization, `safe_join` & whitelist |
| **09** | Security Headers & Clickjacking | UI redressing / iframe clickjacking | CSP, `X-Frame-Options: DENY`, `HSTS`, `X-Content-Type` |
| **10** | Password Brute-Force & Auth | Automated credential stuffing & wordlists | Sliding-window IP rate limiting & HTTP 429 lockout |
| **11** | Reconnaissance & Info Disclosure | `robots.txt` analysis & backup file leaks (`.bak`) | Disallow filtering & sensitive file route removal |

### **Speaker Notes**
> "VulnLab spans 11 comprehensive modules. These range from basic injection attacks to advanced defense mechanisms like Path Traversal prevention, HTTP security header orchestration, and rate-limiting brute force locks."

---

## Slide 6: Technology Stack

### **Slide Content**
- **Backend Architecture:**
  - **Language:** Python 3.11+
  - **Microframework:** Flask 3.0 (Modular Blueprint architecture)
  - **Database & ORM:** SQLite 3 with Flask-SQLAlchemy 3.1
  - **Security Utilities:** Werkzeug (PBKDF2-SHA256 password hashing), Flask-WTF (CSRF tokens), `python-magic` (file signature inspection)
- **Frontend & UI Layer:**
  - **Styling:** Custom Vanilla CSS with Cyberpunk / Glassmorphism aesthetic
  - **Typography:** Google Fonts (`Inter` for UI, `JetBrains Mono` for code)
  - **Scripting:** Modular vanilla JavaScript (`sandbox.js` theme engine, toast alerts, modals)
- **DevOps & Containerization:**
  - **Container Runtime:** Docker Engine & Docker Compose
  - **Base Image:** `python:3.11-slim` (minimal attack surface, fast deployment)
- **Offensive Tooling:**
  - **Automated Exploit Suite:** Native Python `requests` attack scripts in `attacks/`

### **Speaker Notes**
> "We selected Python and Flask for their clean modularity. The database is SQLite with SQLAlchemy. Crucially, the frontend was built without bloated third-party frameworks, allowing precise control over DOM elements, CSP policies, and iframe rendering."

---

## Slide 7: System Architecture

### **Slide Content**
```
+-------------------------------------------------------------------------------+
|                                  Web Browser                                  |
|         (User Interface / Cyberpunk Theme / Intel Vault / Code Diff Modal)    |
+-------------------------------------------------------------------------------+
                                      |
                       HTTP / HTTPS Requests (Port 5000)
                                      v
+-------------------------------------------------------------------------------+
|                      WAF Middleware Inspection Engine                         |
|            (SQLi / XSS / Traversal / Command Injection Signature Matching)    |
|                Mode: PASSIVE (Alert)  vs.  ACTIVE IPS (403 Block)             |
+-------------------------------------------------------------------------------+
                                      |
                           Forward Verified Traffic
                                      v
+-------------------------------------------------------------------------------+
|                             Flask Application Core                            |
|                               (Global State Manager)                          |
+-------------------------------------------------------------------------------+
       |                                                               |
       v                                                               v
[Vulnerable Branch]                                            [Patched Branch]
- Raw string query formatting                                  - Parameterized SQLAlchemy ORM
- Unescaped Jinja2 `|safe` rendering                           - Context-aware HTML entity encoding
- Missing Anti-CSRF verification                               - Flask-WTF CSRF validation
- Arbitrary filename & path concatenation                      - Safe-join path traversal guards
- Unrestricted multi-attempt login                             - Sliding-window IP rate limiting
       |                                                               |
       +-------------------------------+-------------------------------+
                                       |
                                       v
+-------------------------------------------------------------------------------+
|                   Persistent Data & Secure File Storage                       |
|           SQLite Database (instance/vulnlab.db) | /safe_uploads/              |
+-------------------------------------------------------------------------------+
```

### **Speaker Notes**
> "Here is our System Architecture. Every request first passes through our custom WAF middleware. When active, it blocks malicious payloads immediately with HTTP 403. Otherwise, requests hit our Flask application where a global state toggle dictates whether the vulnerable route or the secured route handles execution."

---

## Slide 8: Deployment & Containerization (Docker)

### **Slide Content**
- **Docker-Based Sandboxing:**
  - Complete isolation from the host machine: students can execute dangerous payloads without risking host OS integrity.
  - Multi-stage slim container (`python:3.11-slim`) ensures lightweight footprint (<180 MB).
- **Docker Compose Orchestration:**
  - Mounts persistent volumes for `instance/vulnlab.db` and uploaded media files.
  - One-command deployment:
    ```bash
    # Clone repository and launch sandbox container
    git clone https://github.com/Shaunak-Rahatekar/VulnLab.git
    cd VulnLab
    docker-compose up --build
    ```
- **Alternative Virtual Environment Setup:**
  - Cross-platform support for Windows, Linux, and macOS via `venv` and `requirements.txt`.
- **Public Tunneling Architecture:**
  - Integrated zero-install OpenSSH reverse tunneling (`ssh -R 80:127.0.0.1:5000 nokey@localhost.run`) for remote live demonstrations and team evaluations.

### **Speaker Notes**
> "Containerization is critical for security labs. By wrapping VulnLab in Docker, any file uploads or payloads remain completely quarantined inside the container. It also guarantees that any student or professor can run the lab with a single command without dependency conflicts."

---

## Slide 9: Vulnerability Demonstration — SQL Injection

### **Slide Content**
- **Exploitation Mechanics (Vulnerable Mode):**
  - Query construction uses unsafe string concatenation:
    ```python
    # Vulnerable Code (modules/sqli.py)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    result = db.session.execute(text(query)).fetchone()
    ```
  - **Attacker Payload:** `' OR '1'='1' -- `
  - **Resulting Executed SQL:**
    ```sql
    SELECT * FROM users WHERE username = '' OR '1'='1' -- ' AND password = ''
    ```
  - **Outcome:** The `WHERE` clause evaluates to `TRUE`, returning the first user in the table (Administrator), granting instant unauthorized access!

- **Remediation Mechanics (Patched Mode):**
  - Enforces strict parameterized query binding through the ORM:
    ```python
    # Patched Code (modules/sqli.py)
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
    ```
  - **Defense Result:** The input `' OR '1'='1'` is treated strictly as literal string data, completely neutralizing injection.

### **Speaker Notes**
> "On this slide, we illustrate SQL Injection. In vulnerable mode, user input breaks out of the SQL syntax, transforming data into executable code. In patched mode, we enforce parameterized queries using SQLAlchemy ORM and compare salted hashes with Werkzeug. The payload is treated strictly as characters, making authentication bypass impossible."

---

## Slide 10: Vulnerability Demonstration — XSS & CSRF

### **Slide Content**
- **Stored & Reflected Cross-Site Scripting (XSS):**
  - **Flaw:** Unsanitized user comments rendered directly via Jinja2's `|safe` filter.
  - **Attack Payload:** `<script>alert('XSS: ' + document.cookie);</script>`
  - **Impact:** Malicious script executes inside victim's browser, enabling session hijacking and keystroke logging.
  - **Remediation:** Remove `|safe`, enforce automatic contextual HTML escaping, and deploy a strict Content Security Policy (`Content-Security-Policy: default-src 'self'`).

- **Cross-Site Request Forgery (CSRF):**
  - **Flaw:** State-changing POST endpoints (`/profile`) rely solely on ambient session cookies without request origin validation.
  - **Attack Mechanism:** An external attacker page hosts a hidden auto-submitting form:
    ```html
    <form action="http://localhost:5000/profile" method="POST" id="csrfForm">
      <input type="hidden" name="email" value="attacker@evil.com" />
    </form>
    <script>document.getElementById('csrfForm').submit();</script>
    ```
  - **Remediation:** Deploy Flask-WTF Cryptographic CSRF Tokens and set `SameSite=Strict` cookie policies.

### **Speaker Notes**
> "For XSS, we demonstrate how reflected and stored JavaScript runs in the browser context to steal cookies. For CSRF, we show how an external website can trick an authenticated browser into modifying profile data. We resolve both using HTML entity escaping, CSP headers, SameSite strict cookies, and anti-CSRF synchronizer tokens."

---

## Slide 11: Security Hardening — Vulnerable vs. Patched

### **Slide Content**
- **Direct Side-by-Side Architectural Comparison:**

| Architectural Layer | Vulnerable Sandbox Behavior | Hardened / Patched Behavior |
| :--- | :--- | :--- |
| **Database Queries** | Raw SQL string interpolation (`f"..."`) | Parameterized ORM queries (`filter_by`) |
| **Password Storage** | Plaintext / reversible encoding | PBKDF2 with SHA-256 and unique salts |
| **Template Rendering** | Raw unescaped HTML (`|safe`) | Auto-escaped Jinja2 context encoding |
| **Cookie Security** | `HttpOnly=False`, `SameSite=None` | `HttpOnly=True`, `SameSite=Strict`, `Secure` |
| **File Handling** | Raw extension check, writes to web root | Magic byte MIME check, randomized UUID storage |
| **Path Access** | Concatenation (`os.path.join(DIR, user_input)`) | Whitelist validation & Werkzeug `safe_join` |
| **HTTP Headers** | Leaks `Server: Werkzeug/Python` | Injects CSP, HSTS, X-Frame-Options, X-Content-Type |
| **Authentication Flow** | Unlimited password guessing attempts | 5-attempt sliding lockout with HTTP 429 |
| **WAF Policy** | Inactive / Passive logging | Active IPS Mode (HTTP 403 Forbidden blocking) |

### **Speaker Notes**
> "This comparison table summarizes the security hardening implemented in VulnLab. For every single vulnerability category, we designed a direct, tangible counterpart. Students can toggle between them in real time and see the exact difference in network responses and server logs."

---

## Slide 12: Testing, Verification & Results

### **Slide Content**
- **Automated Verification Test Suite:**
  - Developed end-to-end regression test harness (`verify_all_modules.py`).
  - Achieved **100% test pass rate** across all 11 modules under both vulnerable and patched states.
- **Key Test Results:**
  - **LFI / Path Traversal:** `../config.py` leaked database credentials in vulnerable mode; strictly blocked by `safe_join` in patched mode.
  - **Rate Limiting:** Permitted unlimited brute-force attacks in vulnerable mode; triggered immediate HTTP 429 lockout on the 6th failed attempt in patched mode.
  - **Security Headers:** Injected 5 defense-in-depth headers and eliminated the revealing server banner.
  - **Active WAF Mode:** Successfully intercepted SQLi and XSS payloads, returning HTTP 403 Forbidden and logging IP, timestamp, and signature ID.
- **Executive Pentest Report Output:**
  - Successfully generated comprehensive HTML pentest audit report with CVSS severity badges and remediation guides.

### **Speaker Notes**
> "To guarantee academic rigor, we engineered an automated Python testing suite that programmatically validates every attack script against both modes. In vulnerable mode, all exploits succeed with clear evidence; in patched mode, every attack is cleanly mitigated and logged."

---

## Slide 13: Applications, Limitations & Future Scope

### **Slide Content**
- **Practical Applications:**
  - **Academic Labs:** Laboratory companion for university courses in Ethical Hacking, Information Security, and Web Development.
  - **Secure Coding Training:** Benchmark training platform for junior software engineers and DevOps teams.
  - **CTF & Security Competitions:** Pre-configured challenge environment for collegiate capture-the-flag events.
- **Current Limitations:**
  - Single-container sandbox architecture without multi-tenant user isolation.
  - In-memory WAF signature engine rather than an external reverse proxy (like ModSecurity / Cloudflare).
- **Future Enhancements:**
  - **Cloud-Native Deployment:** Helm charts for Kubernetes cluster scaling.
  - **API Security Modules:** OWASP API Top 10 (GraphQL injection, JWT tampering, BOLA / IDOR).
  - **Gamified Scoring Engine:** User accounts, real-time leaderboard, and automated flag submission.

### **Speaker Notes**
> "VulnLab has direct applications in college classrooms, secure coding bootcamps, and CTFs. In the future, we plan to expand VulnLab to include Kubernetes orchestration, OWASP API Top 10 challenges like JWT tampering, and a gamified student leaderboard."

---

## Slide 14: Conclusion & Q&A

### **Slide Content**
- **Key Project Takeaways:**
  - Developed a comprehensive, 11-module vulnerable web application sandbox aligned with the OWASP Top 10.
  - Successfully implemented dynamic live toggling between vulnerable code and industry-standard defensive mitigations.
  - Integrated enterprise features: an active WAF/IPS protection layer and an automated Pentest Report generator.
  - Containerized with Docker for seamless, platform-independent portability and safe academic experimentation.
- **Project Repository:**
  - **GitHub:** `https://github.com/Shaunak-Rahatekar/VulnLab`
- **Thank You!**
  - We invite any questions, critiques, or feedback from the committee.

### **Speaker Notes**
> "In conclusion, VulnLab successfully bridges theoretical cybersecurity education with real-world secure engineering. By seeing both the exploit and the patch side-by-side, students gain a deep, intuitive understanding of application security. Thank you for your time, and we now welcome any questions."
