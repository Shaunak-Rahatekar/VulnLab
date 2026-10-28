import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

def make_page_callback(dark_mode=False):
    def page_callback(canv, doc):
        canv.saveState()
        # 1. Background
        if dark_mode:
            canv.setFillColor(colors.HexColor("#0b0f19"))
            canv.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1, stroke=0)
            if canv._pageNumber > 1:
                canv.setFont("Helvetica", 9)
                canv.setFillColor(colors.HexColor("#94a3b8"))
                canv.drawString(54, 36, "VulnLab: Project Report — VIT Pune")
                canv.drawRightString(doc.pagesize[0] - 54, 36, f"Page {canv._pageNumber}")
                canv.setStrokeColor(colors.HexColor("#334155"))
                canv.setLineWidth(0.5)
                canv.line(54, 48, doc.pagesize[0] - 54, 48)
        else:
            canv.setFillColor(colors.white)
            canv.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1, stroke=0)
            if canv._pageNumber > 1:
                canv.setFont("Helvetica", 9)
                canv.setFillColor(colors.HexColor("#64748b"))
                canv.drawString(54, 36, "VulnLab: Project Report — VIT Pune")
                canv.drawRightString(doc.pagesize[0] - 54, 36, f"Page {canv._pageNumber}")
                canv.setStrokeColor(colors.HexColor("#cbd5e1"))
                canv.setLineWidth(0.5)
                canv.line(54, 48, doc.pagesize[0] - 54, 48)
        canv.restoreState()
    return page_callback


def build_pdf(filename="VulnLab_Project_Report.pdf", dark_mode=False):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Color palette definition based on theme
    if dark_mode:
        c_title = colors.HexColor("#38bdf8")
        c_subtitle = colors.HexColor("#06b6d4")
        c_meta = colors.HexColor("#cbd5e1")
        c_team = colors.HexColor("#f1f5f9")
        c_h1 = colors.HexColor("#38bdf8")
        c_h2 = colors.HexColor("#22d3ee")
        c_body = colors.HexColor("#e2e8f0")
        c_table_hdr_bg = colors.HexColor("#0284c7")
        c_table_hdr_text = colors.white
        c_table_row1 = colors.HexColor("#0f172a")
        c_table_row2 = colors.HexColor("#1e293b")
        c_table_text = colors.HexColor("#f1f5f9")
        c_grid = colors.HexColor("#334155")
    else:
        c_title = colors.HexColor("#0f172a")
        c_subtitle = colors.HexColor("#0284c7")
        c_meta = colors.HexColor("#334155")
        c_team = colors.HexColor("#1e293b")
        c_h1 = colors.HexColor("#0f172a")
        c_h2 = colors.HexColor("#0369a1")
        c_body = colors.HexColor("#334155")
        c_table_hdr_bg = colors.HexColor("#0284c7")
        c_table_hdr_text = colors.white
        c_table_row1 = colors.white
        c_table_row2 = colors.HexColor("#f8fafc")
        c_table_text = colors.HexColor("#1e293b")
        c_grid = colors.HexColor("#cbd5e1")

    # Typography styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        alignment=1,
        textColor=c_title
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=20,
        alignment=1,
        textColor=c_subtitle
    )

    cover_meta = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        alignment=1,
        textColor=c_meta
    )

    cover_team = ParagraphStyle(
        'CoverTeam',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        alignment=1,
        textColor=c_team
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_h1,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_h2,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=c_body,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=c_table_hdr_text
    )

    table_body = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_table_text
    )

    story = []

    # ================= COVER PAGE =================
    story.append(Spacer(1, 150))
    story.append(Paragraph("VULNLAB", title_style))
    story.append(Spacer(1, 16))
    story.append(Paragraph("A Docker-Based Vulnerable Web Application<br/>for Exploitation and Security Hardening", subtitle_style))
    story.append(Spacer(1, 40))
    story.append(Paragraph("<b>Project Report</b>", cover_meta))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Department of Computer Engineering<br/>Vishwakarma Institute of Technology, Pune<br/>Subject: Ethical Hacking &amp; Application Security", cover_meta))
    story.append(Spacer(1, 130))
    story.append(Paragraph("<b>Team Members:</b> Shaunak Rahatekar, Sanyam Patwari, Raman Vhantale, Sharwari Rajput", cover_team))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Project Mentor / Guide:</b> Ms. Jyoti Hindurao Yadav", cover_team))
    story.append(PageBreak())

    # ================= BODY PAGES =================
    story.append(Paragraph("1. Project Title", h1_style))
    story.append(Paragraph("<b>VulnLab: A Docker-Based Vulnerable Web Application for Exploitation and Security Hardening</b>", body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. Introduction", h1_style))
    story.append(Paragraph("2.1 Introduction", h2_style))
    story.append(Paragraph(
        "VulnLab is an interactive, Docker-containerized educational security sandbox designed to connect cybersecurity "
        "theory with practical offensive and defensive application-security work. It provides 11 interactive vulnerability "
        "modules covering common web-application weaknesses, including injection, cross-site scripting, authentication "
        "weaknesses, access-control issues, file-handling flaws, and information disclosure.", body_style
    ))
    story.append(Paragraph(
        "A central feature is its dual-state design: users can switch at runtime between a deliberately vulnerable mode and "
        "a patched mode. This lets learners observe an attack in a controlled environment, inspect the corresponding code, "
        "and compare it with a defensive implementation. The platform also features a custom Web Application Firewall (WAF) "
        "with passive alerting and active blocking modes, automated Python exploit scripts, CVSS-oriented risk scoring, "
        "and an HTML penetration-test report.", body_style
    ))
    story.append(Paragraph(
        "The application is built with Python and Flask, uses SQLite through Flask-SQLAlchemy, and provides a browser-based "
        "interface built with vanilla JavaScript and CSS. Docker and Docker Compose support repeatable deployment for classroom "
        "demonstrations and security-training exercises.", body_style
    ))

    story.append(Paragraph("2.2 Problem Statement", h2_style))
    story.append(Paragraph(
        "Cybersecurity learners may understand vulnerability definitions in theory but still struggle to recognize unsafe code, "
        "reproduce the underlying behavior, and implement an effective fix. Traditional teaching can lack interactive "
        "environments that show both the exploitable behavior and its secure counterpart. Some existing labs can also require "
        "additional setup and may not provide an immediate side-by-side view of vulnerable and remediated code.", body_style
    ))
    story.append(Paragraph(
        "VulnLab addresses this learning gap by bringing multiple web vulnerabilities into one portable sandbox. For each module, "
        "the learner can examine the attack technique, observe its effect in vulnerable mode, and compare the result with a patched "
        "implementation. The environment is intended for authorized, local or otherwise controlled educational testing, not for "
        "testing systems without permission.", body_style
    ))

    story.append(Paragraph("2.3 Project Objectives", h2_style))
    objectives = [
        "<b>Demonstrate Real-World Vulnerability Mechanics:</b> Expose root causes of vulnerabilities including string concatenation, unescaped rendering, missing headers, and insecure path operations.",
        "<b>Provide Safe &amp; Controlled Exploitation:</b> Deliver automated Python exploit scripts and web forms for hands-on, zero-risk attack reproduction.",
        "<b>Teach Practical Defensive Engineering:</b> Implement enterprise mitigations: parameterized ORM queries, PBKDF2-SHA256 password hashing, anti-CSRF tokens, and safe path joining.",
        "<b>Simulate Enterprise Security Infrastructure:</b> Deploy a custom Web Application Firewall (WAF) with passive alerting and active 403 IPS blocking, alongside automated CVSS pentest risk reports.",
        "<b>Ensure Isolated Portability:</b> Provide one-command deployment via Docker containers to guarantee repeatable, isolated testing across all operating systems."
    ]
    for obj in objectives:
        story.append(Paragraph(f"• {obj}", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("3. Project Scope", h1_style))
    story.append(Paragraph(
        "The project scope covers a comprehensive web-based training environment for demonstrating common web vulnerabilities "
        "and their mitigations. The principal capabilities include:", body_style
    ))
    scope_bullets = [
        "<b>11 Vulnerability Modules:</b> Demonstrations spanning SQL injection, XSS, CSRF, insecure uploads, session weaknesses, path traversal/LFI, security headers, brute-force attempts, and reconnaissance/information disclosure.",
        "<b>Dual-State Execution:</b> A runtime toggle switches between vulnerable and patched behavior across individual modules without requiring a server restart.",
        "<b>Code-Level Learning:</b> Learners can compare vulnerable patterns with safer implementations and inspect root-cause code diffs directly in the user interface.",
        "<b>Guarded Intel Vault:</b> Tiered guidance (Concepts, Attack Vectors, Payloads) protected by confirmation shields to encourage independent student problem-solving.",
        "<b>WAF/IPS Layer:</b> A custom middleware layer inspects requests for selected attack patterns; passive mode records or alerts, while active mode blocks matching requests with HTTP 403 Forbidden.",
        "<b>Automated Testing:</b> Python-based attack scripts and an end-to-end verification suite (<code>verify_all_modules.py</code>) validate behavior across all modules and modes with 100% pass verification.",
        "<b>Risk Reporting:</b> An automated HTML penetration-test report includes CVSS severity indicators and remediation guidance.",
        "<b>Portable Deployment:</b> Docker/Docker Compose deployment and an alternative Python virtual-environment setup support repeatable use across common desktop operating systems.",
        "<b>Training Use Cases:</b> The system is designed for academic laboratories, secure-coding training, and controlled CTF-style exercises."
    ]
    for sc in scope_bullets:
        story.append(Paragraph(f"• {sc}", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("4. Technology Stack", h1_style))
    
    tech_data = [
        [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Technology / Purpose</b>", table_header)],
        [Paragraph("Backend language", table_body), Paragraph("Python 3.11+", table_body)],
        [Paragraph("Web framework", table_body), Paragraph("Flask 3.0, organized with modular Blueprints", table_body)],
        [Paragraph("Database", table_body), Paragraph("SQLite 3", table_body)],
        [Paragraph("ORM", table_body), Paragraph("Flask-SQLAlchemy 3.1", table_body)],
        [Paragraph("Security utilities", table_body), Paragraph("Werkzeug password hashing (PBKDF2-SHA256), Flask-WTF CSRF protection, python-magic file-signature inspection", table_body)],
        [Paragraph("Frontend", table_body), Paragraph("HTML with custom vanilla CSS and modular vanilla JavaScript (sandbox.js)", table_body)],
        [Paragraph("UI styling and fonts", table_body), Paragraph("Cyberpunk / glassmorphism visual style; Inter and JetBrains Mono fonts", table_body)],
        [Paragraph("Containerization", table_body), Paragraph("Docker Engine and Docker Compose; python:3.11-slim base image", table_body)],
        [Paragraph("Automated offensive testing", table_body), Paragraph("Python requests-based attack scripts in the attacks/ directory", table_body)],
        [Paragraph("Testing and reporting", table_body), Paragraph("verify_all_modules.py test harness; HTML penetration-test report with CVSS-oriented severity indicators", table_body)]
    ]
    t = Table(tech_data, colWidths=[150, 354])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_table_hdr_bg),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, c_grid),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [c_table_row1, c_table_row2])
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    story.append(Paragraph("5. System Architecture &amp; Workflow", h1_style))
    story.append(Paragraph(
        "VulnLab operates a layered request-dispatch architecture designed to demonstrate defensive interception and dual-state execution:", body_style
    ))
    arch_bullets = [
        "<b>Client Interaction Layer:</b> A responsive web interface providing interactive challenge forms, theme switching (Dark/Light), runtime mode toggles, and a guarded Intel Vault modal.",
        "<b>WAF Middleware Inspection:</b> Inbound requests are analyzed by regex rules targeting SQLi, XSS, and LFI patterns. In Passive mode, detections are logged to <code>detections.log</code>; in Active IPS mode, requests are terminated immediately with HTTP 403 Forbidden.",
        "<b>Core State Router:</b> Evaluates global toggle state (<code>VULN_MODE</code>) and routes the request to either the vulnerable implementation or the patched implementation.",
        "<b>Storage &amp; Data Layer:</b> Interfaces with SQLite database via SQLAlchemy ORM (patched) or raw SQL strings (vulnerable), maintaining quarantined media in <code>static/uploads/</code>."
    ]
    for ab in arch_bullets:
        story.append(Paragraph(f"• {ab}", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("6. Docker-Based Deployment &amp; Sandbox Isolation", h1_style))
    story.append(Paragraph(
        "To protect the host operating system from untrusted payloads, VulnLab is packaged in a lightweight Docker container:", body_style
    ))
    docker_bullets = [
        "<b>Sandbox Quarantining:</b> File uploads and traversal attempts are constrained entirely within the virtualized container filesystem.",
        "<b>Volume Persistence:</b> Docker Compose maps host volumes for <code>instance/</code> (database) and upload directories, preserving state between restarts.",
        "<b>Multi-Platform Support:</b> Standardized configuration across Windows, macOS, and Linux executed via <code>docker-compose up --build</code>.",
        "<b>Network Binding &amp; Remote Access:</b> Binds to <code>0.0.0.0:5000</code>, enabling local Wi-Fi sharing and public tunneling via OpenSSH reverse tunnels."
    ]
    for db in docker_bullets:
        story.append(Paragraph(f"• {db}", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("7. Vulnerabilities Demonstrated", h1_style))
    story.append(Paragraph(
        "The following 11 modules represent the core application-security curriculum demonstrated in VulnLab:", body_style
    ))

    vulns = [
        ("1. SQL Injection — Authentication Bypass", 
         "Unsafe concatenation of user input into a SQL query alters query logic (<code>' OR '1'='1' -- </code>) and bypasses authentication checks without knowing credentials. <b>Mitigation:</b> Use parameterized SQLAlchemy ORM queries and verify passwords against salted PBKDF2 hashes."),
        ("2. SQL Injection — UNION-Based Data Disclosure",
         "Manipulating an unfiltered search query with a <code>UNION SELECT</code> clause extracts unauthorized tables and credential hashes. <b>Mitigation:</b> Use parameterized queries and enforce strict whitelisting on permitted search columns."),
        ("3. Stored Cross-Site Scripting (Stored XSS)",
         "Malicious script content saved into the guestbook database executes in the browser of users viewing the page due to unescaped Jinja2 <code>|safe</code> filters. <b>Mitigation:</b> Context-aware output escaping, safe template rendering, and a restrictive Content Security Policy (CSP)."),
        ("4. Reflected Cross-Site Scripting (Reflected XSS)",
         "Untrusted search terms reflected immediately in HTTP responses are executed as client-side script code. <b>Mitigation:</b> Contextual HTML entity encoding (<code>html.escape()</code>) before embedding input into templates."),
        ("5. Cross-Site Request Forgery (CSRF)",
         "A logged-in user visiting a malicious external site is tricked into submitting unwanted profile changes via an auto-submitting hidden HTML form. <b>Mitigation:</b> Cryptographic anti-CSRF synchronizer tokens (Flask-WTF) and <code>SameSite=Strict</code> cookie attributes."),
        ("6. Insecure File Upload",
         "Insufficient upload validation allows dangerous web shells (e.g. <code>.py</code>, <code>.php</code>) to be stored in publicly accessible directories. <b>Mitigation:</b> Magic byte signature validation (<code>python-magic</code>), strict extension whitelisting, and isolated storage with randomized UUID filenames."),
        ("7. Session Fixation &amp; Session Hijacking",
         "Weak session handling and omission of <code>HttpOnly</code> cookie flags allow attackers to pre-set session tokens or steal them via <code>document.cookie</code>. <b>Mitigation:</b> Session ID regeneration upon authentication and configuring cookies with <code>HttpOnly</code>, <code>Secure</code>, and <code>SameSite=Strict</code>."),
        ("8. Directory Traversal &amp; Local File Inclusion (LFI)",
         "Manipulating filenames with parent-directory dot-dot-slash sequences (<code>../../config.py</code>) leaks server files outside the document root. <b>Mitigation:</b> Path normalization, Werkzeug's <code>safe_join()</code>, and an explicit file allowlist."),
        ("9. Security Headers &amp; Clickjacking",
         "Missing browser security headers expose users to framing-based UI redressing and MIME-sniffing attacks. <b>Mitigation:</b> Configure comprehensive defense headers: <code>Content-Security-Policy</code>, <code>X-Frame-Options: DENY</code>, <code>X-Content-Type-Options: nosniff</code>, and <code>HSTS</code>."),
        ("10. Password Brute Force &amp; Authentication Abuse",
         "Unrestricted login endpoints allow rapid automated credential-guessing attacks. <b>Mitigation:</b> In-memory sliding-window IP rate limiting, failed attempt tracking, and temporary account lockout with HTTP 429 Too Many Requests."),
        ("11. Reconnaissance &amp; Information Disclosure",
         "Publicly exposed <code>robots.txt</code> files and leftover editor backup copies (<code>config.py.bak</code>) reveal secret endpoints and configuration files. <b>Mitigation:</b> Sanitize public crawler metadata, remove backup artifacts from production, and suppress verbose server banners.")
    ]

    for title, desc in vulns:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(desc, body_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("8. Security Hardening: Vulnerable vs. Patched Matrix", h1_style))
    matrix_data = [
        [Paragraph("<b>Architectural Layer</b>", table_header), Paragraph("<b>Vulnerable Sandbox Behavior</b>", table_header), Paragraph("<b>Hardened / Patched Behavior</b>", table_header)],
        [Paragraph("Database Queries", table_body), Paragraph("Raw SQL string interpolation (<code>f'...'</code>)", table_body), Paragraph("Parameterized ORM queries (<code>filter_by()</code>)", table_body)],
        [Paragraph("Password Storage", table_body), Paragraph("Plaintext / reversible encoding", table_body), Paragraph("PBKDF2 with SHA-256 and unique salts", table_body)],
        [Paragraph("Template Rendering", table_body), Paragraph("Raw unescaped HTML (<code>|safe</code>)", table_body), Paragraph("Auto-escaped Jinja2 context encoding", table_body)],
        [Paragraph("Cookie Security", table_body), Paragraph("<code>HttpOnly=False</code>, <code>SameSite=None</code>", table_body), Paragraph("<code>HttpOnly=True</code>, <code>SameSite=Strict</code>, <code>Secure</code>", table_body)],
        [Paragraph("File Handling", table_body), Paragraph("Raw extension check, writes to web root", table_body), Paragraph("Magic byte MIME check, randomized UUID storage", table_body)],
        [Paragraph("Path Access", table_body), Paragraph("Concatenation (<code>os.path.join()</code>)", table_body), Paragraph("Whitelist validation &amp; <code>safe_join()</code>", table_body)],
        [Paragraph("HTTP Headers", table_body), Paragraph("Leaks <code>Server: Werkzeug/Python</code>", table_body), Paragraph("Injects CSP, HSTS, X-Frame-Options, X-Content-Type", table_body)],
        [Paragraph("Authentication Flow", table_body), Paragraph("Unlimited password guessing attempts", table_body), Paragraph("5-attempt sliding lockout with HTTP 429", table_body)],
        [Paragraph("WAF Policy", table_body), Paragraph("Inactive / Passive logging", table_body), Paragraph("Active IPS Mode (HTTP 403 Forbidden blocking)", table_body)]
    ]
    mt = Table(matrix_data, colWidths=[120, 192, 192])
    mt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_table_hdr_bg),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, c_grid),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [c_table_row1, c_table_row2])
    ]))
    story.append(mt)
    story.append(Spacer(1, 10))

    story.append(Paragraph("9. Testing, Verification &amp; Results", h1_style))
    story.append(Paragraph(
        "An automated end-to-end regression test suite (<code>verify_all_modules.py</code>) was developed to validate all 11 modules across both operational states:", body_style
    ))
    test_results = [
        "<b>100% Test Pass Rate:</b> All 11 functional modules and security controls passed automated verification without failure.",
        "<b>Exploitation Verification:</b> In vulnerable mode, SQLi authentication bypass, UNION data extraction, Stored XSS, Directory Traversal, and unlimited brute-force attacks all succeeded with clear evidentiary output.",
        "<b>Remediation Verification:</b> In patched mode, parameterized ORM queries, output escaping, Werkzeug <code>safe_join()</code>, and IP lockout thresholds completely blocked all automated attack payloads.",
        "<b>WAF IPS Interception:</b> In Active IPS mode, malicious SQL and XSS requests were rejected with HTTP 403 Forbidden, logging IP, endpoint, and signature IDs to <code>detections.log</code>.",
        "<b>Executive Pentest Report Output:</b> The reporting module automatically aggregated system vulnerabilities into an HTML audit report featuring CVSS severity indicators, CVSS vector strings, and remediation blueprints."
    ]
    for tr in test_results:
        story.append(Paragraph(f"• {tr}", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("10. Applications, Limitations &amp; Future Scope", h1_style))
    story.append(Paragraph("<b>Practical Applications:</b>", body_style))
    apps = [
        "<b>Academic Laboratories:</b> Laboratory companion for university courses in Ethical Hacking, Information Security, and Web Engineering.",
        "<b>Secure Coding Training:</b> Benchmark training platform for junior software developers and DevSecOps teams.",
        "<b>CTF Competitions:</b> Pre-configured, zero-setup challenge environment for collegiate capture-the-flag competitions."
    ]
    for ap in apps:
        story.append(Paragraph(f"• {ap}", bullet_style))

    story.append(Paragraph("<b>Current Limitations &amp; Future Scope:</b>", body_style))
    future_bullets = [
        "<b>Cloud-Native Deployment:</b> Add Kubernetes deployment manifests and Helm charts to support container orchestration and horizontal auto-scaling.",
        "<b>API Security Modules:</b> Extend coverage with OWASP API Security Top 10 challenges, including GraphQL injection, JWT tampering, and Broken Object-Level Authorization (BOLA/IDOR).",
        "<b>Gamified Learning Engine:</b> Introduce student user accounts, challenge flags, scoring rubrics, and a live competitive leaderboard.",
        "<b>Multi-Tenant Isolation:</b> Introduce per-user container instances or ephemeral namespaces to prevent multi-user state collisions.",
        "<b>Dedicated WAF Integration:</b> Integrate external industry-standard reverse-proxy firewalls (such as ModSecurity or OWASP Coraza) alongside the built-in regex engine."
    ]
    for fb in future_bullets:
        story.append(Paragraph(f"• {fb}", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("11. Conclusion", h1_style))
    story.append(Paragraph(
        "VulnLab successfully bridges the educational divide between abstract cybersecurity concepts and hands-on secure software "
        "engineering. By combining 11 real-world vulnerability demonstrations with an instant dual-state toggle mechanism, "
        "learners gain direct insight into both offensive exploit mechanics and defensive remediation patterns. The inclusion of "
        "Docker containerization, a custom Web Application Firewall with active IPS blocking, and an automated CVSS penetration-test "
        "reporting engine provides a comprehensive, enterprise-aligned learning platform suitable for academic instruction, "
        "developer training, and application security research.", body_style
    ))

    cb = make_page_callback(dark_mode=dark_mode)
    doc.build(story, onFirstPage=cb, onLaterPages=cb)
    print(f"SUCCESS: Generated {filename} (dark_mode={dark_mode})")


if __name__ == '__main__':
    # 1. Standard Light Theme (with solid white opaque background for dark mode viewers)
    build_pdf("VulnLab_Project_Report.pdf", dark_mode=False)
    # 2. Native Dark Theme (Cyberpunk dark background with bright text and cyan titles)
    build_pdf("VulnLab_Project_Report_Dark.pdf", dark_mode=True)
