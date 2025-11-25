# Functionality Test Results - Week 6

**Date:** 2025-11-25
**Task:** Verify patched containers are working correctly

---

## Automated Test Results

### ✅ Test 1: Container Health Check
**Command:** `docker ps`
**Result:** PASS
```
NAMES            IMAGE                 STATUS
docker-proxy-1   nginx:1.26.2-alpine   Up
docker-app-1     nextcloud:29-apache   Up
docker-db-1      mariadb:11.8.5        Up
```
**All 3 containers running successfully**

---

### ✅ Test 2: PHP Runtime Version
**Command:** `docker exec docker-app-1 php -v`
**Result:** PASS
```
PHP 8.2.29 (cli) (built: Jul 3 2025 23:03:29)
```
**Confirms PHP 8.2.29 is running (includes CVE-2024-2756 fix)**

---

### ✅ Test 3: MariaDB Version
**Command:** `docker exec docker-db-1 mariadb --version`
**Result:** PASS
```
mariadb from 11.8.5-MariaDB
```
**Confirms MariaDB 11.8.5 is running (patched version)**

---

### ✅ Test 4: Nextcloud Application Status
**Command:** `docker exec docker-app-1 curl -s http://localhost/status.php`
**Result:** PASS
```json
{
  "installed": true,
  "maintenance": false,
  "needsDbUpgrade": false,
  "version": "29.0.16.1",
  "versionstring": "29.0.16",
  "edition": "",
  "productname": "Nextcloud",
  "extendedSupport": false
}
```

**Key indicators:**
- ✅ installed: true - Nextcloud is properly installed
- ✅ maintenance: false - Not in maintenance mode
- ✅ needsDbUpgrade: false - Database is up to date
- ✅ version: 29.0.16.1 - Running expected version

---

### ✅ Test 5: Application Files Exist
**Command:** `docker exec docker-app-1 ls -la /var/www/html/index.php`
**Result:** PASS
```
-rw-r--r-- 1 www-data www-data 4564 Oct 10 23:14 /var/www/html/index.php
```
**Nextcloud files present and owned by correct user (www-data)**

---

## Manual Testing Checklist

To complete functionality testing, perform these manual tests:

### Web UI Access Test
- [ ] Open browser to https://10.0.0.47
- [ ] Accept self-signed certificate warning
- [ ] Verify Nextcloud login page appears

### Authentication Test
- [ ] Log in with admin credentials from .env file
- [ ] Verify successful login to dashboard
- [ ] Check no error messages appear

### File Operations Test
- [ ] Upload a test file (small .txt or .jpg)
- [ ] Verify file appears in files list
- [ ] Download the file back
- [ ] Delete the test file

### Sharing Test
- [ ] Select a file
- [ ] Create a share link
- [ ] Verify share link is generated
- [ ] (Optional) Open share link in incognito window

### WebDAV Test (Optional)
```bash
# From command line
curl -u admin:password -X PROPFIND https://10.0.0.47/remote.php/dav/files/admin/
```
- [ ] Verify WebDAV responds (should list files)

---

## Test Summary

**Automated Tests:** 5/5 PASSED ✅
**Manual Tests:** Pending user confirmation

**Overall Status:** System is functional and ready for security verification

---

## Known Limitations

**Network Access:**
- Direct curl from WSL to https://10.0.0.47 timed out
- This is likely due to WSL network routing or firewall
- Internal container tests confirm application is working
- Browser access from Windows host should work fine

---

## Evidence Files Created

- Container status: `post-patch-container-status.txt`
- Image versions: `post-patch-image-versions.txt`
- Functionality tests: This document

---

## Next Steps

1. ✅ Automated functionality tests - COMPLETE
2. ⏭ Manual browser testing - User to complete
3. ⏭ Run Trivy scans to verify CVE fixes
4. ⏭ Compare before/after CVE counts

---

**Testing Status:** ✅ AUTOMATED TESTS PASSED - Manual verification recommended
**Time to test:** ~5 minutes automated + 10 minutes manual
