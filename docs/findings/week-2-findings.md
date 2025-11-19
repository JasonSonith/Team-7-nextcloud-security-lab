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

## Credential Storage Locations

### Finding: Plaintext Secrets in .env File

**Location:** `infra/docker/.env`

**Credentials stored:**
1. **Database credentials**
   - `MYSQL_ROOT_PASSWORD` — MariaDB root password
   - `MYSQL_PASSWORD` — Nextcloud app database password
   - `MYSQL_USER` — Database username (nextcloud)
   - `MYSQL_DATABASE` — Database name

2. **Nextcloud admin credentials**
   - `NEXTCLOUD_ADMIN_USER` — Admin username
   - `NEXTCLOUD_ADMIN_PASSWORD` — Admin password

**Risk Assessment:**
- **Severity:** HIGH
- **CVSS 3.1:** 7.5 (AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N)
- **STRIDE Categories:** Information Disclosure (I), Elevation of Privilege (E)

**Security Implications:**
- All secrets stored in plaintext without encryption
- File accessible to anyone with filesystem access to host
- Compromised `.env` exposes full database and admin access
- Docker compose passes secrets as environment variables (visible in `docker inspect`)
- No secret rotation mechanism documented
- Default passwords from `.env.example` may still be in use

**Evidence:** `infra/docker/.env` (gitignored, not committed)

### Finding: TLS Private Key on Filesystem

**Location:** `infra/docker/nginx/certs/lab.key`

**Risk Assessment:**
- **Severity:** HIGH
- **CVSS 3.1:** 7.4 (AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N)
- **STRIDE Categories:** Spoofing (S), Information Disclosure (I)

**Security Implications:**
- Private key stored in plaintext on host filesystem
- No HSM or secure enclave protection
- Accessible to anyone with volume mount access
- No key rotation procedure documented
- Self-signed certificate with 30-day validity
- Key compromise enables MITM attacks and session decryption

**Evidence:**
- `infra/docker/nginx/certs/lab.key` (gitignored)
- `infra/docker/nginx/certs/lab.crt` (committed to repo)

### Finding: Environment Variable Secret Exposure

**Vector:** Docker container environment variables

**Risk Assessment:**
- **Severity:** MEDIUM
- **CVSS 3.1:** 6.5 (AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N)
- **STRIDE Categories:** Information Disclosure (I)

**Security Implications:**
- All `.env` secrets passed to containers as environment variables
- Visible via `docker inspect <container>`
- Visible via `/proc/<pid>/environ` inside containers
- Logged in container orchestration systems
- Not suitable for production secret management

**Commands to expose secrets:**
```bash
docker compose -f infra/docker/docker-compose.yml exec db env | grep PASSWORD
docker compose -f infra/docker/docker-compose.yml exec app env | grep PASSWORD
docker inspect nextcloud-db | grep -i password
```

## Required actions
- Rotate DB app password (`MARIADB_PASSWORD` and Nextcloud `dbpassword`) and restart.
- Keep `.env` and raw secrets out of Git; commit only redacted evidence.
- Document key management recommendations (Week 2 deliverable).
