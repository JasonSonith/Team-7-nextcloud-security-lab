# Task 4 – Path Traversal / Directory Traversal Findings

## Summary
This task demonstrates how improper input validation on file-handling functionality can allow an attacker to traverse outside the intended directory using sequences like `../`. When successful, the attacker can write files to unauthorized locations or read system files.

---

## Objective
Identify whether Nextcloud’s file upload endpoint is vulnerable to Path Traversal / Directory Traversal by attempting to:

- Upload a file using a manipulated file path (e.g., `../../evil.txt`).
- Observe whether the backend places the file outside the user’s intended directory.
- Confirm protection mechanisms if the upload fails.

---

## Methodology
1. **Created a test payload file:**
   ```bash
echo "WebDAV traversal test" > traversal-test.txt
```

2. **Attempted to upload via WebDAV (curl):**
   ```bash
curl -u 'admin:YOURPASSWORD' -T traversal-test.txt \
'http://<IP>:8080/remote.php/dav/files/admin/../../../../traversal-test.txt'
```

3. **Observed server response and UI behavior.**

4. **Checked if the file appeared in unintended directories** using Docker:
   ```bash
docker exec docker-app-1 find /var/www/html -name 'traversal-test.txt'
```

---

## Evidence Collected
Place the following screenshots in the evidence folder:
- **task4-webui-blocked.png** – UI blocking filename containing `/`.
- **task4-webdav-attempt.png** – curl upload attempt.
- **task4-test-file-visible.png** – The file successfully uploaded only to the legitimate directory.

---

## Results
| Test | Expected | Result |
|------|----------|--------|
| Web UI upload with `../` in filename | Should be blocked | **Blocked – correct behavior** |
| WebDAV upload with crafted path | Should sanitize/deny traversal | **Denied / connection refused** |
| File written outside user directory | Should not occur | **Did not occur** |

---

## Conclusion
Nextcloud *correctly prevents path traversal* through both the Web UI and WebDAV upload endpoints. Attempts to escape the intended directory structure using `../` sequences were blocked, and no unauthorized file placement occurred.

This indicates the system is **not vulnerable** to path traversal in its default configuration, based on the tests performed.

---

## Recommendations
Even though the system behaved correctly, we recommend:
- Continuing to enforce filename sanitization.
- Logging attempts of traversal for detection.
- Hardening WebDAV access with IP restrictions or MFA.

---
**End of Task 4 Findings**

