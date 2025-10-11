Here’s the updated `README.md` with Kali Linux as the testing box.

# Team 7 — Nextcloud Security Lab

## Goal

Deploy a local Nextcloud, attack it in a safe lab from Kali Linux, document real issues, score risk, and propose fixes.

## Scope

In-scope: auth, sessions, permissions, file handling, sharing links, WebDAV/API.
Out-of-scope: DoS, social engineering, anything outside the lab.

## Architecture

* Docker: Nextcloud (app) + MariaDB (db) on the host.
* Kali Linux as the testing workstation (Burp/ZAP, Nmap, wfuzz, gobuster, curl).
* Local only. No real data.

## Prerequisites

* Docker Desktop
* Git
* OS for hosting Nextcloud: Windows, macOS, or Linux
* Testing OS: Kali Linux (VM or bare metal)

## Target URL

* If browsing from the host: `http://localhost:8080`
* If browsing from Kali in a VM: `http://<host-LAN-IP>:8080`
  Find host IP on Windows: `ipconfig` → use the IPv4 address.

## Quick start (host)

```bash
# from repo root
cd infra/docker
cp .env.example .env
docker compose --env-file .env up -d
# then from host use http://localhost:8080
# from Kali VM use http://<host-LAN-IP>:8080
```

### .env.example

```env
MYSQL_ROOT_PASSWORD=changeme-root
MYSQL_PASSWORD=changeme-app
MYSQL_DATABASE=nextcloud
MYSQL_USER=nextcloud
NEXTCLOUD_ADMIN_USER=admin
NEXTCLOUD_ADMIN_PASSWORD=changeme-admin
```

### Useful app commands (run on host)

```bash
docker compose exec app php occ user:add --password-from-env alice
OC_PASS='AlicePass123!' docker compose exec app php occ user:add --password-from-env alice
OC_PASS='BobPass123!'   docker compose exec app php occ user:add --password-from-env bob
docker compose exec app php occ files:scan --all
```

## Kali quick tools

```bash
# discovery
nmap -sV -p- -T4 <host-LAN-IP> -oN scans/nmap-local.txt

# baseline crawl with ZAP (from Kali)
docker run --rm -t owasp/zap2docker-stable zap-baseline.py \
  -t http://<host-LAN-IP>:8080 -r dynamic-testing/zap-baseline.html
```

Use Burp or ZAP as intercepting proxy in Kali. Save exports to `dynamic-testing/`.

## Repository layout

```
docs/                # notes, checklists
threat-model/        # DFDs, STRIDE, assets
infra/docker/        # docker-compose.yml, .env(.example)
static-analysis/     # Semgrep, Trivy outputs
dynamic-testing/     # ZAP/Burp sessions, exports
scans/               # nmap logs
evidence/            # screenshots, pcaps, raw proof
reports/             # REPORT.md and appendices
.github/workflows/   # CI
scripts/             # helpers
```

## Evidence rules

* Save everything. Name `YYYYMMDD-HHMM_area_step_expected-actual.ext`.
* Include steps, tool version, and config.
* Screenshots must show URL, time, and result.

## Finding template

```
Title
Impact: who is affected and how
CVSS: <score> <vector>
Steps to reproduce: 1..N
Evidence: files/links in repo
Fix: config or code guidance
```

---

## Weekly plan (6 weeks)

### Week 1 — Environment

* Stand up Docker stack on host.
* Create admin + test users (alice, bob).
* Seed sample files and shares.
* Commit infra and `.env.example`.
  **Deliverables**
* Nextcloud at `localhost:8080` (host) and reachable at `http://<host-LAN-IP>:8080` from Kali
* Setup notes in `docs/`

### Week 2 — Threat model

* Context + DFD (users, Kali, app, db, boundaries).
* Assets and trust boundaries.
* STRIDE per component. Pick top 10 risks.
  **Deliverables**
* `threat-model/diagram.(drawio|png)`
* `threat-model/STRIDE.md`

### Week 3 — Auth and access control tests

* Password policy, lockout, sessions, CSRF.
* IDOR on users and shares.
  **Deliverables**
* `dynamic-testing/` exports
* 2–3 preliminary findings

### Week 4 — Files, sharing, WebDAV/API

* Upload handling: content-type confusion, SVG/HTML, traversal.
* Public links: revoke tests, token reuse, expiry.
* WebDAV verbs, etags, caching.
  **Deliverables**
* More findings + proof
* `scans/` and `evidence/` updated

### Week 5 — Scans and scoring

* Semgrep (PHP rules if applicable).
* Trivy for images/Dockerfile.
* Nmap baseline.
* CVSS for all findings. Draft fixes.
  **Deliverables**
* `static-analysis/` and `scans/` outputs
* Findings complete with CVSS

### Week 6 — Report and cleanup

* Finalize `reports/REPORT.md`.
* Reproduce on fresh lab.
* Trim out-of-scope. Tag release.
  **Deliverables**
* Final report with exec summary, methods, findings, fixes, appendix
* Evidence bundle consistent and reproducible

---

## Safety and ethics

Test only inside this lab. No real users. No production targets. No DoS.
