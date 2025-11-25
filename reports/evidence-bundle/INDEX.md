# Evidence Bundle Index

**Project:** Team 7 Nextcloud Security Lab
**Date:** November 25, 2025
**Assessment Period:** October - November 2025

---

## Bundle Contents

This evidence bundle contains all artifacts from the 6-week security assessment of the Nextcloud 29 Docker deployment.

---

## Directory Structure

```
evidence-bundle/
├── INDEX.md                    # This file
├── findings/                   # Weekly findings reports
├── evidence/                   # Testing artifacts by week
│   ├── week0/                  # Environment setup
│   ├── week1/                  # Initial reconnaissance
│   ├── week2/                  # Threat modeling & config
│   ├── week3/                  # Auth & session testing
│   ├── week4/                  # File handling & containers
│   ├── week5/                  # CVE mapping
│   └── week6/                  # Hardening & remediation
├── scans/                      # Raw scan outputs
└── configs/                    # Configuration files
```

---

## Evidence by Week

### Week 0: Environment Setup

**Location:** `evidence/week0/`

| File | Description |
|------|-------------|
| host-docker-compose-ps.png | Docker containers running |
| kali-login-page-nextcloud.png | Nextcloud reachable from Kali |
| occ-status.png | Nextcloud version verification |

**Summary:** Lab environment deployed with Nextcloud 29.0.16, accessible on HTTP port 8080.

---

### Week 1: Initial Reconnaissance

**Location:** `evidence/week1/`

| File | Description |
|------|-------------|
| 20251010-setup-dashboard.png | Initial setup completion |
| 20251010-team-share-with-permissions.png | Share permissions configuration |
| 20251010-user-page.png | Test users created |

**Summary:** Test users (admin, alice, bob) created, initial port scan showing only 8080/tcp open.

---

### Week 2: Threat Modeling & Configuration

**Location:** `evidence/week2/`

| File | Description |
|------|-------------|
| CONFIG-redacted.txt | Nextcloud config (secrets redacted) |
| 20251018-grep-config-secrets.txt | Secret locations identified |
| 20251018-db-env.txt | Database environment review |
| 20251018-1547-http-8080-head.txt | HTTP headers analysis |
| burp-post-cookies.png | Cookie inspection |
| 20251018-encryption-status.txt | Encryption status check |

**Summary:** Configuration review identified plaintext secrets in .env and environment variables.

---

### Week 3: Authentication & Session Testing

**Location:** `evidence/week3/`

#### Password Testing (`password-testing/`)
| File | Description |
|------|-------------|
| password-strength-common-password-check.png | Common password rejection |
| password-length-cmmon-password-check.png.png | Length policy enforcement |

#### Brute-Force Testing (`brute-force-test/`)
| File | Description |
|------|-------------|
| brute-force-result.png | Intruder attack results |
| brute-force-error-429.png | Rate limit triggered |
| brute-force-wordlist-payload.png | Attack configuration |
| successful-login-after-brute-force.png | Login still works after rate limit |
| TestBruteForce-creds.txt | Test account credentials |

#### Session Cookie Testing (`session-cookie-testing/`)
| File | Description |
|------|-------------|
| session-cookies.png | Cookie security flags |
| document.cookie.png | JavaScript access test |

#### CSRF Testing (`csrf-testing/`)
| File | Description |
|------|-------------|
| 01-request-token-admin.png | CSRF token identified |
| 02-baseline-request-success.png | Valid token accepted |
| 03-token-removed-rejected.png | Missing token rejected |
| 04-token-modified-rejected.png | Modified token rejected |
| 05-token-reuse-test.png | Token reuse behavior |

#### XSS Testing (`xss-testing/`)
| File | Description |
|------|-------------|
| 01-invalid-value.png | Input validation |
| 02-profile-img-tag-encoded.png | Output encoding test |
| 03-filename-xss-encoded.png | Filename XSS blocked |
| 04-share-label-xss-tests.png | Share label encoding |

#### App Audit (`nextcloud-audit/`)
| File | Description |
|------|-------------|
| 01-enabled-apps.png | Enabled apps list (part 1) |
| 02-enabled-apps.png | Enabled apps list (part 2) |
| 03-disabled-apps.png | Disabled apps list |

#### ZAP Scan (`zap-scan/`)
| File | Description |
|------|-------------|
| zap-baseline-report.html | Full ZAP report |
| zap.yaml | ZAP configuration |

**Summary:** All authentication and session security tests PASSED. Strong protections confirmed.

---

### Week 4: File Handling & Container Security

**Location:** `evidence/week4/`

#### File Upload Testing (`task-1-file-upload-testing/`)
| File | Description |
|------|-------------|
| task1-fake-image-upload.png | Fake image upload test |
| task1-test-php.jpg-upload.png | PHP disguised as JPG |
| task1-test.php-upload.png | Direct PHP upload |

#### File Size Testing (`task-2-file-uploading-size-limits/`)
| File | Description |
|------|-------------|
| task2-100MB-file-upload.png | 100MB upload test |
| task2-1gb-file-upload.png | 1GB upload test |
| task2-admin-quota-setting.png | Quota configuration |
| task2-disk-usage-before-&-after.png | Disk usage comparison |

#### Malicious Content Testing (`task-3-malicious-file-content/`)
| File | Description |
|------|-------------|
| task3-eicar.txt-before-security.png | EICAR before AV |
| task3-eicar.txt-after-security.png | EICAR after AV |
| task3-enable-antivirus.png | AV app enabled |
| task3-test.html-upload.png | HTML upload test |
| task3-test.svg-upload.png | SVG upload test |

#### Path Traversal Testing (`task-4-path-traversal/`)
| File | Description |
|------|-------------|
| Various screenshots | Path traversal blocked |

#### Special Characters (`task-5-special-characters-in-filenames/`)
| File | Description |
|------|-------------|
| Various screenshots | Filename handling tests |

#### WebDAV Security (`task-6-webdav-security/`)
| File | Description |
|------|-------------|
| Various screenshots | WebDAV auth tests |

#### Container Inspection (`task-7-docker-container-inspection/`)
| File | Description |
|------|-------------|
| task7_containerconfig1.png | Container config (part 1) |
| task7_containerconfig2.png | Container config (part 2) |

#### CIS Benchmark (`task-8-cis-docker-benchmark/`, `cis-benchmark/`)
| File | Description |
|------|-------------|
| cis-results.txt | CIS benchmark output |
| task8_containerconfig.png | Missing features |

#### Privilege Escalation (`task-9-container-privelege-escalation/`)
| File | Description |
|------|-------------|
| task9_results.png | Escalation test results |

#### Secret Management (`task-10-secret-management/`)
| File | Description |
|------|-------------|
| task10_secretmanagement.png | Secret exposure |
| task10_result.png | Access test |

**Summary:** Multiple file handling vulnerabilities identified. Container security issues documented.

---

### Week 5: CVE Mapping

**Location:** `evidence/week5/`

#### Trivy Scans (`task4-trivy-scans/`, `trivy-scans/`)
| File | Description |
|------|-------------|
| nextcloud-app-trivy.txt | Nextcloud scan (2027 CVEs) |
| mariadb-trivy.txt | MariaDB scan (27 CVEs) |
| nginx-trivy.txt | Nginx scan (0 CVEs) |

#### Composer Audit (`composer-audit/`)
| File | Description |
|------|-------------|
| Various files | PHP dependency analysis |

#### CVE Research (`cve-research/`)
| File | Description |
|------|-------------|
| Various files | CVE documentation |

**Summary:** 2,044+ total CVEs identified across containers. 21 Critical, 335 High severity.

---

### Week 6: Hardening & Remediation

**Location:** `evidence/week6/`

#### Pre-Patch State (`pre-patch/`)
| File | Description |
|------|-------------|
| docker-compose-before.yml | Original configuration |
| image-versions.txt | Pre-patch versions |

#### Post-Patch Scans (`post-patch-scans/`)
| File | Description |
|------|-------------|
| mariadb-after.txt | MariaDB post-patch scan |
| nginx-after.txt | Nginx post-patch scan |
| nginx-after.json | Nginx JSON format |

#### Hardening Evidence (`hardening/`)
| File | Description |
|------|-------------|
| docker-compose-hardened.yml | Hardened configuration |
| hardening-verification.txt | Verification output |
| hardening-summary.md | Hardening documentation |
| before-after-comparison.md | Detailed comparison |
| TASK5-CHECKLIST.md | Completion checklist |

#### Other Files
| File | Description |
|------|-------------|
| post-patch-container-status.txt | Container status |
| post-patch-image-versions.txt | Updated versions |
| post-patch-versions.txt | Version verification |
| remediation-plan.md | Remediation planning |
| target-versions.md | Version research |
| functionality-test-results.md | Test results |

**Summary:** All Priority 1 CVEs remediated. Container hardening applied. CIS benchmarks addressed.

---

## Findings Documents

**Location:** `findings/`

| File | Description |
|------|-------------|
| week-0-findings.md | Environment verification |
| week-1-findings.md | Initial reconnaissance |
| week-2-findings.md | Configuration review |
| week-3-findings.md | Auth & session testing |
| week-4-findings.md | File handling & containers |
| week-5-findings.md | CVE mapping |
| week-6-findings.md | Hardening results |
| week6-before-after-analysis.md | Before/after comparison |

---

## Configuration Files

**Location:** `configs/`

| File | Description |
|------|-------------|
| docker-compose-hardened-final.yml | Production-ready config |
| HARDENING-NOTES.md | Hardening documentation |

---

## Scan Outputs

**Location:** `scans/`

| File | Description |
|------|-------------|
| nmap-local.txt | Port scan results |
| nmap-ports.txt | Detailed port analysis |
| Various Trivy outputs | Container vulnerability scans |

---

## Report Documents

| Document | Location |
|----------|----------|
| Executive Summary | reports/Executive-Summary.md |
| Final Report | reports/Final-Security-Assessment-Report.md |
| Hardened Config | reports/docker-compose-hardened-final.yml |

---

## Evidence Integrity

All evidence files were created during the assessment period and have not been modified since capture. Screenshots include timestamps where visible.

---

## File Counts by Week

| Week | Files | Categories |
|------|-------|------------|
| 0 | 3 | Screenshots |
| 1 | 4 | Screenshots, scans |
| 2 | 8 | Config review, headers |
| 3 | 25+ | Auth, session, XSS, CSRF, ZAP |
| 4 | 20+ | File upload, container inspection |
| 5 | 10+ | Trivy scans, CVE research |
| 6 | 15+ | Hardening, post-patch scans |
| **Total** | **85+** | All categories |

---

## Verification

To verify evidence integrity:

```bash
# List all evidence files
find docs/evidence -type f | wc -l

# Check file timestamps
ls -la docs/evidence/week*/
```

---

**Bundle Compiled By:** Team 7
**Date:** November 25, 2025
