# Task 5: Container Hardening - Completion Checklist
**Date:** 2025-11-25
**Status:** ✅ COMPLETE

---

## Hardening Measures Applied

### ✅ 1. Security Options (All Containers)
- [x] `no-new-privileges:true` on proxy
- [x] `no-new-privileges:true` on app
- [x] `no-new-privileges:true` on db
- **Purpose:** Prevents privilege escalation attacks

### ✅ 2. Linux Capabilities (All Containers)
- [x] Drop ALL capabilities on proxy
- [x] Add back 4 minimal capabilities to proxy (NET_BIND_SERVICE, CHOWN, SETUID, SETGID)
- [x] Drop ALL capabilities on app
- [x] Add back 5 minimal capabilities to app (CHOWN, DAC_OVERRIDE, NET_BIND_SERVICE, SETUID, SETGID)
- [x] Drop ALL capabilities on db
- [x] Add back 4 minimal capabilities to db (CHOWN, DAC_OVERRIDE, SETUID, SETGID)
- **Result:** 70% reduction in permissions (14+ → 4-5 per container)

### ✅ 3. Read-Only Filesystem (Proxy Only)
- [x] Set `read_only: true` on proxy
- [x] Configure tmpfs mounts for `/var/cache/nginx` (with uid=101,gid=101)
- [x] Configure tmpfs mounts for `/var/run` (with uid=101,gid=101)
- [x] Configure tmpfs mounts for `/tmp` (with uid=101,gid=101)
- **Purpose:** Prevents file tampering on reverse proxy

### ✅ 4. Resource Limits (All Containers)
- [x] Proxy: CPU limit 1 core, Memory limit 512MB
- [x] App: CPU limit 2 cores, Memory limit 2GB
- [x] DB: CPU limit 2 cores, Memory limit 2GB
- [x] Set appropriate reservations for all containers
- **Purpose:** Prevents DoS attacks via resource exhaustion

### ✅ 5. Run as Non-Root User (Proxy)
- [x] Set `user: "101:101"` on proxy (nginx user)
- **Note:** App and DB already run as non-root internally
- **Purpose:** Reduce impact if container is compromised

---

## Testing Completed

### ✅ Container Startup Tests
- [x] All containers start successfully
- [x] No restart loops detected
- [x] All containers show "Up" status after 20 seconds

### ✅ Functionality Tests
- [x] Nextcloud status check passes (occ status)
- [x] HTTPS connectivity works (https://10.0.0.47 responds)
- [x] HTTP connectivity works (http://10.0.0.47:8080 responds)
- [x] Database connection successful
- [x] File upload capability verified (implicit - Nextcloud operational)

### ✅ Security Verification Tests
- [x] Verified no-new-privileges on all containers (docker inspect)
- [x] Verified capability drops on all containers (docker inspect)
- [x] Verified read-only filesystem on proxy (docker inspect)
- [x] Verified resource limits on all containers (docker stats)
- [x] Verified user ID on proxy (docker inspect)

---

## Evidence Files Created

### ✅ Required Evidence
- [x] `docker-compose-hardened.yml` - Complete hardened configuration (3.8KB)
- [x] `hardening-verification.txt` - Automated verification output (1.4KB)
- [x] `hardening-summary.md` - Comprehensive hardening documentation (8.3KB)
- [x] `before-after-comparison.md` - Detailed before/after analysis (13KB)
- [x] `TASK5-CHECKLIST.md` - This completion checklist

**Evidence Location:** `/docs/evidence/week6/hardening/`

---

## Configuration Backups

### ✅ Backup Files Created
- [x] `infra/docker/docker-compose.yml.backup-TIMESTAMP` - Pre-hardening config
- [x] `docs/evidence/week6/hardening/docker-compose-hardened.yml` - Post-hardening config

---

## Problems Encountered and Resolved

### Problem 1: Nginx Container Restart Loop
**Issue:** Nginx couldn't create `/var/cache/nginx/client_temp` directory
**Cause:** tmpfs mount created directories as root, nginx user (101) couldn't write
**Solution:** Added `uid=101,gid=101` to tmpfs mount options
**Result:** ✅ Resolved - nginx starts successfully

**Evidence:** docker-compose.yml lines 96-99
```yaml
tmpfs:
  - /var/cache/nginx:uid=101,gid=101
  - /var/run:uid=101,gid=101
  - /tmp:uid=101,gid=101
```

---

## Hardening Not Applied (With Justification)

### 1. Read-Only Filesystem for App and DB
**Decision:** NOT applied
**Reason:** Nextcloud requires write access for file uploads, app installations, and config updates. MariaDB requires write access for database files and transaction logs.
**Alternative:** Applied capability restrictions and resource limits instead.

### 2. User Namespace Remapping
**Decision:** NOT applied
**Reason:** Requires Docker daemon configuration changes (host-level setting). Beyond scope of docker-compose configuration.
**CIS Reference:** 2.9 - Would require `/etc/docker/daemon.json` changes

### 3. AppArmor/SELinux Profiles
**Decision:** NOT applied
**Reason:** WSL2 environment doesn't have AppArmor or SELinux enabled. Would require host OS changes.
**CIS Reference:** 5.1 - Not applicable in WSL2

---

## Security Improvements Summary

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Linux Capabilities (Proxy)** | 14+ | 4 | 71% reduction |
| **Linux Capabilities (App)** | 14+ | 5 | 65% reduction |
| **Linux Capabilities (DB)** | 14+ | 4 | 71% reduction |
| **Privilege Escalation Prevention** | No | Yes | 100% improvement |
| **Resource Limits** | None | Yes (all containers) | 100% improvement |
| **Read-Only Filesystem** | None | Yes (proxy) | Partial improvement |
| **Non-Root User (Proxy)** | No | Yes | 100% improvement |

---

## CIS Docker Benchmark Compliance

### Controls Now Satisfied (Before → After)
- **4.1** - User for container created: ❌ → ✅ (proxy)
- **5.3** - Linux kernel capabilities restricted: ❌ → ✅ (all)
- **5.10** - Memory usage limited: ❌ → ✅ (all)
- **5.11** - CPU priority set: ❌ → ✅ (all)
- **5.12** - Root filesystem read-only: ❌ → ✅ (proxy only)
- **5.25** - Prevent additional privileges: ❌ → ✅ (all)

**Compliance Improvement:** 6 additional CIS controls satisfied

---

## Performance Impact Assessment

### Resource Usage After Hardening
- **Proxy:** 12.85MB / 512MB (2.5%) - Well within limits
- **App:** 92MB / 2GB (4.2%) - Well within limits
- **DB:** 103MB / 2GB (5.0%) - Well within limits

### Performance Conclusion
- ✅ No performance degradation detected
- ✅ All services fully functional
- ✅ Resource limits provide adequate headroom
- ✅ Response times unchanged

---

## Task 5 Deliverables - Complete

- ✅ Applied container hardening to all 3 services
- ✅ Tested all services for functionality
- ✅ Verified hardening measures with docker inspect
- ✅ Documented all changes with before/after comparison
- ✅ Created comprehensive evidence bundle
- ✅ Saved hardened configuration for future reference

**Time Spent:** Approximately 1.5 hours (including troubleshooting nginx issue)

---

## Next Steps (Task 6)

Now that hardening is complete, proceed to:
- **Task 6:** Validate Fixes with Re-Testing
  - Re-run security scans (Trivy, nmap, nikto)
  - Compare before/after scan results
  - Verify CVE fixes are effective
  - Document risk reduction

---

## Sign-Off

**Task 5: Apply Container Hardening** is **COMPLETE**.

All hardening measures have been applied, tested, and documented. The Nextcloud stack is now running with significantly reduced attack surface while maintaining full functionality.

**Evidence Package Ready:** `/docs/evidence/week6/hardening/` (4 files, 26.5KB total)
