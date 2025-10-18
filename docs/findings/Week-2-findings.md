# Week 2 — Configuration Audit

Brief: Capture key settings, document secrets handling, and record HTTP cookie exposure on :8080.

## Findings

### Secrets in app config
- `passwordsalt` present in `config.php`. Redact in evidence.
- `secret` present in `config.php`. Redact in evidence.
- `dbpassword` in `config.php` is a lab default (`changeme-app`). **Rotate.**

Evidence: `docs/evidence/week2/CONFIG-redacted.txt`, `docs/evidence/week2/20251018-grep-config-secrets.txt`

### DB container environment
- `MARIADB_ROOT_PASSWORD` is set (container env). Treat as secret; never commit.
- `MARIADB_PASSWORD` is set (app user password). Must match the app’s `dbpassword`.
- `MARIADB_USER=nextcloud` (expected for this lab).

Evidence: `docs/evidence/week2/20251018-db-env.txt`

### Paths and trust
- Data directory: `/var/www/html/data` (default). :contentReference[oaicite:0]{index=0}
- Trusted domains: `["localhost", "10.0.0.47"]` (local only).

Evidence: `docs/evidence/week2/20251018-1342-ls-config-and-data.txt`

### Transport security (current HTTP-only on 10.0.0.47:8080)
- Server returns `302` to `/login`.
- `Set-Cookie` values are issued over HTTP without the `Secure` flag; cookies are `HttpOnly; SameSite=Lax`. 
- No HSTS observed on HTTP response headers. 

Evidence:
- `docs/evidence/week2/20251018-1547-http-8080-head.txt` (headers) 
- `docs/evidence/week2/burp-post-cookies.png` (login flow cookies)
- `dynamic-testing/20251018-burp-post-login` (intercepted POST)

### Nextcloud encryption
- Status: **Disabled**.

Evidence: `docs/evidence/week2/2025
