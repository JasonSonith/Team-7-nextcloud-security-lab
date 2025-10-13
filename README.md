# Team 7 — Nextcloud Security Lab

## Goal
Deploy a local Nextcloud lab, attack it from Kali, document issues, score risk, and propose fixes.

## What is Nextcloud
Nextcloud is a self-hosted file share and collaboration platform.  
Inputs: HTTP/WebDAV requests, file uploads, user credentials.  
Core components: PHP app, storage backend (local or external), database (MariaDB/Postgres), optional caching (Redis), web server (nginx/Apache).  
Primary features: file sync, sharing links, WebDAV, user/group auth, apps (collaboration, calendar, contacts).

## How Nextcloud Works
1. Client → HTTP(S) → Web server (nginx/Apache).  
2. Web server runs PHP (PHP-FPM) executing Nextcloud PHP code.  
3. PHP queries database for metadata and user records.  
4. Files written to configured storage (local disk, SMB, or S3).  
5. App layer enforces permissions, tokens, links, and API endpoints.

## Encryption and Key Storage
- **Server-Side Encryption (SSE):** Encrypts files on server disk. Keys can be in database or local file. If both reside on same host, compromise equals full access.  
- **End-to-End Encryption (E2EE):** Keys remain client-side, not stored on server. Protects files even if server compromised.  
- **Transport Encryption (TLS):** Protects client-server traffic. TLS private keys stored on host filesystem.  
- **Best Practice:** Use E2EE for sensitive files, external KMS/HSM for server keys, and TLS with valid certificates.

## Docker Overview
Docker packages applications and dependencies into images. Containers share the host kernel but run isolated processes. `docker compose` manages multiple services locally.

### Container Vulnerabilities
- Image package CVEs or outdated dependencies.  
- Containers running as root.  
- Leaked secrets in `.env` or image layers.  
- Overexposed ports or privileged flags.  
- Outdated base images or insecure Docker daemon.

### How to Detect
- **Trivy:** `trivy image nextcloud:latest`  
- **Static inspection:** Review Dockerfile for bad patterns (`USER root`, embedded secrets).  
- **Runtime:** `docker inspect` for mounts and privileges.  
- **Benchmark:** Run CIS Docker Benchmark.  
- **Dependency audit:** `composer audit` or OWASP Dependency-Check.

## Production Deployment
Do not use the simple compose stack in production.

### Minimum Production Setup
- Orchestrate via Kubernetes or hardened VMs.  
- Isolated database host with network controls.  
- Valid TLS via reverse proxy (nginx/Traefik).  
- External S3 for storage with IAM roles.  
- Key management using Vault or KMS.  
- Secrets in encrypted store (K8s secrets).  
- Monitoring, WAF, rate limiting, and backups.  
- Weekly vulnerability and dependency scans.

## Learning Curve
- **Learning:** Low to moderate for users.  
- **Teaching:** Easy for end users, harder for admins.  
- **Maintenance:** Moderate; requires updates, patching, and key rotation.

## Additional Components That Can Be Compromised
- Database (MariaDB/Postgres).  
- Caching layer (Redis).  
- PHP runtime or web server.  
- Docker host or Nextcloud apps.  
- Reverse proxy or TLS endpoint.

### How to Detect Compromise
- Monitor CVE feeds.  
- Use SCA tools on PHP libs.  
- Use network scans (nmap, ZAP, Burp).  
- Verify app integrity via signatures.  
- Maintain SBOM for all components.

## Evidence and Reproducibility
Store tool versions, scan logs, and configurations under `scans/` or `docs/`.

---

# 6-Week Weekly Plan

### Week 0 — Preparation
- Set up Kali and host networking.  
- Copy `.env.example` to `.env`. Secure secrets.  
- Record versions and environment baseline.

### Week 1 — Lab Setup & Baseline Scans
- Deploy Nextcloud with Docker Compose.  
- Create test accounts.  
- Run initial `nmap`, `nikto`, `trivy`, `composer audit`.  
- Save outputs in `scans/`.

### Week 2 — Threat Model & Key Review
- Create DFD and STRIDE diagrams.  
- Inspect config for secrets and key paths.  
- Test TLS and key storage.  
- Deliver key management recommendations.

### Week 3 — Auth & Session Security
- Test password strength, lockout, CSRF, brute-force limits.  
- Audit Nextcloud apps and remove unused ones.  
- Capture Burp/ZAP findings.

### Week 4 — File Handling & Container Hardening
- Fuzz file uploads and WebDAV operations.  
- Check container configs for privilege issues.  
- Run CIS Docker Benchmark.  
- Document vulnerabilities.

### Week 5 — CVE Mapping & Remediation
- Run full SCA and CVE scans.  
- Score findings with CVSS.  
- Propose mitigations and upgrade paths.

### Week 6 — Final Hardening & Report
- Rebuild environment with fixes.  
- Generate hardened compose or K8s manifest.  
- Produce final report and evidence bundle.

---

# Key Commands
```bash
trivy image nextcloud:latest
docker compose ps && docker inspect <container>
grep -n "USER\|ADD\|COPY\|ENV" infra/docker/Dockerfile
docker run --rm owasp/zap2docker-stable zap-baseline.py -t http://localhost:8080 -r report.html
composer audit --no-interaction
