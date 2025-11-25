# Container Hardening Summary
**Date:** 2025-11-25
**Task:** Week 6 - Task 5: Apply Container Hardening
**Status:** COMPLETE

## Overview
Applied CIS Docker Benchmark hardening controls to all three containers (proxy, app, db) in the Nextcloud stack. All containers are now running with reduced attack surface and resource limits.

---

## Hardening Measures Applied

### 1. Security Options (All Containers)
**Control:** `no-new-privileges:true`
**Purpose:** Prevents privilege escalation attacks
**Simple Explanation:** Even if an attacker finds a bug, they can't gain higher permissions (like root)
**CIS Reference:** 5.25 - Ensure that the container is restricted from acquiring additional privileges

### 2. Linux Capabilities (All Containers)
**Control:** Drop all capabilities, add back only what's needed
**Purpose:** Remove "superuser powers" from containers
**Simple Explanation:** Like giving someone a house key instead of a master key to the whole building

**Capabilities by Container:**

#### Proxy (nginx):
- **Dropped:** ALL
- **Added:** CAP_NET_BIND_SERVICE, CAP_CHOWN, CAP_SETUID, CAP_SETGID
- **Why needed:**
  - `CAP_NET_BIND_SERVICE` - Bind to port 443 (privileged port)
  - `CAP_CHOWN` - Change ownership of cache files
  - `CAP_SETUID/SETGID` - Drop privileges after binding to port

#### App (Nextcloud):
- **Dropped:** ALL
- **Added:** CAP_CHOWN, CAP_DAC_OVERRIDE, CAP_NET_BIND_SERVICE, CAP_SETUID, CAP_SETGID
- **Why needed:**
  - `CAP_CHOWN` - Manage uploaded file ownership
  - `CAP_DAC_OVERRIDE` - Override file permissions for uploads
  - `CAP_NET_BIND_SERVICE` - Apache binds to port 80
  - `CAP_SETUID/SETGID` - Apache switches to www-data user

#### DB (MariaDB):
- **Dropped:** ALL
- **Added:** CAP_CHOWN, CAP_DAC_OVERRIDE, CAP_SETUID, CAP_SETGID
- **Why needed:**
  - `CAP_CHOWN` - Manage database file ownership
  - `CAP_DAC_OVERRIDE` - Override permissions for database operations
  - `CAP_SETUID/SETGID` - Switch to mysql user

**CIS Reference:** 5.3 - Ensure that Linux kernel capabilities are restricted within containers

### 3. Read-Only Root Filesystem (Proxy Only)
**Control:** `read_only: true` with tmpfs mounts for writable areas
**Purpose:** Prevent attackers from modifying system files
**Simple Explanation:** Like write-protecting a USB drive - you can read files but can't change them

**Nginx tmpfs mounts:**
- `/var/cache/nginx` - For caching (owned by nginx user)
- `/var/run` - For PID files (owned by nginx user)
- `/tmp` - For temporary files (owned by nginx user)

**Why only proxy?** Nextcloud and MariaDB need to write to their data directories for uploads and database operations.

**CIS Reference:** 5.12 - Ensure that the container's root filesystem is mounted as read only

### 4. Resource Limits (All Containers)
**Control:** CPU and memory limits via `deploy.resources`
**Purpose:** Prevent Denial of Service (DoS) attacks
**Simple Explanation:** Like setting a speed limit and maximum capacity - stops one container from using all resources

**Limits Applied:**
- **Proxy (nginx):** 1 CPU, 512MB RAM (reservation: 0.25 CPU, 128MB)
- **App (Nextcloud):** 2 CPUs, 2GB RAM (reservation: 0.5 CPU, 512MB)
- **DB (MariaDB):** 2 CPUs, 2GB RAM (reservation: 0.25 CPU, 256MB)

**CIS Reference:** 5.10/5.11 - Ensure memory and CPU priority are set appropriately

### 5. Run as Non-Root User (Proxy)
**Control:** `user: "101:101"` (nginx user)
**Purpose:** Reduce impact if container is compromised
**Simple Explanation:** Run the service as a regular user, not administrator

**Note:** Nextcloud and MariaDB already run as non-root users internally (www-data:33, mysql:999)

**CIS Reference:** 4.1 - Ensure that a user for the container has been created

---

## Testing Results

### Functionality Tests
All services are fully operational after hardening:

**Nextcloud Status:**
- ✅ Version: 29.0.16.1
- ✅ Installed: true
- ✅ Maintenance: false
- ✅ Database: Connected

**Connectivity Tests:**
- ✅ HTTPS (port 443): Working - HTTP/2 302 redirect
- ✅ HTTP (port 8080): Working - HTTP/1.1 302 redirect

### Security Verification
**Proxy Container:**
- ✅ no-new-privileges enabled
- ✅ Read-only filesystem active
- ✅ All capabilities dropped, only 4 added back
- ✅ Running as user 101:101 (nginx)
- ✅ Resource limits: 512MB max

**App Container:**
- ✅ no-new-privileges enabled
- ✅ All capabilities dropped, only 5 added back
- ✅ Resource limits: 2GB max

**DB Container:**
- ✅ no-new-privileges enabled
- ✅ All capabilities dropped, only 4 added back
- ✅ Resource limits: 2GB max

**Current Resource Usage:**
- Proxy: 12.85MB / 512MB (2.5%)
- App: 92MB / 2GB (4.2%)
- DB: 103MB / 2GB (5.0%)

---

## Hardening Not Applied (With Justification)

### 1. Read-Only Filesystem for App and DB
**Why not applied:** Nextcloud requires write access for:
- File uploads to `/var/www/html/data`
- App installations to `/var/www/html/apps`
- Config updates to `/var/www/html/config`

MariaDB requires write access for:
- Database files in `/var/lib/mysql`
- Transaction logs
- Temporary tables

**Alternative mitigation:** Applied capability restrictions and resource limits instead.

### 2. User Namespace Remapping
**Why not applied:** Docker Compose doesn't easily support user namespace remapping without daemon configuration changes. This is a host-level setting.

**CIS Reference:** 2.9 - Enable user namespace support (would require Docker daemon reconfiguration)

### 3. AppArmor/SELinux Profiles
**Why not applied:** WSL2 environment doesn't have AppArmor or SELinux enabled. Would require host OS changes.

**CIS Reference:** 5.1 - Ensure that AppArmor profile is enabled

---

## Security Impact Assessment

### Attack Surface Reduction
**Before Hardening:**
- Containers ran with default capabilities (CAP_AUDIT_WRITE, CAP_CHOWN, CAP_DAC_OVERRIDE, CAP_FOWNER, CAP_FSETID, CAP_KILL, CAP_MKNOD, CAP_NET_BIND_SERVICE, CAP_NET_RAW, CAP_SETFCAP, CAP_SETGID, CAP_SETPCAP, CAP_SETUID, CAP_SYS_CHROOT)
- No resource limits (could consume all host resources)
- No privilege escalation prevention
- Proxy ran as root user

**After Hardening:**
- Only 4-5 capabilities per container (removed 10+ unnecessary capabilities)
- Resource limits prevent DoS
- Privilege escalation blocked
- Proxy runs as non-root
- Proxy has read-only filesystem

### Risk Reduction Examples

**Scenario 1: Web Shell Upload**
- **Before:** Attacker uploads malicious PHP file, executes with full container capabilities
- **After:** Even if executed, attacker can't escalate privileges (no-new-privileges), can't modify system files (read-only on proxy), and is limited to 2GB RAM/2 CPUs

**Scenario 2: Container Escape Attempt**
- **Before:** Attacker might leverage capabilities like CAP_SYS_ADMIN or CAP_NET_RAW to break out
- **After:** Those capabilities are dropped, making escape much harder

**Scenario 3: Resource Exhaustion Attack**
- **Before:** Malicious user could upload huge file or run query that consumes all RAM
- **After:** Container is limited to 2GB max, protecting host and other containers

---

## Evidence Files

1. **docker-compose-hardened.yml** - Complete hardened configuration
2. **hardening-verification.txt** - Automated verification output
3. **hardening-summary.md** - This document

All files located in: `/docs/evidence/week6/hardening/`

---

## Recommendations for Production

For a production deployment, additional hardening should include:

1. **Enable Docker Content Trust** - Verify image signatures
2. **Use minimal base images** - Alpine or distroless variants
3. **Implement seccomp profiles** - Restrict system calls
4. **Enable AppArmor/SELinux** - Mandatory access control
5. **User namespace remapping** - Isolate container users from host
6. **Network segmentation** - Separate database on isolated network
7. **Regular security scanning** - Automated CVE detection
8. **Log aggregation** - Centralized logging for security monitoring

---

## Conclusion

Successfully applied 5 major hardening controls to the Nextcloud Docker stack:
- ✅ Privilege escalation prevention (no-new-privileges)
- ✅ Capability restriction (drop ALL, add minimum required)
- ✅ Read-only filesystem (proxy only)
- ✅ Resource limits (all containers)
- ✅ Non-root user (proxy)

All services remain fully functional while significantly reducing attack surface. The hardening addresses multiple CIS Docker Benchmark findings from Week 4.
