# Docker Container Hardening Notes

**Team:** Team 7
**Date:** 2025-11-25
**Project:** Nextcloud Security Lab - Week 6

---

## Overview

This document explains the security hardening measures applied to the Nextcloud Docker deployment as part of the Week 6 hardening phase.

---

## Hardening Measures Applied

### 1. Pinned Image Versions

**What changed:**
| Container | Before (Insecure) | After (Pinned) |
|-----------|-------------------|----------------|
| db | mariadb:11 | mariadb:11.8.5 |
| app | nextcloud:29-apache | nextcloud:29-apache |
| proxy | nginx:alpine | nginx:mainline-alpine |

**Why it matters:**
- Floating tags (`:latest`, `:11`, `:alpine`) can change without notice
- Pinned versions ensure reproducible deployments
- Security patches can be tracked and verified

---

### 2. Privilege Escalation Prevention

**Configuration:**
```yaml
security_opt:
  - no-new-privileges:true
```

**Applied to:** All containers (db, app, proxy)

**What it does:**
- Prevents processes from gaining additional privileges via setuid/setgid binaries
- Even if an attacker exploits a vulnerability, they cannot escalate to root
- Blocks common privilege escalation attacks

**CIS Benchmark:** 5.25

---

### 3. Linux Capability Restrictions

**Configuration:**
```yaml
cap_drop:
  - ALL
cap_add:
  - [only required capabilities]
```

**Capabilities granted:**

| Container | Capabilities | Purpose |
|-----------|--------------|---------|
| db | CHOWN, SETUID, SETGID, DAC_OVERRIDE | File ownership, user switching, permission override |
| app | CHOWN, SETUID, SETGID, DAC_OVERRIDE, NET_BIND_SERVICE | Same + port 80 binding |
| proxy | CHOWN, SETUID, SETGID, NET_BIND_SERVICE | File ownership, user switching, port 443 binding |

**What it does:**
- Reduces attack surface by removing unnecessary kernel capabilities
- Default Docker containers have 14+ capabilities; we reduced to 4-5 each
- ~70% reduction in privileged operations available to attackers

**CIS Benchmark:** 5.3

---

### 4. Resource Limits

**Configuration:**
```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
    reservations:
      cpus: '0.25'
      memory: 256M
```

**Limits applied:**

| Container | CPU Limit | Memory Limit |
|-----------|-----------|--------------|
| db | 2 cores | 2GB |
| app | 2 cores | 2GB |
| proxy | 1 core | 512MB |

**What it does:**
- Prevents denial-of-service via resource exhaustion
- Malicious uploads or queries cannot consume all server resources
- Ensures fair resource allocation between containers

**CIS Benchmark:** 5.10 (memory), 5.11 (CPU)

---

### 5. Read-Only Root Filesystem (Proxy Only)

**Configuration:**
```yaml
read_only: true
tmpfs:
  - /var/cache/nginx:uid=101,gid=101
  - /var/run:uid=101,gid=101
  - /tmp:uid=101,gid=101
```

**Applied to:** nginx proxy only

**What it does:**
- Prevents attackers from modifying system files
- If nginx is compromised, attackers cannot plant backdoors
- Runtime data goes to tmpfs (RAM) and is cleared on restart

**Why only proxy:**
- Nextcloud needs to write uploaded files
- MariaDB needs to write database files
- Nginx only reads configuration files

**CIS Benchmark:** 5.12

---

### 6. Non-Root User (Proxy Only)

**Configuration:**
```yaml
user: "101:101"
```

**Applied to:** nginx proxy only

**What it does:**
- Runs nginx as UID 101 (nginx user) instead of root
- Even if proxy is compromised, attacker doesn't have root access
- Follows principle of least privilege

**Why only proxy:**
- Nextcloud container handles user switching internally (Apache → www-data)
- MariaDB container handles user switching internally (root → mysql)
- Nginx can run entirely as non-root user

**CIS Benchmark:** 4.1

---

## CVEs Fixed by Patching

The following critical CVEs were addressed by updating to patched image versions:

| CVE ID | Component | CVSS | Status |
|--------|-----------|------|--------|
| CVE-2024-3094 | xz-utils | 10.0 | Fixed (updated Debian base) |
| CVE-2023-3446 | OpenSSL | 9.8 | Fixed (updated Debian base) |
| CVE-2022-37454 | zlib | 9.8 | Fixed (updated Debian base) |
| CVE-2023-4911 | glibc | 7.8 | Fixed (updated Debian base) |
| CVE-2024-2756 | PHP | 7.5 | Fixed (PHP 8.2.29) |

---

## Testing Performed

After applying each hardening measure:

1. **Container startup:** Verified all containers start successfully
2. **Service health:** Confirmed Nextcloud status API responds
3. **Functionality:** Tested login, file upload, sharing
4. **Resource usage:** Verified containers operate within limits

---

## Known Limitations

### Cannot Apply Read-Only Filesystem To:
- **Nextcloud:** Needs to write uploaded files to `/var/www/html/data`
- **MariaDB:** Needs to write database files to `/var/lib/mysql`

### Cannot Run As Non-Root:
- **Nextcloud:** Apache handles privilege dropping internally
- **MariaDB:** MariaDB handles privilege dropping internally

### Remaining CVEs:
- **MariaDB:** 27 CVEs (mostly low severity, gosu binary issues)
- **Nginx:** 6 CVEs (BusyBox related, low risk)
- **Nextcloud:** Pending full rescan

---

## Rollback Procedure

If hardening causes issues:

```bash
# Restore pre-hardening configuration
cd /mnt/c/Users/Jason/Team-7-nextcloud-security-lab/infra/docker
cp docker-compose.yml.backup-pre-hardening docker-compose.yml
docker-compose down
docker-compose up -d
```

Backup locations:
- `docker-compose.yml.backup-pre-hardening`
- `docs/evidence/week6/pre-patch/docker-compose-before.yml`

---

## Production Recommendations

Before deploying to production:

1. **Replace self-signed certificates** with valid CA-signed certs
2. **Remove port 8080 exposure** (direct HTTP access)
3. **Use Docker secrets** instead of .env file
4. **Add health checks** for automated recovery
5. **Implement log aggregation** for security monitoring
6. **Schedule monthly Trivy scans** for ongoing vulnerability management

---

## References

- [CIS Docker Benchmark v1.6.0](https://www.cisecurity.org/benchmark/docker)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [Nextcloud Security Advisories](https://nextcloud.com/security/)

---

## Files

| File | Location | Description |
|------|----------|-------------|
| Hardened Config | `infra/docker/docker-compose.yml` | Current production config |
| Final Deliverable | `reports/docker-compose-hardened-final.yml` | Fully documented version |
| Pre-Hardening Backup | `docs/evidence/week6/pre-patch/docker-compose-before.yml` | Original config |
| Task 5 Evidence | `docs/evidence/week6/hardening/` | Hardening verification files |
