# Task 12: Remediation Priority Matrix

## Priority 1 – Fix Immediately (Within 24–48 Hours)
| CVE ID | Component | CVSS | Remediation | Effort |
|--------|-----------|------|-------------|--------|
| CVE-2024-3094 | xz-utils | 10.0 | Patch xz-utils packages, rebuild image | 2 hrs |
| CVE-2023-3446 | OpenSSL | 9.8 | Upgrade OpenSSL to secured version | 1 hr |
| CVE-2022-37454 | zlib | 9.8 | Update zlib from Debian security repo | 1 hr |

---

## Priority 2 – Fix This Week
| CVE ID | Component | CVSS | Remediation | Effort |
|--------|-----------|------|-------------|--------|
| CVE-2023-42795 | MariaDB | 7.5 | Update mariadb:11 image | 1 hr |
| CVE-2023-5156 | MariaDB | 8.0 | Apply upstream patches | 1 hr |
| CVE-2022-40674 | expat | 8.1 | Update expat libraries | 30m |

---

## Priority 3 – Fix During Scheduled Maintenance
| CVE ID | Component | CVSS | Remediation |
|--------|-----------|------|-------------|
| CVE-2023-40217 | OpenSSH | 7.5 | Regenerate moduli + update server |

---

## Priority 4 – Monitor Only
| CVE ID | Component | CVSS | Reason |
|--------|-----------|------|--------|
| (Low CVEs) | various | <4.0 | No exploit, low risk |
