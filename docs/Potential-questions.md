# Potential Presentation Questions & Answers

**Project:** Nextcloud Security Lab - Team 7
**Course:** CSC-440 Secure Software Engineering
**Date:** Fall 2025

---

## Question 1: Why did you choose Nextcloud over other cloud platforms like ownCloud or Seafile?

**Answer:**
We chose Nextcloud for several reasons:
1. **Popularity** - Nextcloud is the most widely deployed self-hosted cloud solution, so findings are broadly applicable
2. **Active Development** - Large community with frequent security updates, giving us real CVEs to analyze
3. **Docker Support** - Official Docker images made it easy to set up a reproducible lab environment
4. **Attack Surface** - Nextcloud has a rich feature set (file sharing, user management, apps) that provides many areas to test
5. **Documentation** - Excellent security documentation and a public bug bounty program we could reference

---

## Question 2: You found 187 CVEs but only focused on 5. How did you prioritize which ones to fix first?

**Answer:**
We prioritized based on three factors:

1. **CVSS Score** - We focused on Critical (9.0-10.0) and High (7.0-8.9) severity first
2. **Exploitability** - CVEs that required no authentication and had network-based attack vectors were highest priority
3. **Impact** - We prioritized vulnerabilities that could lead to:
   - Remote code execution (RCE)
   - Full system compromise
   - Container escape to host
   - Data exfiltration

The 5 CVEs we highlighted (xz-utils backdoor, OpenSSL, zlib, glibc, PHP) all scored 7.5+ and could lead to complete system takeover. The remaining ~180 CVEs were mostly Low/Medium severity issues in base OS packages with no available fixes or limited attack surface.

---

## Question 3: What is CVSS and how do you calculate those scores?

**Answer:**
CVSS stands for **Common Vulnerability Scoring System**. It's an industry-standard framework for rating vulnerability severity on a 0-10 scale.

The score is calculated based on several factors:
- **Attack Vector** - Network, Adjacent, Local, or Physical
- **Attack Complexity** - Low or High
- **Privileges Required** - None, Low, or High
- **User Interaction** - None or Required
- **Scope** - Changed or Unchanged
- **Impact** - Confidentiality, Integrity, Availability (each rated None/Low/High)

For example, CVE-2024-3094 (xz-utils backdoor) scored 10.0 because:
- Attack Vector: Network (remote)
- Attack Complexity: Low (easy to exploit)
- Privileges Required: None (no login needed)
- User Interaction: None (victim doesn't need to do anything)
- Impact: Complete (full system compromise)

We used the NVD (National Vulnerability Database) for official CVSS scores.

---

## Question 4: You mentioned the XZ backdoor. Can you explain how a supply chain attack like that actually works?

**Answer:**
The XZ backdoor (CVE-2024-3094) was a sophisticated supply chain attack discovered in March 2024:

1. **The Setup** - A malicious actor spent 2+ years building trust as a maintainer of xz-utils, a compression library used by almost every Linux system

2. **The Injection** - They inserted obfuscated malicious code into the build process (not the source code directly, making it harder to detect)

3. **The Payload** - The backdoor hooked into OpenSSH's authentication process. When an attacker sent a specially crafted request, it bypassed all authentication and granted root access

4. **The Discovery** - A Microsoft engineer noticed SSH was running 500ms slower and investigated, discovering the backdoor just before it shipped in major Linux distributions

**Why it matters for our project:** This CVE was present in our Nextcloud container's Debian base image. If exploited, an attacker with network access to SSH could have gained root access with zero credentials.

---

## Question 5: What's the difference between the tools you used - Trivy, ZAP, Burp Suite, and Nmap?

**Answer:**
Each tool serves a different purpose:

| Tool | Type | What It Does |
|------|------|--------------|
| **Nmap** | Network Scanner | Discovers open ports and services - tells us what's exposed to the network |
| **Trivy** | Container Scanner | Scans Docker images for known CVEs in installed packages and libraries |
| **OWASP ZAP** | Web App Scanner | Automated testing for web vulnerabilities (XSS, CSRF, headers, etc.) |
| **Burp Suite** | Proxy/Manual Testing | Intercepts HTTP traffic so we can manually test authentication, sessions, and inject payloads |

**How they worked together:**
1. Nmap told us port 8080 was exposed
2. ZAP crawled the web application and ran 67 automated security checks
3. Burp Suite let us manually test things ZAP couldn't (like brute-force timing, CSRF token manipulation)
4. Trivy found the deep CVEs in system libraries that web scanners can't see

---

## Question 6: What does "container hardening" actually mean? What did you change?

**Answer:**
Container hardening means reducing the attack surface and limiting what a container can do if compromised. We applied several controls:

**1. Dropped Capabilities (~70% reduction)**
- Default Docker containers have 14+ Linux capabilities
- We dropped all and only added back the minimum needed (4-5 per container)
- Example: Removed `CAP_NET_RAW` which could be used for packet sniffing

**2. No-New-Privileges**
- Prevents processes inside the container from gaining additional privileges
- Blocks exploits that try to escalate from www-data to root

**3. Read-Only Filesystem (nginx)**
- The proxy container's filesystem is read-only
- Even if compromised, attackers can't write malware or modify configs

**4. Resource Limits**
- Set CPU and memory limits on all containers
- Prevents denial-of-service attacks from consuming all host resources

**5. Non-Root User (nginx)**
- Nginx runs as user 101:101 instead of root
- Limits damage if the container is compromised

---

## Question 7: You said you reduced CVEs by 63%. Why couldn't you get to zero?

**Answer:**
Getting to zero CVEs is essentially impossible for a real-world application. Here's why:

**1. Unfixed Upstream Issues**
- Some CVEs in base OS packages (Debian, Ubuntu) have no patches available yet
- We can't fix what the maintainers haven't fixed

**2. False Positives / Limited Impact**
- Some CVEs are in libraries that exist but aren't actually used by our application
- Example: BusyBox CVEs in nginx require local shell access, which attackers wouldn't have

**3. Acceptable Risk**
- The remaining 749 CVEs are mostly Low severity
- 47 HIGH CVEs remain but require specific conditions to exploit
- Zero CRITICAL CVEs remain - that's the important metric

**4. Trade-offs**
- We could use distroless/minimal images to reduce CVEs further
- But that would break functionality and make debugging harder
- Security is about risk management, not perfection

---

## Question 8: Did you find any vulnerabilities in Nextcloud itself, or just in the underlying libraries?

**Answer:**
We found issues at multiple layers:

**Application Layer (Nextcloud code):**
- ZAP found a HIGH severity "Vulnerable JS Library" in Nextcloud's bundled JavaScript
- CSP (Content Security Policy) configuration had medium-severity gaps
- These are Nextcloud-specific issues

**Configuration Layer:**
- Plaintext secrets in config.php (passwordsalt, database credentials)
- Server headers leaking Apache/PHP version information
- Missing security headers (HSTS initially missing on port 8080)

**Infrastructure Layer (Libraries/OS):**
- The 5 critical CVEs were all in system libraries (xz-utils, OpenSSL, zlib, glibc, PHP)
- These affect ANY application running on that base image, not just Nextcloud

**What Nextcloud did RIGHT:**
- Strong password policy (10+ chars, blocks top 100k common passwords)
- Effective brute-force protection (rate limiting after ~9 attempts)
- Proper session cookie security (HttpOnly, Secure, SameSite flags)
- CSRF token validation on all state-changing requests
- XSS protection via output encoding

---

## Question 9: If this were a real production deployment, what else would you recommend?

**Answer:**
Our lab environment was intentionally simplified. For production, we'd recommend:

**Immediate Additions:**
1. **Web Application Firewall (WAF)** - Block common attacks before they reach Nextcloud
2. **Valid TLS Certificates** - Replace self-signed certs with Let's Encrypt
3. **Remove Port 8080** - Only expose HTTPS (443), not direct HTTP
4. **Enable 2FA** - Enforce TOTP-based two-factor authentication for all users

**Infrastructure Changes:**
5. **Network Segmentation** - Database on isolated network, not accessible from web tier
6. **Secrets Management** - Use HashiCorp Vault or Docker secrets instead of .env files
7. **Centralized Logging** - Ship logs to SIEM for security monitoring
8. **Automated Scanning** - Integrate Trivy/ZAP into CI/CD pipeline

**Ongoing Operations:**
9. **Patch Schedule** - Monthly security updates with testing
10. **Backup & Recovery** - Tested backup restoration procedures
11. **Incident Response Plan** - Documented procedures for security events
12. **Security Monitoring** - Alerts for suspicious login attempts, file access patterns

---

## Question 10: What was the most surprising or interesting thing you learned from this project?

**Answer:**
*(Each team member can personalize this, but here are good options:)*

**Option A - The XZ Backdoor:**
"The xz-utils backdoor was eye-opening. A single malicious maintainer spent two years building trust, then inserted a backdoor that almost shipped in every major Linux distro. It shows that supply chain security is a real threat, and even 'trusted' open source packages need verification."

**Option B - Defense in Depth:**
"I was surprised how many security controls Nextcloud already had built in. Password policies, rate limiting, CSRF tokens, cookie flags - all working correctly. The vulnerabilities we found were mostly in the underlying infrastructure, not the application itself. It reinforced that security is about layers."

**Option C - The Gap Between Scanning and Exploiting:**
"Trivy found 187 CVEs, which sounds terrifying. But when we actually analyzed them, most were unexploitable in our context. It taught me that vulnerability counts are misleading - what matters is exploitability and impact, not raw numbers."

**Option D - Container Hardening Impact:**
"I didn't realize how insecure default Docker containers are. They run as root with 14+ capabilities by default. Just adding a few lines to docker-compose.yml (no-new-privileges, cap_drop, resource limits) dramatically improved our security posture. It's low effort, high impact."

---

## Bonus: Quick Facts for Rapid-Fire Questions

| Question | Answer |
|----------|--------|
| How many total CVEs before remediation? | 2,034 |
| How many after? | 749 (63% reduction) |
| How many CRITICAL CVEs eliminated? | 21 → 0 (100%) |
| What version of Nextcloud? | Upgraded from 29 (EOL) to 30 |
| What database? | MariaDB 11.8.5 |
| What web server? | Apache (in Nextcloud container) + Nginx reverse proxy |
| What scanning tools? | Trivy, OWASP ZAP, Burp Suite, Nmap |
| What hardening standard? | CIS Docker Benchmark |
| Brute-force lockout threshold? | ~9 failed attempts |
| Password minimum length? | 10 characters |

---

*Document prepared for Team 7 presentation Q&A session*
