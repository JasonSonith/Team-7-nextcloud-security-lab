# Week 2 — Configuration Audit

Brief: Capture key settings, document secrets handling, and record HTTP cookie exposure on :8080.

## Current ports (Kali scan on 10.0.0.47)
- 80/tcp: filtered
- 443/tcp: filtered
- 8080/tcp: open (Apache/2.4.62 → Nextcloud)
Evidence: `scans/nmap-ports.txt`. :contentReference[oaicite:0]{index=0}

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
- Data directory: `/var/www/html/data` (default).
- Trusted domains: `["localhost", "10.0.0.47"]` (local only).

Evidence: `docs/evidence/week2/20251018-1342-ls-config-and-data.txt`

### Transport security (HTTP-only on 10.0.0.47:8080)
- HTTP `302` to `/login`.
- Cookies issued over HTTP lack the `Secure` flag; they are `HttpOnly; SameSite=Lax`.
- No HSTS in HTTP response headers.

Evidence:
- `docs/evidence/week2/20251018-1547-http-8080-head.txt`
- `docs/evidence/week2/burp-post-cookies.png` (cookie screenshot)
- `dynamic-testing/20251018-burp-post-login` (intercepted POST)

### Nextcloud encryption
- Status: **Disabled**.

Evidence: `docs/evidence/week2/20251018-encryption-status.txt`, `docs/evidence/week2/20251018-occ-version.txt`

## Evidence policy
- Raw dumps (e.g., `CONFIG-raw.txt`) are **ignored** by Git.
- Redacted evidence (`CONFIG-redacted.txt`) is committed.
- DB env snapshot (`20251018-db-env.txt`) and config grep (`20251018-grep-config-secrets.txt`) are committed.

## Required actions
1. **Rotate DB app password**
   - Choose a strong value.
   - Update both:
     - Container env (`MARIADB_PASSWORD` / `.env`)
     - Nextcloud `config.php` → `dbpassword`
   - Restart stack and re-test login.

2. **Keep secrets out of Git**
   - `.env` stays local.
   - Commit only redacted evidence.

3. **Track versions for reproducibility**
   - Save `occ -V` output in `docs/evidence/week2/`.
