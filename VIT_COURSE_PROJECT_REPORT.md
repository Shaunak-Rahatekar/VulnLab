# A Ethical Hacking Course Project Report on
# VulnLab: A Docker-Based Vulnerable Web Application for Exploitation and Security Hardening

SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS  
FOR THE DEGREE OF  
**BACHELOR OF TECHNOLOGY IN Computer Engineering**  
OF  
**VISHWAKARMA INSTITUTE OF TECHNOLOGY**  
**Savitribai Phule Pune University**  

**Submitted by:**  
- Shaunak Rahatekar  
- Sanyam Patwari  
- Raman Vhantale  
- Sharwari Rajput  

**UNDER THE GUIDANCE OF**  
**Prof. Jyoti Hindurao Yadav**  

DEPARTMENT OF COMPUTER ENGINEERING  
BANSILAL RAMNATH AGARWAL CHARITABLE TRUST’S  
**VISHWAKARMA INSTITUTE OF TECHNOLOGY**  
(An Autonomous Institute affiliated to Savitribai Phule Pune University)  
PUNE – 411037  
**Academic Year: 2026 – 2027**  

---

## CERTIFICATE

This is to certify that the Course Project titled **“VulnLab: A Docker-Based Vulnerable Web Application for Exploitation and Security Hardening”** submitted by **Shaunak Rahatekar, Sanyam Patwari, Raman Vhantale, and Sharwari Rajput** is in partial fulfillment for the award of Degree of Bachelor of Technology in Department of Computer Engineering of Vishwakarma Institute of Technology, Savitribai Phule Pune University. This project report is a record of bonafide work carried out by them under my guidance during the academic year 2026–27.

| Guide | HOD, Computer Engineering |
| :--- | :--- |
| **Prof. Jyoti Hindurao Yadav** | **Prof. Dr. Sandip Shinde** |

**Place:** VIT, Pune  
**Date:** 28/10/26  

---

## PROJECT SYNOPSIS

**Project Title:** VulnLab: A Docker-Based Vulnerable Web Application for Exploitation and Security Hardening  
**Project Area:** Ethical Hacking and Web Application Security  

VulnLab is an interactive, Docker-containerized educational cybersecurity sandbox designed to connect ethical hacking theory with practical offensive and defensive application-security engineering. The project establishes an isolated multi-tiered testing laboratory comprising 11 interactive vulnerability modules covering the OWASP Top 10 spectrum, an active hybrid Web Application Firewall (WAF/IPS), a runtime dual-state switching engine, and an automated CVSS penetration test reporting pipeline.

The platform focuses on demonstrating real-world exploitation techniques—including SQL Injection (Authentication Bypass and UNION data extraction), Stored and Reflected XSS, Cross-Site Request Forgery (CSRF), Insecure File Upload, Session Fixation, Directory Traversal (LFI), Security Header Misconfiguration, Credential Brute-Forcing, and Information Disclosure. Each vulnerable route is paired with an isolated defensive counterpart. Users can toggle at runtime between Vulnerable and Patched modes to observe how defensive secure-coding patterns (parameterized ORM queries, contextual output escaping, CSRF tokens, safe path normalization, and IP rate limiting) mitigate attacks.

The verified results demonstrate 100% test pass rates across an end-to-end Python regression test suite (`verify_all_modules.py`), successful active WAF interception returning HTTP 429 and HTTP 403 Forbidden responses, and automated HTML audit reporting with CVSS risk scoring.

**Group Members:**

| Roll No. | Name of Student | Email ID |
| :--- | :--- | :--- |
| **1** | Shaunak Rahatekar | shaunak.rahatekar@vit.edu |
| **2** | Sanyam Patwari | sanyam.patwari@vit.edu |
| **3** | Raman Vhantale | raman.vhantale@vit.edu |
| **4** | Sharwari Rajput | sharwari.rajput@vit.edu |

**Internal Guide:** Prof. Jyoti Yadav  
**Signature of Internal Guide:** ___________________________  

---

## ACKNOWLEDGEMENT

We would like to express our sincere gratitude to our project guide, **Prof. Jyoti Yadav**, for the valuable guidance, continuous support, and constructive feedback provided throughout the development of *VulnLab: A Docker-Based Vulnerable Web Application for Exploitation and Security Hardening*.

We are grateful to **Prof. Dr. Sandip Shinde**, Head of the Department of Computer Engineering, and the authorities of **Vishwakarma Institute of Technology, Pune**, for providing the academic infrastructure, laboratories, and resources necessary to successfully execute this project.

We also acknowledge the collaborative efforts of all team members in architecting the Docker sandbox, implementing the vulnerability modules, developing the WAF inspection engine, writing automated exploit scripts, and conducting rigorous security verification. Finally, we thank the open-source community, OWASP Foundation, and Flask developers for their reference standards and documentation.

---

## 5. Introduction

With the increasing reliance on web applications for critical financial, commercial, and personal operations, application security has become an indispensable component of modern computer engineering. Web applications remain the primary entry point for cyber threats globally. Vulnerabilities such as SQL injection, Cross-Site Scripting (XSS), insecure deserialization, broken authentication, and security misconfigurations frequently result in catastrophic data breaches, identity theft, and corporate compromise.

To understand these security threats effectively, cybersecurity students and software engineers require practical, hands-on exposure to how vulnerabilities are exploited and, crucially, how resilient code is designed. Theoretical lectures provide definitions, but learners frequently struggle to bridge the gap between identifying an abstract vulnerability and writing production-grade defensive mitigations.

To address this educational challenge, we developed **VulnLab: A Docker-Based Vulnerable Web Application for Exploitation and Security Hardening**. VulnLab is a full-stack educational security laboratory providing 11 interactive, syllabus-aligned vulnerability modules, paired with runtime side-by-side defensive controls, an active Web Application Firewall (WAF) with Intrusion Prevention System (IPS) blocking, and an automated Executive Penetration Test Reporting system.

### 5.1 Background and Motivation
Traditional web security training platforms (such as DVWA, WebGoat, or bWAPP) often present several significant pedagogical limitations:
1. **Legacy Deployment Friction:** They often require obsolete software environments (PHP 5, legacy MySQL) that are complex to configure and maintain on modern desktop operating systems.
2. **Absence of Dual-State Code Inspection:** Most training environments only expose broken code. Learners see the exploit succeed, but are left without immediate, code-level visibility into how to write the remediated implementation.
3. **Lack of Defensive Controls:** Traditional labs rarely incorporate modern enterprise defense tools, such as Web Application Firewalls, Content Security Policies, rate-limiting thresholds, or automated CVSS audit reporting.

VulnLab was conceived to unify offensive security exploitation and defensive software engineering into a single, cohesive, Docker-isolated platform.

### 5.2 Problem Statement
Cybersecurity education often isolates offensive testing (ethical hacking) from defensive engineering (secure coding). When these concepts are taught separately, learners fail to understand the direct causal relationship between insecure code syntax and exploit feasibility. Furthermore, running live exploits on unprotected host operating systems risks malware infection and accidental system instability.

VulnLab solves this problem by providing a containerized, zero-configuration sandbox that pairs every vulnerable code path with an instant runtime toggle to a secure implementation. Learners can execute automated exploit scripts, observe backend server behavior, inspect side-by-side code diffs, and evaluate active WAF mitigation in real time.

### 5.3 Project Objectives
The core objectives of the VulnLab project are:
1. **Establish a Quarantined Sandbox:** Deploy a containerized environment using Docker and Docker Compose to isolate dangerous payloads from the host operating system.
2. **Demonstrate 11 Core Web Vulnerabilities:** Provide hands-on exploitation across the OWASP Top 10 spectrum, including SQLi, Stored/Reflected XSS, CSRF, File Upload, Session Fixation, LFI, Security Headers, Brute Force, and Reconnaissance.
3. **Implement Dual-State Runtime Execution:** Engineer a global state-switching engine enabling instant toggling between Vulnerable and Patched states without restarting the Flask server.
4. **Deploy an Active WAF/IPS Middleware Layer:** Inspect inbound HTTP traffic for malicious patterns, providing Passive alerting and Active IPS blocking (HTTP 403 Forbidden).
5. **Automate Penetration Test Verification & Reporting:** Develop an end-to-end Python regression test harness (`verify_all_modules.py`) and an automated HTML reporting engine with CVSS severity scoring.

### 5.4 Scope of the Project
The scope of VulnLab encompasses:
- Full-stack web application development in Python 3.11+ using the Flask microframework and SQLAlchemy ORM.
- 11 dedicated challenge modules with associated automated Python exploit scripts in `attacks/`.
- A modern Cyberpunk/Glassmorphism user interface with Dark/Light theme switching and a 3-tier guarded Intel Vault.
- Containerized deployment via multi-stage Docker builds and automated volume mounting.
- In-memory sliding-window rate limiting (HTTP 429) and signature-based WAF filtering.
- Verification and audit reporting aligning with the academic syllabus for Ethical Hacking and Information Security.

### 5.5 Project Methodology
The project followed an agile, test-driven security engineering lifecycle:
1. **Curriculum Alignment:** Identified 11 foundational vulnerability classes covering injection, broken access control, authentication, and reconnaissance.
2. **Architectural Design:** Formulated the dual-state routing model where every route branches into an unsafe function or a hardened function based on `VULN_MODE`.
3. **Module Implementation:** Developed backend Flask blueprints and semantic HTML5 templates, eliminating dangerous inline script parsing quirks.
4. **Defensive Hardening:** Implemented industry-standard mitigations (parameterized queries, PBKDF2 hashing, CSP headers, Werkzeug `safe_join`).
5. **WAF & Automation Engine:** Built regex-based inspection hooks and the automated CVSS executive audit reporter.
6. **Containerization & Testing:** Encapsulated the environment into Docker containers and executed 100% automated regression verification.

---

## 6. SYSTEM ARCHITECTURE AND LAB SETUP

VulnLab is engineered as a self-contained, multi-layered security laboratory. The architecture isolates the presentation layer, inspection middleware, application routing, and persistent database storage.

```
+-----------------------------------------------------------------------------------+
|                                 Client Web Browser                                |
|        (Cyberpunk Glassmorphism UI / Dark-Light Theme / Guarded Intel Vault)      |
+-----------------------------------------------------------------------------------+
                                         │
                          HTTP Requests (Port 5000)
                                         ▼
+-----------------------------------------------------------------------------------+
|                         WAF Middleware Inspection Layer                           |
|        (Regex Pattern Matching: SQLi, XSS, Path Traversal, Command Injection)     |
|               [Passive Mode: Log Alert]  vs.  [Active Mode: HTTP 403 Block]       |
+-----------------------------------------------------------------------------------+
                                         │
                             Verified Traffic Forwarding
                                         ▼
+-----------------------------------------------------------------------------------+
|                        Flask Application Core & State Router                      |
|                               (VULN_MODE State Flags)                             |
+-----------------------------------------------------------------------------------+
           │                                                       │
           ▼                                                       ▼
  [Vulnerable Branch]                                     [Patched Branch]
  - Raw string interpolation SQL                          - Parameterized SQLAlchemy ORM
  - Unescaped Jinja2 (|safe)                              - Context-aware HTML escaping
  - Missing Anti-CSRF verification                        - Flask-WTF CSRF tokens
  - Arbitrary filename joining                            - Safe-join path traversal guards
  - Unrestricted authentication attempts                  - Sliding-window IP rate limiting
           │                                                       │
           └───────────────────────────┬───────────────────────────┘
                                       │
                                       ▼
+-----------------------------------------------------------------------------------+
|                       Persistent Data & Isolated Storage                          |
|             SQLite Database (instance/vulnlab.db) | /safe_uploads/                |
+-----------------------------------------------------------------------------------+
```

### 6.1 Machine and Component Roles

| Component | Technology / Environment | Role & Responsibilities |
| :--- | :--- | :--- |
| **Attacker / Client** | Browser / Python `requests` | Originates simulated exploit payloads and automated attack scripts. |
| **WAF / IPS Filter** | Flask `before_request` hook | Inspects URI, query strings, and POST bodies against malicious signatures. |
| **Application Core** | Python 3.11 / Flask 3.0 | Evaluates state flags and dispatches requests to vulnerable or secured handlers. |
| **Database Tier** | SQLite 3 / Flask-SQLAlchemy | Stores user credentials, product catalogs, and guestbook comments. |
| **Quarantine Storage** | Docker Volume (`safe_uploads/`) | Quarantines file uploads outside the web execution root. |

### 6.2 Network and Processing Architecture
The application binds to `0.0.0.0:5000`, making it accessible across local virtual networks, host-only adapters, and LAN environments (`http://192.168.0.x:5000`). For remote collaborative evaluations, zero-configuration OpenSSH reverse tunnels (`ssh -R 80:127.0.0.1:5000 nokey@localhost.run`) establish public HTTPS endpoints with automatic TLS termination.

### 6.3 Data Flow
1. An incoming HTTP request arrives at Port 5000.
2. The WAF middleware examines the request URI, parameters, and form payload. If Active IPS mode is enabled and a malicious signature matches, the request is terminated with HTTP 403 Forbidden.
3. If approved, the request enters the Flask router, which reads the active module configuration from `VULN_MODE`.
4. The router executes either the vulnerable branch or the patched branch.
5. In vulnerable mode, unsanitized inputs interact directly with the database or filesystem. In patched mode, inputs pass through ORM parameterization, cryptographic hash verification, or path normalization.
6. Security response headers (`X-Frame-Options`, `CSP`, `X-Content-Type-Options`) are injected by the `after_request` filter before sending the response to the client.

### 6.4 Design Considerations and Constraints
- **Host Security:** The entire sandbox is containerized to prevent uploaded web shells or path traversal exploits from escaping into the developer's host filesystem.
- **Independence:** The platform operates with zero external cloud dependencies, utilizing SQLite and local static files.
- **Instructional Guardrails:** Solutions and payloads are shielded inside a locked "Intel Vault" requiring explicit user confirmation to discourage passive answer copying.

---

## 7. IMPLEMENTATION OF MAJOR MODULES

### 7.1 Docker Sandboxing & Virtual Lab Configuration
VulnLab is containerized using Docker to deliver a clean, repeatable environment. The `Dockerfile` uses the official `python:3.11-slim` base image, installing required system libraries (`libmagic1` for file signature inspection) and application dependencies from `requirements.txt`. `docker-compose.yml` mounts host volumes for `instance/` (SQLite database) and upload directories, ensuring data persistence across container restarts while quarantining untrusted file execution.

### 7.2 Web Application Security Modules

#### 1. SQL Injection (Authentication Bypass)
- **Vulnerability:** User credentials in `modules/sqli.py` are interpolated directly into raw SQL strings using Python f-strings: `f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"`.
- **Exploit:** Supplying `' OR '1'='1' -- ` forces the `WHERE` condition to evaluate to true for all records, logging in as the first database user (Administrator) without a password.
- **Mitigation:** Enforcing parameterized queries via SQLAlchemy ORM (`User.query.filter_by(username=username).first()`) and verifying salted PBKDF2 hashes using `check_password_hash()`.

#### 2. SQL Injection (UNION Data Extraction)
- **Vulnerability:** Search queries concatenate raw input: `f"SELECT name, price, description FROM products WHERE name LIKE '%{query}%'"`.
- **Exploit:** Injecting `' UNION SELECT username, password_hash, '1' FROM users -- ` combines product results with sensitive credential hashes from the `users` table.
- **Mitigation:** Utilizing parameterized query binding and strict column whitelisting.

#### 3. Stored Cross-Site Scripting (Stored XSS)
- **Vulnerability:** Guestbook comments are stored in the database and rendered back to the user with Jinja2's `|safe` filter, disabling automatic HTML escaping.
- **Exploit:** Injecting `<script>fetch('/steal?c=' + document.cookie);</script>` stores the script, executing in every victim's browser session upon viewing the guestbook.
- **Mitigation:** Removing the `|safe` filter, enforcing automatic contextual HTML escaping, and deploying strict Content Security Policies (`CSP`).

#### 4. Reflected Cross-Site Scripting (Reflected XSS)
- **Vulnerability:** Search query parameters passed via the URL (`/search_reflected?q=...`) are echoed directly into the DOM without sanitization.
- **Exploit:** Crafting links with malicious payloads that execute when clicked by authenticated users.
- **Mitigation:** Passing reflected parameters through `html.escape()` before template rendering.

#### 5. Cross-Site Request Forgery (CSRF)
- **Vulnerability:** State-changing POST endpoints (such as `/profile`) rely exclusively on ambient session cookies without request origin validation.
- **Exploit:** Hosting an external malicious web page with an auto-submitting hidden HTML form targeting the authenticated user's session.
- **Mitigation:** Enforcing cryptographic Anti-CSRF Synchronizer Tokens via `Flask-WTF` and configuring cookies with `SameSite=Strict`.

#### 6. Insecure File Upload
- **Vulnerability:** Naive file extension checks and reliance on client-controlled `Content-Type` headers allow dangerous executable scripts (`.py`, `.php`) to be saved into publicly accessible directories.
- **Exploit:** Uploading disguised web shells allowing arbitrary remote code execution on the server.
- **Mitigation:** Deep file signature (magic byte) verification using `python-magic`, strict extension whitelisting, randomized UUID filename generation, and storage outside the web root.

#### 7. Session Fixation & Hijacking
- **Vulnerability:** Session identifiers are accepted from client cookies prior to authentication and are not regenerated upon login. Additionally, cookies lack the `HttpOnly` flag.
- **Exploit:** Attackers pre-set a victim's session ID or steal active session tokens via `document.cookie`.
- **Mitigation:** Regenerating session IDs upon successful login and enforcing `HttpOnly=True`, `Secure=True`, and `SameSite=Strict` cookie attributes.

#### 8. Directory Traversal & Local File Inclusion (LFI)
- **Vulnerability:** File viewing parameters are directly concatenated into filesystem paths: `os.path.join(DOCS_DIR, filename)`.
- **Exploit:** Supplying dot-dot-slash sequences (`../../config.py`) to escape the directory root and read sensitive configuration and database credentials.
- **Mitigation:** Path canonicalization using Werkzeug's `safe_join()`, validating paths against base directories, and enforcing an explicit file allowlist.

#### 9. Security Headers & Clickjacking Audit
- **Vulnerability:** Missing browser defense headers leave the application vulnerable to UI Redressing (Clickjacking) via malicious `<iframe>` tags.
- **Exploit:** Embedding the target web page in an invisible iframe overlay to hijack authenticated clicks.
- **Mitigation:** Injecting `Content-Security-Policy`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, and `HSTS`, while stripping revealing server software banners.

#### 10. Password Brute Force & Rate Limiting
- **Vulnerability:** The authentication endpoint allows unlimited login attempts without request throttling or account lockouts.
- **Exploit:** Executing high-speed dictionary brute-force attacks using automated wordlists.
- **Mitigation:** Deploying a sliding-window in-memory rate limiter tracking failed attempts per IP and enforcing an HTTP 429 Too Many Requests lockout after 5 consecutive failures.

#### 11. Reconnaissance & Information Disclosure
- **Vulnerability:** Publicly exposed crawler instructions (`robots.txt`) and developer backup files (`config.py.bak`) advertise sensitive admin routes and internal source code.
- **Exploit:** Performing passive discovery to uncover hidden endpoints and database credentials.
- **Mitigation:** Sanitizing crawler metadata, removing development artifacts from production builds, and suppressing verbose HTTP server banners.

### 7.3 Web Application Firewall (WAF) & Signature Engine
The custom WAF middleware (`modules/detector.py`) inspects all incoming requests against compiled regular expression signatures:
- **SQLi Detection:** Identifies `UNION SELECT`, `' OR '1'='1'`, comment operators (`--`, `/*`), and boolean tautologies.
- **XSS Detection:** Detects `<script>`, `onerror=`, `onload=`, and `javascript:` URIs.
- **Path Traversal Detection:** Identifies `../`, `..\\`, and URL-encoded `%2e%2e%2f` sequences.
- **Operational Modes:**
  - *Passive Mode (IDS):* Records the attack event, source IP, endpoint, and signature ID to `detections.log` and allows traffic to proceed.
  - *Active Mode (IPS):* Halts execution immediately, returning an HTTP 403 Forbidden alert to the client.

### 7.4 Global State Management and Dual-State Engine
The application state is centralized in `config.py` via the `VULN_MODE` dictionary. A dedicated administrative manager blueprint (`modules/admin_manager.py`) exposes secure POST endpoints (`/admin/toggle/<feature>` and `/admin/reset_lab`). Administrators can toggle individual module states dynamically at runtime without restarting the server, as well as restore database tables, clear uploaded files, and flush WAF detection logs to pristine initial states with one click.

### 7.5 Interactive Web Interface & Guarded Intel Vault
The user interface is designed with vanilla CSS adhering to a Cyberpunk/Glassmorphism design system. A modular client-side engine (`static/sandbox.js`) manages theme switching (Dark/Light), toast notifications, and interactive modals. Crucially, challenge hints and payloads are protected inside an interactive **Intel Vault** requiring multi-tier confirmation shields (Concepts $\rightarrow$ Attack Vectors $\rightarrow$ Exploit Payloads), preventing students from passively revealing answers without thoughtful analysis.

### 7.6 Automated Pentest Report Generator
The reporting module (`modules/report.py`) analyzes all verified exploits across the session. It computes CVSS v3.1 base metrics, classifies vulnerabilities by risk rating (Critical, High, Medium, Low), and compiles an executive-ready HTML penetration test report featuring executive summaries, vulnerability registers, and technical remediation blueprints.

---

## 8. RESULTS AND TESTING

The VulnLab project underwent rigorous verification using both automated regression scripts and interactive exploitation.

### 8.1 Automated Regression Verification (`verify_all_modules.py`)
An end-to-end Python test suite was developed to programmatically test all 11 modules under both operational modes:
- **Vulnerable State:** Validates that attack scripts successfully bypass authentication, extract unauthorized data, execute scripts, and traverse directories.
- **Patched State:** Validates that defensive controls neutralize all attack payloads, returning expected security statuses (HTTP 200 sanitized, HTTP 404 not found, HTTP 429 locked, or HTTP 403 forbidden).

### 8.2 Testing Summary Matrix

| Test / Component | Vulnerable Mode Result | Patched Mode Result | Status |
| :--- | :--- | :--- | :--- |
| **SQLi Auth Bypass** | Admin session established via `' OR '1'='1` | Query rejected; invalid credentials | **Verified** |
| **SQLi UNION Extraction** | Admin password hashes extracted | Parameterized query; zero leak | **Verified** |
| **Stored XSS** | `<script>` persisted and executed in DOM | Contextual HTML escaping enforced | **Verified** |
| **Reflected XSS** | Injected URL parameter executed in browser | Reflected query encoded safely | **Verified** |
| **CSRF Protection** | Unauthenticated POST modified profile | Request blocked; missing CSRF token | **Verified** |
| **File Upload Filter** | Arbitrary `.py` web shell uploaded | Blocked by magic byte signature check | **Verified** |
| **Session Fixation** | Pre-set session ID adopted across login | Session ID regenerated; HttpOnly set | **Verified** |
| **Directory Traversal** | `../../config.py` leaked secrets | Blocked by Werkzeug `safe_join` (404) | **Verified** |
| **Security Headers** | Headers missing; iframe embedding allowed | CSP & X-Frame-Options block iframe | **Verified** |
| **Brute Force Lockout** | Unlimited login attempts permitted | 5th failure triggered HTTP 429 lockout | **Verified** |
| **Reconnaissance** | Sensitive routes leaked in `robots.txt` | Admin routes hidden; `.bak` returns 404 | **Verified** |
| **WAF Active IPS** | Malicious requests allowed & logged | Malicious requests blocked (HTTP 403) | **Verified** |
| **Lab Reset Engine** | Database modified by exploits | Restored database & cleared test logs | **Verified** |

### 8.3 Test Evidence & Observations
- **Test Pass Rate:** 100% pass rate achieved across all functional modules.
- **WAF Interception:** In Active IPS mode, the WAF successfully intercepted malicious SQLi and XSS payloads within 2 milliseconds, logging the client IP and signature ID to `detections.log`.
- **Rate-Limiting Lockout:** During automated dictionary testing (`attacks/bruteforce_attack.py`), the backend accepted 5 failed attempts before immediately locking the IP address with an HTTP 429 response on attempt 6.

### 8.4 Evaluation Limitations
- The WAF signature engine operates as an in-memory Python middleware rather than an external reverse proxy (such as ModSecurity or Cloudflare).
- The current deployment uses a single-container sandbox without per-user ephemeral session isolation.
- Rate limiting is tracked in memory, meaning server restarts reset active lockout counters.

---

## 9. CONCLUSION

The **VulnLab: A Docker-Based Vulnerable Web Application for Exploitation and Security Hardening** project successfully bridges the divide between theoretical cybersecurity education and practical secure software engineering. By integrating 11 OWASP Top 10 vulnerability modules with an instant runtime dual-state switching engine, students gain direct, hands-on experience in both offensive exploitation mechanics and defensive remediation patterns.

The addition of Docker container isolation, a custom Web Application Firewall with Active IPS blocking, a guarded 3-tier Intel Vault, and an automated CVSS penetration test reporting engine establishes VulnLab as a robust, production-aligned learning platform for university laboratories, secure coding bootcamps, and CTF competitions.

### 9.1 Current Limitations
- Single-tenant execution model without multi-user resource quotas.
- In-memory WAF signature rules rather than distributed firewall rule evaluation.
- Focus is centered on web application vulnerabilities, excluding lower-level network protocol attacks.

### 9.2 Future Enhancements
- **Cloud-Native Kubernetes Deployment:** Develop Helm charts for container orchestration, horizontal auto-scaling, and per-student isolated container pods.
- **OWASP API Security Top 10:** Expand modules to cover modern API vulnerabilities (GraphQL injection, JWT tampering, and Broken Object-Level Authorization - BOLA/IDOR).
- **Gamified CTF Scoring Engine:** Incorporate user registration, dynamic flag generation, and a real-time competitive leaderboard for university hackathons.

---

## 10. REFERENCES

1. **OWASP Foundation.** *OWASP Top 10: The Ten Most Critical Web Application Security Risks.* OWASP Foundation, 2021.
2. **Flask Documentation.** *Flask Web Development Documentation (v3.0.x).* Pallets Projects, 2023.
3. **SQLAlchemy Documentation.** *SQLAlchemy Unified Tutorial & ORM Security Best Practices.* SQLAlchemy Authors, 2023.
4. **Docker Documentation.** *Docker Engine & Docker Compose Official Architecture Guide.* Docker Inc., 2023.
5. **NIST.** *Special Publication 800-115: Technical Guide to Information Security Testing and Assessment.* National Institute of Standards and Technology, 2008.
6. **Common Vulnerability Scoring System (CVSS).** *CVSS v3.1 Specification Document.* FIRST.Org, Inc., 2019.
7. **B. Sullivan and V. Liu.** *Web Application Security, A Beginner’s Guide.* McGraw-Hill Education, 2012.
8. **D. Stuttard and M. Pinto.** *The Web Application Hacker’s Handbook: Finding and Exploiting Security Flaws.* John Wiley & Sons, 2011.
