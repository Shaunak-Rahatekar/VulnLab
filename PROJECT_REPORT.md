# VULNLAB
## A Docker-Based Vulnerable Web Application for Exploitation and Security Hardening

**Project Report**  
**Department of Computer Engineering**  
**Vishwakarma Institute of Technology, Pune**  
**Subject:** Ethical Hacking & Application Security  

**Team Members:**  
- Shaunak Rahatekar  
- Sanyam Patwari  
- Raman Vhantale  
- Sharwari Rajput  

**Project Mentor / Guide:**  
- Ms. Jyoti Hindurao Yadav  

---

## 1. Project Title
**VulnLab: A Docker-Based Vulnerable Web Application for Exploitation and Security Hardening**

---

## 2. Introduction

### 2.1 Introduction
VulnLab is an interactive, Docker-containerized educational security sandbox designed to connect cybersecurity theory with practical offensive and defensive application-security work. It provides 11 interactive vulnerability modules covering common web-application weaknesses, including injection, cross-site scripting, authentication weaknesses, access-control issues, file-handling flaws, and information disclosure.

A central feature is its dual-state design: users can switch at runtime between a deliberately vulnerable mode and a patched mode. This lets learners observe an attack in a controlled environment, inspect the corresponding code, and compare it with a defensive implementation. The platform also features a custom Web Application Firewall (WAF) with passive alerting and active blocking modes, automated Python exploit scripts, CVSS-oriented risk scoring, and an automated HTML penetration-test report generator.

The application is built with Python and Flask, uses SQLite through Flask-SQLAlchemy, and provides a browser-based interface built with vanilla JavaScript and CSS. Docker and Docker Compose support repeatable, isolated deployment for classroom demonstrations and security-training exercises.

### 2.2 Problem Statement
Cybersecurity learners may understand vulnerability definitions in theory but still struggle to recognize unsafe code, reproduce the underlying behavior, and implement an effective fix. Traditional teaching often lacks interactive environments that show both the exploitable behavior and its secure counterpart side-by-side. Existing training labs frequently require complex legacy setups (such as outdated PHP and MySQL installations) and fail to provide immediate code-level diffs between vulnerable and remediated logic.

VulnLab addresses this learning gap by consolidating multiple web vulnerabilities into one portable, zero-configuration sandbox. For each module, the learner can examine the attack technique, observe its effect in vulnerable mode, and immediately compare the result with a patched implementation. The environment is intended for authorized, local or otherwise controlled educational testing, reinforcing ethical hacking principles and responsible disclosure.

### 2.3 Objectives
The primary objectives of the VulnLab project are:
1. **Demonstrate Real-World Vulnerability Mechanics:** Illustrate how common development oversights (such as raw string concatenation, unescaped output, missing security headers, and permissive path handling) lead to high-impact exploits.
2. **Provide Safe & Controlled Exploitation:** Supply automated Python attack scripts and interactive browser forms for safe, hands-on experimentation.
3. **Teach Secure Coding & Remediation:** Implement production-grade defenses, including ORM parameterized queries, cryptographic password hashing (PBKDF2-SHA256), Contextual HTML escaping, Anti-CSRF synchronizer tokens, and safe file/path normalization.
4. **Simulate Enterprise Security Infrastructure:** Incorporate a custom Web Application Firewall (WAF) supporting both Passive (monitoring) and Active IPS (HTTP 403 blocking) modes, along with an automated CVSS-aligned executive report generator.
5. **Ensure Isolated Portability:** Deliver one-command containerized deployment via Docker and Docker Compose to quarantine exploits and protect host operating systems.

---

## 3. Project Scope
The project scope covers a comprehensive, web-based training environment for demonstrating common web vulnerabilities and their mitigations. The principal capabilities include:

- **11 Vulnerability Modules:** Demonstrations spanning SQL Injection (Auth Bypass & UNION Data Extraction), Stored XSS, Reflected XSS, Cross-Site Request Forgery (CSRF), Insecure File Upload, Session Fixation/Hijacking, Directory Traversal/LFI, Security Headers & Clickjacking, Password Brute-Force & Rate Limiting, and Reconnaissance/Information Disclosure.
- **Dual-State Execution:** A runtime toggle switches between vulnerable and patched behavior across individual modules without requiring a server restart.
- **Code-Level Learning & Diff Inspection:** An integrated modal diff inspector enables learners to compare vulnerable code patterns with defensive implementations directly in the browser.
- **Guarded Intel Vault:** Multi-tier hints, concepts, and exploit payloads are stored behind interactive user shields to promote self-directed learning without immediately revealing answers.
- **WAF/IPS Layer:** A custom middleware layer inspects requests for selected attack signatures; passive mode logs alerts, while active mode blocks matching requests with HTTP 403 Forbidden.
- **Automated Testing Suite:** Python-based attack scripts and an end-to-end regression verification suite (`verify_all_modules.py`) validate expected behaviors across all modules and modes.
- **Risk Reporting:** An automated HTML penetration-test report compiles audit findings with CVSS severity indicators, affected endpoints, and remediation guidance.
- **Portable Deployment:** Docker and Docker Compose support repeatable, quarantined deployment across Windows, macOS, and Linux desktop environments.

---

## 4. Technology Stack

| Component | Technology / Purpose |
| :--- | :--- |
| **Backend Language** | Python 3.11+ |
| **Web Framework** | Flask 3.0, organized with modular Blueprints |
| **Database** | SQLite 3 |
| **ORM** | Flask-SQLAlchemy 3.1 |
| **Security Utilities** | Werkzeug password hashing (PBKDF2-SHA256), Flask-WTF CSRF protection, `python-magic` file-signature inspection |
| **Frontend UI** | Semantic HTML5 with custom Vanilla CSS and modular JavaScript (`sandbox.js`) |
| **UI Styling & Fonts** | Cyberpunk / Glassmorphism visual style; Google Fonts (`Inter` and `JetBrains Mono`) |
| **Containerization** | Docker Engine and Docker Compose; `python:3.11-slim` base image |
| **Automated Offensive Testing** | Python `requests`-based attack scripts in the `attacks/` directory |
| **Testing & Verification** | End-to-end test harness (`verify_all_modules.py`) with 100% pass verification |
| **Audit Reporting** | Built-in HTML penetration-test report generator with CVSS-oriented risk scoring |

---

## 5. System Architecture & Workflow

Every client request to VulnLab passes through a structured, multi-layer security architecture:

1. **Presentation Layer:** A responsive web interface styled with glassmorphism design tokens, providing interactive challenge forms, theme switching (Dark/Light), runtime mode toggles, and a guarded Intel Vault modal.
2. **WAF Middleware Layer:** Inbound HTTP requests (GET query strings, POST form data, and HTTP headers) are inspected by a custom pattern-matching engine against SQLi, XSS, and Path Traversal regex signatures.
   - *Passive Mode:* Logs the attack signature, client IP, and timestamp to `detections.log` and passes the request forward.
   - *Active IPS Mode:* Terminates the connection immediately, returning an HTTP 403 Forbidden alert to the client.
3. **Core Application & State Router:** Evaluates global toggle state (`VULN_MODE`) and dispatches the request to either the vulnerable route handler or the secured route handler.
4. **Data & File Storage:** Interacts with the local SQLite database (`instance/vulnlab.db`) and maintains isolated storage directories (`static/uploads/` vs. `/safe_uploads/`).

---

## 6. Docker-Based Deployment & Isolation

To provide a safe, isolated execution environment that protects the host operating system from malicious payload execution, VulnLab is containerized using Docker:

- **Minimal Attack Surface:** Built from the official `python:3.11-slim` base image, installing only necessary system dependencies (`gcc`, `libmagic1`) and keeping image size under 180 MB.
- **Container Isolation:** Arbitrary file uploads and directory traversal attacks remain strictly contained within the virtualized container filesystem.
- **Volume Persistence:** Docker Compose maps host directories for persistent database storage (`instance/`) and uploaded test files (`static/uploads/`, `safe_uploads/`).
- **Standardized Execution:** The application is built and launched with a single command:
  ```bash
  docker-compose up --build
  ```
- **Port Forwarding & Remote Access:** Port 5000 is exposed and bound to `0.0.0.0`, enabling local network access (`http://<LAN_IP>:5000`) or public access via zero-install OpenSSH reverse tunneling (`ssh -R 80:127.0.0.1:5000 nokey@localhost.run`).

---

## 7. Vulnerabilities Demonstrated

### 1. SQL Injection — Authentication Bypass
- **Vulnerability:** Unsafe string concatenation into SQL query strings (`f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"`).
- **Exploitation:** Supplying `' OR '1'='1' -- ` forces the `WHERE` clause to evaluate to `TRUE`, bypassing password verification and granting immediate access as the administrator.
- **Mitigation:** Enforcing parameterized queries via SQLAlchemy ORM (`User.query.filter_by(username=username).first()`) and verifying passwords against salted cryptographic hashes (`check_password_hash`).

### 2. SQL Injection — UNION-Based Data Disclosure
- **Vulnerability:** Search query terms interpolated directly into multi-column SQL queries without input validation.
- **Exploitation:** Injecting a `UNION SELECT username, password_hash, '1'` payload allows an attacker to extract sensitive credentials from the `users` table through product search results.
- **Mitigation:** Parameterized ORM search filtering and strict column/field whitelisting.

### 3. Stored Cross-Site Scripting (Stored XSS)
- **Vulnerability:** Unsanitized user comments submitted to the guestbook are stored in the database and rendered in the browser using Jinja2's `|safe` filter.
- **Exploitation:** Submitting `<script>fetch('/steal?c=' + document.cookie);</script>` stores the malicious payload, executing JavaScript in the session of every user who subsequently views the guestbook.
- **Mitigation:** Removing the `|safe` filter, enforcing automatic contextual HTML escaping, and applying a restrictive Content Security Policy (CSP).

### 4. Reflected Cross-Site Scripting (Reflected XSS)
- **Vulnerability:** Search parameters passed via URL query strings are echoed directly back into the response HTML without encoding.
- **Exploitation:** Crafting malicious URLs containing JavaScript payloads that execute immediately when opened by an authenticated victim.
- **Mitigation:** Applying explicit HTML entity encoding (`html.escape()`) to all reflected parameters before embedding them into response templates.

### 5. Cross-Site Request Forgery (CSRF)
- **Vulnerability:** State-changing POST endpoints (such as `/profile`) rely exclusively on ambient session cookies without verifying request origin.
- **Exploitation:** An external attacker website hosts an auto-submitting hidden HTML form that forces the victim's authenticated browser to silently change account details.
- **Mitigation:** Enforcing cryptographic anti-CSRF synchronizer tokens (`Flask-WTF`) and configuring session cookies with `SameSite=Strict`.

### 6. Insecure File Upload
- **Vulnerability:** Backend relies naively on client-supplied `Content-Type` headers and weak extension checks, saving files directly into publicly accessible web roots.
- **Exploitation:** Uploading executable scripts (e.g., `.py`, `.php`, `.html`) disguised with spoofed headers allows remote code execution and web defacement.
- **Mitigation:** Deep file signature inspection using `python-magic`, strict extension whitelisting, file content sanitization, and storing uploads outside the document root with randomized UUID filenames.

### 7. Session Fixation & Session Hijacking
- **Vulnerability:** The application accepts pre-set session identifiers without regeneration upon login, and session cookies lack the `HttpOnly` security attribute.
- **Exploitation:** An attacker forces a known session ID onto a victim prior to authentication, or steals active session cookies via client-side JavaScript (`document.cookie`).
- **Mitigation:** Mandatory session ID regeneration upon successful authentication, coupled with `HttpOnly`, `Secure`, and `SameSite=Strict` cookie attributes.

### 8. Directory Traversal & Local File Inclusion (LFI)
- **Vulnerability:** User-supplied document names are concatenated directly into local filesystem paths (`os.path.join(DOCS_DIR, filename)`).
- **Exploitation:** Providing dot-dot-slash sequences (`../../config.py`) breaks out of the intended directory to read sensitive server configuration files and database credentials.
- **Mitigation:** Path canonicalization using Werkzeug's `safe_join()`, enforcing strict base-directory boundaries, and validating input against an explicit document allowlist.

### 9. Security Headers & Clickjacking
- **Vulnerability:** Responses omit modern HTTP defense-in-depth headers and disclose server software banners (`Server: Werkzeug/Python`).
- **Exploitation:** Applications can be framed inside malicious third-party iframes to perform UI clickjacking attacks and are vulnerable to MIME-type sniffing.
- **Mitigation:** Injecting comprehensive security headers on all responses: `Content-Security-Policy`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Strict-Transport-Security`, and suppressing revealing server banners.

### 10. Password Brute Force & Authentication Abuse
- **Vulnerability:** Authentication endpoints allow unlimited login attempts without request throttling, CAPTCHA, or lockout thresholds.
- **Exploitation:** Attackers execute automated dictionary attacks and credential-stuffing tools to guess valid user credentials.
- **Mitigation:** Implementing a sliding-window in-memory rate limiter that tracks failed attempts per IP/username and enforces a temporary lockout with HTTP 429 Too Many Requests.

### 11. Reconnaissance & Information Disclosure
- **Vulnerability:** Overly descriptive crawler control files (`robots.txt`) and exposed editor backup copies (`config.py.bak`) reveal hidden administrative endpoints and internal source code.
- **Exploitation:** Attackers perform passive reconnaissance to discover unlinked admin portals and extract database passwords from forgotten backup files.
- **Mitigation:** Sanitizing `robots.txt` to avoid advertising sensitive administrative routes, removing backup files from deployment packages, and disabling route access to development artifacts.

---

## 8. Security Hardening: Vulnerable vs. Patched Matrix

| Architectural Layer | Vulnerable Sandbox Behavior | Hardened / Patched Behavior |
| :--- | :--- | :--- |
| **Database Queries** | Raw string formatting (`f"SELECT..."`) | Parameterized ORM queries (`filter_by()`) |
| **Password Storage** | Plaintext / reversible encoding | PBKDF2 with SHA-256 and cryptographic salts |
| **Template Rendering** | Unescaped raw HTML (`|safe` filter) | Context-aware HTML entity encoding |
| **Cookie Flags** | `HttpOnly=False`, `SameSite=None` | `HttpOnly=True`, `SameSite=Strict`, `Secure` |
| **File Handling** | Client-supplied MIME checks; web root storage | Magic byte inspection, randomized UUIDs, safe storage |
| **Path Access** | Direct string joining (`os.path.join()`) | Strict base-path enforcement via `safe_join()` |
| **HTTP Headers** | Reveals `Server: Werkzeug/Python` | Injects CSP, X-Frame-Options, HSTS, X-Content-Type |
| **Authentication Flow** | Unrestricted login guessing | 5-attempt sliding lockout with HTTP 429 response |
| **WAF Defense** | Disabled / passive logging only | Active IPS Mode (HTTP 403 Forbidden blocking) |

---

## 9. Testing, Verification & Results

To guarantee engineering reliability, an automated end-to-end regression test harness (`verify_all_modules.py`) was developed to validate all 11 modules across both operational states:

- **Test Coverage:** Achieved a **100% test pass rate** across all 11 functional modules and administrative controls.
- **Injection Testing:** In vulnerable mode, SQLi authentication bypass and stored XSS execution succeeded with complete evidence. In patched mode, parameterized queries and contextual escaping completely neutralized all injected payloads.
- **Path Traversal Results:** Requests to `../config.py` successfully leaked application secrets in vulnerable mode; in patched mode, the traversal was trapped by `safe_join()`, returning HTTP 404.
- **Rate-Limiting Verification:** The brute-force endpoint permitted 6 consecutive failed attempts without restriction in vulnerable mode; in patched mode, the 6th failed attempt immediately triggered an HTTP 429 lockout response.
- **WAF Interception:** In Active IPS Mode, the custom WAF successfully intercepted malicious SQLi and XSS payloads, returning HTTP 403 Forbidden and recording the event in `detections.log`.
- **Automated Pentest Report:** The reporting engine successfully aggregated security posture data into an executive-ready HTML audit report featuring CVSS severity indicators, vulnerability classifications, and step-by-step remediation guidance.

---

## 10. Future Scope

The modular architecture of VulnLab provides a solid foundation for continuous expansion:

- **Cloud-Native Deployment:** Implementing Kubernetes manifests and Helm charts to support container orchestration, auto-scaling, and multi-node cluster deployment.
- **API Security Modules:** Expanding coverage to the OWASP API Security Top 10, including GraphQL injection, JSON Web Token (JWT) signature manipulation, and Broken Object Level Authorization (BOLA/IDOR).
- **Gamified Scoring & CTF Platform:** Introducing user authentication, dynamic challenge flags, an automated submission validator, and a real-time leaderboard for competitive university CTF events.
- **Multi-Tenant User Sandboxing:** Introducing ephemeral per-user container instances or isolated namespaces so multiple learners can experiment concurrently without state collisions.
- **Dedicated Reverse-Proxy WAF:** Evaluating integration with industry-standard web application firewalls such as ModSecurity or OWASP Coraza alongside the built-in Python signature engine.

---

## 11. Conclusion

VulnLab successfully addresses the educational divide between abstract cybersecurity theory and practical, production-grade security engineering. By pairing 11 real-world vulnerability modules with an instant dual-state toggle mechanism, learners gain direct insight into both the offensive mechanics of web exploits and the defensive secure-coding practices required to neutralize them. The integration of Docker container isolation, an active Web Application Firewall, and an automated CVSS penetration-test reporting engine ensures a comprehensive, enterprise-aligned learning experience suitable for academic coursework, secure coding bootcamps, and security research.
