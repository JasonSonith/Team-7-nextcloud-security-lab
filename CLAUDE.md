# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Nextcloud security lab for Team 7. The goal is to deploy a local Nextcloud instance, perform security testing from Kali Linux, document vulnerabilities, assess risk using CVSS scoring, and propose fixes. This is a 6-week academic security assessment project.

**Target:** Nextcloud 29 (Apache variant) running in Docker
**Attack Platform:** Kali Linux VM with Burp/ZAP
**Host IP:** 10.0.0.47
**Methodology:** STRIDE threat modeling, vulnerability scanning, dynamic testing, CVE mapping

## Architecture

### Docker Stack (`infra/docker/docker-compose.yml`)

Three-service compose stack:
- **db** — MariaDB 11 with credentials from `.env`
- **app** — Nextcloud 29-apache on internal port 80, exposed on host:8080
- **proxy** — nginx:alpine terminating TLS on port 443, proxying to app:80

Key directories:
- `infra/docker/nginx/conf.d/` — nginx reverse proxy config
- `infra/docker/nginx/certs/` — TLS assets (lab.key in .gitignore, lab.crt committed)
- `infra/docker/.env` — secrets (gitignored); `.env.example` is the template

### Trust Boundaries (from DFD)

- **VM boundary:** Kali attacker tools
- **Host OS boundary:** Docker daemon, volumes, nginx proxy
- **Docker Network boundary:** app and db containers
- **app↔db split:** Internal database queries over Docker bridge

Critical data flows:
1. Login credentials → app
2. Session cookies, CSRF tokens ↔ browsers
3. File uploads → app → host volumes
4. App ↔ MariaDB queries
5. Nginx TLS termination → app

## Common Commands

### Docker Operations

**For detailed Docker startup and troubleshooting guide, see:** `infra/docker/START-UP.md`

```bash
# Start all services
docker compose -f infra/docker/docker-compose.yml up -d

# View running services
docker compose -f infra/docker/docker-compose.yml ps

# View logs
docker compose -f infra/docker/docker-compose.yml logs -f [proxy|app|db]

# Stop and remove
docker compose -f infra/docker/docker-compose.yml down

# Reload nginx after cert rotation
docker compose -f infra/docker/docker-compose.yml exec proxy nginx -s reload

# Test nginx config
docker compose -f infra/docker/docker-compose.yml exec proxy nginx -t
```

### Security Scanning

```bash
# Nmap port scan (from Kali or host)
nmap -Pn -p 80,443,8080 -sS -T4 10.0.0.47 -oX scans/nmap-<timestamp>.xml

# TLS cipher enumeration
nmap --script ssl-enum-ciphers -p 443 10.0.0.47 -oN scans/nmap-ssl-enum.txt

# Trivy container image scan
trivy image nextcloud:29-apache

# Parse nmap output to CSV + heatmap
./scripts/nmap-parser.py -i scans/nmap-80-8080.xml
# Outputs: scans/nmap-parsed.csv, scans/nmap-heatmap.png

# ZAP baseline scan (from Kali)
docker run --rm owasp/zap2docker-stable zap-baseline.py -t http://10.0.0.47:8080 -r report.html

# Verify HTTPS setup
curl -vkI https://10.0.0.47
openssl s_client -connect 10.0.0.47:443 -servername 10.0.0.47 </dev/null
```

### TLS Certificate Generation

```powershell
# Self-signed cert for lab use (30-day validity)
docker run --rm -v ${PWD}/infra/docker/nginx/certs:/certs alpine sh -lc \
  "apk add --no-cache openssl >/dev/null && \
   openssl req -x509 -newkey rsa:2048 -nodes -days 30 \
   -subj '/CN=10.0.0.47' \
   -keyout /certs/lab.key -out /certs/lab.crt && \
   chmod 600 /certs/lab.key && chmod 644 /certs/lab.crt"
```

## Directory Structure

```
scans/                  # Raw scan outputs (nmap, trivy, etc.)
scripts/                # Automation tools (nmap-parser.py, future tools)
docs/
  ├── evidence/         # Timestamped test artifacts by week
  ├── findings/         # Weekly findings markdown files
  ├── runbooks/         # Procedural guides
  └── week-notes/       # Weekly progress notes
threat-model/
  ├── Data-flow-diagram.png
  ├── STRIDE.md         # STRIDE analysis per component
  └── README.md
infra/docker/
  ├── docker-compose.yml
  ├── .env              # Secrets (gitignored)
  ├── .env.example      # Template
  └── nginx/
      ├── conf.d/       # nginx configs
      └── certs/        # TLS cert/key (lab.key gitignored)
reports/                # Final deliverables
```

## File Naming Convention

Evidence and scan files follow: `YYYYMMDD-HHMM_<area>_<step>.<ext>`

Examples:
- `20251018-1445_stride-browser_xss-probe.html`
- `20251019-0930_nmap_ssl-enum.txt`

## STRIDE Testing Framework

The threat model (threat-model/STRIDE.md) defines test procedures for each component across STRIDE categories:

- **Browser (User/Admin):** Weak passwords, session token security, XSS, CSRF, audit logging
- **Kali Proxy:** TLS validation, MITM testing, request tampering, credential exposure
- **App (Nextcloud):** Auth bypass, file upload attacks, directory traversal, XXE, SSRF
- **DB (MariaDB):** SQL injection, credential exposure, backup security
- **Docker Network:** Trust boundary violations, container escape, secret leakage

Each test requires:
1. Tool name and version
2. Configuration or command used
3. Raw output saved to `scans/` or `docs/evidence/week-N/`
4. Finding documented in `docs/findings/week-N-findings.md`

## 6-Week Project Timeline

- **Week 0:** Environment setup, baseline scans
- **Week 1:** Lab deployment, initial nmap/nikto/trivy scans
- **Week 2:** Threat model (DFD + STRIDE), TLS and key storage review
- **Week 3:** Auth/session testing, app audit, Burp/ZAP dynamic tests
- **Week 4:** File handling fuzzing, container hardening, CIS Docker Benchmark
- **Week 5:** CVE mapping, CVSS scoring, remediation proposals
- **Week 6:** Hardening rebuild, final report and evidence bundle

## Current Project Progress

**Last Updated:** 2025-11-09

### Completed Work

**Week 0-1: ✅ COMPLETE**
- Environment setup and baseline scans completed
- Docker stack deployed (Nextcloud 29-apache, MariaDB 11, nginx proxy)
- Initial nmap, trivy scans performed
- Test accounts created

**Week 2: ⚠️ MOSTLY COMPLETE**
- Threat model created (DFD + STRIDE analysis in threat-model/)
- TLS configuration implemented (nginx reverse proxy on port 443)
- Self-signed certificates generated for 10.0.0.47
- Docker startup documentation created (infra/docker/STARTUP.md)
- **PENDING:** Key management recommendations document

**Week 3: 🔄 IN PROGRESS**

Completed Tests:
1. ✅ **Password Strength Testing** (PASS)
   - Nextcloud enforces 10-character minimum password policy
   - Common password database checking (blocks top 100,000 weak passwords)
   - Evidence: `docs/evidence/week3/password-testing/`
   - Findings documented in `docs/findings/week-3-findings.md`

2. ✅ **Brute-Force Protection Testing** (PASS)
   - Rate limiting triggered after ~9 failed login attempts
   - HTTP 429 "Too Many Requests" response implemented
   - Temporary IP-based rate limiting (not permanent account lockout)
   - Tool used: Burp Suite Intruder
   - Evidence: `docs/evidence/week3/brute-force-test/`
   - Findings documented in `docs/findings/week-3-findings.md`

3. ✅ **Session Cookie Security Flags Testing** (PASS)
   - Delegated/completed testing of HttpOnly, Secure, SameSite attributes
   - document.cookie access testing completed

4. ✅ **CSRF Token Validation Testing** (PASS)
   - CSRF tokens required for all state-changing requests
   - Tokens validated for integrity (HTTP 412 when missing/modified)
   - Time-based tokens (reusable within session window)
   - Token location: `requesttoken` HTTP header
   - Tool used: Burp Suite Proxy and Repeater
   - Evidence: `docs/evidence/week3/csrf-testing/`
   - Findings documented in `docs/findings/week-3-findings.md`

Pending Tests:
- XSS vulnerability testing (filenames, share notes, profile fields)
- Nextcloud apps audit
- OWASP ZAP baseline scan

**Week 4-6:** Not yet started

### Test Account Credentials

For Week 3 testing:
- **Test account:** testbruteforce
- **Credentials documented in:** `docs/evidence/week3/brute-force-test/TestBruteForce-creds.txt`
- **Purpose:** Brute-force and authentication testing

### Key Findings So Far

**Security Strengths Identified:**
- Strong password policy (10-char minimum + common password blocking)
- Effective brute-force protection via rate limiting
- Robust CSRF token validation (required, integrity-checked, time-based)
- Session cookie security flags properly implemented

**No Critical Vulnerabilities Found:** All four completed tests resulted in PASS ratings

### Evidence Organization

Week 3 evidence is organized in subdirectories:
- `docs/evidence/week3/password-testing/` - Password strength test screenshots
- `docs/evidence/week3/brute-force-test/` - Burp Intruder attack results and screenshots
- `docs/evidence/week3/csrf-testing/` - CSRF token validation tests (5 screenshots)

### Tools Used in Week 3

- **Burp Suite Community Edition** - Intruder module for brute-force testing, Repeater for CSRF testing
- **Portswigger Chromium Browser** - Pre-configured browser with Burp proxy
- **Nextcloud Web UI** - Password strength testing via user creation interface

### Attack Platform Architecture

**Current Setup (Correct):**
- **Target Environment:** Nextcloud stack running in Docker containers (nginx proxy, Nextcloud app, MariaDB)
  - Port 443: nginx TLS proxy → Nextcloud
  - Port 8080: Direct HTTP access to Nextcloud
  - Isolated with Docker bridge networking
  - Ephemeral/resettable for destructive testing

- **Attacker Platform:** Kali Linux WSL (separate WSL2 instance)
  - Persistent environment for tools and scan history
  - Full GUI support (Burp Suite, ZAP, browser testing)
  - Network access to Docker containers at 10.0.0.47
  - NOT running in Docker (correct for security testing workflow)

**Why this architecture:**
- Simulates real attack scenario (external attacker → target network)
- Crosses trust boundaries properly (WSL → Docker network)
- Maintains tool persistence without complex volume mounts
- Supports GUI security tools (Burp, ZAP, browser proxying)
- Target can be reset without losing attacker's scan history

**Reference:** See `/infra/docker/STARTUP.md` for Docker operations

### Next Steps

1. Complete remaining Week 3 tests (XSS, app audit, ZAP scan)
2. Finalize Week 2 key management recommendations
3. Begin Week 4: File handling and container hardening

## Security Considerations

### Secrets Management

- **Never commit:** `infra/docker/.env`, `infra/docker/nginx/certs/lab.key`, raw proxy logs with credentials
- **Template:** `.env.example` shows required variables
- **Redaction:** Export Burp/ZAP history to `dynamic-testing/` with credentials redacted before commit

### Known Vulnerabilities to Test

From STRIDE.md and project scope:
- Weak password acceptance
- Missing cookie flags (HttpOnly, Secure, SameSite)
- CSRF token reuse
- XSS in filenames and share notes
- File upload MIME bypass
- SQL injection in search/share endpoints
- Container running as root
- Exposed Docker socket
- Outdated base images with CVEs

### Out of Scope

- Denial of Service attacks
- Physical access attacks
- Supply chain compromise
- Production deployment (this is a lab environment)

## Tools and Scripts

### `scripts/nmap-parser.py`

Parses Nmap XML or text output into CSV + heatmap.

**Dependencies:** Python 3, optional matplotlib/numpy for heatmap

**Usage:**
```bash
./scripts/nmap-parser.py -i scans/nmap-80-8080.xml
```

**Outputs:**
- `scans/nmap-parsed.csv` — host, ip, proto, port, state, service, product, version
- `scans/nmap-heatmap.png` — visual grid of open ports

### Planned Future Scripts

From scripts/README.md:
- `semgrep_runner.py` — Semgrep SAST with SARIF output
- `trivy_summary.py` — Trivy CVE summary from JSON
- `zap_drive.py` — Automated ZAP spider + active scan
- `session_flags_check.py` — Cookie security validation
- `csrf_probe.py` — CSRF protection detection
- `upload_matrix.py` — Systematic file upload testing

## Production Deployment Notes

**DO NOT use this docker-compose setup in production.**

Minimum production requirements (from README.md):
- Kubernetes or hardened VMs with network segmentation
- Isolated database host with firewall rules
- Valid TLS certificates (Let's Encrypt or commercial CA)
- External S3 storage with IAM roles
- Key management via Vault or KMS
- Secrets in encrypted store (not .env files)
- WAF, rate limiting, and monitoring (Prometheus/Grafana)
- Weekly vulnerability scans and dependency audits
- SBOM maintenance for all components

## Testing from Kali

Kali VM should have network access to 10.0.0.47 on ports 443 and 8080.

Browser testing:
1. Add Burp/ZAP CA certificate to browser
2. Configure browser proxy to Kali IP
3. Navigate to https://10.0.0.47 (accept self-signed cert warning in lab)
4. Use credentials from `.env`: `NEXTCLOUD_ADMIN_USER` / `NEXTCLOUD_ADMIN_PASSWORD`

Dynamic testing workflow:
1. Crawl with ZAP/Burp spider
2. Review session cookies and CSRF tokens
3. Test authentication endpoints (login, password reset)
4. Fuzz file uploads and share creation
5. Test for XSS/SQLi/XXE/SSRF
6. Export history and findings to `docs/evidence/week-N/`

## Evidence Requirements

For each vulnerability finding:
- Tool name and version
- Configuration or command used
- Raw output file saved to `scans/` or `docs/evidence/`
- CVSS score and risk assessment
- Remediation proposal
- Retest results after fix

All evidence files must be reproducible by teammates.