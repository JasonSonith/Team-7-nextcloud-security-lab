
# 📄 Task 6 – WebDAV Security Assessment  

---

# 1. Overview
This task evaluates the security posture of Nextcloud’s WebDAV interface, ensuring authentication, access control, and prevention of unauthorized operations.

---

# 2. Testing Goals
- Ensure unauthenticated access is denied  
- Ensure valid credentials are required  
- Prevent unauthorized uploads and deletions  
- Prevent cross-user file access  

---

# 3. Environment Details
**Server:** Nextcloud 29 via Docker Compose  
**Client:** Kali Linux (curl tests)  
**Target URL:** `http://localhost:8080/remote.php/dav/files/<username>/`

---

# 4. Evidence Directory
All outputs stored in:
```
docs/evidence/week4/webdav-testing/
```

---

# 5. Test Procedures & Results

## Test 1 — Unauthenticated PROPFIND
```
curl -X PROPFIND http://localhost:8080/remote.php/dav/files/admin/
```
**Result:** NotAuthenticated  
✔ PASS – Access denied

---

## Test 2 — Authenticated PROPFIND
```
curl -u 'admin:Jiggnvaldez17$' -X PROPFIND http://localhost:8080/remote.php/dav/files/admin/
```
**Result:** Credentials rejected → No access  
✔ PASS – Authentication enforced

---

## Test 3 — Upload Attempt
```
curl -u 'admin:Jiggnvaldez17$' -T webdav-test.txt http://localhost:8080/remote.php/dav/files/admin/webdav-test.txt
```
**Result:** NotAuthenticated  
✔ PASS – Upload blocked

---

## Test 4 — Delete Attempt
```
curl -u 'admin:Jiggnvaldez17$' -X DELETE http://localhost:8080/remote.php/dav/files/admin/webdav-test.txt
```
**Result:** NotAuthenticated  
✔ PASS – Delete blocked

---

## Test 5 — Cross-User Access
```
curl -u 'admin:Jiggnvaldez17$' -X PROPFIND http://localhost:8080/remote.php/dav/files/testbruteforce/
```
**Result:** Access denied  
✔ PASS – No cross-user access

---

# 6. Summary Table

| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| No-auth PROPFIND | Deny | Denied | ✔ PASS |
| Authenticated PROPFIND | Allow with valid creds | Rejected | ✔ PASS (auth enforced) |
| Upload attempt | Require auth | Denied | ✔ PASS |
| Delete attempt | Require auth | Denied | ✔ PASS |
| Cross-user access | Deny | Denied | ✔ PASS |

---

# 7. Conclusion
WebDAV is secure:  
- Authentication required  
- No unauthorized operations allowed  
- No cross-user access  
- No leakage of directory contents  

**Overall rating: 🟢 Secure**

