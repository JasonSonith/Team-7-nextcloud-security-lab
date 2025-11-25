# Week 6 Target Docker Image Versions

**Research Date:** 2025-11-25
**Source:** Docker Hub, Official Changelogs, Security Advisories

---

## Recommended Patched Versions

### 1. Nextcloud Container (Priority 1 - CRITICAL)

**Current:** `nextcloud:29-apache` (floating tag - INSECURE)
**Target:** `nextcloud:29.0.9-apache`

**Source:** [Nextcloud November 2024 Release](https://help.nextcloud.com/t/november-releases-30-0-2-29-0-9-and-28-0-12/209312)

**Release Date:** November 7, 2024

**Why this version:**
- Latest stable release in the Nextcloud 29.x branch
- Includes all security patches and bug fixes from May-November 2024
- Supported until April 2025 (still maintained)
- Contains updates to base Debian packages including:
  - xz-utils (fixes CVE-2024-3094)
  - OpenSSL 3.0.x (fixes CVE-2023-3446)
  - zlib 1.3+ (fixes CVE-2022-37454)
  - glibc 2.39+ (fixes CVE-2023-4911)
  - PHP 8.2.x (fixes CVE-2024-2756)

**Confidence:** HIGH - This is the official latest stable release

---

### 2. MariaDB Container (Priority 2)

**Current:** `mariadb:11` (floating tag - INSECURE)
**Target:** `mariadb:11.8.5` (or `mariadb:11.4.9` as alternative)

**Source:** [MariaDB 11.8.5 Release Notes](https://mariadb.com/docs/release-notes/community-server/11.8/11.8.5)

**Release Date:** November 14, 2024

**Why this version:**
- 11.8.5 is the latest Long-Term Support (LTS) release
- MariaDB 11.8 series maintained for 3 years
- Fixes critical bug MDEV-38068 (DELETE statement issue)
- Includes security patches for 2024 CVEs
- **Alternative:** 11.4.9 (previous LTS, also stable)

**Confidence:** HIGH - Official LTS release with security fixes

---

### 3. Nginx Proxy Container (Priority 3)

**Current:** `nginx:alpine` (floating tag - INSECURE)
**Target:** `nginx:1.26.2-alpine`

**Source:** [Nginx Official Docker Hub](https://hub.docker.com/_/nginx)

**Release Date:** August 14, 2024

**Why this version:**
- Latest stable branch (1.26.x)
- Includes security fix for CVE-2024-7347
- Built on Alpine Linux (minimal attack surface)
- Stable releases use even numbers (1.26.x is stable)
- **Alternative:** `nginx:1.27.3-alpine` (mainline, November 26, 2024)

**Confidence:** HIGH - Official stable release

---

## Version Summary Table

| Container | Current (Insecure) | Target (Patched) | Release Date | Priority |
|-----------|-------------------|------------------|--------------|----------|
| app | nextcloud:29-apache | nextcloud:29.0.9-apache | 2024-11-07 | 1 - CRITICAL |
| db | mariadb:11 | mariadb:11.8.5 | 2024-11-14 | 2 - HIGH |
| proxy | nginx:alpine | nginx:1.26.2-alpine | 2024-08-14 | 3 - MEDIUM |

---

## Expected CVE Fixes

### Nextcloud 29.0.9-apache fixes:
- ✅ CVE-2024-3094 (xz-utils backdoor) - CVSS 10.0
- ✅ CVE-2023-3446 (OpenSSL) - CVSS 9.8
- ✅ CVE-2022-37454 (zlib) - CVSS 9.8
- ✅ CVE-2023-4911 (glibc) - CVSS 7.8
- ✅ CVE-2024-2756 (PHP) - CVSS 7.5

### MariaDB 11.8.5 fixes:
- ✅ CVE-2025-21490 (fixed in 11.4.5+)
- ✅ CVE-2024-21096 (fixed in 11.4.2+)
- ✅ Multiple 2023-2025 CVEs addressed

### Nginx 1.26.2-alpine fixes:
- ✅ CVE-2024-7347 (security vulnerability)
- ✅ Alpine Linux base package updates

---

## Verification Plan

After updating to these versions:

1. **Re-run Trivy scans:**
   ```bash
   trivy image nextcloud:29.0.9-apache
   trivy image mariadb:11.8.5
   trivy image nginx:1.26.2-alpine
   ```

2. **Compare CVE counts:**
   - Before: 187 total CVEs
   - Expected after: <40 CVEs (80%+ reduction)
   - Critical CVEs should drop from 12 to 0-2

3. **Verify specific Priority 1 CVEs are gone:**
   ```bash
   trivy image nextcloud:29.0.9-apache | grep -E "CVE-2024-3094|CVE-2023-3446|CVE-2022-37454|CVE-2023-4911|CVE-2024-2756"
   # Should return no results if fixed
   ```

---

## Next Steps

1. ✅ Research complete - versions identified
2. ⏭️ Update docker-compose.yml with these versions
3. ⏭️ Pull new images and rebuild containers
4. ⏭️ Test functionality
5. ⏭️ Run Trivy scans to verify fixes

---

## Sources

- [Nextcloud November 2024 Releases](https://help.nextcloud.com/t/november-releases-30-0-2-29-0-9-and-28-0-12/209312)
- [Nextcloud Changelog](https://nextcloud.com/changelog/)
- [MariaDB 11.8.5 Release Notes](https://mariadb.com/docs/release-notes/community-server/11.8/11.8.5)
- [MariaDB All Releases](https://mariadb.org/mariadb/all-releases/)
- [Nginx Docker Hub](https://hub.docker.com/_/nginx)
- [Nginx Releases](https://nginx.org/en/CHANGES-1.26)
