# Week 3 Findings — Auth & Session Security

**Date:** 2025-11-08
**Tester:** Team 7
**Target:** Nextcloud 29-apache at 10.0.0.47
**Testing Platform:** Kali Linux

---

## 1. Password Strength Testing

**Objective:** Test if Nextcloud accepts weak passwords

**Test Date:** 2025-11-08
**Evidence:**
- `docs/evidence/week3/password-testing/password-strength-common-password-check.png`
- `docs/evidence/week3/password-testing/password-length-cmmon-password-check.png.png`

### Test Results

| Password Tested | Result (Accept/Reject) | Error Message                                         | Screenshot                                  |
| --------------- | ---------------------- | ----------------------------------------------------- | ------------------------------------------- |
| 123456          | REJECTED               | Password must be at least 10 characters               | password-strength-10char-minimum.png        |
| password123     | REJECTED               | Password is among 100000 most commonly used passwords | password-strength-common-password-check.png |

### Findings

**Status:** PASS (Strong Security Controls Present)

**Description:**
Nextcloud enforces TWO layers of password security:

1. **Minimum Length Policy (10 characters)**: All short passwords (123456, password, abc, qwerty, admin123) were rejected with a clear error message. This exceeds NIST SP 800-63B recommendations for minimum password length (8 characters).

2. **Common Password Blacklist**: Even when a password meets the length requirement, Nextcloud checks it against a database of the top 100,000 most commonly used passwords. For example, "password123" (11 characters) was rejected with the message "password is among 100000 most commonly used passwords". This prevents dictionary attacks using predictable passwords that are technically long enough but still easily guessable.

This dual-layer approach effectively prevents users from creating weak credentials, even when those credentials appear to meet basic length requirements. This is an advanced security control comparable to integration with breach databases like Have I Been Pwned.

**Risk Rating:** Low (No vulnerability identified - this is a positive security control)

**CVSS Score:** N/A (Not a vulnerability)

**Recommendation:**
No action required. The current password policy demonstrates excellent security practices with both length enforcement and common password checking. Consider also implementing:
- Multi-factor authentication (MFA) enforcement for administrative accounts
- Password expiration policies for high-privilege accounts
- User education on creating strong, unique passwords

---

## 2. Brute-Force & Lockout Protection

**Objective:** Test if Nextcloud locks accounts after failed login attempts

**Test Date:** 2025-11-08
**Tool:** Burp Suite Intruder (Community Edition)
**Evidence:**
- `docs/evidence/week3/brute-force-test/brute-force-result.png` - Attack results showing status code transition
- `docs/evidence/week3/brute-force-test/brute-force-error-429.png` - Rate limit error message
- `docs/evidence/week3/brute-force-test/brute-force-wordlist-payload.png` - Intruder payload configuration
- `docs/evidence/week3/brute-force-test/successful-login-after-brute-force.png` - Login success after attack
- `docs/evidence/week3/brute-force-test/TestBruteForce-creds.txt` - Test account credentials
- `docs/evidence/week3/brute-force-test/testbruteforce-acc-creation.png` - Test account creation

### Test Configuration

- **Target endpoint:** `http://10.0.0.47:8080/index.php` (POST request)
- **Number of attempts:** 25 failed login attempts
- **Credentials used:** Username: `testbruteforce`, Passwords: 25 intentionally wrong passwords (wrongpass1-20, admin123, password, 12345678, letmein, qwerty123)
- **Attack type:** Burp Intruder Sniper mode, targeting password parameter only
- **Throttling:** Default Burp Community Edition throttling applied

### Test Results

**Rate limiting triggered:** YES 

**Rate limit threshold:** ~9 failed login attempts (requests 0-8 showed status 303, requests 9-25 showed status 429)

**Lockout type:** Temporary IP-based rate limiting (not permanent account lockout)

**Lockout duration:** Temporary - correct password still works during rate limit period

**Rate-limit headers observed:** HTTP 429 "Too Many Requests" status code

**Error message:** "Too many requests - There were too many requests from your network. Retry later or contact your administrator if this is an error."

**Response analysis:**
- Requests 0-8: Status code 303 (redirect), Length ~923-925 bytes, Error: "Wrong login or password"
- Requests 9-25: Status code 429, Length 12879 bytes (significantly larger), Error: "Too many requests"

### Findings

**Status:** PASS  (Strong Security Controls Present)

**Description:**

Nextcloud implements robust brute-force protection through **IP-based rate limiting**. After approximately 9 consecutive failed login attempts, the system transitions from normal authentication failure responses (HTTP 303 with "Wrong login or password") to rate limiting responses (HTTP 429 with "Too many requests").

**Key Security Features Observed:**
1. **Automatic Detection**: The system automatically detects rapid repeated failed login attempts without manual intervention
2. **Clear Error Messaging**: Users receive clear feedback about why access is denied ("Too many requests from your network")
3. **Legitimate User Protection**: The correct password remains functional during rate limiting, preventing complete lockout of legitimate users who may have forgotten their password
4. **Network-Level Protection**: Rate limiting appears to be IP-based, protecting against distributed attacks from a single source

**Attack Mitigation:**
This implementation effectively defeats automated brute-force attacks by:
- Slowing down attack velocity dramatically after the threshold
- Making password enumeration attacks impractical due to time constraints
- Providing clear deterrent messaging to potential attackers
- Preserving service availability for legitimate users

The rate limiting approach is superior to permanent account lockout because it prevents denial-of-service attacks where attackers intentionally lock out legitimate users.

**Risk Rating:** Low (No vulnerability identified - this is a positive security control)

**CVSS Score:** N/A (Not a vulnerability)

**Recommendation:**

No action required. The current brute-force protection demonstrates excellent security practices. The rate limiting threshold of ~9 attempts is appropriate and aligns with industry best practices (OWASP recommends 5-10 attempts).

**Optional enhancements to consider:**
- Implement CAPTCHA challenge after 3-5 failed attempts (before rate limiting) to distinguish humans from bots
- Log all rate-limited attempts for security monitoring and incident response
- Consider implementing exponential backoff (increasing delay after each failed attempt) for more sophisticated protection
- Add administrator notifications when rate limiting is frequently triggered from specific IPs
- Integrate with fail2ban or similar tools for automatic IP blocking at the firewall level after repeated violations

---

## 3. Session Cookie Security

**Objective:** Verify session cookies have proper security flags

**Test Date:**
**Evidence:**

### Cookie Analysis

| Cookie Name | HttpOnly | Secure | SameSite | Expiration |
|-------------|----------|--------|----------|------------|
|             |          |        |          |            |

### JavaScript Access Test

**document.cookie test result:**

### Findings

**Status:** [PASS / FAIL]

**Description:**

**Risk Rating:** [Low / Medium / High / Critical]

**CVSS Score:**

**Recommendation:**

---

## 4. CSRF Token Validation

**Objective:** Test Cross-Site Request Forgery protections

**Test Date:**
**Tool:** Burp Suite Repeater
**Evidence:**

### Test Cases

1. **Request without CSRF token:**
   - Result:
   - Response code:

2. **Request with invalid CSRF token:**
   - Result:
   - Response code:

3. **Request with token from different session:**
   - Result:
   - Response code:

### Findings

**Status:** [PASS / FAIL]

**Description:**

**Risk Rating:** [Low / Medium / High / Critical]

**CVSS Score:**

**Recommendation:**

---

## 5. XSS Testing

**Objective:** Test for Cross-Site Scripting vulnerabilities

**Test Date:**
**Evidence:**

### Test Locations

| Location Tested | Payload | Result | Screenshot |
|----------------|---------|--------|------------|
| Filename       | `<script>alert('XSS')</script>` | | |
| Share note     | `<img src=x onerror=alert('XSS')>` | | |
| Profile field  | `<svg onload=alert('XSS')>` | | |

### Findings

**Status:** [PASS / FAIL]

**Description:**

**Risk Rating:** [Low / Medium / High / Critical]

**CVSS Score:**

**Recommendation:**

---

## 6. Nextcloud Apps Audit

**Objective:** Identify and disable unnecessary Nextcloud apps

**Test Date:**
**Evidence:**

### Installed Apps

| App Name | Version | Enabled | Purpose | Action Taken |
|----------|---------|---------|---------|--------------|
|          |         |         |         |              |

### Apps Disabled

-

### Findings

**Status:** [PASS / FAIL]

**Description:**

**Risk Rating:** [Low / Medium / High / Critical]

**Recommendation:**

---

## 7. ZAP Baseline Scan

**Objective:** Automated vulnerability scan of Nextcloud application

**Test Date:**
**Tool:** OWASP ZAP
**Evidence:**

### Scan Configuration

- Target URL:
- Scan type: Baseline
- Duration:

### Findings Summary

| Risk Level | Count | Examples |
|-----------|-------|----------|
| High      |       |          |
| Medium    |       |          |
| Low       |       |          |
| Info      |       |          |

### Key Vulnerabilities Identified

1.

### Findings

**Status:** [PASS / FAIL]

**Description:**

**Risk Rating:** [Low / Medium / High / Critical]

**Recommendation:**

---

## Summary

### Total Findings

- **Critical:**
- **High:**
- **Medium:**
- **Low:**
- **Informational:**

### Top Risks

1.
2.
3.

### Recommended Actions

1.
2.
3.

---

## Evidence Index

All evidence stored in: `docs/evidence/week3/`

**Password strength tests:**
- `docs/evidence/week3/password-testing/password-strength-common-password-check.png`
- `docs/evidence/week3/password-testing/password-length-cmmon-password-check.png.png`

**Brute-force tests:**
- `docs/evidence/week3/brute-force-test/brute-force-result.png`
- `docs/evidence/week3/brute-force-test/brute-force-error-429.png`
- `docs/evidence/week3/brute-force-test/brute-force-wordlist-payload.png`
- `docs/evidence/week3/brute-force-test/successful-login-after-brute-force.png`
- `docs/evidence/week3/brute-force-test/TestBruteForce-creds.txt`
- `docs/evidence/week3/brute-force-test/testbruteforce-acc-creation.png`
- `docs/evidence/week3/brute-force-test/brute-force-wordlist.txt`

**Cookie analysis:** (Pending)

**CSRF tests:** (Pending)

**XSS tests:** (Pending)

**App audit:** (Pending)

**ZAP scan report:** (Pending)
