# Week 2 — Findings (Config, HTTP, Keys)

Scope: Local lab at `10.0.0.47`. Documented config, secrets, and HTTP-only risks on `:8080`.

## Ports (Kali scan)
- 80/tcp: filtered
- 443/tcp: filtered
- 8080/tcp: open (Apache → Nextcloud)

Evidence: `scans/nmap-ports.txt`

## Secrets in app config
- `passwordsalt` present in `config.php` → redact in evidence.
- `secret` present in `config.php` → redact in evidence.
- `dbpassword` in `config.php` is lab default (`changeme-app`) → **rotate**.

Evidence: `docs/evidence/week2/CONFIG-redacted.txt`, `docs/evidence/week2/20251018-grep-config-secrets.txt`

## DB container environment
- `MARIADB_ROOT_PASSWORD` set (secret; do not commit).
- `MARIADB_PASSWORD` set (must match Nextcloud `dbpassword`).
- `MARIADB_USER=nextcloud` (expected).

Evidence: `docs/evidence/week2/20251018-db-env.txt`

## Paths and trust
- Data dir: `/var/www/html/data` (default).
- Trusted domains: `["localhost", "10.0.0.47"]` (local only).

Evidence: `docs/evidence/week2/20251018-1342-ls-config-and-data.txt`

## Transport security (HTTP on 10.0.0.47:8080)
- HTTP `302` to `/login`.
- Cookies issued over HTTP lack `Secure`; cookies are `HttpOnly; SameSite=Lax`.
- No HSTS on HTTP.

Evidence:
- `docs/evidence/week2/20251018-1547-http-8080-head.txt`
- `docs/evidence/week2/burp-post-cookies.png` (cookie screenshot)
- `dynamic-testing/20251018-burp-post-login` (intercepted POST)

## Nextcloud encryption
- Status: **Disabled**.

Evidence: `docs/evidence/week2/20251018-encryption-status.txt`, `docs/evidence/week2/20251018-occ-version.txt`

## Required actions
- Rotate DB app password (`MARIADB_PASSWORD` and Nextcloud `dbpassword`) and restart.
- Keep `.env` and raw secrets out of Git; commit only redacted evidence.
