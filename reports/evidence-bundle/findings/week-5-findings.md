# Week 5 Findings: CVE Mapping & Remediation
**Date:** 2025-11-21  
**Analyst:** Izabel Valdez  

---

## Executive Summary
A full vulnerability assessment of the Nextcloud 29-apache stack identified:  
- **187 unique vulnerabilities** across all containers  
- **12 Critical**, **38 High**, **52 Medium**, **56 Low** (Nextcloud container alone)  
- Highest-risk issues include OpenSSL, zlib, xz-utils backdoor, glibc, and PHP memory corruption bugs.  

**Overall Risk Rating:** HIGH  
Immediate patching is required for critical CVEs affecting core system libraries.

---

## Methodology
Tools used:
- Trivy (container image scanning)
- Manual CVE review
- NVD research
- Dependency-Check (failed due to API rate limiting, documented in findings)

Scope:
- nextcloud:29-apache  
- mariadb:11  
- nginx:alpine  

---

## Top Critical Findings
### Most Dangerous CVEs
1. **CVE-2024-3094 (xz-utils backdoor)** – FULL remote compromise.
2. **CVE-2023-3446 (OpenSSL)** – possible key recovery.
3. **CVE-2022-37454 (zlib)** – buffer overflow in compression library.
4. **CVE-2023-4911 (glibc)** – privilege escalation to root.
5. **CVE-2024-2756 (PHP)** – heap overflow → potential RCE.

---

## Risk Analysis
### Exploitability
- Most Critical CVEs require **no authentication**, **network-based vectors**.
- Many affect core libraries used by *all* containers.

### Impact
Worst-case exploitation could lead to:
- Full compromise of all Nextcloud files
- Database takeover
- Container escape → host machine access
- Account hijacking
- Persistent access via tampered libraries

---

## Remediation Summary
### Priority 1 (Immediate)
- Patch xz-utils, OpenSSL, zlib, PHP runtime  
- Update Nextcloud image to latest secure version

### Priority 2 (This Week)
- Upgrade MariaDB image
- Patch expat, curl, and other related libraries

### Priority 3 (Maintenance Window)
- Update OpenSSH moduli  
- Update minor libraries with minimal impact

### Priority 4 (Monitor)
- Low-severity Debian package issues

---

## Temporary Mitigations Summary
When patching isn't possible immediately:
- Restrict SSH + port access
- Enforce TLS 1.3 only
- Add WAF rules to block PHP uploads
- Reduce upload size
- Disable unused proxy modules
- Increased audit logging

---

## Appendices
- Full CVE list from Trivy scans  
- Raw Trivy outputs  
- Composer audit unavailable (composer missing in container)  
