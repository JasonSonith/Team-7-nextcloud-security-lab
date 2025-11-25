# Task 10 – Remediation Matrix (Week 5)

This matrix describes **how we would patch or upgrade** the lab’s Nextcloud stack
to address the top 15 CVEs identified in Task 8–9.

> Note: Exact fixed versions should be confirmed against vendor advisories
> (Debian, Nextcloud, MariaDB, PHP, curl, OpenSSL, etc.). In this lab we assume
> "fixed version" means **the latest stable release in the same major line**.

---

## Remediation Matrix

| CVE ID        | Affected Component                    | Where It Lives (Container)      | Current Lab Version (Approx)      | Target / Fixed Version (Conceptual)                               | Upgrade Type                         | Breaking Changes? (Expected)                         |
|--------------|----------------------------------------|----------------------------------|-----------------------------------|--------------------------------------------------------------------|--------------------------------------|------------------------------------------------------|
| CVE-2024-3094 | xz-utils backdoor                     | Debian base (Nextcloud image)    | Debian 12.11 base image           | Latest Debian 12 image with patched `xz-utils`                     | Rebuild Nextcloud image from newer base | None expected for app; regression-test logins & SSH |
| CVE-2023-3446 | OpenSSL side-channel                  | Debian base (Nextcloud image)    | OpenSSL from Debian 12.11         | OpenSSL patched via `apt upgrade` / newer Nextcloud image         | OS package update / new image       | Low; verify TLS still works with proxy & clients     |
| CVE-2022-37454 | zlib buffer overflow                 | Debian base (Nextcloud image)    | zlib from Debian 12.11            | zlib patched via Debian security updates                          | OS package update / new image       | None expected                                       |
| CVE-2024-22365 | Apache `mod_proxy` RCE               | Apache in `nextcloud:29-apache`  | Apache 2.4.x                      | Apache 2.4.x security patch (latest 2.4.x packaged in base image) | Rebuild from newer Nextcloud image  | Low; test reverse proxy & WebDAV endpoints          |
| CVE-2023-4911 | glibc “Looney Tunables”              | Debian base (Nextcloud & DB)     | glibc from Debian 12.11           | glibc patched via Debian security updates                         | OS package update / new image       | None expected; restart containers                    |
| CVE-2024-2756 | PHP heap buffer overflow              | PHP in Nextcloud app container   | PHP 8.x bundled with Nextcloud    | Nextcloud image with patched PHP 8.x                              | New Nextcloud 29-apache tag         | Medium; confirm Nextcloud still passes integrity check |
| CVE-2024-24808 | PHP-FPM memory corruption            | PHP-FPM in app (if used)         | PHP-FPM 8.x                       | Patched PHP-FPM via new Nextcloud image                           | New Nextcloud 29-apache tag         | Low–Medium; re-test uploads & heavy requests        |
| CVE-2024-0762 | curl SMTP stack buffer overflow       | curl in Debian base              | curl from Debian 12.11            | curl patched via Debian security updates                          | OS package update / new image       | None; test any email/webhook integrations           |
| CVE-2024-1597 | libpq / PostgreSQL SQL injection      | libpq client libs (if present)   | libpq from Debian 12.11           | Patched libpq via Debian security updates                         | OS package update / new image       | None for MariaDB; relevant if Postgres is added     |
| CVE-2023-29491 | Apache HTTP/2 Rapid Reset DoS        | Apache HTTP/2 in `nextcloud`     | Apache 2.4.x with HTTP/2          | Patched Apache 2.4.x (via new image)                              | New Nextcloud 29-apache tag         | Low; re-test HTTP/2 via proxy                       |
| CVE-2023-42795 | MariaDB Denial of Service            | `mariadb:11` container           | MariaDB 11.x                      | Newer `mariadb:11` tag with security fixes                        | Update DB image & migrate            | Medium; backup DB, test schema & queries            |
| CVE-2023-5156 | MariaDB heap overflow                 | `mariadb:11` container           | MariaDB 11.x                      | Newer `mariadb:11` tag with patch                                 | Update DB image & migrate            | Medium; same as above                               |
| CVE-2022-40674 | expat XML parser overflow            | expat in Debian base             | expat from Debian 12.11           | Patched expat via Debian security updates                         | OS package update / new image       | None expected                                       |
| CVE-2023-40217 | OpenSSH weak moduli                  | SSH on host / base image         | OpenSSH from Debian 12.11         | OpenSSH updated; weak moduli removed                              | Host OS / base image update         | Low; may require regenerating host keys             |
| CVE-2024-0727 | curl SOCKS5 buffer overflow           | curl in Debian base              | curl from Debian 12.11            | Patched curl via Debian security updates                          | OS package update / new image       | None; re-test any outbound HTTP/SOCKS use           |

---

## Component-Level Upgrade Plan

### 1. Nextcloud Application Container (`nextcloud:29-apache`)

**CVEs primarily affecting this container:**

- CVE-2024-3094 (xz-utils)
- CVE-2023-3446 (OpenSSL)
- CVE-2022-37454 (zlib)
- CVE-2024-22365, CVE-2023-29491 (Apache HTTPD)
- CVE-2024-2756, CVE-2024-24808 (PHP / PHP-FPM)
- CVE-2024-0762, CVE-2024-0727 (curl)
- CVE-2022-40674 (expat)
- CVE-2024-1597 (libpq, if used)

**Remediation Strategy:**

1. **Update to a newer patched Nextcloud image in the same major line**  
   - Change `docker-compose.yml` from:  
     `image: nextcloud:29-apache`  
     to something like:  
     `image: nextcloud:29-apache` **(latest patch tag)** or a more specific patched tag your instructor recommends.
2. **Pull & recreate container:**
   ```bash
   cd ~/Team-7-nextcloud-security-lab/infra/docker
   docker-compose pull app
   docker-compose up -d app
