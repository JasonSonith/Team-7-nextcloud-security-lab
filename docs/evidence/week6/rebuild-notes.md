# Container Rebuild Notes - Week 6

**Date:** 2025-11-25
**Task:** Rebuild containers with patched images

---

## Issue Encountered: Version Downgrade Error

### Problem
Initial attempt to use `nextcloud:29.0.9-apache` failed with error:
```
Can't start Nextcloud because the version of the data (29.0.16.1) is higher
than the docker image version (29.0.9.2) and downgrading is not supported.
```

### Root Cause
- Existing Nextcloud data was created with version **29.0.16.1**
- Attempted to use version **29.0.9** (older version)
- Nextcloud prevents downgrades to protect data integrity

### Solution
Updated docker-compose.yml to use `nextcloud:29-apache` (floating tag) which provides version 29.0.16+, compatible with existing data.

---

## Final Image Versions Used

| Container | Image Tag | Actual Version | Status |
|-----------|-----------|----------------|--------|
| app | nextcloud:29-apache | 29.0.16+ | ✅ Running |
| db | mariadb:11.8.5 | 11.8.5 | ✅ Running |
| proxy | nginx:1.26.2-alpine | 1.26.2 | ✅ Running |

---

## Container Startup Log Summary

### Nextcloud (app)
```
Apache/2.4.62 (Debian) PHP/8.2.29 configured -- resuming normal operations
Command line: 'apache2 -D FOREGROUND'
```
**Status:** ✅ Started successfully, no errors

### MariaDB (db)
```
Version: '11.8.5-MariaDB-ubu2404'
mariadbd: ready for connections.
```
**Status:** ✅ Database ready for connections

### Nginx (proxy)
```
start worker process 26-35 (10 workers)
```
**Status:** ✅ All workers started

---

## Important Note: Nextcloud 29 EOL

**Discovery:** Nextcloud 29 reached End-of-Life (EOL) in April 2025 and was removed from Docker Hub in July 2025.

**Impact for this lab:**
- ✅ Acceptable for lab/testing environment
- ❌ NOT recommended for production
- 📌 For production, upgrade to Nextcloud 30 or 31

**Why we're using it:**
- Existing data is version 29.0.16
- Lab environment for security testing
- Upgrading to v30/31 is out of scope for Week 6

**Recommendation for final report:**
Include recommendation to upgrade to currently supported version (30 or 31) for production deployment.

---

## Commands Used

```bash
# Update docker-compose.yml to use compatible versions
# (Nextcloud: 29-apache, MariaDB: 11.8.5, Nginx: 1.26.2-alpine)

# Stop old containers
docker-compose down

# Pull new images
docker-compose pull app

# Start new containers
docker-compose up -d

# Verify status
docker ps -a
docker logs docker-app-1 --tail 30
docker logs docker-db-1 --tail 15
docker logs docker-proxy-1 --tail 10
```

---

## Evidence Collected

- ✅ Container status: `post-patch-container-status.txt`
- ✅ Image versions: `post-patch-image-versions.txt`
- ✅ Container logs: Reviewed (no errors)
- ⏭️ Functionality tests: Pending
- ⏭️ Trivy scans: Pending

---

## Next Steps

1. Test Nextcloud web UI access (https://10.0.0.47)
2. Verify admin login works
3. Test file upload functionality
4. Test share creation
5. Run Trivy scans on all images
6. Compare CVE counts (before vs after)

---

**Rebuild Status:** ✅ COMPLETE - All containers running successfully
**Time to rebuild:** ~2 minutes
**Downtime:** ~30 seconds
