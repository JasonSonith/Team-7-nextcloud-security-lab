# Week 5 Quick Start Checklist

Use this as a quick reference while working through Week 5. For detailed explanations, see `/home/Jason/Team-7-nextcloud-security-lab/docs/week-notes/WEEK-5-CVE-MAPPING-GUIDE.md`

## Phase 1: Setup

- [ ] Navigate to project directory: `cd /home/Jason/Team-7-nextcloud-security-lab`
- [ ] Start Docker stack: `cd infra/docker && docker-compose up -d`
- [ ] Verify containers running: `docker ps` (should see 3 containers)

## Phase 2: Run Scans

### Trivy Scans
- [ ] Scan Nextcloud container:
  ```bash
  trivy image nextcloud:29-apache --format json --output /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/trivy-scans/nextcloud-app-trivy.json
  trivy image nextcloud:29-apache --format table --output /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/trivy-scans/nextcloud-app-trivy.txt
  ```

- [ ] Scan MariaDB container:
  ```bash
  trivy image mariadb:11 --format json --output /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/trivy-scans/mariadb-trivy.json
  trivy image mariadb:11 --format table --output /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/trivy-scans/mariadb-trivy.txt
  ```

- [ ] Scan nginx container:
  ```bash
  trivy image nginx:alpine --format json --output /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/trivy-scans/nginx-trivy.json
  trivy image nginx:alpine --format table --output /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/trivy-scans/nginx-trivy.txt
  ```

### Composer Audit
- [ ] Run Composer audit:
  ```bash
  docker exec -it nextcloud-app bash
  cd /var/www/html
  composer audit --format=json > /tmp/composer-audit.json
  composer audit --format=table > /tmp/composer-audit.txt
  exit
  docker cp nextcloud-app:/tmp/composer-audit.json /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/composer-audit/
  docker cp nextcloud-app:/tmp/composer-audit.txt /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/composer-audit/
  ```

### OWASP Dependency-Check (Optional)
- [ ] Download and run Dependency-Check (15-30 min first run):
  ```bash
  cd /home/Jason
  wget https://github.com/jeremylong/DependencyCheck/releases/download/v9.0.0/dependency-check-9.0.0-release.zip
  unzip dependency-check-9.0.0-release.zip
  ./dependency-check/bin/dependency-check.sh --scan /home/Jason/Team-7-nextcloud-security-lab/infra/docker --out /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/dependency-check --format ALL --project "Nextcloud-Security-Lab"
  ```

## Phase 3: Analyze Results

- [ ] Review Trivy outputs:
  ```bash
  less /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/trivy-scans/nextcloud-app-trivy.txt
  ```

- [ ] Create CVE summary: `nano /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/cve-research/cve-summary.txt`
  - Count total CVEs
  - Count by severity (CRITICAL/HIGH/MEDIUM/LOW)
  - Note which container has most vulnerabilities

- [ ] Create top CVEs list: `nano /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/cve-research/top-cves.txt`
  - List 10-15 highest severity CVEs
  - Focus on CVSS 9.0+ (CRITICAL)
  - Include HIGH (7.0-8.9) in Nextcloud app

## Phase 4: Research CVEs

For each top CVE:
- [ ] Look up on NVD: https://nvd.nist.gov/vuln/search
- [ ] Document CVSS score and breakdown
- [ ] Write plain-English explanation
- [ ] Note affected component and version
- [ ] Find fixed version (if available)

## Phase 5: Create Remediation Plan

- [ ] Create upgrade matrix (which versions fix which CVEs)
- [ ] Document temporary mitigations for unpatchable CVEs
- [ ] Prioritize vulnerabilities:
  - Priority 1: CRITICAL (9.0-10.0), fix immediately
  - Priority 2: HIGH (7.0-8.9), fix this week
  - Priority 3: MEDIUM (4.0-6.9), schedule maintenance
  - Priority 4: LOW (0.1-3.9), monitor only

## Phase 6: Documentation

- [ ] Create findings document: `nano /home/Jason/Team-7-nextcloud-security-lab/docs/findings/week-5-findings.md`
  - Executive summary
  - Methodology
  - Detailed findings (top 10-15 CVEs)
  - Risk analysis
  - Remediation recommendations
  - Appendices (full CVE list, references)

- [ ] Create evidence README: `nano /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/README.md`

- [ ] Final verification:
  - All scan files present in evidence directory
  - Findings document complete
  - All file paths are absolute
  - Commands documented for reproducibility

## Expected Files at Completion

Evidence:
- `/home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/trivy-scans/nextcloud-app-trivy.json`
- `/home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/trivy-scans/nextcloud-app-trivy.txt`
- `/home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/trivy-scans/mariadb-trivy.json`
- `/home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/trivy-scans/mariadb-trivy.txt`
- `/home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/trivy-scans/nginx-trivy.json`
- `/home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/trivy-scans/nginx-trivy.txt`
- `/home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/composer-audit/composer-audit.json`
- `/home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/composer-audit/composer-audit.txt`
- `/home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/cve-research/cve-summary.txt`
- `/home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/cve-research/top-cves.txt`
- `/home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/README.md`

Findings:
- `/home/Jason/Team-7-nextcloud-security-lab/docs/findings/week-5-findings.md`

## Time Estimates
- Setup: 15 min
- Running scans: 45-60 min
- Analyzing results: 60-90 min
- CVE research: 60-90 min
- Remediation planning: 60-90 min
- Documentation: 30-60 min
- **Total: 6-8 hours**

## Quick CVSS Reference

**Severity Ranges:**
- 9.0-10.0 = CRITICAL (fix immediately)
- 7.0-8.9 = HIGH (fix this week)
- 4.0-6.9 = MEDIUM (schedule maintenance)
- 0.1-3.9 = LOW (monitor)

**Attack Vector:**
- Network (N) = Exploitable from internet
- Adjacent (A) = Exploitable from local network
- Local (L) = Requires local access
- Physical (P) = Requires physical access

**Attack Complexity:**
- Low (L) = Easy to exploit
- High (H) = Hard to exploit, needs special conditions

**Privileges Required:**
- None (N) = No authentication needed
- Low (L) = Basic user account
- High (H) = Admin privileges

**Impact (Confidentiality/Integrity/Availability):**
- High (H) = Complete compromise
- Low (L) = Partial compromise
- None (N) = No impact

## Need Help?

See full guide with examples and troubleshooting:
`/home/Jason/Team-7-nextcloud-security-lab/docs/week-notes/WEEK-5-CVE-MAPPING-GUIDE.md`
