# Week 3 Findings — Auth & Session Security

**Date:** 2025-11-08
**Tester:** Team 7
**Target:** Nextcloud 29-apache at 10.0.0.47
**Testing Platform:** Kali Linux

---

## 1. Password Strength Testing

**Objective:** Test if Nextcloud accepts weak passwords

**Test Date:** 2025-11-08
**Evidence:** `docs/evidence/week-3/password-strength-10char-minimum.png`

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

**Test Date:**
**Tool:** Burp Suite Intruder
**Evidence:**

### Test Configuration

- Target endpoint:
- Number of attempts: 50
- Credentials used:

### Test Results

**Lockout triggered:** [YES / NO]
**Lockout threshold:**
**Lockout duration:**
**Rate-limit headers observed:**

### Findings

**Status:** [PASS / FAIL]

**Description:**

**Risk Rating:** [Low / Medium / High / Critical]

**CVSS Score:**

**Recommendation:**

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

All evidence stored in: `docs/evidence/week-3/`

- Password strength tests:
- Brute-force tests:
- Cookie analysis:
- CSRF tests:
- XSS tests:
- App audit:
- ZAP scan report:
