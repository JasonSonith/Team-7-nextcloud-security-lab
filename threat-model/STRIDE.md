# STRIDE — Nextcloud Lab (Team 7)

Scope: Browser (user/admin), Kali proxy, App (Nextcloud), DB (MariaDB). Trust boundaries: host↔VM, VM↔Docker network, app↔db. DoS remains out of scope.

Evidence rule: For each test capture tool name, version, config, raw output. Name files `YYYYMMDD-HHMM_stride-<id>_<short>.ext`.

---

## Browser (User/Admin workstation)

**S — Spoofing**

* Risk: Weak password policy permits easily guessed passwords.
* Tests:

  1. Attempt weak passwords on user creation and password change. Record acceptance criteria.
  2. Brute-force simulation with lockout check: Burp Intruder against `/login` with `Sec-RateLimit` observation. Stop at 50 requests.

**T — Tampering**

* Risk: Session token theft via missing `HttpOnly`/`Secure`/`SameSite` flags or XSS sinks.
* Tests:

  1. Inspect cookies after login. Verify flags and `SameSite` behavior using DevTools + `document.cookie` access attempt.
  2. Reflective XSS probe in filename and share note fields. Confirm non-execution in DOM.

**R — Repudiation**

* Risk: Login audit gaps for failed logins and password changes.
* Tests:

  1. Generate failed and successful logins. Check Admin → Logs and server log files for entries with user, IP, timestamp.
  2. Change password and validate audit trail contains actor and target.

**I — Information Disclosure**

* Risk: CSRF token exposure or predictable token reuse.
* Tests:

  1. Confirm CSRF token is per-session and not logged or exposed in URL. Review requests with Burp.
  2. Reuse CSRF token across sessions. Expect rejection.

**D — Denial of Service**

* Out of scope.

**E — Elevation of Privilege**

* Risk: None in browser alone beyond phishing. N/A for lab.

---

## Kali Proxy (Intercepting proxy on Kali)

**S — Spoofing**

* Risk: Accepting fake TLS certificates leads to testing with insecure assumptions.
* Tests:

  1. Validate CA install and confirm leaf cert matches expected CN and pin fingerprint for the reverse proxy/app.
  2. Attempt MITM of HTTPS without proxy certificate trusted. Expect browser hard fail.

**T — Tampering**

* Risk: MITM over HTTP paths if any downgrade occurs.
* Tests:

  1. Crawl for `http://` references. Verify 301/302 to HTTPS and HSTS present.
  2. Modify sensitive parameters in-flight with Burp Repeater. Confirm server-side validation rejects tampering.

**R — Repudiation**

* Risk: Burp/ZAP logs mishandled or lost.
* Tests:

  1. Export history to `dynamic-testing/` and verify reproducibility by teammate.
  2. Check timestamps and request IDs are consistent across exports.

**I — Information Disclosure**

* Risk: Proxy captures credentials and tokens without storage controls.
* Tests:

  1. Search proxy history for `Authorization`, `Set-Cookie`. Ensure exports are redacted before commit.
  2. Verify repo `.gitignore` excludes raw proxy state files if sensitive.

**D — Denial of Service**

* Risk: Fuzz-spam by accident.
* Tests:

  1. Set Intruder/ffuf/wfuzz throttles. Confirm rate limits not exceeded during tests.

**E — Elevation of Privilege**

* Risk: Request manipulation to escalate roles.
* Tests:

  1. Flip user IDs or role flags in JSON bodies. Expect 403 and no stat
