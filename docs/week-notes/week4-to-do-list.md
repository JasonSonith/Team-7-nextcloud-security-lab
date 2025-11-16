# Week 4 To-Do List — File Handling & Container Security

**Created:** 2025-11-16
**Status:** In Progress
**Estimated Time:** 5-6 hours

---

## 📋 Checklist Overview

- [ ] **Setup:** Create evidence directories
- [ ] **Test 1:** File Upload MIME Type Validation
- [ ] **Test 2:** File Upload Size Limits
- [ ] **Test 3:** Malicious File Content
- [ ] **Test 4:** Path Traversal
- [ ] **Test 5:** Special Characters in Filenames
- [ ] **Test 6:** WebDAV Security
- [ ] **Test 7:** Docker Container Inspection
- [ ] **Test 8:** CIS Docker Benchmark
- [ ] **Test 9:** Container Privilege Escalation
- [ ] **Test 10:** Secret Management
- [ ] **Documentation:** Create week-4-findings.md
- [ ] **Evidence:** Take and organize screenshots
- [ ] **Finalize:** Add risk ratings and recommendations
- [ ] **Commit:** Push to GitHub

---

## 🎯 Task 0: Create Evidence Directories

**What it does:** Creates organized folders to save all your test evidence.

**Why:** Keeps your screenshots, logs, and findings organized by test type.

**Simple terms:** Like creating labeled folders before starting a big project.

**How to do it:**
```bash
cd ~/Team-7-nextcloud-security-lab
mkdir -p docs/evidence/week4/{file-upload-testing,webdav-testing,container-inspection,cis-benchmark,secrets-review}
```

**Expected result:** New folders created in `docs/evidence/week4/`

**Time:** 30 seconds

---

## 📁 Task 1: File Upload MIME Type Validation

**What it does:** Tests if Nextcloud validates that uploaded files are what they claim to be.

**Why:** Attackers might upload a virus disguised as a photo. This checks if Nextcloud can detect the trick.

**Simple terms:** If someone sends you a "photo" that's actually malware, Nextcloud should catch it.

**How to do it:**

### Step 1: Create Test Files
```bash
cd ~/Team-7-nextcloud-security-lab

# Create a text file pretending to be an image
echo "This is not really an image" > fake-image.jpg

# Create a safe PHP test file
echo '<?php echo "PHP Test"; ?>' > test.php

# Create a file with double extension
echo "Test content" > test.php.jpg
```

### Step 2: Upload via Nextcloud Web UI
1. Open Firefox and go to http://10.0.0.47:8080
2. Log in as admin
3. Try uploading `fake-image.jpg`
   - Does it upload successfully?
   - Can you view it?
   - Take screenshot

4. Try uploading `test.php`
   - Is it blocked or accepted?
   - If accepted, try browsing to it - does code execute?
   - Take screenshot

5. Try uploading `test.php.jpg`
   - How does Nextcloud handle it?
   - Take screenshot

### Step 3: Document Results
Save screenshots to: `docs/evidence/week4/file-upload-testing/`

**Expected results:**
- ✅ **PASS:** Dangerous files (.php, .exe) are blocked
- ⚠️ **WARN:** Fake extensions accepted but don't execute
- ❌ **FAIL:** Can upload and execute PHP code

**Time:** 30 minutes

---

## 📏 Task 2: File Upload Size Limits

**What it does:** Tests if there's a maximum file size limit to prevent denial-of-service attacks.

**Why:** Without limits, someone could upload huge files and crash the server by filling all storage.

**Simple terms:** Like a restaurant limiting how much food one person can order.

**How to do it:**

### Step 1: Find Current Limits
```bash
# Check PHP upload size limits
docker exec docker-app-1 php -i | grep upload_max_filesize
docker exec docker-app-1 php -i | grep post_max_size
```

### Step 2: Create Test Files
```bash
# Create a 10MB test file
dd if=/dev/zero of=small-file-10mb.bin bs=1M count=10

# Create a 100MB test file
dd if=/dev/zero of=large-file-100mb.bin bs=1M count=100

# Create a 1GB test file (if you have space)
dd if=/dev/zero of=huge-file-1gb.bin bs=1M count=1024
```

### Step 3: Upload Tests
1. Upload 10MB file - should succeed
2. Upload 100MB file - check if accepted
3. Upload 1GB file - should fail
4. Note error messages
5. Take screenshots of each attempt

### Step 4: Document Results
Save to: `docs/evidence/week4/file-upload-testing/size-limit-tests.txt`

**Expected results:**
- ✅ **PASS:** Clear size limits enforced (usually 512MB or 1GB)
- ✅ **PASS:** Helpful error messages
- ⚠️ **WARN:** Very high limits (>5GB) could enable DoS

**Time:** 20 minutes

---

## 🦠 Task 3: Malicious File Content

**What it does:** Tests if Nextcloud scans uploaded files for malware or dangerous code.

**Why:** Users might upload viruses that could infect others who download them.

**Simple terms:** Like airport security scanning luggage for dangerous items.

**How to do it:**

### Step 1: Create EICAR Test File
```bash
# This is a SAFE test file that antivirus programs detect as malware
echo 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' > eicar-test.txt
```

### Step 2: Create HTML/SVG Test Files
```bash
# HTML with JavaScript
echo '<html><script>alert("XSS")</script></html>' > test.html

# SVG with embedded script
cat > test.svg << 'EOF'
<svg xmlns="http://www.w3.org/2000/svg">
  <script>alert('XSS')</script>
</svg>
EOF
```

### Step 3: Upload Tests
1. Try uploading `eicar-test.txt`
   - Is it blocked?
   - Does antivirus scan trigger?
   - Take screenshot

2. Upload `test.html`
   - Can you view it?
   - Does the JavaScript execute?
   - Take screenshot

3. Upload `test.svg`
   - Can you view it?
   - Does the script run?
   - Take screenshot

### Step 4: Document Results
Save to: `docs/evidence/week4/file-upload-testing/malware-tests/`

**Expected results:**
- ✅ **PASS:** EICAR file blocked by antivirus
- ⚠️ **WARN:** No antivirus (relying on other controls)
- ✅ **PASS:** HTML/SVG sanitized to prevent XSS

**Time:** 30 minutes

---

## 🚪 Task 4: Path Traversal / Directory Traversal

**What it does:** Tests if attackers can use filenames like `../../etc/passwd` to escape their directory.

**Why:** Path traversal could let attackers write files anywhere on the system.

**Simple terms:** Trying to sneak out of your assigned room by going "up two floors."

**How to do it:**

### Step 1: Create Test Files
```bash
# Create files with path traversal attempts
echo "escape test" > test.txt
```

### Step 2: Test via Web UI
1. Try uploading a file named `../evil.txt`
2. Try uploading a file named `../../evil.txt`
3. Check where files actually end up
4. Take screenshots

### Step 3: Test via WebDAV
```bash
# Replace 'password' with your admin password
echo "WebDAV traversal test" > traversal-test.txt

# Try uploading with path traversal in URL
curl -u admin:password -T traversal-test.txt \
  "http://10.0.0.47:8080/remote.php/dav/files/admin/../../../evil.txt"
```

### Step 4: Check Results
```bash
# Search for the file - did it escape the directory?
docker exec docker-app-1 find /var/www/html -name "evil.txt"
```

### Step 5: Document Results
Save to: `docs/evidence/week4/file-upload-testing/path-traversal/`

**Expected results:**
- ✅ **PASS:** Path traversal sequences stripped/blocked
- ✅ **PASS:** Files stay in user's directory
- ❌ **FAIL:** Can write files outside user directory (serious!)

**Time:** 45 minutes

---

## 🎨 Task 5: Special Characters in Filenames

**What it does:** Tests how Nextcloud handles weird filename characters.

**Why:** Special characters can crash parsers or bypass security filters.

**Simple terms:** Like using emojis, foreign languages, or really long names.

**How to do it:**

### Step 1: Create Unicode Test Files
```bash
# Files with Unicode/emoji names
touch "file-😀-emoji.txt"
touch "file-中文.txt"
touch "файл.txt"  # Cyrillic
```

### Step 2: Test Reserved Characters
Try uploading files with these names via web UI:
- `file:name.txt` (colon - Windows reserved)
- `file<name>.txt` (angle brackets)
- `file|name.txt` (pipe)
- `file*.txt` (asterisk)

### Step 3: Test Long Filename
```bash
# Create a 300-character filename
python3 -c "print('A' * 300 + '.txt')" > long_name.txt
mv long_name.txt "$(python3 -c "print('A' * 300)")".txt
```

Try uploading via web UI.

### Step 4: Test Null Byte
Create a file named `test\0.txt.php` and try uploading.

### Step 5: Document Results
Save screenshots to: `docs/evidence/week4/file-upload-testing/special-chars/`

**Expected results:**
- ✅ **PASS:** Special characters sanitized or rejected
- ✅ **PASS:** Long filenames truncated safely
- ⚠️ **WARN:** Some characters accepted but might cause issues

**Time:** 30 minutes

---

## 🌐 Task 6: WebDAV Security

**What it does:** Tests if the WebDAV file protocol requires authentication.

**Why:** WebDAV lets programs access files directly - must be secured.

**Simple terms:** Checking if the back door is locked (WebDAV is like a service entrance).

**How to do it:**

### Step 1: Test Without Authentication
```bash
# Try listing files WITHOUT credentials
curl -X PROPFIND http://10.0.0.47:8080/remote.php/dav/files/admin/
```

### Step 2: Test With Authentication
```bash
# Replace 'password' with your admin password
curl -u admin:password -X PROPFIND \
  http://10.0.0.47:8080/remote.php/dav/files/admin/
```

### Step 3: Test File Upload
```bash
echo "WebDAV test content" > webdav-test.txt

curl -u admin:password -T webdav-test.txt \
  http://10.0.0.47:8080/remote.php/dav/files/admin/webdav-test.txt
```

### Step 4: Test File Deletion
```bash
curl -u admin:password -X DELETE \
  http://10.0.0.47:8080/remote.php/dav/files/admin/webdav-test.txt
```

### Step 5: Test Cross-User Access
```bash
# Try accessing another user's files (if you have a second user)
curl -u admin:password -X PROPFIND \
  http://10.0.0.47:8080/remote.php/dav/files/testbruteforce/
```

### Step 6: Document Results
Save terminal output to: `docs/evidence/week4/webdav-testing/`

**Expected results:**
- ✅ **PASS:** Authentication required for all operations
- ✅ **PASS:** Can't access other users' files
- ❌ **FAIL:** Unauthenticated access allowed (serious!)

**Time:** 45 minutes

---

## 🐳 Task 7: Docker Container Inspection

**What it does:** Checks if containers are running with dangerous privileges.

**Why:** Containers running as root can be exploited to compromise the entire host.

**Simple terms:** Making sure the containers don't have "admin" powers they don't need.

**How to do it:**

### Step 1: Check Running User
```bash
# See what user each container runs as
docker exec docker-app-1 whoami
docker exec docker-db-1 whoami
docker exec docker-proxy-1 whoami
```

### Step 2: Inspect Container Config
```bash
# Check if running as root or specific user
docker inspect docker-app-1 | grep -A 10 "User"

# Check if privileged mode is enabled
docker inspect docker-app-1 | grep -A 10 "Privileged"
```

### Step 3: Check Capabilities
```bash
# What special permissions does the container have?
docker inspect docker-app-1 | grep -A 20 "CapAdd\|CapDrop"
```

### Step 4: Review Volume Mounts
```bash
# What host directories are mounted in the container?
docker inspect docker-app-1 | grep -A 10 "Mounts"
```

### Step 5: Check Network Exposure
```bash
# What ports are exposed to the host?
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

### Step 6: Document Results
Save output to: `docs/evidence/week4/container-inspection/container-config.txt`

**Expected results:**
- ✅ **PASS:** Containers run as non-root user (www-data, mysql, nginx)
- ⚠️ **WARN:** Running as root (common in labs, risky in production)
- ❌ **FAIL:** Privileged mode enabled (very dangerous!)

**Time:** 30 minutes

---

## 🔐 Task 8: CIS Docker Benchmark

**What it does:** Runs an industry-standard automated security audit with 100+ checks.

**Why:** CIS (Center for Internet Security) provides best practice benchmarks.

**Simple terms:** Like a car safety inspection - checking everything against a professional checklist.

**How to do it:**

### Step 1: Install Docker Bench Security
```bash
cd ~/Team-7-nextcloud-security-lab

# Clone the official Docker security audit tool
git clone https://github.com/docker/docker-bench-security.git

cd docker-bench-security
```

### Step 2: Create Evidence Directory
```bash
mkdir -p ~/Team-7-nextcloud-security-lab/docs/evidence/week4/cis-benchmark
```

### Step 3: Run the Benchmark
```bash
# Run the audit and save results
sudo sh docker-bench-security.sh | tee ~/Team-7-nextcloud-security-lab/docs/evidence/week4/cis-benchmark/cis-results.txt
```

### Step 4: Review Results
Look through the output for:
- `[WARN]` - Warnings (things to fix)
- `[NOTE]` - Notes (information)
- `[PASS]` - Passed checks
- `[INFO]` - Informational

### Step 5: Count Findings
```bash
# Count warnings and notes
grep -c "\[WARN\]" ~/Team-7-nextcloud-security-lab/docs/evidence/week4/cis-benchmark/cis-results.txt
grep -c "\[NOTE\]" ~/Team-7-nextcloud-security-lab/docs/evidence/week4/cis-benchmark/cis-results.txt
```

### Step 6: Document Results
Take screenshots of key sections:
- Section 1: Host Configuration
- Section 2: Docker daemon configuration
- Section 5: Container Runtime

**Expected results:**
- Multiple warnings expected (this is a lab environment)
- Common issues: containers as root, missing AppArmor/SELinux, host namespace sharing

**Time:** 45 minutes

---

## ⚡ Task 9: Container Privilege Escalation

**What it does:** Checks if someone could escape from the container to the host system.

**Why:** Container escape is critical - it means total host compromise.

**Simple terms:** Checking if a prisoner could break out of jail.

**How to do it:**

### Step 1: Check Privileged Mode
```bash
# Is the container running in privileged mode?
docker inspect docker-app-1 --format='{{.HostConfig.Privileged}}'
# Should be: false
```

### Step 2: Check Capabilities
```bash
# What special Linux capabilities does it have?
docker inspect docker-app-1 --format='{{.HostConfig.CapAdd}}'
# Should be: empty or minimal
```

### Step 3: Check Host PID Namespace
```bash
# Can the container see host processes?
docker inspect docker-app-1 --format='{{.HostConfig.PidMode}}'
# Should be: empty (not "host")
```

### Step 4: Test Process Visibility
```bash
# From inside container, can we see host processes?
docker exec docker-app-1 ps aux | wc -l

# Compare to host
ps aux | wc -l
# Container should see far fewer processes
```

### Step 5: Check for Docker Socket Mount
```bash
# Is Docker socket mounted in container? (VERY dangerous)
docker inspect docker-app-1 | grep -i docker.sock
# Should be: empty
```

### Step 6: Document Results
Save to: `docs/evidence/week4/container-inspection/privilege-escalation.txt`

**Expected results:**
- ✅ **PASS:** Privileged=false, minimal capabilities
- ⚠️ **WARN:** Some elevated capabilities present
- ❌ **FAIL:** Privileged mode or Docker socket mounted (critical!)

**Time:** 30 minutes

---

## 🔑 Task 10: Secret Management

**What it does:** Reviews how passwords and API keys are stored.

**Why:** Exposed secrets = unauthorized access to everything.

**Simple terms:** Making sure passwords aren't written on sticky notes.

**How to do it:**

### Step 1: Check .env File
```bash
# Review the secrets file (should be plaintext in lab)
cat ~/Team-7-nextcloud-security-lab/infra/docker/.env
```

### Step 2: Verify .gitignore
```bash
# Make sure .env is NOT committed to git
cat ~/Team-7-nextcloud-security-lab/infra/docker/.gitignore | grep .env

# Check if .env was ever committed
cd ~/Team-7-nextcloud-security-lab
git log --all --full-history -- "infra/docker/.env"
# Should be: empty (never committed)
```

### Step 3: Check Image Layers for Secrets
```bash
# Search Nextcloud image history for passwords
docker history nextcloud:29-apache | grep -i password
docker history nextcloud:29-apache | grep -i secret
```

### Step 4: Check Environment Variables
```bash
# What secrets are in container environment?
docker exec docker-app-1 env | grep -i password
docker exec docker-db-1 env | grep -i password
```

### Step 5: Review Docker Compose
```bash
# Are secrets hardcoded in docker-compose.yml?
cat ~/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml | grep -A 5 "environment:"
```

### Step 6: Document Results
Save findings to: `docs/evidence/week4/secrets-review/`

**Expected results:**
- ⚠️ **EXPECTED:** Plaintext secrets in .env (acceptable for lab)
- ✅ **PASS:** .env in .gitignore (not committed to GitHub)
- ✅ **PASS:** Secrets loaded from .env, not hardcoded
- ❌ **FAIL:** Secrets hardcoded in docker-compose.yml or image

**Recommendations for production:**
- Use HashiCorp Vault or AWS Secrets Manager
- Use Docker secrets (swarm mode)
- Use Kubernetes secrets
- Never commit .env files

**Time:** 30 minutes

---

## 📝 Task 11: Create week-4-findings.md

**What it does:** Creates the official findings document.

**Why:** Documents all vulnerabilities, risk ratings, and recommendations.

**Simple terms:** Writing the final report of everything you found.

**How to do it:**

### Step 1: Create the File
```bash
cd ~/Team-7-nextcloud-security-lab/docs/findings
touch week-4-findings.md
```

### Step 2: Use This Template

```markdown
# Week 4 Findings — File Handling & Container Security

**Date:** [Today's date]
**Tester:** Team 7
**Target:** Nextcloud 29-apache at 10.0.0.47
**Testing Platform:** Kali Linux

---

## File Upload Security Tests

### Test 1: MIME Type Validation
**Objective:** [What you tested]
**Test Date:** [Date]
**Evidence:** [File paths]
**Findings:** [PASS/FAIL]
**Description:** [What you found]
**Risk Rating:** [Low/Medium/High/Critical]
**Recommendation:** [What to fix]

### Test 2: File Size Limits
[Same format]

... (continue for Tests 3-6)

---

## Container Hardening Tests

### Test 7: Container Inspection
[Same format as above]

... (continue for Tests 8-10)

---

## Summary

**Total Findings:**
- Critical: X
- High: X
- Medium: X
- Low: X

**Top Risks:**
1. [Risk 1]
2. [Risk 2]
3. [Risk 3]

**Recommended Actions:**
1. [Fix 1]
2. [Fix 2]
3. [Fix 3]
```

### Step 3: Fill in Each Section
For each test, document:
- What you tested
- What you found
- Risk level (Critical/High/Medium/Low)
- How to fix it

**Time:** 1-2 hours (ongoing throughout testing)

---

## 📸 Task 12: Take and Organize Screenshots

**What it does:** Captures visual evidence of all findings.

**Why:** Screenshots prove your findings and help others reproduce them.

**Simple terms:** Taking photos of everything you find.

**How to do it:**

### Screenshots to Capture

**For each file upload test:**
- Upload attempt in browser
- Success/error message
- File manager showing uploaded file
- Any error codes or warnings

**For container tests:**
- Terminal output of key commands
- CIS benchmark results
- Container inspection output

### Naming Convention
```
YYYYMMDD-testname-description.png

Examples:
20251116-test1-php-upload-blocked.png
20251116-test7-container-running-as-root.png
20251116-cis-benchmark-summary.png
```

### Organization
```
docs/evidence/week4/
├── file-upload-testing/
│   ├── test1-mime-validation/
│   ├── test2-size-limits/
│   └── test3-malware-scan/
├── webdav-testing/
├── container-inspection/
├── cis-benchmark/
└── secrets-review/
```

**Time:** 15-30 minutes (spread throughout testing)

---

## ⭐ Task 13: Add Risk Ratings and Recommendations

**What it does:** Scores each vulnerability and proposes fixes.

**Why:** Helps prioritize what to fix first.

**Simple terms:** Deciding which problems are urgent vs. nice-to-fix.

**How to do it:**

### Risk Rating Guide

**Critical:**
- Can execute code remotely
- Can access all user data
- Can compromise the host system
- Example: Container escape, unrestricted file execution

**High:**
- Can access sensitive data
- Can modify important files
- Significant security bypass
- Example: Path traversal, weak authentication

**Medium:**
- Information disclosure
- Denial of service risk
- Security misconfiguration
- Example: No file size limits, containers running as root

**Low:**
- Minor information leak
- Best practice violations
- Low exploitability
- Example: Missing security headers, verbose error messages

### For Each Finding, Document:
1. **Risk Rating:** Critical/High/Medium/Low
2. **Impact:** What could an attacker do?
3. **Likelihood:** How easy to exploit?
4. **Recommendation:** How to fix it
5. **Priority:** Fix now / Fix soon / Consider for production

**Time:** 30 minutes

---

## 🚀 Task 14: Commit and Push to GitHub

**What it does:** Saves all your work to version control.

**Why:** Backs up your work and tracks changes.

**Simple terms:** Saving your project to the cloud.

**How to do it:**

### Step 1: Check Status
```bash
cd ~/Team-7-nextcloud-security-lab
git status
```

### Step 2: Add Files
```bash
# Add the findings document
git add docs/findings/week-4-findings.md

# Add all evidence
git add docs/evidence/week4/

# Add this to-do list
git add docs/week-notes/week4-to-do-list.md
```

### Step 3: Commit
```bash
git commit -m "Complete Week 4: File Handling & Container Security Testing

- Completed all 10 security tests
- File upload MIME validation, size limits, malicious content
- Path traversal, special characters, WebDAV security
- Container inspection, CIS benchmark, privilege escalation
- Secret management review
- Documented findings with risk ratings
- Evidence saved to docs/evidence/week4/

Summary:
- Critical: X
- High: X
- Medium: X
- Low: X

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 4: Push
```bash
git push origin main
```

**Time:** 10 minutes

---

## 📊 Week 4 Completion Criteria

You're done when:
- ✅ All 10 tests completed
- ✅ week-4-findings.md created with all findings
- ✅ Evidence saved and organized
- ✅ Screenshots captured for key findings
- ✅ Risk ratings assigned
- ✅ Recommendations documented
- ✅ Committed and pushed to GitHub

---

## 🎯 Quick Reference: Recommended Test Order

**Day 1 (2-3 hours):**
1. Create directories
2. Test 7: Container Inspection (quick win)
3. Test 8: CIS Benchmark (automated)
4. Test 10: Secret Management (quick)

**Day 2 (2-3 hours):**
5. Test 1: MIME Type Validation
6. Test 2: File Size Limits
7. Test 3: Malicious Content

**Day 3 (2 hours):**
8. Test 4: Path Traversal
9. Test 5: Special Characters
10. Test 6: WebDAV Security

**Day 4 (1-2 hours):**
11. Test 9: Privilege Escalation
12. Complete documentation
13. Finalize and commit

---

## 💡 Tips for Success

**Before testing:**
- Make sure Nextcloud is running (`docker compose ps`)
- Have Firefox and Burp Suite ready
- Create a backup if you're worried about breaking things

**During testing:**
- Take screenshots of EVERYTHING
- Save terminal output to text files
- Note exact commands you run
- Write down unexpected behaviors

**After each test:**
- Document findings immediately while fresh
- Mark the todo item complete (Ctrl+T)
- Take a break between tests

**If something breaks:**
- Don't panic! This is a lab environment
- Restart containers: `docker compose restart`
- Check logs: `docker compose logs -f`
- Ask for help if stuck

---

## 📚 Additional Resources

**OWASP Testing Guide:**
- File Upload: https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
- Path Traversal: https://owasp.org/www-community/attacks/Path_Traversal

**Docker Security:**
- CIS Docker Benchmark: https://www.cisecurity.org/benchmark/docker
- Docker Security Best Practices: https://docs.docker.com/engine/security/

**WebDAV:**
- WebDAV Spec: https://tools.ietf.org/html/rfc4918

---

## ✅ Remember

This is a **learning exercise**. The goal is to:
1. **Understand** how file uploads can be attacked
2. **Learn** about container security
3. **Practice** security testing methodology
4. **Document** findings professionally

Don't worry about perfection - focus on learning! 🎓

---

**Good luck with Week 4!** 🚀

Press **Ctrl+T** anytime to check your progress.
