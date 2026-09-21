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
