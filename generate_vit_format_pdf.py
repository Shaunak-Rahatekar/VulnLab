import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class VITNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self):
        self.saveState()
        # Draw solid opaque white background on every page
        self.setFillColor(colors.white)
        self.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
        
        # Draw top-right page number exactly as in the reference format
        self.setFont("Times-Roman", 11)
        self.setFillColor(colors.black)
        self.drawRightString(letter[0] - 54, letter[1] - 40, str(self._pageNumber))
        self.restoreState()


def build_vit_report_pdf():
    pdf_path = "VulnLab_VIT_Project_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Academic Typography Styles matching the reference document
    t_center_bold_lg = ParagraphStyle(
        'TCenterBoldLg',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=15,
        leading=19,
        alignment=1, # Center
        textColor=colors.black
    )

    t_center_bold_md = ParagraphStyle(
        'TCenterBoldMd',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.black
    )

    t_center_reg = ParagraphStyle(
        'TCenterReg',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.black
    )

    t_center_bold_sm = ParagraphStyle(
        'TCenterBoldSm',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.black
    )

    # Section Headings
    h1_style = ParagraphStyle(
        'VITHeading1',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=13,
        leading=17,
        spaceBefore=14,
        spaceAfter=6,
        textColor=colors.black,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'VITHeading2',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11.5,
        leading=15,
        spaceBefore=10,
        spaceAfter=4,
        textColor=colors.black,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'VITBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10.5,
        leading=15,
        spaceAfter=6,
        textColor=colors.black
    )

    body_justify = ParagraphStyle(
        'VITBodyJustify',
        parent=body_style,
        alignment=4 # Justify
    )

    bullet_style = ParagraphStyle(
        'VITBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.black
    )

    table_body = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9,
        leading=12,
        textColor=colors.black
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("A Ethical Hacking Course Project Report on", t_center_reg))
    story.append(Spacer(1, 14))
    story.append(Paragraph("<b>VulnLab: A Docker-Based Vulnerable Web Application<br/>for Exploitation and Security Hardening</b>", t_center_bold_lg))
    story.append(Spacer(1, 18))
    story.append(Paragraph("<i>SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS<br/>FOR THE DEGREE OF</i>", ParagraphStyle('ItalicSub', parent=t_center_reg, fontName='Times-Italic', fontSize=10)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>BACHELOR OF TECHNOLOGY</b><br/>IN<br/><b>Computer Engineering</b>", t_center_bold_md))
    story.append(Spacer(1, 6))
    story.append(Paragraph("OF<br/><b>VISHWAKARMA INSTITUTE OF TECHNOLOGY</b><br/><b>Savitribai Phule Pune University</b>", t_center_bold_sm))
    story.append(Spacer(1, 24))
    
    # Team members
    team_p1 = [
        "<b>Shaunak Rahatekar (12410728)</b>",
        "<b>Sanyam Patwari (12414525)</b>",
        "<b>Raman Vhantale (12410098)</b>",
        "<b>Sharwari Rajput (12414940)</b>"
    ]
    for mem in team_p1:
        story.append(Paragraph(mem, t_center_bold_sm))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 30))
    story.append(Paragraph("<i>UNDER THE GUIDANCE OF</i>", ParagraphStyle('ItalicGuide', parent=t_center_reg, fontName='Times-Italic', fontSize=10)))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Prof. Jyoti Hindurao Yadav</b>", t_center_bold_md))
    story.append(Spacer(1, 40))

    story.append(Paragraph("DEPARTMENT OF COMPUTER ENGINEERING", t_center_bold_sm))
    story.append(Spacer(1, 2))
    story.append(Paragraph("BANSILAL RAMNATH AGARWAL CHARITABLE TRUST’S", t_center_reg))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>VISHWAKARMA INSTITUTE OF TECHNOLOGY</b>", t_center_bold_md))
    story.append(Spacer(1, 2))
    story.append(Paragraph("(An Autonomous Institute affiliated to Savitribai Phule Pune University)", t_center_reg))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>2026 – 2027</b>", t_center_bold_sm))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: CERTIFICATE
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("BANSILAL RAMNATH AGARWAL CHARITABLE TRUST’S", t_center_reg))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>VISHWAKARMA INSTITUTE OF TECHNOLOGY</b>", t_center_bold_md))
    story.append(Spacer(1, 2))
    story.append(Paragraph("(An Autonomous Institute affiliated to Savitribai Phule Pune University)", t_center_reg))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>PUNE – 411037</b>", t_center_bold_sm))
    story.append(Spacer(1, 35))
    story.append(Paragraph("<b>CERTIFICATE</b>", t_center_bold_lg))
    story.append(Spacer(1, 30))

    cert_text = (
        "This is to certify that the Course Project titled <b>“VulnLab: A Docker-Based Vulnerable Web Application "
        "for Exploitation and Security Hardening”</b> submitted by <b>Shaunak Rahatekar (12410728), Sanyam Patwari "
        "(12414525), Raman Vhantale (12410098), Sharwari Rajput (12414940)</b> is in partial fulfillment for the award "
        "of Degree of Bachelor of Technology in Department of Computer Engineering of Vishwakarma Institute of "
        "Technology, Savitribai Phule Pune University. This project report is a record of bonafide work carried out "
        "by them under my guidance during the academic year <b>2026–27</b>."
    )
    story.append(Paragraph(cert_text, body_justify))
    story.append(Spacer(1, 80))

    sig_data = [
        [Paragraph("<b>Guide</b><br/><b>Prof. Jyoti Hindurao Yadav</b>", body_style),
         Paragraph("<b>HOD, Computer Engineering</b><br/><b>Prof. Dr. Sandip Shinde</b>", body_style)]
    ]
    sig_table = Table(sig_data, colWidths=[250, 250])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (0,0), 'LEFT'),
        ('ALIGN', (1,0), (1,0), 'RIGHT')
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 60))

    story.append(Paragraph("<b>Place:</b> VIT, Pune<br/><b>Date:</b> 28/10/26", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: PROJECT SYNOPSIS
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("Bansilal Ramnath Agarwal Charitable Trust’s", t_center_reg))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Vishwakarma Institute of Technology, Pune-37</b>", t_center_bold_md))
    story.append(Spacer(1, 2))
    story.append(Paragraph("DEPARTMENT OF COMPUTER ENGINEERING", t_center_bold_sm))
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>PROJECT SYNOPSIS</b>", t_center_bold_lg))
    story.append(Spacer(1, 16))

    story.append(Paragraph("<b>Project Title:</b> VulnLab: A Docker-Based Vulnerable Web Application for Exploitation and Security Hardening", body_style))
    story.append(Paragraph("<b>Project Area:</b> Ethical Hacking and Web Application Security", body_style))
    story.append(Spacer(1, 6))

    synopsis_p1 = (
        "VulnLab is a course project that combines hands-on vulnerability exploitation, defensive secure-coding "
        "engineering, real-time WAF request inspection, and an automated penetration-test reporting engine. The project "
        "deploys an isolated Docker container hosting 11 interactive vulnerability modules covering the OWASP Top 10 "
        "curriculum, including SQL Injection, Cross-Site Scripting (XSS), CSRF, Insecure File Upload, Path Traversal, "
        "Session Fixation, and Brute-Force Authentication."
    )
    story.append(Paragraph(synopsis_p1, body_justify))

    synopsis_p2 = (
        "A central innovation is its runtime dual-state switching engine: learners can toggle between deliberately vulnerable "
        "implementations and production-grade patched implementations without server restarts. A custom Web Application "
        "Firewall (WAF) inspects inbound HTTP requests, supporting both passive alerting and active IPS blocking (HTTP 403). "
        "An automated test suite (<code>verify_all_modules.py</code>) validates exploit and mitigation behaviors with 100% test pass rate."
    )
    story.append(Paragraph(synopsis_p2, body_justify))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Group No:</b> B24", body_style))
    story.append(Paragraph("<b>Members:</b>", body_style))
    story.append(Spacer(1, 4))

    member_data = [
        [Paragraph("<b>Roll No.</b>", table_header), Paragraph("<b>G.R. No.</b>", table_header), Paragraph("<b>Name of Student</b>", table_header), Paragraph("<b>Email ID</b>", table_header)],
        [Paragraph("16", table_body), Paragraph("12410728", table_body), Paragraph("Shaunak Rahatekar", table_body), Paragraph("shaunak.rahatekar@vit.edu", table_body)],
        [Paragraph("18", table_body), Paragraph("12414525", table_body), Paragraph("Sanyam Patwari", table_body), Paragraph("sanyam.patwari@vit.edu", table_body)],
        [Paragraph("23", table_body), Paragraph("12410098", table_body), Paragraph("Raman Vhantale", table_body), Paragraph("raman.vhantale@vit.edu", table_body)],
        [Paragraph("37", table_body), Paragraph("12414940", table_body), Paragraph("Sharwari Rajput", table_body), Paragraph("sharwari.rajput@vit.edu", table_body)]
    ]
    t_members = Table(member_data, colWidths=[60, 80, 160, 200])
    t_members.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t_members)
    story.append(Spacer(1, 25))

    story.append(Paragraph("<b>Internal Guide:</b> Prof. Jyoti Yadav", body_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Signature of Internal Guide:</b> ___________________________", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: ACKNOWLEDGEMENT
    # =========================================================================
    story.append(Spacer(1, 30))
    story.append(Paragraph("<b>ACKNOWLEDGEMENT</b>", t_center_bold_lg))
    story.append(Spacer(1, 25))

    ack_text = [
        "We would like to express our sincere gratitude to our project guide, <b>Prof. Jyoti Yadav</b>, for the valuable guidance, support, and constructive feedback provided throughout the development of <i>VulnLab: A Docker-Based Vulnerable Web Application for Exploitation and Security Hardening</i>.",
        "We are thankful to <b>Vishwakarma Institute of Technology</b> and the <b>Department of Computer Engineering</b> for providing the academic environment, state-of-the-art computational infrastructure, and opportunity to undertake this project as part of our Ethical Hacking course.",
        "We also acknowledge the contributions of all team members in planning the sandbox architecture, implementing the 11 vulnerability modules, configuring the custom WAF/IPS engine, building automated Python attack scripts, and executing comprehensive test verifications.",
        "Finally, we acknowledge the official documentation, the OWASP Foundation, and the open-source security community for providing the research foundations and benchmark standards that guided this project."
    ]
    for p in ack_text:
        story.append(Paragraph(p, body_justify))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 5: INTRODUCTION
    # =========================================================================
    story.append(Paragraph("5. Introduction", h1_style))
    intro_p1 = (
        "With the rapid expansion of cloud infrastructure and web-delivered services, application security has become "
        "an essential cornerstone of modern software engineering. Web applications are targeted by automated scanners, "
        "credential stuffers, and sophisticated threat actors. Vulnerabilities such as SQL injection, Cross-Site Scripting "
        "(XSS), insecure direct object references, and broken authentication can lead to catastrophic data breaches and system compromise."
    )
    story.append(Paragraph(intro_p1, body_justify))

    intro_p2 = (
        "To address these threats, cybersecurity learners require hands-on experience examining vulnerabilities from both "
        "an offensive perspective (how an attack is mounted) and a defensive perspective (how the underlying code is remediated). "
        "VulnLab combines 11 interactive challenge modules, a runtime dual-state switching engine, a custom Web Application "
        "Firewall (WAF/IPS), and an automated CVSS penetration test reporting pipeline into a single Docker-isolated environment."
    )
    story.append(Paragraph(intro_p2, body_justify))

    story.append(Paragraph("5.1 Background and Motivation", h2_style))
    bg_p = (
        "Traditional training platforms like DVWA or WebGoat provide exploitable exercises but frequently suffer from setup "
        "complexities, outdated software dependencies, and a complete lack of side-by-side defensive code diffs. Learners observe "
        "the attack succeed, but are left guessing how the production patch should look. VulnLab was created to bridge this divide "
        "by pairing every vulnerability with an instant toggle to a secure implementation."
    )
    story.append(Paragraph(bg_p, body_justify))

    story.append(Paragraph("5.2 Problem Statement", h2_style))
    prob_p = (
        "Ethical hacking and secure coding are frequently taught as disconnected disciplines. When students study exploits without "
        "inspecting defensive code, they fail to develop secure development habits. Furthermore, running live exploits on unprotected "
        "host operating systems presents security hazards. VulnLab solves this problem by delivering a containerized, zero-configuration "
        "sandbox featuring runtime toggles, code diff inspection, and active WAF blocking."
    )
    story.append(Paragraph(prob_p, body_justify))

    story.append(Paragraph("5.3 Project Objectives", h2_style))
    objs = [
        "Establish an isolated Docker sandbox to quarantine attack simulations and file uploads.",
        "Implement 11 core web application security modules covering the OWASP Top 10 spectrum.",
        "Engineer a runtime dual-state engine enabling instant switching between Vulnerable and Patched modes.",
        "Develop an active hybrid Web Application Firewall (WAF) supporting Passive logging and Active IPS blocking (HTTP 403).",
        "Automate end-to-end regression testing with Python exploit scripts and compile an executive CVSS pentest report."
    ]
    for ob in objs:
        story.append(Paragraph(f"• {ob}", bullet_style))

    story.append(Paragraph("5.4 Scope of the Project", h2_style))
    scope_p = (
        "The project scope covers full-stack application development in Python 3.11 and Flask 3.0, 11 dedicated vulnerability "
        "modules, automated Python exploit scripts in <code>attacks/</code>, custom WAF pattern matching, and an automated HTML "
        "reporting module. The platform is designed for university laboratories, secure coding bootcamps, and CTF competitions."
    )
    story.append(Paragraph(scope_p, body_justify))

    story.append(Paragraph("5.5 Project Methodology", h2_style))
    method_p = (
        "The project followed an iterative security engineering lifecycle: curriculum alignment, dual-state route architecture, "
        "blueprint implementation, defense hardening, WAF middleware integration, Docker containerization, and 100% automated "
        "regression test verification."
    )
    story.append(Paragraph(method_p, body_justify))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 6: SYSTEM ARCHITECTURE AND LAB SETUP
    # =========================================================================
    story.append(Paragraph("6. SYSTEM ARCHITECTURE AND LAB SETUP", h1_style))
    arch_p = (
        "VulnLab is organized as a layered, modular sandbox. Incoming requests pass through WAF inspection middleware, "
        "reach the Flask core router, and are dispatched to either vulnerable or hardened handlers based on global state flags."
    )
    story.append(Paragraph(arch_p, body_justify))
    story.append(Spacer(1, 4))

    arch_table_data = [
        [Paragraph("<b>Component / Machine</b>", table_header), Paragraph("<b>Address / Environment</b>", table_header), Paragraph("<b>Role &amp; Responsibilities</b>", table_header)],
        [Paragraph("Attacker / Client", table_body), Paragraph("Browser / Localhost", table_body), Paragraph("Executes automated Python exploit scripts and submits interactive forms.", table_body)],
        [Paragraph("WAF Middleware Layer", table_body), Paragraph("In-memory Flask filter", table_body), Paragraph("Inspects URI, queries, and POST bodies. Supports Passive alerting and Active 403 IPS blocking.", table_body)],
        [Paragraph("Flask Application Core", table_body), Paragraph("0.0.0.0:5000 (Python 3.11)", table_body), Paragraph("Evaluates VULN_MODE flags and dispatches requests to vulnerable or secured route handlers.", table_body)],
        [Paragraph("Database Tier", table_body), Paragraph("instance/vulnlab.db (SQLite)", table_body), Paragraph("Persists user accounts, products, and guestbook entries via Flask-SQLAlchemy.", table_body)],
        [Paragraph("Quarantined Storage", table_body), Paragraph("Docker Volume (/safe_uploads)", table_body), Paragraph("Quarantines uploaded test files outside the web execution root.", table_body)]
    ]
    t_arch = Table(arch_table_data, colWidths=[120, 140, 240])
    t_arch.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 8))

    story.append(Paragraph("6.1 Network &amp; Processing Architecture", h2_style))
    story.append(Paragraph(
        "The application binds to <code>0.0.0.0:5000</code>, enabling seamless accessibility across local LAN networks "
        "(<code>http://192.168.0.x:5000</code>). For external collaboration, OpenSSH reverse tunnels "
        "(<code>ssh -R 80:127.0.0.1:5000 nokey@localhost.run</code>) provide instant public HTTPS URLs.", body_justify
    ))

    story.append(Paragraph("6.2 Data Flow", h2_style))
    data_flow_steps = [
        "1. <b>Inbound Request:</b> Client submits an HTTP request to Port 5000.",
        "2. <b>WAF Inspection:</b> Middleware checks the request against SQLi, XSS, and LFI regex signatures. In Active IPS mode, malicious requests terminate immediately with HTTP 403.",
        "3. <b>State Evaluation:</b> The core router reads the active feature toggle in <code>VULN_MODE</code>.",
        "4. <b>Branch Execution:</b> In Vulnerable mode, raw inputs execute unsafe logic. In Patched mode, inputs undergo ORM parameterization, contextual escaping, or path normalization.",
        "5. <b>Header Injection:</b> The <code>after_request</code> hook attaches defense headers (CSP, X-Frame-Options) before returning the response."
    ]
    for dfs in data_flow_steps:
        story.append(Paragraph(dfs, bullet_style))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 7: IMPLEMENTATION OF MAJOR MODULES
    # =========================================================================
    story.append(Paragraph("7. IMPLEMENTATION OF MAJOR MODULES", h1_style))
    story.append(Paragraph(
        "This section details the 11 vulnerability modules, the custom WAF/IPS engine, and the reporting pipeline.", body_justify
    ))

    mod_details = [
        ("7.1 SQL Injection — Authentication Bypass (Level 1)",
         "In vulnerable mode, user input is concatenated directly into SQL queries: <code>f\"SELECT * FROM users WHERE username='{username}' AND password='{password}'\"</code>. Supplying <code>' OR '1'='1' -- </code> bypasses password validation and logs in as Administrator. In patched mode, SQLAlchemy ORM parameterization (<code>User.query.filter_by(...)</code>) and salted PBKDF2 hash checks neutralize the injection completely."),
        ("7.2 SQL Injection — UNION-Based Data Disclosure (Level 2)",
         "In search queries, raw input concatenation allows attackers to append <code>' UNION SELECT username, password_hash, '1' FROM users -- </code>, dumping password hashes onto the screen. In patched mode, parameterized query binding and strict column whitelisting prevent unauthorized data extraction."),
        ("7.3 Stored Cross-Site Scripting (Level 3)",
         "Guestbook comments are rendered using Jinja2's <code>|safe</code> filter. Attackers submit <code>&lt;script&gt;fetch('/steal?c=' + document.cookie)&lt;/script&gt;</code>, which persists in the database and executes in the browsers of all visitors. Patched mode removes <code>|safe</code>, enforcing contextual HTML entity escaping and Content Security Policies."),
        ("7.4 Reflected Cross-Site Scripting (Level 4)",
         "Search parameters in URL queries are echoed directly back into the response without encoding. Patched mode applies <code>html.escape()</code> to encode HTML characters before embedding values into templates."),
        ("7.5 Cross-Site Request Forgery (Level 5)",
         "State-changing POST endpoints (<code>/profile</code>) rely solely on ambient session cookies. An external page with an auto-submitting hidden form forces unauthorized profile updates. Patched mode enforces Flask-WTF Anti-CSRF Synchronizer Tokens and <code>SameSite=Strict</code> cookies."),
        ("7.6 Insecure File Upload (Level 6)",
         "The upload handler naively trusts client-supplied MIME headers and saves files in the web root. Attackers upload executable <code>.py</code> or <code>.php</code> scripts for remote code execution. Patched mode uses <code>python-magic</code> for binary signature validation, whitelists extensions, and saves files outside the web root with randomized UUID filenames."),
        ("7.7 Session Fixation &amp; Hijacking (Level 7)",
         "Session IDs are accepted before login and cookies lack the <code>HttpOnly</code> attribute, allowing cookie theft via <code>document.cookie</code>. Patched mode regenerates session identifiers upon authentication and sets <code>HttpOnly=True</code>, <code>Secure=True</code>, and <code>SameSite=Strict</code>."),
        ("7.8 Directory Traversal &amp; LFI (Level 8)",
         "Document names are concatenated directly into paths: <code>os.path.join(DOCS_DIR, filename)</code>. Submitting <code>../../config.py</code> leaks backend credentials. Patched mode normalizes paths using Werkzeug's <code>safe_join()</code> and enforces an explicit file allowlist."),
        ("7.9 Security Headers &amp; Clickjacking (Level 9)",
         "Missing HTTP defense headers allow third-party sites to frame the application in an invisible <code>&lt;iframe&gt;</code> (UI Redressing). Patched mode injects <code>Content-Security-Policy</code>, <code>X-Frame-Options: DENY</code>, and <code>X-Content-Type-Options: nosniff</code>, blocking frame embedding."),
        ("7.10 Password Brute Force &amp; Rate Limiting (Level 10)",
         "Unrestricted login endpoints allow automated dictionary guessing attacks. Patched mode implements an in-memory sliding-window IP rate limiter that enforces an HTTP 429 Too Many Requests lockout after 5 consecutive failures."),
        ("7.11 Reconnaissance &amp; Information Disclosure (Level 11)",
         "Overly descriptive <code>robots.txt</code> files and exposed <code>config.py.bak</code> backup files disclose administrative routes and database passwords. Patched mode sanitizes crawler metadata and removes sensitive backup endpoints.")
    ]

    for title, desc in mod_details:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(desc, body_justify))

    story.append(Paragraph("7.12 Web Application Firewall (WAF/IPS) Engine", h2_style))
    story.append(Paragraph(
        "The WAF inspects inbound requests against compiled regular expression signatures targeting SQLi, XSS, and LFI. "
        "In Passive mode, it logs alerts to <code>detections.log</code>. In Active IPS mode, it terminates malicious requests "
        "immediately with an HTTP 403 Forbidden response.", body_justify
    ))

    story.append(Paragraph("7.13 Automated Pentest Report Generator", h2_style))
    story.append(Paragraph(
        "The reporting module (<code>modules/report.py</code>) calculates CVSS v3.1 severity scores for all verified exploits "
        "and compiles an executive-ready HTML penetration test report with risk ratings, affected endpoints, and remediation blueprints.", body_justify
    ))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 8: RESULTS AND TESTING
    # =========================================================================
    story.append(Paragraph("8. RESULTS AND TESTING", h1_style))
    story.append(Paragraph(
        "VulnLab was verified through automated end-to-end Python test scripts (<code>verify_all_modules.py</code>) "
        "and manual attack validation.", body_justify
    ))
    story.append(Spacer(1, 4))

    test_matrix = [
        [Paragraph("<b>Test / Component</b>", table_header), Paragraph("<b>Vulnerable State Observation</b>", table_header), Paragraph("<b>Patched State Mitigation</b>", table_header), Paragraph("<b>Status</b>", table_header)],
        [Paragraph("SQLi Auth Bypass", table_body), Paragraph("Admin login bypass via ' OR '1'='1", table_body), Paragraph("Query rejected; invalid credentials", table_body), Paragraph("Verified", table_body)],
        [Paragraph("SQLi UNION Extraction", table_body), Paragraph("Password hashes leaked in search", table_body), Paragraph("Safe parameterized query; zero leak", table_body), Paragraph("Verified", table_body)],
        [Paragraph("Stored XSS", table_body), Paragraph("&lt;script&gt; executed from DB in DOM", table_body), Paragraph("Contextual HTML escaping enforced", table_body), Paragraph("Verified", table_body)],
        [Paragraph("Reflected XSS", table_body), Paragraph("URL parameter executed in browser", table_body), Paragraph("Reflected parameter encoded safely", table_body), Paragraph("Verified", table_body)],
        [Paragraph("CSRF Protection", table_body), Paragraph("External POST forged profile update", table_body), Paragraph("HTTP 400 Bad Request; missing token", table_body), Paragraph("Verified", table_body)],
        [Paragraph("File Upload Security", table_body), Paragraph("Arbitrary .py web shell uploaded", table_body), Paragraph("Rejected by magic byte signature check", table_body), Paragraph("Verified", table_body)],
        [Paragraph("Session Fixation", table_body), Paragraph("Pre-set session adopted across login", table_body), Paragraph("Session regenerated; HttpOnly enabled", table_body), Paragraph("Verified", table_body)],
        [Paragraph("Directory Traversal", table_body), Paragraph("../../config.py leaked credentials", table_body), Paragraph("Trapped by safe_join; returns HTTP 404", table_body), Paragraph("Verified", table_body)],
        [Paragraph("Security Headers", table_body), Paragraph("Headers omitted; iframe framing allowed", table_body), Paragraph("CSP & X-Frame-Options block iframe", table_body), Paragraph("Verified", table_body)],
        [Paragraph("Brute Force Lockout", table_body), Paragraph("Unlimited login attempts allowed", table_body), Paragraph("6th attempt triggered HTTP 429 lockout", table_body), Paragraph("Verified", table_body)],
        [Paragraph("Reconnaissance", table_body), Paragraph("Hidden routes leaked in robots.txt", table_body), Paragraph("Routes sanitized; backup files 404", table_body), Paragraph("Verified", table_body)],
        [Paragraph("WAF Active IPS Mode", table_body), Paragraph("Attacks logged in passive mode", table_body), Paragraph("Attacks blocked with HTTP 403 Forbidden", table_body), Paragraph("Verified", table_body)]
    ]
    t_test = Table(test_matrix, colWidths=[100, 150, 190, 60])
    t_test.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_test)
    story.append(Spacer(1, 8))

    story.append(Paragraph("8.1 Summary of Results", h2_style))
    res_summary = (
        "The automated verification suite confirmed a <b>100% test pass rate</b> across all 11 modules. In vulnerable mode, "
        "every exploit successfully demonstrated security impact. In patched mode, every attack was cleanly neutralized. "
        "The active WAF intercepted malicious payloads within 2 milliseconds, and the rate limiter triggered an HTTP 429 lockout "
        "upon the 6th failed attempt during automated brute-force execution."
    )
    story.append(Paragraph(res_summary, body_justify))

    story.append(Paragraph("8.2 Evaluation Limitations", h2_style))
    story.append(Paragraph(
        "Current testing relies on simulated attack traffic and Python in-memory rate limiting. Real-world deployments "
        "would benefit from distributed reverse-proxy WAFs (such as ModSecurity) and multi-tenant user isolation.", body_justify
    ))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 9: CONCLUSION
    # =========================================================================
    story.append(Paragraph("9. CONCLUSION", h1_style))
    concl_p = (
        "The <b>VulnLab: A Docker-Based Vulnerable Web Application for Exploitation and Security Hardening</b> project "
        "successfully demonstrates the integration of ethical hacking attack methodologies with production-grade defensive "
        "software engineering. By providing 11 interactive vulnerability modules with an instant runtime dual-state switching "
        "engine, learners gain direct insight into how insecure code syntax produces exploitable vulnerabilities and how modern "
        "defensive mitigations neutralize threats."
    )
    story.append(Paragraph(concl_p, body_justify))

    concl_p2 = (
        "The inclusion of Docker container sandboxing, an active Web Application Firewall with IPS blocking, a guarded Intel Vault, "
        "and an automated CVSS penetration test reporting engine establishes VulnLab as an effective, self-contained educational "
        "laboratory suitable for academic courses in Ethical Hacking, Application Security, and Software Engineering."
    )
    story.append(Paragraph(concl_p2, body_justify))

    story.append(Paragraph("9.1 Current Limitations", h2_style))
    story.append(Paragraph(
        "The current implementation uses a single-container sandbox without per-user resource quotas or multi-tenant session isolation. "
        "The WAF operates as a Python middleware signature engine rather than an external reverse proxy.", body_justify
    ))

    story.append(Paragraph("9.2 Future Enhancements", h2_style))
    future_enh = [
        "<b>Cloud-Native Kubernetes Deployment:</b> Helm charts for auto-scaling and per-student isolated container pods.",
        "<b>OWASP API Security Top 10:</b> Expanding modules to include GraphQL injection, JWT tampering, and BOLA/IDOR.",
        "<b>Gamified CTF Engine:</b> Adding student authentication, dynamic flag generation, and a real-time leaderboard."
    ]
    for fe in future_enh:
        story.append(Paragraph(f"• {fe}", bullet_style))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 10: REFERENCES
    # =========================================================================
    story.append(Paragraph("10. REFERENCES", h1_style))
    refs = [
        "1. <b>OWASP Foundation.</b> <i>OWASP Top 10: The Ten Most Critical Web Application Security Risks.</i> OWASP Foundation, 2021.",
        "2. <b>Flask Documentation.</b> <i>Flask Web Development Documentation (v3.0.x).</i> Pallets Projects, 2023.",
        "3. <b>SQLAlchemy Documentation.</b> <i>SQLAlchemy Unified Tutorial &amp; ORM Security Best Practices.</i> SQLAlchemy Authors, 2023.",
        "4. <b>Docker Documentation.</b> <i>Docker Engine &amp; Docker Compose Architecture Guide.</i> Docker Inc., 2023.",
        "5. <b>NIST.</b> <i>Special Publication 800-115: Technical Guide to Information Security Testing and Assessment.</i> National Institute of Standards and Technology, 2008.",
        "6. <b>Common Vulnerability Scoring System (CVSS).</b> <i>CVSS v3.1 Specification Document.</i> FIRST.Org, Inc., 2019.",
        "7. <b>B. Sullivan and V. Liu.</b> <i>Web Application Security, A Beginner’s Guide.</i> McGraw-Hill Education, 2012.",
        "8. <b>D. Stuttard and M. Pinto.</b> <i>The Web Application Hacker’s Handbook: Finding and Exploiting Security Flaws.</i> John Wiley &amp; Sons, 2011."
    ]
    for r in refs:
        story.append(Paragraph(r, body_justify))
        story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=VITNumberedCanvas)
    print("SUCCESS: VulnLab_VIT_Project_Report.pdf generated successfully!")

if __name__ == '__main__':
    build_vit_report_pdf()
