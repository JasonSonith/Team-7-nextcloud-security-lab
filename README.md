Team 7 — Nextcloud Security Lab
Here’s a ready-to-paste `README.md` for your repo.

# Team 7 — Nextcloud Security Lab

## Goal

Deploy a local Nextcloud, attack it inside a safe lab, document real issues, score risk, and propose fixes.

## Scope

In-scope: auth, sessions, permissions, file handling, sharing links, WebDAV/API.
Out-of-scope: DoS, social engineering, anything outside the lab.

## Architecture

* Docker: Nextcloud (app) + MariaDB (db)
* Local host only. No real data.

## Prerequisites

* Docker Desktop
* Git
* OS: Windows, macOS, or Linux

## Quick start

```bash
# from repo root
cd infra/docker
# copy and edit secrets
cp .env.example .env
docker compose --env-file .env up -d
# open http://localhost:8080
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

### Useful app commands

```bash
# run inside container
docker compose exec app php occ user:add --password-from-env alice
# example
OC_PASS='AlicePass123!' docker compose exec app php occ user:add --password-from-env alice
OC_PASS='BobPass123!'   docker compose exec app php occ user:add --password-from-env bob
docker compose exec app php occ files:scan --all
```

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

* Save everything. Name as `YYYYMMDD-HHMM_area_step_expected-actual.ext`.
* Include steps, tool version, and config used.
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

* Stand up Docker stack.
* Create admin + test users (alice, bob).
* Seed sample files and shares.
* Commit infra and `.env.example`.
  **Deliverables**
* Running Nextcloud at `localhost:8080`
* Setup notes in `docs/`

### Week 2 — Threat model

* Draw context + DFD (users, app, db, boundaries).
* List assets and trust boundaries.
* STRIDE per component. Select top 10 risks to test.
  **Deliverables**
* `threat-model/diagram.(drawio|png)`
* `threat-model/STRIDE.md`

### Week 3 — Auth and access control tests

* Password policy, lockout, session handling, CSRF.
* IDOR checks on user and share objects.
* Start evidence capture discipline.
  **Deliverables**
* `dynamic-testing/` exports
* 2–3 preliminary findings drafted

### Week 4 — Files, sharing, WebDAV/API

* Upload handling: content-type confusion, SVG/HTML, path traversal.
* Public links: permission revocation, token reuse, expiry.
* WebDAV: verbs, etags, caching.
  **Deliverables**
* More findings with proof
* `scans/` and `evidence/` updated

### Week 5 — Scans and scoring

* Semgrep (rulesets relevant to PHP/Nextcloud addons if any).
* Trivy filesystem scan for images/Dockerfile.
* Nmap baseline of exposed services.
* Score all findings with CVSS. Draft fixes.
  **Deliverables**
* `static-analysis/` and `scans/` outputs
* Finding cards complete with CVSS

### Week 6 — Report and cleanup

* Finalize `reports/REPORT.md`.
* Cross-check steps reproduce on fresh lab.
* Trim out-of-scope notes. Tag release.
  **Deliverables**
* Final report with exec summary, methods, findings, fixes, appendix
* Evidence bundle consistent and reproducible

---


## Safety and ethics

Test only inside this lab. No real users. No production targets. No DoS.


