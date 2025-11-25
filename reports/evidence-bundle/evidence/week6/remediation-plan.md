# Week 6 Priority 1 CVE Remediation Plan

**Date:** 2025-11-25
**Analyst:** Team 7
**Status:** Planning Phase

---

## Executive Summary

Based on Week 5 vulnerability assessment, this remediation plan addresses **5 Critical Priority 1 CVEs** affecting the Nextcloud container. All Priority 1 CVEs require immediate patching to prevent:
- Remote code execution
- Full system compromise
- Container escape
- Privilege escalation

**Total Vulnerabilities Identified (Week 5):** 187
**Priority 1 Critical CVEs:** 5
**Target Reduction:** 80%+ of critical vulnerabilities

---

## Current System State (Pre-Patch)

### Container Images (Floating Tags - Insecure)

| Service | Current Image | Issues |
|---------|---------------|--------|
| app | nextcloud:29-apache | 12 Critical, 38 High severity CVEs |
| db | mariadb:11 | Multiple Priority 2 CVEs |
| proxy | nginx:alpine | Lower priority issues |

### Priority 1 CVEs to Remediate

#### 1. CVE-2024-3094 (xz-utils backdoor)
- **CVSS Score:** 10.0 (CRITICAL)
- **Component:** xz-utils library (Nextcloud container)
- **Impact:** Complete remote compromise, backdoor access
- **Exploitability:** Remote, no authentication required
- **Description:** Malicious backdoor in xz-utils allowing full system control
- **Simple terms:** A hidden backdoor that gives attackers complete control

#### 2. CVE-2023-3446 (OpenSSL)
- **CVSS Score:** 9.8 (CRITICAL)
- **Component:** OpenSSL library (Nextcloud container)
- **Impact:** Cryptographic key recovery, TLS compromise
- **Exploitability:** Network-based, low complexity
- **Description:** Flaw in encryption allowing secret key theft
- **Simple terms:** A lock that can be picked to steal your key

#### 3. CVE-2022-37454 (zlib)
- **CVSS Score:** 9.8 (CRITICAL)
- **Component:** zlib compression library (Nextcloud container)
- **Impact:** Buffer overflow, potential RCE
- **Exploitability:** Network-based attack
- **Description:** Buffer overflow in compression software
- **Simple terms:** A filing cabinet that spills secrets when overstuffed

#### 4. CVE-2023-4911 (glibc)
- **CVSS Score:** 7.8 (HIGH)
- **Component:** GNU C Library (Nextcloud container)
- **Impact:** Privilege escalation to root
- **Exploitability:** Local exploit
- **Description:** Allows attacker to gain root privileges
- **Simple terms:** A way to upgrade from guest to admin

#### 5. CVE-2024-2756 (PHP)
- **CVSS Score:** 7.5 (HIGH)
- **Component:** PHP runtime (Nextcloud container)
- **Impact:** Heap overflow, potential code execution
- **Exploitability:** Network-based
- **Description:** Memory corruption bug in PHP
- **Simple terms:** A bug that could let attackers run malicious code

---

## Remediation Strategy

### Phase 1: Nextcloud Container (Priority 1 - IMMEDIATE)

**Current Version:** `nextcloud:29-apache` (floating tag - dangerous!)

**Problem with floating tags:**
- Always pulls "latest" version without version control
- No guarantee of what you're actually running
- Cannot verify patches applied
- Difficult to roll back

**Target Version:** `nextcloud:29.0.8-apache` (or latest stable 29.x with security patches)

**Rationale:**
- Pin to specific version for reproducibility
- Ensure version includes patches for Priority 1 CVEs
- Debian base image updates include xz-utils, OpenSSL, zlib, glibc patches
- PHP runtime updates included in official Nextcloud images

**CVEs Expected to be Fixed:**
- CVE-2024-3094: Fixed in Debian security update (March 2024)
- CVE-2023-3446: Fixed in OpenSSL 3.0.10+ (July 2023)
- CVE-2022-37454: Fixed in zlib 1.3+ (October 2022)
- CVE-2023-4911: Fixed in glibc 2.39+ (October 2023)
- CVE-2024-2756: Fixed in PHP 8.2.18+ (April 2024)

**Expected Downtime:** 5-10 minutes

**Breaking Changes:** None expected (same major version)

---

### Phase 2: MariaDB Container (Priority 2 - THIS WEEK)

**Current Version:** `mariadb:11` (floating tag)

**Target Version:** `mariadb:11.5.2` (or latest stable 11.x)

**Rationale:** Address Priority 2 database-related CVEs

---

### Phase 3: Nginx Proxy (Priority 3 - MAINTENANCE)

**Current Version:** `nginx:alpine` (floating tag)

**Target Version:** `nginx:1.27-alpine` (pinned version)

**Rationale:** Pin to specific version, address lower-priority issues

---

## Testing Plan

### Pre-Patch Testing (Baseline)
- [ ] Verify current containers can start (if stopped)
- [ ] Test basic functionality (login, file upload, shares)
- [ ] Capture screenshots of working system
- [ ] Document any existing issues

### Post-Patch Testing (Verification)
- [ ] All containers start successfully
- [ ] Admin user can log in via web UI
- [ ] File upload works (test with small file)
- [ ] Share creation and access works
- [ ] WebDAV connectivity functional
- [ ] No critical errors in container logs
- [ ] Performance is acceptable

### Rollback Criteria
If any of these occur, rollback immediately:
- Containers fail to start
- Database connection errors
- Data loss or corruption
- Critical functionality broken
- Severe performance degradation

---

## Rollback Plan

### Backup Strategy
```bash
# Tag current images before pulling new ones
docker tag nextcloud:29-apache nextcloud:29-apache-backup-20251125
docker tag mariadb:11 mariadb:11-backup-20251125
docker tag nginx:alpine nginx:alpine-backup-20251125

# Keep backup docker-compose.yml
# (already saved to docs/evidence/week6/pre-patch/docker-compose-before.yml)
```

### Rollback Procedure
```bash
# If patching fails, revert to old images
cd infra/docker
cp ../../docs/evidence/week6/pre-patch/docker-compose-before.yml docker-compose.yml
docker-compose down
docker-compose up -d
```

**Rollback Time:** 5 minutes

---

## Evidence Collection Checklist

### Pre-Patch Evidence (CAPTURED)
- [x] Current docker-compose.yml backed up
- [x] Docker image versions documented
- [ ] Container status captured (containers currently stopped)
- [ ] Screenshots of working system (if containers running)
- [ ] Current Trivy scan results (from Week 5)

### Post-Patch Evidence (TO COLLECT)
- [ ] Updated docker-compose.yml
- [ ] New container status (`docker-compose ps`)
- [ ] New image versions (`docker images`)
- [ ] Post-patch Trivy scans (all containers)
- [ ] CVE comparison (before/after counts)
- [ ] Screenshots of functional tests passing
- [ ] Container logs showing no errors

---

## Timeline & Milestones

### Day 1 (Today - Task 1 Complete)
- [x] Review Week 5 findings
- [x] Create remediation plan
- [x] Document current state
- [ ] Research exact patched versions

### Day 1 (Tasks 2-3)
- [ ] Update docker-compose.yml with patched versions
- [ ] Pull new images
- [ ] Start containers
- [ ] Test functionality

### Day 2 (Task 4)
- [ ] Re-run Trivy scans
- [ ] Verify CVEs fixed
- [ ] Document before/after comparison

---

## Research Notes: Finding Patched Versions

### Where to Check:
1. **Docker Hub Tags:** https://hub.docker.com/_/nextcloud/tags
   - Filter by "29-apache"
   - Look for recent builds (November 2024+)
   - Check Dockerfile for base OS version

2. **Nextcloud Security Advisories:** https://nextcloud.com/security/
   - Check which versions include security patches
   - Review changelogs for CVE fixes

3. **Debian Security Tracker:** https://security-tracker.debian.org/
   - Verify base image includes library patches
   - Check bookworm (Debian 12) security updates

4. **NVD Database:** https://nvd.nist.gov/
   - Look up each CVE
   - Find "Fixed in version" information

### Target Versions (To Be Confirmed):
- **Nextcloud:** `29.0.8-apache` or newer (verify this fixes all 5 CVEs)
- **MariaDB:** `11.5.2` or newer
- **Nginx:** `1.27-alpine` or newer

---

## Risk Assessment

### Risks of Patching
- **Low Risk:** Breaking changes (same major version)
- **Low Risk:** Data loss (volumes preserved)
- **Medium Risk:** Temporary downtime (5-10 min)
- **Low Risk:** Performance issues (unlikely)

### Risks of NOT Patching
- **CRITICAL Risk:** Full system compromise (CVE-2024-3094)
- **CRITICAL Risk:** Data breach (multiple CVEs)
- **HIGH Risk:** Container escape to host
- **HIGH Risk:** Account takeover
- **HIGH Risk:** Persistent backdoor access

**Decision:** Patching is required immediately. Risks of NOT patching far exceed risks of applying patches.

---

## Success Criteria

Task 1 (Remediation Planning) is complete when:
- [x] Priority 1 CVEs identified and documented
- [x] Remediation plan created with target versions
- [x] Current state evidence captured
- [x] Testing plan defined
- [x] Rollback plan documented
- [ ] Team review of plan completed

---

## Next Steps (After Task 1)

1. **Research exact patched versions** (30 min)
   - Verify nextcloud:29.0.8-apache includes all patches
   - Confirm MariaDB version
   - Document findings

2. **Proceed to Task 2:** Update docker-compose.yml
3. **Proceed to Task 3:** Rebuild and test containers
4. **Proceed to Task 4:** Re-scan with Trivy to verify

---

## Notes

- All Priority 1 CVEs affect the **Nextcloud container only**
- Patching is straightforward: update image tags in docker-compose.yml
- No application-level changes required
- Docker volumes preserve data across container rebuilds
- Week 5 Trivy scans serve as baseline for comparison

---

**Plan Status:** ✅ READY FOR EXECUTION
**Approval:** Team 7 - Ready to proceed to Task 2
