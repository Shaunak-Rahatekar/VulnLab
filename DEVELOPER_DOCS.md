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
